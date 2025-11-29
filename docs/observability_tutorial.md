# 🌟 ADK Observability — Full Tutorial

### *A very simple guide to understand what we built together*

This tutorial covers:

1. **What is an ADK Plugin?**
2. **What are ADK callbacks?**
3. **What is a Plugin Manager?**
4. **The folder structure we created (and why)**
5. **Your ADKObservabilityPlugin explained line-by-line**
6. **How ADK triggers your callback functions**
7. **Why some messages show in console but not in logs**
8. **How the entire observability pipeline works end-to-end**

---

# 1️⃣ What is an ADK Plugin?

A plugin in Google ADK is like a **listener** or a **hook** that ADK calls automatically when something important happens.

Examples:

* When an agent starts
* When an agent finishes
* When LLM request is sent
* When LLM responds
* When a tool is about to run
* When tool finishes
* When an error happens

You don’t manually call plugins.
**ADK calls them for you.**

---

# 2️⃣ What are ADK callbacks?

Callbacks are **predefined function names** ADK looks for:

| Callback                  | Meaning                     |
| ------------------------- | --------------------------- |
| `before_agent_callback`   | Called before an agent runs |
| `after_agent_callback`    | Called after agent finishes |
| `before_model_callback`   | Before LLM call             |
| `after_model_callback`    | After LLM call              |
| `before_tool_callback`    | Before tool runs            |
| `after_tool_callback`     | After tool runs             |
| `on_model_error_callback` | If LLM raises error         |

If your plugin defines these methods, ADK will call them automatically.

---

# 3️⃣ What is PluginManager?

`PluginManager` is ADK’s internal engine that:

* stores all registered plugins
* runs the right callback at the right moment
* passes arguments to your callback methods
* handles errors inside plugins

You never create PluginManager yourself.

---

# 4️⃣ Folder Structure (Why We Created It)

```
app
├── observability
│   ├── __init__.py
│   ├── plugins
│   │   ├── adk_observability_plugin.py   👈 Your custom plugin class
│   ├── logging
│   │   ├── logging_config.py            👈 Local/production logging logic
│   ├── metrics
│   │   ├── metrics_store.py             👈 Future extension
│   └── tracing
│       ├── trace_utils.py               👈 Future extension
```

This structure allows:

* **plugins/** → ADK Plugin system
* **logging/** → Python loggers
* **tracing/** → OpenTelemetry future usage
* **metrics/** → For Prometheus or Azure Monitor

You now have a **clean, enterprise-grade observability layer**.

---

# 5️⃣ Understanding Your Plugin (Line-by-line)

Here is the simplified version of your plugin:

```python
class ADKObservabilityPlugin(BasePlugin):
    name = "ADKObservabilityPlugin"

    async def before_agent_callback(self, agent, callback_context):
        logger.info({
            "event": "agent_start",
            "agent": agent.name,
            "trace_id": callback_context.trace_id,
            "input": callback_context.input
        })
```

Meaning:

* ADK runs this **before any agent starts**
* You log an event
* Your logger sends it to console/file depending on env

Same pattern continues:

### Before LLM Call

```python
async def before_model_callback(self, callback_context, llm_request):
    logger.info({
        "event": "llm_request",
        "trace_id": callback_context.trace_id,
        "model": llm_request.model,
        "prompt": llm_request.prompt
    })
```

### After LLM Call

```python
async def after_model_callback(self, callback_context, llm_response):
    logger.info({
        "event": "llm_response",
        "trace_id": callback_context.trace_id,
        "tokens_used": llm_response.token_usage
    })
```

### After Agent Finishes

```python
async def after_agent_callback(self, agent, callback_context):
    logger.info({
        "event": "agent_end",
        "agent": agent.name,
        "trace_id": callback_context.trace_id,
        "output": callback_context.output
    })
```

---

# 6️⃣ How ADK Triggers Your Plugin

Let’s follow the actual call path.

---

## 👉 Step A: User clicks “Run” in ADK Studio UI

ADK calls:

```
Runner.run_async()
```

Inside that method:

```
run_before_run_callback()
```

---

## 👉 Step B: Before Running an Agent

ADK calls:

```
plugin.before_agent_callback(agent, callback_context)
```

Your plugin logs:

```
{"event": "agent_start", "agent": "...", "trace_id": "...", "input": ...}
```

---

## 👉 Step C: When LLM request is made

ADK calls:

```
plugin.before_model_callback(callback_context, llm_request)
```

Your plugin logs:

```
{"event": "llm_request", "model": "...", ...}
```

---

## 👉 Step D: After LLM responds

ADK calls:

```
plugin.after_model_callback(callback_context, llm_response)
```

Your plugin logs:

```
{"event": "llm_response", ...}
```

---

## 👉 Step E: When tool is about to run

```
plugin.before_tool_callback(tool, tool_args, tool_context)
```

---

## 👉 Step F: After tool finishes

```
plugin.after_tool_callback(tool, tool_args, tool_context, result)
```

---

## 👉 Step G: When agent completes

```
plugin.after_agent_callback(agent, callback_context)
```

---

## 👉 Step H: Finish run

ADK calls:

```
plugin.after_run_callback()
```

---

# 7️⃣ Why your console prints "Video Agent Instruction" but logs do not?

Because this line:

```python
print("Video Agent Instruction:--------", video_agent_instruction)
```

goes to **stdout**
NOT through your logger.

Your logger only captures:

```python
logger.info(...)
logger.warning(...)
logger.error(...)
```

If you want that instruction to appear in logs:

Replace:

```python
print("Video Agent Instruction:--------", video_agent_instruction)
```

With:

```python
logger.info(f"Video Agent Instruction:\n{video_agent_instruction}")
```

Important rule:

➤ **Everything printed using print() will appear in Azure Container Logs, but NOT in your app.log file.**

---

# 8️⃣ Full Workflow Diagram (Super Simple)

```
[User Runs Agent]
        |
        v
[ADK Runner]
        |
        v
[PluginManager] ------------------------
        |                               |
        v                               |
[Your Plugin Callbacks]                 |
   - before_agent_callback              |
   - before_model_callback              |
   - after_model_callback               |
   - before_tool_callback               |
   - after_tool_callback                |
   - after_agent_callback               |
                                        |
            (each logs event) <---------
```

Each callback writes logs → logging system →
Console + (if development) log file.

---

# ⭐ FINAL SUMMARY

You have successfully:

### ✔ Implemented a **production-grade observability system**

### ✔ Using ADK plugin callbacks

### ✔ With modular folder structure

### ✔ Logging all important events:

* Agent start
* Agent end
* LLM request
* LLM response
* Tool execution

### ✔ Sending logs to both file (local) and console (Azure)

### ✔ Allowing Azure Log Analytics to collect everything automatically

This is the **exact architecture used by enterprise AI/ML platforms**.



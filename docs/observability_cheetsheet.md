# 📘 **ADK Observability Cheatsheet**

### *Your quick guide to plugins, callbacks, logging, and workflow*

---

# 1️⃣ ADK Plugin System — At a Glance

```
ADK → PluginManager → YourPluginCallbacks → Logs
```

A plugin is a small class that ADK automatically calls during:

* Agent lifecycle
* LLM requests/responses
* Tools execution
* Errors

You never call plugins yourself.
ADK triggers them automatically.

---

# 2️⃣ Folder Structure Used in Your Project

```
app
└── observability
    ├── plugins/
    │   └── adk_observability_plugin.py   ← Your ADK plugin
    ├── logging/
    │   └── logging_config.py             ← Logging setup
    ├── metrics/                          ← (future use)
    └── tracing/                          ← (future use)
```

---

# 3️⃣ Minimal ADK Plugin Structure

```python
from google.adk.plugins.base_plugin import BasePlugin
from app.observability import get_logger

logger = get_logger(__name__)

class ADKObservabilityPlugin(BasePlugin):
    name = "ADKObservabilityPlugin"

    async def before_agent_callback(self, agent, callback_context):
        logger.info({
            "event": "agent_start",
            "agent": agent.name,
            "trace_id": callback_context.trace_id,
        })
```

**Important:**
Method names must match ADK’s expected callback names.

---

# 4️⃣ ADK Callback Methods (YOU can implement these)

| Callback                  | When it fires                       |
| ------------------------- | ----------------------------------- |
| `before_agent_callback`   | Before agent starts                 |
| `after_agent_callback`    | After agent finishes                |
| `before_model_callback`   | Before LLM request                  |
| `after_model_callback`    | After LLM response                  |
| `before_tool_callback`    | Just before tool function is called |
| `after_tool_callback`     | After tool completes                |
| `on_model_error_callback` | LLM error                           |
| `on_tool_error_callback`  | Tool error                          |

Arguments passed to each callback come from ADK.

---

# 5️⃣ Logging Setup (Local vs Production)

### Development (your laptop)

✔ Logs go to:

```
logs/app.log
and console
```

### Production (Azure)

✔ Logs go to:

```
console → Container Logs → Log Analytics → Application Insights
```

**Tip:** Azure collects everything written to stdout/stderr.
So your logger must write to console in production mode.

---

# 6️⃣ Your Logging Configuration Rules

```python
environment = settings.app_env

if environment == "production":
    console only
else:
    console + rotating file logs
```

---

# 7️⃣ How Your Plugin Is Registered

You added:

```python
extra_plugins=["app.observability.plugins.adk_observability_plugin.ADKObservabilityPlugin"]
```

ADK loads them automatically.

---

# 8️⃣ Full Execution Flow (Very Simple Diagram)

```
[User clicks RUN]  
       ↓  
ADK Runner  
       ↓  
PluginManager  
       ↓  
[before_agent_callback]  
       ↓  
[before_model_callback]  
       ↓  
[after_model_callback]  
       ↓  
[before_tool_callback]  
       ↓  
[after_tool_callback]  
       ↓  
[after_agent_callback]  
```

Each step → logged to your logger → file/console/Azure.

---

# 9️⃣ Why Some Prints Are Not Logged

* `print()` goes **only** to console.
* `logger.info()` goes to **file + console** (dev)
* `logger.info()` goes to **console only** (Azure)

To store prints in logs → replace:

```python
print("Video Agent Instruction")
```

With:

```python
logger.info("Video Agent Instruction")
```

---

# 🔟 Best Practices

✔ Use structured logs (JSON-like dicts)
✔ Always include `trace_id` and `agent_name`
✔ No heavy logic inside plugin methods
✔ Avoid blocking operations (e.g., no long sleeps)
✔ Ensure plugin never breaks agent flow

---

# 🎯Summary

* ADK plugins are automatic hooks
* You implemented full observability: agent, LLM, tool
* Logs are centralized under `app.observability`
* File logs for development
* Azure Log Analytics for production
* Clean plugin architecture ensures enterprise-ready monitoring

---

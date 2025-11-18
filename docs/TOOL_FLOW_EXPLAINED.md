Below is a clean, detailed, step-by-step **flow explanation**, using the **Math Add Tool** as the example.

📁 `docs/TOOL_FLOW_EXPLAINED.md`

---

# 🧠 MCP Tool Flow Explained — Example: Math Add Tool

This document explains, in simple and complete detail, **how a tool works end-to-end** inside our MCP server.

We trace the flow using the **Math Add Tool** as a real example.

---

# 🔄 High-Level Overview

When an MCP Client (e.g., VSCode, Cursor, JetBrains, custom app) calls a tool:

1. **Client sends an MCP request**
2. **FastMCP receives the request**
3. **Tool function gets invoked**
4. **Tool validates input using Pydantic**
5. **Tool calls service logic**
6. **Service returns structured data (Pydantic Output Model)**
7. **Tool returns output back to FastMCP**
8. **FastMCP sends the response to MCP Client**
9. **Client displays the result to the user**

This is how all tools (math, Google, Bing, weather, etc.) work in our architecture.

---

# 🧩 Architecture Recap

```
MCP Client (VSCode/Cursor)
        ↓
   MCP Protocol
        ↓
FastMCP Server
        ↓
   Tool Layer (tools/)
        ↓
 Service Layer (services/)
        ↓
 Pydantic Models (models/)
        ↓
  Return structured output
```

---

# 🟦 1. User Calls a Tool (from MCP Client)

Example (user types in VSCode):

> “Add 5 and 7”

The AI agent recognizes this as a tool call and sends the tool request:

```json
{
  "tool": "add_tool",
  "input": { "a": 5, "b": 7 }
}
```

FastMCP receives this request.

---

# 🟦 2. FastMCP Looks Up the Tool

In `app/server/routes.py`:

```python
from app.tools.math_tools import add_tool

def register_tools(mcp: FastMCP):
    mcp.add_tool(add_tool)
```

This tells the MCP server:

> “If someone calls **add_tool**, execute the Python function `add_tool()`.”

---

# 🟦 3. MCP Server Executes Tool Function

**File:** `app/tools/math_tools.py`

```python
def add_tool(input: MathAddInput) -> MathAddOutput:
    return add_numbers(input)
```

Two big things happen here:

### ✔ Pydantic Validation

Before the function even runs, FastMCP uses Pydantic to validate input:

* Is `a` an integer?
* Is `b` an integer?
* Missing fields?
* Wrong types?

If anything is invalid → FastMCP returns a **400 error** automatically.

### ✔ Validated Input Model

The `input` parameter is an instance of:

```python
MathAddInput(a=5, b=7)
```

Now the tool is guaranteed to receive clean data.

---

# 🟦 4. Tool Calls the Service Layer

**Inside the tool function:**

```python
return add_numbers(input)
```

We use a **service layer** so tool functions stay:

* clean
* reusable
* testable
* maintainable

---

# 🟦 5. Service Logic Executes

**File:** `app/services/math_service.py`

```python
def add_numbers(input: MathAddInput) -> MathAddOutput:
    return MathAddOutput(result=input.a + input.b)
```

This step does the actual work.

### ✔ Takes structured input (`MathAddInput`)

### ✔ Performs core logic:

```python
input.a + input.b
```

### ✔ Returns structured output (`MathAddOutput`)

The service layer **does not** know anything about MCP — only business logic.

---

# 🟦 6. Pydantic Output Model Created

**File:** `app/models/math_models.py`

```python
class MathAddOutput(BaseModel):
    result: int
```

The service constructs an instance:

```python
MathAddOutput(result=12)
```

This ensures:

* type safety
* schema generation
* AI-friendly structured output
* clean API response

---

# 🟦 7. Tool Returns Output to MCP Server

Tool → FastMCP receives:

```python
MathAddOutput(result=12)
```

FastMCP automatically converts the Pydantic model → JSON:

```json
{
  "result": 12
}
```

---

# 🟦 8. MCP Server Sends Back Response to Client

FastMCP sends JSON back to the MCP client via standard MCP response format.

---

# 🟦 9. MCP Client Displays Response

In Cursor, VSCode, or JetBrains, the AI responds:

> **"The result is 12."**

Or if using the raw tool output:

```json
{
  "result": 12
}
```

---

# 🧠 Complete Flow Diagram (Simplified)

```
    MCP Client
        ↓  tool call: add_tool {a:5, b:7}
    FastMCP Receives Request
        ↓
 Validates Input (Pydantic)
        ↓
 Calls add_tool() from app/tools
        ↓
 Tool calls add_numbers() in services/
        ↓
 Service returns MathAddOutput(result=12)
        ↓
 Tool returns output to FastMCP
        ↓
 FastMCP → MCP Response
        ↓
   Client displays "12"
```

---

# 📝 Summary of Responsibilities

| Layer        | Responsibility                                    |
| ------------ | ------------------------------------------------- |
| **models**   | Input/output validation & schema                  |
| **services** | Business logic (APIs, computation, DB, etc.)      |
| **tools**    | MCP-facing interface; docstrings; Pydantic bridge |
| **routes**   | Tool registration                                 |
| **server**   | MCP server initialization                         |
| **client**   | Sends/receives MCP tool calls                     |

Each layer has exactly *one* job → clean, scalable architecture.
# Agentic AI Video Ad Generator

An agentic-AI based system that generates video advertisements using multi-agent workflows and an MCP-powered video generation backend.

---

## 1. Setup

This project uses **uv** for dependency management and environment creation.

```bash
uv sync
.venv/Scripts/activate.ps1
````

`uv sync` will automatically create the `.venv` folder and install all dependencies.

---

## 2. Run the Project

### Step 1 — Update `app/main.py`

Make sure the following block is **enabled**:

```python
app: FastAPI = get_fast_api_app(
    agents_dir=AGENT_DIR,
    session_service_uri=SESSION_DB_URL,
    allow_origins=["*"],
    lifespan=lifespan_wrapper,
    web=True,
    a2a=True,
    reload_agents=True,
    extra_plugins=[
        "app.observability.plugins.adk_observability_plugin.ADKObservabilityPlugin"
    ]
)
```

And direct FastAPI integration is **disabled**:

```python
# app = FastAPI(
#     ...
# )
```

---

### Step 2 — Start FastAPI

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

*(Adjust path based on your folder, e.g. backend > uvicorn app.main:app)*

---

### Step 3 — Run MCP Server

Run your MCP server (code is in the `mcp` branch) **before** generating videos.

---

## 3. Project Input Format

Sample business requirements used by the system:

1. **Business Name:** BrightFuture Tech Academy
2. **What do you do?** We teach Python and AI to kids, school students, and freshers.
3. **Target Audience:** Kids (10–17), beginners, parents looking for coding classes.
4. **Problem You Solve:** Students do not get practical coding experience needed for real jobs.
5. **What makes you unique?** Hands-on projects, fun learning, job-ready skills.
6. **Tone of Your Brand:** Friendly, youthful, motivating.
7. **Goal of Advertisement:** Increase awareness and get new enrollments.

---


# compliance_server.py

import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types
import uvicorn
from fastapi.responses import FileResponse
import os

load_dotenv()

app = FastAPI(title="Compliance Review Service")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("Missing GOOGLE_API_KEY in .env")


# ------------------------------
# Schema for input
# ------------------------------
class ComplianceInput(BaseModel):
    creative_prompt: str
    business_name: str | None = None
    business_type: str | None = None
    target_audience: str | None = None


# ------------------------------
# Compliance LLM Agent
# ------------------------------
compliance_agent = LlmAgent(
    name="compliance_agent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        api_key=GOOGLE_API_KEY,
    ),
    instruction="""
You are a compliance review agent.

INPUT:
- creative_prompt
- optional business info

OUTPUT (strict JSON):
{
  "approved": true/false,
  "issues": ["..."],
  "suggested_changes": "..."
}
Never return anything except JSON.
""",
)


# ------------------------------
# Main endpoint
# ------------------------------
@app.post("/review")
async def review_compliance(payload: ComplianceInput):

    user_message = types.UserContent(
        parts=[types.Part(text=payload.model_dump_json())]
    )

    final_text = None

    async for event in compliance_agent.run_async(
        user_message=user_message,
    ):
        if event.is_final_response() and event.content:
            for p in event.content.parts:
                if p.text:
                    final_text = p.text

    return {"compliance": final_text}

# -----------------------------------------
# Serve A2A Agent Card (ADK 1.18 requires manual hosting)
# -----------------------------------------
@app.get("/.well-known/agent-card.json", include_in_schema=False)
async def agent_card():
    path = os.path.join(os.getcwd(), ".well-known", "agent-card.json")
    if not os.path.exists(path):
        return {"error": "agent-card.json not found. Expected at /.well-known/agent-card.json"}
    return FileResponse(path, media_type="application/json")

# ------------------------------
# Run server
# ------------------------------
if __name__ == "__main__":
    uvicorn.run("compliance_server:app", host="127.0.0.1", port=8101, reload=True)

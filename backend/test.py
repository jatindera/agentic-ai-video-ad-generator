# test_adk.py  (FINAL verified version for ADK 1.18.0)

from fastapi import FastAPI, HTTPException
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.genai import types
from uuid import uuid4
import uvicorn
import json
import os
from dotenv import load_dotenv

load_dotenv()

# ----------------------------------------------------------------
# 1️⃣  VERIFY GOOGLE API KEY
# ----------------------------------------------------------------
if not os.getenv("GOOGLE_API_KEY"):
    raise Exception("❌ GOOGLE_API_KEY is missing from environment!")

print("GOOGLE_API_KEY loaded ✔️")

# ----------------------------------------------------------------
# 2️⃣  SIMPLE TEST AGENT (no tools)
# ----------------------------------------------------------------
agent = LlmAgent(
    name="test_agent",
    instruction="You are a test agent. Respond very briefly.",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        api_key=os.getenv("GOOGLE_API_KEY")
    )
)

# ----------------------------------------------------------------
# 3️⃣  RUNNER (ADK 1.18.0 style)
#     ⚠️ DO NOT pass session_service manually.
# ----------------------------------------------------------------
APP_NAME = "test_app"

runner = InMemoryRunner(
    agent=agent,
    app_name=APP_NAME
)

# ----------------------------------------------------------------
# 4️⃣  FASTAPI APP
# ----------------------------------------------------------------
app = FastAPI()


@app.post("/run")
async def run_test(payload: dict):
    try:
        session_id = f"s_{uuid4().hex[:8]}"
        user_id = "user_001"

        # ------------------------------------------------------------
        # Create session (MUST use runner.session_service)
        # ------------------------------------------------------------
        await runner.session_service.create_session(
            app_name=APP_NAME,
            user_id=user_id,
            session_id=session_id
        )

        # ------------------------------------------------------------
        # Format input into ADK Content structure
        # ------------------------------------------------------------
        message = types.Content(
            parts=[types.Part(text=json.dumps(payload))]
        )

        final_text = None

        # ------------------------------------------------------------
        # Run agent (ADK 1.18.0 signature)
        # ------------------------------------------------------------
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=message
        ):
            if event.is_final_response() and event.content:
                for part in event.content.parts:
                    if part.text:
                        final_text = part.text

        if not final_text:
            raise HTTPException(500, "Agent produced no output")

        return {"response": final_text}

    except Exception as e:
        raise HTTPException(500, f"ERROR: {str(e)}")


# ----------------------------------------------------------------
# 5️⃣  Run server
# ----------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("test:app", host="127.0.0.1", port=8001, reload=True)

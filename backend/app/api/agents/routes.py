# app/api/agents/routes.py

from fastapi import APIRouter, HTTPException
from uuid import uuid4
import json
from google.genai import types
from google.adk.runners import Runner

from google.adk.sessions import InMemorySessionService, DatabaseSessionService
from app.adk_app import video_app, APP_NAME
from app.core.config import settings
from app.video_pipeline_app.root_agent.sub_agents.business_requirements_agent.schema import RawRequirements
# Observability
from app.observability import configure_logging, get_logger

# Configure logging once
configure_logging()
logger = get_logger(__name__)


router = APIRouter()

DB_URL = f"postgresql+psycopg2://{settings.db_user}:{settings.db_password}@{settings.db_host}:5432/{settings.db_name}"


# Use persistent session in production version.
# session_service = DatabaseSessionService(DB_URL)
# For Hackathon In memory session service
session_service = InMemorySessionService()

# Basic in memory runner
runner = Runner(
    # App contains the information of root agent to run so no need to pass agent in Runner
    app=video_app, #Required for long running tasks / Human in the loop
    session_service=session_service)


@router.post("/generate-video-ad", summary="Run the full video creation pipeline")
async def run_video_pipeline(req: RawRequirements):
    """
    Runs the multi-agent video pipeline.
    """

    try:
        session_id = f"s_{uuid4().hex[:8]}"
        user_id = "user_001" # Get it dynamically in future versions

        # Create ADK session. We don't use session service directly because it needs to come via Runner
        await runner.session_service.create_session(
            app_name=APP_NAME,
            user_id=user_id,
            session_id=session_id
        )

        # Extract the raw string
        raw_requirements = req.raw_requirements

        message = types.Content(
            parts=[types.Part(text=raw_requirements)]
        )

        final_result = None

        # Run orchestrator step-by-step
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=message
        ):

            # 1. Check for errors early
            if event.error_code or event.error_message:
                logger.error(
                    "Agent error (code=%s): %s", 
                    event.error_code, 
                    event.error_message
                )
                raise HTTPException(
                    500,
                    f"Agent error: {event.error_code or ''} {event.error_message or ''}".strip()
                )


            if event.is_final_response():
                # Extract only the TEXT of the final response
                if event.content and event.content.parts:
                    part = event.content.parts[0]
                    if part.text:
                        try:
                            final_result = json.loads(part.text)
                        except Exception:
                            final_result = part.text

        if final_result is None:
            raise HTTPException(500, "Pipeline ended without final response.")

        return final_result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

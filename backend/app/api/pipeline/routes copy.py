# app/api/pipeline/routes.py

from fastapi import APIRouter, HTTPException
from uuid import uuid4
import json
from google.genai import types
from google.adk.runners import Runner

from app.schemas.video_pipeline_schema import VideoPipelineRequest
from google.adk.sessions import InMemorySessionService
from app.adk_app import video_app, APP_NAME



router = APIRouter()


session_service = InMemorySessionService()

runner = Runner(
    app=video_app,
    session_service=session_service
)


@router.post("/run", summary="Run the full video creation pipeline")
async def run_video_pipeline(payload: VideoPipelineRequest):
    """
    Runs the multi-agent video pipeline.
    """

    try:
        session_id = f"s_{uuid4().hex[:8]}"
        user_id = "user_001"

        # Create ADK session
        await runner.session_service.create_session(
            app_name=APP_NAME,
            user_id=user_id,
            session_id=session_id
        )

        # Convert Pydantic → JSON → ADK message
        payload_dict = payload.model_dump()
        message = types.Content(
            parts=[types.Part(text=json.dumps(payload_dict))]
        )

        final_result = None

        # Run orchestrator step-by-step
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=message
        ):

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

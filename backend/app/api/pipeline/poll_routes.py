# app/api/pipeline/poll_routes.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter()

api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)


# ------------------------------
# Request Schema
# ------------------------------
class VideoPollRequest(BaseModel):
    operation_id: str


# ------------------------------
# Polling Endpoint
# ------------------------------
@router.post("/poll", summary="Poll long-running Veo3 video generation")
async def poll_video_generation(req: VideoPollRequest):
    """
    Polls the Veo3 Generation API to check if the video is finished.
    - operation_id is returned by video_agent inside orchestrator flow.
    """

    try:
        operation_id = req.operation_id

        # Fetch current status
        operation = client.operations.get(operation_id)

        # Not done yet → return current status
        if not operation.done:
            return {
                "status": "running",
                "operation_id": operation_id,
                "progress": getattr(operation, "metadata", None)
            }

        # Completed → extract generated video
        if operation.response and operation.response.generated_videos:
            video_obj = operation.response.generated_videos[0]

            return {
                "status": "completed",
                "operation_id": operation_id,
                "video_file_uri": video_obj.video.uri,  # downloadable
                "thumbnail": getattr(video_obj, "thumbnail_uri", None)
            }

        # Done but failed or empty
        return {
            "status": "error",
            "operation_id": operation_id,
            "message": "Operation completed but no video was returned."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

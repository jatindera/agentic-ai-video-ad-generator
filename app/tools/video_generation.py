from app.server import mcp_server
from app.schema.video_generation_schema import FinalPromptSchema
import logging
from app.core.config import settings
from google import genai
import time
from datetime import datetime

logger = logging.getLogger(__name__)

@mcp_server.tool
def start_video_generation(
    veo3_prompt_writer_output: FinalPromptSchema,
) -> dict:

    logger.info("Starting video generation tool...")

    try:
        # Convert structured schema → JSON prompt
        final_prompt = veo3_prompt_writer_output.model_dump_json(indent=2, ensure_ascii=False)

        logger.info("Final Prompt JSON:")
        logger.info(final_prompt)

        client = genai.Client(api_key=settings.google_api_key)

        # ---------------------------------------------------------
        # 1) Call Veo 3.1 preview video generation
        # ---------------------------------------------------------
        operation = client.models.generate_videos(
            model="veo-3.1-fast-generate-preview",
            prompt=final_prompt,
        )

        # ---------------------------------------------------------
        # 2) Synchronous polling
        # ---------------------------------------------------------
        while not operation.done:
            logger.info("⏳ Waiting for Veo video generation to complete...")
            time.sleep(10)
            operation = client.operations.get(operation)

        # ---------------------------------------------------------
        # 3) Save resulting video
        # ---------------------------------------------------------
        video = operation.response.generated_videos[0]
        client.files.download(file=video.video)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        video_name = f"video_{timestamp}.mp4"

        video.video.save(video_name)

        logger.info(f"🎉 Video generation completed. Saved as: {video_name}")

        return {
            "status": "completed",
            "message": f"Video generation completed and saved as {video_name}",
        }

        # return {
        #     "status": "completed",
        #     "message": "Dummy video has been generated. Uncomment code to generate real video",
        # }

    except Exception as e:
        logger.error(f"Video generation failed: {str(e)}")

        return {
            "status": "failed",
            "operation_id": None,
            "message": str(e),
        }

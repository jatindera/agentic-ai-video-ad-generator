# app/agents/video_generator_agent/agent.py

import time
from datetime import datetime

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.adk.tools.tool_context import ToolContext
from google import genai
from google.adk.models.google_llm import Gemini

from app.core.config import settings
from app.utils.retry_config import retry_config
from app.video_pipeline_app.root_agent.sub_agents.veo3_prompt_writer_agent.schema import FinalPromptSchema

# -----------------------------------------------------------------------------------
# Use centralized logger
# -----------------------------------------------------------------------------------
from app.observability import get_logger
logger = get_logger(__name__)

DEFAULT_VIDEO_DURATION = 8


# ===================================================================================
# TOOL: start_video_generation
# ===================================================================================
def start_video_generation(
    veo3_prompt_writer_output: FinalPromptSchema,
) -> dict:

    logger.info("🎬 Starting video generation tool...")

    try:
        # Convert structured schema → JSON prompt
        final_prompt = veo3_prompt_writer_output.model_dump_json(indent=2, ensure_ascii=False)

        logger.info("📝 Final Prompt JSON:")
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

    except Exception as e:
        logger.error(f"❌ Video generation failed: {str(e)}")

        return {
            "status": "failed",
            "operation_id": None,
            "message": str(e),
        }


# ===================================================================================
# AGENT INSTRUCTIONS
# ===================================================================================
video_agent_instruction = """
You are the Video Generator Agent.
Follow these steps exactly:

1. Receive the full {veo3_prompt_writer_output} object.
2. Pass it directly to the function:
       `start_video_generation(veo3_prompt_writer_output)`
3. Return ONLY the tool output exactly as received.

Rules:
- Your response MUST be strictly the raw tool result.
- If the tool raises an error, return that exact error without modification.
"""

# Log the instruction ONCE at startup (not on every call)
logger.info("📄 Loaded Video Generator Agent Instruction:")
logger.info(video_agent_instruction)


# ===================================================================================
# VIDEO GENERATOR AGENT
# ===================================================================================
video_generator_agent = Agent(
    name="video_generator_agent",
    instruction=video_agent_instruction,
    model=Gemini(
        model=settings.google_model_name,
        retry_config=retry_config
    ),
    tools=[FunctionTool(start_video_generation)],
    input_schema=FinalPromptSchema,
)

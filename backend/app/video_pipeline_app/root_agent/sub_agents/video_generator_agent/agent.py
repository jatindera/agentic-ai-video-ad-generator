# app/agents/video_generator_agent/agent.py

from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from google import genai
import time
from app.core.config import settings
from google.adk.tools import FunctionTool
from datetime import datetime
from google.adk.models.google_llm import Gemini
from app.utils.retry_config import retry_config
from app.video_pipeline_app.root_agent.sub_agents.veo3_prompt_writer_agent.schema import FinalPromptSchema

DEFAULT_VIDEO_DURATION = 8


# =====================================================================
# 🚀 UPDATED TOOL — Now expects ONLY final_json_prompt (FIXED)
# =====================================================================
def start_video_generation(veo3_prompt_writer_output: FinalPromptSchema) -> dict:
    """
    Starts the Veo 3.1 video generation pipeline using the structured creative output.

    Process:
      1. Converts the creative output into a final prompt string.
      2. Uses the Gemini Flash Image model ("gemini-2.5-flash-image") to generate a reference image.
      3. Calls Veo 3.1 ("veo-3.1-generate-preview") to generate a video using the prompt and image.
      4. Polls the long-running video operation until completion.
      5. Downloads and saves the generated MP4 video locally.

    Args:
        veo3_prompt_writer_output (dict):
            The creative agent's final JSON prompt containing timeline, scene,
            and stylistic details required for Veo video generation.

    Returns:
        dict: {
            "status": "completed" | "failed",
            "operation_id": str or None,
            "message": str
        }

    Notes:
        - This function performs synchronous polling until the Veo operation finishes.
        - Videos are saved with a timestamp-based filename for uniqueness.
    """
    print("------------Final Prompt--------------")
    try:
        final_prompt = veo3_prompt_writer_output.model_dump_json(indent=2, ensure_ascii=False)
        print(final_prompt)
        print("--------------------------")
    
        
        client = genai.Client(api_key=settings.google_api_key)

        # # 1) Generate image
        # image = client.models.generate_content(
        #     model="gemini-2.5-flash-image",
        #     contents=final_prompt,
        #     config={"response_modalities": ['IMAGE']}
        # )

        # 2) Generate video with Veo 3.1
        operation = client.models.generate_videos(
            model="veo-3.1-fast-generate-preview",
            prompt=final_prompt,
            # image=image.parts[0].as_image(),
        )

        # Synchronous polling
        while not operation.done:
            print("Waiting for video generation to complete...")
            time.sleep(10)
            operation = client.operations.get(operation)

        # Save video
        video = operation.response.generated_videos[0]
        client.files.download(file=video.video)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        video_name =  f"video_{timestamp}.mp4"
        video.video.save(video_name)

        return {
            "status": "completed",
            "message": f"Video generation completed and saved with name. {video_name}"
        }

    except Exception as e:
        return {
            "status": "failed",
            "operation_id": None,
            "message": str(e),
        }



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
print("Video Agent Instruction:--------", video_agent_instruction)

video_generator_agent = Agent(
    name="video_generator_agent",
    instruction=video_agent_instruction,
    model=Gemini(model=settings.google_model_name, retry_config=retry_config),
    tools=[FunctionTool(start_video_generation)],
    input_schema=FinalPromptSchema,
)

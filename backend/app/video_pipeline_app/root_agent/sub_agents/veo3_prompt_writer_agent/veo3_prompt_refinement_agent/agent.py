# path: app/video_pipeline_app/root_agent/sub_agents/veo3_prompt_writer_agent/veo3_prompt_refinement_agent/agent.py

from google.adk.agents import Agent
from app.core.config import settings
from .instructions import veo3_prompt_refinement_agent_instructions
from google.adk.models.google_llm import Gemini
from app.utils.retry_config import retry_config
from google.adk.tools import FunctionTool
from ..schema import FinalPromptSchema

# This is the function that the RefinerAgent will call to exit the loop.
def exit_loop() -> dict:
    """Call this function ONLY when the review status is 'APPROVED', indicating the story is finished and no more changes are needed."""

    return {
        "status": "approved",
        "message": "Veo3 prompt approved by reviewer. Exiting refinement loop."
    }

veo3_prompt_refinement_agent = Agent(
    name="veo3_prompt_refinement_agent",
    instruction=veo3_prompt_refinement_agent_instructions,
    model=Gemini(model=settings.google_model_name, retry_config=retry_config),
    tools=[FunctionTool(exit_loop)],
    output_key="veo3_prompt_writer_output", # IMPORTANT: The key name should match the veo3_prompt_writer_agent's output key  
    output_schema=FinalPromptSchema,
)


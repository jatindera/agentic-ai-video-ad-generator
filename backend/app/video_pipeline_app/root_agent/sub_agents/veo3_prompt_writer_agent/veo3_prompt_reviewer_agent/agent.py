# path: app/video_pipeline_app/root_agent/sub_agents/veo3_prompt_writer_agent/veo3_prompt_reviewer_agent/agent.py

from google.adk.agents import Agent
from app.core.config import settings
from .instructions import veo3_prompt_reviewer_agent_instructions
from google.adk.models.google_llm import Gemini
from app.utils.retry_config import retry_config

veo3_prompt_reviewer_agent = Agent(
    name="veo3_prompt_reviewer_agent",
    instruction=veo3_prompt_reviewer_agent_instructions,
    model=Gemini(model=settings.google_model_name, retry_config=retry_config),
    tools=[],
    output_key="veo3_prompt_reviewer_output",  
)


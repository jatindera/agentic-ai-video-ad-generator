# path: app/video_pipeline_app/root_agent/sub_agents/creative_prompt_agent/agent.py

from google.adk.agents import Agent
from app.core.config import settings
from .instructions import creative_prompt_instructions
from google.adk.models.google_llm import Gemini
from app.utils.retry_config import retry_config

creative_agent = Agent(
    name="creative_agent",
    instruction=creative_prompt_instructions,
    model=Gemini(model=settings.google_model_name, retry_config=retry_config),
    tools=[],
    output_key="creative_output",  
)


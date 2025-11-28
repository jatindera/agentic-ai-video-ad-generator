# path: app/video_pipeline_app/root_agent/sub_agents/domain_search_agent/agent.py

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from app.tools.search_tools import search_similar_examples
from app.tools.example_tools import fetch_examples_by_ids
from app.core.config import settings
from .instructions import domain_search_instructions
from google.adk.models.google_llm import Gemini
from app.utils.retry_config import retry_config
from app.video_pipeline_app.root_agent.sub_agents.business_requirements_agent.schema import BusinessRequirements


domain_search_agent = Agent(
    name="domain_search_agent",
    model=Gemini(model=settings.google_model_name, retry_config=retry_config),
    tools=[FunctionTool(search_similar_examples), FunctionTool(fetch_examples_by_ids)],
    output_key="domain_search_output",
    input_schema=BusinessRequirements,
    instruction=domain_search_instructions
)




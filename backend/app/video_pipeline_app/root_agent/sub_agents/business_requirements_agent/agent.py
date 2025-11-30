# app/video_pipeline_app/business_requirements_agent/agent.py

from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from app.utils.retry_config import retry_config
from app.core.config import settings
from .schema import BusinessRequirements
from .instructions import business_requirements_instructions
# Observability
from app.observability import configure_logging, get_logger

# Configure logging once
configure_logging()
logger = get_logger(__name__)




business_requirements_agent = Agent(
    name="business_requirements_agent",
    model=Gemini(model=settings.google_model_name, retry_config=retry_config),
    instruction=business_requirements_instructions,
    output_schema=BusinessRequirements,
    output_key="business_requirements_output",
)

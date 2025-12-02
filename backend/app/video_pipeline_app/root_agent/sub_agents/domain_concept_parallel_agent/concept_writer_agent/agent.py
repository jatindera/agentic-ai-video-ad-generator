# app/video_pipeline_app/orchestrator_agent/concept_writer_agent/agent.py

from google.adk.agents import Agent, LlmAgent
from app.core.config import settings
from .instructions import concept_writer_instructions
from .schema import ConceptWriterOutput
from google.genai import types
from google.adk.models.google_llm import Gemini
from app.utils.retry_config import retry_config
from app.video_pipeline_app.root_agent.sub_agents.business_requirements_agent.schema import BusinessRequirements
from app.core.config import settings


concept_writer_agent = Agent(
    name="concept_writer_agent",
    model=Gemini(model=settings.google_model_name, retry_config=retry_config),
    output_key="concept_writer_output",
    input_schema=BusinessRequirements,
    output_schema=ConceptWriterOutput,
    generate_content_config=types.GenerateContentConfig(temperature=0.9),  
    instruction=concept_writer_instructions
    
)



    



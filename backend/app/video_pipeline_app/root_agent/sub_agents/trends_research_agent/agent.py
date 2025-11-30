from google.adk.agents import Agent, SequentialAgent
from google.adk.tools import google_search
from app.core.config import settings
from .instructions import trends_query_creator_instructions
# Observability
from app.observability import configure_logging, ADKObservabilityPlugin, get_logger

# Configure logging once
configure_logging()
logger = get_logger(__name__)


trends_query_creator_agent = Agent(
    name="trends_research_agent",
    model=settings.google_model_name,
    instruction=trends_query_creator_instructions,
    output_key="trends_query_creator_output",
)


google_trends_search_agent = Agent(
    name="google_trends_search_agent",
    model=settings.google_model_name,
    instruction="use tool `google_search` and search for {trends_query_creator_output}",
    tools=[google_search],
    output_key="google_trends_search_output",
)

trends_refiner_agent = Agent(
    name = "trends_research_agent",
    model=settings.google_model_name,
    instruction="You will receive {google_trends_search_output}. Your task is to beautify, clean, and summarize the information into 4–6 clear, well-formatted bullet points. Focus on clarity, relevance, and readability; remove noise, repetition, or unnecessary details.",
    output_key="trends_refiner_agent_output"

)

trends_research_agent = SequentialAgent(
    name="trends_research_agent",
    sub_agents=[trends_query_creator_agent, google_trends_search_agent, trends_refiner_agent]
    )

logger.info("trends_research_agent..........")



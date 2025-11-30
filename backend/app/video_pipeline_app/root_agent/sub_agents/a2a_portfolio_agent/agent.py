from google.adk.agents import Agent
from google.adk.agents.remote_a2a_agent import (
    RemoteA2aAgent,
    AGENT_CARD_WELL_KNOWN_PATH,
)
from google.adk.models.google_llm import Gemini
from app.utils.retry_config import retry_config
from app.core.config import settings
from app.observability import configure_logging, get_logger
from google.genai import types
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
import uuid
from google.adk.tools.function_tool import FunctionTool

# Configure logging once
configure_logging()
logger = get_logger(__name__)



# ---------------------------------------------------------------------------
# 🌐 CONNECT TO REMOTE CREATIVE PORTFOLIO AGENT (A2A PROXY)
# ---------------------------------------------------------------------------
remote_portfolio_agent = RemoteA2aAgent(
    name="remote_portfolio_agent",
    description="Remote Portfolio Agent that provides creative services, skills, and portfolio information.",
    # URL where your Creative Portfolio Agent is running
    agent_card=f"http://127.0.0.1:9001{AGENT_CARD_WELL_KNOWN_PATH}",
)

logger.info("✅ Remote Creative Portfolio Agent proxy created!")
logger.info("   Connected to: http://127.0.0.1:9001")
logger.info(f"   Agent card:   http://127.0.0.1:9001{AGENT_CARD_WELL_KNOWN_PATH}")
logger.info("   The main agent can now use this like a local sub-agent!")


# ---------------------------------------------------------------------------
# 🤖 MAIN LLM AGENT (Support Agent for Client Interaction)
# ---------------------------------------------------------------------------
a2a_portfolio_agent = Agent(
    model=Gemini(model=settings.google_model_name, retry_config=retry_config),
    name="a2a_portfolio_agent",
    instruction="""
    You are part of an automated pipeline.

    RULES:
    - ALWAYS call the `remote_portfolio_agent` sub-agent.
    - NEVER answer on your own.
    - ALWAYS pass the entire input to the sub-agent.
    - Return EXACTLY the sub-agent's response.
    """,
    sub_agents=[remote_portfolio_agent],  # A2A sub-agent added here!
)





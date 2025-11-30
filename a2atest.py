from google.genai import types
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
import uuid
from google.adk.tools.function_tool import FunctionTool
from google.adk.agents import Agent
from google.adk.agents.remote_a2a_agent import (
    RemoteA2aAgent,
    AGENT_CARD_WELL_KNOWN_PATH,
)
from google.adk.models.google_llm import Gemini
from dotenv import load_dotenv

load_dotenv("backend\.env")


remote_portfolio_agent = RemoteA2aAgent(
    name="remote_portfolio_agent",
    description="Remote Portfolio Agent that provides creative services, skills, and portfolio information.",
    # URL where your Creative Portfolio Agent is running
    agent_card=f"http://127.0.0.1:9001{AGENT_CARD_WELL_KNOWN_PATH}",
)


a2a_portfolio_agent = Agent(
    model=Gemini(model="gemini-2.5-flash"),
    name="a2a_portfolio_agent",
    instruction="""
    When user asks about creative portfolio:
    - Always call the remote_portfolio_agent sub-agent.
    """,
    sub_agents=[remote_portfolio_agent],  # A2A sub-agent added here!
)


async def test_call():
    session = InMemorySessionService()
    app_name = "portfolio_test"
    user_id = "user1"
    session_id = "sess1"

    await session.create_session(app_name=app_name, user_id=user_id, session_id=session_id)

    runner = Runner(
        agent=a2a_portfolio_agent,
        app_name=app_name,
        session_service=session,
    )

    msg = types.Content(parts=[types.Part(text="Show me portfolio services")])

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=msg,
    ):
        if event.is_final_response():
            print("FINAL:", event.content.parts[0].text)


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_call())

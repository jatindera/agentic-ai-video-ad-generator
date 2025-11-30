# app/agents/orchestrator_agent/agent.py

from google.adk.agents import SequentialAgent
from .sub_agents.business_requirements_agent import business_requirements_agent
from .sub_agents.domain_concept_parallel_agent import domain_concept_parallel_agent
from .sub_agents.concept_selector_agent import concept_selector_agent
from .sub_agents.creative_prompt_agent.agent import creative_agent
from .sub_agents.veo3_prompt_writer_agent import refined_veo3_prompt_writer_agent
from .sub_agents.video_generator_agent import video_generator_agent
from .sub_agents.trends_research_agent import trends_research_agent
from .sub_agents.a2a_portfolio_agent import a2a_portfolio_agent
# ------------------------------------------------------------
# Import sub-agents in correct execution order
# ------------------------------------------------------------



# ------------------------------------------------------------
# Build the deterministic ADK pipeline
# ------------------------------------------------------------

root_agent = SequentialAgent(
    name="root_orchestrator_agent",
    description="""
    This agent coordinates the execution of multiple sub-agents to create a complete video production workflow.
    It ensures that each sub-agent runs in the correct order and passes necessary information between them.
    """,
    sub_agents=[
        business_requirements_agent,
        domain_concept_parallel_agent, # parallel agent
        concept_selector_agent,
        creative_agent,
        refined_veo3_prompt_writer_agent, #loop agent
        video_generator_agent,
        trends_research_agent,
        # a2a_portfolio_agent
    ],
)


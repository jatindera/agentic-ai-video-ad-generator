# path: app/video_pipeline_app/root_agent/sub_agents/veo3_prompt_writer_agent/agent.py

from google.adk.agents import Agent, LoopAgent, SequentialAgent
from app.core.config import settings
from .instructions import veo3_prompt_writer_instructions
from .veo3_prompt_reviewer_agent import veo3_prompt_reviewer_agent
from .veo3_prompt_refinement_agent import veo3_prompt_refinement_agent
from .schema import FinalPromptSchema





print("✅ exit_loop function created.")

veo3_prompt_writer_agent = Agent(
    name="veo3_prompt_writer_agent",
    model=settings.google_model_name,
    instruction=veo3_prompt_writer_instructions,
    output_key="veo3_prompt_writer_output",
    output_schema=FinalPromptSchema,
)

# The LoopAgent contains the agents that will run repeatedly: Critic -> Refiner.
refinement_loop_agent = LoopAgent(
    name="refinement_loop_agent",
    sub_agents=[veo3_prompt_reviewer_agent, veo3_prompt_refinement_agent],
    max_iterations=1, # Prevents infinite loops
)

refined_veo3_prompt_writer_agent = SequentialAgent(
    name="refined_veo3_prompt_writer_agent",
    sub_agents=[veo3_prompt_writer_agent, refinement_loop_agent],
)
# path: app/video_pipeline_app/root_agent/sub_agents/domain_concept_parallel_agent/agent.py

from google.adk.agents import ParallelAgent, SequentialAgent
from .domain_search_agent import domain_search_agent
from .concept_writer_agent import concept_writer_agent

# --------------------------
# Parallel stage
# ******IMPORTANT*****
# Using FastAPI it fails, if we don't define the second agent as SequentialAgent
# --------------------------


domain_concept_parallel_agent = ParallelAgent(
    name="domain_concept_parallel_agent",
    sub_agents=[
        domain_search_agent,
        SequentialAgent(name="seq_concept_writer_agent",sub_agents=[concept_writer_agent]),
    ]
)


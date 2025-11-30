# app/agents/video_generator_agent/agent.py
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.adk.models.google_llm import Gemini
from app.core.config import settings
from app.utils.retry_config import retry_config
from app.video_pipeline_app.root_agent.sub_agents.veo3_prompt_writer_agent.schema import FinalPromptSchema
#MCP Client
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams
from mcp import StdioServerParameters

# -----------------------------------------------------------------------------------
# Use centralized logger
# -----------------------------------------------------------------------------------
from app.observability import get_logger
logger = get_logger(__name__)

DEFAULT_VIDEO_DURATION = 8

mcp_ai_vidoe_generation = McpToolset(
    connection_params=StreamableHTTPServerParams(
        url="http://127.0.0.1:9000/mcp/",
        headers={
            "X-MCP-Toolsets": "all",
            "X-MCP-Readonly": "true"
        },        
    ),
    tool_filter=["start_video_generation"]   # <-- filter by name
)


# ===================================================================================
# AGENT INSTRUCTIONS
# ===================================================================================
video_agent_instruction = """
You are the Video Generator Agent.
Follow these steps exactly:

1. Receive the full {veo3_prompt_writer_output} object.
2. Pass it directly to the function:
       `start_video_generation(veo3_prompt_writer_output)`
3. Return ONLY the tool output exactly as received.

Rules:
- Your response MUST be strictly the raw tool result.
- If the tool raises an error, return that exact error without modification.
"""

# Log the instruction ONCE at startup (not on every call)
logger.info("📄 Loaded Video Generator Agent Instruction:")
logger.info(video_agent_instruction)


# ===================================================================================
# VIDEO GENERATOR AGENT
# ===================================================================================
video_generator_agent = Agent(
    name="video_generator_agent",
    instruction=video_agent_instruction,
    model=Gemini(
        model=settings.google_model_name,
        retry_config=retry_config
    ),
    tools=[mcp_ai_vidoe_generation],
    input_schema=FinalPromptSchema,
)

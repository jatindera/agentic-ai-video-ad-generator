# app/observability/adk_plugins.py

import logging
from typing import Optional

from google.adk.plugins.logging_plugin import LoggingPlugin
from google.adk.plugins.base_plugin import BasePlugin
from google.adk.agents.base_agent import BaseAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest

logger = logging.getLogger("google_adk.observability")


class CountInvocationPlugin(BasePlugin):
    """
    Simple metrics-style plugin:
    - Counts agent invocations
    - Counts LLM requests
    - (Optional) Counts tool calls in future
    """

    def __init__(self) -> None:
        super().__init__(name="count_invocation")
        self.agent_count: int = 0
        self.llm_request_count: int = 0
        # you can add: self.tool_count: int = 0

    async def before_agent_callback(
        self,
        *,
        agent: BaseAgent,
        callback_context: CallbackContext,
    ) -> None:
        """
        Called before ANY agent runs (root or sub-agent).
        """
        self.agent_count += 1
        logger.info(
            "[CountInvocationPlugin] Agent '%s' run #%d",
            agent.name,
            self.agent_count,
        )

    async def before_model_callback(
        self,
        *,
        callback_context: CallbackContext,
        llm_request: LlmRequest,
    ) -> None:
        """
        Called before each LLM request.
        """
        self.llm_request_count += 1
        logger.info(
            "[CountInvocationPlugin] LLM request #%d | agent=%s | model=%s",
            self.llm_request_count,
            callback_context.agent_name,
            getattr(llm_request, "model", "unknown"),
        )


def default_adk_plugins():
    """
    Helper to get a consistent plugin set for all runners.
    - LoggingPlugin → structured ADK logs (events, tools, etc.)
    - CountInvocationPlugin → very lightweight metrics
    """
    return [
        LoggingPlugin(),
        CountInvocationPlugin(),
    ]

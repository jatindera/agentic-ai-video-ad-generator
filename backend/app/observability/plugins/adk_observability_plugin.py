import json
import logging
import time
from typing import Any

from google.adk.plugins.base_plugin import BasePlugin
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse

from app.observability.tracing.trace_utils import get_trace_id_from_context
from app.observability.metrics.metrics_store import increment

logger = logging.getLogger("adk.observability")


def _safe_json(obj: Any) -> Any:
    """Best-effort JSON-safe representation."""
    try:
        json.dumps(obj)
        return obj
    except TypeError:
        return str(obj)


class ADKObservabilityPlugin(BasePlugin):
    def __init__(self, name: str = "adk_observability", **kwargs):
        # ADK may pass name or other kwargs
        super().__init__(name=name, **kwargs)

    # ---------------------------------------------------------------
    # AGENT CALLBACKS
    # ---------------------------------------------------------------
    async def before_agent_callback(self, **kwargs):
        """
        Called as:
          before_agent_callback(agent=..., callback_context=...)
        """
        agent = kwargs.get("agent")
        callback_context: CallbackContext = kwargs.get("callback_context")
        if callback_context is None:
            return

        trace_id = get_trace_id_from_context(callback_context)
        increment("agents_total")

        # Store start time in context state, per agent invocation
        callback_context.state["agent_start"] = time.time()

        payload = getattr(callback_context, "payload", None)

        logger.info(json.dumps({
            "event": "agent_start",
            "agent": getattr(agent, "name", None),
            "trace_id": trace_id,
            "input": _safe_json(payload),
        }))

    async def after_agent_callback(self, **kwargs):
        """
        Called as:
          after_agent_callback(agent=..., callback_context=...)
        """
        agent = kwargs.get("agent")
        callback_context: CallbackContext = kwargs.get("callback_context")
        if callback_context is None:
            return

        trace_id = get_trace_id_from_context(callback_context)

        start = callback_context.state.get("agent_start", time.time())
        elapsed = time.time() - start

        # ADK usually stores final output on the context
        result = getattr(callback_context, "output", None)

        logger.info(json.dumps({
            "event": "agent_end",
            "agent": getattr(agent, "name", None),
            "trace_id": trace_id,
            "elapsed_sec": round(elapsed, 3),
            "output": _safe_json(result),
        }))

    # ---------------------------------------------------------------
    # LLM CALLBACKS
    # ---------------------------------------------------------------
    async def before_model_callback(self, **kwargs):
        """
        Called as:
          before_model_callback(callback_context=..., llm_request=...)
        """
        callback_context: CallbackContext = kwargs.get("callback_context")
        llm_request: LlmRequest = kwargs.get("llm_request")
        if callback_context is None or llm_request is None:
            return

        trace_id = get_trace_id_from_context(callback_context)
        increment("llm_requests_total")

        req = llm_request.model_dump()

        logger.info(json.dumps({
            "event": "llm_request",
            "trace_id": trace_id,
            "model": req.get("model"),
            "prompt": req.get("prompt"),
            "input_tokens": req.get("input_tokens"),
        }))

    async def after_model_callback(self, **kwargs):
        """
        Called as:
          after_model_callback(callback_context=..., llm_response=...)
        """
        callback_context: CallbackContext = kwargs.get("callback_context")
        llm_response: LlmResponse = kwargs.get("llm_response")
        if callback_context is None or llm_response is None:
            return

        trace_id = get_trace_id_from_context(callback_context)

        res = llm_response.model_dump()

        logger.info(json.dumps({
            "event": "llm_response",
            "trace_id": trace_id,
            "output": res.get("output_text"),
            "tokens_used": res.get("total_tokens"),
        }))

    # ---------------------------------------------------------------
    # TOOL CALLBACKS
    # ---------------------------------------------------------------
    async def before_tool_callback(self, **kwargs):
        """
        Called as:
          before_tool_callback(tool=..., tool_args=..., tool_context=...)
        """
        tool = kwargs.get("tool")
        tool_args = kwargs.get("tool_args")
        tool_context = kwargs.get("tool_context")  # ToolContext

        if tool_context is None:
            return

        trace_id = get_trace_id_from_context(tool_context)
        increment("tools_total")

        # Track per-tool timing
        state = getattr(tool_context, "state", None)
        if isinstance(state, dict):
            state.setdefault("tool_start", {})
            state["tool_start"][getattr(tool, "name", "")] = time.time()

        logger.info(json.dumps({
            "event": "tool_start",
            "tool": getattr(tool, "name", None),
            "trace_id": trace_id,
            "input": _safe_json(tool_args),
        }))

    async def after_tool_callback(self, **kwargs):
        """
        Called as:
          after_tool_callback(tool=..., tool_args=..., tool_context=..., result=...)
        """
        tool = kwargs.get("tool")
        tool_args = kwargs.get("tool_args")
        tool_context = kwargs.get("tool_context")
        result: Any = kwargs.get("result")

        if tool_context is None:
            return

        trace_id = get_trace_id_from_context(tool_context)

        state = getattr(tool_context, "state", None)
        if isinstance(state, dict):
            tool_start_map = state.get("tool_start", {})
            start = tool_start_map.get(getattr(tool, "name", ""), time.time())
        else:
            start = time.time()

        elapsed = time.time() - start

        logger.info(json.dumps({
            "event": "tool_end",
            "tool": getattr(tool, "name", None),
            "trace_id": trace_id,
            "elapsed_sec": round(elapsed, 3),
            "input": _safe_json(tool_args),
            "result": _safe_json(result),
        }))

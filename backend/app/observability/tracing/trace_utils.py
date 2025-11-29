import uuid
from typing import Any

TRACE_ID_KEY = "trace_id"


def new_trace_id() -> str:
    """Generate a new short trace ID."""
    return uuid.uuid4().hex[:16]


def get_trace_id_from_context(ctx: Any) -> str:
    """
    Get or create a trace_id stored in ctx.state (CallbackContext or ToolContext).

    If ctx.state doesn't exist or isn't a dict, we just generate a new one
    without trying to persist it.
    """
    state = getattr(ctx, "state", None)

    if isinstance(state, dict):
        trace_id = state.get(TRACE_ID_KEY)
        if not trace_id:
            trace_id = new_trace_id()
            state[TRACE_ID_KEY] = trace_id
        return trace_id

    # Fallback: no state → just generate a new one
    return new_trace_id()

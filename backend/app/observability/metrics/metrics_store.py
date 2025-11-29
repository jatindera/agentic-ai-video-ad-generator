from typing import Dict
from threading import Lock

_METRICS: Dict[str, int] = {
    "agents_total": 0,
    "agents_errors_total": 0,
    "llm_requests_total": 0,
    "llm_errors_total": 0,
    "tools_total": 0,
    "tools_errors_total": 0,
}

_LOCK = Lock()


def increment(metric_name: str, amount: int = 1) -> None:
    """
    Thread-safe increment of a metric counter.
    """
    with _LOCK:
        if metric_name not in _METRICS:
            _METRICS[metric_name] = 0
        _METRICS[metric_name] += amount


def get_metrics_snapshot() -> Dict[str, int]:
    """
    Return a copy of current metrics.
    Useful for exposing via /metrics endpoint.
    """
    with _LOCK:
        return dict(_METRICS)

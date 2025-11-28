from google.genai import types


# This controls how Gemini retries on transient errors
retry_config = types.HttpRetryOptions(
    attempts=2,             # Maximum retry attempts
    exp_base=7,             # Exponential backoff base
    initial_delay=1,        # Initial delay in seconds
    http_status_codes=[     # Retry on these HTTP errors
        429, 500, 503, 504
    ],
)
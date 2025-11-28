import json
from typing import Dict, Any

def clean_output(raw_output: Dict[str, Any]) -> Dict[str, Any]:
    """
    Removes unwanted fields (summary, notes, etc.) from an LLM output.

    Expected LLM output can vary:
      - may contain summary
      - may contain extra keys
      - may miss keys
      - may include hallucinated keys

    This function ensures:
      {
         "similar_examples": [...]
      }

    Nothing else is allowed.
    """

    print("🔧 Sanitizer Tool – Received:", raw_output)

    # Ensure root is dict
    if not isinstance(raw_output, dict):
        return {"similar_examples": []}

    # Extract similar_examples safely
    examples = raw_output.get("similar_examples", [])

    # Must be a list — otherwise fix it
    if not isinstance(examples, list):
        examples = []

    # Build sanitized output
    sanitized = {
        "similar_examples": examples
    }

    print("🔧 Sanitizer Tool – Returning:", sanitized)
    return sanitized

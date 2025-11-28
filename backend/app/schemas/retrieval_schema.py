# app/schemas/retrieval_schema.py

from typing import List, Optional
from pydantic import BaseModel


class RetrievalPreferences(BaseModel):
    """
    Preferences that influence how examples are selected and ranked.
    Passed by agents or orchestrators.
    """
    category: Optional[str] = None          # e.g. "grocery", "boutique"
    tones: List[str] = []                   # e.g. ["funny", "premium"]
    region: Optional[str] = None            # e.g. "punjab"
    max_examples: int = 6                   # default = return top 6 examples


class RetrievedExample(BaseModel):
    """
    Clean, agent-facing example object returned after re-ranking.
    """
    id: str
    title: str
    content: str
    category: Optional[str]
    tags: List[str]
    score: float

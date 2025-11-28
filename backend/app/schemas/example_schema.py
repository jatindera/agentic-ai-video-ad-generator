# app/schemas/example_schema.py

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, model_validator


# ---------------------------------------------------------
# 1. CREATE REQUEST — supports TEXT + JSON prompts
# ---------------------------------------------------------
class ExampleCreateRequest(BaseModel):
    title: str

    # Either this (text prompt)...
    prompt_text: Optional[str] = None

    # ...or this (JSON-style structured prompt) must be provided
    prompt_json: Optional[Dict[str, Any]] = None

    # Optional metadata for better retrieval
    business_type: Optional[str] = None
    ad_style: Optional[str] = None
    tone: Optional[str] = None
    target_audience: Optional[str] = None

    tags: List[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_prompt(self):
        """Ensure at least one form of prompt is provided."""
        has_text = bool(self.prompt_text and self.prompt_text.strip())
        has_json = self.prompt_json is not None

        if not (has_text or has_json):
            raise ValueError("Either prompt_text or prompt_json must be provided.")
        return self

# ---------------------------------------------------------
# 2. SEARCH REQUEST
# ---------------------------------------------------------
class ExampleSearchRequest(BaseModel):
    query: str = Field(..., description="Free-text query processed by LLM")
    top_k: int = Field(5, ge=1, le=50)

    # optional filters
    business_type: Optional[str] = None
    ad_style: Optional[str] = None
    tone: Optional[str] = None
    target_audience: Optional[str] = None
    tags: Optional[List[str]] = None


# ---------------------------------------------------------
# 3. SEARCH RESULT — complete metadata returned
# ---------------------------------------------------------
class ExampleSearchResult(BaseModel):
    id: str

    title: str
    prompt_text: Optional[str]
    prompt_json: Optional[Dict[str, Any]]

    business_type: Optional[str]
    ad_style: Optional[str]
    tone: Optional[str]
    target_audience: Optional[str]

    tags: List[str] = []

    score: float


# ---------------------------------------------------------
# 4. SEARCH RESPONSE
# ---------------------------------------------------------
class ExampleSearchResponse(BaseModel):
    results: List[ExampleSearchResult]

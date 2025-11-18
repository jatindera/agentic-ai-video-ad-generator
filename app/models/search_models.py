from pydantic import BaseModel, Field
from typing import List, Optional

# ------------------------------
# Google Search Models
# ------------------------------

class GoogleSearchInput(BaseModel):
    """Input model for Google Search tool."""
    query: str = Field(
        ...,
        description="Search query string.",
        example="latest AI news"
    )
    num_results: Optional[int] = Field(
        5,
        ge=1,
        le=10,
        description="Number of search results to return (1–10). Default is 5."
    )


class GoogleSearchResult(BaseModel):
    """Single search result entry."""
    title: str = Field(..., description="Title of the search result.")
    link: str = Field(..., description="URL of the result.")
    snippet: str = Field(..., description="Summary or snippet from the result.")


class GoogleSearchOutput(BaseModel):
    """Output model for Google Search tool."""
    query: str = Field(..., description="Original search query.")
    results: List[GoogleSearchResult] = Field(
        ..., description="List of search result entries."
    )

# ------------------------------
# Bing Search Models
# ------------------------------

class BingSearchInput(BaseModel):
    """Input model for Bing Search tool."""
    query: str = Field(
        ...,
        description="Search query text.",
        example="Azure AI Foundry"
    )
    num_results: Optional[int] = Field(
        5,
        ge=1,
        le=10,
        description="Maximum number of results to return (1–10). Default = 5."
    )


class BingSearchResult(BaseModel):
    """Single Bing search result entry."""
    title: str = Field(..., description="Title of the search result.")
    url: str = Field(..., description="URL of the result.")
    snippet: Optional[str] = Field(
        None, description="Short description or snippet from the page."
    )


class BingSearchOutput(BaseModel):
    """Output model for Bing Search."""
    query: str = Field(..., description="Original search query.")
    results: List[BingSearchResult] = Field(
        ..., description="List of Bing search results."
    )
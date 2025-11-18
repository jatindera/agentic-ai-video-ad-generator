import httpx
from app.core.config import settings
from app.models.search_models import (
    BingSearchInput,
    BingSearchOutput,
    BingSearchResult
)

BING_SEARCH_URL = "https://api.bing.microsoft.com/v7.0/search"


async def bing_search(input: BingSearchInput) -> BingSearchOutput:
    """
    Perform a Bing Web Search query and return structured results
    using Pydantic models.
    """
    headers = {
        "Ocp-Apim-Subscription-Key": settings.BING_API_KEY
    }

    params = {
        "q": input.query,
        "count": input.num_results,
        "textDecorations": False,
        "textFormat": "Raw",
    }

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(BING_SEARCH_URL, params=params, headers=headers)
        data = resp.json()

    web_pages = data.get("webPages", {}).get("value", [])
    results = []

    for item in web_pages:
        results.append(
            BingSearchResult(
                title=item.get("name", ""),
                url=item.get("url", ""),
                snippet=item.get("snippet")
            )
        )

    return BingSearchOutput(query=input.query, results=results)

import httpx
from app.core.config import settings
from app.models.search_models import (
    GoogleSearchInput,
    GoogleSearchOutput,
    GoogleSearchResult
)

GOOGLE_SEARCH_URL = "https://www.googleapis.com/customsearch/v1"


async def google_search(input: GoogleSearchInput) -> GoogleSearchOutput:
    """
    Perform a Google Custom Search query and return structured results.
    """
    params = {
        "q": input.query,
        "key": settings.GOOGLE_API_KEY,
        "cx": settings.GOOGLE_SEARCH_ENGINE_ID,
        "num": input.num_results,
    }

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(GOOGLE_SEARCH_URL, params=params)
        data = resp.json()

    items = data.get("items", [])
    results = []

    for item in items:
        results.append(
            GoogleSearchResult(
                title=item.get("title", ""),
                link=item.get("link", ""),
                snippet=item.get("snippet", "")
            )
        )

    return GoogleSearchOutput(query=input.query, results=results)

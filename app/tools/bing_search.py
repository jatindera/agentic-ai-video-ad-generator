from app.models.search_models import BingSearchInput, BingSearchOutput
from app.services.bing_service import bing_search


async def bing_search_tool(input: BingSearchInput) -> BingSearchOutput:
    """
    Execute a Bing search and return structured search results.

    This MCP tool enables AI Agents and MCP Clients to perform
    real-time web searches using Microsoft's Bing Search API.
    By using Pydantic models for input/output, this tool ensures
    strong validation, schema clarity, and reliable agent behavior.

    Parameters
    ----------
    input : BingSearchInput
        A Pydantic model containing:
        - query (str): Search query text.
        - num_results (int): Number of results (1–10).

    Returns
    -------
    BingSearchOutput
        A Pydantic model containing the list of search results.
        Each result includes:
        - title (str)
        - url (str)
        - snippet (str | None)

    Raises
    ------
    HTTPError
        If the Bing API request fails.
    ValueError
        If the query string is empty.

    Examples
    --------
    >>> await bing_search_tool(
    ...     BingSearchInput(query="FastMCP tutorial", num_results=3)
    ... )
    BingSearchOutput(
        query="FastMCP tutorial",
        results=[BingSearchResult(...), ...]
    )

    Notes
    -----
    This tool is exposed to MCP-based applications like VSCode, Cursor,
    and AI-powered automation systems for web information retrieval.
    """
    return await bing_search(input)

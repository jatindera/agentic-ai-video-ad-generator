from app.models.search_models import GoogleSearchInput, GoogleSearchOutput
from app.services.google_service import google_search


async def google_search_tool(input: GoogleSearchInput) -> GoogleSearchOutput:
    """
    Execute a Google search and return structured search results.

    This MCP tool enables AI Agents and MCP Clients to perform
    real-time Google searches using the Google Custom Search API.
    Inputs and outputs are validated using Pydantic for maximum
    reliability and schema clarity.

    Parameters
    ----------
    input : GoogleSearchInput
        A Pydantic model containing:
        - query (str): Search query text.
        - num_results (int): Max results to return (1–10).

    Returns
    -------
    GoogleSearchOutput
        A Pydantic model containing:
        - query (str): Original query.
        - results (List[GoogleSearchResult])

    Raises
    ------
    HTTPError
        If the Google API call fails.
    ValueError
        If query is empty or invalid.

    Examples
    --------
    >>> await google_search_tool(
    ...     GoogleSearchInput(query="agentic AI", num_results=3)
    ... )
    GoogleSearchOutput(
        query="agentic AI",
        results=[GoogleSearchResult(...), ...]
    )

    Notes
    -----
    This tool is exposed to MCP Clients such as VSCode, Cursor,
    and custom AI applications for automated search tasks.
    """
    return await google_search(input)

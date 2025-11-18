from app.models.math_models import MathAddInput, MathAddOutput
from app.services.math_service import add_numbers


def add_tool(input: MathAddInput) -> MathAddOutput:
    """
    Add two integers and return the computed result.

    This MCP tool performs a simple arithmetic addition using validated
    Pydantic models. It ensures that both inputs are integers and returns
    a strongly typed output that AI Agents can rely on.

    Parameters
    ----------
    input : MathAddInput
        A Pydantic model containing:
        - a (int): First number to add.
        - b (int): Second number to add.

    Returns
    -------
    MathAddOutput
        A Pydantic model with:
        - result (int): The sum of `a` and `b`.

    Examples
    --------
    >>> add_tool(MathAddInput(a=5, b=7))
    MathAddOutput(result=12)

    Notes
    -----
    This function is exposed as an MCP tool. MCP Clients (VSCode, Cursor,
    JetBrains, or custom apps) will call this automatically when the user
    requests a calculation such as "Add 10 and 25".
    """
    return add_numbers(input)

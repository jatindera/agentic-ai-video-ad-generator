from app.models.math_models import MathAddInput, MathAddOutput


def add_numbers(input: MathAddInput) -> MathAddOutput:
    """
    Add two numbers and return the result as a Pydantic model.
    """
    return MathAddOutput(result=input.a + input.b)

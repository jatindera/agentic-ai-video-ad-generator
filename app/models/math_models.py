from pydantic import BaseModel, Field


class MathAddInput(BaseModel):
    """Input model for the add tool."""
    a: int = Field(..., description="First number to add.", example=2)
    b: int = Field(..., description="Second number to add.", example=3)


class MathAddOutput(BaseModel):
    """Output model for the add tool."""
    result: int = Field(..., description="The computed sum of a and b.")

from pydantic import BaseModel, Field
from typing import List

class Concept(BaseModel):
    Concept_Name: str = Field(..., description="Title of the concept.")
    The_Hook: str = Field(..., description="Opening moment that grabs viewer attention.")
    The_Action: str = Field(..., description="Main transformation or event shown in the ad.")
    The_Feeling: str = Field(..., description="Primary emotions the scene should evoke.")
    Visual_Metaphor: str = Field(..., description="Symbolic visual expressing the product’s value.")
    Dialog: str = Field(..., description="Short line of character dialogue.")
    Background_Music: str = Field(..., description="Music style or mood for the scene.")
    Sound_Effects: str = Field(..., description="Key sound effects used during the scene.")

class ConceptWriterOutput(BaseModel):
    concepts: List[Concept] = Field(
        ..., 
        description="A list of 3 creative ad concepts, each with complete details."
    )

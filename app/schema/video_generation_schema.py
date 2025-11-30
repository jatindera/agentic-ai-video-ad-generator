from typing import List, Optional
from pydantic import BaseModel


# -------------------------
# Audio Model
# -------------------------
class Audio(BaseModel):
    sfx: Optional[str] = None
    music: Optional[str] = None
    spoken_line: Optional[str] = None


# -------------------------
# Sequence Item Model
# -------------------------
class SequenceItem(BaseModel):
    label: str
    visual_description: str
    cinematography: str
    audio: Audio
    emotional_intention: str
    transition: Optional[str] = None
    on_screen_text_element: Optional[str] = None


# -------------------------
# Final Root Model
# -------------------------
class FinalPromptSchema(BaseModel):
    final_text_prompt: str
    sequence: List[SequenceItem]
    visual_style_notes: str
    audio_plan: str
    negative_prompts: List[str]
    director_notes: str

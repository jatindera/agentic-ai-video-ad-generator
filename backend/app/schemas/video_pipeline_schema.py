# app/schemas/video_pipeline_schema.py

from pydantic import BaseModel, HttpUrl, Field, field_validator
from typing import Optional, List, Dict


# ---------------------------------------------------------
# 1. Main Input Schema (User → API)
# ---------------------------------------------------------

class VideoPipelineRequest(BaseModel):
    business_info: str
    
    

# ---------------------------------------------------------
# 2. Output of Requirements Agent
# ---------------------------------------------------------

class RequirementsOutput(BaseModel):
    extracted_requirements: Dict[str, str]  # key/value pairs
    missing_information: List[str] = []
    reasoning: Optional[str] = None


# ---------------------------------------------------------
# 3. Output of Search Agent
# ---------------------------------------------------------

class SearchResult(BaseModel):
    title: str
    url: Optional[str]
    summary: Optional[str] = None


class SearchAgentOutput(BaseModel):
    similar_examples: List[SearchResult]
    embedded_context: Optional[str] = None


# ---------------------------------------------------------
# 4. Output of Creative Prompt Agent
# ---------------------------------------------------------

class CreativePromptOutput(BaseModel):
    prompt: str
    reasoning: Optional[str] = None


# ---------------------------------------------------------
# 5. Output of Review Agent
# ---------------------------------------------------------

class ReviewOutput(BaseModel):
    approved: bool
    feedback: Optional[str] = None
    updated_prompt: Optional[str] = None


# ---------------------------------------------------------
# 6. Output of Video Agent (long-running)
# ---------------------------------------------------------

class VideoGenerationStatus(BaseModel):
    operation_id: str
    status: str  # pending / running / completed / failed
    progress: Optional[int] = None  # % complete
    video_url: Optional[str] = None
    error_message: Optional[str] = None


class VideoAgentOutput(BaseModel):
    operation_id: str
    message: str
    polling_required: bool = True


# ---------------------------------------------------------
# 7. Final Orchestrator Output (complete pipeline)
# ---------------------------------------------------------

class VideoPipelineResponse(BaseModel):
    requirements: RequirementsOutput
    examples: SearchAgentOutput
    creative_prompt: CreativePromptOutput
    review: ReviewOutput
    video_generation: VideoGenerationStatus

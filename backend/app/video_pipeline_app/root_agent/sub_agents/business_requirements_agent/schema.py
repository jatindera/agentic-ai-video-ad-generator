from pydantic import BaseModel
from typing import List, Optional


class TargetAudience(BaseModel):
    age_group: str
    demographics: str
    pain_points: str


class BusinessInfo(BaseModel):
    business_name: str
    industry: str
    business_type: str
    target_audience: TargetAudience
    brand_tone: str
    core_offer: str
    unique_selling_point: str
    ad_objective: str
    visual_preferences: str
    platform: str


class BusinessRequirements(BaseModel):
    business_info: BusinessInfo
    gaps_filled: List[str]
    assumptions_made: List[str]



class RawRequirements(BaseModel):
    raw_requirements: str




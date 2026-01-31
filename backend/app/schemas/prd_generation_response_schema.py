from typing import List
from pydantic import BaseModel, Field


class StoryOut(BaseModel):
    title: str = Field(..., min_length=5)
    description: str = Field(..., min_length=10)
    acceptance_criteria: List[str] = Field(..., min_items=1)
    justification: str = Field(..., min_length=5)


class EpicOut(BaseModel):
    title: str = Field(..., min_length=3)
    justification: str = Field(..., min_length=5)
    stories: List[StoryOut] = Field(..., min_items=1)


class PRDGenerationResponse(BaseModel):
    epics: List[EpicOut] = Field(..., min_items=1)

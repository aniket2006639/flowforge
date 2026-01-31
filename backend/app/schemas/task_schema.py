from typing import List, Literal
from pydantic import BaseModel, Field, validator


# ----------------------------
# Story / Task Schema
# ----------------------------

class Story(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=10)
    acceptance_criteria: List[str] = Field(..., min_items=1)
    priority: Literal["High", "Medium", "Low"]
    story_points: Literal[1, 2, 3, 5, 8]

    @validator("acceptance_criteria", each_item=True)
    def validate_acceptance_criteria(cls, v: str):
        if len(v.strip()) < 5:
            raise ValueError("Acceptance criteria must be meaningful")
        return v.strip()


# ----------------------------
# Epic Schema
# ----------------------------

class Epic(BaseModel):
    epic_name: str = Field(..., min_length=3, max_length=100)
    epic_description: str = Field(..., min_length=10)
    stories: List[Story] = Field(..., min_items=1)


# ----------------------------
# Root Task Generation Output
# ----------------------------

class TaskGenerationResponse(BaseModel):
    project_key: str = Field(..., min_length=2, max_length=10)
    epics: List[Epic] = Field(..., min_items=1)
# ----------------------------
# Generate Tasks Request
# ----------------------------

class GenerateTasksRequest(BaseModel):
    prd_text: str = Field(..., min_length=20)
    project_key: str = Field(..., min_length=2, max_length=10)
    provider: Literal["ollama", "neysa", "openai", "fastrouter"] = "neysa"

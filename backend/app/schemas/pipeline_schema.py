from typing import List
from pydantic import BaseModel, Field


# ----------------------------
# PRD → Pipeline Request
# ----------------------------

class PRDPipelineRequest(BaseModel):
    project: str = Field(..., min_length=2, max_length=10)
    prd: str = Field(..., min_length=20)


# ----------------------------
# Push Selected Tasks
# ----------------------------

class SelectedTask(BaseModel):
    title: str = Field(..., min_length=3)
    description: str = Field(..., min_length=5)
    type: str = "Task"


class PushSelectedRequest(BaseModel):
    project: str = Field(..., min_length=2, max_length=10)
    tasks: List[SelectedTask]

from pydantic import BaseModel, Field


class GenerateFromPrdRequest(BaseModel):
    prd: str = Field(..., min_length=50)

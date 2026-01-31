from pydantic import BaseModel
from typing import Optional

class UpdateIssueRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

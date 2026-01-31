from pydantic import BaseModel
from typing import List, Optional


class SubtaskRequest(BaseModel):
    title: str
    description: str


class CreateIssueRequest(BaseModel):
    project: str
    title: str
    description: str
    issue_type: str = "Task"

    # create subtasks under this issue
    subtasks: Optional[List[SubtaskRequest]] = None

    # optional direct parent (for standalone subtask creation)
    parent_key: Optional[str] = None

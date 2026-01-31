from typing import Dict, List
from pydantic import BaseModel, Field


class JiraAuth(BaseModel):
    jira_domain: str = Field(..., example="yourcompany.atlassian.net")
    email: str
    api_token: str


class PushToJiraRequest(BaseModel):
    auth: JiraAuth
    tasks: Dict   # already validated TaskGenerationResponse JSON


class PushToJiraResponse(BaseModel):
    created_issues: List[str]

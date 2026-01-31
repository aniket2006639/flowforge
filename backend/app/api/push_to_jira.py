from fastapi import APIRouter, HTTPException

from app.schemas.jira_schema import (
    PushToJiraRequest,
    PushToJiraResponse
)
from app.services.jira_service import JiraService

router = APIRouter(prefix="/push-to-jira", tags=["Jira"])


@router.post("", response_model=PushToJiraResponse)
def push_to_jira(payload: PushToJiraRequest):
    jira = JiraService(
        domain=payload.auth.jira_domain,
        email=payload.auth.email,
        api_token=payload.auth.api_token
    )

    created = []

    try:
        project_key = payload.tasks["project_key"]

        for epic in payload.tasks["epics"]:
            for story in epic["stories"]:
                issue_key = jira.create_issue(
                    project_key=project_key,
                    title=story["title"],
                    description=story["description"]
                )
                created.append(issue_key)

        return {"created_issues": created}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.db.models.user import User
from app.db.models.jira_connection import JiraConnection

from app.schemas.jira_connect_schema import JiraConnectRequest
from app.schemas.jira_issue_schema import CreateIssueRequest
from app.schemas.jira_update_schema import UpdateIssueRequest
from app.schemas.jira_comment_schema import AddCommentRequest
from app.schemas.jira_move_schema import BatchMoveRequest
from app.schemas.generate_from_prd_schema import GenerateFromPrdRequest

from app.services.jira_connection_service import connect_jira
from app.services.jira_proxy_service import (
    create_issue,
    create_issue_with_subtasks,
    update_issue,
    get_transitions,
    transition_issue,
    add_comment,
    delete_issue,
    fetch_issues,
    get_kanban_board,
    batch_move_issues,
    get_workflow_metadata
)
from app.services.prd_to_jira_service import PRDToJiraService


router = APIRouter(prefix="/jira", tags=["jira"])


# ---------------- CONNECT ----------------

@router.post("/connect")
def jira_connect(
    data: JiraConnectRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        connect_jira(db, user.id, data.site_url, data.email, data.api_token)
        return {"status": "connected"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/status")
def jira_status(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    conn = db.query(JiraConnection).filter(
        JiraConnection.user_id == user.id
    ).first()

    return {"connected": bool(conn)}


@router.delete("/disconnect")
def jira_disconnect(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    conn = db.query(JiraConnection).filter(
        JiraConnection.user_id == user.id
    ).first()

    if conn:
        db.delete(conn)
        db.commit()

    return {"status": "disconnected"}


# ---------------- ISSUES ----------------

@router.get("/issues")
def jira_issues(
    project: str = Query(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    issues = fetch_issues(db, user.id, project)
    return {"issues": issues}


@router.post("/issue")
def jira_create_issue(
    data: CreateIssueRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Case 1 — create parent + subtasks
    if data.subtasks:
        result = create_issue_with_subtasks(
            db=db,
            user_id=user.id,
            project=data.project,
            title=data.title,
            description=data.description,
            issue_type=data.issue_type,
            subtasks=[s.model_dump() for s in data.subtasks]
        )
        return {"created": result}

    # Case 2 — normal issue or single subtask
    result = create_issue(
        db=db,
        user_id=user.id,
        project=data.project,
        title=data.title,
        description=data.description,
        issue_type=data.issue_type,
        parent_key=data.parent_key
    )

    return {"created": result}


@router.post("/generate")
async def jira_generate(
    data: GenerateFromPrdRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate Epics & Stories from a raw PRD (preview only).

    - PRD must be >= 50 characters
    - Calls isolated PRD->Jira LLM service
    - Returns strictly validated JSON for preview
    """
    try:
        generated = await PRDToJiraService.generate(data.prd)
        return generated.dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.patch("/issue/{key}")
def jira_update_issue(
    key: str,
    data: UpdateIssueRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return update_issue(
        db=db,
        user_id=user.id,
        issue_key=key,
        title=data.title,
        description=data.description
    )


@router.delete("/issue/{key}")
def jira_delete_issue(
    key: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return delete_issue(db, user.id, key)


# ---------------- TRANSITIONS ----------------

@router.get("/issue/{key}/transitions")
def jira_transitions(
    key: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return {"transitions": get_transitions(db, user.id, key)}


@router.post("/issue/{key}/transition/{transition_id}")
def jira_transition_issue(
    key: str,
    transition_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return transition_issue(db, user.id, key, transition_id)


# ---------------- COMMENTS ----------------

@router.post("/issue/{key}/comment")
def jira_add_comment(
    key: str,
    data: AddCommentRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return add_comment(
        db=db,
        user_id=user.id,
        issue_key=key,
        text=data.text
    )


# ---------------- BOARD ----------------

@router.get("/board")
def jira_board(
    project: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_kanban_board(db, user.id, project)


@router.post("/board/move")
def jira_batch_move(
    data: BatchMoveRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return batch_move_issues(
        db=db,
        user_id=user.id,
        moves=[m.model_dump() for m in data.moves]
    )


@router.get("/workflow")
def jira_workflow(
    project: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_workflow_metadata(db, user.id, project)

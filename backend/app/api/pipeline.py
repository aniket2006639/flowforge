from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.db.models.user import User

from app.schemas.pipeline_schema import PRDPipelineRequest
from app.schemas.pipeline_schema import PushSelectedRequest

from app.services.pipeline_service import (
    prd_to_jira_pipeline,
    prd_preview_pipeline,
    push_selected_tasks,
)

router = APIRouter(prefix="/pipeline", tags=["pipeline"])


@router.post("/prd-to-jira")
async def prd_pipeline(
    data: PRDPipelineRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return await prd_to_jira_pipeline(
        db=db,
        user_id=user.id,
        project=data.project,
        prd=data.prd,
    )


@router.post("/preview")
async def prd_preview(data: PRDPipelineRequest):
    return await prd_preview_pipeline(
        project=data.project,
        prd=data.prd,
    )


@router.post("/push-selected")
def push_selected(
    data: PushSelectedRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return push_selected_tasks(
        db=db,
        user_id=user.id,
        project=data.project,
        tasks=[t.model_dump() for t in data.tasks],
    )

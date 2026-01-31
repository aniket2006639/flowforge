from fastapi import APIRouter, HTTPException

from app.schemas.task_schema import (
    GenerateTasksRequest,
    TaskGenerationResponse,
)
from app.services.task_generator import TaskGeneratorService

router = APIRouter(prefix="/generate-tasks", tags=["Task Generation"])


@router.post("", response_model=TaskGenerationResponse)
async def generate_tasks(payload: GenerateTasksRequest):
    try:
        return await TaskGeneratorService.generate(
            prd_text=payload.prd_text,
            project_key=payload.project_key,
            provider=payload.provider
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

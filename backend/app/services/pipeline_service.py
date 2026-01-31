from fastapi import HTTPException

from app.services.jira_proxy_service import (
    bulk_create_issues,
    get_kanban_board,
)
from app.services.prd_to_jira_service import PRDToJiraService


async def prd_to_jira_pipeline(
    db,
    user_id: str,
    project: str,
    prd: str,
    provider: str | None = None,
):
    try:
        # Step 1 — AI generates structured epics/stories
        result = await PRDToJiraService.generate(prd, provider=provider)

        jira_tasks = []

        # Flatten epics → stories into Jira issues
        for epic in result.epics:
            for story in epic.stories:
                jira_tasks.append(
                    {
                        "title": f"[{epic.title}] {story.title}",
                        "description": (
                            story.description
                            + "\n\nAcceptance Criteria:\n- "
                            + "\n- ".join(story.acceptance_criteria)
                        ),
                        "type": "Task",
                    }
                )

        # Step 2 — Create Jira issues
        created = bulk_create_issues(
            db,
            user_id,
            project,
            jira_tasks,
        )

        # Step 3 — Fetch updated board
        board = get_kanban_board(db, user_id, project)

        return {
            "created": created,
            "board": board,
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


async def prd_preview_pipeline(
    project: str,
    prd: str,
    provider: str | None = None,
):
    try:
        result = await PRDToJiraService.generate(prd, provider=provider)
        return result.model_dump()

    except ValueError as e:
        # PRD / validation errors
        raise HTTPException(status_code=400, detail=str(e))

    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


def push_selected_tasks(
    db,
    user_id: str,
    project: str,
    tasks: list,
):
    created = bulk_create_issues(
        db,
        user_id,
        project,
        tasks,
    )

    board = get_kanban_board(db, user_id, project)

    return {
        "created": created,
        "board": board,
    }

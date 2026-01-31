from app.llm.router import get_llm_client
from app.schemas.task_schema import TaskGenerationResponse


class TaskGeneratorService:

    @staticmethod
    async def generate(prd_text: str, project_key: str, provider: str):
        llm_client = get_llm_client(provider)

        raw_output = await llm_client.generate_tasks(
            prd_text=prd_text,
            project_key=project_key
        )

        # 🔒 Schema validation (critical)
        validated = TaskGenerationResponse.parse_obj(raw_output)

        return validated

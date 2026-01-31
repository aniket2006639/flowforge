from app.llm.base import BaseLLMClient


class OpenAIClient(BaseLLMClient):

    async def generate_tasks(self, prd_text: str, project_key: str):
        # Temporary stub response (schema-valid)
        return {
            "project_key": project_key,
            "epics": [
                {
                    "epic_name": "Core Features",
                    "epic_description": "Primary product functionality",
                    "stories": [
                        {
                            "title": "Initial setup",
                            "description": "Set up initial project structure and configuration",
                            "acceptance_criteria": [
                                "Project structure is created",
                                "Application runs without errors"
                            ],
                            "priority": "Medium",
                            "story_points": 2
                        }
                    ]
                }
            ]
        }

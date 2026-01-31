from app.llm.base import BaseLLMClient


class OllamaClient(BaseLLMClient):

    async def generate_tasks(self, prd_text: str, project_key: str):
        return {
            "project_key": project_key,
            "epics": [
                {
                    "epic_name": "Authentication",
                    "epic_description": "User authentication and access control",
                    "stories": [
                        {
                            "title": "User login",
                            "description": "Allow users to login using email and password",
                            "acceptance_criteria": [
                                "User can login with valid credentials",
                                "Error shown for invalid credentials"
                            ],
                            "priority": "High",
                            "story_points": 3
                        }
                    ]
                }
            ]
        }

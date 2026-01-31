import os
import json
import httpx


class FastRouterClient:
    def __init__(self):
        self.api_key = os.getenv("FASTROUTER_API_KEY")
        self.model = os.getenv("FASTROUTER_MODEL", "openai/gpt-4o-mini")
        self.url = "https://openrouter.ai/api/v1/chat/completions"

        if not self.api_key:
            raise ValueError("FASTROUTER_API_KEY is not set")

    async def generate_tasks(self, prd_text: str, project_key: str = "") -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "temperature": 0,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a senior Product Manager and Software Architect."
                },
                {
                    "role": "user",
                    "content": prd_text
                }
            ],
        }

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                self.url,
                headers=headers,
                json=payload,
            )

        if response.status_code != 200:
            raise ValueError(
                f"OpenRouter API error {response.status_code}: {response.text}"
            )

        data = response.json()

        try:
            return data["choices"][0]["message"]["content"]
        except Exception:
            raise ValueError(
                f"Unexpected OpenRouter response: {json.dumps(data)}"
            )

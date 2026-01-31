import httpx
import json


class FastRouterLLMClient:
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    async def generate_tasks(self, prd_text: str, project_key: str = "") -> dict:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",
            "X-Title": "FlowForge",
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
                self.base_url,
                headers=headers,
                json=payload,
            )

        if response.status_code != 200:
            raise ValueError(
                f"FastRouter API error {response.status_code}: {response.text}"
            )

        data = response.json()

        try:
            return data["choices"][0]["message"]["content"]
        except Exception:
            raise ValueError(f"Unexpected FastRouter response: {json.dumps(data)}")

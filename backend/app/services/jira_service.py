import base64
import requests

from app.utils.adf import text_to_adf


class JiraService:

    def __init__(self, domain: str, email: str, api_token: str):
        self.base_url = f"https://{domain}/rest/api/3"
        auth_str = f"{email}:{api_token}"
        self.headers = {
            "Authorization": "Basic " + base64.b64encode(auth_str.encode()).decode(),
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def create_issue(self, project_key: str, title: str, description: str):
        payload = {
            "fields": {
                "project": {"key": project_key},
                "summary": title,
                "issuetype": {"name": "Task"},
                "description": text_to_adf(description)
            }
        }

        response = requests.post(
            f"{self.base_url}/issue",
            headers=self.headers,
            json=payload,
            timeout=10
        )

        if response.status_code not in (200, 201):
            raise RuntimeError(
                f"Jira error {response.status_code}: {response.text}"
            )

        return response.json()["key"]

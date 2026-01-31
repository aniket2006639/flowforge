import base64
import requests

email = "31240571@vupune.ac.in"
import os

API_TOKEN = os.getenv("JIRA_API_TOKEN")

domain = "yuktix.atlassian.net"

auth = base64.b64encode(f"{email}:{api_token}".encode()).decode()

r = requests.get(
    f"https://{domain}/rest/api/3/myself",
    headers={
        "Authorization": f"Basic {auth}",
        "Accept": "application/json"
    }
)

print(r.status_code)
print(r.json())

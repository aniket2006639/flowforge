import os
import requests
from dotenv import load_dotenv

# Load env
load_dotenv(".env")

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

print("✅ CONFIG LOADED")
print("JIRA_BASE_URL:", JIRA_BASE_URL)
print("JIRA_EMAIL:", JIRA_EMAIL)
print("JIRA_API_TOKEN exists:", bool(JIRA_API_TOKEN))

assert JIRA_BASE_URL and JIRA_EMAIL and JIRA_API_TOKEN, "Missing env vars"

url = f"{JIRA_BASE_URL}/rest/api/3/myself"

response = requests.get(
    url,
    auth=(JIRA_EMAIL, JIRA_API_TOKEN),
    headers={"Accept": "application/json"},
    timeout=10
)

print("\nSTATUS CODE:", response.status_code)
print("RESPONSE:\n", response.text)

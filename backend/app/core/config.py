import os

class Settings:
    # Jira (single system user)
    JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
    JIRA_EMAIL = os.getenv("JIRA_EMAIL")
    JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

    # LLM
    FASTROUTER_API_KEY = os.getenv("FASTROUTER_API_KEY")
    FASTROUTER_MODEL = os.getenv("FASTROUTER_MODEL")

    # Security
    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

settings = Settings()
print("✅ CONFIG LOADED")
print("JIRA_BASE_URL:", settings.JIRA_BASE_URL)
print("JIRA_EMAIL:", settings.JIRA_EMAIL)
print("JIRA_API_TOKEN exists:", bool(settings.JIRA_API_TOKEN))

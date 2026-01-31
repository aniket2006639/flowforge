from pydantic import BaseModel, HttpUrl

class JiraConnectRequest(BaseModel):
    site_url: str
    email: str
    api_token: str

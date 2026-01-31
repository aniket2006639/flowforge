from pydantic import BaseModel

class AddCommentRequest(BaseModel):
    text: str

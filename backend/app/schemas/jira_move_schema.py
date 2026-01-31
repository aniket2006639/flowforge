from pydantic import BaseModel
from typing import List


class MoveItem(BaseModel):
    issue: str
    to: str


class BatchMoveRequest(BaseModel):
    moves: List[MoveItem]

from datetime import datetime

from pydantic import BaseModel


class DigestIn(BaseModel):
    content: str


class DigestOut(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    content: str
    created_at: datetime

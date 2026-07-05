from pydantic import BaseModel


class DigestIn(BaseModel):
    content: str

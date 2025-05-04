from pydantic import BaseModel
from typing import Dict, Optional


class Document(BaseModel):
    id:str
    content: str | None = None
    metadata: Dict

class Documents(BaseModel):
    documents: list[Document] = []

class Message(BaseModel):
    message: str
    id: str | None = None
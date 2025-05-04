from pydantic import BaseModel
from typing import Dict


class Document(BaseModel):
    id:str
    content: str | None = None
    metadata: Dict

class Documents(BaseModel):
    documents: list[Document] = []

class Message(BaseModel):
    message: str
    id: str | None = None

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str

from pydantic import BaseModel
from typing import List, Dict

class EmbeddingInput(BaseModel):
    id: str
    embedding: List[float]
    metadata: Dict[str, str]

class QueryInput(BaseModel):
    embedding: List[float]
    top_k: int = 5
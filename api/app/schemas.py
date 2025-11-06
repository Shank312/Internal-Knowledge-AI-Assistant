

from pydantic import BaseModel

class ChatRequest(BaseModel):
    query: str
    top_k: int | None = None

class Citation(BaseModel):
    document_id: str
    filename: str
    snippet: str

class ChatResponse(BaseModel):
    answer: str
    citations: list[Citation]

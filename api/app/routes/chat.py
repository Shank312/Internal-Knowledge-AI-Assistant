

from fastapi import APIRouter, Depends
from ..deps import get_current_tenant
from ..schemas import ChatRequest, ChatResponse, Citation
from ..retrieval import hybrid_search
from ..llm import answer_with_context

router = APIRouter(prefix="/v1", tags=["chat"])

@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, tenant_id: str = Depends(get_current_tenant)):
    hits = hybrid_search(req.query, tenant_id, req.top_k)
    context_snippets = [h["content"] for h in hits]
    answer = answer_with_context(req.query, context_snippets)
    citations = [
        Citation(document_id=str(h["document_id"]), filename=h["filename"], snippet=h["content"][:300])
        for h in hits[:5]
    ]
    return ChatResponse(answer=answer, citations=citations)

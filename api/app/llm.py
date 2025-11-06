

from openai import OpenAI
from .config import settings

SYSTEM_PROMPT = (
    "You are Company Brain, a helpful internal assistant. "
    "Answer only from the provided context snippets. If unsure, say you don't know. "
    "Cite sources succinctly."
)

def answer_with_context(query: str, context_snippets: list[str]) -> str:
    client = OpenAI(api_key=settings.openai_api_key)
    context = "\n\n".join(f"[{i+1}] " + s for i, s in enumerate(context_snippets))
    msgs = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Question: {query}\n\nContext:\n{context}"},
    ]
    resp = client.chat.completions.create(
        model=settings.llm_model,
        messages=msgs,
        temperature=settings.temperature,
        max_tokens=settings.max_tokens,
    )
    return resp.choices[0].message.content.strip()

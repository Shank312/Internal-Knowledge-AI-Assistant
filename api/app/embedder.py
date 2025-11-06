

from typing import List
from openai import OpenAI
from .config import settings

def embed_texts(texts: List[str]) -> list[list[float]]:
    client = OpenAI(api_key=settings.openai_api_key)
    resp = client.embeddings.create(model=settings.embedding_model, input=texts)
    return [d.embedding for d in resp.data]

def embed_query(text: str) -> list[float]:
    return embed_texts([text])[0]

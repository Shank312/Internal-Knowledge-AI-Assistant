

from typing import List
from openai import OpenAI
import re, os

REDACTED = os.getenv("REDACTED")

def chunk_text(text: str, max_len: int = 1200, overlap: int = 120) -> List[str]:
    text = re.sub(r"\s+"," ", text).strip()
    words = text.split(" ")
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + max_len, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        if end == len(words):
            break
        start = max(0, end - overlap)
    return chunks

def embed_texts(texts: List[str]) -> list[list[float]]:
    client = OpenAI(api_key=REDACTED)
    resp = client.embeddings.create(
        model=os.getenv("EMBEDDING_MODEL","text-embedding-3-small"),
        input=texts
    )
    return [d.embedding for d in resp.data]

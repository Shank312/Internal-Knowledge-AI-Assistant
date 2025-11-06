

import re
from typing import List

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

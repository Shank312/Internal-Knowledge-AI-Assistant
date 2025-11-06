

from fastapi import FastAPI
from .routes import chat, ingest

app = FastAPI(title="Company Brain API", version="0.1.0")

@app.get("/v1/healthz")
def healthz():
    return {"status": "ok"}

app.include_router(chat.router)
app.include_router(ingest.router)

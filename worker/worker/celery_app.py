

import os
from redis import Redis
from .ingest_tasks import process_upload

REDIS_URL = os.getenv("REDIS_URL","redis://localhost:6379/0")

def worker_loop():
    r = Redis.from_url(REDIS_URL)
    print("[ingest-worker] started; listening on 'ingest_queue'")
    while True:
        item = r.blpop("ingest_queue", timeout=5)
        if not item:
            continue
        _, payload = item
        try:
            payload = payload.decode("utf-8")
            print("[ingest-worker] got job:", payload)
            tenant_id, doc_id, key, mime, filename = payload.split(":", 4)
            process_upload(tenant_id, doc_id, key, mime, filename)
        except Exception as e:
            print("[ingest-worker] error:", e)

if __name__ == "__main__":
    worker_loop()

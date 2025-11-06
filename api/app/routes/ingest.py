

from fastapi import APIRouter, UploadFile, File, Depends
from ..deps import get_current_tenant
from ..utils.storage import put_object
from ..config import settings
from redis import Redis
import psycopg, uuid

router = APIRouter(prefix="/v1/ingest", tags=["ingest"])

@router.post("/upload")
async def upload(file: UploadFile = File(...), tenant_id: str = Depends(get_current_tenant)):
    data = await file.read()
    key = f"{tenant_id}/{uuid.uuid4()}_{file.filename}"
    put_object(key, data, file.content_type or "application/octet-stream")

    with psycopg.connect(
        host=settings.pg_host,
        port=settings.pg_port,
        dbname=settings.pg_db,
        user=settings.pg_user,
        password=settings.pg_pass,
        autocommit=True,
    ) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT set_config('app.current_tenant', %s, true)", (tenant_id,))
            cur.execute(
                """
                INSERT INTO documents(tenant_id, filename, source, mime_type, size_bytes, s3_uri)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (tenant_id, file.filename, "upload", file.content_type, len(data), key),
            )
            doc_id = cur.fetchone()[0]

    r = Redis.from_url(settings.redis_url)
    r.rpush("ingest_queue", f"{tenant_id}:{doc_id}:{key}:{file.content_type or ''}:{file.filename}")
    return {"document_id": str(doc_id), "s3_key": key}

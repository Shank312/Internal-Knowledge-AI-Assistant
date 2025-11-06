

import os, io, pathlib, psycopg, boto3
from psycopg.rows import dict_row
from .parsers import parse_pdf, parse_docx, parse_pptx, parse_table, parse_txt
from .api_like_chunker import chunk_text, embed_texts

PG = dict(
    host=os.getenv("POSTGRES_HOST","localhost"),
    port=int(os.getenv("POSTGRES_PORT","5432")),
    dbname=os.getenv("POSTGRES_DB","company_brain"),
    user=os.getenv("POSTGRES_USER","brain"),
    password=os.getenv("POSTGRES_PASSWORD","brainpass"),
)

MINIO = dict(
    endpoint_url=os.getenv("MINIO_ENDPOINT_URL","http://localhost:9000"),
    aws_access_key_id=os.getenv("MINIO_ROOT_USER","minio"),
    aws_secret_access_key=os.getenv("MINIO_ROOT_PASSWORD","minio123"),
    region_name=os.getenv("MINIO_REGION","us-east-1"),
    bucket=os.getenv("MINIO_BUCKET","company-brain"),
)

def s3_client():
    return boto3.client(
        "s3",
        endpoint_url=MINIO["endpoint_url"],
        aws_access_key_id=MINIO["aws_access_key_id"],
        aws_secret_access_key=MINIO["aws_secret_access_key"],
        region_name=MINIO["region_name"],
    )

def download_s3(key: str) -> bytes:
    s3 = s3_client()
    bio = io.BytesIO()
    s3.download_fileobj(MINIO["bucket"], key, bio)
    bio.seek(0)
    return bio.read()

def process_upload(tenant_id: str, doc_id: str, key: str, mime: str, filename: str):
    data = download_s3(key)
    ext = pathlib.Path(filename).suffix.lower()

    if (mime and "pdf" in mime) or ext == ".pdf":
        text = parse_pdf(data)
    elif ext == ".docx":
        text = parse_docx(data)
    elif ext == ".pptx":
        text = parse_pptx(data)
    elif ext in (".csv", ".xlsx", ".xls"):
        text = parse_table(data, ext)
    else:
        text = parse_txt(data)

    chunks = chunk_text(text, max_len=1200, overlap=120)
    embeddings = embed_texts(chunks)

    with psycopg.connect(**PG, autocommit=True, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT set_config('app.current_tenant', %s, true)", (tenant_id,))
            for idx, (ch, emb) in enumerate(zip(chunks, embeddings)):
                cur.execute(
                    """
                    INSERT INTO chunks(tenant_id, document_id, chunk_index, content, metadata, embedding, fts)
                    VALUES (%s, %s, %s, %s, '{}'::jsonb, %s, to_tsvector('simple', unaccent(%s)))
                    """,
                    (tenant_id, doc_id, idx, ch, emb, ch),
                )

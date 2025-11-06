

import psycopg
from psycopg.rows import dict_row
from .config import settings
from .embedder import embed_query

def _set_tenant(cur, tenant_id: str):
    cur.execute("SELECT set_config('app.current_tenant', %s, true)", (tenant_id,))

def hybrid_search(query: str, tenant_id: str, top_k: int | None = None) -> list[dict]:
    top_k = top_k or settings.top_k
    q_emb = embed_query(query)

    with psycopg.connect(
        host=settings.pg_host,
        port=settings.pg_port,
        dbname=settings.pg_db,
        user=settings.pg_user,
        password=settings.pg_pass,
        autocommit=True,
        row_factory=dict_row,
    ) as conn:
        with conn.cursor() as cur:
            _set_tenant(cur, tenant_id)
            cur.execute(
                """
                WITH q AS (
                  SELECT %s::vector AS qv,
                         plainto_tsquery('simple', unaccent(%s)) AS qts
                )
                SELECT
                  c.id,
                  c.document_id,
                  d.filename,
                  c.content,
                  0.5 * (1 - (c.embedding <=> (SELECT qv FROM q)))
                  + 0.5 * ts_rank_cd(c.fts, (SELECT qts FROM q))
                  AS score
                FROM chunks c
                JOIN documents d ON d.id = c.document_id
                WHERE c.fts @@ (SELECT qts FROM q)
                   OR c.embedding IS NOT NULL
                ORDER BY score DESC
                LIMIT %s
                """,
                (q_emb, query, top_k),
            )
            return cur.fetchall()

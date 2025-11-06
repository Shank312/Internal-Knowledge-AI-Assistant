

ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE chunks ENABLE ROW LEVEL SECURITY;

CREATE POLICY doc_isolation ON documents
USING (tenant_id = current_setting('app.current_tenant', true));

CREATE POLICY chunk_isolation ON chunks
USING (tenant_id = current_setting('app.current_tenant', true));



from fastapi import Header, HTTPException
from .config import settings

def get_current_tenant(authorization: str | None = Header(default=None)) -> str:
    # Replace with real JWT/SSO mapping in prod
    tenant_id = settings.default_tenant_id
    if not tenant_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return tenant_id

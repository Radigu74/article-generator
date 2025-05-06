from fastapi import Request, HTTPException
from crud import get_client_by_key

async def api_key_auth(request: Request, db):
    key = request.headers.get("X-API-KEY")
    client = get_client_by_key(db, key)
    if not client:
        raise HTTPException(401, "Invalid API key")
    request.state.client = client

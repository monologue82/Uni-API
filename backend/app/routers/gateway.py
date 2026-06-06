from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.cache import route_cache
from app.database import get_db
from app.models import ApiKey
from app.services.proxy import proxy_request

router = APIRouter(tags=["gateway"])


def extract_api_key(request: Request) -> str | None:
    """Extract Uni-API key from Authorization: Bearer or X-API-Key header."""
    # Try Authorization: Bearer ua-xxxxx
    auth = request.headers.get("authorization", "")
    if auth.lower().startswith("bearer ua-"):
        return auth[7:].strip()
    # Try X-API-Key header
    xkey = request.headers.get("x-api-key", "")
    if xkey.startswith("ua-"):
        return xkey.strip()
    return None


async def validate_api_key(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> ApiKey:
    """Validate the Uni-API key and return the ApiKey record."""
    key = extract_api_key(request)
    if not key:
        raise HTTPException(
            status_code=401,
            detail="Missing Uni-API key. Pass it via 'Authorization: Bearer ua-xxx' or 'X-API-Key: ua-xxx'",
        )
    result = await db.execute(select(ApiKey).where(ApiKey.key == key))
    api_key = result.scalar_one_or_none()
    if not api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    if not api_key.is_active:
        raise HTTPException(status_code=403, detail="API key is disabled")
    return api_key


@router.api_route(
    "/{route_name}/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
)
async def gateway(
    route_name: str,
    path: str,
    request: Request,
    api_key: ApiKey = Depends(validate_api_key),
    db: AsyncSession = Depends(get_db),
):
    route = route_cache.get(route_name)
    if route is None:
        raise HTTPException(status_code=404, detail=f"Route '{route_name}' not found")

    body = await request.body()
    query_params = str(request.query_params)

    return await proxy_request(
        route=route,
        path=path,
        method=request.method,
        headers=dict(request.headers),
        query_params=query_params,
        body=body,
        user=api_key.name,
    )

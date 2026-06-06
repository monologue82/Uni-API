from fastapi import APIRouter, Request, HTTPException

from app.core.cache import route_cache
from app.services.proxy import proxy_request

router = APIRouter(tags=["gateway"])


@router.api_route(
    "/{route_name}/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
)
async def gateway(
    route_name: str,
    path: str,
    request: Request,
):
    # API key 已由 ApiKeyMiddleware 全局验证，name 存于 request.state
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
        user=getattr(request.state, "api_key_name", ""),
    )

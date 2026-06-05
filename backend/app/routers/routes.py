from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Route
from app.schemas import RouteCreate, RouteUpdate, RouteResponse, RouteListResponse, RouteTestResponse
from app.services import route_service
from app.services.route_service import route_to_response

router = APIRouter(prefix="/routes", tags=["routes"])


@router.get("", response_model=RouteListResponse)
async def list_routes(db: AsyncSession = Depends(get_db)):
    routes = await route_service.list_routes(db)
    return RouteListResponse(
        total=len(routes),
        items=[RouteResponse(**route_to_response(r)) for r in routes],
    )


@router.post("", response_model=RouteResponse, status_code=201)
async def create_route(data: RouteCreate, db: AsyncSession = Depends(get_db)):
    existing = await route_service.get_route_by_name(db, data.name)
    if existing:
        raise HTTPException(status_code=409, detail=f"Route '{data.name}' already exists")
    route = await route_service.create_route(db, data)
    return RouteResponse(**route_to_response(route))


@router.get("/{route_id}", response_model=RouteResponse)
async def get_route(route_id: int, db: AsyncSession = Depends(get_db)):
    route = await route_service.get_route(db, route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    route.api_key = ""
    return RouteResponse(**route_to_response(route))


@router.put("/{route_id}", response_model=RouteResponse)
async def update_route(route_id: int, data: RouteUpdate, db: AsyncSession = Depends(get_db)):
    route = await route_service.get_route(db, route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    if data.name and data.name != route.name:
        existing = await route_service.get_route_by_name(db, data.name)
        if existing:
            raise HTTPException(status_code=409, detail=f"Route '{data.name}' already exists")
    route = await route_service.update_route(db, route, data)
    return RouteResponse(**route_to_response(route))


@router.delete("/{route_id}", status_code=204)
async def delete_route(route_id: int, db: AsyncSession = Depends(get_db)):
    route = await route_service.get_route(db, route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    await route_service.delete_route(db, route)


@router.post("/{route_id}/test", response_model=RouteTestResponse)
async def test_route(route_id: int, db: AsyncSession = Depends(get_db)):
    route = await route_service.get_route(db, route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    import httpx
    from app.services.crypto import decrypt

    api_key = decrypt(route.api_key)
    headers = {}
    if api_key:
        headers[route.api_key_header] = f"{route.api_key_prefix}{api_key}"

    try:
        async with httpx.AsyncClient(trust_env=False, timeout=10) as client:
            resp = await client.get(route.base_url, headers=headers)
        return RouteTestResponse(
            success=resp.status_code < 500,
            status_code=resp.status_code,
            message=f"Status: {resp.status_code}",
        )
    except httpx.ConnectError:
        return RouteTestResponse(success=False, status_code=None, message=f"Connection refused: {route.base_url}")
    except httpx.TimeoutException:
        return RouteTestResponse(success=False, status_code=None, message=f"Connection timeout: {route.base_url}")
    except Exception as exc:
        return RouteTestResponse(success=False, status_code=None, message=str(exc))

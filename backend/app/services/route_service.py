from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Route
from app.schemas import RouteCreate, RouteUpdate
from app.services.crypto import encrypt, decrypt
from app.core.cache import route_cache


async def list_routes(db: AsyncSession) -> list[Route]:
    result = await db.execute(select(Route).order_by(Route.id))
    return list(result.scalars().all())


async def get_route(db: AsyncSession, route_id: int) -> Route | None:
    result = await db.execute(select(Route).where(Route.id == route_id))
    return result.scalar_one_or_none()


async def get_route_by_name(db: AsyncSession, name: str) -> Route | None:
    result = await db.execute(select(Route).where(Route.name == name))
    return result.scalar_one_or_none()


async def create_route(db: AsyncSession, data: RouteCreate) -> Route:
    route = Route(
        name=data.name,
        base_url=data.base_url,
        description=data.description,
        api_key=encrypt(data.api_key) if data.api_key else "",
        api_key_header=data.api_key_header,
        api_key_prefix=data.api_key_prefix,
        api_type=data.api_type,
        is_active=data.is_active,
        timeout=data.timeout,
    )
    db.add(route)
    await db.commit()
    await db.refresh(route)
    route.api_key = decrypt(route.api_key)
    if route.is_active:
        await route_cache.add_or_update(route)
    return route


async def update_route(db: AsyncSession, route: Route, data: RouteUpdate) -> Route:
    if data.name is not None:
        route.name = data.name
    if data.base_url is not None:
        route.base_url = data.base_url
    if data.description is not None:
        route.description = data.description
    if data.api_key is not None:
        route.api_key = encrypt(data.api_key) if data.api_key else ""
    if data.api_key_header is not None:
        route.api_key_header = data.api_key_header
    if data.api_key_prefix is not None:
        route.api_key_prefix = data.api_key_prefix
    if data.api_type is not None:
        route.api_type = data.api_type
    if data.is_active is not None:
        route.is_active = data.is_active
    if data.timeout is not None:
        route.timeout = data.timeout

    await db.commit()
    await db.refresh(route)
    route.api_key = decrypt(route.api_key)

    if route.is_active:
        await route_cache.add_or_update(route)
    else:
        await route_cache.remove(route.name)

    return route


async def delete_route(db: AsyncSession, route: Route) -> None:
    name = route.name
    await db.delete(route)
    await db.commit()
    await route_cache.remove(name)


def route_to_response(route: Route) -> dict:
    return {
        "id": route.id,
        "name": route.name,
        "base_url": route.base_url,
        "description": route.description,
        "api_key_header": route.api_key_header,
        "api_key_prefix": route.api_key_prefix,
        "api_type": route.api_type,
        "is_active": route.is_active,
        "timeout": route.timeout,
        "created_at": route.created_at,
        "updated_at": route.updated_at,
    }

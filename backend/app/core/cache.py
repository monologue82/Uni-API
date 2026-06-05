import asyncio
import logging
from dataclasses import dataclass

logger = logging.getLogger("uniapi.cache")


@dataclass
class RouteConfig:
    id: int
    name: str
    base_url: str
    api_key: str
    api_key_header: str
    api_key_prefix: str
    timeout: int


class RouteCache:
    def __init__(self):
        self._routes: dict[str, RouteConfig] = {}
        self._lock = asyncio.Lock()

    def get(self, name: str) -> RouteConfig | None:
        return self._routes.get(name)

    def get_all(self) -> list[RouteConfig]:
        return list(self._routes.values())

    async def refresh(self, db_session):
        from sqlalchemy import select
        from app.models import Route
        from app.services.crypto import decrypt

        result = await db_session.execute(
            select(Route).where(Route.is_active == True)
        )
        rows = result.scalars().all()

        new_routes: dict[str, RouteConfig] = {}
        for row in rows:
            new_routes[row.name] = RouteConfig(
                id=row.id,
                name=row.name,
                base_url=row.base_url.rstrip("/"),
                api_key=decrypt(row.api_key),
                api_key_header=row.api_key_header,
                api_key_prefix=row.api_key_prefix,
                timeout=row.timeout,
            )

        async with self._lock:
            self._routes = new_routes

        logger.info("Route cache refreshed: %d routes loaded", len(new_routes))

    async def add_or_update(self, route):
        config = RouteConfig(
            id=route.id,
            name=route.name,
            base_url=route.base_url.rstrip("/"),
            api_key=route.api_key,
            api_key_header=route.api_key_header,
            api_key_prefix=route.api_key_prefix,
            timeout=route.timeout,
        )
        async with self._lock:
            self._routes[route.name] = config

    async def remove(self, name: str):
        async with self._lock:
            self._routes.pop(name, None)


route_cache = RouteCache()

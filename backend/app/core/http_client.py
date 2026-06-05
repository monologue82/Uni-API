import logging

import httpx

from app.config import settings

logger = logging.getLogger("uniapi.http")

http_client: httpx.AsyncClient | None = None


async def init_http_client():
    global http_client
    http_client = httpx.AsyncClient(
        trust_env=False,
        limits=httpx.Limits(
            max_connections=settings.max_connections,
            max_keepalive_connections=settings.max_keepalive_connections,
            keepalive_expiry=settings.keepalive_expiry,
        ),
        timeout=httpx.Timeout(
            connect=5.0,
            read=settings.default_timeout,
            write=settings.default_timeout,
            pool=5.0,
        ),
    )
    logger.info(
        "HTTP client initialized (max_connections=%d, keepalive=%d)",
        settings.max_connections,
        settings.max_keepalive_connections,
    )


async def close_http_client():
    global http_client
    if http_client:
        await http_client.aclose()
        http_client = None
        logger.info("HTTP client closed")


def get_http_client() -> httpx.AsyncClient:
    if http_client is None:
        raise RuntimeError("HTTP client not initialized")
    return http_client

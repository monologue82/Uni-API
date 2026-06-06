import logging

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from sqlalchemy import select

from app.database import async_session_factory
from app.models import ApiKey

logger = logging.getLogger("uniapi.apikey")

# Paths that remain public (no API key required)
# Auth/setup/health are fully public; management endpoints use JWT instead
PUBLIC_PATHS = (
    "/api/v1/auth/",
    "/api/v1/setup/",
    "/api/v1/health",
    "/api/v1/routes",
    "/api/v1/logs",
    "/api/v1/apikeys",
    "/api/v1/monitoring",
    "/api/v1/routes/types",
)


class ApiKeyMiddleware(BaseHTTPMiddleware):
    """Require a valid API key for all /api/v1 requests except public paths."""

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Only enforce on /api/v1 paths
        if not path.startswith("/api/v1/"):
            return await call_next(request)

        # Allow public paths
        if any(path.startswith(p) for p in PUBLIC_PATHS):
            return await call_next(request)

        # Allow CORS preflight
        if request.method == "OPTIONS":
            return await call_next(request)

        # Extract API key
        key = self._extract_key(request)
        if not key:
            return JSONResponse(
                status_code=401,
                content={"detail": "Missing API key. Pass via 'Authorization: Bearer ua-xxx' or 'X-API-Key: ua-xxx'"},
            )

        # Validate against database
        try:
            async with async_session_factory() as session:
                result = await session.execute(
                    select(ApiKey).where(ApiKey.key == key)
                )
                api_key = result.scalar_one_or_none()
        except Exception:
            logger.exception("API key validation database error")
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error during authentication"},
            )

        if not api_key:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid API key"},
            )

        if not api_key.is_active:
            return JSONResponse(
                status_code=403,
                content={"detail": "API key is disabled"},
            )

        # Attach key name to request state for downstream logging
        request.state.api_key_name = api_key.name
        return await call_next(request)

    @staticmethod
    def _extract_key(request: Request) -> str | None:
        # Authorization: Bearer ua-xxx
        auth = request.headers.get("authorization", "")
        if auth.lower().startswith("bearer ua-"):
            return auth[7:].strip()
        # X-API-Key: ua-xxx
        xkey = request.headers.get("x-api-key", "")
        if xkey.startswith("ua-"):
            return xkey.strip()
        return None

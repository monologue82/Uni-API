"""
Access log middleware.

Logs every /api/v1 request at INFO level and feeds data to the metrics collector.
Also generates and propagates a request_id via contextvars for distributed tracing.
"""

import time
import uuid
import logging
from contextvars import ContextVar

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.core.metrics import metrics_collector

logger = logging.getLogger("uniapi.access")

# Context variable for request_id, usable anywhere in the async call chain
request_id_var: ContextVar[str] = ContextVar("request_id", default="")


class AccessLogMiddleware(BaseHTTPMiddleware):
    """Log every request and record metrics."""

    async def dispatch(self, request: Request, call_next):
        # Skip non-API and health check requests for access logging
        path = request.url.path
        if not path.startswith("/api/v1/"):
            return await call_next(request)

        # Generate or extract request_id
        rid = request.headers.get("x-request-id") or str(uuid.uuid4())
        request_id_var.set(rid)

        start = time.monotonic()
        status = 500
        try:
            response = await call_next(request)
            status = response.status_code
            # Inject request_id into response headers
            response.headers["x-request-id"] = rid
            return response
        except Exception:
            status = 500
            raise
        finally:
            elapsed = (time.monotonic() - start) * 1000

            # Extract route name from path: /api/v1/gateway/{route_name}/...
            route_name = ""
            parts = path.split("/")
            if len(parts) > 4 and parts[3] == "gateway":
                route_name = parts[4]

            # Log at INFO level (visible in production)
            logger.info(
                "%s %s → %d (%.1fms) [%s]",
                request.method,
                path,
                status,
                elapsed,
                rid[:8],
            )

            # Record metrics (skip health check to avoid noise)
            if path != "/api/v1/health":
                try:
                    await metrics_collector.record(
                        method=request.method,
                        path=path,
                        status=status,
                        duration_ms=elapsed,
                        route_name=route_name,
                    )
                except Exception:
                    pass  # Never let metrics errors break the request

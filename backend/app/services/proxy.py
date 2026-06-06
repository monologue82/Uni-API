import time
import uuid
import logging

from fastapi import Response
from fastapi.responses import StreamingResponse
from starlette.background import BackgroundTask

from app.core.cache import RouteConfig
from app.core.http_client import get_http_client
from app.middleware.access_log import request_id_var

logger = logging.getLogger("uniapi.proxy")

TRACE_REQUEST_HEADER = "x-request-id"
TRACE_ROUTE_HEADER = "x-uniapi-route"
TRACE_TARGET_HEADER = "x-uniapi-target"
TRACE_DURATION_HEADER = "x-uniapi-duration-ms"

FORBIDDEN_REQUEST_HEADERS = {
    "host",
    "content-length",
    "transfer-encoding",
    "connection",
    "keep-alive",
}

FORBIDDEN_RESPONSE_HEADERS = {
    "transfer-encoding",
    "content-length",
    "connection",
    "keep-alive",
}


async def proxy_request(
    route: RouteConfig,
    path: str,
    method: str,
    headers: dict,
    query_params: str,
    body: bytes,
    user: str = "",
) -> StreamingResponse:
    start_time = time.monotonic()

    request_id = _extract_or_generate_request_id(headers)
    request_id_var.set(request_id)

    target_url = _build_url(route.base_url, path, query_params)
    request_headers = _prepare_request_headers(headers, route)
    request_headers[TRACE_REQUEST_HEADER] = request_id

    client = get_http_client()

    logger.info("Proxy %s [%s] %s → %s", request_id, method, path, target_url)

    try:
        req = client.build_request(
            method=method,
            url=target_url,
            headers=request_headers,
            content=body if body else None,
        )
        resp = await client.send(req, stream=True)
    except Exception as exc:
        elapsed = int((time.monotonic() - start_time) * 1000)
        logger.warning("Proxy failed [%s] %s %s: %s (%dms)", request_id, method, target_url, exc, elapsed)
        return _error_response(request_id, route.name, target_url, 502, str(exc), elapsed)

    elapsed = int((time.monotonic() - start_time) * 1000)
    response_headers = _filter_response_headers(dict(resp.headers))
    _inject_trace_headers(response_headers, request_id, route.name, target_url, elapsed)

    bg_log = BackgroundTask(
        _log_call, route.id, route.name, method, path, resp.status_code, elapsed, request_id, user
    )

    logger.info("Proxy done [%s] %s %s → %d (%dms)", request_id, method, target_url, resp.status_code, elapsed)

    return StreamingResponse(
        content=resp.aiter_raw(),
        status_code=resp.status_code,
        headers=response_headers,
        background=bg_log,
    )


def _extract_or_generate_request_id(headers: dict) -> str:
    for key, value in headers.items():
        if key.lower() == TRACE_REQUEST_HEADER:
            return value
    return str(uuid.uuid4())


def _inject_trace_headers(
    headers: dict,
    request_id: str,
    route_name: str,
    target_url: str,
    duration_ms: int,
) -> None:
    headers[TRACE_REQUEST_HEADER] = request_id
    headers[TRACE_ROUTE_HEADER] = route_name
    headers[TRACE_TARGET_HEADER] = target_url
    headers[TRACE_DURATION_HEADER] = str(duration_ms)


def _build_url(base_url: str, path: str, query_params: str) -> str:
    url = f"{base_url}/{path.lstrip('/')}"
    if query_params:
        url = f"{url}?{query_params}"
    return url


def _prepare_request_headers(headers: dict, route: RouteConfig) -> dict:
    cleaned = {
        k: v
        for k, v in headers.items()
        if k.lower() not in FORBIDDEN_REQUEST_HEADERS
    }

    if route.api_key:
        key_header = route.api_key_header or "Authorization"
        key_value = f"{route.api_key_prefix}{route.api_key}"
        cleaned[key_header] = key_value

    return cleaned


def _filter_response_headers(headers: dict) -> dict:
    return {
        k: v
        for k, v in headers.items()
        if k.lower() not in FORBIDDEN_RESPONSE_HEADERS
    }


def _error_response(
    request_id: str,
    route_name: str,
    target_url: str,
    status_code: int,
    message: str,
    duration_ms: int,
) -> Response:
    headers = {
        "Content-Type": "application/json",
    }
    _inject_trace_headers(headers, request_id, route_name, target_url, duration_ms)
    return Response(
        content=f'{{"error":"proxy_error","message":"{message}","request_id":"{request_id}","duration_ms":{duration_ms}}}',
        status_code=status_code,
        headers=headers,
    )


async def _log_call(
    route_id: int,
    route_name: str,
    method: str,
    path: str,
    status_code: int,
    duration_ms: int,
    request_id: str,
    user: str = "",
):
    try:
        from app.database import async_session_factory
        from app.models import CallLog

        async with async_session_factory() as session:
            log = CallLog(
                route_id=route_id,
                route_name=route_name,
                method=method,
                path=path[:500],
                status_code=status_code,
                duration_ms=duration_ms,
                user=user,
                error_message=request_id,
            )
            session.add(log)
            await session.commit()
    except Exception:
        pass

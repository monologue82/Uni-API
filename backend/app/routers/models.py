import logging

import httpx
from fastapi import APIRouter, HTTPException, Query
from app.services.api_types import get_type_by_id
from app.core.http_client import get_http_client

logger = logging.getLogger("uniapi.models")

router = APIRouter(prefix="/models", tags=["models"])


def _extract_models(data: dict, key_path: str) -> list[str]:
    """Extract model IDs from response data using a dot-path like 'data.*.id'."""
    parts = key_path.split(".")
    current = data

    for part in parts:
        if part == "*":
            # Wildcard: iterate over list items, extract remaining path from each
            if not isinstance(current, list):
                return []
            remaining = ".".join(parts[parts.index("*") + 1:])
            results = []
            for item in current:
                results.extend(_extract_models(item, remaining) if remaining else [str(item)])
            return results
        if isinstance(current, dict):
            current = current.get(part)
        else:
            return []

    # No wildcard — if we landed on a list of dicts, extract the last key
    if isinstance(current, list) and parts:
        field = parts[-1]
        return [item.get(field, "") for item in current if isinstance(item, dict) and item.get(field)]
    return []


@router.get("/{type_id}")
async def fetch_models(
    type_id: str,
    api_key: str = Query(default=""),
):
    """Fetch available models from a provider using the provided API key."""
    preset = get_type_by_id(type_id)
    if not preset:
        raise HTTPException(status_code=404, detail="Preset not found")

    models_endpoint = preset.get("models_endpoint")
    if not models_endpoint:
        raise HTTPException(status_code=400, detail="This provider does not support model listing")

    base_url = preset.get("base_url", "")
    if not base_url:
        raise HTTPException(status_code=400, detail="No base URL configured for this provider")

    url = base_url.rstrip("/") + models_endpoint

    # Build headers
    headers = {}
    api_key_header = preset.get("api_key_header", "")
    api_key_prefix = preset.get("api_key_prefix", "")
    if api_key and api_key_header:
        headers[api_key_header] = f"{api_key_prefix}{api_key}"

    logger.info("Fetching models: GET %s (key_header=%s, key=%s***, prefix=%r)", url, api_key_header, api_key[:6] if api_key else "", api_key_prefix)

    try:
        client = get_http_client()
        resp = await client.get(url, headers=headers, timeout=10)
        logger.info("Upstream response: %d %s", resp.status_code, resp.reason_phrase)
        resp.raise_for_status()
        data = resp.json()
    except httpx.HTTPStatusError as e:
        # Try to extract the upstream error message from the response body
        upstream_detail = ""
        try:
            err_body = e.response.json()
            upstream_detail = err_body.get("error", {}).get("message", "") or err_body.get("message", "")
        except Exception:
            upstream_detail = e.response.text[:200] if e.response.text else ""

        if e.response.status_code in (401, 403):
            msg = "Authentication failed — please check your API key"
            if upstream_detail:
                msg += f" ({upstream_detail})"
            raise HTTPException(status_code=502, detail=msg)
        raise HTTPException(status_code=502, detail=f"Failed to fetch models: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch models: {str(e)}")

    models_key = preset.get("models_key", "")
    if not models_key:
        raise HTTPException(status_code=400, detail="No models_key configured for this provider")

    models = _extract_models(data, models_key)
    return {"models": sorted(models)}

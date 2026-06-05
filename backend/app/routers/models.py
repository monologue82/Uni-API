from fastapi import APIRouter, HTTPException, Query
from app.services.api_types import get_type_by_id
from app.core.http_client import get_http_client

router = APIRouter(prefix="/models", tags=["models"])


def _extract_models(data: dict, key_path: str) -> list[str]:
    """Extract model IDs from response data using a dot-path like 'data.*.id'."""
    parts = key_path.split(".")
    current = data
    for part in parts:
        if part == "*":
            continue
        if isinstance(current, dict):
            current = current.get(part, [])
        else:
            return []
    # If we have a list, extract the final field
    if isinstance(current, list) and len(parts) >= 2:
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

    try:
        client = get_http_client()
        resp = await client.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch models: {str(e)}")

    models_key = preset.get("models_key", "")
    if not models_key:
        raise HTTPException(status_code=400, detail="No models_key configured for this provider")

    models = _extract_models(data, models_key)
    return {"models": sorted(models)}

import secrets
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models import ApiKey, User
from app.schemas.apikey import ApiKeyCreate, ApiKeyResponse, ApiKeyListResponse
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/apikeys", tags=["apikeys"])


def generate_key() -> str:
    """Generate a random API key prefixed with 'ua-'."""
    return "ua-" + secrets.token_hex(24)


async def _build_response(api_key: ApiKey, db: AsyncSession) -> ApiKeyResponse:
    """Build ApiKeyResponse with username from User table."""
    username = None
    if api_key.user_id:
        user = await db.get(User, api_key.user_id)
        if user:
            username = user.username
    return ApiKeyResponse(
        id=api_key.id,
        key=api_key.key,
        name=api_key.name,
        user_id=api_key.user_id,
        username=username,
        is_active=api_key.is_active,
        created_at=api_key.created_at,
    )


@router.get("", response_model=ApiKeyListResponse)
async def list_api_keys(
    page: int = 1,
    page_size: int = 50,
    db: AsyncSession = Depends(get_db),
):
    total = await db.scalar(select(func.count(ApiKey.id)))
    result = await db.execute(
        select(ApiKey)
        .order_by(ApiKey.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    items = result.scalars().all()
    responses = []
    for item in items:
        responses.append(await _build_response(item, db))
    return ApiKeyListResponse(total=total or 0, items=responses)


@router.post("", response_model=ApiKeyResponse)
async def create_api_key(
    data: ApiKeyCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    key = generate_key()
    api_key = ApiKey(key=key, name=data.name, user_id=current_user.id)
    db.add(api_key)
    await db.commit()
    await db.refresh(api_key)
    return await _build_response(api_key, db)


@router.get("/{key_id}", response_model=ApiKeyResponse)
async def get_api_key(
    key_id: int,
    db: AsyncSession = Depends(get_db),
):
    api_key = await db.get(ApiKey, key_id)
    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")
    return await _build_response(api_key, db)


@router.put("/{key_id}", response_model=ApiKeyResponse)
async def update_api_key(
    key_id: int,
    data: ApiKeyCreate,
    db: AsyncSession = Depends(get_db),
):
    api_key = await db.get(ApiKey, key_id)
    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")
    api_key.name = data.name
    await db.commit()
    await db.refresh(api_key)
    return await _build_response(api_key, db)


@router.put("/{key_id}/toggle", response_model=ApiKeyResponse)
async def toggle_api_key(
    key_id: int,
    db: AsyncSession = Depends(get_db),
):
    api_key = await db.get(ApiKey, key_id)
    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")
    api_key.is_active = not api_key.is_active
    await db.commit()
    await db.refresh(api_key)
    return await _build_response(api_key, db)


@router.delete("/{key_id}")
async def delete_api_key(
    key_id: int,
    db: AsyncSession = Depends(get_db),
):
    api_key = await db.get(ApiKey, key_id)
    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")
    await db.delete(api_key)
    await db.commit()
    return {"ok": True}

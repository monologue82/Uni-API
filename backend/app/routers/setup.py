from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database import get_db
from app.models import User
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import hash_password, create_token

router = APIRouter(prefix="/setup", tags=["setup"])


@router.get("/status")
async def setup_status(db: AsyncSession = Depends(get_db)):
    count = await db.scalar(select(func.count(User.id)))
    return {"initialized": count > 0}


@router.post("/initialize", response_model=TokenResponse)
async def initialize(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    count = await db.scalar(select(func.count(User.id)))
    if count > 0:
        raise HTTPException(status_code=400, detail="Already initialized")

    if len(data.username) < 3:
        raise HTTPException(status_code=400, detail="Username must be at least 3 characters")
    if len(data.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

    user = User(
        username=data.username,
        hashed_password=hash_password(data.password),
    )
    db.add(user)
    await db.commit()

    token = create_token({"sub": user.username, "user_id": user.id})
    return TokenResponse(access_token=token)
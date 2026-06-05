from pydantic import BaseModel, Field
from datetime import datetime


class ApiKeyCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class ApiKeyResponse(BaseModel):
    id: int
    key: str
    name: str
    user_id: int | None
    username: str | None = None
    is_active: bool
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class ApiKeyListResponse(BaseModel):
    total: int
    items: list[ApiKeyResponse]

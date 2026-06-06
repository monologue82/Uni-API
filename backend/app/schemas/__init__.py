from datetime import datetime

from pydantic import BaseModel, Field


class RouteCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100, pattern=r"^[a-zA-Z0-9_-]+$")
    base_url: str = Field(min_length=1, max_length=500)
    description: str = ""
    api_key: str = ""
    api_key_header: str = "Authorization"
    api_key_prefix: str = "Bearer "
    api_type: str = "custom"
    is_active: bool = True
    timeout: int = Field(default=30, ge=1, le=300)


class RouteUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100, pattern=r"^[a-zA-Z0-9_-]+$")
    base_url: str | None = Field(default=None, min_length=1, max_length=500)
    description: str | None = None
    api_key: str | None = None
    api_key_header: str | None = None
    api_key_prefix: str | None = None
    api_type: str | None = None
    is_active: bool | None = None
    timeout: int | None = Field(default=None, ge=1, le=300)


class RouteResponse(BaseModel):
    id: int
    name: str
    base_url: str
    description: str
    api_key_header: str
    api_key_prefix: str
    api_type: str
    is_active: bool
    timeout: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class RouteListResponse(BaseModel):
    total: int
    items: list[RouteResponse]


class RouteTestResponse(BaseModel):
    success: bool
    status_code: int | None
    message: str

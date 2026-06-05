from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database import get_db
from app.models import CallLog
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/logs", tags=["logs"])


@router.get("")
async def list_logs(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
    route_id: int | None = None,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    query = select(CallLog)
    count_query = select(func.count(CallLog.id))

    if route_id is not None:
        query = query.where(CallLog.route_id == route_id)
        count_query = count_query.where(CallLog.route_id == route_id)

    total = (await db.execute(count_query)).scalar() or 0

    query = query.order_by(CallLog.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    logs = result.scalars().all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [
            {
                "id": log.id,
                "route_id": log.route_id,
                "route_name": log.route_name,
                "method": log.method,
                "path": log.path,
                "status_code": log.status_code,
                "duration_ms": log.duration_ms,
                "error_message": log.error_message,
                "created_at": log.created_at.isoformat(),
            }
            for log in logs
        ],
    }

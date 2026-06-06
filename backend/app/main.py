import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.config import settings
from app.database import engine, async_session_factory
from app.models import Base
from app.core.cache import route_cache
from app.core.http_client import init_http_client, close_http_client
from app.routers import gateway, routes, auth, logs, setup, apikeys, models, monitoring
from app.middleware.auth import get_current_user
from app.middleware.apikey import ApiKeyMiddleware
from app.middleware.access_log import AccessLogMiddleware
from app.core.system_monitor import system_monitor
from app.core.alerts import alert_manager

logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("uniapi")


async def _refresh_cache_loop():
    while True:
        await asyncio.sleep(settings.route_cache_refresh_seconds)
        try:
            async with async_session_factory() as session:
                await route_cache.refresh(session)
        except Exception:
            logger.exception("Route cache refresh failed")


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

        # Migration: add api_type column if not exists
        try:
            await conn.exec_driver_sql(
                "ALTER TABLE routes ADD COLUMN api_type VARCHAR(50) DEFAULT 'custom'"
            )
        except Exception:
            pass  # Column already exists

        # Migration: add model column if not exists
        try:
            await conn.exec_driver_sql(
                "ALTER TABLE routes ADD COLUMN model VARCHAR(200) DEFAULT ''"
            )
        except Exception:
            pass  # Column already exists

        # Migration: add user column to call_logs if not exists
        try:
            await conn.exec_driver_sql(
                "ALTER TABLE call_logs ADD COLUMN user VARCHAR(100) DEFAULT ''"
            )
        except Exception:
            pass  # Column already exists

    logger.info("Database tables created")

    async with async_session_factory() as session:
        await route_cache.refresh(session)

    await init_http_client()

    refresh_task = asyncio.create_task(_refresh_cache_loop())

    # Start monitoring background tasks
    await system_monitor.start()
    await alert_manager.start()

    yield

    # Stop monitoring
    await alert_manager.stop()
    await system_monitor.stop()

    refresh_task.cancel()
    try:
        await refresh_task
    except asyncio.CancelledError:
        pass

    await close_http_client()
    await engine.dispose()
    logger.info("Uni-API shut down")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局 API Key 鉴权（auth/setup/health 除外）
app.add_middleware(ApiKeyMiddleware)

# 访问日志 + 指标采集
app.add_middleware(AccessLogMiddleware)

# 网关入口 - 需要 API Key 认证
app.include_router(gateway.router, prefix="/api/v1/gateway")

# API 类型预设 - 公开
from app.services.api_types import get_all_types

@app.get("/api/v1/routes/types")
async def list_api_types():
    return get_all_types()

# 模型列表 - 公开
app.include_router(models.router, prefix="/api/v1")

# 管理 API - 需要认证
app.include_router(
    auth.router,
    prefix="/api/v1",
)
app.include_router(
    setup.router,
    prefix="/api/v1",
)
app.include_router(
    routes.router,
    prefix="/api/v1",
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    logs.router,
    prefix="/api/v1",
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    apikeys.router,
    prefix="/api/v1",
    dependencies=[Depends(get_current_user)],
)

# 监控 API - 需要 JWT 认证
app.include_router(
    monitoring.router,
    prefix="/api/v1",
    dependencies=[Depends(get_current_user)],
)


@app.get("/api/v1/health")
async def health_check():
    """Enhanced health check: verifies DB connectivity and reports system status."""
    health = {
        "status": "ok",
        "routes_loaded": len(route_cache.get_all()),
    }

    # Check database connectivity
    try:
        async with async_session_factory() as session:
            await session.execute(text("SELECT 1"))
        health["database"] = "ok"
    except Exception as e:
        health["database"] = "error"
        health["status"] = "degraded"

    # System resource snapshot (lightweight)
    try:
        sys_data = await system_monitor.get_current()
        health["system"] = {
            "cpu_percent": sys_data.get("cpu_percent", 0),
            "memory_percent": sys_data.get("memory_percent", 0),
            "disk_percent": sys_data.get("disk_percent", 0),
        }
    except Exception:
        health["system"] = "unavailable"

    # Active alerts
    try:
        active_alerts = alert_manager.get_active()
        health["alerts"] = len(active_alerts)
        if active_alerts:
            health["status"] = "warning"
    except Exception:
        health["alerts"] = "unavailable"

    return health

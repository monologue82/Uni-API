"""
Monitoring API endpoints.

All endpoints require JWT authentication (registered under get_current_user dependency).
"""

from fastapi import APIRouter

from app.core.metrics import metrics_collector
from app.core.system_monitor import system_monitor
from app.core.alerts import alert_manager

router = APIRouter(prefix="/monitoring", tags=["monitoring"])


@router.get("/summary")
async def get_summary():
    """Real-time metrics summary: QPS, error rate, latency, connections."""
    summary = await metrics_collector.get_summary()
    active_alerts = alert_manager.get_active()
    return {
        **summary,
        "active_alerts": len(active_alerts),
    }


@router.get("/timeseries")
async def get_timeseries():
    """Last 60 minutes of request metrics for charting."""
    return await metrics_collector.get_timeseries()


@router.get("/routes")
async def get_route_stats():
    """Per-route request statistics."""
    return await metrics_collector.get_routes()


@router.get("/system")
async def get_system():
    """Current system resource usage: CPU, memory, disk, network."""
    return await system_monitor.get_current()


@router.get("/system/timeseries")
async def get_system_timeseries():
    """Last 60 system snapshots for resource trend charts."""
    return await system_monitor.get_timeseries()


@router.get("/alerts")
async def get_alerts():
    """Current active alerts and recent alert history."""
    return {
        "active": alert_manager.get_active(),
        "history": alert_manager.get_history(),
    }

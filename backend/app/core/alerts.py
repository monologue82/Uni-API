"""
Alert manager with configurable threshold rules.

Evaluates metrics against rules and logs warnings when thresholds are exceeded.
Alerts are deduplicated — each rule fires once per breach, then auto-resolves.
"""

import time
import asyncio
import logging
from dataclasses import dataclass, field

from app.core.metrics import metrics_collector
from app.core.system_monitor import system_monitor

logger = logging.getLogger("uniapi.alerts")


@dataclass
class AlertRule:
    name: str
    description: str
    threshold: float
    unit: str = ""
    severity: str = "warning"  # warning | critical


@dataclass
class ActiveAlert:
    rule_name: str
    message: str
    value: float
    threshold: float
    severity: str
    triggered_at: float = field(default_factory=time.time)
    resolved: bool = False


# Default rules
DEFAULT_RULES = [
    AlertRule("high_error_rate", "Error rate (5min) exceeds threshold", 10.0, "%"),
    AlertRule("high_latency", "Average latency (5min) exceeds threshold", 5000.0, "ms"),
    AlertRule("high_cpu", "CPU usage exceeds threshold", 90.0, "%"),
    AlertRule("high_memory", "Memory usage exceeds threshold", 90.0, "%"),
    AlertRule("high_disk", "Disk usage exceeds threshold", 90.0, "%"),
]


class AlertManager:
    """Evaluates alert rules against metrics and system data."""

    def __init__(self):
        self._rules: dict[str, AlertRule] = {r.name: r for r in DEFAULT_RULES}
        self._active: dict[str, ActiveAlert] = {}
        self._history: list[ActiveAlert] = []  # last 100 resolved alerts
        self._task: asyncio.Task | None = None

    async def start(self, interval: int = 15):
        self._task = asyncio.create_task(self._eval_loop(interval))
        logger.info("AlertManager started (interval=%ds, rules=%d)", interval, len(self._rules))

    async def stop(self):
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    def get_active(self) -> list[dict]:
        return [
            {
                "rule": a.rule_name,
                "message": a.message,
                "value": round(a.value, 2),
                "threshold": a.threshold,
                "severity": a.severity,
                "triggered_at": a.triggered_at,
                "duration_seconds": int(time.time() - a.triggered_at),
            }
            for a in self._active.values()
            if not a.resolved
        ]

    def get_history(self, limit: int = 50) -> list[dict]:
        return [
            {
                "rule": a.rule_name,
                "message": a.message,
                "value": round(a.value, 2),
                "threshold": a.threshold,
                "severity": a.severity,
                "triggered_at": a.triggered_at,
                "resolved": a.resolved,
            }
            for a in self._history[-limit:]
        ]

    # -- Internal ---------------------------------------------------------

    async def _eval_loop(self, interval: int):
        while True:
            try:
                await asyncio.sleep(interval)
                await self._evaluate()
            except asyncio.CancelledError:
                break
            except Exception:
                logger.exception("Alert evaluation failed")

    async def _evaluate(self):
        summary = await metrics_collector.get_summary()
        sys_data = await system_monitor.get_current()

        checks = [
            ("high_error_rate", summary.get("error_rate_5min", 0)),
            ("high_latency", summary.get("avg_latency_5min", 0)),
            ("high_cpu", sys_data.get("cpu_percent", 0)),
            ("high_memory", sys_data.get("memory_percent", 0)),
            ("high_disk", sys_data.get("disk_percent", 0)),
        ]

        active_names = set()

        for rule_name, value in checks:
            rule = self._rules.get(rule_name)
            if not rule:
                continue

            if value > rule.threshold:
                active_names.add(rule_name)
                if rule_name not in self._active:
                    alert = ActiveAlert(
                        rule_name=rule_name,
                        message=f"{rule.description}: {value}{rule.unit} > {rule.threshold}{rule.unit}",
                        value=value,
                        threshold=rule.threshold,
                        severity=rule.severity,
                    )
                    self._active[rule_name] = alert
                    logger.warning("ALERT [%s] %s", rule.severity.upper(), alert.message)
            else:
                # Auto-resolve
                if rule_name in self._active:
                    alert = self._active.pop(rule_name)
                    alert.resolved = True
                    self._history.append(alert)
                    if len(self._history) > 100:
                        self._history = self._history[-100:]
                    logger.info("ALERT RESOLVED: %s", rule_name)


# Global singleton
alert_manager = AlertManager()

"""
Background system resource monitor.

Periodically collects CPU, memory, disk, and network metrics using psutil.
Stores the last 60 data points (one per collection interval).
"""

import asyncio
import time
import logging
from dataclasses import dataclass, field

logger = logging.getLogger("uniapi.system")

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False
    logger.warning("psutil not installed — system monitoring disabled")


@dataclass
class SystemSnapshot:
    """A single point-in-time system resource reading."""
    timestamp: float = 0.0
    cpu_percent: float = 0.0
    memory_percent: float = 0.0
    memory_used_mb: float = 0.0
    memory_total_mb: float = 0.0
    disk_percent: float = 0.0
    disk_used_gb: float = 0.0
    disk_total_gb: float = 0.0
    net_sent_mb: float = 0.0
    net_recv_mb: float = 0.0
    net_sent_rate: float = 0.0  # MB/s since last sample
    net_recv_rate: float = 0.0
    process_count: int = 0
    open_files: int = 0


class SystemMonitor:
    """Collects system metrics in a background loop."""

    def __init__(self, interval: int = 5, window: int = 60):
        self._interval = interval
        self._window = window
        self._snapshots: list[SystemSnapshot] = []
        self._task: asyncio.Task | None = None
        self._prev_net_sent: float = 0
        self._prev_net_recv: float = 0
        self._prev_time: float = 0

    async def start(self):
        if not HAS_PSUTIL:
            logger.warning("SystemMonitor not started — psutil unavailable")
            return
        self._task = asyncio.create_task(self._collect_loop())
        logger.info("SystemMonitor started (interval=%ds)", self._interval)

    async def stop(self):
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    async def get_current(self) -> dict:
        if not HAS_PSUTIL:
            return {"error": "psutil not installed"}

        if self._snapshots:
            s = self._snapshots[-1]
        else:
            s = self._collect()

        return {
            "timestamp": s.timestamp,
            "cpu_percent": s.cpu_percent,
            "memory_percent": s.memory_percent,
            "memory_used_mb": round(s.memory_used_mb, 1),
            "memory_total_mb": round(s.memory_total_mb, 1),
            "disk_percent": s.disk_percent,
            "disk_used_gb": round(s.disk_used_gb, 2),
            "disk_total_gb": round(s.disk_total_gb, 2),
            "net_sent_mb": round(s.net_sent_mb, 2),
            "net_recv_mb": round(s.net_recv_mb, 2),
            "net_sent_rate": round(s.net_sent_rate, 3),
            "net_recv_rate": round(s.net_recv_rate, 3),
            "process_count": s.process_count,
            "open_files": s.open_files,
        }

    async def get_timeseries(self) -> list[dict]:
        return [
            {
                "timestamp": s.timestamp,
                "cpu": s.cpu_percent,
                "memory": s.memory_percent,
                "disk": s.disk_percent,
                "net_sent_rate": round(s.net_sent_rate, 3),
                "net_recv_rate": round(s.net_recv_rate, 3),
            }
            for s in self._snapshots
        ]

    # -- Internal ---------------------------------------------------------

    async def _collect_loop(self):
        while True:
            try:
                await asyncio.sleep(self._interval)
                snapshot = await asyncio.to_thread(self._collect)
                self._snapshots.append(snapshot)
                # Trim to window
                if len(self._snapshots) > self._window:
                    self._snapshots = self._snapshots[-self._window:]
            except asyncio.CancelledError:
                break
            except Exception:
                logger.exception("System snapshot failed")

    def _collect(self) -> SystemSnapshot:
        now = time.time()
        s = SystemSnapshot(timestamp=now)

        try:
            s.cpu_percent = psutil.cpu_percent(interval=0)
        except Exception:
            pass

        try:
            mem = psutil.virtual_memory()
            s.memory_percent = mem.percent
            s.memory_used_mb = mem.used / (1024 * 1024)
            s.memory_total_mb = mem.total / (1024 * 1024)
        except Exception:
            pass

        try:
            disk = psutil.disk_usage("/")
            s.disk_percent = disk.percent
            s.disk_used_gb = disk.used / (1024 ** 3)
            s.disk_total_gb = disk.total / (1024 ** 3)
        except Exception:
            pass

        try:
            net = psutil.net_io_counters()
            s.net_sent_mb = net.bytes_sent / (1024 * 1024)
            s.net_recv_mb = net.bytes_recv / (1024 * 1024)

            elapsed = now - self._prev_time if self._prev_time else 0
            if elapsed > 0:
                s.net_sent_rate = (net.bytes_sent - self._prev_net_sent) / (1024 * 1024) / elapsed
                s.net_recv_rate = (net.bytes_recv - self._prev_net_recv) / (1024 * 1024) / elapsed

            self._prev_net_sent = net.bytes_sent
            self._prev_net_recv = net.bytes_recv
            self._prev_time = now
        except Exception:
            pass

        try:
            s.process_count = len(psutil.pids())
        except Exception:
            pass

        try:
            proc = psutil.Process()
            s.open_files = proc.num_fds() if hasattr(proc, "num_fds") else 0
        except Exception:
            pass

        return s


# Global singleton
system_monitor = SystemMonitor()

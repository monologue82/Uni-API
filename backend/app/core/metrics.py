"""
In-memory metrics collector with per-minute aggregation.

Stores the last 60 minutes of request data in a ring buffer.
Thread-safe via asyncio lock (single-event-loop assumption).
"""

import time
import asyncio
import logging
from collections import defaultdict
from dataclasses import dataclass, field

logger = logging.getLogger("uniapi.metrics")


@dataclass
class MinuteBucket:
    """One minute of aggregated metrics."""
    timestamp: int = 0  # minute epoch (time.time() // 60)
    requests: int = 0
    errors: int = 0  # status >= 500
    client_errors: int = 0  # 400 <= status < 500
    latency_sum: float = 0.0
    latency_max: float = 0.0
    latency_count: int = 0
    latency_p99_samples: list = field(default_factory=list)  # capped at 1000

    def avg_latency(self) -> float:
        return self.latency_sum / self.latency_count if self.latency_count else 0

    def p99_latency(self) -> float:
        if not self.latency_p99_samples:
            return 0
        s = sorted(self.latency_p99_samples)
        idx = int(len(s) * 0.99)
        return s[min(idx, len(s) - 1)]


@dataclass
class RouteStats:
    """Per-route aggregated stats (cumulative since startup)."""
    route_name: str = ""
    requests: int = 0
    errors: int = 0
    latency_sum: float = 0.0
    latency_max: float = 0.0
    last_status: int = 0
    last_latency: float = 0.0

    def avg_latency(self) -> float:
        return self.latency_sum / self.requests if self.requests else 0


class MetricsCollector:
    """Collects and stores request metrics in a 60-minute ring buffer."""

    def __init__(self, window: int = 60):
        self._window = window
        self._buckets: list[MinuteBucket] = []
        self._routes: dict[str, RouteStats] = {}
        self._active_connections: int = 0
        self._total_requests: int = 0
        self._total_errors: int = 0
        self._lock = asyncio.Lock()
        self._started_at: float = time.time()

    # -- Recording --------------------------------------------------------

    async def record(
        self,
        method: str,
        path: str,
        status: int,
        duration_ms: float,
        route_name: str = "",
    ):
        now_min = int(time.time() // 60)

        async with self._lock:
            self._total_requests += 1
            if status >= 500:
                self._total_errors += 1

            # Get or create current minute bucket
            bucket = self._get_or_create_bucket(now_min)
            bucket.requests += 1
            bucket.latency_sum += duration_ms
            bucket.latency_count += 1
            if duration_ms > bucket.latency_max:
                bucket.latency_max = duration_ms
            if status >= 500:
                bucket.errors += 1
            elif 400 <= status < 500:
                bucket.client_errors += 1
            # Keep a sample for p99 (cap at 1000 per minute)
            if len(bucket.latency_p99_samples) < 1000:
                bucket.latency_p99_samples.append(duration_ms)

            # Per-route stats
            if route_name:
                rs = self._routes.get(route_name)
                if rs is None:
                    rs = RouteStats(route_name=route_name)
                    self._routes[route_name] = rs
                rs.requests += 1
                rs.latency_sum += duration_ms
                if duration_ms > rs.latency_max:
                    rs.latency_max = duration_ms
                rs.last_status = status
                rs.last_latency = duration_ms
                if status >= 500:
                    rs.errors += 1

            # Trim old buckets
            self._trim(now_min)

    async def connection_open(self):
        async with self._lock:
            self._active_connections += 1

    async def connection_close(self):
        async with self._lock:
            self._active_connections = max(0, self._active_connections - 1)

    # -- Queries ----------------------------------------------------------

    async def get_summary(self) -> dict:
        async with self._lock:
            now_min = int(time.time() // 60)
            self._trim(now_min)

            # Current minute stats
            current = self._buckets[-1] if self._buckets else MinuteBucket()

            # Last 5 minutes for error rate
            recent_errors = 0
            recent_requests = 0
            recent_latency_sum = 0.0
            recent_latency_count = 0
            for b in self._buckets[-5:]:
                recent_errors += b.errors
                recent_requests += b.requests
                recent_latency_sum += b.latency_sum
                recent_latency_count += b.latency_count

            error_rate = (
                (recent_errors / recent_requests * 100) if recent_requests else 0
            )
            avg_latency = (
                recent_latency_sum / recent_latency_count
                if recent_latency_count
                else 0
            )

            return {
                "active_connections": self._active_connections,
                "total_requests": self._total_requests,
                "total_errors": self._total_errors,
                "current_qps": current.requests / 60,
                "error_rate_5min": round(error_rate, 2),
                "avg_latency_5min": round(avg_latency, 1),
                "p99_latency": round(current.p99_latency(), 1),
                "routes_count": len(self._routes),
                "uptime_seconds": int(time.time() - self._started_at),
            }

    async def get_timeseries(self) -> list[dict]:
        """Return last 60 minutes of data for charting."""
        async with self._lock:
            now_min = int(time.time() // 60)
            self._trim(now_min)

            result = []
            for b in self._buckets:
                result.append({
                    "time": b.timestamp * 60,  # epoch seconds
                    "requests": b.requests,
                    "errors": b.errors,
                    "avg_latency": round(b.avg_latency(), 1),
                    "p99_latency": round(b.p99_latency(), 1),
                    "error_rate": round(
                        (b.errors / b.requests * 100) if b.requests else 0, 2
                    ),
                })
            return result

    async def get_routes(self) -> list[dict]:
        async with self._lock:
            return [
                {
                    "route": rs.route_name,
                    "requests": rs.requests,
                    "errors": rs.errors,
                    "avg_latency": round(rs.avg_latency(), 1),
                    "max_latency": round(rs.latency_max, 1),
                    "error_rate": round(
                        (rs.errors / rs.requests * 100) if rs.requests else 0, 2
                    ),
                    "last_status": rs.last_status,
                }
                for rs in sorted(
                    self._routes.values(),
                    key=lambda r: r.requests,
                    reverse=True,
                )
            ]

    # -- Internal ---------------------------------------------------------

    def _get_or_create_bucket(self, now_min: int) -> MinuteBucket:
        if self._buckets and self._buckets[-1].timestamp == now_min:
            return self._buckets[-1]
        bucket = MinuteBucket(timestamp=now_min)
        self._buckets.append(bucket)
        return bucket

    def _trim(self, now_min: int):
        cutoff = now_min - self._window
        self._buckets = [b for b in self._buckets if b.timestamp > cutoff]


# Global singleton
metrics_collector = MetricsCollector()

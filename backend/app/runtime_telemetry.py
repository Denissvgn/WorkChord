"""Small dependency-free runtime telemetry used by probes and qualification.

The registry intentionally keeps only aggregate counters, gauges, and bounded
histogram summaries.  It never records SQL text, parameters, credentials, or
request bodies.
"""

from __future__ import annotations

from collections import defaultdict
from contextvars import ContextVar
from dataclasses import dataclass
import math
from threading import Lock
from time import monotonic
from typing import Mapping


MetricKey = tuple[str, tuple[tuple[str, str], ...]]


def _metric_key(name: str, labels: Mapping[str, str] | None = None) -> MetricKey:
    return name, tuple(sorted((labels or {}).items()))


def _render_labels(labels: tuple[tuple[str, str], ...]) -> str:
    if not labels:
        return ""
    escaped = [
        f'{key}="{value.replace(chr(92), chr(92) * 2).replace(chr(34), chr(92) + chr(34))}"'
        for key, value in labels
    ]
    return "{" + ",".join(escaped) + "}"


class MetricRegistry:
    """Process-local Prometheus-compatible aggregate registry."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._counters: dict[MetricKey, float] = defaultdict(float)
        self._gauges: dict[MetricKey, float] = {}
        self._histograms: dict[MetricKey, tuple[int, float, float]] = {}

    def increment(
        self,
        name: str,
        amount: float = 1.0,
        *,
        labels: Mapping[str, str] | None = None,
    ) -> None:
        with self._lock:
            self._counters[_metric_key(name, labels)] += amount

    def set_gauge(
        self,
        name: str,
        value: float,
        *,
        labels: Mapping[str, str] | None = None,
    ) -> None:
        with self._lock:
            self._gauges[_metric_key(name, labels)] = float(value)

    def add_gauge(
        self,
        name: str,
        amount: float,
        *,
        labels: Mapping[str, str] | None = None,
    ) -> float:
        key = _metric_key(name, labels)
        with self._lock:
            value = self._gauges.get(key, 0.0) + amount
            self._gauges[key] = value
            return value

    def observe(
        self,
        name: str,
        value: float,
        *,
        labels: Mapping[str, str] | None = None,
    ) -> None:
        key = _metric_key(name, labels)
        with self._lock:
            count, total, maximum = self._histograms.get(key, (0, 0.0, 0.0))
            self._histograms[key] = (
                count + 1,
                total + float(value),
                max(maximum, float(value)),
            )

    def gauge_value(
        self,
        name: str,
        *,
        labels: Mapping[str, str] | None = None,
    ) -> float:
        with self._lock:
            return self._gauges.get(_metric_key(name, labels), 0.0)

    def render_prometheus(self) -> str:
        """Render a stable scrape without leaking high-cardinality values."""

        with self._lock:
            counters = sorted(self._counters.items())
            gauges = sorted(self._gauges.items())
            histograms = sorted(self._histograms.items())

        lines: list[str] = []
        seen_types: set[tuple[str, str]] = set()

        def declare(name: str, kind: str) -> None:
            marker = (name, kind)
            if marker not in seen_types:
                lines.append(f"# TYPE {name} {kind}")
                seen_types.add(marker)

        for (name, labels), value in counters:
            declare(name, "counter")
            lines.append(f"{name}{_render_labels(labels)} {value:.12g}")
        for (name, labels), value in gauges:
            declare(name, "gauge")
            rendered = value if math.isfinite(value) else 0.0
            lines.append(f"{name}{_render_labels(labels)} {rendered:.12g}")
        for (name, labels), (count, total, maximum) in histograms:
            declare(name, "summary")
            rendered_labels = _render_labels(labels)
            lines.append(f"{name}_count{rendered_labels} {count}")
            lines.append(f"{name}_sum{rendered_labels} {total:.12g}")
            lines.append(f"{name}_max{rendered_labels} {maximum:.12g}")
        return "\n".join(lines) + "\n"


@dataclass(frozen=True)
class ActivitySnapshot:
    active_requests: int
    active_mutations: int
    active_transactions: int
    checked_out_connections: int
    worker_running: bool
    worker_in_flight: int
    worker_last_success_monotonic: float | None


class RuntimeActivity:
    """Track drain-relevant process activity without database-backed flags."""

    def __init__(self, registry: MetricRegistry) -> None:
        self._lock = Lock()
        self._registry = registry
        self._active_requests = 0
        self._active_mutations = 0
        self._active_transactions = 0
        self._checked_out_connections = 0
        self._worker_running = False
        self._worker_in_flight = 0
        self._worker_last_success_monotonic: float | None = None

    def begin_request(self, *, mutation: bool) -> None:
        with self._lock:
            self._active_requests += 1
            if mutation:
                self._active_mutations += 1
            self._publish_locked()

    def end_request(self, *, mutation: bool) -> None:
        with self._lock:
            self._active_requests = max(0, self._active_requests - 1)
            if mutation:
                self._active_mutations = max(0, self._active_mutations - 1)
            self._publish_locked()

    def connection_checked_out(self) -> None:
        with self._lock:
            self._checked_out_connections += 1
            self._publish_locked()

    def transaction_started(self) -> None:
        with self._lock:
            self._active_transactions += 1
            self._publish_locked()

    def transaction_finished(self) -> None:
        with self._lock:
            self._active_transactions = max(0, self._active_transactions - 1)
            self._publish_locked()

    def connection_checked_in(self) -> None:
        with self._lock:
            self._checked_out_connections = max(0, self._checked_out_connections - 1)
            self._publish_locked()

    def worker_started(self) -> None:
        with self._lock:
            self._worker_running = True
            self._publish_locked()

    def worker_stopped(self) -> None:
        with self._lock:
            self._worker_running = False
            self._worker_in_flight = 0
            self._publish_locked()

    def worker_job_started(self) -> None:
        with self._lock:
            self._worker_in_flight += 1
            self._publish_locked()

    def worker_job_finished(self, *, success: bool) -> None:
        with self._lock:
            self._worker_in_flight = max(0, self._worker_in_flight - 1)
            if success:
                self._worker_last_success_monotonic = monotonic()
            self._publish_locked()

    def snapshot(self) -> ActivitySnapshot:
        with self._lock:
            return ActivitySnapshot(
                active_requests=self._active_requests,
                active_mutations=self._active_mutations,
                active_transactions=self._active_transactions,
                checked_out_connections=self._checked_out_connections,
                worker_running=self._worker_running,
                worker_in_flight=self._worker_in_flight,
                worker_last_success_monotonic=self._worker_last_success_monotonic,
            )

    def _publish_locked(self) -> None:
        self._registry.set_gauge("workchord_active_requests", self._active_requests)
        self._registry.set_gauge("workchord_active_mutations", self._active_mutations)
        self._registry.set_gauge(
            "workchord_database_active_transactions",
            self._active_transactions,
        )
        self._registry.set_gauge(
            "workchord_database_connections_checked_out",
            self._checked_out_connections,
        )
        self._registry.set_gauge(
            "workchord_delivery_worker_running",
            int(self._worker_running),
        )
        self._registry.set_gauge(
            "workchord_delivery_worker_in_flight",
            self._worker_in_flight,
        )


metrics = MetricRegistry()
activity = RuntimeActivity(metrics)
correlation_id_context: ContextVar[str | None] = ContextVar(
    "workchord_correlation_id",
    default=None,
)

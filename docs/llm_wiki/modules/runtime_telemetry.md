# runtime_telemetry Module

**Path:** `backend/app/runtime_telemetry.py`

## Description

Small dependency-free runtime telemetry used by probes and qualification.

The registry intentionally keeps only aggregate counters, gauges, and bounded
histogram summaries.  It never records SQL text, parameters, credentials, or
request bodies.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `collections` | `defaultdict` |
| `contextvars` | `ContextVar` |
| `dataclasses` | `dataclass` |
| `math` | `math` |
| `threading` | `Lock` |
| `time` | `monotonic` |
| `typing` | `Mapping` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/app/runtime_telemetry.py"]
    n0 --> n1
    click n1 "../modules/runtime_telemetry.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (12) |

> All 12 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [MetricRegistry](../entities/MetricRegistry.md) | 36 | — | Process-local Prometheus-compatible aggregate registry. |
| [ActivitySnapshot](../entities/ActivitySnapshot.md) | 137 | — | — |
| [RuntimeActivity](../entities/RuntimeActivity.md) | 147 | — | Track drain-relevant process activity without database-backed flags. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_metric_key` | `(name: str, labels: Mapping[str, str] \| None = None) -> MetricKey` | — | — |
| `_render_labels` | `(labels: tuple[tuple[str, str], ...]) -> str` | — | — |

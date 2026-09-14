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
    n0["backend/app/database_runtime.py"]
    n1["backend/app/main.py"]
    n2["backend/app/maintenance.py"]
    n3["backend/app/observability.py"]
    n4["backend/app/runtime_telemetry.py"]
    n5["backend/app/services/agent_routing_observability.py"]
    n6["backend/app/services/outbound_webhook_service.py"]
    n7["backend/app/services/session_service.py"]
    n8["backend/tests/database/test_observability.py"]
    n9["backend/tests/test_agent_routing_observability.py"]
    n0 --> n4
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n2 --> n4
    n3 --> n0
    n3 --> n2
    n3 --> n4
    n5 --> n4
    n5 --> n6
    n6 --> n0
    n6 --> n2
    n6 --> n4
    n7 --> n2
    n7 --> n4
    n8 --> n3
    n8 --> n4
    n9 --> n4
    n9 --> n5
    n9 --> n6
    click n0 "../modules/database_runtime.md"
    click n1 "../modules/app_main.md"
    click n2 "../modules/maintenance.md"
    click n3 "../modules/observability.md"
    click n4 "../modules/runtime_telemetry.md"
    click n5 "../modules/agent_routing_observability.md"
    click n6 "../modules/outbound_webhook_service.md"
    click n7 "../modules/session_service.md"
    click n8 "../modules/test_observability.md"
    click n9 "../modules/test_agent_routing_observability.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [database_runtime](../modules/database_runtime.md) |
| Inbound | [app_main](../modules/app_main.md) |
| Inbound | [maintenance](../modules/maintenance.md) |
| Inbound | [observability](../modules/observability.md) |
| Inbound | [agent_routing_observability](../modules/agent_routing_observability.md) |
| Inbound | [outbound_webhook_service](../modules/outbound_webhook_service.md) |
| Inbound | [session_service](../modules/session_service.md) |
| Inbound | [test_observability](../modules/test_observability.md) |
| Inbound | [test_agent_routing_observability](../modules/test_agent_routing_observability.md) |

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

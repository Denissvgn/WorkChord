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
    n0["backend/app/commands.py"]
    n1["backend/app/database_runtime.py"]
    n2["backend/app/main.py"]
    n3["backend/app/maintenance.py"]
    n4["backend/app/mutation_versions.py"]
    n5["backend/app/observability.py"]
    n6["backend/app/runtime_telemetry.py"]
    n7["backend/app/services/agent_routing_observability.py"]
    n8["backend/app/services/outbound_webhook_service.py"]
    n9["backend/app/services/session_service.py"]
    n10["backend/tests/database/test_observability.py"]
    n11["backend/tests/test_agent_routing_observability.py"]
    n0 --> n4
    n0 --> n6
    n1 --> n6
    n2 --> n0
    n2 --> n1
    n2 --> n3
    n2 --> n4
    n2 --> n5
    n2 --> n6
    n3 --> n6
    n4 --> n6
    n5 --> n1
    n5 --> n3
    n5 --> n6
    n7 --> n0
    n7 --> n6
    n7 --> n8
    n8 --> n0
    n8 --> n1
    n8 --> n3
    n8 --> n6
    n9 --> n0
    n9 --> n3
    n9 --> n6
    n10 --> n5
    n10 --> n6
    n11 --> n6
    n11 --> n7
    n11 --> n8
    click n0 "../modules/commands.md"
    click n1 "../modules/database_runtime.md"
    click n2 "../modules/app_main.md"
    click n3 "../modules/maintenance.md"
    click n4 "../modules/mutation_versions.md"
    click n5 "../modules/observability.md"
    click n6 "../modules/runtime_telemetry.md"
    click n7 "../modules/agent_routing_observability.md"
    click n8 "../modules/outbound_webhook_service.md"
    click n9 "../modules/session_service.md"
    click n10 "../modules/test_observability.md"
    click n11 "../modules/test_agent_routing_observability.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [commands](../modules/commands.md) |
| Inbound | [database_runtime](../modules/database_runtime.md) |
| Inbound | [app_main](../modules/app_main.md) |
| Inbound | [maintenance](../modules/maintenance.md) |
| Inbound | [mutation_versions](../modules/mutation_versions.md) |
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

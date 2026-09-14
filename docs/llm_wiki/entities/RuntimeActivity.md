# RuntimeActivity

**Location:** `backend/app/runtime_telemetry.py:147`
**Kind:** Class
**Bases:** —
**Module:** [runtime_telemetry](../modules/runtime_telemetry.md)

## Description

Track drain-relevant process activity without database-backed flags.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(registry: MetricRegistry) -> None` | — | — |
| `begin_request` | `(*, mutation: bool) -> None` | — | — |
| `end_request` | `(*, mutation: bool) -> None` | — | — |
| `connection_checked_out` | `() -> None` | — | — |
| `transaction_started` | `() -> None` | — | — |
| `transaction_finished` | `() -> None` | — | — |
| `connection_checked_in` | `() -> None` | — | — |
| `worker_started` | `() -> None` | — | — |
| `worker_stopped` | `() -> None` | — | — |
| `worker_job_started` | `() -> None` | — | — |
| `worker_job_finished` | `(*, success: bool) -> None` | — | — |
| `snapshot` | `() -> ActivitySnapshot` | — | — |
| `_publish_locked` | `() -> None` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
*No generated relationships detected.*

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [runtime_telemetry](../modules/runtime_telemetry.md) | 13 | — |

# DeliveryObservation

**Location:** `backend/app/models/delivery_observation.py:16`
**Kind:** Class
**Bases:** `Base`
**Module:** [delivery_observation](../modules/delivery_observation.md)

## Description

Retain delivery identity and scope independently of later hierarchy edits.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `Mapped[int]` | `mapped_column(Integer, primary_key=True)` | — |
| `original_task_id` | `Mapped[int]` | `mapped_column(Integer, nullable=False, index=True)` | — |
| `task_version` | `Mapped[int]` | `mapped_column(Integer, nullable=False)` | — |
| `project_id` | `Mapped[int \| None]` | `mapped_column(ForeignKey('projects.id', ondelete='SET NULL'))` | — |
| `iteration_id` | `Mapped[int \| None]` | `mapped_column(ForeignKey('iterations.id', ondelete='SET NULL'))` | — |
| `original_project_id` | `Mapped[int \| None]` | `mapped_column(Integer)` | — |
| `original_iteration_id` | `Mapped[int \| None]` | `mapped_column(Integer)` | — |
| `kind` | `Mapped[str]` | `mapped_column(String(32), nullable=False)` | — |
| `source` | `Mapped[str]` | `mapped_column(String(32), nullable=False)` | — |
| `observed_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), nullable=False)` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["DeliveryObservation (backend/app/models/delivery_observation.py)"]
    n1["Base (backend/app/database.py)"]
    n2["backend/app/models/__init__.py"]
    n3["backend/app/services/delivery_metrics_service.py"]
    n4["backend/app/services/execution_usage_service.py"]
    n5["backend/tests/test_delivery_metrics.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/delivery_observation.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/models___init__.md"
    click n3 "../modules/delivery_metrics_service.md"
    click n4 "../modules/execution_usage_service.md"
    click n5 "../modules/test_delivery_metrics.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [delivery_observation](../modules/delivery_observation.md) | 0 | `id`, `iteration_id`, `kind`, `observed_at`, `original_iteration_id`, `original_project_id`, `original_task_id`, `project_id`, `source`, `task_version` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Base` | [app_database](../modules/app_database.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `delivery_metrics_service` | import | [delivery_metrics_service](../modules/delivery_metrics_service.md) | — |
| `execution_usage_service` | import | [execution_usage_service](../modules/execution_usage_service.md) | — |
| `test_delivery_metrics` | import | [test_delivery_metrics](../modules/test_delivery_metrics.md) | — |

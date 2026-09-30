# ApplicationSnapshot

**Location:** `backend/app/models/recovery.py:12`
**Kind:** Class
**Bases:** `Base`
**Module:** [recovery](../modules/recovery.md)

## Description

_Auto-generated from `ApplicationSnapshot` in `backend/app/models/recovery.py`._

Checksummed application recovery data belongs to an iteration or a project backlog. Capture and retention share the mutation transaction. This record is not a full database backup.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `Mapped[int]` | `mapped_column(Integer, primary_key=True)` | — |
| `iteration_id` | `Mapped[int \| None]` | `mapped_column(ForeignKey('iterations.id', ondelete='CASCADE'), index=True)` | — |
| `project_id` | `Mapped[int \| None]` | `mapped_column(ForeignKey('projects.id', ondelete='CASCADE'), index=True)` | — |
| `filename` | `Mapped[str]` | `mapped_column(String(255), nullable=False)` | — |
| `schema_version` | `Mapped[int]` | `mapped_column(Integer, default=1, nullable=False)` | — |
| `input_revision` | `Mapped[int]` | `mapped_column(Integer, nullable=False)` | — |
| `payload` | `Mapped[dict]` | `mapped_column(JSON, nullable=False)` | — |
| `checksum` | `Mapped[str]` | `mapped_column(String(64), nullable=False)` | — |
| `provenance` | `Mapped[str]` | `mapped_column(String(32), default='command', nullable=False)` | — |
| `created_by_principal_id` | `Mapped[int \| None]` | `mapped_column(ForeignKey('principals.id', ondelete='RESTRICT'))` | — |
| `created_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), default=utc_now, index=True)` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ApplicationSnapshot (backend/app/models/recovery.py)"]
    n1["Base (backend/app/database.py)"]
    n2["backend/app/models/__init__.py"]
    n3["BacklogSnapshotService.capture (backend/app/services/backlog_snapshot_service.py)"]
    n4["SnapshotService.create_snapshot (backend/app/services/snapshot_service.py)"]
    n5["backend/tests/test_identity_lifecycle.py"]
    n6["backend/tests/test_managed_authority.py"]
    n7["backend/tests/test_task_domain_integrity.py"]
    n8["backend/tests/test_work_correctness.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    click n0 "../modules/recovery.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/models___init__.md"
    click n3 "../modules/backlog_snapshot_service.md"
    click n4 "../modules/snapshot_service.md"
    click n5 "../modules/test_identity_lifecycle.md"
    click n6 "../modules/test_managed_authority.md"
    click n7 "../modules/test_task_domain_integrity.md"
    click n8 "../modules/test_work_correctness.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [recovery](../modules/recovery.md) | 0 | `checksum`, `created_at`, `created_by_principal_id`, `filename`, `id`, `input_revision`, `iteration_id`, `payload`, `project_id`, `provenance`, `schema_version` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Base` | [app_database](../modules/app_database.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `BacklogSnapshotService.capture` | call | [backlog_snapshot_service](../modules/backlog_snapshot_service.md) | 1 |
| `SnapshotService.create_snapshot` | call | [snapshot_service](../modules/snapshot_service.md) | 1 |
| `test_identity_lifecycle` | import | [test_identity_lifecycle](../modules/test_identity_lifecycle.md) | — |
| `test_managed_authority` | import | [test_managed_authority](../modules/test_managed_authority.md) | — |
| `test_task_domain_integrity` | import | [test_task_domain_integrity](../modules/test_task_domain_integrity.md) | — |
| `test_work_correctness` | import | [test_work_correctness](../modules/test_work_correctness.md) | — |

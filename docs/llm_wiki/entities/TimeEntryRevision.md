# TimeEntryRevision

**Location:** `backend/app/models/time_entry.py:40`
**Kind:** Class
**Bases:** `Base`
**Module:** [models_time_entry](../modules/models_time_entry.md)

## Description

_Auto-generated from `TimeEntryRevision` in `backend/app/models/time_entry.py`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `Mapped[int]` | `mapped_column(Integer, primary_key=True)` | — |
| `entry_id` | `Mapped[int]` | `mapped_column(Integer, nullable=False)` | — |
| `project_id` | `Mapped[int]` | `mapped_column(Integer, nullable=False)` | — |
| `principal_id` | `Mapped[int]` | `mapped_column(Integer, nullable=False)` | — |
| `version` | `Mapped[int]` | `mapped_column(Integer, nullable=False)` | — |
| `work_date` | `Mapped[date]` | `mapped_column(Date, nullable=False)` | — |
| `timezone` | `Mapped[str]` | `mapped_column(String(64), nullable=False)` | — |
| `minutes` | `Mapped[int]` | `mapped_column(Integer, nullable=False)` | — |
| `note` | `Mapped[str]` | `mapped_column(Text, nullable=False)` | — |
| `voided` | `Mapped[bool]` | `mapped_column(nullable=False)` | — |
| `reason` | `Mapped[str]` | `mapped_column(String(1000), nullable=False)` | — |
| `created_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), nullable=False, default=utc_now)` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TimeEntryRevision (backend/app/models/time_entry.py)"]
    n1["Base (backend/app/database.py)"]
    n2["backend/app/models/__init__.py"]
    n3["TimeEntryService.append_revision (backend/app/services/time_entry_service.py)"]
    n4["backend/tests/database_migration/test_project_identity_scope.py"]
    n5["backend/tests/migrations/test_project_identity.py"]
    n6["backend/tests/test_time_entries.py"]
    n7["backend/tests/test_time_reports.py"]
    n8["scripts/ci/installed_wheel_postgresql_qualification.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    click n0 "../modules/models_time_entry.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/models___init__.md"
    click n3 "../modules/time_entry_service.md"
    click n4 "../modules/test_project_identity_scope.md"
    click n5 "../modules/test_project_identity.md"
    click n6 "../modules/test_time_entries.md"
    click n7 "../modules/test_time_reports.md"
    click n8 "../modules/installed_wheel_postgresql_qualification.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [models_time_entry](../modules/models_time_entry.md) | 0 | `created_at`, `entry_id`, `id`, `minutes`, `note`, `principal_id`, `project_id`, `reason`, `timezone`, `version`, `voided`, `work_date` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Base` | [app_database](../modules/app_database.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `TimeEntryService.append_revision` | call | [time_entry_service](../modules/time_entry_service.md) | 1 |
| `test_project_identity_scope` | import | [test_project_identity_scope](../modules/test_project_identity_scope.md) | — |
| `test_project_identity` | import | [test_project_identity](../modules/test_project_identity.md) | — |
| `test_time_entries` | import | [test_time_entries](../modules/test_time_entries.md) | — |
| `test_time_reports` | import | [test_time_reports](../modules/test_time_reports.md) | — |
| `installed_wheel_postgresql_qualification` | import | [installed_wheel_postgresql_qualification](../modules/installed_wheel_postgresql_qualification.md) | — |

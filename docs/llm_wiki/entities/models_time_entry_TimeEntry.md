# TimeEntry

**Location:** `backend/app/models/time_entry.py:12`
**Kind:** Class
**Bases:** `Base`
**Module:** [models_time_entry](../modules/models_time_entry.md)

## Description

_Auto-generated from `TimeEntry` in `backend/app/models/time_entry.py`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `Mapped[int]` | `mapped_column(Integer, primary_key=True)` | — |
| `project_id` | `Mapped[int]` | `mapped_column(Integer, nullable=False)` | — |
| `task_id` | `Mapped[int \| None]` | `mapped_column(Integer)` | — |
| `principal_id` | `Mapped[int]` | `mapped_column(Integer, nullable=False)` | — |
| `task_title` | `Mapped[str \| None]` | `mapped_column(String(500))` | — |
| `request_id` | `Mapped[str]` | `mapped_column(String(36), nullable=False)` | — |
| `creation_digest` | `Mapped[str]` | `mapped_column(String(64), nullable=False)` | — |
| `work_date` | `Mapped[date]` | `mapped_column(Date, nullable=False)` | — |
| `timezone` | `Mapped[str]` | `mapped_column(String(64), nullable=False)` | — |
| `minutes` | `Mapped[int]` | `mapped_column(Integer, nullable=False)` | — |
| `note` | `Mapped[str]` | `mapped_column(Text, nullable=False, default='')` | — |
| `version` | `Mapped[int]` | `mapped_column(Integer, nullable=False, default=1)` | — |
| `voided` | `Mapped[bool]` | `mapped_column(nullable=False, default=False)` | — |
| `created_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), nullable=False, default=utc_now)` | — |
| `updated_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), nullable=False, default=utc_now)` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TimeEntry (backend/app/models/time_entry.py)"]
    n1["Base (backend/app/database.py)"]
    n2["backend/app/models/__init__.py"]
    n3["TimeEntryService.create (backend/app/services/time_entry_service.py)"]
    n4["backend/app/services/time_report_service.py"]
    n5["backend/tests/migrations/test_project_identity.py"]
    n6["backend/tests/test_time_entries.py"]
    n7["backend/tests/test_time_reports.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    click n0 "../modules/models_time_entry.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/models___init__.md"
    click n3 "../modules/time_entry_service.md"
    click n4 "../modules/time_report_service.md"
    click n5 "../modules/test_project_identity.md"
    click n6 "../modules/test_time_entries.md"
    click n7 "../modules/test_time_reports.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [models_time_entry](../modules/models_time_entry.md) | 0 | `created_at`, `creation_digest`, `id`, `minutes`, `note`, `principal_id`, `project_id`, `request_id`, `task_id`, `task_title`, `timezone`, `updated_at` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Base` | [app_database](../modules/app_database.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `TimeEntryService.create` | call | [time_entry_service](../modules/time_entry_service.md) | 1 |
| `time_report_service` | import | [time_report_service](../modules/time_report_service.md) | — |
| `test_project_identity` | import | [test_project_identity](../modules/test_project_identity.md) | — |
| `test_time_entries` | import | [test_time_entries](../modules/test_time_entries.md) | — |
| `test_time_reports` | import | [test_time_reports](../modules/test_time_reports.md) | — |

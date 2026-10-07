# time_report_service Module

**Path:** `backend/app/services/time_report_service.py`

## Description

Authorized scalar totals and exports without exposing other authors' records.

Personal reports default to the authenticated author's active records. Team totals require manager authority and select only scalar task/project aggregates; individual notes and revisions never enter that projection. The cohort includes current leaf work and retained historical associations, with unavailable estimates for moved/deleted/composite work. Missing recorded time stays null; zero estimates stay known. Finite ID pages carry independent live scope totals, and CSV exports reject more than 5,000 rows and neutralize formula prefixes in text. Individual exports remain author-only.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `AuthorityError`, `internal_authority` |
| `app.models.task` | `Task` |
| `app.models.time_entry` | `TimeEntry` |
| `app.query_limits` | `CollectionLimitExceededError` |
| `app.services.time_entry_service` | `TimeEntryService` |
| `csv` | `csv` |
| `io` | `StringIO` |
| `sqlalchemy` | `and_`, `case`, `func`, `select`, `union` |
| `sqlalchemy.orm` | `aliased` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/authority.py"]
    n1["backend/app/models/task.py"]
    n2["backend/app/models/time_entry.py"]
    n3["backend/app/query_limits.py"]
    n4["backend/app/routers/time_entries.py"]
    n5["backend/app/services/time_entry_service.py"]
    n6["backend/app/services/time_report_service.py"]
    n7["backend/tests/test_time_reports.py"]
    n0 --> n1
    n4 --> n5
    n4 --> n6
    n5 --> n0
    n5 --> n1
    n5 --> n2
    n6 --> n0
    n6 --> n1
    n6 --> n2
    n6 --> n3
    n6 --> n5
    n7 --> n0
    n7 --> n2
    n7 --> n3
    n7 --> n5
    n7 --> n6
    click n0 "../modules/authority.md"
    click n1 "../modules/models_task.md"
    click n2 "../modules/models_time_entry.md"
    click n3 "../modules/query_limits.md"
    click n4 "../modules/time_entries.md"
    click n5 "../modules/time_entry_service.md"
    click n6 "../modules/time_report_service.md"
    click n7 "../modules/test_time_reports.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [time_entries](../modules/time_entries.md) |
| Inbound | [test_time_reports](../modules/test_time_reports.md) |
| Outbound | [authority](../modules/authority.md) |
| Outbound | [models_task](../modules/models_task.md) |
| Outbound | [models_time_entry](../modules/models_time_entry.md) |
| Outbound | [query_limits](../modules/query_limits.md) |
| Outbound | [time_entry_service](../modules/time_entry_service.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [TimeReportService](../entities/TimeReportService.md) | 16 | — | — |

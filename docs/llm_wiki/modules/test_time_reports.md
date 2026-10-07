# test_time_reports Module

**Path:** `backend/tests/test_time_reports.py`

## Description

Recorded coverage and manager totals preserve private entry boundaries.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `Authority`, `AuthorityError` |
| `app.models.time_entry` | `TimeEntry` |
| `app.query_limits` | `CollectionLimitExceededError` |
| `app.schemas.task` | `TaskCreate`, `TaskUpdate` |
| `app.services.task_service` | `TaskService` |
| `app.services.time_entry_service` | `TimeEntryService` |
| `app.services.time_report_service` | `TimeReportService` |
| `app.utils.time` | `utc_now` |
| `datetime` | `date`, `timedelta` |
| `pytest` | `pytest` |
| `sqlalchemy` | `insert` |
| `tests.test_delivery_scenarios` | `delivery_store` |
| `tests.test_time_entries` | `prepare`, `entry_data`, `isolated_time_settings` |
| `uuid` | `uuid4` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/authority.py"]
    n1["backend/app/models/time_entry.py"]
    n2["backend/app/query_limits.py"]
    n3["backend/app/schemas/task.py"]
    n4["backend/app/services/task_service.py"]
    n5["backend/app/services/time_entry_service.py"]
    n6["backend/app/services/time_report_service.py"]
    n7["backend/app/utils/time.py"]
    n8["backend/tests/test_delivery_scenarios.py"]
    n9["backend/tests/test_time_entries.py"]
    n10["backend/tests/test_time_reports.py"]
    n1 --> n7
    n4 --> n0
    n4 --> n2
    n4 --> n3
    n5 --> n0
    n5 --> n1
    n5 --> n7
    n6 --> n0
    n6 --> n1
    n6 --> n2
    n6 --> n5
    n8 --> n4
    n9 --> n0
    n9 --> n1
    n9 --> n3
    n9 --> n4
    n9 --> n5
    n9 --> n8
    n10 --> n0
    n10 --> n1
    n10 --> n2
    n10 --> n3
    n10 --> n4
    n10 --> n5
    n10 --> n6
    n10 --> n7
    n10 --> n8
    n10 --> n9
    click n0 "../modules/authority.md"
    click n1 "../modules/models_time_entry.md"
    click n2 "../modules/query_limits.md"
    click n3 "../modules/schemas_task.md"
    click n4 "../modules/task_service.md"
    click n5 "../modules/time_entry_service.md"
    click n6 "../modules/time_report_service.md"
    click n7 "../modules/time.md"
    click n8 "../modules/test_delivery_scenarios.md"
    click n9 "../modules/test_time_entries.md"
    click n10 "../modules/test_time_reports.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [authority](../modules/authority.md) |
| Outbound | [models_time_entry](../modules/models_time_entry.md) |
| Outbound | [query_limits](../modules/query_limits.md) |
| Outbound | [schemas_task](../modules/schemas_task.md) |
| Outbound | [task_service](../modules/task_service.md) |
| Outbound | [time_entry_service](../modules/time_entry_service.md) |
| Outbound | [time_report_service](../modules/time_report_service.md) |
| Outbound | [time](../modules/time.md) |
| Outbound | [test_delivery_scenarios](../modules/test_delivery_scenarios.md) |
| Outbound | [test_time_entries](../modules/test_time_entries.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 1 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `test_personal_and_manager_totals_do_not_expose_private_records` | *(async)* `(delivery_store, monkeypatch)` | — | — |
| `test_unknown_time_zero_estimates_project_work_and_finite_pages` | *(async)* `(delivery_store, monkeypatch)` | — | — |
| `test_moved_task_keeps_original_scope_and_does_not_expose_new_title` | *(async)* `(delivery_store, monkeypatch)` | — | — |
| `test_csv_rejects_spreadsheet_formula_interpretation_without_manufacturing_missing_values` | `()` | — | — |
| `test_personal_export_bound_is_explicit` | *(async)* `(delivery_store, monkeypatch)` | — | — |

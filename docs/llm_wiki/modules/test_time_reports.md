# test_time_reports Module

**Path:** `backend/tests/test_time_reports.py`

## Description

Recorded coverage and manager totals preserve private entry boundaries.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `Authority`, `AuthorityError`, `internal_authority` |
| `app.config` | `get_settings`, `get_settings` |
| `app.models.iteration` | `Iteration` |
| `app.models.project` | `Project` |
| `app.models.time_entry` | `TimeEntry`, `TimeEntryRevision`, `TimeEntry` |
| `app.query_limits` | `CollectionLimitExceededError` |
| `app.schemas.iteration` | `IterationCreate` |
| `app.schemas.project` | `ProjectCreate`, `ProjectCreate` |
| `app.schemas.task` | `TaskCreate`, `TaskUpdate` |
| `app.schemas.time_entry` | `TimeEntryCorrection` |
| `app.services.iteration_service` | `IterationService` |
| `app.services.project_service` | `ProjectService`, `ProjectService` |
| `app.services.task_service` | `TaskService` |
| `app.services.time_entry_service` | `TimeEntryService` |
| `app.services.time_report_service` | `TimeReportService` |
| `app.utils.time` | `utc_now` |
| `datetime` | `date`, `timedelta` |
| `pytest` | `pytest` |
| `sqlalchemy` | `create_engine`, `select`, `insert` |
| `sqlite3` | `sqlite3` |
| `tests.test_delivery_scenarios` | `delivery_store` |
| `tests.test_time_entries` | `prepare`, `entry_data`, `isolated_time_settings` |
| `uuid` | `uuid4` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/test_time_reports.py"]
    n1 --> n0
    click n1 "../modules/test_time_reports.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `backend` (18) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 1 |

> All 18 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `test_deleted_project_time_is_not_visible_to_replacement_manager` | *(async)* `(delivery_store, monkeypatch)` | — | — |
| `test_retained_titles_notes_and_corrections_never_attach_to_replacement_scope` | *(async)* `(delivery_store, monkeypatch, tmp_path)` | — | — |
| `test_personal_and_manager_totals_do_not_expose_private_records` | *(async)* `(delivery_store, monkeypatch)` | — | — |
| `test_unknown_time_zero_estimates_project_work_and_finite_pages` | *(async)* `(delivery_store, monkeypatch)` | — | — |
| `test_moved_task_keeps_original_scope_and_does_not_expose_new_title` | *(async)* `(delivery_store, monkeypatch)` | — | — |
| `test_csv_rejects_spreadsheet_formula_interpretation_without_manufacturing_missing_values` | `()` | — | — |
| `test_personal_export_bound_is_explicit` | *(async)* `(delivery_store, monkeypatch)` | — | — |

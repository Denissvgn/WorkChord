# test_time_entries Module

**Path:** `backend/tests/test_time_entries.py`

## Description

Private explicit minutes, retained corrections and independent recovery behavior.

## Imports

| Source | Symbols |
|--------|---------|
| `app` | `http_authority` |
| `app.authority` | `Authority`, `AuthorityError`, `internal_authority` |
| `app.commands` | `PlanningConflict` |
| `app.config` | `get_settings` |
| `app.main` | `app` |
| `app.models.task` | `Task` |
| `app.models.time_entry` | `TimeEntry`, `TimeEntryRevision` |
| `app.schemas.task` | `TaskCreate`, `TaskUpdate` |
| `app.schemas.time_entry` | `TimeEntryCreate`, `TimeEntryCorrection`, `TimeEntryVoid` |
| `app.services.backlog_snapshot_service` | `BacklogSnapshotService` |
| `app.services.task_service` | `TaskService` |
| `app.services.time_entry_service` | `TimeEntryService`, `TimeEntryVersionConflict` |
| `asyncio` | `asyncio` |
| `datetime` | `date` |
| `httpx` | `httpx` |
| `pydantic` | `ValidationError` |
| `pytest` | `pytest` |
| `sqlalchemy` | `func`, `select`, `update`, `delete` |
| `tests.test_delivery_scenarios` | `delivery_store` |
| `tests.test_task_domain` | `human_context` |
| `uuid` | `uuid4` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/test_time_entries.py"]
    n1 --> n0
    click n1 "../modules/test_time_entries.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `backend` (14) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 4 | 1 |

> All 14 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `isolated_time_settings` | `()` | `@pytest.fixture(autouse=True)` | — |
| `prepare` | *(async)* `(db, scenario, monkeypatch)` | — | — |
| `entry_data` | `(scenario, **values)` | — | — |
| `test_record_correct_void_retains_private_history_and_task_state` | *(async)* `(delivery_store, monkeypatch)` | — | — |
| `test_retry_identity_and_payload_conflict` | *(async)* `(delivery_store, monkeypatch)` | — | — |
| `test_other_people_projects_agents_and_disabled_feature_are_protected` | *(async)* `(delivery_store, monkeypatch)` | — | — |
| `test_history_survives_task_removal_and_remains_append_only` | *(async)* `(delivery_store, monkeypatch)` | — | — |
| `test_history_failure_rolls_back_record_and_retry` | *(async)* `(delivery_store, monkeypatch)` | — | — |
| `test_independent_clients_serialize_the_daily_recorded_total` | *(async)* `(delivery_store, monkeypatch)` | — | — |
| `test_invalid_recorded_values_are_rejected` | `(field, value)` | `@pytest.mark.parametrize('field,value', [('minutes', 0), ('minutes', -1), ('minutes', 1.5), ('minutes', True), ('minutes', 1441), ('timezone', 'Unknown/Zone'), ('timezone', '../etc'), ('work_date', 'not-a-date'), ('work_date', '2026-10-07T00:00:00Z'), ('work_date', 1791331200), ('project_id', True), ('task_id', True)])` | — |
| `test_project_work_finite_paging_and_scope_validation` | *(async)* `(delivery_store, monkeypatch)` | — | — |
| `test_http_privacy_conflict_and_feature_disabled` | *(async)* `(delivery_store, monkeypatch)` | — | — |
| `test_task_snapshot_restore_does_not_rewind_recorded_time` | *(async)* `(delivery_store, monkeypatch)` | — | — |

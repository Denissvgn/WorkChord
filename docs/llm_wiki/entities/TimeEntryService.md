# TimeEntryService

**Location:** `backend/app/services/time_entry_service.py:29`
**Kind:** Class
**Bases:** —
**Module:** [time_entry_service](../modules/time_entry_service.md)

## Description

_Auto-generated from `TimeEntryService` in `backend/app/services/time_entry_service.py`._

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(db)` | — | — |
| `principal_id` | `()` | — | — |
| `project` | *(async)* `(project_id, *, writing = False)` | — | — |
| `lock_author` | *(async)* `()` | — | — |
| `authorize_object` | `(obj)` | — | — |
| `serialize` | `(entry)` | `@staticmethod` | — |
| `get` | *(async)* `(entry_id)` | — | — |
| `check_window` | `(start, end)` | `@staticmethod` | — |
| `list` | *(async)* `(*, project_id = None, task_id = None, start = None, end = None, after_id = 0, upper_id = None, limit = 50, include_voided = False)` | — | — |
| `check_day_total` | *(async)* `(principal_id, work_date, minutes, *, exclude_id = None)` | — | — |
| `append_revision` | *(async)* `(entry, reason)` | — | — |
| `create` | *(async)* `(data)` | `@atomic_command` | — |
| `correct` | *(async)* `(entry_id, data, *, void = False)` | `@atomic_command` | — |
| `history` | *(async)* `(entry_id, *, after_version = 0, limit = 50)` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TimeEntryService (backend/app/services/time_entry_service.py)"]
    n1["correct_entry (backend/app/routers/time_entries.py)"]
    n2["create_entry (backend/app/routers/time_entries.py)"]
    n3["get_entry (backend/app/routers/time_entries.py)"]
    n4["history (backend/app/routers/time_entries.py)"]
    n5["list_entries (backend/app/routers/time_entries.py)"]
    n6["void_entry (backend/app/routers/time_entries.py)"]
    n7["TimeReportService.__init__ (backend/app/services/time_report_service.py)"]
    n8["test_history_failure_rolls_back_record_and_retry (backend/tests/test_time_entries.py)"]
    n9["test_history_survives_task_removal_and_remains_append_only (backend/tests/test_time_entries.py)"]
    n10["test_other_people_projects_agents_and_disabled_feature_are_protected (backend/tests/test_time_entries.py)"]
    n11["test_project_work_finite_paging_and_scope_validation (backend/tests/test_time_entries.py)"]
    n12["test_record_correct_void_retains_private_history_and_task_state (backend/tests/test_time_entries.py)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    n10 --> n0
    n11 --> n0
    n12 --> n0
    click n0 "../modules/time_entry_service.md"
    click n1 "../modules/time_entries.md"
    click n2 "../modules/time_entries.md"
    click n3 "../modules/time_entries.md"
    click n4 "../modules/time_entries.md"
    click n5 "../modules/time_entries.md"
    click n6 "../modules/time_entries.md"
    click n7 "../modules/time_report_service.md"
    click n8 "../modules/test_time_entries.md"
    click n9 "../modules/test_time_entries.md"
    click n10 "../modules/test_time_entries.md"
    click n11 "../modules/test_time_entries.md"
    click n12 "../modules/test_time_entries.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [time_entry_service](../modules/time_entry_service.md) | 14 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `correct_entry` | call | [time_entries](../modules/time_entries.md) | 1 |
| `create_entry` | call | [time_entries](../modules/time_entries.md) | 1 |
| `get_entry` | call | [time_entries](../modules/time_entries.md) | 1 |
| `history` | call | [time_entries](../modules/time_entries.md) | 1 |
| `list_entries` | call | [time_entries](../modules/time_entries.md) | 1 |
| `void_entry` | call | [time_entries](../modules/time_entries.md) | 1 |
| `TimeReportService.__init__` | call | [time_report_service](../modules/time_report_service.md) | 1 |
| `test_history_failure_rolls_back_record_and_retry` | call | [test_time_entries](../modules/test_time_entries.md) | 1 |
| `test_history_survives_task_removal_and_remains_append_only` | call | [test_time_entries](../modules/test_time_entries.md) | 1 |
| `test_other_people_projects_agents_and_disabled_feature_are_protected` | call | [test_time_entries](../modules/test_time_entries.md) | 1 |
| `test_project_work_finite_paging_and_scope_validation` | call | [test_time_entries](../modules/test_time_entries.md) | 1 |
| `test_record_correct_void_retains_private_history_and_task_state` | call | [test_time_entries](../modules/test_time_entries.md) | 1 |

> References: showing 12 of 17 logical references; 5 omitted by the 12-row generated summary limit.

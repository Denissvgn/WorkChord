# TriageItemStatus

**Location:** `backend/app/models/triage.py:20`
**Kind:** Enum
**Bases:** `str`, `Enum`
**Module:** [models_triage](../modules/models_triage.md)

## Description

Triage item lifecycle status.

## Attributes

| Name | Declared value | Description |
|------|-------|-------------|
| `NEW` | `'new'` | — |
| `ACCEPTED` | `'accepted'` | — |
| `DECLINED` | `'declined'` | — |
| `DUPLICATE` | `'duplicate'` | — |
| `SNOOZED` | `'snoozed'` | — |
| `CONVERTED` | `'converted'` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TriageItemStatus (backend/app/models/triage.py)"]
    n1["Enum"]
    n2["str"]
    n3["backend/app/models/__init__.py"]
    n4["backend/app/services/task_import_service.py"]
    n5["TriageService._filtered_list_query (backend/app/services/triage_service.py)"]
    n6["TriageService.count_items (backend/app/services/triage_service.py)"]
    n7["TriageService.list_items (backend/app/services/triage_service.py)"]
    n8["backend/tests/database/test_postgresql_concurrency.py"]
    n0 --> n1
    n0 --> n2
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    click n0 "../modules/models_triage.md"
    click n3 "../modules/models___init__.md"
    click n4 "../modules/task_import_service.md"
    click n5 "../modules/triage_service.md"
    click n6 "../modules/triage_service.md"
    click n7 "../modules/triage_service.md"
    click n8 "../modules/test_postgresql_concurrency.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [models_triage](../modules/models_triage.md) | 0 | `ACCEPTED`, `CONVERTED`, `DECLINED`, `DUPLICATE`, `NEW`, `SNOOZED` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Enum` | — |
| Base | `str` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `task_import_service` | import | [task_import_service](../modules/task_import_service.md) | — |
| `TriageService._filtered_list_query` | type_reference | [triage_service](../modules/triage_service.md) | — |
| `TriageService.count_items` | type_reference | [triage_service](../modules/triage_service.md) | — |
| `TriageService.list_items` | type_reference | [triage_service](../modules/triage_service.md) | — |
| `test_postgresql_concurrency` | import | [test_postgresql_concurrency](../modules/test_postgresql_concurrency.md) | — |

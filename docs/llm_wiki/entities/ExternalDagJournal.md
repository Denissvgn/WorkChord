# ExternalDagJournal

**Location:** `backend/app/autonomy/orchestration.py:148`
**Kind:** Class
**Bases:** `Protocol`
**Module:** [orchestration](../modules/orchestration.md)

**Decorators:** `@runtime_checkable`

## Description

CAS state service deployed outside the WorkChord database/runtime.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `read` | `(*, run_id: str) -> DagJournalSnapshot` | — | — |
| `compare_and_append` | `(*, run_id: str, expected_revision: int, expected_head_digest: str, entry: DagJournalEntry) -> bool` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ExternalDagJournal (backend/app/autonomy/orchestration.py)"]
    n1["Protocol"]
    n2["DagController.__init__ (backend/app/autonomy/orchestration.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/orchestration.md"
    click n2 "../modules/orchestration.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [orchestration](../modules/orchestration.md) | 2 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Protocol` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `DagController.__init__` | type_reference | [orchestration](../modules/orchestration.md) | — |

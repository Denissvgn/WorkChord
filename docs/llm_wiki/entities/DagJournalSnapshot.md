# DagJournalSnapshot

**Location:** `backend/app/autonomy/orchestration.py:141`
**Kind:** Pydantic model
**Bases:** `StrictContractModel`
**Module:** [orchestration](../modules/orchestration.md)

## Description

_Auto-generated from `DagJournalSnapshot` in `backend/app/autonomy/orchestration.py`._

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `revision` | `int` | `revision` | Yes | No | — | ge=0 | — | — |
| `head_digest` | `str` | `head_digest` | Yes | No | — | pattern=unknown (SHA256_PATTERN) | — | — |
| `entries` | `tuple[DagJournalEntry, ...]` | `entries` | No | No | `()` | max_length=2000000 | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["DagJournalSnapshot (backend/app/autonomy/orchestration.py)"]
    n1["StrictContractModel (backend/app/autonomy/canonical.py)"]
    n2["DagController._validated_snapshot (backend/app/autonomy/orchestration.py)"]
    n3["ExternalDagJournal.read (backend/app/autonomy/orchestration.py)"]
    n4["MemoryDagJournal.read (backend/tests/autonomy/test_autonomy_foundation.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/orchestration.md"
    click n1 "../modules/autonomy_canonical.md"
    click n2 "../modules/orchestration.md"
    click n3 "../modules/orchestration.md"
    click n4 "../modules/test_autonomy_foundation.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [orchestration](../modules/orchestration.md) | 0 | `entries`, `head_digest`, `revision` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `StrictContractModel` | [autonomy_canonical](../modules/autonomy_canonical.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `DagController._validated_snapshot` | type_reference | [orchestration](../modules/orchestration.md) | — |
| `ExternalDagJournal.read` | type_reference | [orchestration](../modules/orchestration.md) | — |
| `MemoryDagJournal.read` | call | [test_autonomy_foundation](../modules/test_autonomy_foundation.md) | 1 |
| `MemoryDagJournal.read` | type_reference | [test_autonomy_foundation](../modules/test_autonomy_foundation.md) | — |

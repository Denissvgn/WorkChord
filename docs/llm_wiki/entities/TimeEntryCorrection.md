# TimeEntryCorrection

**Location:** `backend/app/schemas/time_entry.py:56`
**Kind:** Pydantic model
**Bases:** `TimeValues`, `CorrectionReason`
**Module:** [schemas_time_entry](../modules/schemas_time_entry.md)

## Description

_Auto-generated from `TimeEntryCorrection` in `backend/app/schemas/time_entry.py`._

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `expected_version` | `StrictInt` | `expected_version` | Yes | No | — | ge=1 | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TimeEntryCorrection (backend/app/schemas/time_entry.py)"]
    n1["CorrectionReason (backend/app/schemas/time_entry.py)"]
    n2["TimeValues (backend/app/schemas/time_entry.py)"]
    n3["correct_entry (backend/app/routers/time_entries.py)"]
    n4["test_history_survives_task_removal_and_remains_append_only (backend/tests/test_time_entries.py)"]
    n5["test_record_correct_void_retains_private_history_and_task_state (backend/tests/test_time_entries.py)"]
    n6["test_task_snapshot_restore_does_not_rewind_recorded_time (backend/tests/test_time_entries.py)"]
    n0 --> n1
    n0 --> n2
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    click n0 "../modules/schemas_time_entry.md"
    click n1 "../modules/schemas_time_entry.md"
    click n2 "../modules/schemas_time_entry.md"
    click n3 "../modules/time_entries.md"
    click n4 "../modules/test_time_entries.md"
    click n5 "../modules/test_time_entries.md"
    click n6 "../modules/test_time_entries.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_time_entry](../modules/schemas_time_entry.md) | 0 | `expected_version` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `CorrectionReason` | [schemas_time_entry](../modules/schemas_time_entry.md) |
| Base | `TimeValues` | [schemas_time_entry](../modules/schemas_time_entry.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `correct_entry` | type_reference | [time_entries](../modules/time_entries.md) | — |
| `test_history_survives_task_removal_and_remains_append_only` | call | [test_time_entries](../modules/test_time_entries.md) | 1 |
| `test_record_correct_void_retains_private_history_and_task_state` | call | [test_time_entries](../modules/test_time_entries.md) | 1 |
| `test_task_snapshot_restore_does_not_rewind_recorded_time` | call | [test_time_entries](../modules/test_time_entries.md) | 1 |

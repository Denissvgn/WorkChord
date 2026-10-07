# TimeRevisionResponse

**Location:** `backend/app/schemas/time_entry.py:84`
**Kind:** Pydantic model
**Bases:** `TimeValues`
**Module:** [schemas_time_entry](../modules/schemas_time_entry.md)

## Description

_Auto-generated from `TimeRevisionResponse` in `backend/app/schemas/time_entry.py`._

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `version` | `int` | `version` | Yes | No | — | — | — | — |
| `principal_id` | `int` | `principal_id` | Yes | No | — | — | — | — |
| `reason` | `str` | `reason` | Yes | No | — | — | — | — |
| `voided` | `bool` | `voided` | Yes | No | — | — | — | — |
| `created_at` | `datetime` | `created_at` | Yes | No | — | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TimeRevisionResponse (backend/app/schemas/time_entry.py)"]
    n1["TimeValues (backend/app/schemas/time_entry.py)"]
    n2["TimeEntryService.history (backend/app/services/time_entry_service.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/schemas_time_entry.md"
    click n1 "../modules/schemas_time_entry.md"
    click n2 "../modules/time_entry_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_time_entry](../modules/schemas_time_entry.md) | 0 | `created_at`, `principal_id`, `reason`, `version`, `voided` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `TimeValues` | [schemas_time_entry](../modules/schemas_time_entry.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `TimeEntryService.history` | call | [time_entry_service](../modules/time_entry_service.md) | 1 |

# SnapshotRestoreRequest

**Location:** `backend/app/schemas/snapshot.py:6`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [snapshot](../modules/snapshot.md)

## Description

Explicit acknowledgement required before destructive snapshot restore.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `confirm` | `bool` | `confirm` | No | No | `False` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["SnapshotRestoreRequest (backend/app/schemas/snapshot.py)"]
    n1["BaseModel"]
    n2["restore_snapshot (backend/app/routers/snapshots.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/snapshot.md"
    click n2 "../modules/snapshots.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [snapshot](../modules/snapshot.md) | 0 | `confirm` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `restore_snapshot` | type_reference | [snapshots](../modules/snapshots.md) | — |

# LegacySnapshotImport

**Location:** `backend/app/models/recovery.py:30`
**Kind:** Class
**Bases:** `Base`
**Module:** [recovery](../modules/recovery.md)

## Description

_Auto-generated from `LegacySnapshotImport` in `backend/app/models/recovery.py`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `checksum` | `Mapped[str]` | `mapped_column(String(64), primary_key=True)` | — |
| `iteration_id` | `Mapped[int]` | `mapped_column(ForeignKey('iterations.id', ondelete='CASCADE'), index=True)` | — |
| `source_name` | `Mapped[str]` | `mapped_column(String(255), nullable=False)` | — |
| `disposition` | `Mapped[str]` | `mapped_column(String(32), nullable=False)` | — |
| `reason` | `Mapped[str]` | `mapped_column(Text, nullable=False)` | — |
| `imported_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), default=utc_now)` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["LegacySnapshotImport (backend/app/models/recovery.py)"]
    n1["Base (backend/app/database.py)"]
    n2["backend/app/models/__init__.py"]
    n3["SnapshotService.import_legacy (backend/app/services/snapshot_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/recovery.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/models___init__.md"
    click n3 "../modules/snapshot_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [recovery](../modules/recovery.md) | 0 | `checksum`, `disposition`, `imported_at`, `iteration_id`, `reason`, `source_name` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Base` | [app_database](../modules/app_database.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `SnapshotService.import_legacy` | call | [snapshot_service](../modules/snapshot_service.md) | 1 |

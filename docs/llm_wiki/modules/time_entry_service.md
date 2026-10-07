# time_entry_service Module

**Path:** `backend/app/services/time_entry_service.py`

## Description

Attributable minute commands with private reads and independent version history.

Human authors can read and correct only their own records with current access to the original recording project. Author-row locking serializes creation retries and daily totals across both dialects; UUID/digest replay returns the current record without adding minutes. Commands append private revisions atomically and never reserve task or planning revisions. Task/project associations survive deletion as stable recording-scope IDs; task snapshots do not rewind the ledger. The optional capability defaults disabled and agent/guest credentials cannot author records.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `AuthorityError`, `internal_authority`, `require_project` |
| `app.commands` | `PlanningConflict`, `atomic_command` |
| `app.config` | `get_settings` |
| `app.models.identity` | `Principal` |
| `app.models.project` | `Project` |
| `app.models.task` | `Task` |
| `app.models.time_entry` | `TimeEntry`, `TimeEntryRevision` |
| `app.schemas.time_entry` | `TimeEntryResponse`, `TimeRevisionResponse` |
| `app.utils.time` | `utc_now` |
| `hashlib` | `hashlib` |
| `json` | `json` |
| `sqlalchemy` | `func`, `select`, `update` |
| `sqlalchemy.orm` | `raiseload` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/app/services/time_entry_service.py"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/time_entry_service.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (4) |
| Outbound | `backend` (9) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

> All 13 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [TimeEntryVersionConflict](../entities/TimeEntryVersionConflict.md) | 20 | `PlanningConflict` | — |
| [TimeEntryService](../entities/TimeEntryService.md) | 29 | — | — |
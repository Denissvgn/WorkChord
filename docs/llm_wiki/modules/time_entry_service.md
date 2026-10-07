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
    n0["backend/app/authority.py"]
    n1["backend/app/commands.py"]
    n2["backend/app/config.py"]
    n3["backend/app/models/identity.py"]
    n4["backend/app/models/project.py"]
    n5["backend/app/models/task.py"]
    n6["backend/app/models/time_entry.py"]
    n7["backend/app/routers/time_entries.py"]
    n8["backend/app/schemas/time_entry.py"]
    n9["backend/app/services/time_entry_service.py"]
    n10["backend/app/utils/time.py"]
    n11["backend/tests/test_time_entries.py"]
    n0 --> n2
    n0 --> n3
    n0 --> n5
    n1 --> n0
    n1 --> n4
    n1 --> n5
    n3 --> n10
    n4 --> n5
    n4 --> n10
    n5 --> n4
    n5 --> n10
    n6 --> n10
    n7 --> n2
    n7 --> n8
    n7 --> n9
    n9 --> n0
    n9 --> n1
    n9 --> n2
    n9 --> n3
    n9 --> n4
    n9 --> n5
    n9 --> n6
    n9 --> n8
    n9 --> n10
    n11 --> n0
    n11 --> n1
    n11 --> n2
    n11 --> n5
    n11 --> n6
    n11 --> n8
    n11 --> n9
    click n0 "../modules/authority.md"
    click n1 "../modules/commands.md"
    click n2 "../modules/config.md"
    click n3 "../modules/models_identity.md"
    click n4 "../modules/models_project.md"
    click n5 "../modules/models_task.md"
    click n6 "../modules/models_time_entry.md"
    click n7 "../modules/time_entries.md"
    click n8 "../modules/schemas_time_entry.md"
    click n9 "../modules/time_entry_service.md"
    click n10 "../modules/time.md"
    click n11 "../modules/test_time_entries.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [time_entries](../modules/time_entries.md) |
| Inbound | [test_time_entries](../modules/test_time_entries.md) |
| Outbound | [authority](../modules/authority.md) |
| Outbound | [commands](../modules/commands.md) |
| Outbound | [config](../modules/config.md) |
| Outbound | [models_identity](../modules/models_identity.md) |
| Outbound | [models_project](../modules/models_project.md) |
| Outbound | [models_task](../modules/models_task.md) |
| Outbound | [models_time_entry](../modules/models_time_entry.md) |
| Outbound | [schemas_time_entry](../modules/schemas_time_entry.md) |
| Outbound | [time](../modules/time.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [TimeEntryVersionConflict](../entities/TimeEntryVersionConflict.md) | 20 | `PlanningConflict` | — |
| [TimeEntryService](../entities/TimeEntryService.md) | 29 | — | — |
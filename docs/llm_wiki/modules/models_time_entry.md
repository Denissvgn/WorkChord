# time_entry Module

**Path:** `backend/app/models/time_entry.py`

## Description

Private explicit work records and retained corrections, independent of task state.

The ledger retains original project/task/principal IDs without deletion-cascading foreign keys. Current records can be corrected or voided only through authorized versioned commands; revisions are append-only. ORM guards reject physical deletion, scope/authorship rewrites and unjournaled mutation. Full database transfer/backup preserves the tables, while task recovery leaves them intact.

## Imports

| Source | Symbols |
|--------|---------|
| `app.database` | `Base` |
| `app.utils.time` | `UTCDateTime`, `utc_now` |
| `datetime` | `date`, `datetime` |
| `sqlalchemy` | `CheckConstraint`, `Date`, `Index`, `Integer`, `String`, `Text`, `UniqueConstraint`, `event`, `inspect` |
| `sqlalchemy.orm` | `Mapped`, `Session`, `mapped_column` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/database.py"]
    n1["backend/app/models/__init__.py"]
    n2["backend/app/models/time_entry.py"]
    n3["backend/app/services/time_entry_service.py"]
    n4["backend/app/utils/time.py"]
    n5["backend/tests/test_time_entries.py"]
    n1 --> n2
    n2 --> n0
    n2 --> n4
    n3 --> n2
    n3 --> n4
    n5 --> n2
    n5 --> n3
    click n0 "../modules/app_database.md"
    click n1 "../modules/models___init__.md"
    click n2 "../modules/models_time_entry.md"
    click n3 "../modules/time_entry_service.md"
    click n4 "../modules/time.md"
    click n5 "../modules/test_time_entries.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [models___init__](../modules/models___init__.md) |
| Inbound | [time_entry_service](../modules/time_entry_service.md) |
| Inbound | [test_time_entries](../modules/test_time_entries.md) |
| Outbound | [app_database](../modules/app_database.md) |
| Outbound | [time](../modules/time.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [TimeEntry](../entities/TimeEntry.md) | 12 | `Base` | — |
| [TimeEntryRevision](../entities/TimeEntryRevision.md) | 40 | `Base` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `retain_time_entry_history` | `(session, _context, _instances)` | `@event.listens_for(Session, 'before_flush')` | — |
| `reject_time_history_rewrites` | `(state)` | `@event.listens_for(Session, 'do_orm_execute')` | — |
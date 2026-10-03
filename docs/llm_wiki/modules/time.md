# time Module

**Path:** `backend/app/utils/time.py`

## Description

Timezone-safe UTC helpers and SQLAlchemy datetime normalization.

## Imports

| Source | Symbols |
|--------|---------|
| `datetime` | `UTC`, `datetime` |
| `sqlalchemy` | `DateTime` |
| `sqlalchemy.engine.interfaces` | `Dialect` |
| `sqlalchemy.types` | `TypeDecorator` |
| `typing` | `Any` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/app/utils/time.py"]
    n0 --> n1
    click n1 "../modules/time.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (62) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

> All 62 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [UTCDateTime](../entities/UTCDateTime.md) | 28 | `TypeDecorator[datetime]` | Persist UTC datetimes and always return aware UTC values. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `utc_now` | `() -> datetime` | — | Return the current time as an aware UTC datetime. |
| `as_utc` | `(value: datetime) -> datetime` | — | Normalize an aware or legacy-naive UTC datetime to aware UTC. |

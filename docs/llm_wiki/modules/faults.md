# faults Module

**Path:** `backend/tests/support/faults.py`

## Description

Clock, concurrency, and deterministic fault-injection helpers.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `asyncio` | `asyncio` |
| `dataclasses` | `dataclass` |
| `datetime` | `UTC`, `datetime`, `timedelta` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/tests/support/__init__.py"]
    n1["backend/tests/support/faults.py"]
    n0 --> n1
    click n0 "../modules/support___init__.md"
    click n1 "../modules/faults.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [support___init__](../modules/support___init__.md) |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [FrozenClock](../entities/FrozenClock.md) | 11 | — | A manually advanced UTC clock for lease and expiry tests. |
| [FailureInjector](../entities/FailureInjector.md) | 26 | — | Raise an explicit queued failure at a named deterministic checkpoint. |
| [AsyncBarrier](../entities/AsyncBarrier.md) | 45 | — | Reusable asyncio barrier for controlled concurrency interleavings. |

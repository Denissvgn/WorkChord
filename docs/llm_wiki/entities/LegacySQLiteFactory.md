# LegacySQLiteFactory

**Location:** `backend/tests/support/factories.py:80`
**Kind:** Class
**Bases:** —
**Module:** [factories](../modules/factories.md)

## Description

Create representative pre-Alembic SQLite sources for migration tests.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `create` | `(path: Path, *, with_orphan: bool = False) -> Path` | — | Create a valid source, or one deliberately containing an orphan. |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["LegacySQLiteFactory (backend/tests/support/factories.py)"]
    n1["legacy_sqlite_factory (backend/tests/conftest.py)"]
    n2["backend/tests/support/__init__.py"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/factories.md"
    click n1 "../modules/conftest.md"
    click n2 "../modules/support___init__.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [factories](../modules/factories.md) | 1 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `legacy_sqlite_factory` | call | [conftest](../modules/conftest.md) | 1 |
| `__init__` | import | [support___init__](../modules/support___init__.md) | — |

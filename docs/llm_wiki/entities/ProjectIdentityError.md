# ProjectIdentityError

**Location:** `backend/app/database_migration/project_identity.py:9`
**Kind:** Class
**Bases:** `RuntimeError`
**Module:** [project_identity](../modules/project_identity.md)

## Description

Refuse an ambiguous identity without changing historical associations.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(code, diagnostics = (), *, truncated = False)` | — | — |
| `detail` | `()` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ProjectIdentityError (backend/app/database_migration/project_identity.py)"]
    n1["RuntimeError"]
    n2["inspect_project_identity (backend/app/database_migration/project_identity.py)"]
    n3["backend/app/services/upgrade_service.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/project_identity.md"
    click n2 "../modules/project_identity.md"
    click n3 "../modules/upgrade_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [project_identity](../modules/project_identity.md) | 2 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `RuntimeError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `inspect_project_identity` | call | [project_identity](../modules/project_identity.md) | 7 |
| `upgrade_service` | import | [upgrade_service](../modules/upgrade_service.md) | — |

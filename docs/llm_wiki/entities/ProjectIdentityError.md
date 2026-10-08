# ProjectIdentityError

**Location:** `backend/app/database_migration/project_identity.py:12`
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
    n3["backend/app/database_migration/source.py"]
    n4["backend/app/database_migration/transfer.py"]
    n5["backend/app/services/upgrade_service.py"]
    n6["backend/tests/database_migration/test_project_identity_scope.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    click n0 "../modules/project_identity.md"
    click n2 "../modules/project_identity.md"
    click n3 "../modules/source.md"
    click n4 "../modules/transfer.md"
    click n5 "../modules/upgrade_service.md"
    click n6 "../modules/test_project_identity_scope.md"
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
| `source` | import | [source](../modules/source.md) | — |
| `transfer` | import | [transfer](../modules/transfer.md) | — |
| `upgrade_service` | import | [upgrade_service](../modules/upgrade_service.md) | — |
| `test_project_identity_scope` | import | [test_project_identity_scope](../modules/test_project_identity_scope.md) | — |

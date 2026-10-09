# WorkspaceAuthorityState

**Location:** `backend/app/models/identity.py:41`
**Kind:** Class
**Bases:** `Base`
**Module:** [models_identity](../modules/models_identity.md)

## Description

_Auto-generated from `WorkspaceAuthorityState` in `backend/app/models/identity.py`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `Mapped[int]` | `mapped_column(Integer, primary_key=True)` | — |
| `bootstrap_principal_id` | `Mapped[int \| None]` | `mapped_column(ForeignKey('principals.id', ondelete='RESTRICT'))` | — |
| `operator_principal_id` | `Mapped[int \| None]` | `mapped_column(ForeignKey('principals.id', ondelete='RESTRICT'))` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["WorkspaceAuthorityState (backend/app/models/identity.py)"]
    n1["Base (backend/app/database.py)"]
    n2["backend/app/http_authority.py"]
    n3["backend/app/routers/identity.py"]
    n4["initialize_control_plane (backend/app/services/identity_service.py)"]
    n5["backend/tests/test_allocation_recovery.py"]
    n6["managed_store (backend/tests/test_managed_authority.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    click n0 "../modules/models_identity.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/http_authority.md"
    click n3 "../modules/routers_identity.md"
    click n4 "../modules/identity_service.md"
    click n5 "../modules/test_allocation_recovery.md"
    click n6 "../modules/test_managed_authority.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [models_identity](../modules/models_identity.md) | 0 | `bootstrap_principal_id`, `id`, `operator_principal_id` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Base` | [app_database](../modules/app_database.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `http_authority` | import | [http_authority](../modules/http_authority.md) | — |
| `identity` | import | [routers_identity](../modules/routers_identity.md) | — |
| `initialize_control_plane` | call | [identity_service](../modules/identity_service.md) | 1 |
| `test_allocation_recovery` | import | [test_allocation_recovery](../modules/test_allocation_recovery.md) | — |
| `managed_store` | call | [test_managed_authority](../modules/test_managed_authority.md) | 1 |

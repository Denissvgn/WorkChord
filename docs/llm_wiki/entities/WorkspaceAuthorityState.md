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

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["WorkspaceAuthorityState (backend/app/models/identity.py)"]
    n1["Base (backend/app/database.py)"]
    n2["backend/app/http_authority.py"]
    n3["backend/app/routers/identity.py"]
    n4["initialize_control_plane (backend/app/services/identity_service.py)"]
    n5["backend/app/services/import_review_service.py"]
    n6["backend/app/services/review_evidence.py"]
    n7["test_binding_and_preset_routes_preserve_credential_permissions (backend/tests/test_agent_model_catalog_api.py)"]
    n8["test_model_catalog_routes_accept_admin_key_agent_key_and_refuse_neither (backend/tests/test_agent_model_catalog_api.py)"]
    n9["backend/tests/test_allocation_recovery.py"]
    n10["_store (backend/tests/test_maintenance_window.py)"]
    n11["managed_store (backend/tests/test_managed_authority.py)"]
    n12["seed (backend/tests/test_pipeline_active_outside_run.py)"]
    n13["backend/tests/test_scoped_review_evidence.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    n10 --> n0
    n11 --> n0
    n12 --> n0
    n13 --> n0
    click n0 "../modules/models_identity.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/http_authority.md"
    click n3 "../modules/routers_identity.md"
    click n4 "../modules/identity_service.md"
    click n5 "../modules/import_review_service.md"
    click n6 "../modules/services_review_evidence.md"
    click n7 "../modules/test_agent_model_catalog_api.md"
    click n8 "../modules/test_agent_model_catalog_api.md"
    click n9 "../modules/test_allocation_recovery.md"
    click n10 "../modules/test_maintenance_window.md"
    click n11 "../modules/test_managed_authority.md"
    click n12 "../modules/test_pipeline_active_outside_run.md"
    click n13 "../modules/test_scoped_review_evidence.md"
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
| `import_review_service` | import | [import_review_service](../modules/import_review_service.md) | — |
| `review_evidence` | import | [services_review_evidence](../modules/services_review_evidence.md) | — |
| `test_binding_and_preset_routes_preserve_credential_permissions` | call | [test_agent_model_catalog_api](../modules/test_agent_model_catalog_api.md) | 1 |
| `test_model_catalog_routes_accept_admin_key_agent_key_and_refuse_neither` | call | [test_agent_model_catalog_api](../modules/test_agent_model_catalog_api.md) | 1 |
| `test_allocation_recovery` | import | [test_allocation_recovery](../modules/test_allocation_recovery.md) | — |
| `_store` | call | [test_maintenance_window](../modules/test_maintenance_window.md) | 1 |
| `managed_store` | call | [test_managed_authority](../modules/test_managed_authority.md) | 1 |
| `seed` | call | [test_pipeline_active_outside_run](../modules/test_pipeline_active_outside_run.md) | 1 |
| `test_scoped_review_evidence` | import | [test_scoped_review_evidence](../modules/test_scoped_review_evidence.md) | — |

> References: showing 12 of 13 logical references; 1 omitted by the 12-row generated summary limit.

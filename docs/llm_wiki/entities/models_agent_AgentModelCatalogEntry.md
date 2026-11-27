# AgentModelCatalogEntry

**Location:** `backend/app/models/agent.py:135`
**Kind:** Class
**Bases:** `Base`
**Module:** [models_agent](../modules/models_agent.md)

## Description

Secret-free provider-neutral model capability declaration.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `Mapped[int]` | `mapped_column(Integer, primary_key=True, autoincrement=True)` | — |
| `key` | `Mapped[str]` | `mapped_column(String(120), unique=True, nullable=False)` | — |
| `provider` | `Mapped[str]` | `mapped_column(String(120), nullable=False)` | — |
| `publisher_key` | `Mapped[Optional[str]]` | `mapped_column(String(120))` | — |
| `configured_model_alias` | `Mapped[str]` | `mapped_column(String(255), nullable=False)` | — |
| `reasoning_tier` | `Mapped[int]` | `mapped_column(Integer, nullable=False)` | — |
| `context_tier` | `Mapped[str]` | `mapped_column(String(20), nullable=False)` | — |
| `modality_tags` | `Mapped[list[Any]]` | `mapped_column(JSON, default=lambda: ['text'], nullable=False)` | — |
| `cost_tier` | `Mapped[str]` | `mapped_column(String(20), nullable=False)` | — |
| `local_first` | `Mapped[bool]` | `mapped_column(Boolean, default=False, server_default=false(), nullable=False)` | — |
| `latency_tier` | `Mapped[str]` | `mapped_column(String(20), nullable=False)` | — |
| `enabled` | `Mapped[bool]` | `mapped_column(Boolean, default=True, nullable=False)` | — |
| `revision` | `Mapped[int]` | `mapped_column(Integer, default=1, nullable=False)` | — |
| `last_verified_at` | `Mapped[Optional[datetime]]` | `mapped_column(UTCDateTime(), nullable=True)` | — |
| `created_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), default=utc_now, nullable=False)` | — |
| `updated_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), default=utc_now, onupdate=utc_now, nullable=False)` | — |
| `bindings` | `Mapped[list['AgentModelBinding']]` | `relationship('AgentModelBinding', back_populates='model_catalog', passive_deletes=True)` | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentModelCatalogEntry (backend/app/models/agent.py)"]
    n1["Base (backend/app/database.py)"]
    n2["backend/app/models/__init__.py"]
    n3["AgentModelCatalogService._catalog_entry (backend/app/services/agent_model_catalog_service.py)"]
    n4["AgentModelCatalogService._catalog_response (backend/app/services/agent_model_catalog_service.py)"]
    n5["backend/app/services/agent_service.py"]
    n6["AgentTeamSetupService._catalog_entries (backend/app/services/agent_team_setup_service.py)"]
    n7["AgentTeamSetupService._reconcile_bindings (backend/app/services/agent_team_setup_service.py)"]
    n8["backend/app/services/execution_planning_window.py"]
    n9["backend/app/services/manual_provenance_service.py"]
    n10["backend/app/services/review_evidence.py"]
    n11["backend/app/services/review_provenance.py"]
    n12["test_actor_provisioning_creates_binding_and_audit_atomically (backend/tests/test_agent_model_catalog_api.py)"]
    n13["test_binding_and_preset_routes_preserve_credential_permissions (backend/tests/test_agent_model_catalog_api.py)"]
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
    click n0 "../modules/models_agent.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/models___init__.md"
    click n3 "../modules/agent_model_catalog_service.md"
    click n4 "../modules/agent_model_catalog_service.md"
    click n5 "../modules/agent_service.md"
    click n6 "../modules/agent_team_setup_service.md"
    click n7 "../modules/agent_team_setup_service.md"
    click n8 "../modules/execution_planning_window.md"
    click n9 "../modules/manual_provenance_service.md"
    click n10 "../modules/services_review_evidence.md"
    click n11 "../modules/review_provenance.md"
    click n12 "../modules/test_agent_model_catalog_api.md"
    click n13 "../modules/test_agent_model_catalog_api.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [models_agent](../modules/models_agent.md) | 0 | `bindings`, `configured_model_alias`, `context_tier`, `cost_tier`, `created_at`, `enabled`, `id`, `key`, `last_verified_at`, `latency_tier`, `local_first`, `modality_tags` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Base` | [app_database](../modules/app_database.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `AgentModelCatalogService._catalog_entry` | type_reference | [agent_model_catalog_service](../modules/agent_model_catalog_service.md) | — |
| `AgentModelCatalogService._catalog_response` | type_reference | [agent_model_catalog_service](../modules/agent_model_catalog_service.md) | — |
| `agent_service` | import | [agent_service](../modules/agent_service.md) | — |
| `AgentTeamSetupService._catalog_entries` | type_reference | [agent_team_setup_service](../modules/agent_team_setup_service.md) | — |
| `AgentTeamSetupService._reconcile_bindings` | type_reference | [agent_team_setup_service](../modules/agent_team_setup_service.md) | — |
| `execution_planning_window` | import | [execution_planning_window](../modules/execution_planning_window.md) | — |
| `manual_provenance_service` | import | [manual_provenance_service](../modules/manual_provenance_service.md) | — |
| `review_evidence` | import | [services_review_evidence](../modules/services_review_evidence.md) | — |
| `review_provenance` | import | [review_provenance](../modules/review_provenance.md) | — |
| `test_actor_provisioning_creates_binding_and_audit_atomically` | call | [test_agent_model_catalog_api](../modules/test_agent_model_catalog_api.md) | 1 |
| `test_binding_and_preset_routes_preserve_credential_permissions` | call | [test_agent_model_catalog_api](../modules/test_agent_model_catalog_api.md) | 2 |

> References: showing 12 of 54 logical references; 42 omitted by the 12-row generated summary limit.

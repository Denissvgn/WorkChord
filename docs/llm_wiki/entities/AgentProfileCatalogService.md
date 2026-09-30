# AgentProfileCatalogService

**Location:** `backend/app/services/agent_profile_catalog_service.py:276`
**Kind:** Class
**Bases:** —
**Module:** [agent_profile_catalog_service](../modules/agent_profile_catalog_service.md)

## Description

Expose and apply stable capability/profile presets without granting permissions.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(db: AsyncSession)` | — | — |
| `catalog` | `() -> list[dict[str, Any]]` | — | — |
| `capability_label_skill_map` | `() -> dict[str, list[str]]` | — | Expose coarse readiness labels as explicit precise-skill choices. |
| `presets` | `() -> list[dict[str, Any]]` | — | — |
| `routes` | `() -> list[dict[str, Any]]` | — | — |
| `apply_preset` | *(async)* `(preset_key: str, *, commit: bool = True) -> TeamMemberProfile` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentProfileCatalogService (backend/app/services/agent_profile_catalog_service.py)"]
    n1["get_agent_profile_presets (backend/app/mcp_agent_tools.py)"]
    n2["get_agent_routes (backend/app/mcp_agent_tools.py)"]
    n3["get_profile_skill_catalog (backend/app/mcp_agent_tools.py)"]
    n4["get_agent_profile_presets (backend/app/routers/agent_catalog.py)"]
    n5["get_agent_route_index (backend/app/routers/agent_catalog.py)"]
    n6["get_profile_skill_catalog (backend/app/routers/agent_catalog.py)"]
    n7["AgentPlanningService.__init__ (backend/app/services/agent_planning_service.py)"]
    n8["AgentTeamSetupService._resolve_profile (backend/app/services/agent_team_setup_service.py)"]
    n9["test_capability_labels_only_expose_explicit_skill_choices (backend/tests/test_agent_routing_contract.py)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    click n0 "../modules/agent_profile_catalog_service.md"
    click n1 "../modules/mcp_agent_tools.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/mcp_agent_tools.md"
    click n4 "../modules/agent_catalog.md"
    click n5 "../modules/agent_catalog.md"
    click n6 "../modules/agent_catalog.md"
    click n7 "../modules/agent_planning_service.md"
    click n8 "../modules/agent_team_setup_service.md"
    click n9 "../modules/test_agent_routing_contract.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_profile_catalog_service](../modules/agent_profile_catalog_service.md) | 6 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `get_agent_profile_presets` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 1 |
| `get_agent_routes` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 1 |
| `get_profile_skill_catalog` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 1 |
| `get_agent_profile_presets` | call | [agent_catalog](../modules/agent_catalog.md) | 1 |
| `get_agent_route_index` | call | [agent_catalog](../modules/agent_catalog.md) | 1 |
| `get_profile_skill_catalog` | call | [agent_catalog](../modules/agent_catalog.md) | 1 |
| `AgentPlanningService.__init__` | call | [agent_planning_service](../modules/agent_planning_service.md) | 1 |
| `AgentTeamSetupService._resolve_profile` | call | [agent_team_setup_service](../modules/agent_team_setup_service.md) | 1 |
| `test_capability_labels_only_expose_explicit_skill_choices` | call | [test_agent_routing_contract](../modules/test_agent_routing_contract.md) | 1 |

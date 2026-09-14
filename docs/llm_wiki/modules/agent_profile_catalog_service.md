# agent_profile_catalog_service Module

**Path:** `backend/app/services/agent_profile_catalog_service.py`

## Description

Code-owned capability catalog, profile presets, and explainable agent routes.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app.models.team_member` | `TeamMemberProfile`, `TeamMemberProfileSkill` |
| `app.services.agent_routing_policy` | `CAPABILITY_LABEL_SKILL_KEYS`, `ROUTING_SKILL_DEFINITIONS` |
| `sqlalchemy` | `select` |
| `sqlalchemy.exc` | `IntegrityError` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |
| `sqlalchemy.orm` | `selectinload` |
| `typing` | `Any` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/mcp_agent_tools.py"]
    n1["backend/app/models/team_member.py"]
    n2["backend/app/routers/agent_catalog.py"]
    n3["backend/app/services/agent_planning_service.py"]
    n4["backend/app/services/agent_profile_catalog_service.py"]
    n5["backend/app/services/agent_routing_policy.py"]
    n6["backend/app/services/agent_team_setup_service.py"]
    n7["backend/tests/test_agent_routing_contract.py"]
    n0 --> n3
    n0 --> n4
    n0 --> n6
    n2 --> n3
    n2 --> n4
    n3 --> n1
    n3 --> n4
    n4 --> n1
    n4 --> n5
    n6 --> n1
    n6 --> n4
    n7 --> n4
    n7 --> n5
    click n0 "../modules/mcp_agent_tools.md"
    click n1 "../modules/team_member.md"
    click n2 "../modules/agent_catalog.md"
    click n3 "../modules/agent_planning_service.md"
    click n4 "../modules/agent_profile_catalog_service.md"
    click n5 "../modules/agent_routing_policy.md"
    click n6 "../modules/agent_team_setup_service.md"
    click n7 "../modules/test_agent_routing_contract.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [mcp_agent_tools](../modules/mcp_agent_tools.md) |
| Inbound | [agent_catalog](../modules/agent_catalog.md) |
| Inbound | [agent_planning_service](../modules/agent_planning_service.md) |
| Inbound | [agent_team_setup_service](../modules/agent_team_setup_service.md) |
| Inbound | [test_agent_routing_contract](../modules/test_agent_routing_contract.md) |
| Outbound | [team_member](../modules/team_member.md) |
| Outbound | [agent_routing_policy](../modules/agent_routing_policy.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [AgentProfileCatalogService](../entities/AgentProfileCatalogService.md) | 274 | — | Expose and apply stable capability/profile presets without granting permissions. |

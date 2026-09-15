# agent_profile_catalog_service Module

**Path:** `backend/app/services/agent_profile_catalog_service.py`

## Description

Code-owned capability catalog, profile presets, and explainable agent routes.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app.commands` | `commit_or_flush` |
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
    n0["backend/app/commands.py"]
    n1["backend/app/mcp_agent_tools.py"]
    n2["backend/app/models/team_member.py"]
    n3["backend/app/routers/agent_catalog.py"]
    n4["backend/app/services/agent_planning_service.py"]
    n5["backend/app/services/agent_profile_catalog_service.py"]
    n6["backend/app/services/agent_routing_policy.py"]
    n7["backend/app/services/agent_team_setup_service.py"]
    n8["backend/tests/test_agent_routing_contract.py"]
    n0 --> n2
    n1 --> n0
    n1 --> n4
    n1 --> n5
    n1 --> n7
    n3 --> n4
    n3 --> n5
    n4 --> n0
    n4 --> n2
    n4 --> n5
    n5 --> n0
    n5 --> n2
    n5 --> n6
    n7 --> n0
    n7 --> n2
    n7 --> n5
    n8 --> n5
    n8 --> n6
    click n0 "../modules/commands.md"
    click n1 "../modules/mcp_agent_tools.md"
    click n2 "../modules/team_member.md"
    click n3 "../modules/agent_catalog.md"
    click n4 "../modules/agent_planning_service.md"
    click n5 "../modules/agent_profile_catalog_service.md"
    click n6 "../modules/agent_routing_policy.md"
    click n7 "../modules/agent_team_setup_service.md"
    click n8 "../modules/test_agent_routing_contract.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [mcp_agent_tools](../modules/mcp_agent_tools.md) |
| Inbound | [agent_catalog](../modules/agent_catalog.md) |
| Inbound | [agent_planning_service](../modules/agent_planning_service.md) |
| Inbound | [agent_team_setup_service](../modules/agent_team_setup_service.md) |
| Inbound | [test_agent_routing_contract](../modules/test_agent_routing_contract.md) |
| Outbound | [commands](../modules/commands.md) |
| Outbound | [team_member](../modules/team_member.md) |
| Outbound | [agent_routing_policy](../modules/agent_routing_policy.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [AgentProfileCatalogService](../entities/AgentProfileCatalogService.md) | 276 | — | Expose and apply stable capability/profile presets without granting permissions. |

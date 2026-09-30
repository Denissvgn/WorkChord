# assignee_recommendation_service Module

**Path:** `backend/app/services/assignee_recommendation_service.py`

## Description

Explainable assignee recommendations from team capability profiles.

## Imports

| Source | Symbols |
|--------|---------|
| `app.models.task` | `Task` |
| `app.models.team_member` | `TeamMember`, `TeamMemberProfile`, `TeamMemberProfileSkill` |
| `app.models.triage` | `TriageClassificationSuggestion`, `TriageItem` |
| `app.schemas.team` | `AssigneeRecommendationResponse` |
| `app.services.team_service` | `TeamService` |
| `dataclasses` | `dataclass` |
| `datetime` | `date` |
| `json` | `json` |
| `re` | `re` |
| `sqlalchemy` | `select` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |
| `sqlalchemy.orm` | `selectinload` |
| `typing` | `Any`, `Optional`, `Sequence` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/mcp_agent_tools.py"]
    n1["backend/app/models/task.py"]
    n2["backend/app/models/team_member.py"]
    n3["backend/app/models/triage.py"]
    n4["backend/app/routers/tasks.py"]
    n5["backend/app/routers/triage.py"]
    n6["backend/app/schemas/team.py"]
    n7["backend/app/services/assignee_recommendation_service.py"]
    n8["backend/app/services/task_bulk_operation_service.py"]
    n9["backend/app/services/team_service.py"]
    n10["backend/tests/test_agent_routing_wave6_qualification.py"]
    n0 --> n6
    n0 --> n7
    n0 --> n9
    n1 --> n2
    n2 --> n1
    n3 --> n1
    n3 --> n2
    n4 --> n1
    n4 --> n6
    n4 --> n7
    n4 --> n8
    n5 --> n6
    n5 --> n7
    n7 --> n1
    n7 --> n2
    n7 --> n3
    n7 --> n6
    n7 --> n9
    n8 --> n1
    n8 --> n6
    n8 --> n7
    n9 --> n1
    n9 --> n2
    n9 --> n6
    n10 --> n0
    n10 --> n1
    n10 --> n2
    n10 --> n7
    click n0 "../modules/mcp_agent_tools.md"
    click n1 "../modules/models_task.md"
    click n2 "../modules/team_member.md"
    click n3 "../modules/models_triage.md"
    click n4 "../modules/tasks.md"
    click n5 "../modules/routers_triage.md"
    click n6 "../modules/schemas_team.md"
    click n7 "../modules/assignee_recommendation_service.md"
    click n8 "../modules/task_bulk_operation_service.md"
    click n9 "../modules/team_service.md"
    click n10 "../modules/test_agent_routing_wave6_qualification.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [mcp_agent_tools](../modules/mcp_agent_tools.md) |
| Inbound | [tasks](../modules/tasks.md) |
| Inbound | [routers_triage](../modules/routers_triage.md) |
| Inbound | [task_bulk_operation_service](../modules/task_bulk_operation_service.md) |
| Inbound | [test_agent_routing_wave6_qualification](../modules/test_agent_routing_wave6_qualification.md) |
| Outbound | [models_task](../modules/models_task.md) |
| Outbound | [team_member](../modules/team_member.md) |
| Outbound | [models_triage](../modules/models_triage.md) |
| Outbound | [schemas_team](../modules/schemas_team.md) |
| Outbound | [team_service](../modules/team_service.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [RecommendationContext](../entities/RecommendationContext.md) | 23 | — | Normalized work item context for assignee recommendation scoring. |
| [AssigneeRecommendationService](../entities/AssigneeRecommendationService.md) | 38 | — | Rank iteration team members for task and triage assignment. |

# test_verification_preview_history Module

**Path:** `backend/tests/test_verification_preview_history.py`

## Description

Verification previews keep assignment-based independence until the stricter policy is enabled.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `Authority` |
| `app.models.agent` | `AgentModelBinding`, `AgentRun`, `AgentTaskAssignment` |
| `app.models.project` | `Project` |
| `app.models.team_member` | `TeamMemberProfileSkill` |
| `app.query_limits` | `CollectionLimitExceededError`, `MAX_BOUNDED_LIST_ITEMS` |
| `app.schemas.agent_routing` | `AgentRoutingPreviewCreate` |
| `app.services` | `agent_routing_service` |
| `app.services.agent_routing_policy` | `ROUTING_DECISION_AUTHORITY` |
| `app.services.agent_routing_service` | `AgentRoutingService` |
| `app.services.identity_service` | `initialize_control_plane` |
| `datetime` | `UTC`, `datetime` |
| `json` | `json` |
| `pytest` | `pytest` |
| `sqlalchemy` | `insert` |
| `tests.test_agent_routing_service` | `_assessment_command`, `_command_context`, `_rollout`, `_routing_fixture` |
| `tests.test_team_pm_dispatch` | `db_session_factory` |
| `unittest.mock` | `AsyncMock` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/authority.py"]
    n1["backend/app/models/agent.py"]
    n2["backend/app/models/project.py"]
    n3["backend/app/models/team_member.py"]
    n4["backend/app/query_limits.py"]
    n5["backend/app/schemas/agent_routing.py"]
    n6["backend/app/services/agent_routing_policy.py"]
    n7["backend/app/services/agent_routing_service.py"]
    n8["backend/app/services/identity_service.py"]
    n9["backend/tests/test_agent_routing_service.py"]
    n10["backend/tests/test_team_pm_dispatch.py"]
    n11["backend/tests/test_verification_preview_history.py"]
    n0 --> n1
    n0 --> n2
    n1 --> n2
    n1 --> n3
    n2 --> n1
    n2 --> n3
    n3 --> n1
    n3 --> n2
    n5 --> n6
    n7 --> n0
    n7 --> n1
    n7 --> n3
    n7 --> n4
    n7 --> n5
    n7 --> n6
    n8 --> n0
    n8 --> n3
    n9 --> n0
    n9 --> n1
    n9 --> n2
    n9 --> n3
    n9 --> n5
    n9 --> n6
    n9 --> n7
    n10 --> n0
    n10 --> n1
    n10 --> n2
    n10 --> n8
    n11 --> n0
    n11 --> n1
    n11 --> n2
    n11 --> n3
    n11 --> n4
    n11 --> n5
    n11 --> n6
    n11 --> n7
    n11 --> n8
    n11 --> n9
    n11 --> n10
    click n0 "../modules/authority.md"
    click n1 "../modules/models_agent.md"
    click n2 "../modules/models_project.md"
    click n3 "../modules/team_member.md"
    click n4 "../modules/query_limits.md"
    click n5 "../modules/agent_routing.md"
    click n6 "../modules/agent_routing_policy.md"
    click n7 "../modules/agent_routing_service.md"
    click n8 "../modules/identity_service.md"
    click n9 "../modules/test_agent_routing_service.md"
    click n10 "../modules/test_team_pm_dispatch.md"
    click n11 "../modules/test_verification_preview_history.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [authority](../modules/authority.md) |
| Outbound | [models_agent](../modules/models_agent.md) |
| Outbound | [models_project](../modules/models_project.md) |
| Outbound | [team_member](../modules/team_member.md) |
| Outbound | [query_limits](../modules/query_limits.md) |
| Outbound | [agent_routing](../modules/agent_routing.md) |
| Outbound | [agent_routing_policy](../modules/agent_routing_policy.md) |
| Outbound | [agent_routing_service](../modules/agent_routing_service.md) |
| Outbound | [identity_service](../modules/identity_service.md) |
| Outbound | [test_agent_routing_service](../modules/test_agent_routing_service.md) |
| Outbound | [test_team_pm_dispatch](../modules/test_team_pm_dispatch.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 1 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `test_verification_preview_applies_execution_history_bound_only_for_strict_projects` | *(async)* `(db_session, profile_factory, actor_factory, team_member_factory, task_factory, monkeypatch)` | `@pytest.mark.asyncio`, `@pytest.mark.parametrize('db_session_factory', [pytest.param('sqlite', marks=pytest.mark.sqlite), pytest.param('postgresql', marks=[pytest.mark.postgresql, pytest.mark.allow_network])], indirect=True)` | — |

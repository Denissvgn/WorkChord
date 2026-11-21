# test_team_member_agent_connected Module

**Path:** `backend/tests/test_team_member_agent_connected.py`

## Description

Team-member responses say whether an agent is connected, to every reader, without naming it.

## Imports

| Source | Symbols |
|--------|---------|
| `app.models.agent` | `AgentActor` |
| `app.models.identity` | `WorkspaceMembership` |
| `app.models.team_member` | `TeamMember`, `TeamMemberProfile` |
| `app.services.agent_service` | `hash_api_key` |
| `pytest` | `pytest` |
| `tests.test_delivery_scenarios` | `delivery_store` |
| `tests.test_managed_authority` | `client`, `managed_store` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/models/agent.py"]
    n1["backend/app/models/identity.py"]
    n2["backend/app/models/team_member.py"]
    n3["backend/app/services/agent_service.py"]
    n4["backend/tests/test_delivery_scenarios.py"]
    n5["backend/tests/test_managed_authority.py"]
    n6["backend/tests/test_task_assignee_kind.py"]
    n7["backend/tests/test_team_member_agent_connected.py"]
    n0 --> n2
    n2 --> n0
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n4 --> n2
    n4 --> n3
    n5 --> n0
    n5 --> n1
    n5 --> n4
    n6 --> n2
    n6 --> n4
    n6 --> n5
    n6 --> n7
    n7 --> n0
    n7 --> n1
    n7 --> n2
    n7 --> n3
    n7 --> n4
    n7 --> n5
    click n0 "../modules/models_agent.md"
    click n1 "../modules/models_identity.md"
    click n2 "../modules/team_member.md"
    click n3 "../modules/agent_service.md"
    click n4 "../modules/test_delivery_scenarios.md"
    click n5 "../modules/test_managed_authority.md"
    click n6 "../modules/test_task_assignee_kind.md"
    click n7 "../modules/test_team_member_agent_connected.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [test_task_assignee_kind](../modules/test_task_assignee_kind.md) |
| Outbound | [models_agent](../modules/models_agent.md) |
| Outbound | [models_identity](../modules/models_identity.md) |
| Outbound | [team_member](../modules/team_member.md) |
| Outbound | [agent_service](../modules/agent_service.md) |
| Outbound | [test_delivery_scenarios](../modules/test_delivery_scenarios.md) |
| Outbound | [test_managed_authority](../modules/test_managed_authority.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 1 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_seed_agent_members` | *(async)* `(factory, scenario, people, *, workspace_member = True)` | — | One connected agent, one whose only actor is disabled, one still onboarding, beside the human row. |
| `test_every_reader_sees_agent_connected_on_the_embedded_profile` | *(async)* `(managed_store, reader)` | `@pytest.mark.parametrize('reader', list(READERS))` | — |
| `test_reader_without_profile_access_still_cannot_read_the_profile` | *(async)* `(managed_store)` | — | The team row carries the reader-safe part; the profile endpoints stay closed to that reader. |
| `_assert_names_no_agent` | `(text)` | — | — |
| `test_single_member_read_carries_agent_connected` | *(async)* `(managed_store, workspace_member)` | `@pytest.mark.parametrize('workspace_member', [True, False], ids=['workspace member', 'project-only member'])` | — |

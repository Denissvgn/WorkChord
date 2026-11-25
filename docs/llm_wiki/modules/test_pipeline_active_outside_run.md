# test_pipeline_active_outside_run Module

**Path:** `backend/tests/test_pipeline_active_outside_run.py`

## Description

Active work with no WorkChord run is shown in its own pipeline stage.

## Imports

| Source | Symbols |
|--------|---------|
| `app` | `mcp_agent_tools` |
| `app.config` | `get_settings` |
| `app.models.agent` | `AgentActor`, `AgentRun`, `AgentTaskAssignment` |
| `app.models.calendar` | `Calendar` |
| `app.models.identity` | `Principal`, `WorkspaceAuthorityState` |
| `app.models.iteration` | `Iteration` |
| `app.models.task` | `Task` |
| `app.models.team_member` | `TeamMember`, `TeamMemberProfile` |
| `app.utils.time` | `utc_now` |
| `datetime` | `date`, `timedelta` |
| `json` | `json` |
| `sqlalchemy` | `select` |
| `tests.test_delivery_scenarios` | `delivery_store` |
| `tests.test_managed_authority` | `client` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/config.py"]
    n1["backend/app/mcp_agent_tools.py"]
    n2["backend/app/models/agent.py"]
    n3["backend/app/models/calendar.py"]
    n4["backend/app/models/identity.py"]
    n5["backend/app/models/iteration.py"]
    n6["backend/app/models/task.py"]
    n7["backend/app/models/team_member.py"]
    n8["backend/app/utils/time.py"]
    n9["backend/tests/test_delivery_scenarios.py"]
    n10["backend/tests/test_managed_authority.py"]
    n11["backend/tests/test_pipeline_active_outside_run.py"]
    n1 --> n0
    n1 --> n2
    n2 --> n6
    n2 --> n7
    n2 --> n8
    n3 --> n5
    n4 --> n8
    n5 --> n3
    n5 --> n6
    n5 --> n7
    n6 --> n2
    n6 --> n5
    n6 --> n7
    n6 --> n8
    n7 --> n2
    n7 --> n5
    n7 --> n6
    n7 --> n8
    n9 --> n6
    n9 --> n7
    n10 --> n0
    n10 --> n2
    n10 --> n4
    n10 --> n6
    n10 --> n8
    n10 --> n9
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
    click n0 "../modules/config.md"
    click n1 "../modules/mcp_agent_tools.md"
    click n2 "../modules/models_agent.md"
    click n3 "../modules/models_calendar.md"
    click n4 "../modules/models_identity.md"
    click n5 "../modules/models_iteration.md"
    click n6 "../modules/models_task.md"
    click n7 "../modules/team_member.md"
    click n8 "../modules/time.md"
    click n9 "../modules/test_delivery_scenarios.md"
    click n10 "../modules/test_managed_authority.md"
    click n11 "../modules/test_pipeline_active_outside_run.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [config](../modules/config.md) |
| Outbound | [mcp_agent_tools](../modules/mcp_agent_tools.md) |
| Outbound | [models_agent](../modules/models_agent.md) |
| Outbound | [models_calendar](../modules/models_calendar.md) |
| Outbound | [models_identity](../modules/models_identity.md) |
| Outbound | [models_iteration](../modules/models_iteration.md) |
| Outbound | [models_task](../modules/models_task.md) |
| Outbound | [team_member](../modules/team_member.md) |
| Outbound | [time](../modules/time.md) |
| Outbound | [test_delivery_scenarios](../modules/test_delivery_scenarios.md) |
| Outbound | [test_managed_authority](../modules/test_managed_authority.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `seed` | *(async)* `(factory)` | — | — |
| `stage_of` | `(pipeline, task_id)` | — | — |
| `test_active_task_without_a_run_is_its_own_stage_on_rest_and_mcp` | *(async)* `(delivery_store, monkeypatch)` | — | — |
| `test_every_open_task_appears_in_exactly_one_stage` | *(async)* `(delivery_store)` | — | — |
| `test_outside_run_task_is_not_offered_for_recovery` | *(async)* `(delivery_store)` | — | — |

# test_unscheduled_tasks Module

**Path:** `backend/tests/test_unscheduled_tasks.py`

## Description

The scheduler says which planned tasks it left without dates, and readiness says how to fix it.

## Imports

| Source | Symbols |
|--------|---------|
| `app.models.agent` | `AgentActor` |
| `app.models.task` | `Task` |
| `app.models.team_member` | `TeamMember`, `TeamMemberProfile` |
| `app.schemas.agent_planning` | `AgentPlanningCommandContext`, `AgentScheduleCommand` |
| `app.services.agent_planning_service` | `AgentPlanningService` |
| `app.services.agent_readiness` | `evaluate_agent_readiness` |
| `app.services.scheduler_service` | `SchedulerService` |
| `pytest` | `pytest` |
| `sqlalchemy` | `select` |
| `tests.test_delivery_scenarios` | `delivery_store` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/models/agent.py"]
    n1["backend/app/models/task.py"]
    n2["backend/app/models/team_member.py"]
    n3["backend/app/schemas/agent_planning.py"]
    n4["backend/app/services/agent_planning_service.py"]
    n5["backend/app/services/agent_readiness.py"]
    n6["backend/app/services/scheduler_service.py"]
    n7["backend/tests/test_delivery_scenarios.py"]
    n8["backend/tests/test_unscheduled_tasks.py"]
    n0 --> n1
    n0 --> n2
    n1 --> n0
    n1 --> n2
    n2 --> n0
    n2 --> n1
    n4 --> n0
    n4 --> n1
    n4 --> n2
    n4 --> n3
    n4 --> n6
    n5 --> n1
    n6 --> n1
    n6 --> n2
    n7 --> n1
    n7 --> n2
    n8 --> n0
    n8 --> n1
    n8 --> n2
    n8 --> n3
    n8 --> n4
    n8 --> n5
    n8 --> n6
    n8 --> n7
    click n0 "../modules/models_agent.md"
    click n1 "../modules/models_task.md"
    click n2 "../modules/team_member.md"
    click n3 "../modules/schemas_agent_planning.md"
    click n4 "../modules/agent_planning_service.md"
    click n5 "../modules/agent_readiness.md"
    click n6 "../modules/scheduler_service.md"
    click n7 "../modules/test_delivery_scenarios.md"
    click n8 "../modules/test_unscheduled_tasks.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [models_agent](../modules/models_agent.md) |
| Outbound | [models_task](../modules/models_task.md) |
| Outbound | [team_member](../modules/team_member.md) |
| Outbound | [schemas_agent_planning](../modules/schemas_agent_planning.md) |
| Outbound | [agent_planning_service](../modules/agent_planning_service.md) |
| Outbound | [agent_readiness](../modules/agent_readiness.md) |
| Outbound | [scheduler_service](../modules/scheduler_service.md) |
| Outbound | [test_delivery_scenarios](../modules/test_delivery_scenarios.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 1 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_schedule_reason` | `(task: Task) -> tuple[bool, str]` | — | — |
| `test_readiness_names_the_missing_scheduling_step` | `(iteration_id, assignee_id, expected)` | `@pytest.mark.parametrize(('iteration_id', 'assignee_id', 'expected'), [(None, None, 'add it to an iteration'), (1, None, 'Assign it to a capacity row in this iteration'), (1, 7, 'run the scheduler for this iteration')])` | — |
| `test_scheduler_reports_unassigned_and_outside_assignee_tasks` | *(async)* `(delivery_store)` | — | — |
| `test_agent_capacity_row_assignment_and_apply_schedule_an_unassigned_task` | *(async)* `(delivery_store)` | — | — |

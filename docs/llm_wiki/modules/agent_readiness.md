# agent_readiness Module

**Path:** `backend/app/services/agent_readiness.py`

## Description

Deterministic task readiness evaluation for agent handoff.

Readiness uses the same inherited work flags as human lifecycle policy. Complete ancestry is required; direct or ancestor deferral prevents handoff, and missing ancestry is reported as unavailable rather than a ready leaf.

## Imports

| Source | Symbols |
|--------|---------|
| `app.models.task` | `Task`, `TaskDependency`, `TaskStatus` |
| `app.schemas.task` | `TaskAgentReadiness`, `TaskAgentReadinessCriterion` |
| `app.services.agent_routing_policy` | `CAPABILITY_LABEL_SKILL_KEYS` |
| `app.services.task_brief_service` | `brief_definition_blockers` |
| `app.services.work_metrics` | `effective_work_flags`, `postponed_work_under` |
| `app.utils.time` | `as_utc`, `utc_now` |
| `datetime` | `datetime` |
| `re` | `re` |
| `sqlalchemy.orm` | `attributes` |
| `typing` | `Any`, `Iterable`, `Optional`, `Sequence` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/models/task.py"]
    n1["backend/app/schemas/task.py"]
    n2["backend/app/services/agent_readiness.py"]
    n3["backend/app/services/agent_routing_policy.py"]
    n4["backend/app/services/agent_service.py"]
    n5["backend/app/services/task_brief_service.py"]
    n6["backend/app/services/task_service.py"]
    n7["backend/app/services/work_metrics.py"]
    n8["backend/app/utils/time.py"]
    n9["backend/tests/test_postponed_out_of_scheduling.py"]
    n10["backend/tests/test_postponement_agent_tools.py"]
    n11["backend/tests/test_unscheduled_tasks.py"]
    n0 --> n8
    n2 --> n0
    n2 --> n1
    n2 --> n3
    n2 --> n5
    n2 --> n7
    n2 --> n8
    n4 --> n0
    n4 --> n1
    n4 --> n2
    n4 --> n6
    n4 --> n8
    n5 --> n0
    n5 --> n6
    n6 --> n0
    n6 --> n1
    n6 --> n2
    n6 --> n5
    n6 --> n7
    n7 --> n0
    n7 --> n8
    n9 --> n0
    n9 --> n2
    n9 --> n4
    n9 --> n7
    n10 --> n0
    n10 --> n2
    n10 --> n4
    n10 --> n8
    n11 --> n0
    n11 --> n2
    click n0 "../modules/models_task.md"
    click n1 "../modules/schemas_task.md"
    click n2 "../modules/agent_readiness.md"
    click n3 "../modules/agent_routing_policy.md"
    click n4 "../modules/agent_service.md"
    click n5 "../modules/task_brief_service.md"
    click n6 "../modules/task_service.md"
    click n7 "../modules/services_work_metrics.md"
    click n8 "../modules/time.md"
    click n9 "../modules/test_postponed_out_of_scheduling.md"
    click n10 "../modules/test_postponement_agent_tools.md"
    click n11 "../modules/test_unscheduled_tasks.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [agent_service](../modules/agent_service.md) |
| Inbound | [task_service](../modules/task_service.md) |
| Inbound | [test_postponed_out_of_scheduling](../modules/test_postponed_out_of_scheduling.md) |
| Inbound | [test_postponement_agent_tools](../modules/test_postponement_agent_tools.md) |
| Inbound | [test_unscheduled_tasks](../modules/test_unscheduled_tasks.md) |
| Outbound | [models_task](../modules/models_task.md) |
| Outbound | [schemas_task](../modules/schemas_task.md) |
| Outbound | [agent_routing_policy](../modules/agent_routing_policy.md) |
| Outbound | [task_brief_service](../modules/task_brief_service.md) |
| Outbound | [services_work_metrics](../modules/services_work_metrics.md) |
| Outbound | [time](../modules/time.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_dependency_task` | `(dependency: TaskDependency) -> Optional[Task]` | — | Return loaded dependency target without triggering lazy IO. |
| `_description_is_actionable` | `(description: Optional[str]) -> tuple[bool, str]` | — | Return whether task description gives enough execution/verification context. |
| `_add_criterion` | `(criteria: list[TaskAgentReadinessCriterion], blockers: list[str], *, key: str, label: str, passed: bool, reason: str) -> None` | — | Append one criterion and record failed reasons as blockers. |
| `evaluate_agent_readiness` | `(task: Task, *, tags: Iterable[str], children: Sequence[Task], dependencies: Sequence[TaskDependency], now: Optional[datetime] = None, current_actor_id: Optional[int] = None, capability_slugs: Optional[set[str]] = None) -> TaskAgentReadiness` | — | Evaluate whether a task is ready for explicit agent execution. |

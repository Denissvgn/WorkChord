# planning_input_context Module

**Path:** `backend/app/services/planning_input_context.py`

## Description

Resolves the same complete affected iteration set for initial resource observations and shared-input commands. Global calendar/profile edits require operator authority; scoped edits require a complete authorized graph. Reads compare revisions before and after resource data, reject scopes above 500 entries or the transport byte limit, and never reserve versions or emit work. New-member drafts observe the target iteration; valid unused inputs return an explicit empty map.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `AuthorityError`, `internal_authority`, `require_operator`, `require_project` |
| `app.commands` | `PlanningConflict` |
| `app.config` | `get_settings` |
| `app.models.calendar` | `Calendar`, `Calendar` |
| `app.models.capacity` | `ProfileAvailability` |
| `app.models.iteration` | `Iteration`, `Iteration` |
| `app.models.project` | `Project`, `Project` |
| `app.models.task` | `Task` |
| `app.models.team_member` | `TeamMember`, `TeamMemberProfile`, `Vacation`, `TeamMember`, `TeamMemberProfile`, `Vacation` |
| `json` | `json` |
| `sqlalchemy` | `select` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/authority.py"]
    n1["backend/app/commands.py"]
    n2["backend/app/config.py"]
    n3["backend/app/models/calendar.py"]
    n4["backend/app/models/capacity.py"]
    n5["backend/app/models/iteration.py"]
    n6["backend/app/models/project.py"]
    n7["backend/app/models/task.py"]
    n8["backend/app/models/team_member.py"]
    n9["backend/app/routers/task_domain.py"]
    n10["backend/app/services/planning_input_context.py"]
    n11["backend/tests/test_planning_input_context.py"]
    n0 --> n2
    n0 --> n6
    n0 --> n7
    n1 --> n0
    n1 --> n4
    n1 --> n5
    n1 --> n6
    n1 --> n7
    n1 --> n10
    n3 --> n5
    n5 --> n3
    n5 --> n6
    n5 --> n7
    n5 --> n8
    n6 --> n5
    n6 --> n7
    n6 --> n8
    n7 --> n5
    n7 --> n6
    n7 --> n8
    n8 --> n5
    n8 --> n6
    n8 --> n7
    n9 --> n0
    n9 --> n7
    n9 --> n8
    n9 --> n10
    n10 --> n0
    n10 --> n1
    n10 --> n2
    n10 --> n3
    n10 --> n4
    n10 --> n5
    n10 --> n6
    n10 --> n7
    n10 --> n8
    n11 --> n0
    n11 --> n1
    n11 --> n2
    n11 --> n3
    n11 --> n4
    n11 --> n5
    n11 --> n8
    n11 --> n10
    click n0 "../modules/authority.md"
    click n1 "../modules/commands.md"
    click n2 "../modules/config.md"
    click n3 "../modules/models_calendar.md"
    click n4 "../modules/models_capacity.md"
    click n5 "../modules/models_iteration.md"
    click n6 "../modules/models_project.md"
    click n7 "../modules/models_task.md"
    click n8 "../modules/team_member.md"
    click n9 "../modules/routers_task_domain.md"
    click n10 "../modules/planning_input_context.md"
    click n11 "../modules/test_planning_input_context.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [commands](../modules/commands.md) |
| Inbound | [routers_task_domain](../modules/routers_task_domain.md) |
| Inbound | [test_planning_input_context](../modules/test_planning_input_context.md) |
| Outbound | [authority](../modules/authority.md) |
| Outbound | [commands](../modules/commands.md) |
| Outbound | [config](../modules/config.md) |
| Outbound | [models_calendar](../modules/models_calendar.md) |
| Outbound | [models_capacity](../modules/models_capacity.md) |
| Outbound | [models_iteration](../modules/models_iteration.md) |
| Outbound | [models_project](../modules/models_project.md) |
| Outbound | [models_task](../modules/models_task.md) |
| Outbound | [team_member](../modules/team_member.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `affected_iteration_ids` | *(async)* `(db, kind, values)` | — | Resolve one complete scope for both read observations and atomic writes. |
| `observe_planning_input` | *(async)* `(db, kind, resource_id, *, creating_member = False)` | — | Read data and revisions together; reject drift without advancing any state. |

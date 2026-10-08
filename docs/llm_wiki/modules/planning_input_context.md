# planning_input_context Module

**Path:** `backend/app/services/planning_input_context.py`

## Description

Resolves the same complete affected iteration set for initial resource observations and shared-input commands. Global calendar/profile edits require operator authority; scoped edits require a complete authorized graph. Reads compare revisions before and after resource data, reject scopes above 500 entries or the transport byte limit, and never reserve versions or emit work. New-member drafts observe the target iteration; valid unused inputs return an explicit empty map.

Profile observations include a bounded current skill snapshot and all affected iteration revisions. Oversized scopes fail explicitly before returning a partial map.

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
| `app.models.team_member` | `TeamMember`, `TeamMemberProfile`, `Vacation`, `TeamMember`, `TeamMemberProfile`, `Vacation`, `TeamMemberProfileSkill` |
| `json` | `json` |
| `sqlalchemy` | `select` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/app/services/planning_input_context.py"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/planning_input_context.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (4) |
| Outbound | `backend` (9) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

> All 12 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `affected_iteration_ids` | *(async)* `(db, kind, values)` | — | Resolve one complete scope for both read observations and atomic writes. |
| `observe_planning_input` | *(async)* `(db, kind, resource_id, *, creating_member = False)` | — | Read data and revisions together; reject drift without advancing any state. |
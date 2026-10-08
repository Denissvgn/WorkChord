# planning_input_context Module

**Path:** `backend/app/services/planning_input_context.py`

## Description

Resolves the same complete affected iteration set for initial resource observations and shared-input commands. Global calendar/profile edits require operator authority; scoped edits require a complete authorized graph. Reads compare revisions before and after resource data, reject scopes above 500 entries or the transport byte limit, and never reserve versions or emit work. New-member drafts observe the target iteration; valid unused inputs return an explicit empty map.

Profile observations include a bounded current skill snapshot and all affected iteration revisions. Oversized scopes fail explicitly before returning a partial map.

Member and legacy vacation observations include all allocations of each affected durable person. Allocation and import intent is resolved read-only before returning complete maps; CSV and member previews reject oversized input and scopes. Member observations include bounded vacation rows. Missing or inaccessible shared inputs use a dedicated not-found exception.

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
| `app.models.team_member` | `TeamMember`, `TeamMember`, `TeamMemberProfile`, `Vacation`, `TeamMember`, `TeamMemberProfile`, `Vacation`, `TeamMemberProfileSkill` |
| `app.services.team_service` | `TeamService` |
| `app.utils.import_parser` | `parse_team_members_text` |
| `csv` | `csv` |
| `io` | `StringIO` |
| `itertools` | `islice` |
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
| Inbound | `backend` (7) |
| Outbound | `backend` (11) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

> All 17 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [PlanningInputUnavailable](../entities/PlanningInputUnavailable.md) | 10 | `LookupError` | A shared planning input is absent or outside the authorized graph. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `prospective_member_profiles` | *(async)* `(db, values)` | — | Resolve import and allocation intent without creating profiles or changing data. |
| `affected_iteration_ids` | *(async)* `(db, kind, values)` | — | Resolve one complete scope for both read observations and atomic writes. |
| `observe_planning_input` | *(async)* `(db, kind, resource_id, *, creating_member = False, intent = None)` | — | Read data and revisions together; reject drift without advancing any state. |
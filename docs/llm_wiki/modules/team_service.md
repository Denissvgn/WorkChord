# team_service Module

**Path:** `backend/app/services/team_service.py`

## Description

Team member service with business logic.

## Imports

| Source | Symbols |
|--------|---------|
| `app.commands` | `commit_or_flush`, `schedule_input_command` |
| `app.models.iteration` | `Iteration` |
| `app.models.task` | `Task` |
| `app.models.team_member` | `TeamMember`, `TeamMemberProfile`, `TeamMemberProfileSkill`, `Vacation` |
| `app.query_limits` | `CollectionLimitExceededError`, `MAX_BOUNDED_LIST_ITEMS` |
| `app.schemas.team` | `TeamMemberCreate`, `TeamMemberProfileCreate`, `TeamMemberProfileSkillCreate`, `TeamMemberProfileSkillUpdate`, `TeamMemberProfileUpdate`, `TeamMemberOptionResponse`, `TeamMemberUpdate`, `VacationCreate`, `VacationUpdate`, `VacationImportError`, `VacationImportResponse`, `MemberCapacity`, `MemberWorkload` |
| `app.services.calendar_service` | `CalendarService` |
| `app.sql_semantics` | `portable_case_insensitive_equal` |
| `csv` | `csv` |
| `datetime` | `date` |
| `io` | `StringIO` |
| `sqlalchemy` | `select` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |
| `sqlalchemy.orm` | `selectinload` |
| `typing` | `Sequence` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/app/services/team_service.py"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/team_service.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (9) |
| Outbound | `backend` (8) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

> All 17 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [TeamService](../entities/TeamService.md) | 36 | — | Service for team member operations. |

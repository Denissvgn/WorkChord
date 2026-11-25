# team_service Module

**Path:** `backend/app/services/team_service.py`

## Description

Manages durable profiles and iteration allocations while adapting legacy vacation routes to canonical profile absences. Imports use the shared planning transaction. Reassigning an allocation removes old absence adapters without changing the former person’s canonical absence; unresolved legacy ranges need reconciliation. Workload comparisons use authoritative hours and the selected nominal workday.

Capacity and workload reads can omit task relationship hydration. Workload hours use the canonical scoped inclusion selector; private person calendar and absence factors remain the same basis as scheduling and readiness.

Workload reads identify uncovered years and unresolved personal calendar rules alongside known capacity. The displayed day equivalents require a finite, positive normal day length from the primary calendar.

Removing a proven unused allocation preserves unrelated task versions. The optional unused-only precondition refuses removal if the row is referenced or its history cannot be verified. The shared profile and allocations in other iterations retain their identities.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `internal_authority`, `AuthorityError`, `internal_authority`, `internal_authority`, `internal_authority`, `internal_authority` |
| `app.commands` | `PlanningConflict`, `atomic_command`, `commit_or_flush`, `schedule_input_command`, `PlanningConflict`, `PlanningConflict`, `PlanningConflict` |
| `app.models.capacity` | `ProfileAbsence`, `ProfileAbsence`, `ProfileAbsence`, `ProfileAbsence` |
| `app.models.identity` | `CommandAudit` |
| `app.models.iteration` | `Iteration` |
| `app.models.task` | `Task` |
| `app.models.team_member` | `TeamMember`, `TeamMemberProfile`, `TeamMemberProfileSkill`, `Vacation` |
| `app.query_limits` | `CollectionLimitExceededError`, `MAX_BOUNDED_LIST_ITEMS` |
| `app.schemas.team` | `TeamMemberCreate`, `TeamMemberProfileCreate`, `TeamMemberProfileSeedKeyBind`, `TeamMemberProfileSkillCreate`, `TeamMemberProfileSkillUpdate`, `TeamMemberProfileUpdate`, `TeamMemberOptionResponse`, `TeamMemberProfileCompact`, `TeamMemberUpdate`, `VacationCreate`, `VacationUpdate`, `VacationImportError`, `VacationImportResponse`, `MemberCapacity`, `MemberWorkload` |
| `app.services.calendar_service` | `CalendarService` |
| `app.services.capacity_adjustments` | `load_dated_availability` |
| `app.services.capacity_service` | `CapacityService`, `CapacityService`, `CapacityService`, `CapacityService`, `CapacityService` |
| `app.services.capacity_transfers` | `refuse_removing_transfer_row` |
| `app.services.work_metrics` | `included_work_ids` |
| `app.sql_semantics` | `portable_case_insensitive_equal` |
| `app.utils.import_parser` | `parse_team_members_text` |
| `csv` | `csv` |
| `datetime` | `date` |
| `io` | `StringIO` |
| `math` | `math` |
| `sqlalchemy` | `select`, `func`, `update` |
| `sqlalchemy.exc` | `IntegrityError` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |
| `sqlalchemy.orm` | `selectinload` |
| `typing` | `Sequence` |
| `uuid` | `uuid4` |

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
| Inbound | `backend` (21) |
| Outbound | `backend` (16) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

> All 37 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [TeamService](../entities/TeamService.md) | 45 | — | Service for team member operations. |
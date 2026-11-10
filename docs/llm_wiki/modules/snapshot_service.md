# snapshot_service Module

**Path:** `backend/app/services/snapshot_service.py`

## Description

Scheduled restoration appends a per-task restoration event after rebuilding the task state. This marks an execution-history boundary without inventing a new capture time or acceptance, while retaining the existing aggregate recovery audit and version-allocation safeguards.

Stores bounded recovery points within the owning planning transaction. Iteration restoration preserves current shared person availability and delivery prerequisites, while legacy unlinked allocation absences retain local recovery. Incoming delivery references block destructive restoration. Restored task versions exceed retained fences and history; current evidence and acceptance are invalidated.

Restoration reconciles the exact saved allocation membership. Safe allocations created after capture detach from the iteration while retaining their identifiers, profiles and global/history references. Complete registered and physical reference ownership is checked before recovery mutation; external task, live assignment, run or evaluating-package references block incompatible restoration. Current shared profiles, availability and canonical absences are preserved.

Allocation recovery validates stable lifetime provenance before any writes, preserves global owner references, and recreates deleted allocations with their saved lifetime. Snapshots lacking lifetime provenance remain immutable and require explicit reconciliation before restore.

Saved planning graphs include complete person lifetime provenance for allocation profiles and all recursive task owners. Preflight validates these references before any recovery mutation, using internal ID/token projections without serializing private profile data; current owner eligibility remains required.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `internal_authority`, `internal_authority`, `require_operator` |
| `app.commands` | `atomic_command`, `current_command`, `lock_iterations`, `PlanningConflict`, `PlanningConflict`, `PlanningConflict`, `PlanningConflict` |
| `app.config` | `get_settings` |
| `app.database` | `Base` |
| `app.models.agent` | `AgentRun`, `AgentTaskAssignment` |
| `app.models.autonomy` | `AgentWorkPackage` |
| `app.models.delivery_dependency` | `DeliveryDependency` |
| `app.models.iteration` | `Iteration` |
| `app.models.recovery` | `ApplicationSnapshot`, `LegacySnapshotImport`, `TaskScheduleBaseline` |
| `app.models.task` | `Task`, `Task`, `TaskDependency` |
| `app.models.team_member` | `TeamMemberProfile`, `TeamMemberProfile`, `TeamMember`, `TeamMemberProfile`, `TeamMember`, `Vacation` |
| `app.routers.snapshots` | `_validate_snapshot_task_payloads` |
| `app.services.delivery_dependency_service` | `DeliveryDependencyService` |
| `app.services.iteration_service` | `IterationService` |
| `app.services.task_brief_service` | `TaskBriefService` |
| `app.services.task_domain_service` | `require_owner` |
| `app.services.task_recovery_service` | `reserve_restored_task_version` |
| `app.services.task_service` | `TaskService`, `TaskService` |
| `app.services.team_service` | `TeamService`, `TeamService` |
| `app.utils.time` | `utc_now` |
| `datetime` | `datetime`, `timedelta`, `date` |
| `hashlib` | `hashlib` |
| `json` | `json` |
| `pathlib` | `Path` |
| `re` | `re` |
| `sqlalchemy` | `select`, `delete`, `inspect`, `or_`, `func` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |
| `uuid` | `UUID`, `UUID` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/app/services/snapshot_service.py"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/snapshot_service.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (20) |
| Outbound | `backend` (20) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

> All 34 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [SnapshotPathError](../entities/SnapshotPathError.md) | 27 | `ValueError` | Raised when a snapshot name cannot be safely resolved inside its iteration directory. |
| [SnapshotService](../entities/SnapshotService.md) | 31 | — | Service for creating and managing iteration snapshots. |
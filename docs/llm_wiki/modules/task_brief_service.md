# task_brief_service Module

**Path:** `backend/app/services/task_brief_service.py`

## Description

Canonical brief rendering, conservative legacy conversion and evidence commands.

One structured brief owns goal, context, scope, exclusions, stable criteria, verification and artifact expectations. Markdown is derived. Conservative legacy conversion retains original prose and review notes; code examples and checkmarks do not establish acceptance. Progress is independently saved, and review requires current revisions and a distinct executor/evidence author. Work-package verification remains authoritative and context-bound.

Actual dependency changes invalidate current progress and acceptance through general updates and individual add/remove commands. Immutable evidence history remains available, a command reserves one task version, and no-op dependency requests retain their current version. Locked graph relationships are loaded explicitly before applying a dependency update.

Formal review on a project with the different-publisher policy requires the assigned verifier’s command to have checked the current task, brief and artifact revisions. A new artifact or changed task version requires a new candidate check before acceptance.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `AuthorityError`, `require_owner_override`, `require_project` |
| `app.autonomy.canonical` | `sha256_hex` |
| `app.commands` | `atomic_command`, `command_transaction`, `command_transaction`, `current_command`, `current_command`, `PlanningConflict`, `current_command` |
| `app.models.autonomy` | `AgentWorkPackage` |
| `app.models.task` | `Task` |
| `app.models.task_brief` | `TaskBriefRevision`, `TaskProgressRecord`, `TaskReviewRecord` |
| `app.schemas.task_brief` | `TaskBrief`, `OwnerAcceptanceWrite`, `ProgressWrite`, `TaskReviewWrite`, `BriefCriterion` |
| `app.schemas.task_routing` | `TaskRouting` |
| `app.services.delivery_dependency_service` | `DeliveryDependencyService` |
| `app.services.identity_service` | `acting_principal_id` |
| `app.services.review_provenance` | `different_publisher_required`, `different_publisher_required` |
| `app.services.snapshot_service` | `SnapshotService` |
| `app.services.task_replacement_service` | `require_acceptable` |
| `app.services.task_routing_service` | `resolve_routing`, `enforce_routing`, `enforce_routing`, `check_routing`, `convert_text_routing` |
| `app.services.task_service` | `TaskService` |
| `copy` | `copy` |
| `dataclasses` | `replace` |
| `re` | `re` |
| `sqlalchemy` | `func`, `select` |
| `uuid` | `NAMESPACE_URL`, `uuid5` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/app/services/task_brief_service.py"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/task_brief_service.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (29) |
| Outbound | `backend` (15) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

> All 39 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [TaskBriefService](../entities/TaskBriefService.md) | 208 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_render_rung` | `(rung: dict) -> str` | — | — |
| `render_routing` | `(routing: dict \| None) -> str` | — | Render the structured routing as the brief's Routing section body. |
| `evidence_brief` | `(brief: dict \| None) -> dict \| None` | — | The part of a stored brief that the brief revision and criterion evidence bind to. |
| `brief_payload` | `(brief: TaskBrief) -> dict` | — | The stored JSON form; a brief without routing keeps the shape it had before routing existed. |
| `render_brief` | `(brief: TaskBrief \| dict) -> str` | — | Derive Markdown from canonical fields without projecting progress as acceptance. |
| `brief_definition_blockers` | `(brief: dict) -> list[str]` | — | Shared structured definition requirements for every agent projection. |
| `import_legacy_brief` | `(task_id: int, description: str \| None) -> tuple[TaskBrief, list[str]]` | — | Conservatively parse supported headings and preserve every unparsed line. |
| `clear_acceptance` | `(task: Task) -> None` | — | Invalidate the current projection while immutable verdict history remains. |
| `clear_execution_evidence` | `(task: Task) -> None` | — | A changed execution context needs fresh progress; history remains immutable. |
| `brief_from_draft` | `(draft, *, title = None, context = None) -> TaskBrief` | — | Project old draft/template fields into the canonical input contract. |
| `_accountable_review_override` | `(authority)` | — | — |

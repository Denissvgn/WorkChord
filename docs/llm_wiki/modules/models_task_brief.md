# task_brief Module

**Path:** `backend/app/models/task_brief.py`

## Description

Append-only brief, progress and ordinary review history.

These records describe task collaboration. Autonomous work-package verification
continues to require its own trusted evidence and fenced verifier protocol.

Brief revisions, criterion progress and review verdicts are append-only records. Original task IDs preserve historical identity when a task is removed; current links may become null. These collaboration records do not replace the trusted autonomous work-package verification protocol.

## Imports

| Source | Symbols |
|--------|---------|
| `app.database` | `Base` |
| `app.utils.time` | `UTCDateTime`, `utc_now` |
| `datetime` | `datetime` |
| `sqlalchemy` | `ForeignKey`, `Integer`, `JSON`, `String`, `Text`, `UniqueConstraint`, `event` |
| `sqlalchemy.orm` | `Mapped`, `mapped_column` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/app/models/task_brief.py"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/models_task_brief.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (10) |
| Outbound | `backend` (2) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

> All 12 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [TaskBriefRevision](../entities/TaskBriefRevision.md) | 16 | `Base` | — |
| [TaskProgressRecord](../entities/TaskProgressRecord.md) | 30 | `Base` | — |
| [TaskReviewRecord](../entities/TaskReviewRecord.md) | 44 | `Base` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_immutable_history` | `(*_args)` | — | — |
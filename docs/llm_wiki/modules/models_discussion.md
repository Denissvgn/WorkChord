# discussion Module

**Path:** `backend/app/models/discussion.py`

## Description

Persists current comments, append-only revisions, per-person subscriptions and unique delivery receipts. Original task identifiers retain discussion through supported restoration; task deletion removes current foreign-key links without deleting revision history. Lifecycle and blockage changes collect transactional notification intents.

## Imports

| Source | Symbols |
|--------|---------|
| `app.database` | `Base` |
| `app.models.task` | `Task` |
| `app.utils.time` | `UTCDateTime`, `utc_now` |
| `datetime` | `datetime` |
| `sqlalchemy` | `CheckConstraint`, `ForeignKey`, `Integer`, `JSON`, `String`, `Text`, `UniqueConstraint`, `event`, `inspect` |
| `sqlalchemy.orm` | `Mapped`, `Session`, `mapped_column` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/database.py"]
    n1["backend/app/models/__init__.py"]
    n2["backend/app/models/discussion.py"]
    n3["backend/app/models/task.py"]
    n4["backend/app/services/discussion_service.py"]
    n5["backend/app/utils/time.py"]
    n6["backend/tests/test_task_discussion.py"]
    n1 --> n2
    n1 --> n3
    n2 --> n0
    n2 --> n3
    n2 --> n5
    n3 --> n0
    n3 --> n5
    n4 --> n2
    n4 --> n3
    n6 --> n2
    n6 --> n3
    n6 --> n4
    n6 --> n5
    click n0 "../modules/app_database.md"
    click n1 "../modules/models___init__.md"
    click n2 "../modules/models_discussion.md"
    click n3 "../modules/models_task.md"
    click n4 "../modules/discussion_service.md"
    click n5 "../modules/time.md"
    click n6 "../modules/test_task_discussion.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [models___init__](../modules/models___init__.md) |
| Inbound | [discussion_service](../modules/discussion_service.md) |
| Inbound | [test_task_discussion](../modules/test_task_discussion.md) |
| Outbound | [app_database](../modules/app_database.md) |
| Outbound | [models_task](../modules/models_task.md) |
| Outbound | [time](../modules/time.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [TaskComment](../entities/models_discussion_TaskComment.md) | 12 | `Base` | — |
| [TaskCommentRevision](../entities/TaskCommentRevision.md) | 27 | `Base` | — |
| [TaskSubscription](../entities/TaskSubscription.md) | 41 | `Base` | — |
| [InboxNotification](../entities/InboxNotification.md) | 50 | `Base` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `prevent_comment_history_rewrite` | `(state)` | `@event.listens_for(Session, 'do_orm_execute')` | — |
| `protect_discussion_history` | `(session, _flush_context, _instances)` | `@event.listens_for(Session, 'before_flush')` | — |

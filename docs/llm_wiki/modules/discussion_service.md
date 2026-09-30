# discussion_service Module

**Path:** `backend/app/services/discussion_service.py`

## Description

Owns bounded human discussion, validated mentions, subscriptions and personal inbox projections. Comment edits use their own versions and retained revision history, without changing task execution evidence or planning revisions. Writes recheck task scope after locking. Worker intents are idempotent per event/recipient and dispatch rechecks live access and preferences; suppression terminates without claiming delivery. Inbox reads and read-state changes remain personal and task-scoped.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `AuthorityError`, `internal_authority`, `require_project` |
| `app.commands` | `PlanningConflict`, `atomic_command` |
| `app.models.discussion` | `InboxNotification`, `TaskComment`, `TaskCommentRevision`, `TaskSubscription` |
| `app.models.identity` | `Principal`, `ProjectMembership`, `WorkspaceMembership` |
| `app.models.outbound_webhook` | `OutboundWebhookDelivery`, `OutboundWebhookEvent` |
| `app.models.task` | `Task` |
| `hashlib` | `sha256` |
| `sqlalchemy` | `or_`, `select`, `update` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/authority.py"]
    n1["backend/app/commands.py"]
    n2["backend/app/models/discussion.py"]
    n3["backend/app/models/identity.py"]
    n4["backend/app/models/outbound_webhook.py"]
    n5["backend/app/models/task.py"]
    n6["backend/app/routers/discussion.py"]
    n7["backend/app/services/discussion_service.py"]
    n8["backend/tests/test_task_discussion.py"]
    n0 --> n3
    n0 --> n5
    n1 --> n0
    n1 --> n5
    n1 --> n7
    n2 --> n5
    n6 --> n7
    n7 --> n0
    n7 --> n1
    n7 --> n2
    n7 --> n3
    n7 --> n4
    n7 --> n5
    n8 --> n0
    n8 --> n1
    n8 --> n2
    n8 --> n3
    n8 --> n4
    n8 --> n5
    n8 --> n7
    click n0 "../modules/authority.md"
    click n1 "../modules/commands.md"
    click n2 "../modules/models_discussion.md"
    click n3 "../modules/models_identity.md"
    click n4 "../modules/models_outbound_webhook.md"
    click n5 "../modules/models_task.md"
    click n6 "../modules/routers_discussion.md"
    click n7 "../modules/discussion_service.md"
    click n8 "../modules/test_task_discussion.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [commands](../modules/commands.md) |
| Inbound | [routers_discussion](../modules/routers_discussion.md) |
| Inbound | [test_task_discussion](../modules/test_task_discussion.md) |
| Outbound | [authority](../modules/authority.md) |
| Outbound | [commands](../modules/commands.md) |
| Outbound | [models_discussion](../modules/models_discussion.md) |
| Outbound | [models_identity](../modules/models_identity.md) |
| Outbound | [models_outbound_webhook](../modules/models_outbound_webhook.md) |
| Outbound | [models_task](../modules/models_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [DiscussionService](../entities/DiscussionService.md) | 19 | — | — |

# discussionService Module

**Path:** `frontend/src/services/discussionService.ts`

## Description

Typed browser client for comment revisions, mentions, subscriptions, personal inbox state and delivery retry. It carries expected comment/subscription versions and leaves task execution commands to the separate task service.

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `./api` | `api` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `CommentRevision`, `InboxItem`, `NotificationDelivery`, `Page`, `Subscription`, `TaskComment`, `discussionService` |
| Constants | `discussionService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/tasks/TaskDiscussion.tsx"]
    n1["frontend/src/pages/MyWorkPage.tsx"]
    n2["frontend/src/services/api.ts"]
    n3["frontend/src/services/discussionService.ts"]
    n0 --> n3
    n1 --> n2
    n1 --> n3
    n3 --> n2
    click n0 "../modules/TaskDiscussion.md"
    click n1 "../modules/MyWorkPage.md"
    click n2 "../modules/api.md"
    click n3 "../modules/discussionService.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TaskDiscussion](../modules/TaskDiscussion.md) |
| Inbound | [MyWorkPage](../modules/MyWorkPage.md) |
| Outbound | [api](../modules/api.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [TaskComment](../entities/discussionService_TaskComment.md) | Interface | 3 | — | — |
| [CommentRevision](../entities/CommentRevision.md) | Interface | 10 | — | — |
| [Subscription](../entities/Subscription.md) | Interface | 11 | — | — |
| [InboxItem](../entities/InboxItem.md) | Interface | 12 | — | — |
| [NotificationDelivery](../entities/NotificationDelivery.md) | Interface | 13 | — | — |
| [Page](../entities/Page.md) | Interface | 14 | — | — |
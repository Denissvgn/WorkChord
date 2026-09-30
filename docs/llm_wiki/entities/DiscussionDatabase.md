# DiscussionDatabase

**Location:** `backend/app/routers/discussion.py:14`
**Kind:** Type alias
**Bases:** —
**Module:** [routers_discussion](../modules/routers_discussion.md)
**Target:** `Annotated[AsyncSession, Depends(get_db, scope='function')]`

## Description

_Auto-generated from `DiscussionDatabase` in `backend/app/routers/discussion.py`._

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["DiscussionDatabase (backend/app/routers/discussion.py)"]
    n1["create_task_comment (backend/app/routers/discussion.py)"]
    n2["get_task_subscription (backend/app/routers/discussion.py)"]
    n3["list_task_comments (backend/app/routers/discussion.py)"]
    n4["mark_notification_read (backend/app/routers/discussion.py)"]
    n5["personal_inbox (backend/app/routers/discussion.py)"]
    n6["personal_notification_deliveries (backend/app/routers/discussion.py)"]
    n7["retry_personal_notification (backend/app/routers/discussion.py)"]
    n8["set_task_subscription (backend/app/routers/discussion.py)"]
    n9["task_comment_history (backend/app/routers/discussion.py)"]
    n10["task_mention_options (backend/app/routers/discussion.py)"]
    n11["update_task_comment (backend/app/routers/discussion.py)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    n10 --> n0
    n11 --> n0
    click n0 "../modules/routers_discussion.md"
    click n1 "../modules/routers_discussion.md"
    click n2 "../modules/routers_discussion.md"
    click n3 "../modules/routers_discussion.md"
    click n4 "../modules/routers_discussion.md"
    click n5 "../modules/routers_discussion.md"
    click n6 "../modules/routers_discussion.md"
    click n7 "../modules/routers_discussion.md"
    click n8 "../modules/routers_discussion.md"
    click n9 "../modules/routers_discussion.md"
    click n10 "../modules/routers_discussion.md"
    click n11 "../modules/routers_discussion.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [routers_discussion](../modules/routers_discussion.md) | 0 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `create_task_comment` | type_reference | [routers_discussion](../modules/routers_discussion.md) | — |
| `get_task_subscription` | type_reference | [routers_discussion](../modules/routers_discussion.md) | — |
| `list_task_comments` | type_reference | [routers_discussion](../modules/routers_discussion.md) | — |
| `mark_notification_read` | type_reference | [routers_discussion](../modules/routers_discussion.md) | — |
| `personal_inbox` | type_reference | [routers_discussion](../modules/routers_discussion.md) | — |
| `personal_notification_deliveries` | type_reference | [routers_discussion](../modules/routers_discussion.md) | — |
| `retry_personal_notification` | type_reference | [routers_discussion](../modules/routers_discussion.md) | — |
| `set_task_subscription` | type_reference | [routers_discussion](../modules/routers_discussion.md) | — |
| `task_comment_history` | type_reference | [routers_discussion](../modules/routers_discussion.md) | — |
| `task_mention_options` | type_reference | [routers_discussion](../modules/routers_discussion.md) | — |
| `update_task_comment` | type_reference | [routers_discussion](../modules/routers_discussion.md) | — |

# TaskComment

**Location:** `backend/app/models/discussion.py:12`
**Kind:** Class
**Bases:** `Base`
**Module:** [models_discussion](../modules/models_discussion.md)

## Description

Current comment projection with durable human authorship, an independent version and a removal marker. Its original task identity survives supported deletion and restoration; immutable revisions retain prior content.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `Mapped[int]` | `mapped_column(Integer, primary_key=True)` | — |
| `task_id` | `Mapped[int \| None]` | `mapped_column(ForeignKey('tasks.id', ondelete='SET NULL'), index=True)` | — |
| `original_task_id` | `Mapped[int]` | `mapped_column(Integer, nullable=False)` | — |
| `principal_id` | `Mapped[int]` | `mapped_column(ForeignKey('principals.id', ondelete='RESTRICT'))` | — |
| `body` | `Mapped[str]` | `mapped_column(Text, nullable=False)` | — |
| `mentions` | `Mapped[list]` | `mapped_column(JSON, nullable=False, default=list)` | — |
| `version` | `Mapped[int]` | `mapped_column(Integer, nullable=False, default=1)` | — |
| `deleted` | `Mapped[bool]` | `mapped_column(nullable=False, default=False)` | — |
| `created_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), nullable=False, default=utc_now)` | — |
| `updated_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), nullable=False, default=utc_now, onupdate=utc_now)` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskComment (backend/app/models/discussion.py)"]
    n1["Base (backend/app/database.py)"]
    n2["backend/app/models/__init__.py"]
    n3["DiscussionService.save (backend/app/services/discussion_service.py)"]
    n4["backend/tests/test_task_discussion.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/models_discussion.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/models___init__.md"
    click n3 "../modules/discussion_service.md"
    click n4 "../modules/test_task_discussion.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [models_discussion](../modules/models_discussion.md) | 0 | `body`, `created_at`, `deleted`, `id`, `mentions`, `original_task_id`, `principal_id`, `task_id`, `updated_at`, `version` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Base` | [app_database](../modules/app_database.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `DiscussionService.save` | call | [discussion_service](../modules/discussion_service.md) | 1 |
| `test_task_discussion` | import | [test_task_discussion](../modules/test_task_discussion.md) | — |

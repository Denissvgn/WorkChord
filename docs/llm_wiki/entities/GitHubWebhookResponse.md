# GitHubWebhookResponse

**Location:** `backend/app/schemas/github.py:72`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_github](../modules/schemas_github.md)

## Description

Response returned after receiving a GitHub webhook delivery.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `accepted` | `bool` | `accepted` | Yes | No | — | — | — | — |
| `event` | `str` | `event` | Yes | No | — | — | — | — |
| `action` | `Optional[str]` | `action` | No | Yes | `None` | — | — | — |
| `matched` | `bool` | `matched` | No | No | `False` | — | — | — |
| `external_link_id` | `Optional[int]` | `external_link_id` | No | Yes | `None` | — | — | — |
| `task_id` | `Optional[int]` | `task_id` | No | Yes | `None` | — | — | — |
| `triage_item_id` | `Optional[int]` | `triage_item_id` | No | Yes | `None` | — | — | — |
| `ignored_reason` | `Optional[str]` | `ignored_reason` | No | Yes | `None` | — | — | — |
| `automation_results` | `list[GitHubStatusAutomationResult]` | `automation_results` | No | No | factory: `list` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["GitHubWebhookResponse (backend/app/schemas/github.py)"]
    n1["BaseModel"]
    n2["receive_github_webhook (backend/app/routers/github.py)"]
    n3["backend/app/schemas/__init__.py"]
    n4["GitHubWebhookService.process (backend/app/services/github_webhook_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/schemas_github.md"
    click n2 "../modules/routers_github.md"
    click n3 "../modules/schemas___init__.md"
    click n4 "../modules/github_webhook_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_github](../modules/schemas_github.md) | 0 | `accepted`, `action`, `automation_results`, `event`, `external_link_id`, `ignored_reason`, `matched`, `task_id`, `triage_item_id` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `receive_github_webhook` | type_reference | [routers_github](../modules/routers_github.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `GitHubWebhookService.process` | call | [github_webhook_service](../modules/github_webhook_service.md) | 6 |
| `GitHubWebhookService.process` | type_reference | [github_webhook_service](../modules/github_webhook_service.md) | — |

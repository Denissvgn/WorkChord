# GitHubWebhookPayloadError

**Location:** `backend/app/services/github_webhook_service.py:47`
**Kind:** Class
**Bases:** `ValueError`
**Module:** [github_webhook_service](../modules/github_webhook_service.md)

## Description

Raised when a webhook payload cannot be processed.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["GitHubWebhookPayloadError (backend/app/services/github_webhook_service.py)"]
    n1["ValueError"]
    n2["backend/app/routers/github.py"]
    n3["GitHubWebhookService._pull_request (backend/app/services/github_webhook_service.py)"]
    n4["GitHubWebhookService._pull_request_number (backend/app/services/github_webhook_service.py)"]
    n5["GitHubWebhookService._repository_full_name (backend/app/services/github_webhook_service.py)"]
    n6["GitHubWebhookService.parse_payload (backend/app/services/github_webhook_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    click n0 "../modules/github_webhook_service.md"
    click n2 "../modules/routers_github.md"
    click n3 "../modules/github_webhook_service.md"
    click n4 "../modules/github_webhook_service.md"
    click n5 "../modules/github_webhook_service.md"
    click n6 "../modules/github_webhook_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [github_webhook_service](../modules/github_webhook_service.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `ValueError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `github` | import | [routers_github](../modules/routers_github.md) | — |
| `GitHubWebhookService._pull_request` | call | [github_webhook_service](../modules/github_webhook_service.md) | 1 |
| `GitHubWebhookService._pull_request_number` | call | [github_webhook_service](../modules/github_webhook_service.md) | 1 |
| `GitHubWebhookService._repository_full_name` | call | [github_webhook_service](../modules/github_webhook_service.md) | 2 |
| `GitHubWebhookService.parse_payload` | call | [github_webhook_service](../modules/github_webhook_service.md) | 2 |

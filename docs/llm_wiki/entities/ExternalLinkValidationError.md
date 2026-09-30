# ExternalLinkValidationError

**Location:** `backend/app/services/external_link_service.py:25`
**Kind:** Class
**Bases:** `ValueError`
**Module:** [external_link_service](../modules/external_link_service.md)

## Description

Raised when a provider-specific link cannot be parsed.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ExternalLinkValidationError (backend/app/services/external_link_service.py)"]
    n1["ValueError"]
    n2["backend/app/routers/tasks.py"]
    n3["ExternalLinkService.parse_github_url (backend/app/services/external_link_service.py)"]
    n4["GitHubStatusService._pr_metadata (backend/app/services/github_status_service.py)"]
    n5["GitHubStatusService.refresh_pull_request_status (backend/app/services/github_status_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/external_link_service.md"
    click n2 "../modules/tasks.md"
    click n3 "../modules/external_link_service.md"
    click n4 "../modules/github_status_service.md"
    click n5 "../modules/github_status_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [external_link_service](../modules/external_link_service.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `ValueError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `tasks` | import | [tasks](../modules/tasks.md) | — |
| `ExternalLinkService.parse_github_url` | call | [external_link_service](../modules/external_link_service.md) | 4 |
| `GitHubStatusService._pr_metadata` | call | [github_status_service](../modules/github_status_service.md) | 2 |
| `GitHubStatusService.refresh_pull_request_status` | call | [github_status_service](../modules/github_status_service.md) | 1 |

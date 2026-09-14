# github_status_service Module

**Path:** `backend/app/services/github_status_service.py`

## Description

GitHub pull request status refresh service.

## Imports

| Source | Symbols |
|--------|---------|
| `app.config` | `get_settings` |
| `app.models.external_link` | `ExternalLink`, `ExternalLinkEntityType` |
| `app.services.external_link_service` | `ExternalLinkService`, `ExternalLinkValidationError` |
| `app.services.task_context_revision_service` | `reserve_task_context_revision` |
| `app.utils.url_policy` | `normalize_provider_api_url` |
| `datetime` | `datetime`, `timezone` |
| `httpx` | `httpx` |
| `logging` | `logging` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |
| `typing` | `Any`, `Optional` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/config.py"]
    n1["backend/app/models/external_link.py"]
    n2["backend/app/routers/tasks.py"]
    n3["backend/app/services/external_link_service.py"]
    n4["backend/app/services/github_status_service.py"]
    n5["backend/app/services/github_webhook_service.py"]
    n6["backend/app/services/task_context_revision_service.py"]
    n7["backend/app/utils/url_policy.py"]
    n2 --> n3
    n2 --> n4
    n3 --> n1
    n3 --> n6
    n4 --> n0
    n4 --> n1
    n4 --> n3
    n4 --> n6
    n4 --> n7
    n5 --> n0
    n5 --> n1
    n5 --> n4
    n5 --> n6
    n7 --> n0
    click n0 "../modules/config.md"
    click n1 "../modules/models_external_link.md"
    click n2 "../modules/tasks.md"
    click n3 "../modules/external_link_service.md"
    click n4 "../modules/github_status_service.md"
    click n5 "../modules/github_webhook_service.md"
    click n6 "../modules/task_context_revision_service.md"
    click n7 "../modules/url_policy.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [tasks](../modules/tasks.md) |
| Inbound | [github_webhook_service](../modules/github_webhook_service.md) |
| Outbound | [config](../modules/config.md) |
| Outbound | [models_external_link](../modules/models_external_link.md) |
| Outbound | [external_link_service](../modules/external_link_service.md) |
| Outbound | [task_context_revision_service](../modules/task_context_revision_service.md) |
| Outbound | [url_policy](../modules/url_policy.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [GitHubStatusService](../entities/GitHubStatusService.md) | 22 | — | Refresh cached GitHub pull request metadata for external links. |

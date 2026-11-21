# github_status_service Module

**Path:** `backend/app/services/github_status_service.py`

## Description

GitHub pull request status refresh service.

Candidate verification reads a pull request’s current head or compares an immutable base and head in the submitted repository. Every commit in the bounded range must have attributable evidence. Incomplete pagination, an unexpected head or unattributed contributors prevent a passing candidate observation.

## Imports

| Source | Symbols |
|--------|---------|
| `app.commands` | `commit_or_flush` |
| `app.config` | `get_settings` |
| `app.models.external_link` | `ExternalLink`, `ExternalLinkEntityType` |
| `app.services.external_link_service` | `ExternalLinkService`, `ExternalLinkValidationError` |
| `app.services.system_settings_service` | `RuntimeSettingsService` |
| `app.services.task_context_revision_service` | `reserve_task_context_revision` |
| `app.utils.url_policy` | `normalize_provider_api_url` |
| `datetime` | `datetime`, `timezone` |
| `httpx` | `httpx` |
| `logging` | `logging` |
| `re` | `re` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |
| `typing` | `Any`, `Optional` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/app/services/github_status_service.py"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/github_status_service.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (7) |
| Outbound | `backend` (7) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 0 |

> All 14 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [GitHubStatusService](../entities/GitHubStatusService.md) | 25 | — | Refresh cached GitHub pull request metadata for external links. |

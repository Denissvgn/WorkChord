# github_reconciliation_service Module

**Path:** `backend/app/services/github_reconciliation_service.py`

## Description

Reconcile what a task submitted with what GitHub currently shows for its pull requests.

The read model compares the commit each run submitted with the observed head,
checks, merge or unmerged closure, and the review state, and names who acts
next. Catch-up refreshes the task's own pull request links from GitHub for
events a deployment never received. Observing a merge never accepts or closes a
task: acceptance stays with the independent reviewer's verdict.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `require_project` |
| `app.models.agent` | `AgentRun`, `AgentTaskAssignment` |
| `app.models.external_link` | `ExternalLink`, `ExternalLinkEntityType` |
| `app.models.task` | `Task` |
| `app.query_limits` | `MAX_BOUNDED_LIST_ITEMS` |
| `app.services.github_status_service` | `GitHubStatusService`, `parse_github_time` |
| `app.services.task_replacement_service` | `relation_for` |
| `app.utils.github_links` | `GitHubLinkError`, `parse_github_url` |
| `sqlalchemy` | `select` |
| `typing` | `Any`, `Optional` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/app/services/github_reconciliation_service.py"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/github_reconciliation_service.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (7) |
| Outbound | `backend` (8) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

> All 14 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [GitHubReconciliationService](../entities/GitHubReconciliationService.md) | 71 | — | Read and catch up the GitHub reconciliation of one task. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_sha` | `(url: Optional[str]) -> Optional[str]` | — | — |
| `_pull_key` | `(url: Optional[str]) -> Optional[str]` | — | — |
| `pull_state` | `(link: ExternalLink) -> str` | — | open, draft, merged, closed_unmerged, or unobserved. |
| `observed_head_keeps_acceptance` | *(async)* `(db, link: ExternalLink, head_sha: Optional[str]) -> bool` | — | Whether recording an observed pull request head may carry the task's acceptance. |

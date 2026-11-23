# GitHubStatusService

**Location:** `backend/app/services/github_status_service.py:25`
**Kind:** Class
**Bases:** —
**Module:** [github_status_service](../modules/github_status_service.md)

## Description

Refresh cached GitHub pull request metadata for external links.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(db: AsyncSession, settings_override = None, transport: Optional[httpx.AsyncBaseTransport] = None)` | — | — |
| `from_runtime` | *(async)* `(db: AsyncSession, transport: Optional[httpx.AsyncBaseTransport] = None) -> 'GitHubStatusService'` | `@classmethod` | Construct the service from DB-backed runtime GitHub settings. |
| `_now_iso` | `() -> str` | — | Return an API-friendly UTC timestamp. |
| `_headers` | `() -> dict[str, str]` | — | Build GitHub request headers. |
| `_pr_metadata` | `(link: ExternalLink) -> tuple[str, str, int]` | — | Extract GitHub PR identity from external link metadata. |
| `status_from_payload` | `(payload: dict[str, Any]) -> str` | — | Normalize GitHub PR state into the external link status field. |
| `_fetch_pull_request` | *(async)* `(owner: str, repo: str, number: int) -> dict[str, Any]` | — | Fetch one pull request payload from GitHub. |
| `_fetch_pr_resource` | *(async)* `(owner, repo, number, suffix = '')` | — | — |
| `_fetch_resource` | *(async)* `(url)` | — | — |
| `_check_review_commits` | `(commits, count, expected_sha, attributed_commits, failure_context = None)` | `@staticmethod` | — |
| `verify_review_range` | *(async)* `(base, head, attributed_commits, *, failure_context = None)` | — | Verify every commit after the submitted immutable base. |
| `verify_review_head` | *(async)* `(pr, expected_sha, attributed_commits, *, expected_repository = None, failure_context = None)` | — | Observe the exact PR candidate and flag additional, unbound authors. |
| `_provider_error_message` | `(error: Exception) -> str` | — | Convert provider exceptions into a safe cached message. |
| `_save_link` | *(async)* `(link: ExternalLink) -> ExternalLink` | — | Persist changed link fields. |
| `_reserve_task_context_revision` | *(async)* `(link: ExternalLink, *, outcome: str) -> None` | — | Fence a task assignment before provider data dirties its linked context. |
| `refresh_pull_request_status` | *(async)* `(link_id: int) -> Optional[ExternalLink]` | — | Refresh a GitHub PR link and cache status metadata. |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["GitHubStatusService (backend/app/services/github_status_service.py)"]
    n1["get_github_status_service (backend/app/routers/tasks.py)"]
    n2["refresh_github_external_link (backend/app/routers/tasks.py)"]
    n3["GitHubStatusService.from_runtime (backend/app/services/github_status_service.py)"]
    n4["GitHubWebhookService.__init__ (backend/app/services/github_webhook_service.py)"]
    n5["backend/app/services/review_provenance.py"]
    n6["backend/tests/test_manual_review_provenance.py"]
    n7["test_commit_only_review_verifies_the_entire_pinned_range (backend/tests/test_review_provenance.py)"]
    n8["test_github_candidate_uses_full_head_and_contributions (backend/tests/test_review_provenance.py)"]
    n9["backend/tests/test_review_provenance_transports.py"]
    n10["backend/tests/test_scoped_review_evidence.py"]
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
    click n0 "../modules/github_status_service.md"
    click n1 "../modules/tasks.md"
    click n2 "../modules/tasks.md"
    click n3 "../modules/github_status_service.md"
    click n4 "../modules/github_webhook_service.md"
    click n5 "../modules/review_provenance.md"
    click n6 "../modules/test_manual_review_provenance.md"
    click n7 "../modules/test_review_provenance.md"
    click n8 "../modules/test_review_provenance.md"
    click n9 "../modules/test_review_provenance_transports.md"
    click n10 "../modules/test_scoped_review_evidence.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [github_status_service](../modules/github_status_service.md) | 16 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `get_github_status_service` | type_reference | [tasks](../modules/tasks.md) | — |
| `refresh_github_external_link` | type_reference | [tasks](../modules/tasks.md) | — |
| `GitHubStatusService.from_runtime` | call | [github_status_service](../modules/github_status_service.md) | 1 |
| `GitHubStatusService.from_runtime` | type_reference | [github_status_service](../modules/github_status_service.md) | — |
| `GitHubWebhookService.__init__` | call | [github_webhook_service](../modules/github_webhook_service.md) | 1 |
| `review_provenance` | import | [review_provenance](../modules/review_provenance.md) | — |
| `test_manual_review_provenance` | import | [test_manual_review_provenance](../modules/test_manual_review_provenance.md) | — |
| `test_commit_only_review_verifies_the_entire_pinned_range` | call | [test_review_provenance](../modules/test_review_provenance.md) | 1 |
| `test_github_candidate_uses_full_head_and_contributions` | call | [test_review_provenance](../modules/test_review_provenance.md) | 1 |
| `test_review_provenance_transports` | import | [test_review_provenance_transports](../modules/test_review_provenance_transports.md) | — |
| `test_scoped_review_evidence` | import | [test_scoped_review_evidence](../modules/test_scoped_review_evidence.md) | — |

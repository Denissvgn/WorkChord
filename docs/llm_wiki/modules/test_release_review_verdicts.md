# test_release_review_verdicts Module

**Path:** `backend/tests/test_release_review_verdicts.py`

## Description

A release counts the current independent decisions on its linked work.

## Imports

| Source | Symbols |
|--------|---------|
| `app.main` | `app` |
| `app.models.agent` | `AgentTaskAssignment`, `TaskEvent`, `AgentIdempotencyRecord` |
| `app.models.identity` | `Principal` |
| `app.models.project` | `Project` |
| `app.models.release` | `Release` |
| `app.models.task_brief` | `TaskReviewRecord` |
| `app.models.team_member` | `TeamMemberProfile` |
| `app.services.agent_routing_policy` | `ROUTING_DECISION_AUTHORITY` |
| `app.services.agent_service` | `hash_api_key` |
| `app.services.identity_service` | `IdentityService` |
| `app.services.release_service` | `ReleaseService` |
| `app.services.task_context_revision_service` | `reserve_task_context_revision` |
| `app.utils.time` | `utc_now` |
| `httpx` | `httpx` |
| `json` | `json` |
| `pytest` | `pytest` |
| `secrets` | `secrets` |
| `tests.test_review_provenance_transports` | `databases` |
| `tests.test_scoped_review_evidence` | `through` |
| `tests.test_team_pm_dispatch` | `db_session_factory` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/test_release_review_verdicts.py"]
    n1 --> n0
    click n1 "../modules/test_release_review_verdicts.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `backend` (16) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 1 |

> All 16 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `test_release_counts_independent_verdict` | *(async)* `(db_session, db_session_factory, task_factory, actor_factory, profile_factory, monkeypatch, transport)` | `@databases`, `@pytest.mark.parametrize('transport', ['rest', 'mcp'])` | — |
| `test_older_acceptance_needs_an_assigned_verdict_receipt` | *(async)* `(db_session, task_factory, actor_factory)` | — | — |

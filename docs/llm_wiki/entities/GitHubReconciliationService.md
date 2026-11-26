# GitHubReconciliationService

**Location:** `backend/app/services/github_reconciliation_service.py:71`
**Kind:** Class
**Bases:** —
**Module:** [github_reconciliation_service](../modules/github_reconciliation_service.md)

## Description

Read and catch up the GitHub reconciliation of one task.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(db)` | — | — |
| `_task` | *(async)* `(task_id: int, action: str) -> Task` | — | — |
| `_pull_links` | *(async)* `(task_id: int) -> list[ExternalLink]` | — | — |
| `catch_up` | *(async)* `(task_id: int) -> dict[str, Any]` | — | Refresh this task's pull request links from GitHub, then return the reconciliation. |
| `view` | *(async)* `(task_id: int) -> dict[str, Any]` | — | — |
| `_submissions` | `(link, runs, reviews, only_link)` | — | — |
| `_pull` | `(task, link, runs, reviews, accepted, replaced, relation, link_count = 1)` | — | — |
| `_next` | `(state, meta, checks_state, submitted, head_differs, accepted, replaced, relation, reviews)` | `@staticmethod` | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["GitHubReconciliationService (backend/app/services/github_reconciliation_service.py)"]
    n1["get_github_reconciliation (backend/app/mcp_agent_tools.py)"]
    n2["run_github_catch_up (backend/app/mcp_agent_tools.py)"]
    n3["task_github_catch_up (backend/app/routers/task_domain.py)"]
    n4["task_github_reconciliation (backend/app/routers/task_domain.py)"]
    n5["DeliveryDependencyService._merge_evidence (backend/app/services/delivery_dependency_service.py)"]
    n6["observed_head_keeps_acceptance (backend/app/services/github_reconciliation_service.py)"]
    n7["record_merge (backend/tests/test_delivery_merge_prerequisites.py)"]
    n8["test_a_head_pushed_after_acceptance_makes_acceptance_stale (backend/tests/test_delivery_merge_prerequisites.py)"]
    n9["test_a_recorded_provider_error_keeps_acceptance (backend/tests/test_delivery_merge_prerequisites.py)"]
    n10["test_an_observed_merge_keeps_acceptance_and_releases_the_dependent (backend/tests/test_delivery_merge_prerequisites.py)"]
    n11["test_a_closure_seen_by_catch_up_and_then_delivered_stays_one_entry (backend/tests/test_github_reconciliation.py)"]
    n12["test_a_never_observed_link_shows_its_submission_and_asks_for_catch_up (backend/tests/test_github_reconciliation.py)"]
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
    n12 --> n0
    click n0 "../modules/github_reconciliation_service.md"
    click n1 "../modules/mcp_agent_tools.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/routers_task_domain.md"
    click n4 "../modules/routers_task_domain.md"
    click n5 "../modules/delivery_dependency_service.md"
    click n6 "../modules/github_reconciliation_service.md"
    click n7 "../modules/test_delivery_merge_prerequisites.md"
    click n8 "../modules/test_delivery_merge_prerequisites.md"
    click n9 "../modules/test_delivery_merge_prerequisites.md"
    click n10 "../modules/test_delivery_merge_prerequisites.md"
    click n11 "../modules/test_github_reconciliation.md"
    click n12 "../modules/test_github_reconciliation.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [github_reconciliation_service](../modules/github_reconciliation_service.md) | 8 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `get_github_reconciliation` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 1 |
| `run_github_catch_up` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 1 |
| `task_github_catch_up` | call | [routers_task_domain](../modules/routers_task_domain.md) | 1 |
| `task_github_reconciliation` | call | [routers_task_domain](../modules/routers_task_domain.md) | 1 |
| `DeliveryDependencyService._merge_evidence` | call | [delivery_dependency_service](../modules/delivery_dependency_service.md) | 1 |
| `observed_head_keeps_acceptance` | call | [github_reconciliation_service](../modules/github_reconciliation_service.md) | 1 |
| `record_merge` | call | [test_delivery_merge_prerequisites](../modules/test_delivery_merge_prerequisites.md) | 1 |
| `test_a_head_pushed_after_acceptance_makes_acceptance_stale` | call | [test_delivery_merge_prerequisites](../modules/test_delivery_merge_prerequisites.md) | 1 |
| `test_a_recorded_provider_error_keeps_acceptance` | call | [test_delivery_merge_prerequisites](../modules/test_delivery_merge_prerequisites.md) | 1 |
| `test_an_observed_merge_keeps_acceptance_and_releases_the_dependent` | call | [test_delivery_merge_prerequisites](../modules/test_delivery_merge_prerequisites.md) | 1 |
| `test_a_closure_seen_by_catch_up_and_then_delivered_stays_one_entry` | call | [test_github_reconciliation](../modules/test_github_reconciliation.md) | 1 |
| `test_a_never_observed_link_shows_its_submission_and_asks_for_catch_up` | call | [test_github_reconciliation](../modules/test_github_reconciliation.md) | 1 |

> References: showing 12 of 21 logical references; 9 omitted by the 12-row generated summary limit.

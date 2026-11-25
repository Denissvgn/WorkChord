# test_github_reconciliation Module

**Path:** `backend/tests/test_github_reconciliation.py`

## Description

A task's submitted commit is reconciled with its linked pull request as GitHub shows it now.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `Authority`, `AuthorityError` |
| `app.config` | `get_settings` |
| `app.models.agent` | `AgentRun`, `AgentTaskAssignment`, `TaskEvent` |
| `app.models.external_link` | `ExternalLink` |
| `app.models.iteration` | `Iteration` |
| `app.models.project` | `Project` |
| `app.models.task_replacement` | `TaskReplacement` |
| `app.services.external_link_service` | `ExternalLinkService` |
| `app.services.github_reconciliation_service` | `GitHubReconciliationService` |
| `app.services.github_status_service` | `GitHubStatusService` |
| `app.services.github_webhook_service` | `GitHubWebhookService` |
| `httpx` | `httpx` |
| `pytest` | `pytest` |
| `sqlalchemy` | `select` |
| `types` | `SimpleNamespace` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/authority.py"]
    n1["backend/app/config.py"]
    n2["backend/app/models/agent.py"]
    n3["backend/app/models/external_link.py"]
    n4["backend/app/models/iteration.py"]
    n5["backend/app/models/project.py"]
    n6["backend/app/models/task_replacement.py"]
    n7["backend/app/services/external_link_service.py"]
    n8["backend/app/services/github_reconciliation_service.py"]
    n9["backend/app/services/github_status_service.py"]
    n10["backend/app/services/github_webhook_service.py"]
    n11["backend/tests/test_github_reconciliation.py"]
    n0 --> n1
    n0 --> n2
    n0 --> n5
    n2 --> n5
    n4 --> n5
    n5 --> n2
    n5 --> n4
    n7 --> n0
    n7 --> n3
    n8 --> n0
    n8 --> n2
    n8 --> n3
    n8 --> n9
    n9 --> n1
    n9 --> n2
    n9 --> n3
    n9 --> n7
    n10 --> n1
    n10 --> n2
    n10 --> n3
    n10 --> n9
    n11 --> n0
    n11 --> n1
    n11 --> n2
    n11 --> n3
    n11 --> n4
    n11 --> n5
    n11 --> n6
    n11 --> n7
    n11 --> n8
    n11 --> n9
    n11 --> n10
    click n0 "../modules/authority.md"
    click n1 "../modules/config.md"
    click n2 "../modules/models_agent.md"
    click n3 "../modules/models_external_link.md"
    click n4 "../modules/models_iteration.md"
    click n5 "../modules/models_project.md"
    click n6 "../modules/models_task_replacement.md"
    click n7 "../modules/external_link_service.md"
    click n8 "../modules/github_reconciliation_service.md"
    click n9 "../modules/github_status_service.md"
    click n10 "../modules/github_webhook_service.md"
    click n11 "../modules/test_github_reconciliation.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [authority](../modules/authority.md) |
| Outbound | [config](../modules/config.md) |
| Outbound | [models_agent](../modules/models_agent.md) |
| Outbound | [models_external_link](../modules/models_external_link.md) |
| Outbound | [models_iteration](../modules/models_iteration.md) |
| Outbound | [models_project](../modules/models_project.md) |
| Outbound | [models_task_replacement](../modules/models_task_replacement.md) |
| Outbound | [external_link_service](../modules/external_link_service.md) |
| Outbound | [github_reconciliation_service](../modules/github_reconciliation_service.md) |
| Outbound | [github_status_service](../modules/github_status_service.md) |
| Outbound | [github_webhook_service](../modules/github_webhook_service.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 3 | 1 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [FakeGitHub](../entities/FakeGitHub.md) | 28 | — | A mutable pull request behind a mock transport; records every request. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `github` | `(monkeypatch)` | `@pytest.fixture` | — |
| `_project` | *(async)* `(db)` | — | — |
| `_delivery` | *(async)* `(db, task_factory, actor_factory, project, *, submitted = SHA_A, pr_url = PR_URL, number = 39)` | — | A task whose run submitted a commit for a pull request linked to it. |
| `_as` | `(db, project, role = 'manager')` | — | — |
| `_events` | *(async)* `(db, task_id, event_type)` | — | — |
| `test_a_never_observed_link_shows_its_submission_and_asks_for_catch_up` | *(async)* `(db_session, task_factory, actor_factory)` | — | — |
| `test_catch_up_shows_an_advanced_head_with_checks_on_that_head` | *(async)* `(db_session, task_factory, actor_factory, github)` | — | — |
| `test_failing_and_pending_checks_name_the_worker_or_reviewer` | *(async)* `(db_session, task_factory, actor_factory, github)` | — | — |
| `test_an_external_merge_is_recorded_once_and_never_accepts_the_task` | *(async)* `(db_session, task_factory, actor_factory, github)` | — | — |
| `test_an_unmerged_closure_is_a_pm_decision` | *(async)* `(db_session, task_factory, actor_factory, github)` | — | — |
| `_webhook` | `(db, secret = 's')` | — | — |
| `_delivery_payload` | `(action, pull)` | — | — |
| `test_duplicate_and_out_of_order_deliveries_leave_the_newest_state` | *(async)* `(db_session, task_factory, actor_factory, github)` | — | — |
| `test_catch_up_recovers_a_merge_whose_event_was_missed_and_keeps_older_review_on_its_commit` | *(async)* `(db_session, task_factory, actor_factory, github)` | — | — |
| `test_catch_up_never_reads_a_link_outside_the_callers_teams` | *(async)* `(db_session, task_factory, actor_factory, github)` | — | — |
| `test_a_viewer_reads_the_reconciliation_but_cannot_trigger_catch_up` | *(async)* `(db_session, task_factory, actor_factory, github)` | — | — |
| `test_a_replaced_task_points_at_its_successor_and_its_own_pull_request` | *(async)* `(db_session, task_factory, actor_factory, github)` | — | — |
| `test_checks_read_for_an_older_head_are_not_reported_for_the_new_head` | *(async)* `(db_session, task_factory, actor_factory, github, old_checks, old_owner)` | `@pytest.mark.parametrize('old_checks, old_owner', [('failure', 'worker'), ('success', 'pm')])` | — |

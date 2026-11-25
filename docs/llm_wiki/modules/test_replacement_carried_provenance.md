# test_replacement_carried_provenance Module

**Path:** `backend/tests/test_replacement_carried_provenance.py`

## Description

A replacement's carried contributors stay out of independent review, and their history walk is bounded.

## Imports

| Source | Symbols |
|--------|---------|
| `app.config` | `get_settings` |
| `app.models.agent` | `AgentActor`, `AgentRun`, `AgentTaskAssignment` |
| `app.models.iteration` | `Iteration` |
| `app.models.project` | `Project` |
| `app.models.task` | `Task` |
| `app.models.task_replacement` | `TaskReplacement` |
| `app.services` | `review_provenance` |
| `app.services.agent_routing_service` | `AgentRoutingConflictError` |
| `app.services.review_provenance` | `carried_profile_history`, `require_independent_profile` |
| `app.services.task_replacement_service` | `carried_contributors` |
| `app.utils.time` | `utc_now` |
| `copy` | `deepcopy` |
| `pytest` | `pytest` |
| `tests` | `test_agent_team_setup_qualification` |
| `tests.test_agent_routing_wave6_qualification` | `_assessment_command` |
| `tests.test_review_provenance_transports` | `databases`, `fence` |
| `tests.test_scoped_review_evidence` | `through` |
| `tests.test_task_replacement` | `BASE`, `_replacement`, `_scenario` |
| `tests.test_team_pm_dispatch` | `db_session_factory` |
| `tests.test_team_pm_recovery` | `recovery_api` |
| `types` | `SimpleNamespace` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/test_replacement_carried_provenance.py"]
    n1 --> n0
    click n1 "../modules/test_replacement_carried_provenance.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `backend` (17) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 1 |

> All 17 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `restore_settings_cache` | `()` | `@pytest.fixture(autouse=True)` | — |
| `_with_second_verifier` | `(payload)` | — | The standard topology plus one more automation verifier with its own profile and runtime. |
| `_use_two_verifiers` | `(monkeypatch)` | — | Provision the usual topology with a second verifier inside the same topology. |
| `row_for` | `(preview, actor_id)` | — | — |
| `_carry_run` | *(async)* `(db, author, original, replacement, unattributed)` | — | The original's carried run belongs to ``author``, whose profile its authenticated begin recorded. |
| `_submit_replacement` | *(async)* `(transport, db_session_factory, monkeypatch, team, member, replacement_id, version)` | — | The worker executes and submits the replacement, so it is resolved and ready for verification. |
| `test_routing_preview_excludes_a_carried_contributor_without_the_strict_policy` | *(async)* `(db_session, db_session_factory, task_factory, team_member_factory, monkeypatch, transport)` | `@databases`, `@pytest.mark.parametrize('transport', ['rest', 'mcp'])`, `@pytest.mark.usefixtures('deployed_agent_skill_release')` | — |
| `test_verification_reassignment_refuses_a_carried_contributor` | *(async)* `(db_session, db_session_factory, task_factory, team_member_factory, monkeypatch, transport)` | `@databases`, `@pytest.mark.parametrize('transport', ['rest', 'mcp'])`, `@pytest.mark.usefixtures('deployed_agent_skill_release')` | — |
| `_linked_chain` | *(async)* `(db, length, *, cycle = False)` | — | Replacement links t0 -> t1 -> ... -> t<length>, each carrying one run id; a cycle closes the chain. |
| `test_carried_history_walk_is_bounded_and_fails_closed` | *(async)* `(db_session, db_session_factory, monkeypatch, case)` | `@databases`, `@pytest.mark.parametrize('case', ['depth', 'runs', 'cycle'])` | — |

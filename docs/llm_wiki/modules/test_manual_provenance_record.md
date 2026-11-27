# test_manual_provenance_record Module

**Path:** `backend/tests/test_manual_provenance_record.py`

## Description

Recorded provenance lets work resolved outside recorded runs receive an ordinary independent review.

## Imports

| Source | Symbols |
|--------|---------|
| `app` | `database`, `mcp_server` |
| `app.authority` | `Authority`, `AuthorityError` |
| `app.commands` | `PlanningConflict` |
| `app.config` | `get_settings` |
| `app.main` | `app` |
| `app.models.agent` | `AgentActor`, `AgentModelBinding`, `AgentModelCatalogEntry`, `AgentRun`, `AgentTaskAssignment`, `TaskEvent` |
| `app.models.identity` | `CommandAudit`, `IdentitySubject`, `Principal`, `PrincipalProfileLink`, `ProjectMembership`, `WorkspaceMembership` |
| `app.models.iteration` | `Iteration` |
| `app.models.project` | `Project` |
| `app.models.task` | `Task` |
| `app.models.team_member` | `TeamMemberProfile` |
| `app.models.user_session` | `UserSession` |
| `app.schemas.agent` | `AgentTaskAssignmentCreate` |
| `app.schemas.manual_provenance` | `ManualProvenanceWrite` |
| `app.services.agent_routing_service` | `AgentRoutingConflictError` |
| `app.services.agent_work_service` | `AgentWorkService` |
| `app.services.github_status_service` | `GitHubStatusService` |
| `app.services.identity_service` | `IdentityService`, `digest`, `initialize_control_plane` |
| `app.services.manual_provenance_service` | `ManualProvenanceService` |
| `app.services.review_provenance` | `require_verifiable_candidate`, `review_history` |
| `app.utils.time` | `utc_now` |
| `contextlib` | `nullcontext` |
| `datetime` | `timedelta` |
| `httpx` | `httpx` |
| `json` | `json` |
| `pytest` | `pytest` |
| `sqlalchemy` | `select`, `update` |
| `tests.test_agent_routing_service` | `_rollout`, `_routing_fixture` |
| `tests.test_agent_team_setup_qualification` | `provision_ready_topology`, `routing_base` |
| `tests.test_delivery_scenarios` | `delivery_store` |
| `tests.test_review_provenance_transports` | `databases` |
| `tests.test_team_pm_dispatch` | `db_session_factory` |
| `types` | `SimpleNamespace` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/test_manual_provenance_record.py"]
    n1 --> n0
    click n1 "../modules/test_manual_provenance_record.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `backend` (27) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 3 | 1 |

> All 27 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [AgentProtocol](../entities/AgentProtocol.md) | 72 | — | Call agent commands over REST or MCP with the planning command headers. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `provenance_body` | `(task, executor, **changes)` | — | — |
| `mock_github` | `(monkeypatch, commits, head = HEAD)` | — | Serve one pull request whose head and commits the test controls, as the verdict check reads them. |
| `plain_commits` | `(*shas)` | — | — |
| `test_recorded_provenance_allows_an_independent_review_of_work_merged_outside_runs` | *(async)* `(db_session, db_session_factory, task_factory, team_member_factory, profile_factory, monkeypatch, recorder, transport, executor_kind, publishers)` | `@databases`, `@pytest.mark.parametrize(('recorder', 'transport', 'executor_kind', 'publishers'), [('human', 'rest', 'agent', 'distinct'), ('human', 'rest', 'human', 'distinct'), ('pm', 'mcp', 'agent', 'distinct'), ('pm', 'rest', 'agent', 'distinct'), ('human', 'rest', 'agent', 'executor_is_reviewer'), ('human', 'rest', 'agent', 'status_route'), ('pm', 'rest', 'agent', 'recorder_is_reviewer'), ('pm', 'rest', 'agent', 'recorder_unknown'), ('pm', 'rest', 'human', 'distinct')])`, `@pytest.mark.usefixtures('deployed_agent_skill_release')` | — |
| `test_no_verification_assignment_for_a_known_unverifiable_candidate` | *(async)* `(db_session, actor_factory, profile_factory, team_member_factory, task_factory)` | `@pytest.mark.asyncio`, `@databases` | — |
| `test_a_candidate_less_refusal_names_only_a_remedy_that_can_help` | `()` | `@pytest.mark.sqlite` | — |
| `provenance_scope` | *(async)* `(factory, scenario)` | — | — |
| `write` | `(task, executor_id, **changes)` | — | — |
| `task_state` | *(async)* `(factory, task_id)` | — | — |
| `agent_executor` | *(async)* `(factory, *, publisher = 'executor-model-maker', enabled = True, key = 'executor-model', project_id = None)` | — | An agent actor with a profile and one binding whose catalog entry declares the publisher. |
| `test_only_an_accountable_owner_or_pm_may_record` | *(async)* `(delivery_store, authority)` | `@pytest.mark.parametrize('authority', [lambda pid, principal: Authority(None, 'local', local=True), lambda pid, principal: Authority(principal, 'system', workspace_role='operator', review_override=True, reason=REASON), lambda pid, principal: Authority(principal, 'agent', actor_id=1, actor_role='worker', projects={pid: 'manager'}, scopes=frozenset({'planning:read', 'planning:write'})), lambda pid, principal: Authority(principal, 'human', workspace_role='owner', read_only=True), lambda pid, principal: Authority(principal, 'human', workspace_role='member', projects={pid: 'reviewer'})], ids=['trusted-local', 'operator-key', 'worker-agent', 'observer', 'project-reviewer'])` | — |
| `test_a_pm_agent_cannot_attest_a_human_executor` | *(async)* `(delivery_store)` | — | — |
| `test_record_refuses_unresolved_stale_executed_and_unattributable_work` | *(async)* `(delivery_store, monkeypatch)` | — | — |
| `test_a_record_cannot_contradict_the_recorded_executor` | *(async)* `(delivery_store, monkeypatch)` | — | — |
| `test_record_refuses_a_candidate_the_verdict_could_never_pass` | *(async)* `(delivery_store, monkeypatch, commits, head, sha, gap)` | `@pytest.mark.parametrize(('commits', 'head', 'sha', 'gap'), [(plain_commits(FIRST, UNLISTED, HEAD), HEAD, UNLISTED, 'commit_attribution'), (plain_commits(FIRST) + [{'sha': HEAD, 'commit': {'message': 'Change\n\nCo-authored-by: Pair <pair@example.test>'}}], HEAD, HEAD, 'coauthor_trailer'), (plain_commits(FIRST, HEAD), UNLISTED, None, 'head_mismatch')], ids=['unlisted-commit', 'coauthor-trailer', 'different-head'])` | — |
| `test_recorded_contribution_survives_rework_and_accepts_a_retired_binding` | *(async)* `(delivery_store, monkeypatch)` | — | — |
| `test_a_stale_human_record_points_at_a_fresh_record` | *(async)* `(delivery_store, monkeypatch)` | — | — |
| `test_record_refuses_once_review_could_no_longer_read_every_record` | *(async)* `(delivery_store, monkeypatch)` | — | — |
| `test_an_agent_recorder_counts_under_every_enabled_binding` | *(async)* `(delivery_store, monkeypatch)` | — | — |
| `test_record_reports_unreadable_or_missing_github_answers_as_unverifiable` | *(async)* `(delivery_store, monkeypatch, answer, wording)` | `@pytest.mark.parametrize(('answer', 'wording'), [(httpx.Response(200, json=['not', 'an', 'object']), 'does not describe'), (httpx.Response(200, json={'head': 'not-an-object', 'commits': 2}), 'does not describe'), (httpx.Response(404, json={'message': 'Not Found'}), 'repository access')], ids=['non-object', 'malformed-object', 'not-found'])` | — |
| `test_record_refuses_an_executor_from_another_project` | *(async)* `(delivery_store, monkeypatch)` | — | — |

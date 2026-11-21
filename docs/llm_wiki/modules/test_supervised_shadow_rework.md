# test_supervised_shadow_rework Module

**Path:** `backend/tests/test_supervised_shadow_rework.py`

## Description

A prior supervised worker resumes the exact strict handback on its original publisher.

## Imports

| Source | Symbols |
|--------|---------|
| `app.config` | `get_settings` |
| `app.main` | `app` |
| `app.models.agent` | `AgentActor`, `AgentIdempotencyRecord`, `AgentModelBinding`, `AgentModelCatalogEntry`, `AgentRun`, `AgentTaskAssignment`, `AgentTeamTopology`, `AgentTeamTopologyMember`, `TaskEvent` |
| `app.models.identity` | `ProjectMembership`, `WorkspaceMembership` |
| `app.models.iteration` | `Iteration` |
| `app.models.project` | `Project` |
| `app.models.task` | `Task` |
| `app.models.team_member` | `TeamMember` |
| `app.schemas.agent_team_setup` | `AgentTeamMaster` |
| `app.services` | `agent_work_service`, `review_provenance` |
| `app.services.agent_team_setup_service` | `AgentTeamSetupService` |
| `app.services.identity_service` | `IdentityService`, `initialize_control_plane` |
| `copy` | `deepcopy` |
| `httpx` | `httpx` |
| `json` | `json` |
| `pytest` | `pytest` |
| `sqlalchemy` | `event`, `func`, `inspect`, `select`, `text`, `update` |
| `sqlalchemy.exc` | `DBAPIError` |
| `tests.test_agent_routing_service` | `_assessment_command` |
| `tests.test_agent_team_setup` | `CapturingCredentialSink` |
| `tests.test_agent_team_setup_qualification` | `ReadyTopology`, `acknowledge_all`, `apply_manifest`, `provision_ready_topology`, `routing_base`, `seed_model_catalog`, `topology_actors`, `topology_payload` |
| `tests.test_review_provenance_transports` | `databases`, `fence` |
| `tests.test_team_pm_dispatch` | `db_session_factory` |
| `tests.test_team_pm_recovery` | `recovery_api` |
| `unittest.mock` | `patch` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/test_supervised_shadow_rework.py"]
    n1 --> n0
    click n1 "../modules/test_supervised_shadow_rework.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `backend` (19) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 3 | 1 |

> All 19 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `stored_history` | *(async)* `(factory, rework_id, verdict_id, source_id)` | — | — |
| `topology_with_two_reviewers` | *(async)* `(db)` | — | — |
| `control_plane_writes` | `(project_id, capacity_id, manager, worker, reviewer, earlier_actor, binding, topology_id)` | — | — |
| `assert_postgresql_locks` | *(async)* `(factory, writes)` | — | — |
| `assert_floor_preview` | *(async)* `(task_id, task_version, pm_key, reviewer, alternate_verifier)` | — | — |
| `assert_lookup_indexes` | `(session)` | — | — |
| `test_authenticated_shadow_handback` | *(async)* `(db_session, db_session_factory, task_factory, team_member_factory, monkeypatch, transport, case, record_property)` | `@databases`, `@pytest.mark.parametrize('transport', ['rest', 'mcp'])`, `@pytest.mark.parametrize('case', ['same_worker', 'alternate_worker', 'cross_team', 'changed_binding', 'missing_verdict', 'missing_submit', 'wrong_rework_event', 'model_escalation', 'binding_changed_before_begin', 'off_after_rejection', 'enforced_after_rejection', 'verifier_disabled', 'verifier_rebound', 'worker_membership_lost', 'verifier_membership_lost', 'task_changed_before_begin', 'previous_canceled_run', 'identity_revision_during_begin', 'identity_publisher_during_begin', 'failed_recovery', 'canceled_recovery', 'two_items', 'recovered_submitter', 'older_contributor', 'missing_recovery_receipt', 'wrong_recovery_event', 'wrong_submitted_version', 'wrong_issued_version', 'legacy_verdict_selection', 'legacy_verdict_wrong_candidate', 'policy_changed_before_begin'])`, `@pytest.mark.usefixtures('deployed_agent_skill_release')` | — |

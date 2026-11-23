# review_evidence Module

**Path:** `backend/app/services/review_evidence.py`

## Description

Operator-attested review material. The receipt never grants access to a host or runs a command.

An independent workspace operator attests the exact submitted candidate, current assessment, reviewer binding and packet. The recorded issuer must retain operator authority and remain independent of the contributors and reviewer through assignment and verdict. Explicit revocation and expiry end the receipt's validity.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `AuthorityError`, `internal_authority`, `require_operator` |
| `app.commands` | `command_transaction`, `current_command` |
| `app.config` | `get_settings` |
| `app.models.agent` | `AgentActor`, `AgentModelBinding`, `AgentModelCatalogEntry`, `AgentTaskAssignment`, `TaskEvent`, `TaskRoutingAssessment` |
| `app.models.identity` | `Principal`, `PrincipalProfileLink`, `WorkspaceAuthorityState`, `WorkspaceMembership` |
| `app.query_limits` | `MAX_BOUNDED_LIST_ITEMS`, `CollectionLimitExceededError` |
| `app.schemas.agent_planning` | `AgentPlanningCommandContext` |
| `app.schemas.agent_routing` | `AgentRoutingPreviewCreate` |
| `app.schemas.review_evidence` | `ReviewEvidenceCommand`, `ReviewEvidenceIssue` |
| `app.services.agent_routing_policy` | `ROUTING_POLICY_VERSION`, `evaluate_model_envelope` |
| `app.services.agent_routing_service` | `AgentRoutingConflictError`, `AgentRoutingService`, `AgentRoutingService` |
| `app.services.agent_service` | `actor_has_scope`, `is_admin_key_principal` |
| `app.services.review_provenance` | `actor_provenance`, `digest`, `select_reviewer` |
| `app.utils.time` | `as_utc`, `utc_now` |
| `datetime` | `datetime`, `timedelta` |
| `json` | `json` |
| `pydantic` | `TypeAdapter` |
| `sqlalchemy` | `select` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/app/services/review_evidence.py"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/services_review_evidence.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (6) |
| Outbound | `backend` (14) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 0 |

> All 18 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_conflict` | `(message, **details)` | — | — |
| `_event` | *(async)* `(db, task_id, evidence_id)` | — | — |
| `_revocation_id` | *(async)* `(db, task_id, evidence_id)` | — | — |
| `history_digest` | `(contributors, manual_execution)` | — | — |
| `_issuer_identity` | *(async)* `(db, principal_id, actor_id, reviewer, contributors, manual)` | — | Read the issuing principal's current authority and attributable identities inside the server. |
| `assignment_observation` | `(task, assignments, assignment_id, scope, candidate)` | — | Validate the existing review owner before fresh-dispatch capacity is evaluated. |
| `resolve` | *(async)* `(db, task, evidence_id, history, *, reviewer = None)` | — | Recheck expiry, revocation and immutable source/binding identity at each consuming boundary. |
| `requirements_for` | `(assessment, scope, actor_id, binding_id)` | — | Use an exact review packet in place of host-shell only for its named verification binding. |
| `_check_model` | *(async)* `(db, task, reviewer, expected_assessment, method, tests)` | — | — |
| `check_supervised_selection` | *(async)* `(db, task, principal, selection, reviewer_profile_id)` | — | Supervised dispatch must also produce a positive live route for an evidence-backed verifier. |
| `record_review_evidence` | *(async)* `(db, actor, task_id, payload, *, idempotency_key, rationale, correlation_id)` | — | — |
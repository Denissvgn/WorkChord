# attest_review_evidence

**Entry point:** `attest_review_evidence` (`http`)
**Source:** [agent_catalog](../modules/agent_catalog.md)
**Modules touched:** [agent_catalog](../modules/agent_catalog.md), [agent_routing_policy](../modules/agent_routing_policy.md), [agent_routing_service](../modules/agent_routing_service.md), and 25 more

**Complete modules touched:**

- [agent_catalog](../modules/agent_catalog.md)
- [agent_routing_policy](../modules/agent_routing_policy.md)
- [agent_routing_service](../modules/agent_routing_service.md)
- [agent_service](../modules/agent_service.md)
- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [config](../modules/config.md)
- [delivery_dependency_service](../modules/delivery_dependency_service.md)
- [discussion_service](../modules/discussion_service.md)
- [github_links](../modules/github_links.md)
- [identity_service](../modules/identity_service.md)
- [manual_provenance_service](../modules/manual_provenance_service.md)
- [models_agent](../modules/models_agent.md)
- [models_outbound_webhook](../modules/models_outbound_webhook.md)
- [mutation_versions](../modules/mutation_versions.md)
- [query_limits](../modules/query_limits.md)
- [refusal_next_steps](../modules/refusal_next_steps.md)
- [retained_planning_output](../modules/retained_planning_output.md)
- [review_provenance](../modules/review_provenance.md)
- [routers_agent_planning](../modules/routers_agent_planning.md)
- [schemas_agent_planning](../modules/schemas_agent_planning.md)
- [services_review_evidence](../modules/services_review_evidence.md)
- [task_brief_service](../modules/task_brief_service.md)
- [task_reactivation_service](../modules/task_reactivation_service.md)
- [task_replacement_service](../modules/task_replacement_service.md)
- [task_service](../modules/task_service.md)
- [time](../modules/time.md)
- [url_policy](../modules/url_policy.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as attest_review_evidence
    participant p1 as record_review_evidence
    participant p2 as _handle_agent_error
    participant p3 as require_operator
    participant p4 as actor_has_scope
    participant p5 as digest
    participant p6 as command_transaction
    participant p7 as AgentRoutingService._lock_task
    participant p8 as _conflict (backend/app/services/review_evidence.py)
    participant p9 as select_reviewer
    participant p10 as _conflict (backend/app/services/review_provenance.py)
    participant p11 as AgentRoutingService.lock_selection_inputs
    participant p12 as different_publisher_required
    participant p13 as canonical_routing_json_bytes
    participant p14 as review_history
    participant p15 as process_reactivation_checks
    participant p16 as actor_provenance
    participant p17 as DeliveryDependencyService.reconcile
    participant p18 as _carries_unattributed_run
    participant p19 as DiscussionService.enqueue
    participant p20 as _publisher_step
    participant p21 as resolve
    participant p22 as next_step_for
    participant p23 as _attempt_history
    participant p24 as _event
    participant p25 as _validate_json_native
    participant p26 as carried_contributors
    participant p27 as ReactivationService.evaluate_waiting
    participant p28 as history_digest
    participant p29 as isinstance (backend/app/routers/agent…ng.py:_handle_agent_error)
    participant p30 as TypeAdapter(…).validate_python
    p0->>p1: record_review_evidence
    p0->>p2: _handle_agent_error
    p1->>p3: require_operator
    p1->>p4: actor_has_scope
    p1->>p5: digest
    p1->>p6: command_transaction
    p1->>p7: AgentRoutingService._lock_task
    p1->>p8: _conflict (backend/app/services/review_evidence.py)
    p1->>p9: select_reviewer
    p9->>p10: _conflict (backend/app/services/review_provenance.py)
    p7->>p11: AgentRoutingService.lock_selection_inputs
    p9->>p12: different_publisher_required
    p5->>p13: canonical_routing_json_bytes
    p9->>p14: review_history
    p6->>p15: process_reactivation_checks
    p9->>p16: actor_provenance
    p6->>p17: DeliveryDependencyService.reconcile
    p9->>p18: _carries_unattributed_run
    p6->>p19: DiscussionService.enqueue
    p9->>p20: _publisher_step
    p9->>p21: resolve
    p10->>p22: next_step_for
    p14->>p23: _attempt_history
    p21->>p24: _event
    p13->>p25: _validate_json_native
    p14->>p26: carried_contributors
    p15->>p27: ReactivationService.evaluate_waiting
    p21->>p28: history_digest
    p2-->>p29: isinstance (backend/app/routers/agent…ng.py:_handle_agent_error)(exc, AgentPermissionError)
    p1-->>p30: TypeAdapter(…).validate_python(payload)
```

> Call sequence diagram shows 30 of 811 interactions; 781 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 1 of 210 (209 omitted); unresolved 1 of 370 (369 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/authority.py:require_operator` | 3 | - | unresolved | 1 |
| `backend/app/authority.py:require_operator` | 3 | [backend/app/authority.py](../modules/authority.md) | internal | 1 |
| `backend/app/services/review_evidence.py:record_review_evidence` | 2 | [backend/app/services/agent_service.py](../modules/agent_service.md) | internal | 1 |
| `backend/app/services/agent_service.py:actor_has_scope` | 7 | [backend/app/services/agent_service.py](../modules/agent_service.md) | internal | 1 |
| `backend/app/services/agent_service.py:actor_scopes` | 8 | - | external | 2 |
| `backend/app/services/review_evidence.py:record_review_evidence` | 2 | [backend/app/authority.py](../modules/authority.md) | internal | 1 |
| `backend/app/services/review_evidence.py:record_review_evidence` | 2 | - | external | 12 |
| `backend/app/services/review_evidence.py:record_review_evidence` | 2 | [backend/app/schemas/agent_planning.py](../modules/schemas_agent_planning.md) | internal | 1 |
> Omission summary shows 8 of 178 groups; 170 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 232; effect analysis evaluated: 178, partial: 6, unavailable: 48. Counts include steps omitted from the displayed trace.

Collector observations for 184 source steps with known totals: observed: 1027, emitted: 994, omitted: 33. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector omitted observations before flow assembly; displayed effects are partial.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `attest_review_evidence` | `available` | `evaluated` | `available` | `6` | `6` | `0` |
| `record_review_evidence` | `available` | `partial` | `available` | `23` | `18` | `5` |
| `require_operator` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `db.info.get (backend/app/authority.py:require_operator)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `AuthorityError` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `is_admin_key_principal` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `actor_has_scope` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `actor_scopes` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `json.loads (backend/app/services/agent_service.py:actor_scopes)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `isinstance (backend/app/services/agent_service.py:actor_scopes)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `AuthorityError` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `TypeAdapter(…).validate_python` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. attest_review_evidence"]
    s2["2. record_review_evidence"]
    s3["3. require_operator"]
    s4["4. db.info.get (backend/app/authority.py:require_operator)"]
    s5["5. AuthorityError"]
    s6["6. is_admin_key_principal"]
    s7["7. actor_has_scope"]
    s8["8. actor_scopes"]
    s9["9. json.loads (backend/app/services/agent_service.py:actor_scopes)"]
    s10["10. isinstance (backend/app/services/agent_service.py:actor_scopes)"]
    s11["11. AuthorityError"]
    s12["12. TypeAdapter(…).validate_python"]
    s1 -->|"record_review_evidence(db, actor, task_id, data, idempotency_key=command.idempotency_key, rationale=command.rationale, correlation_id=command.correlation_id)"| s2
    s2 -->|"require_operator(db)"| s3
    s3 -. "db.info.get (backend/app/authority.py:require_operator)('authority')" .-> s4
    s3 -->|"AuthorityError('operator_required', 'Workspace operator permission is required.')"| s5
    s2 -->|"is_admin_key_principal(actor)"| s6
    s2 -->|"actor_has_scope(actor, 'admin')"| s7
    s7 -->|"actor_scopes(actor)"| s8
    s8 -. "json.loads (backend/app/services/agent_service.py:actor_scopes)(actor.scopes)" .-> s9
    s8 -. "isinstance (backend/app/services/agent_service.py:actor_scopes)(scopes, list)" .-> s10
    s2 -->|"AuthorityError('operator_required', 'The authenticated workspace operator must attest review evidence.')"| s11
    s2 -. "TypeAdapter(…).validate_python(payload)" .-> s12
    b0["mutation db.add"]
    s2 -. "mutation db.add" .-> b0
    click s1 "../modules/agent_catalog.md"
    click s2 "../modules/services_review_evidence.md"
    click s3 "../modules/authority.md"
    click s5 "../modules/authority.md"
    click s6 "../modules/agent_service.md"
    click s7 "../modules/agent_service.md"
    click s8 "../modules/agent_service.md"
    click s11 "../modules/authority.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `attest_review_evidence` | `task_id: int`, `data: ReviewEvidenceCommand`, `actor: Annotated[AgentActor, Depends(get_model_catalog_principal)]`, `db: Annotated[AsyncSession, Depends(get_db, scope='function')]`, `command: Annotated[AgentPlanningCommandContext, Depends(get_agent_planning_command_context)]` | - | - | `...` |
| `record_review_evidence` | `db`, `actor`, `task_id`, `payload`, `idempotency_key`, `rationale`, `correlation_id` | `ReviewEvidenceIssue`, `ISSUED`, `REVOKED`, `TaskEvent`, `TaskEvent`, `TaskEvent`, `TaskEvent`, `TaskEvent` | - | `{...}`, `{...}` |
| `require_operator` | `db` | - | - | - |
| `db.info.get (backend/app/authority.py:require_operator)` | - | - | - | - |
| `AuthorityError` | - | - | - | - |
| `is_admin_key_principal` | `actor: AgentActor` | `ADMIN_KEY_PRINCIPAL_NAME` | - | `...` |
| `actor_has_scope` | `actor: AgentActor`, `scope: str` | - | - | `...` |
| `actor_scopes` | `actor: AgentActor` | `json` | - | `...` |
| `json.loads (backend/app/services/agent_service.py:actor_scopes)` | - | - | - | - |
| `isinstance (backend/app/services/agent_service.py:actor_scopes)` | - | - | - | - |
| `AuthorityError` | - | - | - | - |
| `TypeAdapter(…).validate_python` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| attest_review_evidence | record_review_evidence | 92 | `record_review_evidence(db, actor, task_id, data, idempotency_key=command.idempotency_key, rationale=command.rationale, correlation_id=command.correlation_id)` |
| record_review_evidence | require_operator | 325 | `require_operator(db)` |
| require_operator | db.info.get (backend/app/authority.py:require_operator) | 92 | `db.info.get('authority')` |
| require_operator | AuthorityError | 94 | `AuthorityError('operator_required', 'Workspace operator permission is required.')` |
| record_review_evidence | is_admin_key_principal | 328 | `is_admin_key_principal(actor)` |
| record_review_evidence | actor_has_scope | 332 | `actor_has_scope(actor, 'admin')` |
| actor_has_scope | actor_scopes | 95 | `actor_scopes(actor)` |
| actor_scopes | json.loads (backend/app/services/agent_service.py:actor_scopes) | 87 | `json.loads(actor.scopes)` |
| actor_scopes | isinstance (backend/app/services/agent_service.py:actor_scopes) | 90 | `isinstance(scopes, list)` |
| record_review_evidence | AuthorityError | 334 | `AuthorityError('operator_required', 'The authenticated workspace operator must attest review evidence.')` |
| record_review_evidence | TypeAdapter(…).validate_python | 338 | `TypeAdapter(ReviewEvidenceCommand).validate_python(payload)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `db.add` | `record_review_evidence` | 457 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `require_operator` | `db.info.get` | 92 |
| external_call | `actor_scopes` | `json.loads` | 87 |
| external_call | `actor_scopes` | `isinstance` | 90 |
| unresolved_call | `record_review_evidence` | `TypeAdapter(ReviewEvidenceCommand).validate_python` | 338 |
| step_limit | `attest_review_evidence` | `first 12 steps` | 0 |
| truncated_flow | `attest_review_evidence` | `depth limit` | 0 |

## Behavior

This flow starts at `attest_review_evidence` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

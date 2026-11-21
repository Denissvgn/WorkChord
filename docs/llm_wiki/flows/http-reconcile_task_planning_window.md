# reconcile_task_planning_window

**Entry point:** `reconcile_task_planning_window` (`http`)
**Source:** [agent_catalog](../modules/agent_catalog.md)
**Modules touched:** [agent_catalog](../modules/agent_catalog.md), [agent_model_catalog_service](../modules/agent_model_catalog_service.md), [agent_planning_service](../modules/agent_planning_service.md), and 27 more

**Complete modules touched:**

- [agent_catalog](../modules/agent_catalog.md)
- [agent_model_catalog_service](../modules/agent_model_catalog_service.md)
- [agent_planning_service](../modules/agent_planning_service.md)
- [agent_routing_policy](../modules/agent_routing_policy.md)
- [agent_routing_service](../modules/agent_routing_service.md)
- [agent_service](../modules/agent_service.md)
- [agent_team_setup](../modules/agent_team_setup.md)
- [agent_team_setup_service](../modules/agent_team_setup_service.md)
- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [config](../modules/config.md)
- [delivery_dependency_service](../modules/delivery_dependency_service.md)
- [discussion_service](../modules/discussion_service.md)
- [execution_planning_window](../modules/execution_planning_window.md)
- [execution_reconciliation](../modules/execution_reconciliation.md)
- [identity_service](../modules/identity_service.md)
- [models_agent](../modules/models_agent.md)
- [models_identity](../modules/models_identity.md)
- [models_outbound_webhook](../modules/models_outbound_webhook.md)
- [mutation_versions](../modules/mutation_versions.md)
- [planning_window_reconciliation](../modules/planning_window_reconciliation.md)
- [query_limits](../modules/query_limits.md)
- [review_provenance](../modules/review_provenance.md)
- [routers_agent_planning](../modules/routers_agent_planning.md)
- [schemas_agent_planning](../modules/schemas_agent_planning.md)
- [snapshot_service](../modules/snapshot_service.md)
- [task_brief_service](../modules/task_brief_service.md)
- [task_hierarchy_service](../modules/task_hierarchy_service.md)
- [task_service](../modules/task_service.md)
- [time](../modules/time.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as reconcile_task_planning_window
    participant p1 as reconcile_window
    participant p2 as _handle_model_error
    participant p3 as require_operator
    participant p4 as actor_has_scope
    participant p5 as command_transaction
    participant p6 as source_receipt_id
    participant p7 as TaskService.get_by_id
    participant p8 as _planning_proof
    participant p9 as original_ownership
    participant p10 as make_window
    participant p11 as seal_authority
    participant p12 as assignment_context
    participant p13 as authority_stamp
    participant p14 as TaskService._load_iteration_tree
    participant p15 as task_context
    participant p16 as DeliveryDependencyService.reconcile
    participant p17 as DiscussionService.enqueue
    participant p18 as SnapshotService._task_to_export
    participant p19 as actor_provenance
    participant p20 as _snapshot_task
    participant p21 as TaskHierarchyService._load_iteration_tree
    participant p22 as DeliveryDependencyService.validate_cycles
    participant p23 as _canonical_snapshot_checksum
    participant p24 as AgentRoutingService._profile_revision
    participant p25 as DiscussionService.recipient_authorized
    participant p26 as TaskService.reserve_task_version
    participant p27 as clear_execution_evidence
    participant p28 as _digest
    participant p29 as HTTPException (backend/app/routers/agent…cile_task_planning_window)
    participant p30 as exc.detail (backend/app/routers/agent…og.py:_handle_model_error)
    p0->>p1: reconcile_window
    p0->>p2: _handle_model_error
    p1->>p3: require_operator
    p1->>p4: actor_has_scope
    p1->>p5: command_transaction
    p1->>p6: source_receipt_id
    p1->>p7: TaskService.get_by_id
    p1->>p8: _planning_proof
    p1->>p9: original_ownership
    p1->>p10: make_window
    p1->>p11: seal_authority
    p10->>p12: assignment_context
    p11->>p13: authority_stamp
    p7->>p14: TaskService._load_iteration_tree
    p10->>p15: task_context
    p5->>p16: DeliveryDependencyService.reconcile
    p5->>p17: DiscussionService.enqueue
    p8->>p18: SnapshotService._task_to_export
    p9->>p19: actor_provenance
    p8->>p20: _snapshot_task
    p14->>p21: TaskHierarchyService._load_iteration_tree
    p16->>p22: DeliveryDependencyService.validate_cycles
    p20->>p23: _canonical_snapshot_checksum
    p19->>p24: AgentRoutingService._profile_revision
    p17->>p25: DiscussionService.recipient_authorized
    p16->>p26: TaskService.reserve_task_version
    p16->>p27: clear_execution_evidence
    p13->>p28: _digest
    p0-->>p29: HTTPException (backend/app/routers/agent…cile_task_planning_window)(status_code=422, detail=str(...))
    p2-->>p30: exc.detail (backend/app/routers/agent…og.py:_handle_model_error)
```

> Call sequence diagram shows 30 of 721 interactions; 691 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 1 of 233 (232 omitted); unresolved 1 of 368 (367 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/authority.py:require_operator` | 3 | - | unresolved | 1 |
| `backend/app/authority.py:require_operator` | 3 | [backend/app/authority.py](../modules/authority.md) | internal | 1 |
| `backend/app/services/planning_window_reconciliation.py:reconcile_window` | 2 | [backend/app/services/agent_service.py](../modules/agent_service.md) | internal | 1 |
| `backend/app/services/agent_service.py:actor_has_scope` | 7 | [backend/app/services/agent_service.py](../modules/agent_service.md) | internal | 1 |
| `backend/app/services/agent_service.py:actor_scopes` | 8 | - | external | 2 |
| `backend/app/services/planning_window_reconciliation.py:reconcile_window` | 2 | [backend/app/authority.py](../modules/authority.md) | internal | 1 |
| `backend/app/services/planning_window_reconciliation.py:reconcile_window` | 2 | [backend/app/schemas/agent_planning.py](../modules/schemas_agent_planning.md) | internal | 1 |
| `backend/app/services/planning_window_reconciliation.py:reconcile_window` | 2 | - | external | 19 |
> Omission summary shows 8 of 148 groups; 140 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 121; effect analysis evaluated: 81, partial: 9, unavailable: 31. Counts include steps omitted from the displayed trace.

Collector observations for 90 source steps with known totals: observed: 546, emitted: 483, omitted: 63. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector omitted observations before flow assembly; displayed effects are partial.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `reconcile_task_planning_window` | `available` | `partial` | `available` | `13` | `10` | `3` |
| `reconcile_window` | `available` | `partial` | `available` | `27` | `24` | `3` |
| `require_operator` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `db.info.get (backend/app/authority.py:require_operator)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `AuthorityError` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `is_admin_key_principal` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `actor_has_scope` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `actor_scopes` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `json.loads (backend/app/services/agent_service.py:actor_scopes)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `isinstance (backend/app/services/agent_service.py:actor_scopes)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `AuthorityError` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `AgentPlanningCommandContext` | `unavailable` | `unavailable` | `unavailable` | — | — | — |

```mermaid
flowchart LR
    s1["1. reconcile_task_planning_window"]
    s2["2. reconcile_window"]
    s3["3. require_operator"]
    s4["4. db.info.get (backend/app/authority.py:require_operator)"]
    s5["5. AuthorityError"]
    s6["6. is_admin_key_principal"]
    s7["7. actor_has_scope"]
    s8["8. actor_scopes"]
    s9["9. json.loads (backend/app/services/agent_service.py:actor_scopes)"]
    s10["10. isinstance (backend/app/services/agent_service.py:actor_scopes)"]
    s11["11. AuthorityError"]
    s12["12. AgentPlanningCommandContext"]
    s1 -->|"reconcile_window(…)"| s2
    s2 -->|"require_operator(db)"| s3
    s3 -. "db.info.get (backend/app/authority.py:require_operator)('authority')" .-> s4
    s3 -->|"AuthorityError('operator_required', 'Workspace operator permission is required.')"| s5
    s2 -->|"is_admin_key_principal(actor)"| s6
    s2 -->|"actor_has_scope(actor, 'admin')"| s7
    s7 -->|"actor_scopes(actor)"| s8
    s8 -. "json.loads (backend/app/services/agent_service.py:actor_scopes)(actor.scopes)" .-> s9
    s8 -. "isinstance (backend/app/services/agent_service.py:actor_scopes)(scopes, list)" .-> s10
    s2 -->|"AuthorityError('operator_required', 'An authenticated workspace operator is required.')"| s11
    s2 -->|"AgentPlanningCommandContext(idempotency_key=idempotency_key, rationale=rationale, correlation_id=correlation_id)"| s12
    b0["mutation db.add"]
    s2 -. "mutation db.add" .-> b0
    b1["mutation result.update"]
    s2 -. "mutation result.update" .-> b1
    b2["mutation db.add"]
    s2 -. "mutation db.add" .-> b2
    click s1 "../modules/agent_catalog.md"
    click s2 "../modules/planning_window_reconciliation.md"
    click s3 "../modules/authority.md"
    click s5 "../modules/authority.md"
    click s6 "../modules/agent_service.md"
    click s7 "../modules/agent_service.md"
    click s8 "../modules/agent_service.md"
    click s11 "../modules/authority.md"
    click s12 "../modules/schemas_agent_planning.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `reconcile_task_planning_window` | `task_id: int`, `actor: Annotated[AgentActor, Depends(get_model_catalog_principal)]`, `db: Annotated[AsyncSession, Depends(get_db, scope='function')]`, `planning_receipt_id: Annotated[int \| None, Query(gt=0)]`, `planning_actor_id: Annotated[int \| None, Query(gt=0)]`, `planning_command_key: Annotated[str \| None, Query(min_length=1, max_length=255)]`, `apply: bool`, `expected_evidence_digest: Annotated[str \| None, Query(pattern='^[a-f0-9]{64}$')]` | `AgentModelConflictError` | - | `...` |
| `reconcile_window` | `db`, `actor`, `task_id`, `receipt_id`, `planning_actor_id`, `planning_command_key`, `apply`, `expected_evidence_digest` | `Task`, `Task`, `Iteration`, `CommandAudit`, `ACTION`, `CommandAudit`, `ACTION`, `ACTION` | `result[...]`, `task.execution_planning_window` | `previous.details[...]`, `result`, `result` |
| `require_operator` | `db` | - | - | - |
| `db.info.get (backend/app/authority.py:require_operator)` | - | - | - | - |
| `AuthorityError` | - | - | - | - |
| `is_admin_key_principal` | `actor: AgentActor` | `ADMIN_KEY_PRINCIPAL_NAME` | - | `...` |
| `actor_has_scope` | `actor: AgentActor`, `scope: str` | - | - | `...` |
| `actor_scopes` | `actor: AgentActor` | `json` | - | `...` |
| `json.loads (backend/app/services/agent_service.py:actor_scopes)` | - | - | - | - |
| `isinstance (backend/app/services/agent_service.py:actor_scopes)` | - | - | - | - |
| `AuthorityError` | - | - | - | - |
| `AgentPlanningCommandContext` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| reconcile_task_planning_window | reconcile_window | 112 | `reconcile_window(db, actor, task_id, planning_receipt_id, apply=apply, planning_actor_id=planning_actor_id, planning_command_key=planning_command_key, expected_evidence_digest=expected_evidence_digest, idempotency_key=idempotency_key, rationale=rationale, correlation_id=correlation_id)` |
| reconcile_window | require_operator | 312 | `require_operator(db)` |
| require_operator | db.info.get (backend/app/authority.py:require_operator) | 84 | `db.info.get('authority')` |
| require_operator | AuthorityError | 86 | `AuthorityError('operator_required', 'Workspace operator permission is required.')` |
| reconcile_window | is_admin_key_principal | 318 | `is_admin_key_principal(actor)` |
| reconcile_window | actor_has_scope | 322 | `actor_has_scope(actor, 'admin')` |
| actor_has_scope | actor_scopes | 95 | `actor_scopes(actor)` |
| actor_scopes | json.loads (backend/app/services/agent_service.py:actor_scopes) | 87 | `json.loads(actor.scopes)` |
| actor_scopes | isinstance (backend/app/services/agent_service.py:actor_scopes) | 90 | `isinstance(scopes, list)` |
| reconcile_window | AuthorityError | 325 | `AuthorityError('operator_required', 'An authenticated workspace operator is required.')` |
| reconcile_window | AgentPlanningCommandContext | 328 | `AgentPlanningCommandContext(idempotency_key=idempotency_key, rationale=rationale, correlation_id=correlation_id)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `db.add` | `reconcile_window` | 449 |
| mutation | `result.update` | `reconcile_window` | 451 |
| mutation | `db.add` | `reconcile_window` | 452 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `require_operator` | `db.info.get` | 84 |
| external_call | `actor_scopes` | `json.loads` | 87 |
| external_call | `actor_scopes` | `isinstance` | 90 |
| step_limit | `reconcile_task_planning_window` | `first 12 steps` | 0 |
| truncated_flow | `reconcile_task_planning_window` | `depth limit` | 0 |

## Behavior

This flow starts at `reconcile_task_planning_window` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

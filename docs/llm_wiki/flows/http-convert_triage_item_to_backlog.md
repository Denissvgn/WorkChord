# convert_triage_item_to_backlog

**Entry point:** `convert_triage_item_to_backlog` (`http`)
**Source:** [routers_triage](../modules/routers_triage.md)
**Modules touched:** [authority](../modules/authority.md), [commands](../modules/commands.md), [config](../modules/config.md), [delivery_dependency_service](../modules/delivery_dependency_service.md), and 11 more

**Complete modules touched:**

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [config](../modules/config.md)
- [delivery_dependency_service](../modules/delivery_dependency_service.md)
- [discussion_service](../modules/discussion_service.md)
- [identity_service](../modules/identity_service.md)
- [models_outbound_webhook](../modules/models_outbound_webhook.md)
- [mutation_versions](../modules/mutation_versions.md)
- [routers_task_domain](../modules/routers_task_domain.md)
- [routers_triage](../modules/routers_triage.md)
- [schemas_triage](../modules/schemas_triage.md)
- [source_link_policy](../modules/source_link_policy.md)
- [task_brief_service](../modules/task_brief_service.md)
- [task_service](../modules/task_service.md)
- [url_policy](../modules/url_policy.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as convert_triage_item_to_backlog
    participant p1 as command_transaction
    participant p2 as TriageSourceLinkOutcome.for_link
    participant p3 as domain_result
    participant p4 as TriageConvertToTaskResponse
    participant p5 as evaluate_source_link
    participant p6 as DeliveryDependencyService.reconcile
    participant p7 as DiscussionService.enqueue
    participant p8 as _instance_authorities
    participant p9 as DeliveryDependencyService.validate_cycles
    participant p10 as normalize_stored_display_url
    participant p11 as DiscussionService.recipient_authorized
    participant p12 as TaskService.reserve_task_version
    participant p13 as clear_execution_evidence
    participant p14 as DeliveryDependencyService.graph
    participant p15 as normalize_external_http_url
    participant p16 as lock_iterations
    participant p17 as IdentityService.context
    participant p18 as lock_planning
    participant p19 as require_mutation_revision
    participant p20 as validate_public_host
    participant p21 as current_command
    participant p22 as TriageSourceLinkOutcome
    participant p23 as CommandState
    participant p24 as DeliveryDependencyService
    participant p25 as DiscussionService
    participant p26 as internal_authority
    participant p27 as SourceLinkDecision
    participant p28 as _is_instance_path
    participant p29 as HTTPException (backend/app/routers/triag…rt_triage_item_to_backlog)
    participant p30 as service.convert_to_task
    p0->>p1: command_transaction
    p0->>p2: TriageSourceLinkOutcome.for_link
    p0->>p3: domain_result
    p0->>p4: TriageConvertToTaskResponse
    p2->>p5: evaluate_source_link
    p1->>p6: DeliveryDependencyService.reconcile
    p1->>p7: DiscussionService.enqueue
    p5->>p8: _instance_authorities
    p6->>p9: DeliveryDependencyService.validate_cycles
    p5->>p10: normalize_stored_display_url
    p7->>p11: DiscussionService.recipient_authorized
    p6->>p12: TaskService.reserve_task_version
    p6->>p13: clear_execution_evidence
    p9->>p14: DeliveryDependencyService.graph
    p10->>p15: normalize_external_http_url
    p12->>p16: lock_iterations
    p11->>p17: IdentityService.context
    p16->>p18: lock_planning
    p16->>p19: require_mutation_revision
    p15->>p20: validate_public_host
    p1->>p21: current_command
    p2->>p22: TriageSourceLinkOutcome
    p1->>p23: CommandState
    p1->>p24: DeliveryDependencyService
    p1->>p25: DiscussionService
    p7->>p26: internal_authority
    p5->>p27: SourceLinkDecision
    p5->>p28: _is_instance_path
    p0-->>p29: HTTPException (backend/app/routers/triag…rt_triage_item_to_backlog)(409, detail=str(...))
    p0-->>p30: service.convert_to_task(triage_item_id, data)
```

> Call sequence diagram shows 30 of 326 interactions; 296 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 1 of 78 (77 omitted); unresolved 1 of 157 (156 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/commands.py:current_command` | 3 | - | external | 2 |
| `backend/app/commands.py:current_command` | 3 | - | unresolved | 1 |
| `backend/app/commands.py:command_transaction` | 2 | - | external | 4 |
| `backend/app/commands.py:command_transaction` | 2 | - | unresolved | 12 |
| `backend/app/services/delivery_dependency_service.py:DeliveryDependencyService.reconcile` | 14 | - | unresolved | 23 |
| `backend/app/services/delivery_dependency_service.py:DeliveryDependencyService.reconcile` | 14 | - | external | 10 |
| `backend/app/services/delivery_dependency_service.py:DeliveryDependencyService.reconcile` | 14 | [backend/app/authority.py](../modules/authority.md) | internal | 3 |
| `backend/app/authority.py:internal_authority` | 20 | - | unresolved | 1 |
> Omission summary shows 8 of 74 groups; 66 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 92; effect analysis evaluated: 54, partial: 0, unavailable: 38. Counts include steps omitted from the displayed trace.

Collector observations for 54 source steps with known totals: observed: 210, emitted: 210, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `convert_triage_item_to_backlog` | `available` | `evaluated` | `available` | `5` | `5` | `0` |
| `command_transaction` | `available` | `evaluated` | `available` | `10` | `10` | `0` |
| `current_command` | `available` | `evaluated` | `available` | `2` | `2` | `0` |
| `getattr (backend/app/commands.py:current_command)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `isinstance` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `info.get` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `RuntimeError (backend/app/commands.py:command_transaction)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `CommandState` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `RuntimeError (backend/app/commands.py:command_transaction)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `db.flush` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `db.info.get (backend/app/commands.py:command_transaction)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `db.info.get (backend/app/commands.py:command_transaction)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. convert_triage_item_to_backlog"]
    s2["2. command_transaction"]
    s3["3. current_command"]
    s4["4. getattr (backend/app/commands.py:current_command)"]
    s5["5. isinstance"]
    s6["6. info.get"]
    s7["7. RuntimeError (backend/app/commands.py:command_transaction)"]
    s8["8. CommandState"]
    s9["9. RuntimeError (backend/app/commands.py:command_transaction)"]
    s10["10. db.flush"]
    s11["11. db.info.get (backend/app/commands.py:command_transaction)"]
    s12["12. db.info.get (backend/app/commands.py:command_transaction)"]
    s1 -->|"command_transaction(service.db)"| s2
    s2 -->|"current_command(db)"| s3
    s3 -. "getattr (backend/app/commands.py:current_command)(db, 'info', None)" .-> s4
    s3 -. "isinstance(info, dict)" .-> s5
    s3 -. "info.get('command')" .-> s6
    s2 -. "RuntimeError (backend/app/commands.py:command_transaction)('A preview must own its rollback boundary')" .-> s7
    s2 -->|"CommandState(mode=mode)"| s8
    s2 -. "RuntimeError (backend/app/commands.py:command_transaction)('A failed nested command cannot commit')" .-> s9
    s2 -. "db.flush(data not statically known)" .-> s10
    s2 -. "db.info.get (backend/app/commands.py:command_transaction)('delivery_changed_nodes')" .-> s11
    s2 -. "db.info.get (backend/app/commands.py:command_transaction)('delivery_graph_changed')" .-> s12
    b0["mutation db.info.pop"]
    s2 -. "mutation db.info.pop" .-> b0
    b1["mutation db.info.pop"]
    s2 -. "mutation db.info.pop" .-> b1
    b2["mutation db.info.pop"]
    s2 -. "mutation db.info.pop" .-> b2
    b3["mutation db.info.pop"]
    s2 -. "mutation db.info.pop" .-> b3
    click s1 "../modules/routers_triage.md"
    click s2 "../modules/commands.md"
    click s3 "../modules/commands.md"
    click s8 "../modules/commands.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
    class b3 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `convert_triage_item_to_backlog` | `triage_item_id: int`, `data: TriageConvertToBacklogRequest`, `service: Annotated[TriageService, Depends(get_triage_service)]` | `TriageConflictError` | - | `TriageConvertToTaskResponse(...)` |
| `command_transaction` | `db: AsyncSession`, `mode`, `commit` | - | `previous.failed`, `db.info[...]` | `none` |
| `current_command` | `db` | - | - | `...` |
| `getattr (backend/app/commands.py:current_command)` | - | - | - | - |
| `isinstance` | - | - | - | - |
| `info.get` | - | - | - | - |
| `RuntimeError (backend/app/commands.py:command_transaction)` | - | - | - | - |
| `CommandState` | - | - | - | - |
| `RuntimeError (backend/app/commands.py:command_transaction)` | - | - | - | - |
| `db.flush` | - | - | - | - |
| `db.info.get (backend/app/commands.py:command_transaction)` | - | - | - | - |
| `db.info.get (backend/app/commands.py:command_transaction)` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| convert_triage_item_to_backlog | command_transaction | 392 | `command_transaction(service.db)` |
| command_transaction | current_command | 100 | `current_command(db)` |
| current_command | getattr (backend/app/commands.py:current_command) | 86 | `getattr(db, 'info', None)` |
| current_command | isinstance | 87 | `isinstance(info, dict)` |
| current_command | info.get | 87 | `info.get('command')` |
| command_transaction | RuntimeError (backend/app/commands.py:command_transaction) | 103 | `RuntimeError('A preview must own its rollback boundary')` |
| command_transaction | CommandState | 110 | `CommandState(mode=mode)` |
| command_transaction | RuntimeError (backend/app/commands.py:command_transaction) | 115 | `RuntimeError('A failed nested command cannot commit')` |
| command_transaction | db.flush | 116 | `db.flush(data not statically known)` |
| command_transaction | db.info.get (backend/app/commands.py:command_transaction) | 117 | `db.info.get('delivery_changed_nodes')` |
| command_transaction | db.info.get (backend/app/commands.py:command_transaction) | 117 | `db.info.get('delivery_graph_changed')` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `db.info.pop` | `command_transaction` | 120 |
| mutation | `db.info.pop` | `command_transaction` | 133 |
| mutation | `db.info.pop` | `command_transaction` | 134 |
| mutation | `db.info.pop` | `command_transaction` | 136 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `current_command` | `getattr` | 86 |
| external_call | `current_command` | `isinstance` | 87 |
| unresolved_call | `current_command` | `info.get` | 87 |
| external_call | `command_transaction` | `RuntimeError` | 103 |
| external_call | `command_transaction` | `RuntimeError` | 115 |
| unresolved_call | `command_transaction` | `db.flush` | 116 |
| unresolved_call | `command_transaction` | `db.info.get` | 117 |
| step_limit | `convert_triage_item_to_backlog` | `first 12 steps` | 0 |
| truncated_flow | `convert_triage_item_to_backlog` | `depth limit` | 0 |

## Behavior

This flow starts at `convert_triage_item_to_backlog` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

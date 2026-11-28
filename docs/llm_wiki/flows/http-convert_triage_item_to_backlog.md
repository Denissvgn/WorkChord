# convert_triage_item_to_backlog

**Entry point:** `convert_triage_item_to_backlog` (`http`)
**Source:** [routers_triage](../modules/routers_triage.md)
**Modules touched:** [authority](../modules/authority.md), [commands](../modules/commands.md), [config](../modules/config.md), [delivery_dependency_service](../modules/delivery_dependency_service.md), and 13 more

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
- [task_reactivation_service](../modules/task_reactivation_service.md)
- [task_service](../modules/task_service.md)
- [time](../modules/time.md)
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
    participant p6 as process_reactivation_checks
    participant p7 as DeliveryDependencyService.reconcile
    participant p8 as DiscussionService.enqueue
    participant p9 as ReactivationService.evaluate_waiting
    participant p10 as _instance_authorities
    participant p11 as DeliveryDependencyService.validate_cycles
    participant p12 as normalize_stored_display_url
    participant p13 as DiscussionService.recipient_authorized
    participant p14 as TaskService.reserve_task_version
    participant p15 as clear_execution_evidence
    participant p16 as DeliveryDependencyService.graph
    participant p17 as normalize_external_http_url
    participant p18 as lock_iterations
    participant p19 as IdentityService.context
    participant p20 as ReactivationService._evaluate_isolated
    participant p21 as ReactivationService._due
    participant p22 as lock_planning
    participant p23 as ReactivationService._save_state
    participant p24 as ReactivationService._evaluate
    participant p25 as ReactivationService._restore_state
    participant p26 as require_mutation_revision
    participant p27 as validate_public_host
    participant p28 as current_command
    participant p29 as HTTPException (backend/app/routers/triag…rt_triage_item_to_backlog)
    participant p30 as service.convert_to_task
    p0->>p1: command_transaction
    p0->>p2: TriageSourceLinkOutcome.for_link
    p0->>p3: domain_result
    p0->>p4: TriageConvertToTaskResponse
    p2->>p5: evaluate_source_link
    p1->>p6: process_reactivation_checks
    p1->>p7: DeliveryDependencyService.reconcile
    p1->>p8: DiscussionService.enqueue
    p6->>p9: ReactivationService.evaluate_waiting
    p5->>p10: _instance_authorities
    p7->>p11: DeliveryDependencyService.validate_cycles
    p5->>p12: normalize_stored_display_url
    p8->>p13: DiscussionService.recipient_authorized
    p7->>p14: TaskService.reserve_task_version
    p7->>p15: clear_execution_evidence
    p11->>p16: DeliveryDependencyService.graph
    p12->>p17: normalize_external_http_url
    p14->>p18: lock_iterations
    p13->>p19: IdentityService.context
    p9->>p20: ReactivationService._evaluate_isolated
    p20->>p21: ReactivationService._due
    p20->>p22: lock_planning
    p20->>p23: ReactivationService._save_state
    p20->>p24: ReactivationService._evaluate
    p20->>p25: ReactivationService._restore_state
    p18->>p26: require_mutation_revision
    p17->>p27: validate_public_host
    p1->>p28: current_command
    p0-->>p29: HTTPException (backend/app/routers/triag…rt_triage_item_to_backlog)(409, detail=str(...))
    p0-->>p30: service.convert_to_task(triage_item_id, data)
```

> Call sequence diagram shows 30 of 411 interactions; 381 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 1 of 98 (97 omitted); unresolved 1 of 201 (200 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/commands.py:current_command` | 3 | - | external | 2 |
| `backend/app/commands.py:current_command` | 3 | - | unresolved | 1 |
| `backend/app/commands.py:command_transaction` | 2 | - | external | 4 |
| `backend/app/commands.py:command_transaction` | 2 | [backend/app/commands.py](../modules/commands.md) | internal | 1 |
| `backend/app/commands.py:command_transaction` | 2 | - | unresolved | 13 |
| `backend/app/services/task_reactivation_service.py:process_reactivation_checks` | 12 | [backend/app/services/task_reactivation_service.py](../modules/task_reactivation_service.md) | internal | 1 |
| `backend/app/services/task_reactivation_service.py:process_reactivation_checks` | 12 | - | external | 3 |
| `backend/app/services/task_reactivation_service.py:process_reactivation_checks` | 12 | - | unresolved | 3 |
> Omission summary shows 8 of 103 groups; 95 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 113; effect analysis evaluated: 74, partial: 0, unavailable: 39. Counts include steps omitted from the displayed trace.

Collector observations for 74 source steps with known totals: observed: 301, emitted: 301, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `convert_triage_item_to_backlog` | `available` | `evaluated` | `available` | `5` | `5` | `0` |
| `command_transaction` | `available` | `evaluated` | `available` | `10` | `10` | `0` |
| `current_command` | `available` | `evaluated` | `available` | `2` | `2` | `0` |
| `getattr (backend/app/commands.py:current_command)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `isinstance (backend/app/commands.py:current_command)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `info.get` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `RuntimeError (backend/app/commands.py:command_transaction)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `CommandState` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `RuntimeError (backend/app/commands.py:command_transaction)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `db.flush` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `db.info.get (backend/app/commands.py:command_transaction)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `process_reactivation_checks` | `available` | `evaluated` | `available` | `8` | `8` | `0` |

```mermaid
flowchart LR
    s1["1. convert_triage_item_to_backlog"]
    s2["2. command_transaction"]
    s3["3. current_command"]
    s4["4. getattr (backend/app/commands.py:current_command)"]
    s5["5. isinstance (backend/app/commands.py:current_command)"]
    s6["6. info.get"]
    s7["7. RuntimeError (backend/app/commands.py:command_transaction)"]
    s8["8. CommandState"]
    s9["9. RuntimeError (backend/app/commands.py:command_transaction)"]
    s10["10. db.flush"]
    s11["11. db.info.get (backend/app/commands.py:command_transaction)"]
    s12["12. process_reactivation_checks"]
    s1 -->|"command_transaction(service.db)"| s2
    s2 -->|"current_command(db)"| s3
    s3 -. "getattr (backend/app/commands.py:current_command)(db, 'info', None)" .-> s4
    s3 -. "isinstance (backend/app/commands.py:current_command)(info, dict)" .-> s5
    s3 -. "info.get('command')" .-> s6
    s2 -. "RuntimeError (backend/app/commands.py:command_transaction)('A preview must own its rollback boundary')" .-> s7
    s2 -->|"CommandState(mode=mode)"| s8
    s2 -. "RuntimeError (backend/app/commands.py:command_transaction)('A failed nested command cannot commit')" .-> s9
    s2 -. "db.flush(data not statically known)" .-> s10
    s2 -. "db.info.get (backend/app/commands.py:command_transaction)('reactivation_checks')" .-> s11
    s2 -->|"process_reactivation_checks(db)"| s12
    b0["mutation db.info.pop"]
    s2 -. "mutation db.info.pop" .-> b0
    b1["mutation db.info.pop"]
    s2 -. "mutation db.info.pop" .-> b1
    b2["mutation db.info.pop"]
    s2 -. "mutation db.info.pop" .-> b2
    b3["mutation db.info.pop"]
    s2 -. "mutation db.info.pop" .-> b3
    b4["mutation db.info.pop"]
    s12 -. "mutation db.info.pop" .-> b4
    b5["mutation db.info.pop"]
    s12 -. "mutation db.info.pop" .-> b5
    click s1 "../modules/routers_triage.md"
    click s2 "../modules/commands.md"
    click s3 "../modules/commands.md"
    click s8 "../modules/commands.md"
    click s12 "../modules/task_reactivation_service.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
    class b3 boundary
    class b4 boundary
    class b5 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `convert_triage_item_to_backlog` | `triage_item_id: int`, `data: TriageConvertToBacklogRequest`, `service: Annotated[TriageService, Depends(get_triage_service)]` | `TriageConflictError` | - | `TriageConvertToTaskResponse(...)` |
| `command_transaction` | `db: AsyncSession`, `mode`, `commit` | - | `previous.failed`, `db.info[...]` | `none` |
| `current_command` | `db` | - | - | `...` |
| `getattr (backend/app/commands.py:current_command)` | - | - | - | - |
| `isinstance (backend/app/commands.py:current_command)` | - | - | - | - |
| `info.get` | - | - | - | - |
| `RuntimeError (backend/app/commands.py:command_transaction)` | - | - | - | - |
| `CommandState` | - | - | - | - |
| `RuntimeError (backend/app/commands.py:command_transaction)` | - | - | - | - |
| `db.flush` | - | - | - | - |
| `db.info.get (backend/app/commands.py:command_transaction)` | - | - | - | - |
| `process_reactivation_checks` | `db` | `MAX_CASCADE_ROUNDS`, `_CHECKS`, `_CHECKS`, `MAX_CASCADE_ROUNDS` | - | `none` |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| convert_triage_item_to_backlog | command_transaction | 392 | `command_transaction(service.db)` |
| command_transaction | current_command | 103 | `current_command(db)` |
| current_command | getattr (backend/app/commands.py:current_command) | 89 | `getattr(db, 'info', None)` |
| current_command | isinstance (backend/app/commands.py:current_command) | 90 | `isinstance(info, dict)` |
| current_command | info.get | 90 | `info.get('command')` |
| command_transaction | RuntimeError (backend/app/commands.py:command_transaction) | 106 | `RuntimeError('A preview must own its rollback boundary')` |
| command_transaction | CommandState | 113 | `CommandState(mode=mode)` |
| command_transaction | RuntimeError (backend/app/commands.py:command_transaction) | 118 | `RuntimeError('A failed nested command cannot commit')` |
| command_transaction | db.flush | 119 | `db.flush(data not statically known)` |
| command_transaction | db.info.get (backend/app/commands.py:command_transaction) | 120 | `db.info.get('reactivation_checks')` |
| command_transaction | process_reactivation_checks | 123 | `process_reactivation_checks(db)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `db.info.pop` | `command_transaction` | 127 |
| mutation | `db.info.pop` | `command_transaction` | 140 |
| mutation | `db.info.pop` | `command_transaction` | 141 |
| mutation | `db.info.pop` | `command_transaction` | 143 |
| mutation | `db.info.pop` | `process_reactivation_checks` | 64 |
| mutation | `db.info.pop` | `process_reactivation_checks` | 68 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `current_command` | `getattr` | 89 |
| external_call | `current_command` | `isinstance` | 90 |
| unresolved_call | `current_command` | `info.get` | 90 |
| external_call | `command_transaction` | `RuntimeError` | 106 |
| external_call | `command_transaction` | `RuntimeError` | 118 |
| unresolved_call | `command_transaction` | `db.flush` | 119 |
| unresolved_call | `command_transaction` | `db.info.get` | 120 |
| step_limit | `convert_triage_item_to_backlog` | `first 12 steps` | 0 |
| truncated_flow | `convert_triage_item_to_backlog` | `depth limit` | 0 |

## Behavior

This flow starts at `convert_triage_item_to_backlog` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

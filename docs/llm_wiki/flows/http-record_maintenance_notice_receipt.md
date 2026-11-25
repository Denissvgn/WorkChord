# record_maintenance_notice_receipt

**Entry point:** `record_maintenance_notice_receipt` (`http`)
**Source:** [routers_agent](../modules/routers_agent.md)
**Modules touched:** [authority](../modules/authority.md), [commands](../modules/commands.md), [maintenance_window_service](../modules/maintenance_window_service.md), [models_maintenance](../modules/models_maintenance.md), and 2 more

**Complete modules touched:**

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [maintenance_window_service](../modules/maintenance_window_service.md)
- [models_maintenance](../modules/models_maintenance.md)
- [routers_agent](../modules/routers_agent.md)
- [time](../modules/time.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as record_maintenance_notice_receipt
    participant p1 as MaintenanceWindowService.record_own_notice
    participant p2 as MaintenanceWindowService
    participant p3 as _handle_agent_error
    participant p4 as MaintenanceWindowService._require_state
    participant p5 as MaintenanceWindowService._add_receipt
    participant p6 as receipt_view
    participant p7 as window_view
    participant p8 as commit_or_flush
    participant p9 as MaintenanceWindowService._window
    participant p10 as MaintenanceWindowConflict
    participant p11 as MaintenanceWindowReceipt
    participant p12 as _pm_key
    participant p13 as utc_now
    participant p14 as _iso
    participant p15 as internal_authority
    participant p16 as current_command
    participant p17 as isinstance (backend/app/routers/agent.py:_handle_agent_error)
    participant p18 as exc.detail
    participant p19 as str
    participant p20 as HTTPException
    p0->>p1: MaintenanceWindowService.record_own_notice
    p0->>p2: MaintenanceWindowService
    p0->>p3: _handle_agent_error
    p1->>p4: MaintenanceWindowService._require_state
    p1->>p5: MaintenanceWindowService._add_receipt
    p1->>p6: receipt_view
    p1->>p7: window_view
    p5->>p8: commit_or_flush
    p1->>p9: MaintenanceWindowService._window
    p1->>p10: MaintenanceWindowConflict
    p1->>p11: MaintenanceWindowReceipt
    p1->>p12: _pm_key
    p1->>p13: utc_now
    p6->>p14: _iso
    p5->>p15: internal_authority
    p8->>p16: current_command
    p3-->>p17: isinstance (backend/app/routers/agent.py:_handle_agent_error)(exc, AgentPermissionError)
    p3-->>p18: exc.detail
    p3-->>p19: str(exc)
    p3-->>p19: str(exc)
    p3-->>p20: HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
    p3-->>p17: isinstance (backend/app/routers/agent.py:_handle_agent_error)(exc, AgentRoutingConflictError)
    p3-->>p20: HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))
    p3-->>p17: isinstance (backend/app/routers/agent.py:_handle_agent_error)(exc, AgentTeamSetupConflictError)
    p3-->>p20: HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))
    p3-->>p18: exc.detail
    p3-->>p17: isinstance (backend/app/routers/agent.py:_handle_agent_error)(exc, TaskVersionConflictError)
    p3-->>p20: HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))
    p3-->>p18: exc.detail
    p3-->>p17: isinstance (backend/app/routers/agent.py:_handle_agent_error)(exc, AgentConflictError)
```

> Call sequence diagram shows 30 of 66 interactions; 36 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 11 of 28 (17 omitted); unresolved 3 of 15 (12 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/services/maintenance_window_service.py:MaintenanceWindowService._window` | 3 | - | unresolved | 3 |
| `backend/app/services/maintenance_window_service.py:MaintenanceWindowService._window` | 3 | - | external | 2 |
| `backend/app/services/maintenance_window_service.py:MaintenanceWindowService._require_state` | 9 | [backend/app/services/maintenance_window_service.py](../modules/maintenance_window_service.md) | internal | 1 |
| `backend/app/services/maintenance_window_service.py:MaintenanceWindowService._add_receipt` | 12 | - | unresolved | 4 |
| `backend/app/services/maintenance_window_service.py:MaintenanceWindowService._add_receipt` | 12 | - | external | 1 |
| `backend/app/authority.py:internal_authority` | 16 | - | unresolved | 1 |
| `backend/app/commands.py:current_command` | 21 | - | external | 2 |
| `backend/app/commands.py:current_command` | 21 | - | unresolved | 1 |
> Omission summary shows 8 of 14 groups; 6 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 24; effect analysis evaluated: 19, partial: 1, unavailable: 4. Counts include steps omitted from the displayed trace.

Collector observations for 20 source steps with known totals: observed: 63, emitted: 59, omitted: 4. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector omitted observations before flow assembly; displayed effects are partial.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `record_maintenance_notice_receipt` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `MaintenanceWindowService.record_own_notice` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `MaintenanceWindowService._window` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `select(…).where (backend/app/services/main…nanceWindowService._window)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select (backend/app/services/main…nanceWindowService._window)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `statement.with_for_update` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `self.db.scalar (backend/app/services/main…nanceWindowService._window)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `LookupError` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `MaintenanceWindowService._require_state` | `available` | `evaluated` | `available` | `2` | `2` | `0` |
| `MaintenanceWindowConflict` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `MaintenanceWindowConflict` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `MaintenanceWindowService._add_receipt` | `available` | `evaluated` | `available` | `8` | `8` | `0` |

```mermaid
flowchart LR
    s1["1. record_maintenance_notice_receipt"]
    s2["2. MaintenanceWindowService.record_own_notice"]
    s3["3. MaintenanceWindowService._window"]
    s4["4. select(…).where (backend/app/services/main…nanceWindowService._window)"]
    s5["5. select (backend/app/services/main…nanceWindowService._window)"]
    s6["6. statement.with_for_update"]
    s7["7. self.db.scalar (backend/app/services/main…nanceWindowService._window)"]
    s8["8. LookupError"]
    s9["9. MaintenanceWindowService._require_state"]
    s10["10. MaintenanceWindowConflict"]
    s11["11. MaintenanceWindowConflict"]
    s12["12. MaintenanceWindowService._add_receipt"]
    s1 -->|"MaintenanceWindowService.record_own_notice(actor, window_id)"| s2
    s2 -->|"MaintenanceWindowService._window(window_id, lock=True)"| s3
    s3 -. "select(…).where (backend/app/services/main…nanceWindowService._window)(...)" .-> s4
    s3 -. "select (backend/app/services/main…nanceWindowService._window)(MaintenanceWindow)" .-> s5
    s3 -. "statement.with_for_update(data not statically known)" .-> s6
    s3 -. "self.db.scalar (backend/app/services/main…nanceWindowService._window)(statement)" .-> s7
    s3 -. "LookupError('Maintenance window not found')" .-> s8
    s2 -->|"MaintenanceWindowService._require_state(window, 'announced')"| s9
    s9 -->|"MaintenanceWindowConflict('maintenance_window_state_conflict', ..., maintenance_window_id=window.id, maintenance_window_state=window.state)"| s10
    s2 -->|"MaintenanceWindowConflict('maintenance_notice_not_required', 'Only an active PM agent records a maintenance notice receipt.')"| s11
    s2 -->|"MaintenanceWindowService._add_receipt(MaintenanceWindowReceipt(...))"| s12
    b0["mutation self.db.add"]
    s12 -. "mutation self.db.add" .-> b0
    click s1 "../modules/routers_agent.md"
    click s2 "../modules/maintenance_window_service.md"
    click s3 "../modules/maintenance_window_service.md"
    click s9 "../modules/maintenance_window_service.md"
    click s10 "../modules/maintenance_window_service.md"
    click s11 "../modules/maintenance_window_service.md"
    click s12 "../modules/maintenance_window_service.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `record_maintenance_notice_receipt` | `window_id: int`, `actor: Annotated[AgentActor, Depends(get_agent_actor)]`, `db: Annotated[AsyncSession, Depends(get_db, scope='function')]` | - | - | `...` |
| `MaintenanceWindowService.record_own_notice` | `actor: AgentActor`, `window_id: int` | - | - | `{...}` |
| `MaintenanceWindowService._window` | `window_id: int`, `lock: bool` | `MaintenanceWindow` | - | `window` |
| `select(…).where (backend/app/services/main…nanceWindowService._window)` | - | - | - | - |
| `select (backend/app/services/main…nanceWindowService._window)` | - | - | - | - |
| `statement.with_for_update` | - | - | - | - |
| `self.db.scalar (backend/app/services/main…nanceWindowService._window)` | - | - | - | - |
| `LookupError` | - | - | - | - |
| `MaintenanceWindowService._require_state` | `window: MaintenanceWindow`, `state: str` | - | - | - |
| `MaintenanceWindowConflict` | - | - | - | - |
| `MaintenanceWindowConflict` | - | - | - | - |
| `MaintenanceWindowService._add_receipt` | `receipt: MaintenanceWindowReceipt` | `MaintenanceWindowReceipt`, `MaintenanceWindowReceipt`, `self.db`, `self.db` | - | `existing`, `receipt` |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| record_maintenance_notice_receipt | MaintenanceWindowService.record_own_notice | 1109 | `MaintenanceWindowService(db).record_own_notice(actor, window_id)` |
| MaintenanceWindowService.record_own_notice | MaintenanceWindowService._window | 476 | `self._window(window_id, lock=True)` |
| MaintenanceWindowService._window | select(…).where (backend/app/services/main…nanceWindowService._window) | 134 | `select(MaintenanceWindow).where(...)` |
| MaintenanceWindowService._window | select (backend/app/services/main…nanceWindowService._window) | 134 | `select(MaintenanceWindow)` |
| MaintenanceWindowService._window | statement.with_for_update | 136 | `statement.with_for_update(data not statically known)` |
| MaintenanceWindowService._window | self.db.scalar (backend/app/services/main…nanceWindowService._window) | 137 | `self.db.scalar(statement)` |
| MaintenanceWindowService._window | LookupError | 139 | `LookupError('Maintenance window not found')` |
| MaintenanceWindowService.record_own_notice | MaintenanceWindowService._require_state | 477 | `self._require_state(window, 'announced')` |
| MaintenanceWindowService._require_state | MaintenanceWindowConflict | 493 | `MaintenanceWindowConflict('maintenance_window_state_conflict', ..., maintenance_window_id=window.id, maintenance_window_state=window.state)` |
| MaintenanceWindowService.record_own_notice | MaintenanceWindowConflict | 479 | `MaintenanceWindowConflict('maintenance_notice_not_required', 'Only an active PM agent records a maintenance notice receipt.')` |
| MaintenanceWindowService.record_own_notice | MaintenanceWindowService._add_receipt | 482 | `self._add_receipt(MaintenanceWindowReceipt(...))` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `self.db.add` | `MaintenanceWindowService._add_receipt` | 508 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `MaintenanceWindowService._window` | `select(MaintenanceWindow).where` | 134 |
| external_call | `MaintenanceWindowService._window` | `select` | 134 |
| unresolved_call | `MaintenanceWindowService._window` | `statement.with_for_update` | 136 |
| unresolved_call | `MaintenanceWindowService._window` | `self.db.scalar` | 137 |
| external_call | `MaintenanceWindowService._window` | `LookupError` | 139 |
| step_limit | `record_maintenance_notice_receipt` | `first 12 steps` | 0 |

## Behavior

Records that this PM has received the maintenance notice, which the operator's begin check counts. It carries no consent for any run. A coordinated control-plane maintenance window has one open window at a time. Announcing it closes admission for new work at once; work already holding a live claim keeps renewing and may finish. The operator can begin only when every live claim owner has acknowledged for the claim's current generation, each lease outlives the bounded outage plus its margin, no running run lacks a live claim and every PM has a notice receipt. A PM notice is recorded evidence of notification, never run-owner consent. Closing or cancelling reopens admission.

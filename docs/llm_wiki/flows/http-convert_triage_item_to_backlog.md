# convert_triage_item_to_backlog

**Entry point:** `convert_triage_item_to_backlog` (`http`)
**Source:** [routers_triage](../modules/routers_triage.md)
**Modules touched:** [commands](../modules/commands.md), [delivery_dependency_service](../modules/delivery_dependency_service.md), [discussion_service](../modules/discussion_service.md), and 3 more

**Complete modules touched:**

- [commands](../modules/commands.md)
- [delivery_dependency_service](../modules/delivery_dependency_service.md)
- [discussion_service](../modules/discussion_service.md)
- [routers_task_domain](../modules/routers_task_domain.md)
- [routers_triage](../modules/routers_triage.md)
- [schemas_triage](../modules/schemas_triage.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as convert_triage_item_to_backlog
    participant p1 as command_transaction
    participant p2 as current_command
    participant p3 as getattr
    participant p4 as isinstance
    participant p5 as info.get
    participant p6 as RuntimeError
    participant p7 as CommandState
    participant p8 as db.flush
    participant p9 as db.info.get
    participant p10 as DeliveryDependencyService(…).reconcile
    participant p11 as DeliveryDependencyService
    participant p12 as sorted
    participant p13 as db.info.pop
    participant p14 as set
    participant p15 as DiscussionService(…).enqueue
    participant p16 as DiscussionService
    participant p17 as db.rollback
    participant p18 as db.commit
    participant p19 as domain_result
    participant p20 as HTTPException (backend/app/routers/task_domain.py:domain_result)
    participant p21 as exc.detail
    participant p22 as str (backend/app/routers/task_domain.py:domain_result)
    p0->>p1: command_transaction
    p1->>p2: current_command
    p2-->>p3: getattr
    p2-->>p4: isinstance
    p2-->>p5: info.get
    p1-->>p6: RuntimeError
    p1->>p7: CommandState
    p1-->>p6: RuntimeError
    p1-->>p8: db.flush
    p1-->>p9: db.info.get
    p1-->>p9: db.info.get
    p1-->>p9: db.info.get
    p1-->>p10: DeliveryDependencyService(…).reconcile
    p1->>p11: DeliveryDependencyService
    p1-->>p12: sorted
    p1-->>p13: db.info.pop
    p1-->>p14: set
    p1-->>p15: DiscussionService(…).enqueue
    p1->>p16: DiscussionService
    p1-->>p17: db.rollback
    p1-->>p18: db.commit
    p1-->>p8: db.flush
    p1-->>p17: db.rollback
    p1-->>p13: db.info.pop
    p1-->>p13: db.info.pop
    p0->>p19: domain_result
    p19-->>p20: HTTPException (backend/app/routers/task_domain.py:domain_result)
    p19-->>p21: exc.detail
    p19-->>p20: HTTPException (backend/app/routers/task_domain.py:domain_result)
    p19-->>p22: str (backend/app/routers/task_domain.py:domain_result)
```

> Call sequence diagram shows 30 of 37 interactions; 7 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. convert_triage_item_to_backlog"]
    s2["2. command_transaction"]
    s3["3. current_command"]
    s4["4. getattr"]
    s5["5. isinstance"]
    s6["6. info.get"]
    s7["7. RuntimeError"]
    s8["8. CommandState"]
    s9["9. RuntimeError"]
    s10["10. db.flush"]
    s11["11. db.info.get"]
    s12["12. db.info.get"]
    s1 -->|"command_transaction(service.db)"| s2
    s2 -->|"current_command(db)"| s3
    s3 -. "getattr(db, 'info', None)" .-> s4
    s3 -. "isinstance(info, dict)" .-> s5
    s3 -. "info.get('command')" .-> s6
    s2 -. "RuntimeError('A preview must own its rollback boundary')" .-> s7
    s2 -->|"CommandState(mode=mode)"| s8
    s2 -. "RuntimeError('A failed nested command cannot commit')" .-> s9
    s2 -. "db.flush(data not statically known)" .-> s10
    s2 -. "db.info.get('delivery_changed_nodes')" .-> s11
    s2 -. "db.info.get('delivery_graph_changed')" .-> s12
    b0["mutation db.info.pop"]
    s2 -. "mutation db.info.pop" .-> b0
    b1["mutation db.info.pop"]
    s2 -. "mutation db.info.pop" .-> b1
    b2["mutation db.info.pop"]
    s2 -. "mutation db.info.pop" .-> b2
    click s1 "../modules/routers_triage.md"
    click s2 "../modules/commands.md"
    click s3 "../modules/commands.md"
    click s8 "../modules/commands.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `convert_triage_item_to_backlog` | `triage_item_id: int`, `data: TriageConvertToBacklogRequest`, `service: Annotated[TriageService, Depends(get_triage_service)]` | `TriageConflictError` | - | `TriageConvertToTaskResponse(...)` |
| `command_transaction` | `db: AsyncSession`, `mode`, `commit` | - | `previous.failed`, `db.info[...]` | `none` |
| `current_command` | `db` | - | - | `...` |
| `getattr` | - | - | - | - |
| `isinstance` | - | - | - | - |
| `info.get` | - | - | - | - |
| `RuntimeError` | - | - | - | - |
| `CommandState` | - | - | - | - |
| `RuntimeError` | - | - | - | - |
| `db.flush` | - | - | - | - |
| `db.info.get` | - | - | - | - |
| `db.info.get` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| convert_triage_item_to_backlog | command_transaction | 387 | `command_transaction(service.db)` |
| command_transaction | current_command | 85 | `current_command(db)` |
| current_command | getattr | 71 | `getattr(db, 'info', None)` |
| current_command | isinstance | 72 | `isinstance(info, dict)` |
| current_command | info.get | 72 | `info.get('command')` |
| command_transaction | RuntimeError | 88 | `RuntimeError('A preview must own its rollback boundary')` |
| command_transaction | CommandState | 95 | `CommandState(mode=mode)` |
| command_transaction | RuntimeError | 100 | `RuntimeError('A failed nested command cannot commit')` |
| command_transaction | db.flush | 101 | `db.flush(data not statically known)` |
| command_transaction | db.info.get | 102 | `db.info.get('delivery_changed_nodes')` |
| command_transaction | db.info.get | 102 | `db.info.get('delivery_graph_changed')` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `db.info.pop` | `command_transaction` | 105 |
| mutation | `db.info.pop` | `command_transaction` | 118 |
| mutation | `db.info.pop` | `command_transaction` | 120 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `current_command` | `getattr` | 71 |
| external_call | `current_command` | `isinstance` | 72 |
| unresolved_call | `current_command` | `info.get` | 72 |
| external_call | `command_transaction` | `RuntimeError` | 88 |
| external_call | `command_transaction` | `RuntimeError` | 100 |
| unresolved_call | `command_transaction` | `db.flush` | 101 |
| unresolved_call | `command_transaction` | `db.info.get` | 102 |
| step_limit | `convert_triage_item_to_backlog` | `first 12 steps` | 0 |

## Behavior

This flow starts at `convert_triage_item_to_backlog` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

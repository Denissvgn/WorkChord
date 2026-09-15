# preview_iteration_schedule

**Entry point:** `preview_iteration_schedule` (`http`)
**Source:** [routers_gantt](../modules/routers_gantt.md)
**Modules touched:** [authority](../modules/authority.md), [commands](../modules/commands.md), [iteration_service](../modules/iteration_service.md), [routers_gantt](../modules/routers_gantt.md), and 6 more

**Complete modules touched:**

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [iteration_service](../modules/iteration_service.md)
- [routers_gantt](../modules/routers_gantt.md)
- [schemas_gantt](../modules/schemas_gantt.md)
- [schemas_task](../modules/schemas_task.md)
- [services_work_metrics](../modules/services_work_metrics.md)
- [task_service](../modules/task_service.md)
- [tasks](../modules/tasks.md)
- [time](../modules/time.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as preview_iteration_schedule
    participant p1 as IterationService
    participant p2 as TaskService
    participant p3 as iteration_service.get_by_id
    participant p4 as HTTPException
    participant p5 as command_transaction
    participant p6 as current_command
    participant p7 as getattr (backend/app/commands.py:current_command)
    participant p8 as isinstance
    participant p9 as info.get
    participant p10 as RuntimeError (backend/app/commands.py:command_transaction)
    participant p11 as CommandState
    participant p12 as db.rollback
    participant p13 as db.commit
    participant p14 as db.flush
    participant p15 as db.info.pop
    participant p16 as lock_iterations
    participant p17 as RuntimeError (backend/app/commands.py:lock_iterations)
    participant p18 as sorted (backend/app/commands.py:lock_iterations)
    participant p19 as set (backend/app/commands.py:lock_iterations)
    participant p20 as AggregateVersionConflict
    participant p21 as db.scalar
    participant p22 as select(…).where(…).with_for_update
    participant p23 as select(…).where (backend/app/commands.py:lock_iterations)
    participant p24 as select
    participant p25 as ValueError (backend/app/commands.py:lock_iterations)
    participant p26 as db.info.get (backend/app/commands.py:lock_iterations)
    p0->>p1: IterationService
    p0->>p2: TaskService
    p0-->>p3: iteration_service.get_by_id
    p0-->>p4: HTTPException
    p0->>p5: command_transaction
    p5->>p6: current_command
    p6-->>p7: getattr (backend/app/commands.py:current_command)
    p6-->>p8: isinstance
    p6-->>p9: info.get
    p5-->>p10: RuntimeError (backend/app/commands.py:command_transaction)
    p5->>p11: CommandState
    p5-->>p10: RuntimeError (backend/app/commands.py:command_transaction)
    p5-->>p12: db.rollback
    p5-->>p13: db.commit
    p5-->>p14: db.flush
    p5-->>p12: db.rollback
    p5-->>p15: db.info.pop
    p5-->>p15: db.info.pop
    p0->>p16: lock_iterations
    p16->>p6: current_command
    p16-->>p17: RuntimeError (backend/app/commands.py:lock_iterations)
    p16-->>p18: sorted (backend/app/commands.py:lock_iterations)
    p16-->>p19: set (backend/app/commands.py:lock_iterations)
    p16->>p20: AggregateVersionConflict
    p16-->>p21: db.scalar
    p16-->>p22: select(…).where(…).with_for_update
    p16-->>p23: select(…).where (backend/app/commands.py:lock_iterations)
    p16-->>p24: select
    p16-->>p25: ValueError (backend/app/commands.py:lock_iterations)
    p16-->>p26: db.info.get (backend/app/commands.py:lock_iterations)
```

> Call sequence diagram shows 30 of 140 interactions; 110 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. preview_iteration_schedule"]
    s2["2. IterationService"]
    s3["3. TaskService"]
    s4["4. iteration_service.get_by_id"]
    s5["5. HTTPException"]
    s6["6. command_transaction"]
    s7["7. current_command"]
    s8["8. getattr (backend/app/commands.py:current_command)"]
    s9["9. isinstance"]
    s10["10. info.get"]
    s11["11. RuntimeError (backend/app/commands.py:command_transaction)"]
    s12["12. CommandState"]
    s1 -->|"IterationService(db)"| s2
    s1 -->|"TaskService(db)"| s3
    s1 -. "iteration_service.get_by_id(iteration_id)" .-> s4
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s5
    s1 -->|"command_transaction(db, mode='preview')"| s6
    s6 -->|"current_command(db)"| s7
    s7 -. "getattr (backend/app/commands.py:current_command)(db, 'info', None)" .-> s8
    s7 -. "isinstance(info, dict)" .-> s9
    s7 -. "info.get('command')" .-> s10
    s6 -. "RuntimeError (backend/app/commands.py:command_transaction)('A preview must own its rollback boundary')" .-> s11
    s6 -->|"CommandState(mode=mode)"| s12
    b0["mutation gantt_tasks.append"]
    s1 -. "mutation gantt_tasks.append" .-> b0
    b1["mutation db.info.pop"]
    s6 -. "mutation db.info.pop" .-> b1
    b2["mutation db.info.pop"]
    s6 -. "mutation db.info.pop" .-> b2
    click s1 "../modules/routers_gantt.md"
    click s2 "../modules/iteration_service.md"
    click s3 "../modules/task_service.md"
    click s6 "../modules/commands.md"
    click s7 "../modules/commands.md"
    click s12 "../modules/commands.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `preview_iteration_schedule` | `iteration_id: int`, `data: SchedulePreviewRequest`, `service: Annotated[SchedulerService, Depends(get_scheduler_service)]`, `db: Annotated[AsyncSession, Depends(get_db, scope='function')]` | `status`, `status`, `status` | - | `SchedulePreviewResponse(...)` |
| `IterationService` | - | - | - | - |
| `TaskService` | - | - | - | - |
| `iteration_service.get_by_id` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `command_transaction` | `db: AsyncSession`, `mode`, `commit` | - | `previous.failed`, `db.info[...]` | `none` |
| `current_command` | `db` | - | - | `...` |
| `getattr (backend/app/commands.py:current_command)` | - | - | - | - |
| `isinstance` | - | - | - | - |
| `info.get` | - | - | - | - |
| `RuntimeError (backend/app/commands.py:command_transaction)` | - | - | - | - |
| `CommandState` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| preview_iteration_schedule | IterationService | 72 | `IterationService(db)` |
| preview_iteration_schedule | TaskService | 73 | `TaskService(db)` |
| preview_iteration_schedule | iteration_service.get_by_id | 74 | `iteration_service.get_by_id(iteration_id)` |
| preview_iteration_schedule | HTTPException | 76 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| preview_iteration_schedule | command_transaction | 81 | `command_transaction(db, mode='preview')` |
| command_transaction | current_command | 52 | `current_command(db)` |
| current_command | getattr (backend/app/commands.py:current_command) | 38 | `getattr(db, 'info', None)` |
| current_command | isinstance | 39 | `isinstance(info, dict)` |
| current_command | info.get | 39 | `info.get('command')` |
| command_transaction | RuntimeError (backend/app/commands.py:command_transaction) | 55 | `RuntimeError('A preview must own its rollback boundary')` |
| command_transaction | CommandState | 62 | `CommandState(mode=mode)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `gantt_tasks.append` | `preview_iteration_schedule` | 100 |
| mutation | `db.info.pop` | `command_transaction` | 78 |
| mutation | `db.info.pop` | `command_transaction` | 80 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `preview_iteration_schedule` | `iteration_service.get_by_id` | 74 |
| external_call | `preview_iteration_schedule` | `HTTPException` | 76 |
| external_call | `current_command` | `getattr` | 38 |
| external_call | `current_command` | `isinstance` | 39 |
| unresolved_call | `current_command` | `info.get` | 39 |
| external_call | `command_transaction` | `RuntimeError` | 55 |
| step_limit | `preview_iteration_schedule` | `first 12 steps` | 0 |

## Behavior

This flow starts at `preview_iteration_schedule` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

Applies sandbox inputs and the real scheduler inside a rollback-only owner, serializes the projected result with its input revision, and leaves durable state and snapshot retention unchanged.

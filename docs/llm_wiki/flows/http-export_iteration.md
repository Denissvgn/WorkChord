# export_iteration

**Entry point:** `export_iteration` (`http`)
**Source:** [export](../modules/export.md)
**Modules touched:** [export](../modules/export.md), [iteration_service](../modules/iteration_service.md), [task_service](../modules/task_service.md), [team_service](../modules/team_service.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as export_iteration
    participant p1 as IterationService
    participant p2 as iteration_service.get_by_id
    participant p3 as HTTPException
    participant p4 as TaskService
    participant p5 as task_service.get_by_iteration
    participant p6 as TeamService
    participant p7 as team_service.get_by_iteration
    participant p8 as iteration.start_date.isoformat
    participant p9 as iteration.end_date.isoformat
    participant p10 as calculate_member_workload
    participant p11 as v.start_date.isoformat
    participant p12 as v.end_date.isoformat
    participant p13 as _task_to_export
    participant p14 as isinstance
    participant p15 as json.loads
    participant p16 as task.start_date.isoformat
    participant p17 as task.end_date.isoformat
    participant p18 as task.actual_start_date.isoformat
    participant p19 as task.actual_end_date.isoformat
    participant p20 as task.min_start_date.isoformat
    participant p21 as task.max_end_date.isoformat
    participant p22 as getattr
    participant p23 as JSONResponse
    p0->>p1: IterationService
    p0-->>p2: iteration_service.get_by_id
    p0-->>p3: HTTPException
    p0->>p4: TaskService
    p0-->>p5: task_service.get_by_iteration
    p0->>p6: TeamService
    p0-->>p7: team_service.get_by_iteration
    p0-->>p8: iteration.start_date.isoformat
    p0-->>p9: iteration.end_date.isoformat
    p0-->>p10: calculate_member_workload
    p0-->>p11: v.start_date.isoformat
    p0-->>p12: v.end_date.isoformat
    p0->>p13: _task_to_export
    p13-->>p14: isinstance
    p13-->>p15: json.loads
    p13-->>p16: task.start_date.isoformat
    p13-->>p17: task.end_date.isoformat
    p13-->>p18: task.actual_start_date.isoformat
    p13-->>p19: task.actual_end_date.isoformat
    p13-->>p20: task.min_start_date.isoformat
    p13-->>p21: task.max_end_date.isoformat
    p13-->>p22: getattr
    p13->>p13: _task_to_export
    p0-->>p23: JSONResponse
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. export_iteration"]
    s2["2. IterationService"]
    s3["3. iteration_service.get_by_id"]
    s4["4. HTTPException"]
    s5["5. TaskService"]
    s6["6. task_service.get_by_iteration"]
    s7["7. TeamService"]
    s8["8. team_service.get_by_iteration"]
    s9["9. iteration.start_date.isoformat"]
    s10["10. iteration.end_date.isoformat"]
    s11["11. calculate_member_workload"]
    s12["12. v.start_date.isoformat"]
    s1 -->|"IterationService(db)"| s2
    s1 -. "iteration_service.get_by_id(iteration_id)" .-> s3
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s4
    s1 -->|"TaskService(db)"| s5
    s1 -. "task_service.get_by_iteration(iteration_id, max_tasks=MAX_SYNC_EXPORT_TASKS)" .-> s6
    s1 -->|"TeamService(db)"| s7
    s1 -. "team_service.get_by_iteration(iteration_id)" .-> s8
    s1 -. "iteration.start_date.isoformat(data not statically known)" .-> s9
    s1 -. "iteration.end_date.isoformat(data not statically known)" .-> s10
    s1 -. "calculate_member_workload(m, tasks)" .-> s11
    s1 -. "v.start_date.isoformat(data not statically known)" .-> s12
    click s1 "../modules/export.md"
    click s2 "../modules/iteration_service.md"
    click s5 "../modules/task_service.md"
    click s7 "../modules/team_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `export_iteration` | `iteration_id: int`, `db: Annotated[AsyncSession, Depends(get_db)]` | `status`, `MAX_SYNC_EXPORT_TASKS` | - | `JSONResponse(...)` |
| `IterationService` | - | - | - | - |
| `iteration_service.get_by_id` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `TaskService` | - | - | - | - |
| `task_service.get_by_iteration` | - | - | - | - |
| `TeamService` | - | - | - | - |
| `team_service.get_by_iteration` | - | - | - | - |
| `iteration.start_date.isoformat` | - | - | - | - |
| `iteration.end_date.isoformat` | - | - | - | - |
| `calculate_member_workload` | - | - | - | - |
| `v.start_date.isoformat` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| export_iteration | IterationService | 79 | `IterationService(db)` |
| export_iteration | iteration_service.get_by_id | 80 | `iteration_service.get_by_id(iteration_id)` |
| export_iteration | HTTPException | 83 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| export_iteration | TaskService | 88 | `TaskService(db)` |
| export_iteration | task_service.get_by_iteration | 89 | `task_service.get_by_iteration(iteration_id, max_tasks=MAX_SYNC_EXPORT_TASKS)` |
| export_iteration | TeamService | 94 | `TeamService(db)` |
| export_iteration | team_service.get_by_iteration | 95 | `team_service.get_by_iteration(iteration_id)` |
| export_iteration | iteration.start_date.isoformat | 128 | `iteration.start_date.isoformat(data not statically known)` |
| export_iteration | iteration.end_date.isoformat | 129 | `iteration.end_date.isoformat(data not statically known)` |
| export_iteration | calculate_member_workload | 140 | `calculate_member_workload(m, tasks)` |
| export_iteration | v.start_date.isoformat | 143 | `v.start_date.isoformat(data not statically known)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `export_iteration` | `iteration_service.get_by_id` | 80 |
| external_call | `export_iteration` | `HTTPException` | 83 |
| unresolved_call | `export_iteration` | `task_service.get_by_iteration` | 89 |
| unresolved_call | `export_iteration` | `team_service.get_by_iteration` | 95 |
| unresolved_call | `export_iteration` | `iteration.start_date.isoformat` | 128 |
| unresolved_call | `export_iteration` | `iteration.end_date.isoformat` | 129 |
| unresolved_call | `export_iteration` | `calculate_member_workload` | 140 |
| unresolved_call | `export_iteration` | `v.start_date.isoformat` | 143 |
| step_limit | `export_iteration` | `first 12 steps` | 0 |

## Behavior

This flow starts at `export_iteration` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

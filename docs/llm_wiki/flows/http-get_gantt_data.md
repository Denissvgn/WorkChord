# get_gantt_data

**Entry point:** `get_gantt_data` (`http`)
**Source:** [routers_gantt](../modules/routers_gantt.md)
**Modules touched:** [calendar_service](../modules/calendar_service.md), [iteration_service](../modules/iteration_service.md), [routers_gantt](../modules/routers_gantt.md), [schemas_gantt](../modules/schemas_gantt.md), and 3 more

**Complete modules touched:**

- [calendar_service](../modules/calendar_service.md)
- [iteration_service](../modules/iteration_service.md)
- [routers_gantt](../modules/routers_gantt.md)
- [schemas_gantt](../modules/schemas_gantt.md)
- [schemas_iteration](../modules/schemas_iteration.md)
- [task_service](../modules/task_service.md)
- [team_service](../modules/team_service.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as get_gantt_data
    participant p1 as IterationService
    participant p2 as TaskService
    participant p3 as TeamService
    participant p4 as iteration_service.get_by_id
    participant p5 as task_service.get_by_iteration
    participant p6 as team_service.get_by_iteration
    participant p7 as HTTPException
    participant p8 as CalendarService
    participant p9 as calendar_service.calculate_working_days
    participant p10 as _task_to_gantt
    participant p11 as attributes.instance_state
    participant p12 as len
    participant p13 as bool
    participant p14 as GanttAssignee
    participant p15 as GanttMilestone
    participant p16 as set (backend/app/routers/gantt.py:_task_to_gantt)
    participant p17 as assignees.append
    participant p18 as seen_ids.add
    participant p19 as json.loads
    participant p20 as task.start_date.isoformat
    participant p21 as task.end_date.isoformat
    participant p22 as children.append
    participant p23 as sum
    p0->>p1: IterationService
    p0->>p2: TaskService
    p0->>p3: TeamService
    p0-->>p4: iteration_service.get_by_id
    p0-->>p5: task_service.get_by_iteration
    p0-->>p6: team_service.get_by_iteration
    p0-->>p7: HTTPException
    p0->>p8: CalendarService
    p0-->>p9: calendar_service.calculate_working_days
    p0->>p10: _task_to_gantt
    p10-->>p11: attributes.instance_state
    p10-->>p11: attributes.instance_state
    p10-->>p11: attributes.instance_state
    p10-->>p11: attributes.instance_state
    p10-->>p12: len
    p10-->>p13: bool
    p10->>p14: GanttAssignee
    p10->>p15: GanttMilestone
    p10-->>p16: set (backend/app/routers/gantt.py:_task_to_gantt)
    p10-->>p11: attributes.instance_state
    p10-->>p17: assignees.append
    p10->>p14: GanttAssignee
    p10-->>p18: seen_ids.add
    p10-->>p19: json.loads
    p10-->>p20: task.start_date.isoformat
    p10-->>p21: task.end_date.isoformat
    p10->>p10: _task_to_gantt
    p10-->>p22: children.append
    p10-->>p23: sum
    p10-->>p12: len
```

> Call sequence diagram shows 30 of 44 interactions; 14 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. get_gantt_data"]
    s2["2. IterationService"]
    s3["3. TaskService"]
    s4["4. TeamService"]
    s5["5. iteration_service.get_by_id"]
    s6["6. task_service.get_by_iteration"]
    s7["7. team_service.get_by_iteration"]
    s8["8. HTTPException"]
    s9["9. CalendarService"]
    s10["10. calendar_service.calculate_working_days"]
    s11["11. _task_to_gantt"]
    s12["12. attributes.instance_state"]
    s1 -->|"IterationService(db)"| s2
    s1 -->|"TaskService(db)"| s3
    s1 -->|"TeamService(db)"| s4
    s1 -. "iteration_service.get_by_id(iteration_id)" .-> s5
    s1 -. "task_service.get_by_iteration(iteration_id)" .-> s6
    s1 -. "team_service.get_by_iteration(iteration_id)" .-> s7
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s8
    s1 -->|"CalendarService(db)"| s9
    s1 -. "calendar_service.calculate_working_days(iteration.calendar, iteration.start_date, iteration.end_date)" .-> s10
    s1 -->|"_task_to_gantt(task, iteration.end_date)"| s11
    s11 -. "attributes.instance_state(task)" .-> s12
    b0["mutation gantt_tasks.append"]
    s1 -. "mutation gantt_tasks.append" .-> b0
    b1["mutation overdue_ids.append"]
    s1 -. "mutation overdue_ids.append" .-> b1
    b2["mutation overdue_ids.append"]
    s1 -. "mutation overdue_ids.append" .-> b2
    b3["mutation vacation_dates.update"]
    s1 -. "mutation vacation_dates.update" .-> b3
    b4["mutation assignees.append"]
    s11 -. "mutation assignees.append" .-> b4
    b5["mutation seen_ids.add"]
    s11 -. "mutation seen_ids.add" .-> b5
    b6["mutation children.append"]
    s11 -. "mutation children.append" .-> b6
    click s1 "../modules/routers_gantt.md"
    click s2 "../modules/iteration_service.md"
    click s3 "../modules/task_service.md"
    click s4 "../modules/team_service.md"
    click s9 "../modules/calendar_service.md"
    click s11 "../modules/routers_gantt.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
    class b3 boundary
    class b4 boundary
    class b5 boundary
    class b6 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `get_gantt_data` | `iteration_id: int`, `db: Annotated[AsyncSession, Depends(get_db)]` | `status` | `member_vacations[...]` | `GanttResponse(...)` |
| `IterationService` | - | - | - | - |
| `TaskService` | - | - | - | - |
| `TeamService` | - | - | - | - |
| `iteration_service.get_by_id` | - | - | - | - |
| `task_service.get_by_iteration` | - | - | - | - |
| `team_service.get_by_iteration` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `CalendarService` | - | - | - | - |
| `calendar_service.calculate_working_days` | - | - | - | - |
| `_task_to_gantt` | `task: Task`, `iteration_end_date: date`, `issues: Optional[list[WorkloadIssue]]`, `decisions: Optional[list[SchedulingDecision]]` | `json` | - | `None`, `GanttTask(...)` |
| `attributes.instance_state` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| get_gantt_data | IterationService | 144 | `IterationService(db)` |
| get_gantt_data | TaskService | 145 | `TaskService(db)` |
| get_gantt_data | TeamService | 146 | `TeamService(db)` |
| get_gantt_data | iteration_service.get_by_id | 151 | `iteration_service.get_by_id(iteration_id)` |
| get_gantt_data | task_service.get_by_iteration | 152 | `task_service.get_by_iteration(iteration_id)` |
| get_gantt_data | team_service.get_by_iteration | 153 | `team_service.get_by_iteration(iteration_id)` |
| get_gantt_data | HTTPException | 156 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| get_gantt_data | CalendarService | 162 | `CalendarService(db)` |
| get_gantt_data | calendar_service.calculate_working_days | 163 | `calendar_service.calculate_working_days(iteration.calendar, iteration.start_date, iteration.end_date)` |
| get_gantt_data | _task_to_gantt | 175 | `_task_to_gantt(task, iteration.end_date)` |
| _task_to_gantt | attributes.instance_state | 253 | `attributes.instance_state(task)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `gantt_tasks.append` | `get_gantt_data` | 178 |
| mutation | `overdue_ids.append` | `get_gantt_data` | 181 |
| mutation | `overdue_ids.append` | `get_gantt_data` | 186 |
| mutation | `vacation_dates.update` | `get_gantt_data` | 205 |
| mutation | `assignees.append` | `_task_to_gantt` | 297 |
| mutation | `seen_ids.add` | `_task_to_gantt` | 300 |
| mutation | `children.append` | `_task_to_gantt` | 332 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `get_gantt_data` | `iteration_service.get_by_id` | 151 |
| unresolved_call | `get_gantt_data` | `task_service.get_by_iteration` | 152 |
| unresolved_call | `get_gantt_data` | `team_service.get_by_iteration` | 153 |
| external_call | `get_gantt_data` | `HTTPException` | 156 |
| unresolved_call | `get_gantt_data` | `calendar_service.calculate_working_days` | 163 |
| external_call | `_task_to_gantt` | `attributes.instance_state` | 253 |
| step_limit | `get_gantt_data` | `first 12 steps` | 0 |

## Behavior

This flow starts at `get_gantt_data` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

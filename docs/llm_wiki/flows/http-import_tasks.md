# import_tasks

**Entry point:** `import_tasks` (`http`)
**Source:** [tasks](../modules/tasks.md)
**Modules touched:** [iteration_service](../modules/iteration_service.md), [schemas_task](../modules/schemas_task.md), [tasks](../modules/tasks.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as import_tasks
    participant p1 as IterationService
    participant p2 as iteration_service.get_by_id
    participant p3 as HTTPException
    participant p4 as service.import_tasks
    participant p5 as TasksImportResponse
    participant p6 as len
    participant p7 as service.task_to_response
    participant p8 as TaskImportTriageItemResponse.model_validate
    participant p9 as str
    p0->>p1: IterationService
    p0-->>p2: iteration_service.get_by_id
    p0-->>p3: HTTPException
    p0-->>p4: service.import_tasks
    p0->>p5: TasksImportResponse
    p0-->>p6: len
    p0-->>p6: len
    p0-->>p6: len
    p0-->>p6: len
    p0-->>p7: service.task_to_response
    p0-->>p8: TaskImportTriageItemResponse.model_validate
    p0-->>p3: HTTPException
    p0-->>p9: str
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. import_tasks"]
    s2["2. IterationService"]
    s3["3. iteration_service.get_by_id"]
    s4["4. HTTPException"]
    s5["5. service.import_tasks"]
    s6["6. TasksImportResponse"]
    s7["7. len"]
    s8["8. len"]
    s9["9. len"]
    s10["10. len"]
    s11["11. service.task_to_response"]
    s12["12. TaskImportTriageItemResponse.model_validate"]
    s1 -->|"IterationService(db)"| s2
    s1 -. "iteration_service.get_by_id(iteration_id)" .-> s3
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s4
    s1 -. "service.import_tasks(iteration_id, data.text, data.destination)" .-> s5
    s1 -->|"TasksImportResponse(imported_count=..., task_count=len(...), triage_count=len(...), tasks=..., triage_items=...)"| s6
    s1 -. "len(tasks)" .-> s7
    s1 -. "len(triage_items)" .-> s8
    s1 -. "len(tasks)" .-> s9
    s1 -. "len(triage_items)" .-> s10
    s1 -. "service.task_to_response(t, iteration.end_date)" .-> s11
    s1 -. "TaskImportTriageItemResponse.model_validate(item)" .-> s12
    click s1 "../modules/tasks.md"
    click s2 "../modules/iteration_service.md"
    click s6 "../modules/schemas_task.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `import_tasks` | `iteration_id: int`, `data: TasksImportRequest`, `service: Annotated[TaskService, Depends(get_task_service)]`, `db: Annotated[AsyncSession, Depends(get_db)]` | `status`, `status` | - | `TasksImportResponse(...)` |
| `IterationService` | - | - | - | - |
| `iteration_service.get_by_id` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `service.import_tasks` | - | - | - | - |
| `TasksImportResponse` | - | - | - | - |
| `len` | - | - | - | - |
| `len` | - | - | - | - |
| `len` | - | - | - | - |
| `len` | - | - | - | - |
| `service.task_to_response` | - | - | - | - |
| `TaskImportTriageItemResponse.model_validate` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| import_tasks | IterationService | 770 | `IterationService(db)` |
| import_tasks | iteration_service.get_by_id | 771 | `iteration_service.get_by_id(iteration_id)` |
| import_tasks | HTTPException | 774 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| import_tasks | service.import_tasks | 780 | `service.import_tasks(iteration_id, data.text, data.destination)` |
| import_tasks | TasksImportResponse | 785 | `TasksImportResponse(imported_count=..., task_count=len(...), triage_count=len(...), tasks=..., triage_items=...)` |
| import_tasks | len | 786 | `len(tasks)` |
| import_tasks | len | 786 | `len(triage_items)` |
| import_tasks | len | 787 | `len(tasks)` |
| import_tasks | len | 788 | `len(triage_items)` |
| import_tasks | service.task_to_response | 789 | `service.task_to_response(t, iteration.end_date)` |
| import_tasks | TaskImportTriageItemResponse.model_validate | 791 | `TaskImportTriageItemResponse.model_validate(item)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `import_tasks` | `iteration_service.get_by_id` | 771 |
| external_call | `import_tasks` | `HTTPException` | 774 |
| unresolved_call | `import_tasks` | `service.import_tasks` | 780 |
| unresolved_call | `import_tasks` | `service.task_to_response` | 789 |
| unresolved_call | `import_tasks` | `TaskImportTriageItemResponse.model_validate` | 791 |
| step_limit | `import_tasks` | `first 12 steps` | 0 |

## Behavior

This flow starts at `import_tasks` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

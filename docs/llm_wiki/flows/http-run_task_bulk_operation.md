# run_task_bulk_operation

**Entry point:** `run_task_bulk_operation` (`http`)
**Source:** [tasks](../modules/tasks.md)
**Modules touched:** [tasks](../modules/tasks.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as run_task_bulk_operation
    participant p1 as service.run
    p0-->>p1: service.run
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. run_task_bulk_operation"]
    s2["2. service.run"]
    s1 -. "service.run(data)" .-> s2
    click s1 "../modules/tasks.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `run_task_bulk_operation` | `data: TaskBulkOperationRequest`, `service: Annotated[TaskBulkOperationService, Depends(get_task_bulk_operation_service)]` | - | - | `...` |
| `service.run` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| run_task_bulk_operation | service.run | 277 | `service.run(data)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `run_task_bulk_operation` | `service.run` | 277 |

## Behavior

This flow starts at `run_task_bulk_operation` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

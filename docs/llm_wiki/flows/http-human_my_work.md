# human_my_work

**Entry point:** `human_my_work` (`http`)
**Source:** [routers_task_domain](../modules/routers_task_domain.md)
**Modules touched:** [routers_task_domain](../modules/routers_task_domain.md), [task_detail_service](../modules/task_detail_service.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as human_my_work
    participant p1 as TaskDetailService(…).my_work
    participant p2 as TaskDetailService
    participant p3 as HTTPException
    participant p4 as str
    p0-->>p1: TaskDetailService(…).my_work
    p0->>p2: TaskDetailService
    p0-->>p3: HTTPException
    p0-->>p4: str
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. human_my_work"]
    s2["2. TaskDetailService(…).my_work"]
    s3["3. TaskDetailService"]
    s4["4. HTTPException"]
    s5["5. str"]
    s1 -. "TaskDetailService(…).my_work(limit=limit, after_id=after_id, project_id=project_id, iteration_id=iteration_id, backlog_only=backlog_only)" .-> s2
    s1 -->|"TaskDetailService(db)"| s3
    s1 -. "HTTPException(422, detail=[...])" .-> s4
    s1 -. "str(exc)" .-> s5
    click s1 "../modules/routers_task_domain.md"
    click s3 "../modules/task_detail_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `human_my_work` | `db: DB`, `limit: int`, `after_id: int`, `project_id: int \| None`, `iteration_id: int \| None`, `backlog_only: bool` | - | - | `...` |
| `TaskDetailService(…).my_work` | - | - | - | - |
| `TaskDetailService` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| human_my_work | TaskDetailService(…).my_work | 77 | `TaskDetailService(db).my_work(limit=limit, after_id=after_id, project_id=project_id, iteration_id=iteration_id, backlog_only=backlog_only)` |
| human_my_work | TaskDetailService | 77 | `TaskDetailService(db)` |
| human_my_work | HTTPException | 80 | `HTTPException(422, detail=[...])` |
| human_my_work | str | 80 | `str(exc)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `human_my_work` | `TaskDetailService(db).my_work` | 77 |
| external_call | `human_my_work` | `HTTPException` | 80 |

## Behavior

Returns authenticated ownership queues across visible projects, including nested/backlog work. Optional project, iteration and backlog filters apply before cursor pagination; incompatible iteration/backlog selection fails explicitly. Missing profile or membership is explicit. Page cursors are live observations rather than a frozen complete inventory.

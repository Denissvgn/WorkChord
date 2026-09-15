# formalize_task

**Entry point:** `formalize_task` (`http`)
**Source:** [routers_llm](../modules/routers_llm.md)
**Modules touched:** [routers_llm](../modules/routers_llm.md), [task_service](../modules/task_service.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as formalize_task
    participant p1 as TaskService
    participant p2 as task_service.get_by_id
    participant p3 as HTTPException
    participant p4 as db.rollback
    participant p5 as llm_service.formalize_task
    p0->>p1: TaskService
    p0-->>p2: task_service.get_by_id
    p0-->>p3: HTTPException
    p0-->>p4: db.rollback
    p0-->>p5: llm_service.formalize_task
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. formalize_task"]
    s2["2. TaskService"]
    s3["3. task_service.get_by_id"]
    s4["4. HTTPException"]
    s5["5. db.rollback"]
    s6["6. llm_service.formalize_task"]
    s1 -->|"TaskService(db)"| s2
    s1 -. "task_service.get_by_id(task_id)" .-> s3
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s4
    s1 -. "db.rollback(data not statically known)" .-> s5
    s1 -. "llm_service.formalize_task(title=title, description=description, context=data.context)" .-> s6
    click s1 "../modules/routers_llm.md"
    click s2 "../modules/task_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `formalize_task` | `task_id: int`, `data: FormalizeRequest`, `db: Annotated[AsyncSession, Depends(get_db, scope='function')]`, `llm_service: Annotated[LLMService, Depends(get_llm_service)]` | `status` | - | `...` |
| `TaskService` | - | - | - | - |
| `task_service.get_by_id` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `db.rollback` | - | - | - | - |
| `llm_service.formalize_task` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| formalize_task | TaskService | 178 | `TaskService(db)` |
| formalize_task | task_service.get_by_id | 179 | `task_service.get_by_id(task_id)` |
| formalize_task | HTTPException | 182 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| formalize_task | db.rollback | 189 | `db.rollback(data not statically known)` |
| formalize_task | llm_service.formalize_task | 190 | `llm_service.formalize_task(title=title, description=description, context=data.context)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `formalize_task` | `task_service.get_by_id` | 179 |
| external_call | `formalize_task` | `HTTPException` | 182 |
| unresolved_call | `formalize_task` | `db.rollback` | 189 |
| unresolved_call | `formalize_task` | `llm_service.formalize_task` | 190 |

## Behavior

This flow starts at `formalize_task` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

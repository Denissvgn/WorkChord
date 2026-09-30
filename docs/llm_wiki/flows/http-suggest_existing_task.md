# suggest_existing_task

**Entry point:** `suggest_existing_task` (`http`)
**Source:** [routers_llm](../modules/routers_llm.md)
**Modules touched:** [routers_llm](../modules/routers_llm.md), [task_service](../modules/task_service.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as suggest_existing_task
    participant p1 as TaskService
    participant p2 as task_service.get_by_id
    participant p3 as HTTPException
    participant p4 as _task_ai_context_pack
    participant p5 as data.model_dump
    participant p6 as context.update
    participant p7 as db.get
    participant p8 as db.execute
    participant p9 as select(…).where
    participant p10 as select
    participant p11 as Task.id.in_
    participant p12 as result.scalars().all
    participant p13 as result.scalars
    participant p14 as db.rollback
    participant p15 as llm_service.suggest_task
    p0->>p1: TaskService
    p0-->>p2: task_service.get_by_id
    p0-->>p3: HTTPException
    p0->>p4: _task_ai_context_pack
    p4-->>p5: data.model_dump
    p4-->>p6: context.update
    p4-->>p7: db.get
    p4-->>p7: db.get
    p4-->>p7: db.get
    p4-->>p8: db.execute
    p4-->>p9: select(…).where
    p4-->>p10: select
    p4-->>p11: Task.id.in_
    p4-->>p12: result.scalars().all
    p4-->>p13: result.scalars
    p0-->>p14: db.rollback
    p0-->>p15: llm_service.suggest_task
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. suggest_existing_task"]
    s2["2. TaskService"]
    s3["3. task_service.get_by_id"]
    s4["4. HTTPException"]
    s5["5. _task_ai_context_pack"]
    s6["6. data.model_dump"]
    s7["7. context.update"]
    s8["8. db.get"]
    s9["9. db.get"]
    s10["10. db.get"]
    s11["11. db.execute"]
    s12["12. select(…).where"]
    s1 -->|"TaskService(db)"| s2
    s1 -. "task_service.get_by_id(task_id)" .-> s3
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s4
    s1 -->|"_task_ai_context_pack(db, data, task=task)"| s5
    s5 -. "data.model_dump(data not statically known)" .-> s6
    s5 -. "context.update({...})" .-> s7
    s5 -. "db.get(Project, project_id)" .-> s8
    s5 -. "db.get(ProjectMilestone, milestone_id)" .-> s9
    s5 -. "db.get(WorkTemplate, data.template_id)" .-> s10
    s5 -. "db.execute(...)" .-> s11
    s5 -. "select(…).where(Task.id.in_(...))" .-> s12
    b0["mutation context.update"]
    s5 -. "mutation context.update" .-> b0
    click s1 "../modules/routers_llm.md"
    click s2 "../modules/task_service.md"
    click s5 "../modules/routers_llm.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `suggest_existing_task` | `task_id: int`, `data: TaskAISuggestRequest`, `db: Annotated[AsyncSession, Depends(get_db, scope='function')]`, `llm_service: Annotated[LLMService, Depends(get_llm_service)]` | `status` | - | `...` |
| `TaskService` | - | - | - | - |
| `task_service.get_by_id` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `_task_ai_context_pack` | `db: AsyncSession`, `data: TaskAISuggestRequest`, `task: Task \| None` | `Project`, `ProjectMilestone`, `WorkTemplate` | `context[...]`, `context[...]`, `context[...]`, `context[...]` | `context` |
| `data.model_dump` | - | - | - | - |
| `context.update` | - | - | - | - |
| `db.get` | - | - | - | - |
| `db.get` | - | - | - | - |
| `db.get` | - | - | - | - |
| `db.execute` | - | - | - | - |
| `select(…).where` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| suggest_existing_task | TaskService | 230 | `TaskService(db)` |
| suggest_existing_task | task_service.get_by_id | 231 | `task_service.get_by_id(task_id)` |
| suggest_existing_task | HTTPException | 233 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| suggest_existing_task | _task_ai_context_pack | 237 | `_task_ai_context_pack(db, data, task=task)` |
| _task_ai_context_pack | data.model_dump | 41 | `data.model_dump(data not statically known)` |
| _task_ai_context_pack | context.update | 49 | `context.update({...})` |
| _task_ai_context_pack | db.get | 64 | `db.get(Project, project_id)` |
| _task_ai_context_pack | db.get | 77 | `db.get(ProjectMilestone, milestone_id)` |
| _task_ai_context_pack | db.get | 89 | `db.get(WorkTemplate, data.template_id)` |
| _task_ai_context_pack | db.execute | 105 | `db.execute(...)` |
| _task_ai_context_pack | select(…).where | 105 | `select(Task).where(Task.id.in_(...))` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `context.update` | `_task_ai_context_pack` | 49 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `suggest_existing_task` | `task_service.get_by_id` | 231 |
| external_call | `suggest_existing_task` | `HTTPException` | 233 |
| unresolved_call | `_task_ai_context_pack` | `data.model_dump` | 41 |
| unresolved_call | `_task_ai_context_pack` | `db.get` | 64 |
| unresolved_call | `_task_ai_context_pack` | `db.get` | 77 |
| unresolved_call | `_task_ai_context_pack` | `db.get` | 89 |
| unresolved_call | `_task_ai_context_pack` | `db.execute` | 105 |
| unresolved_call | `_task_ai_context_pack` | `select(Task).where` | 105 |
| step_limit | `suggest_existing_task` | `first 12 steps` | 0 |

## Behavior

This flow starts at `suggest_existing_task` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

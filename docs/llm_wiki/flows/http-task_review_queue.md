# task_review_queue

**Entry point:** `task_review_queue` (`http`)
**Source:** [routers_task_domain](../modules/routers_task_domain.md)
**Modules touched:** [routers_task_domain](../modules/routers_task_domain.md), [task_detail_service](../modules/task_detail_service.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as task_review_queue
    participant p1 as db.info.get
    participant p2 as TaskDetailService
    participant p3 as service.references().where
    participant p4 as service.references
    participant p5 as Task.canceled_at.is_
    participant p6 as Task.is_summary.is_
    participant p7 as query.where
    participant p8 as Task.project_id.in_
    participant p9 as authority.allows
    participant p10 as or_
    participant p11 as Task.executed_by_principal_id.is_
    participant p12 as select(…).where(…).exists
    participant p13 as select(…).where
    participant p14 as select
    participant p15 as service.page
    p0-->>p1: db.info.get
    p0->>p2: TaskDetailService
    p0-->>p3: service.references().where
    p0-->>p4: service.references
    p0-->>p5: Task.canceled_at.is_
    p0-->>p6: Task.is_summary.is_
    p0-->>p7: query.where
    p0-->>p8: Task.project_id.in_
    p0-->>p9: authority.allows
    p0-->>p7: query.where
    p0-->>p10: or_
    p0-->>p11: Task.executed_by_principal_id.is_
    p0-->>p12: select(…).where(…).exists
    p0-->>p13: select(…).where
    p0-->>p14: select
    p0-->>p7: query.where
    p0-->>p15: service.page
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. task_review_queue"]
    s2["2. db.info.get"]
    s3["3. TaskDetailService"]
    s4["4. service.references().where"]
    s5["5. service.references"]
    s6["6. Task.canceled_at.is_"]
    s7["7. Task.is_summary.is_"]
    s8["8. query.where"]
    s9["9. Task.project_id.in_"]
    s10["10. authority.allows"]
    s11["11. query.where"]
    s12["12. or_"]
    s1 -. "db.info.get('authority')" .-> s2
    s1 -->|"TaskDetailService(db)"| s3
    s1 -. "service.references().where(..., Task.canceled_at.is_(...), Task.is_summary.is_(...))" .-> s4
    s1 -. "service.references(data not statically known)" .-> s5
    s1 -. "Task.canceled_at.is_(None)" .-> s6
    s1 -. "Task.is_summary.is_(False)" .-> s7
    s1 -. "query.where(Task.project_id.in_(...))" .-> s8
    s1 -. "Task.project_id.in_(...)" .-> s9
    s1 -. "authority.allows(project_id, 'review')" .-> s10
    s1 -. "query.where(or_(...))" .-> s11
    s1 -. "or_(Task.executed_by_principal_id.is_(...), ...)" .-> s12
    click s1 "../modules/routers_task_domain.md"
    click s3 "../modules/task_detail_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `task_review_queue` | `db: DB`, `limit: int`, `after_id: int` | `Task`, `Task` | - | `...` |
| `db.info.get` | - | - | - | - |
| `TaskDetailService` | - | - | - | - |
| `service.references().where` | - | - | - | - |
| `service.references` | - | - | - | - |
| `Task.canceled_at.is_` | - | - | - | - |
| `Task.is_summary.is_` | - | - | - | - |
| `query.where` | - | - | - | - |
| `Task.project_id.in_` | - | - | - | - |
| `authority.allows` | - | - | - | - |
| `query.where` | - | - | - | - |
| `or_` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| task_review_queue | db.info.get | 86 | `db.info.get('authority')` |
| task_review_queue | TaskDetailService | 87 | `TaskDetailService(db)` |
| task_review_queue | service.references().where | 88 | `service.references().where(..., Task.canceled_at.is_(...), Task.is_summary.is_(...))` |
| task_review_queue | service.references | 88 | `service.references(data not statically known)` |
| task_review_queue | Task.canceled_at.is_ | 88 | `Task.canceled_at.is_(None)` |
| task_review_queue | Task.is_summary.is_ | 88 | `Task.is_summary.is_(False)` |
| task_review_queue | query.where | 91 | `query.where(Task.project_id.in_(...))` |
| task_review_queue | Task.project_id.in_ | 91 | `Task.project_id.in_(...)` |
| task_review_queue | authority.allows | 91 | `authority.allows(project_id, 'review')` |
| task_review_queue | query.where | 93 | `query.where(or_(...))` |
| task_review_queue | or_ | 93 | `or_(Task.executed_by_principal_id.is_(...), ...)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `task_review_queue` | `db.info.get` | 86 |
| unresolved_call | `task_review_queue` | `service.references().where` | 88 |
| unresolved_call | `task_review_queue` | `service.references` | 88 |
| unresolved_call | `task_review_queue` | `Task.canceled_at.is_` | 88 |
| unresolved_call | `task_review_queue` | `Task.is_summary.is_` | 88 |
| unresolved_call | `task_review_queue` | `query.where` | 91 |
| unresolved_call | `task_review_queue` | `Task.project_id.in_` | 91 |
| unresolved_call | `task_review_queue` | `authority.allows` | 91 |
| unresolved_call | `task_review_queue` | `query.where` | 93 |
| external_call | `task_review_queue` | `or_` | 93 |
| step_limit | `task_review_queue` | `first 12 steps` | 0 |

## Behavior

This flow starts at `task_review_queue` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

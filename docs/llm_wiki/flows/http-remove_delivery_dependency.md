# remove_delivery_dependency

**Entry point:** `remove_delivery_dependency` (`http`)
**Source:** [delivery_dependencies](../modules/delivery_dependencies.md)
**Modules touched:** [delivery_dependencies](../modules/delivery_dependencies.md), [delivery_dependency_service](../modules/delivery_dependency_service.md), [routers_task_domain](../modules/routers_task_domain.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as remove_delivery_dependency
    participant p1 as domain_result
    participant p2 as HTTPException
    participant p3 as exc.detail
    participant p4 as str
    participant p5 as DeliveryDependencyService(…).remove
    participant p6 as DeliveryDependencyService
    p0->>p1: domain_result
    p1-->>p2: HTTPException
    p1-->>p3: exc.detail
    p1-->>p2: HTTPException
    p1-->>p4: str
    p1-->>p2: HTTPException
    p1-->>p4: str
    p1-->>p2: HTTPException
    p0-->>p5: DeliveryDependencyService(…).remove
    p0->>p6: DeliveryDependencyService
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. remove_delivery_dependency"]
    s2["2. domain_result"]
    s3["3. HTTPException"]
    s4["4. exc.detail"]
    s5["5. HTTPException"]
    s6["6. str"]
    s7["7. HTTPException"]
    s8["8. str"]
    s9["9. HTTPException"]
    s10["10. DeliveryDependencyService(…).remove"]
    s11["11. DeliveryDependencyService"]
    s1 -->|"domain_result(...)"| s2
    s2 -. "HTTPException(409, detail=exc.detail(...))" .-> s3
    s2 -. "exc.detail(data not statically known)" .-> s4
    s2 -. "HTTPException(404, detail=str(...))" .-> s5
    s2 -. "str(exc)" .-> s6
    s2 -. "HTTPException(422, detail=[...])" .-> s7
    s2 -. "str(exc)" .-> s8
    s2 -. "HTTPException(404, detail='Task not found or inaccessible')" .-> s9
    s1 -. "DeliveryDependencyService(…).remove(task_id, edge_id, expected_version)" .-> s10
    s1 -->|"DeliveryDependencyService(db)"| s11
    click s1 "../modules/delivery_dependencies.md"
    click s2 "../modules/routers_task_domain.md"
    click s11 "../modules/delivery_dependency_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `remove_delivery_dependency` | `task_id: int`, `edge_id: int`, `db: DeliveryDatabase`, `expected_version: int` | - | - | `...` |
| `domain_result` | `awaitable` | `TaskVersionConflictError` | - | `result` |
| `HTTPException` | - | - | - | - |
| `exc.detail` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `DeliveryDependencyService(…).remove` | - | - | - | - |
| `DeliveryDependencyService` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| remove_delivery_dependency | domain_result | 35 | `domain_result(...)` |
| domain_result | HTTPException | 42 | `HTTPException(409, detail=exc.detail(...))` |
| domain_result | exc.detail | 42 | `exc.detail(data not statically known)` |
| domain_result | HTTPException | 44 | `HTTPException(404, detail=str(...))` |
| domain_result | str | 44 | `str(exc)` |
| domain_result | HTTPException | 46 | `HTTPException(422, detail=[...])` |
| domain_result | str | 46 | `str(exc)` |
| domain_result | HTTPException | 48 | `HTTPException(404, detail='Task not found or inaccessible')` |
| remove_delivery_dependency | DeliveryDependencyService(…).remove | 35 | `DeliveryDependencyService(db).remove(task_id, edge_id, expected_version)` |
| remove_delivery_dependency | DeliveryDependencyService | 35 | `DeliveryDependencyService(db)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `domain_result` | `HTTPException` | 42 |
| unresolved_call | `domain_result` | `exc.detail` | 42 |
| external_call | `domain_result` | `HTTPException` | 44 |
| external_call | `domain_result` | `HTTPException` | 46 |
| external_call | `domain_result` | `HTTPException` | 48 |
| unresolved_call | `remove_delivery_dependency` | `DeliveryDependencyService(db).remove` | 35 |

## Behavior

Uses the dependent task’s current version and edit permission. An inaccessible target can still be unlinked by an authorized dependent-task editor. Actual changes invalidate execution evidence and downstream context in the owning transaction.

# list_delivery_dependencies

**Entry point:** `list_delivery_dependencies` (`http`)
**Source:** [delivery_dependencies](../modules/delivery_dependencies.md)
**Modules touched:** [delivery_dependencies](../modules/delivery_dependencies.md), [delivery_dependency_service](../modules/delivery_dependency_service.md), [routers_task_domain](../modules/routers_task_domain.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as list_delivery_dependencies
    participant p1 as domain_result
    participant p2 as HTTPException
    participant p3 as exc.detail
    participant p4 as str
    participant p5 as DeliveryDependencyService(…).projection
    participant p6 as DeliveryDependencyService
    p0->>p1: domain_result
    p1-->>p2: HTTPException
    p1-->>p3: exc.detail
    p1-->>p2: HTTPException
    p1-->>p4: str
    p1-->>p2: HTTPException
    p0-->>p5: DeliveryDependencyService(…).projection
    p0->>p6: DeliveryDependencyService
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. list_delivery_dependencies"]
    s2["2. domain_result"]
    s3["3. HTTPException"]
    s4["4. exc.detail"]
    s5["5. HTTPException"]
    s6["6. str"]
    s7["7. HTTPException"]
    s8["8. DeliveryDependencyService(…).projection"]
    s9["9. DeliveryDependencyService"]
    s1 -->|"domain_result(...)"| s2
    s2 -. "HTTPException(409, detail=exc.detail(...))" .-> s3
    s2 -. "exc.detail(data not statically known)" .-> s4
    s2 -. "HTTPException(422, detail=[...])" .-> s5
    s2 -. "str(exc)" .-> s6
    s2 -. "HTTPException(404, detail='Task not found or inaccessible')" .-> s7
    s1 -. "DeliveryDependencyService(…).projection(task_id)" .-> s8
    s1 -->|"DeliveryDependencyService(db)"| s9
    click s1 "../modules/delivery_dependencies.md"
    click s2 "../modules/routers_task_domain.md"
    click s9 "../modules/delivery_dependency_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `list_delivery_dependencies` | `task_id: int`, `db: DeliveryDatabase` | - | - | `...` |
| `domain_result` | `awaitable` | `TaskVersionConflictError` | - | `result` |
| `HTTPException` | - | - | - | - |
| `exc.detail` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `DeliveryDependencyService(…).projection` | - | - | - | - |
| `DeliveryDependencyService` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| list_delivery_dependencies | domain_result | 25 | `domain_result(...)` |
| domain_result | HTTPException | 29 | `HTTPException(409, detail=exc.detail(...))` |
| domain_result | exc.detail | 29 | `exc.detail(data not statically known)` |
| domain_result | HTTPException | 31 | `HTTPException(422, detail=[...])` |
| domain_result | str | 31 | `str(exc)` |
| domain_result | HTTPException | 33 | `HTTPException(404, detail='Task not found or inaccessible')` |
| list_delivery_dependencies | DeliveryDependencyService(…).projection | 25 | `DeliveryDependencyService(db).projection(task_id)` |
| list_delivery_dependencies | DeliveryDependencyService | 25 | `DeliveryDependencyService(db)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `domain_result` | `HTTPException` | 29 |
| unresolved_call | `domain_result` | `exc.detail` | 29 |
| external_call | `domain_result` | `HTTPException` | 31 |
| external_call | `domain_result` | `HTTPException` | 33 |
| unresolved_call | `list_delivery_dependencies` | `DeliveryDependencyService(db).projection` | 25 |

## Behavior

Shows current delivery readiness for an authorized task. A target must have current attributed acceptance; hidden or missing targets expose a generic unavailable blocker without target identity or status.

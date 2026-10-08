# restore_backlog

**Entry point:** `restore_backlog` (`http`)
**Source:** [routers_task_domain](../modules/routers_task_domain.md)
**Modules touched:** [backlog_snapshot_service](../modules/backlog_snapshot_service.md), [routers_task_domain](../modules/routers_task_domain.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as restore_backlog
    participant p1 as domain_result
    participant p2 as HTTPException
    participant p3 as exc.detail
    participant p4 as str
    participant p5 as BacklogSnapshotService(…).restore
    participant p6 as BacklogSnapshotService
    p0->>p1: domain_result
    p1-->>p2: HTTPException
    p1-->>p3: exc.detail
    p1-->>p2: HTTPException
    p1-->>p4: str
    p1-->>p2: HTTPException
    p1-->>p4: str
    p1-->>p2: HTTPException
    p0-->>p5: BacklogSnapshotService(…).restore
    p0->>p6: BacklogSnapshotService
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. restore_backlog"]
    s2["2. domain_result"]
    s3["3. HTTPException"]
    s4["4. exc.detail"]
    s5["5. HTTPException"]
    s6["6. str"]
    s7["7. HTTPException"]
    s8["8. str"]
    s9["9. HTTPException"]
    s10["10. BacklogSnapshotService(…).restore"]
    s11["11. BacklogSnapshotService"]
    s1 -->|"domain_result(...)"| s2
    s2 -. "HTTPException(409, detail=exc.detail(...))" .-> s3
    s2 -. "exc.detail(data not statically known)" .-> s4
    s2 -. "HTTPException(404, detail=str(...))" .-> s5
    s2 -. "str(exc)" .-> s6
    s2 -. "HTTPException(422, detail=[...])" .-> s7
    s2 -. "str(exc)" .-> s8
    s2 -. "HTTPException(404, detail='Task not found or inaccessible')" .-> s9
    s1 -. "BacklogSnapshotService(…).restore(project_id, snapshot_id, data.expected_versions, reason=data.reason)" .-> s10
    s1 -->|"BacklogSnapshotService(db)"| s11
    click s1 "../modules/routers_task_domain.md"
    click s2 "../modules/routers_task_domain.md"
    click s11 "../modules/backlog_snapshot_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `restore_backlog` | `project_id: int`, `snapshot_id: int`, `data: BacklogRestoreRequest`, `db: DB` | - | - | `...` |
| `domain_result` | `awaitable` | `TaskVersionConflictError` | - | `result` |
| `HTTPException` | - | - | - | - |
| `exc.detail` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `BacklogSnapshotService(…).restore` | - | - | - | - |
| `BacklogSnapshotService` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| restore_backlog | domain_result | 246 | `domain_result(...)` |
| domain_result | HTTPException | 42 | `HTTPException(409, detail=exc.detail(...))` |
| domain_result | exc.detail | 42 | `exc.detail(data not statically known)` |
| domain_result | HTTPException | 44 | `HTTPException(404, detail=str(...))` |
| domain_result | str | 44 | `str(exc)` |
| domain_result | HTTPException | 46 | `HTTPException(422, detail=[...])` |
| domain_result | str | 46 | `str(exc)` |
| domain_result | HTTPException | 48 | `HTTPException(404, detail='Task not found or inaccessible')` |
| restore_backlog | BacklogSnapshotService(…).restore | 246 | `BacklogSnapshotService(db).restore(project_id, snapshot_id, data.expected_versions, reason=data.reason)` |
| restore_backlog | BacklogSnapshotService | 246 | `BacklogSnapshotService(db)` |

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
| unresolved_call | `restore_backlog` | `BacklogSnapshotService(db).restore` | 246 |

## Behavior

This flow starts at `restore_backlog` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

Scheduled and backlog restoration share a version allocator under the owning scope lock. It advances above the saved version, live task, retained history and durable deletion fence. Current progress and acceptance are cleared; immutable history survives. A deleted task without a reliable deletion fence returns snapshot_version_history_unknown (409), requiring recovery from a complete matching database backup.

Delivery prerequisites survive scoped recovery; removing a referenced target requires explicit unlinking. Original task identity makes retained discussion readable again after restoration.

# list_snapshots

**Entry point:** `list_snapshots` (`http`)
**Source:** [snapshots](../modules/snapshots.md)
**Modules touched:** [iteration_service](../modules/iteration_service.md), [snapshot_service](../modules/snapshot_service.md), [snapshots](../modules/snapshots.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as list_snapshots
    participant p1 as IterationService
    participant p2 as iteration_service.get_by_id
    participant p3 as HTTPException
    participant p4 as SnapshotService
    participant p5 as snapshot_service.list_snapshots
    participant p6 as str
    p0->>p1: IterationService
    p0-->>p2: iteration_service.get_by_id
    p0-->>p3: HTTPException
    p0->>p4: SnapshotService
    p0-->>p5: snapshot_service.list_snapshots
    p0-->>p3: HTTPException
    p0-->>p6: str
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. list_snapshots"]
    s2["2. IterationService"]
    s3["3. iteration_service.get_by_id"]
    s4["4. HTTPException"]
    s5["5. SnapshotService"]
    s6["6. snapshot_service.list_snapshots"]
    s7["7. HTTPException"]
    s8["8. str"]
    s1 -->|"IterationService(db)"| s2
    s1 -. "iteration_service.get_by_id(iteration_id)" .-> s3
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s4
    s1 -->|"SnapshotService(db)"| s5
    s1 -. "snapshot_service.list_snapshots(iteration_id)" .-> s6
    s1 -. "HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))" .-> s7
    s1 -. "str(exc)" .-> s8
    click s1 "../modules/snapshots.md"
    click s2 "../modules/iteration_service.md"
    click s5 "../modules/snapshot_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `list_snapshots` | `iteration_id: int`, `db: Annotated[AsyncSession, Depends(get_db)]` | `status`, `SnapshotPathError`, `status` | - | `snapshot_service.list_snapshots(...)` |
| `IterationService` | - | - | - | - |
| `iteration_service.get_by_id` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `SnapshotService` | - | - | - | - |
| `snapshot_service.list_snapshots` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| list_snapshots | IterationService | 188 | `IterationService(db)` |
| list_snapshots | iteration_service.get_by_id | 189 | `iteration_service.get_by_id(iteration_id)` |
| list_snapshots | HTTPException | 192 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| list_snapshots | SnapshotService | 197 | `SnapshotService(db)` |
| list_snapshots | snapshot_service.list_snapshots | 199 | `snapshot_service.list_snapshots(iteration_id)` |
| list_snapshots | HTTPException | 201 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))` |
| list_snapshots | str | 201 | `str(exc)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `list_snapshots` | `iteration_service.get_by_id` | 189 |
| external_call | `list_snapshots` | `HTTPException` | 192 |
| unresolved_call | `list_snapshots` | `snapshot_service.list_snapshots` | 199 |
| external_call | `list_snapshots` | `HTTPException` | 201 |

## Behavior

This flow starts at `list_snapshots` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

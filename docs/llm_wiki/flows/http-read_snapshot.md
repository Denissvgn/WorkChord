# read_snapshot

**Entry point:** `read_snapshot` (`http`)
**Source:** [snapshots](../modules/snapshots.md)
**Modules touched:** [snapshot_service](../modules/snapshot_service.md), [snapshots](../modules/snapshots.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as read_snapshot
    participant p1 as SnapshotService(…).get_snapshot
    participant p2 as SnapshotService
    participant p3 as HTTPException
    p0-->>p1: SnapshotService(…).get_snapshot
    p0->>p2: SnapshotService
    p0-->>p3: HTTPException
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. read_snapshot"]
    s2["2. SnapshotService(…).get_snapshot"]
    s3["3. SnapshotService"]
    s4["4. HTTPException"]
    s1 -. "SnapshotService(…).get_snapshot(iteration_id, filename)" .-> s2
    s1 -->|"SnapshotService(db)"| s3
    s1 -. "HTTPException(status_code=404, detail='Snapshot not found or inaccessible')" .-> s4
    click s1 "../modules/snapshots.md"
    click s3 "../modules/snapshot_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `read_snapshot` | `iteration_id: int`, `filename: str`, `db: Annotated[AsyncSession, Depends(get_db, scope='function')]` | - | - | `payload` |
| `SnapshotService(…).get_snapshot` | - | - | - | - |
| `SnapshotService` | - | - | - | - |
| `HTTPException` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| read_snapshot | SnapshotService(…).get_snapshot | 283 | `SnapshotService(db).get_snapshot(iteration_id, filename)` |
| read_snapshot | SnapshotService | 283 | `SnapshotService(db)` |
| read_snapshot | HTTPException | 285 | `HTTPException(status_code=404, detail='Snapshot not found or inaccessible')` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `read_snapshot` | `SnapshotService(db).get_snapshot` | 283 |
| external_call | `read_snapshot` | `HTTPException` | 285 |

## Behavior

This flow starts at `read_snapshot` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

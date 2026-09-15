# restore_snapshot

**Entry point:** `restore_snapshot` (`http`)
**Source:** [snapshots](../modules/snapshots.md)
**Modules touched:** [iteration_service](../modules/iteration_service.md), [snapshot_service](../modules/snapshot_service.md), [snapshots](../modules/snapshots.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as restore_snapshot
    participant p1 as HTTPException
    participant p2 as IterationService
    participant p3 as iteration_service.get_by_id
    participant p4 as SnapshotService(…).restore
    participant p5 as SnapshotService
    participant p6 as str
    p0-->>p1: HTTPException
    p0->>p2: IterationService
    p0-->>p3: iteration_service.get_by_id
    p0-->>p1: HTTPException
    p0-->>p4: SnapshotService(…).restore
    p0->>p5: SnapshotService
    p0-->>p1: HTTPException
    p0-->>p6: str
    p0-->>p1: HTTPException
    p0-->>p6: str
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. restore_snapshot"]
    s2["2. HTTPException"]
    s3["3. IterationService"]
    s4["4. iteration_service.get_by_id"]
    s5["5. HTTPException"]
    s6["6. SnapshotService(…).restore"]
    s7["7. SnapshotService"]
    s8["8. HTTPException"]
    s9["9. str"]
    s10["10. HTTPException"]
    s11["11. str"]
    s1 -. "HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Snapshot restore requires confirm=true.')" .-> s2
    s1 -->|"IterationService(db)"| s3
    s1 -. "iteration_service.get_by_id(iteration_id)" .-> s4
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s5
    s1 -. "SnapshotService(…).restore(iteration_id, filename, expected_revision=data.expected_revision)" .-> s6
    s1 -->|"SnapshotService(db)"| s7
    s1 -. "HTTPException(status_code=404, detail=str(...))" .-> s8
    s1 -. "str(exc)" .-> s9
    s1 -. "HTTPException(status_code=400, detail=str(...))" .-> s10
    s1 -. "str(exc)" .-> s11
    click s1 "../modules/snapshots.md"
    click s3 "../modules/iteration_service.md"
    click s7 "../modules/snapshot_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `restore_snapshot` | `iteration_id: int`, `filename: str`, `data: SnapshotRestoreRequest`, `db: Annotated[AsyncSession, Depends(get_db, scope='function')]`, `_admin: Annotated[None, Depends(require_admin_api_key)]` | `status`, `status` | - | `...` |
| `HTTPException` | - | - | - | - |
| `IterationService` | - | - | - | - |
| `iteration_service.get_by_id` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `SnapshotService(…).restore` | - | - | - | - |
| `SnapshotService` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| restore_snapshot | HTTPException | 219 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Snapshot restore requires confirm=true.')` |
| restore_snapshot | IterationService | 224 | `IterationService(db)` |
| restore_snapshot | iteration_service.get_by_id | 225 | `iteration_service.get_by_id(iteration_id)` |
| restore_snapshot | HTTPException | 228 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| restore_snapshot | SnapshotService(…).restore | 234 | `SnapshotService(db).restore(iteration_id, filename, expected_revision=data.expected_revision)` |
| restore_snapshot | SnapshotService | 234 | `SnapshotService(db)` |
| restore_snapshot | HTTPException | 236 | `HTTPException(status_code=404, detail=str(...))` |
| restore_snapshot | str | 236 | `str(exc)` |
| restore_snapshot | HTTPException | 238 | `HTTPException(status_code=400, detail=str(...))` |
| restore_snapshot | str | 238 | `str(exc)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `restore_snapshot` | `HTTPException` | 219 |
| unresolved_call | `restore_snapshot` | `iteration_service.get_by_id` | 225 |
| external_call | `restore_snapshot` | `HTTPException` | 228 |
| unresolved_call | `restore_snapshot` | `SnapshotService(db).restore` | 234 |
| external_call | `restore_snapshot` | `HTTPException` | 236 |
| external_call | `restore_snapshot` | `HTTPException` | 238 |

## Behavior

This flow starts at `restore_snapshot` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

Requires operator authority and explicit restore confirmation. Checks the observed revision and captured provenance before restoring supported IDs and planning state, recording a pre-restore point and invalidating current acceptance.

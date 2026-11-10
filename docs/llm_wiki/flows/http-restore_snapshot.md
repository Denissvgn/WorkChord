# restore_snapshot

**Entry point:** `restore_snapshot` (`http`)
**Source:** [snapshots](../modules/snapshots.md)
**Modules touched:** [iteration_service](../modules/iteration_service.md), [snapshot_service](../modules/snapshot_service.md), [snapshots](../modules/snapshots.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as restore_snapshot
    participant p1 as HTTPException
    participant p2 as IterationService
    participant p3 as IterationService.get_by_id
    participant p4 as SnapshotService(…).restore
    participant p5 as SnapshotService
    participant p6 as str
    participant p7 as self.db.execute
    participant p8 as select(…).options(…).where
    participant p9 as select(…).options
    participant p10 as select
    participant p11 as selectinload
    participant p12 as result.scalar_one_or_none
    p0-->>p1: HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Snapshot restore requires confirm=true.')
    p0->>p2: IterationService
    p0->>p3: IterationService.get_by_id
    p0-->>p1: HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)
    p0-->>p4: SnapshotService(…).restore(iteration_id, filename, expected_revision=data.expected_revision)
    p0->>p5: SnapshotService
    p0-->>p1: HTTPException(status_code=404, detail=str(...))
    p0-->>p6: str(exc)
    p0-->>p1: HTTPException(status_code=400, detail=str(...))
    p0-->>p6: str(exc)
    p3-->>p7: self.db.execute(...)
    p3-->>p8: select(…).options(…).where(...)
    p3-->>p9: select(…).options(selectinload(...), selectinload(...))
    p3-->>p10: select(Iteration)
    p3-->>p11: selectinload(Iteration.calendar)
    p3-->>p11: selectinload(Iteration.project)
    p3-->>p12: result.scalar_one_or_none
```

> Call sequence diagram shows 17 of 17 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 9 of 9 (0 omitted); unresolved 5 of 5 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 4; effect analysis evaluated: 2, partial: 0, unavailable: 2. Counts include steps omitted from the displayed trace.

Collector observations for 2 source steps with known totals: observed: 11, emitted: 11, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `restore_snapshot` | `available` | `evaluated` | `available` | `8` | `8` | `0` |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `IterationService` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `IterationService.get_by_id` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `self.db.execute` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select(…).options(…).where` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select(…).options` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `selectinload` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `selectinload` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `result.scalar_one_or_none` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. restore_snapshot"]
    s2["2. HTTPException"]
    s3["3. IterationService"]
    s4["4. IterationService.get_by_id"]
    s5["5. self.db.execute"]
    s6["6. select(…).options(…).where"]
    s7["7. select(…).options"]
    s8["8. select"]
    s9["9. selectinload"]
    s10["10. selectinload"]
    s11["11. result.scalar_one_or_none"]
    s12["12. HTTPException"]
    s1 -. "HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Snapshot restore requires confirm=true.')" .-> s2
    s1 -->|"IterationService(db)"| s3
    s1 -->|"IterationService.get_by_id(iteration_id)"| s4
    s4 -. "self.db.execute(...)" .-> s5
    s4 -. "select(…).options(…).where(...)" .-> s6
    s4 -. "select(…).options(selectinload(...), selectinload(...))" .-> s7
    s4 -. "select(Iteration)" .-> s8
    s4 -. "selectinload(Iteration.calendar)" .-> s9
    s4 -. "selectinload(Iteration.project)" .-> s10
    s4 -. "result.scalar_one_or_none(data not statically known)" .-> s11
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s12
    click s1 "../modules/snapshots.md"
    click s3 "../modules/iteration_service.md"
    click s4 "../modules/iteration_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `restore_snapshot` | `iteration_id: int`, `filename: str`, `data: SnapshotRestoreRequest`, `db: Annotated[AsyncSession, Depends(get_db, scope='function')]`, `_admin: Annotated[None, Depends(require_admin_api_key)]` | `status`, `status` | - | `...` |
| `HTTPException` | - | - | - | - |
| `IterationService` | - | - | - | - |
| `IterationService.get_by_id` | `iteration_id: int` | `Iteration` | - | `result.scalar_one_or_none(...)` |
| `self.db.execute` | - | - | - | - |
| `select(…).options(…).where` | - | - | - | - |
| `select(…).options` | - | - | - | - |
| `select` | - | - | - | - |
| `selectinload` | - | - | - | - |
| `selectinload` | - | - | - | - |
| `result.scalar_one_or_none` | - | - | - | - |
| `HTTPException` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| restore_snapshot | HTTPException | 219 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Snapshot restore requires confirm=true.')` |
| restore_snapshot | IterationService | 224 | `IterationService(db)` |
| restore_snapshot | IterationService.get_by_id | 225 | `iteration_service.get_by_id(iteration_id)` |
| IterationService.get_by_id | self.db.execute | 323 | `self.db.execute(...)` |
| IterationService.get_by_id | select(…).options(…).where | 324 | `select(Iteration).options(selectinload(Iteration.calendar), selectinload(Iteration.project)).where(...)` |
| IterationService.get_by_id | select(…).options | 324 | `select(Iteration).options(selectinload(...), selectinload(...))` |
| IterationService.get_by_id | select | 324 | `select(Iteration)` |
| IterationService.get_by_id | selectinload | 326 | `selectinload(Iteration.calendar)` |
| IterationService.get_by_id | selectinload | 327 | `selectinload(Iteration.project)` |
| IterationService.get_by_id | result.scalar_one_or_none | 331 | `result.scalar_one_or_none(data not statically known)` |
| restore_snapshot | HTTPException | 228 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `restore_snapshot` | `HTTPException` | 219 |
| unresolved_call | `IterationService.get_by_id` | `self.db.execute` | 323 |
| unresolved_call | `IterationService.get_by_id` | `select(Iteration).options(selectinload(Iteration.calendar), selectinload(Iteration.project)).where` | 324 |
| unresolved_call | `IterationService.get_by_id` | `select(Iteration).options` | 324 |
| external_call | `IterationService.get_by_id` | `select` | 324 |
| external_call | `IterationService.get_by_id` | `selectinload` | 326 |
| external_call | `IterationService.get_by_id` | `selectinload` | 327 |
| unresolved_call | `IterationService.get_by_id` | `result.scalar_one_or_none` | 331 |
| external_call | `restore_snapshot` | `HTTPException` | 228 |
| step_limit | `restore_snapshot` | `first 12 steps` | 0 |

## Behavior

This flow starts at `restore_snapshot` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

Requires operator authority and explicit restore confirmation. Checks the observed revision and captured provenance before restoring supported IDs and planning state, recording a pre-restore point and invalidating current acceptance.

Scheduled and backlog restoration share a version allocator under the owning scope lock. It advances above the saved version, live task, retained history and durable deletion fence. Current progress and acceptance are cleared; immutable history survives. A deleted task without a reliable deletion fence returns snapshot_version_history_unknown (409), requiring recovery from a complete matching database backup.

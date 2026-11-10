# read_snapshot

**Entry point:** `read_snapshot` (`http`)
**Source:** [snapshots](../modules/snapshots.md)
**Modules touched:** [config](../modules/config.md), [snapshot_service](../modules/snapshot_service.md), [snapshots](../modules/snapshots.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as read_snapshot
    participant p1 as SnapshotService.get_snapshot
    participant p2 as SnapshotService
    participant p3 as HTTPException
    participant p4 as SNAPSHOT_FILENAME_PATTERN.fullmatch
    participant p5 as SnapshotPathError
    participant p6 as self.db.scalar
    participant p7 as select(…).where
    participant p8 as select
    participant p9 as SnapshotService._payload_visible
    participant p10 as hashlib.sha256(…).hexdigest
    participant p11 as hashlib.sha256
    participant p12 as SnapshotService._encode
    participant p13 as self.db.info.get
    participant p14 as json.dumps(…).encode
    participant p15 as list
    participant p16 as json.dumps
    participant p17 as payload.get
    participant p18 as len
    participant p19 as tasks.pop
    participant p20 as get_settings
    participant p21 as authority.allows
    participant p22 as ValueError
    participant p23 as task.get
    participant p24 as tasks.extend
    participant p25 as Settings
    p0->>p1: SnapshotService.get_snapshot
    p0->>p2: SnapshotService
    p0-->>p3: HTTPException(status_code=404, detail='Snapshot not found or inaccessible')
    p1-->>p4: SNAPSHOT_FILENAME_PATTERN.fullmatch(filename)
    p1->>p5: SnapshotPathError
    p1-->>p6: self.db.scalar(...)
    p1-->>p7: select(…).where(..., ...)
    p1-->>p8: select(ApplicationSnapshot)
    p1->>p9: SnapshotService._payload_visible
    p1-->>p10: hashlib.sha256(…).hexdigest
    p1-->>p11: hashlib.sha256(self._encode(...))
    p1->>p12: SnapshotService._encode
    p1->>p5: SnapshotPathError
    p9-->>p13: self.db.info.get('authority')
    p12-->>p14: json.dumps(…).encode
    p9-->>p15: list(payload.get(...))
    p12-->>p16: json.dumps(payload, sort_keys=True, separators=(...), ensure_ascii=False)
    p9-->>p17: payload.get('tasks', [...])
    p12-->>p18: len(encoded)
    p9-->>p19: tasks.pop
    p12->>p20: get_settings
    p9-->>p21: authority.allows(task.get(...), 'read')
    p12-->>p22: ValueError('Application snapshot exceeds the configured payload limit')
    p9-->>p23: task.get('project_id')
    p9-->>p24: tasks.extend(task.get(...))
    p9-->>p23: task.get('children', [...])
    p20->>p25: Settings
```

> Call sequence diagram shows 27 of 27 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 7 of 7 (0 omitted); unresolved 12 of 12 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 9; effect analysis evaluated: 5, partial: 0, unavailable: 4. Counts include steps omitted from the displayed trace.

Collector observations for 5 source steps with known totals: observed: 18, emitted: 18, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `read_snapshot` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `SnapshotService.get_snapshot` | `available` | `evaluated` | `available` | `5` | `5` | `0` |
| `SNAPSHOT_FILENAME_PATTERN.fullmatch` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `SnapshotPathError` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `self.db.scalar` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select(…).where` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `SnapshotService._payload_visible` | `available` | `evaluated` | `available` | `6` | `6` | `0` |
| `self.db.info.get` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `list` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `payload.get` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `tasks.pop` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. read_snapshot"]
    s2["2. SnapshotService.get_snapshot"]
    s3["3. SNAPSHOT_FILENAME_PATTERN.fullmatch"]
    s4["4. SnapshotPathError"]
    s5["5. self.db.scalar"]
    s6["6. select(…).where"]
    s7["7. select"]
    s8["8. SnapshotService._payload_visible"]
    s9["9. self.db.info.get"]
    s10["10. list"]
    s11["11. payload.get"]
    s12["12. tasks.pop"]
    s1 -->|"SnapshotService.get_snapshot(iteration_id, filename)"| s2
    s2 -. "SNAPSHOT_FILENAME_PATTERN.fullmatch(filename)" .-> s3
    s2 -->|"SnapshotPathError('Invalid snapshot filename')"| s4
    s2 -. "self.db.scalar(...)" .-> s5
    s2 -. "select(…).where(..., ...)" .-> s6
    s2 -. "select(ApplicationSnapshot)" .-> s7
    s2 -->|"SnapshotService._payload_visible(row.payload)"| s8
    s8 -. "self.db.info.get('authority')" .-> s9
    s8 -. "list(payload.get(...))" .-> s10
    s8 -. "payload.get('tasks', [...])" .-> s11
    s8 -. "tasks.pop(data not statically known)" .-> s12
    b0["mutation tasks.pop"]
    s8 -. "mutation tasks.pop" .-> b0
    b1["mutation tasks.extend"]
    s8 -. "mutation tasks.extend" .-> b1
    click s1 "../modules/snapshots.md"
    click s2 "../modules/snapshot_service.md"
    click s4 "../modules/snapshot_service.md"
    click s8 "../modules/snapshot_service.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `read_snapshot` | `iteration_id: int`, `filename: str`, `db: Annotated[AsyncSession, Depends(get_db, scope='function')]` | - | - | `payload` |
| `SnapshotService.get_snapshot` | `iteration_id: int`, `filename: str` | `ApplicationSnapshot` | - | `None`, `row.payload` |
| `SNAPSHOT_FILENAME_PATTERN.fullmatch` | - | - | - | - |
| `SnapshotPathError` | - | - | - | - |
| `self.db.scalar` | - | - | - | - |
| `select(…).where` | - | - | - | - |
| `select` | - | - | - | - |
| `SnapshotService._payload_visible` | `payload` | - | - | `True`, `False`, `True` |
| `self.db.info.get` | - | - | - | - |
| `list` | - | - | - | - |
| `payload.get` | - | - | - | - |
| `tasks.pop` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| read_snapshot | SnapshotService.get_snapshot | 283 | `SnapshotService(db).get_snapshot(iteration_id, filename)` |
| SnapshotService.get_snapshot | SNAPSHOT_FILENAME_PATTERN.fullmatch | 306 | `SNAPSHOT_FILENAME_PATTERN.fullmatch(filename)` |
| SnapshotService.get_snapshot | SnapshotPathError | 307 | `SnapshotPathError('Invalid snapshot filename')` |
| SnapshotService.get_snapshot | self.db.scalar | 308 | `self.db.scalar(...)` |
| SnapshotService.get_snapshot | select(…).where | 308 | `select(ApplicationSnapshot).where(..., ...)` |
| SnapshotService.get_snapshot | select | 308 | `select(ApplicationSnapshot)` |
| SnapshotService.get_snapshot | SnapshotService._payload_visible | 309 | `self._payload_visible(row.payload)` |
| SnapshotService._payload_visible | self.db.info.get | 317 | `self.db.info.get('authority')` |
| SnapshotService._payload_visible | list | 320 | `list(payload.get(...))` |
| SnapshotService._payload_visible | payload.get | 320 | `payload.get('tasks', [...])` |
| SnapshotService._payload_visible | tasks.pop | 322 | `tasks.pop(data not statically known)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `tasks.pop` | `SnapshotService._payload_visible` | 322 |
| mutation | `tasks.extend` | `SnapshotService._payload_visible` | 325 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `SnapshotService.get_snapshot` | `SNAPSHOT_FILENAME_PATTERN.fullmatch` | 306 |
| unresolved_call | `SnapshotService.get_snapshot` | `self.db.scalar` | 308 |
| unresolved_call | `SnapshotService.get_snapshot` | `select(ApplicationSnapshot).where` | 308 |
| external_call | `SnapshotService.get_snapshot` | `select` | 308 |
| unresolved_call | `SnapshotService._payload_visible` | `self.db.info.get` | 317 |
| unresolved_call | `SnapshotService._payload_visible` | `payload.get` | 320 |
| step_limit | `read_snapshot` | `first 12 steps` | 0 |

## Behavior

This flow starts at `read_snapshot` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

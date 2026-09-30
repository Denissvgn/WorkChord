# repair_hierarchy

**Entry point:** `repair_hierarchy` (`http`)
**Source:** [snapshots](../modules/snapshots.md)
**Modules touched:** [hierarchy_repair_service](../modules/hierarchy_repair_service.md), [snapshots](../modules/snapshots.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as repair_hierarchy
    participant p1 as HierarchyRepairService
    participant p2 as service.audit
    participant p3 as service.repair
    p0->>p1: HierarchyRepairService
    p0-->>p2: service.audit
    p0-->>p3: service.repair
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. repair_hierarchy"]
    s2["2. HierarchyRepairService"]
    s3["3. service.audit"]
    s4["4. service.repair"]
    s1 -->|"HierarchyRepairService(db)"| s2
    s1 -. "service.audit(iteration_id, after_id=data.after_id, limit=data.limit)" .-> s3
    s1 -. "service.repair(…)" .-> s4
    click s1 "../modules/snapshots.md"
    click s2 "../modules/hierarchy_repair_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `repair_hierarchy` | `iteration_id: int`, `data: HierarchyRepairRequest`, `db: Annotated[AsyncSession, Depends(get_db, scope='function')]`, `_operator: Annotated[None, Depends(require_admin_api_key)]` | - | - | `...`, `...` |
| `HierarchyRepairService` | - | - | - | - |
| `service.audit` | - | - | - | - |
| `service.repair` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| repair_hierarchy | HierarchyRepairService | 262 | `HierarchyRepairService(db)` |
| repair_hierarchy | service.audit | 264 | `service.audit(iteration_id, after_id=data.after_id, limit=data.limit)` |
| repair_hierarchy | service.repair | 265 | `service.repair(iteration_id, expected_versions=data.expected_versions, expected_revision=data.expected_revision, reason=data.reason, after_id=data.after_id, limit=data.limit)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `repair_hierarchy` | `service.audit` | 264 |
| unresolved_call | `repair_hierarchy` | `service.repair` | 265 |

## Behavior

This flow starts at `repair_hierarchy` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

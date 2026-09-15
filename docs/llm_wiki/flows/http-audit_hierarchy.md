# audit_hierarchy

**Entry point:** `audit_hierarchy` (`http`)
**Source:** [snapshots](../modules/snapshots.md)
**Modules touched:** [hierarchy_repair_service](../modules/hierarchy_repair_service.md), [snapshots](../modules/snapshots.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as audit_hierarchy
    participant p1 as HierarchyRepairService(…).audit
    participant p2 as HierarchyRepairService
    p0-->>p1: HierarchyRepairService(…).audit
    p0->>p2: HierarchyRepairService
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. audit_hierarchy"]
    s2["2. HierarchyRepairService(…).audit"]
    s3["3. HierarchyRepairService"]
    s1 -. "HierarchyRepairService(…).audit(iteration_id)" .-> s2
    s1 -->|"HierarchyRepairService(db)"| s3
    click s1 "../modules/snapshots.md"
    click s3 "../modules/hierarchy_repair_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `audit_hierarchy` | `iteration_id: int`, `db: Annotated[AsyncSession, Depends(get_db, scope='function')]`, `_operator: Annotated[None, Depends(require_admin_api_key)]` | - | - | `...` |
| `HierarchyRepairService(…).audit` | - | - | - | - |
| `HierarchyRepairService` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| audit_hierarchy | HierarchyRepairService(…).audit | 254 | `HierarchyRepairService(db).audit(iteration_id)` |
| audit_hierarchy | HierarchyRepairService | 254 | `HierarchyRepairService(db)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `audit_hierarchy` | `HierarchyRepairService(db).audit` | 254 |

## Behavior

This flow starts at `audit_hierarchy` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

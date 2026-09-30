# list_roadmap_milestones

**Entry point:** `list_roadmap_milestones` (`http`)
**Source:** [projects](../modules/projects.md)
**Modules touched:** [projects](../modules/projects.md), [schemas_project](../modules/schemas_project.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as list_roadmap_milestones
    participant p1 as service.list_portfolio_milestones
    participant p2 as RoadmapMilestonePage
    p0-->>p1: service.list_portfolio_milestones
    p0->>p2: RoadmapMilestonePage
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. list_roadmap_milestones"]
    s2["2. service.list_portfolio_milestones"]
    s3["3. RoadmapMilestonePage"]
    s1 -. "service.list_portfolio_milestones(after_id=after_id, limit=limit)" .-> s2
    s1 -->|"RoadmapMilestonePage(items=milestones, next_cursor=next_cursor)"| s3
    click s1 "../modules/projects.md"
    click s3 "../modules/schemas_project.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `list_roadmap_milestones` | `service: Annotated[ProjectService, Depends(get_project_service)]`, `after_id: Annotated[int \| None, Query(ge=0)]`, `limit: Annotated[int, Query(ge=1, le=MAX_BOUNDED_LIST_ITEMS)]` | - | - | `RoadmapMilestonePage(...)` |
| `service.list_portfolio_milestones` | - | - | - | - |
| `RoadmapMilestonePage` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| list_roadmap_milestones | service.list_portfolio_milestones | 112 | `service.list_portfolio_milestones(after_id=after_id, limit=limit)` |
| list_roadmap_milestones | RoadmapMilestonePage | 116 | `RoadmapMilestonePage(items=milestones, next_cursor=next_cursor)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `list_roadmap_milestones` | `service.list_portfolio_milestones` | 112 |

## Behavior

This flow starts at `list_roadmap_milestones` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

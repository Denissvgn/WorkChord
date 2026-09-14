# create_label_group

**Entry point:** `create_label_group` (`http`)
**Source:** [labels](../modules/labels.md)
**Modules touched:** [labels](../modules/labels.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as create_label_group
    participant p1 as service.create_group
    participant p2 as HTTPException
    participant p3 as str
    p0-->>p1: service.create_group
    p0-->>p2: HTTPException
    p0-->>p3: str
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. create_label_group"]
    s2["2. service.create_group"]
    s3["3. HTTPException"]
    s4["4. str"]
    s1 -. "service.create_group(data)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(...))" .-> s3
    s1 -. "str(exc)" .-> s4
    click s1 "../modules/labels.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `create_label_group` | `data: LabelGroupCreate`, `service: Annotated[LabelService, Depends(get_label_service)]` | `LabelConflictError`, `status` | - | `...` |
| `service.create_group` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| create_label_group | service.create_group | 49 | `service.create_group(data)` |
| create_label_group | HTTPException | 51 | `HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(...))` |
| create_label_group | str | 51 | `str(exc)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `create_label_group` | `service.create_group` | 49 |
| external_call | `create_label_group` | `HTTPException` | 51 |

## Behavior

This flow starts at `create_label_group` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

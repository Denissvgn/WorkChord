# formalize_task_draft

**Entry point:** `formalize_task_draft` (`http`)
**Source:** [routers_llm](../modules/routers_llm.md)
**Modules touched:** [routers_llm](../modules/routers_llm.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as formalize_task_draft
    participant p1 as data.title.strip
    participant p2 as HTTPException
    participant p3 as llm_service.formalize_task
    p0-->>p1: data.title.strip
    p0-->>p2: HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Task title is required')
    p0-->>p3: llm_service.formalize_task(title=title, description=data.description, context=data.context)
```

> Call sequence diagram shows 3 of 3 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 1 of 1 (0 omitted); unresolved 2 of 2 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis evaluated.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 1; effect analysis evaluated: 1, partial: 0, unavailable: 0. Counts include steps omitted from the displayed trace.

Collector observations for 1 source steps with known totals: observed: 4, emitted: 4, omitted: 0. Unavailable totals are excluded.

```mermaid
flowchart LR
    s1["1. formalize_task_draft"]
    s2["2. data.title.strip"]
    s3["3. HTTPException"]
    s4["4. llm_service.formalize_task"]
    s1 -. "data.title.strip(data not statically known)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Task title is required')" .-> s3
    s1 -. "llm_service.formalize_task(title=title, description=data.description, context=data.context)" .-> s4
    click s1 "../modules/routers_llm.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `formalize_task_draft` | `data: FormalizeDraftRequest`, `llm_service: Annotated[LLMService, Depends(get_llm_service)]` | `status` | - | `...` |
| `data.title.strip` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `llm_service.formalize_task` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| formalize_task_draft | data.title.strip | 127 | `data.title.strip(data not statically known)` |
| formalize_task_draft | HTTPException | 129 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Task title is required')` |
| formalize_task_draft | llm_service.formalize_task | 134 | `llm_service.formalize_task(title=title, description=data.description, context=data.context)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `formalize_task_draft` | `data.title.strip` | 127 |
| external_call | `formalize_task_draft` | `HTTPException` | 129 |
| unresolved_call | `formalize_task_draft` | `llm_service.formalize_task` | 134 |

## Behavior

This flow starts at `formalize_task_draft` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

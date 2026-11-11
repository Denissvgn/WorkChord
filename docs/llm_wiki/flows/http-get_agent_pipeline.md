# get_agent_pipeline

**Entry point:** `get_agent_pipeline` (`http`)
**Source:** [routers_agent](../modules/routers_agent.md)
**Modules touched:** [routers_agent](../modules/routers_agent.md), [schemas_agent](../modules/schemas_agent.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as get_agent_pipeline
    participant p1 as service.get_pipeline
    participant p2 as AgentPipelineResponse
    p0-->>p1: service.get_pipeline
    p0->>p2: AgentPipelineResponse
```

> Call sequence diagram shows 2 of 2 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 0 of 0 (0 omitted); unresolved 1 of 1 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 2; effect analysis evaluated: 1, partial: 0, unavailable: 1. Counts include steps omitted from the displayed trace.

Collector observations for 1 source steps with known totals: observed: 3, emitted: 3, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `get_agent_pipeline` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `service.get_pipeline` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `AgentPipelineResponse` | `unavailable` | `unavailable` | `unavailable` | — | — | — |

```mermaid
flowchart LR
    s1["1. get_agent_pipeline"]
    s2["2. service.get_pipeline"]
    s3["3. AgentPipelineResponse"]
    s1 -. "service.get_pipeline(data not statically known)" .-> s2
    s1 -->|"AgentPipelineResponse(**=cols)"| s3
    click s1 "../modules/routers_agent.md"
    click s3 "../modules/schemas_agent.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `get_agent_pipeline` | `service: Annotated[AgentService, Depends(get_agent_service)]`, `_: Annotated[None, Depends(require_agent_read_access)]` | - | - | `AgentPipelineResponse(...)` |
| `service.get_pipeline` | - | - | - | - |
| `AgentPipelineResponse` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| get_agent_pipeline | service.get_pipeline | 1315 | `service.get_pipeline(data not statically known)` |
| get_agent_pipeline | AgentPipelineResponse | 1316 | `AgentPipelineResponse(**=cols)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `get_agent_pipeline` | `service.get_pipeline` | 1315 |

## Behavior

This flow starts at `get_agent_pipeline` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

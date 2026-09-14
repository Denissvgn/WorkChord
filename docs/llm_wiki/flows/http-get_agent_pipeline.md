# get_agent_pipeline

**Entry point:** `get_agent_pipeline` (`http`)
**Source:** [routers_agent](../modules/routers_agent.md)
**Modules touched:** [routers_agent](../modules/routers_agent.md), [schemas_agent](../modules/schemas_agent.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as get_agent_pipeline
    participant p1 as service.get_pipeline
    participant p2 as AgentPipelineResponse
    participant p3 as cols.get
    p0-->>p1: service.get_pipeline
    p0->>p2: AgentPipelineResponse
    p0-->>p3: cols.get
    p0-->>p3: cols.get
    p0-->>p3: cols.get
    p0-->>p3: cols.get
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. get_agent_pipeline"]
    s2["2. service.get_pipeline"]
    s3["3. AgentPipelineResponse"]
    s4["4. cols.get"]
    s5["5. cols.get"]
    s6["6. cols.get"]
    s7["7. cols.get"]
    s1 -. "service.get_pipeline(data not statically known)" .-> s2
    s1 -->|"AgentPipelineResponse(…)"| s3
    s1 -. "cols.get('definition_ready_unassigned', [...])" .-> s4
    s1 -. "cols.get('assigned_waiting', [...])" .-> s5
    s1 -. "cols.get('start_ready', [...])" .-> s6
    s1 -. "cols.get('recovery_required', [...])" .-> s7
    click s1 "../modules/routers_agent.md"
    click s3 "../modules/schemas_agent.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `get_agent_pipeline` | `service: Annotated[AgentService, Depends(get_agent_service)]`, `_: Annotated[None, Depends(require_agent_read_access)]` | - | - | `AgentPipelineResponse(...)` |
| `service.get_pipeline` | - | - | - | - |
| `AgentPipelineResponse` | - | - | - | - |
| `cols.get` | - | - | - | - |
| `cols.get` | - | - | - | - |
| `cols.get` | - | - | - | - |
| `cols.get` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| get_agent_pipeline | service.get_pipeline | 1303 | `service.get_pipeline(data not statically known)` |
| get_agent_pipeline | AgentPipelineResponse | 1304 | `AgentPipelineResponse(needs_definition=cols[...], ready_for_agent=cols[...], definition_ready_unassigned=cols.get(...), assigned_waiting=cols.get(...), start_ready=cols.get(...), executing=cols[...], verification_required=cols[...], recovery_required=cols.get(...))` |
| get_agent_pipeline | cols.get | 1307 | `cols.get('definition_ready_unassigned', [...])` |
| get_agent_pipeline | cols.get | 1308 | `cols.get('assigned_waiting', [...])` |
| get_agent_pipeline | cols.get | 1309 | `cols.get('start_ready', [...])` |
| get_agent_pipeline | cols.get | 1312 | `cols.get('recovery_required', [...])` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `get_agent_pipeline` | `service.get_pipeline` | 1303 |
| unresolved_call | `get_agent_pipeline` | `cols.get` | 1307 |
| unresolved_call | `get_agent_pipeline` | `cols.get` | 1308 |
| unresolved_call | `get_agent_pipeline` | `cols.get` | 1309 |
| unresolved_call | `get_agent_pipeline` | `cols.get` | 1312 |

## Behavior

This flow starts at `get_agent_pipeline` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

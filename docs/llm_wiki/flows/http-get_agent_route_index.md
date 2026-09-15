# get_agent_route_index

**Entry point:** `get_agent_route_index` (`http`)
**Source:** [agent_catalog](../modules/agent_catalog.md)
**Modules touched:** [agent_catalog](../modules/agent_catalog.md), [agent_profile_catalog_service](../modules/agent_profile_catalog_service.md), [agent_service](../modules/agent_service.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as get_agent_route_index
    participant p1 as _require_catalog_read
    participant p2 as any
    participant p3 as actor_has_scope
    participant p4 as actor_scopes
    participant p5 as json.loads
    participant p6 as isinstance
    participant p7 as HTTPException
    participant p8 as AgentProfileCatalogService(…).routes
    participant p9 as AgentProfileCatalogService
    p0->>p1: _require_catalog_read
    p1-->>p2: any
    p1->>p3: actor_has_scope
    p3->>p4: actor_scopes
    p4-->>p5: json.loads
    p4-->>p6: isinstance
    p1-->>p7: HTTPException
    p0-->>p8: AgentProfileCatalogService(…).routes
    p0->>p9: AgentProfileCatalogService
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. get_agent_route_index"]
    s2["2. _require_catalog_read"]
    s3["3. any"]
    s4["4. actor_has_scope"]
    s5["5. actor_scopes"]
    s6["6. json.loads"]
    s7["7. isinstance"]
    s8["8. HTTPException"]
    s9["9. AgentProfileCatalogService(…).routes"]
    s10["10. AgentProfileCatalogService"]
    s1 -->|"_require_catalog_read(actor)"| s2
    s2 -. "any(...)" .-> s3
    s2 -->|"actor_has_scope(actor, scope)"| s4
    s4 -->|"actor_scopes(actor)"| s5
    s5 -. "json.loads(actor.scopes)" .-> s6
    s5 -. "isinstance(scopes, list)" .-> s7
    s2 -. "HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Missing catalog read scope')" .-> s8
    s1 -. "AgentProfileCatalogService(…).routes(data not statically known)" .-> s9
    s1 -->|"AgentProfileCatalogService(db)"| s10
    click s1 "../modules/agent_catalog.md"
    click s2 "../modules/agent_catalog.md"
    click s4 "../modules/agent_service.md"
    click s5 "../modules/agent_service.md"
    click s10 "../modules/agent_profile_catalog_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `get_agent_route_index` | `actor: Annotated[AgentActor, Depends(get_agent_actor)]`, `db: Annotated[AsyncSession, Depends(get_db, scope='function')]` | - | - | `...` |
| `_require_catalog_read` | `actor: AgentActor` | `status` | - | - |
| `any` | - | - | - | - |
| `actor_has_scope` | `actor: AgentActor`, `scope: str` | - | - | `...` |
| `actor_scopes` | `actor: AgentActor` | `json` | - | `...` |
| `json.loads` | - | - | - | - |
| `isinstance` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `AgentProfileCatalogService(…).routes` | - | - | - | - |
| `AgentProfileCatalogService` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| get_agent_route_index | _require_catalog_read | 104 | `_require_catalog_read(actor)` |
| _require_catalog_read | any | 68 | `any(...)` |
| _require_catalog_read | actor_has_scope | 69 | `actor_has_scope(actor, scope)` |
| actor_has_scope | actor_scopes | 80 | `actor_scopes(actor)` |
| actor_scopes | json.loads | 72 | `json.loads(actor.scopes)` |
| actor_scopes | isinstance | 75 | `isinstance(scopes, list)` |
| _require_catalog_read | HTTPException | 72 | `HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Missing catalog read scope')` |
| get_agent_route_index | AgentProfileCatalogService(…).routes | 105 | `AgentProfileCatalogService(db).routes(data not statically known)` |
| get_agent_route_index | AgentProfileCatalogService | 105 | `AgentProfileCatalogService(db)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `_require_catalog_read` | `any` | 68 |
| external_call | `actor_scopes` | `json.loads` | 72 |
| external_call | `actor_scopes` | `isinstance` | 75 |
| external_call | `_require_catalog_read` | `HTTPException` | 72 |
| unresolved_call | `get_agent_route_index` | `AgentProfileCatalogService(db).routes` | 105 |

## Behavior

This flow starts at `get_agent_route_index` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

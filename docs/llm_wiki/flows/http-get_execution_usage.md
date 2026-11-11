# get_execution_usage

**Entry point:** `get_execution_usage` (`http`)
**Source:** [routers_agent](../modules/routers_agent.md)
**Modules touched:** [agent_service](../modules/agent_service.md), [authority](../modules/authority.md), [config](../modules/config.md), [execution_usage_service](../modules/execution_usage_service.md), and 4 more

**Complete modules touched:**

- [agent_service](../modules/agent_service.md)
- [authority](../modules/authority.md)
- [config](../modules/config.md)
- [execution_usage_service](../modules/execution_usage_service.md)
- [query_limits](../modules/query_limits.md)
- [routers_agent](../modules/routers_agent.md)
- [schemas_execution_usage](../modules/schemas_execution_usage.md)
- [time](../modules/time.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as get_execution_usage
    participant p1 as ExecutionUsageService.latest
    participant p2 as ExecutionUsageService
    participant p3 as _handle_agent_error
    participant p4 as ExecutionUsageService._run
    participant p5 as ExecutionUsageService._history
    participant p6 as run_identity
    participant p7 as ExecutionUsageService.response
    participant p8 as actor_has_scope
    participant p9 as ExecutionUsageService._scope
    participant p10 as require_project
    participant p11 as get_settings
    participant p12 as internal_authority
    participant p13 as ExecutionUsageResponse
    participant p14 as AgentPermissionError
    participant p15 as as_utc
    participant p16 as CollectionLimitExceededError
    participant p17 as actor_scopes
    participant p18 as AuthorityError
    participant p19 as Settings
    participant p20 as isinstance (backend/app/routers/agent.py:_handle_agent_error)
    participant p21 as exc.detail
    participant p22 as str
    participant p23 as HTTPException
    p0->>p1: ExecutionUsageService.latest
    p0->>p2: ExecutionUsageService
    p0->>p3: _handle_agent_error
    p1->>p4: ExecutionUsageService._run
    p1->>p5: ExecutionUsageService._history
    p1->>p6: run_identity
    p1->>p7: ExecutionUsageService.response
    p4->>p8: actor_has_scope
    p5->>p9: ExecutionUsageService._scope
    p9->>p10: require_project
    p10->>p11: get_settings
    p5->>p12: internal_authority
    p7->>p13: ExecutionUsageResponse
    p4->>p14: AgentPermissionError
    p6->>p15: as_utc
    p5->>p16: CollectionLimitExceededError
    p8->>p17: actor_scopes
    p9->>p18: AuthorityError
    p11->>p19: Settings
    p3-->>p20: isinstance (backend/app/routers/agent.py:_handle_agent_error)(exc, AgentPermissionError)
    p3-->>p21: exc.detail
    p3-->>p22: str(exc)
    p3-->>p22: str(exc)
    p3-->>p23: HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
    p3-->>p20: isinstance (backend/app/routers/agent.py:_handle_agent_error)(exc, AgentRoutingConflictError)
    p3-->>p23: HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))
    p3-->>p20: isinstance (backend/app/routers/agent.py:_handle_agent_error)(exc, AgentTeamSetupConflictError)
    p3-->>p23: HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))
    p3-->>p21: exc.detail
    p3-->>p20: isinstance (backend/app/routers/agent.py:_handle_agent_error)(exc, TaskVersionConflictError)
```

> Call sequence diagram shows 30 of 77 interactions; 47 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 9 of 32 (23 omitted); unresolved 2 of 21 (19 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/services/execution_usage_service.py:ExecutionUsageService._run` | 3 | - | external | 3 |
| `backend/app/services/agent_service.py:actor_scopes` | 6 | - | external | 2 |
| `backend/app/services/execution_usage_service.py:ExecutionUsageService._run` | 3 | - | unresolved | 3 |
| `backend/app/services/execution_usage_service.py:ExecutionUsageService._run` | 3 | [backend/app/services/agent_service.py](../modules/agent_service.md) | internal | 3 |
| `backend/app/authority.py:internal_authority` | 19 | - | unresolved | 1 |
| `backend/app/services/execution_usage_service.py:ExecutionUsageService._history` | 18 | - | external | 3 |
| `backend/app/services/execution_usage_service.py:ExecutionUsageService._history` | 18 | - | unresolved | 5 |
| `backend/app/services/execution_usage_service.py:ExecutionUsageService._scope` | 30 | - | unresolved | 1 |
> Omission summary shows 8 of 16 groups; 8 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 25; effect analysis evaluated: 15, partial: 1, unavailable: 9. Counts include steps omitted from the displayed trace.

Collector observations for 16 source steps with known totals: observed: 62, emitted: 58, omitted: 4. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector omitted observations before flow assembly; displayed effects are partial.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `get_execution_usage` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `ExecutionUsageService.latest` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `ExecutionUsageService._run` | `available` | `evaluated` | `available` | `5` | `5` | `0` |
| `any` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `actor_has_scope` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `actor_scopes` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `json.loads` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `isinstance (backend/app/services/agent_service.py:actor_scopes)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `AgentPermissionError` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `select(…).where (backend/app/services/exec…ExecutionUsageService._run)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select (backend/app/services/exec…ExecutionUsageService._run)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `statement.with_for_update` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. get_execution_usage"]
    s2["2. ExecutionUsageService.latest"]
    s3["3. ExecutionUsageService._run"]
    s4["4. any"]
    s5["5. actor_has_scope"]
    s6["6. actor_scopes"]
    s7["7. json.loads"]
    s8["8. isinstance (backend/app/services/agent_service.py:actor_scopes)"]
    s9["9. AgentPermissionError"]
    s10["10. select(…).where (backend/app/services/exec…ExecutionUsageService._run)"]
    s11["11. select (backend/app/services/exec…ExecutionUsageService._run)"]
    s12["12. statement.with_for_update"]
    s1 -->|"ExecutionUsageService.latest(actor, run_id)"| s2
    s2 -->|"ExecutionUsageService._run(actor, run_id)"| s3
    s3 -. "any(...)" .-> s4
    s3 -->|"actor_has_scope(actor, scope)"| s5
    s5 -->|"actor_scopes(actor)"| s6
    s6 -. "json.loads(actor.scopes)" .-> s7
    s6 -. "isinstance (backend/app/services/agent_service.py:actor_scopes)(scopes, list)" .-> s8
    s3 -->|"AgentPermissionError('The actor cannot access execution usage')"| s9
    s3 -. "select(…).where (backend/app/services/exec…ExecutionUsageService._run)(...)" .-> s10
    s3 -. "select (backend/app/services/exec…ExecutionUsageService._run)(AgentRun)" .-> s11
    s3 -. "statement.with_for_update(data not statically known)" .-> s12
    click s1 "../modules/routers_agent.md"
    click s2 "../modules/execution_usage_service.md"
    click s3 "../modules/execution_usage_service.md"
    click s5 "../modules/agent_service.md"
    click s6 "../modules/agent_service.md"
    click s9 "../modules/agent_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `get_execution_usage` | `run_id: int`, `actor: Annotated[AgentActor, Depends(get_agent_actor)]`, `db: Annotated[AsyncSession, Depends(get_db, scope='function')]` | - | - | `...` |
| `ExecutionUsageService.latest` | `actor`, `run_id` | - | - | `...` |
| `ExecutionUsageService._run` | `actor`, `run_id`, `writing` | `AgentRun` | - | `run` |
| `any` | - | - | - | - |
| `actor_has_scope` | `actor: AgentActor`, `scope: str` | - | - | `...` |
| `actor_scopes` | `actor: AgentActor` | `json` | - | `...` |
| `json.loads` | - | - | - | - |
| `isinstance (backend/app/services/agent_service.py:actor_scopes)` | - | - | - | - |
| `AgentPermissionError` | - | - | - | - |
| `select(…).where (backend/app/services/exec…ExecutionUsageService._run)` | - | - | - | - |
| `select (backend/app/services/exec…ExecutionUsageService._run)` | - | - | - | - |
| `statement.with_for_update` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| get_execution_usage | ExecutionUsageService.latest | 1336 | `ExecutionUsageService(db).latest(actor, run_id)` |
| ExecutionUsageService.latest | ExecutionUsageService._run | 93 | `self._run(actor, run_id)` |
| ExecutionUsageService._run | any | 62 | `any(...)` |
| ExecutionUsageService._run | actor_has_scope | 62 | `actor_has_scope(actor, scope)` |
| actor_has_scope | actor_scopes | 94 | `actor_scopes(actor)` |
| actor_scopes | json.loads | 86 | `json.loads(actor.scopes)` |
| actor_scopes | isinstance (backend/app/services/agent_service.py:actor_scopes) | 89 | `isinstance(scopes, list)` |
| ExecutionUsageService._run | AgentPermissionError | 63 | `AgentPermissionError('The actor cannot access execution usage')` |
| ExecutionUsageService._run | select(…).where (backend/app/services/exec…ExecutionUsageService._run) | 64 | `select(AgentRun).where(...)` |
| ExecutionUsageService._run | select (backend/app/services/exec…ExecutionUsageService._run) | 64 | `select(AgentRun)` |
| ExecutionUsageService._run | statement.with_for_update | 66 | `statement.with_for_update(data not statically known)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `ExecutionUsageService._run` | `any` | 62 |
| external_call | `actor_scopes` | `json.loads` | 86 |
| external_call | `actor_scopes` | `isinstance` | 89 |
| unresolved_call | `ExecutionUsageService._run` | `select(AgentRun).where` | 64 |
| external_call | `ExecutionUsageService._run` | `select` | 64 |
| unresolved_call | `ExecutionUsageService._run` | `statement.with_for_update` | 66 |
| step_limit | `get_execution_usage` | `first 12 steps` | 0 |

## Behavior

This flow starts at `get_execution_usage` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

# list_runtime_observations

**Entry point:** `list_runtime_observations` (`http`)
**Source:** [routers_agent](../modules/routers_agent.md)
**Modules touched:** [routers_agent](../modules/routers_agent.md), [runtime_observation_service](../modules/runtime_observation_service.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as list_runtime_observations
    participant p1 as _refuse_agents
    participant p2 as db.info.get
    participant p3 as _reads_work_as_person
    participant p4 as HTTPException (backend/app/routers/agent…:list_runtime_observations)
    participant p5 as RuntimeObservationService.list
    participant p6 as RuntimeObservationService
    participant p7 as service_db.info.get
    participant p8 as bool
    participant p9 as select
    participant p10 as HTTPException (backend/app/routers/agent.py:_refuse_agents)
    participant p11 as query.where
    participant p12 as self.db.execute
    participant p13 as query.order_by(…).limit
    participant p14 as query.order_by
    participant p15 as AgentRuntimeObservation.received_at.desc
    participant p16 as AgentRuntimeObservation.id.desc
    participant p17 as list
    participant p18 as rows.scalars().all
    participant p19 as rows.scalars
    p0->>p1: _refuse_agents
    p0-->>p2: db.info.get('authority')
    p0->>p3: _reads_work_as_person
    p0-->>p4: HTTPException (backend/app/routers/agent…:list_runtime_observations)(status_code=status.HTTP_401_UNAUTHORIZED, detail='Sign in to read observations.')
    p0->>p5: RuntimeObservationService.list
    p0->>p6: RuntimeObservationService
    p1-->>p7: service_db.info.get('authority')
    p3-->>p8: bool(authority.projects)
    p5-->>p9: select(AgentRuntimeObservation)
    p1-->>p10: HTTPException (backend/app/routers/agent.py:_refuse_agents)(…)
    p5-->>p11: query.where(...)
    p5-->>p11: query.where(...)
    p5-->>p11: query.where(...)
    p5-->>p11: query.where(...)
    p5-->>p12: self.db.execute(...)
    p5-->>p13: query.order_by(…).limit(limit)
    p5-->>p14: query.order_by(AgentRuntimeObservation.received_at.desc(...), AgentRuntimeObservation.id.desc(...))
    p5-->>p15: AgentRuntimeObservation.received_at.desc
    p5-->>p16: AgentRuntimeObservation.id.desc
    p5-->>p17: list(...)
    p5-->>p18: rows.scalars().all
    p5-->>p19: rows.scalars
```

> Call sequence diagram shows 22 of 22 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 5 of 5 (0 omitted); unresolved 13 of 13 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 5; effect analysis evaluated: 4, partial: 0, unavailable: 1. Counts include steps omitted from the displayed trace.

Collector observations for 4 source steps with known totals: observed: 25, emitted: 25, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `list_runtime_observations` | `available` | `evaluated` | `available` | `9` | `9` | `0` |
| `_refuse_agents` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `service_db.info.get` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException (backend/app/routers/agent.py:_refuse_agents)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `db.info.get` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `_reads_work_as_person` | `available` | `evaluated` | `available` | `2` | `2` | `0` |
| `bool` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException (backend/app/routers/agent…:list_runtime_observations)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `RuntimeObservationService.list` | `available` | `evaluated` | `available` | `11` | `11` | `0` |
| `select` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `query.where` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `query.where` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. list_runtime_observations"]
    s2["2. _refuse_agents"]
    s3["3. service_db.info.get"]
    s4["4. HTTPException (backend/app/routers/agent.py:_refuse_agents)"]
    s5["5. db.info.get"]
    s6["6. _reads_work_as_person"]
    s7["7. bool"]
    s8["8. HTTPException (backend/app/routers/agent…:list_runtime_observations)"]
    s9["9. RuntimeObservationService.list"]
    s10["10. select"]
    s11["11. query.where"]
    s12["12. query.where"]
    s1 -->|"_refuse_agents(db, agent_api_key)"| s2
    s2 -. "service_db.info.get('authority')" .-> s3
    s2 -. "HTTPException (backend/app/routers/agent.py:_refuse_agents)(…)" .-> s4
    s1 -. "db.info.get('authority')" .-> s5
    s1 -->|"_reads_work_as_person(authority)"| s6
    s6 -. "bool(authority.projects)" .-> s7
    s1 -. "HTTPException (backend/app/routers/agent…:list_runtime_observations)(status_code=status.HTTP_401_UNAUTHORIZED, detail='Sign in to read observations.')" .-> s8
    s1 -->|"RuntimeObservationService.list(task_id=task_id, run_id=run_id, harness_kind=harness_kind, harness_session_id=harness_session_id, limit=limit)"| s9
    s9 -. "select(AgentRuntimeObservation)" .-> s10
    s9 -. "query.where(...)" .-> s11
    s9 -. "query.where(...)" .-> s12
    click s1 "../modules/routers_agent.md"
    click s2 "../modules/routers_agent.md"
    click s6 "../modules/routers_agent.md"
    click s9 "../modules/runtime_observation_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `list_runtime_observations` | `db: Annotated[AsyncSession, Depends(get_db, scope='function')]`, `agent_api_key: Annotated[Optional[str], Header(alias='X-Agent-API-Key')]`, `task_id: Optional[int]`, `run_id: Optional[int]`, `harness_kind: Optional[str]`, `harness_session_id: Optional[str]`, `limit: int` | `status` | - | `...` |
| `_refuse_agents` | `service_db`, `agent_api_key` | `status` | - | - |
| `service_db.info.get` | - | - | - | - |
| `HTTPException (backend/app/routers/agent.py:_refuse_agents)` | - | - | - | - |
| `db.info.get` | - | - | - | - |
| `_reads_work_as_person` | `authority` | - | - | `...` |
| `bool` | - | - | - | - |
| `HTTPException (backend/app/routers/agent…:list_runtime_observations)` | - | - | - | - |
| `RuntimeObservationService.list` | `task_id`, `run_id`, `harness_kind`, `harness_session_id`, `limit` | `AgentRuntimeObservation`, `AgentRuntimeObservation`, `AgentRuntimeObservation`, `AgentRuntimeObservation`, `AgentRuntimeObservation` | - | `list(...)` |
| `select` | - | - | - | - |
| `query.where` | - | - | - | - |
| `query.where` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| list_runtime_observations | _refuse_agents | 1560 | `_refuse_agents(db, agent_api_key)` |
| _refuse_agents | service_db.info.get | 1518 | `service_db.info.get('authority')` |
| _refuse_agents | HTTPException (backend/app/routers/agent.py:_refuse_agents) | 1520 | `HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Runtime observations are advisory and are not available to agents.')` |
| list_runtime_observations | db.info.get | 1561 | `db.info.get('authority')` |
| list_runtime_observations | _reads_work_as_person | 1562 | `_reads_work_as_person(authority)` |
| _reads_work_as_person | bool | 267 | `bool(authority.projects)` |
| list_runtime_observations | HTTPException (backend/app/routers/agent…:list_runtime_observations) | 1563 | `HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Sign in to read observations.')` |
| list_runtime_observations | RuntimeObservationService.list | 1564 | `RuntimeObservationService(db).list(task_id=task_id, run_id=run_id, harness_kind=harness_kind, harness_session_id=harness_session_id, limit=limit)` |
| RuntimeObservationService.list | select | 100 | `select(AgentRuntimeObservation)` |
| RuntimeObservationService.list | query.where | 102 | `query.where(...)` |
| RuntimeObservationService.list | query.where | 104 | `query.where(...)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `_refuse_agents` | `service_db.info.get` | 1518 |
| external_call | `_refuse_agents` | `HTTPException` | 1520 |
| unresolved_call | `list_runtime_observations` | `db.info.get` | 1561 |
| external_call | `list_runtime_observations` | `HTTPException` | 1563 |
| external_call | `RuntimeObservationService.list` | `select` | 100 |
| unresolved_call | `RuntimeObservationService.list` | `query.where` | 102 |
| unresolved_call | `RuntimeObservationService.list` | `query.where` | 104 |
| step_limit | `list_runtime_observations` | `first 12 steps` | 0 |

## Behavior

Lists observations for people (on the pipeline's read rule), observers and operators, newest first, filtered by task, run or harness session. The request's task read scope applies, so rows without a task are visible only to operators and trusted-local readers. Agent keys get 403, so agents cannot steer on observations.

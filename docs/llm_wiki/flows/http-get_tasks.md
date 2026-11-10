# get_tasks

**Entry point:** `get_tasks` (`http`)
**Source:** [tasks](../modules/tasks.md)
**Modules touched:** [config](../modules/config.md), [iteration_service](../modules/iteration_service.md), [language_service](../modules/language_service.md), [system_settings_service](../modules/system_settings_service.md), and 2 more

**Complete modules touched:**

- [config](../modules/config.md)
- [iteration_service](../modules/iteration_service.md)
- [language_service](../modules/language_service.md)
- [system_settings_service](../modules/system_settings_service.md)
- [tasks](../modules/tasks.md)
- [url_policy](../modules/url_policy.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as get_tasks
    participant p1 as _not_found_detail
    participant p2 as IterationService
    participant p3 as IterationService.get_by_id
    participant p4 as resolve_runtime_ui_language
    participant p5 as entity_not_found_message
    participant p6 as RuntimeSettingsService.get_app_settings
    participant p7 as localized
    participant p8 as get_settings
    participant p9 as RuntimeSettingsService.resolve
    participant p10 as RuntimeSettingsService._definition
    participant p11 as RuntimeSettingsService._decrypt_secret
    participant p12 as RuntimeSettingsService._coerce
    participant p13 as normalize_language
    participant p14 as RuntimeSettingsService
    participant p15 as Settings
    participant p16 as RuntimeSettingsService._row
    participant p17 as RuntimeSettingsService._env_value
    participant p18 as RuntimeSettingsError
    participant p19 as RuntimeSettingsService._fernet
    participant p20 as RuntimeSettingsEncryptionError
    participant p21 as normalize_provider_api_url
    participant p22 as HTTPException
    participant p23 as service.get_by_iteration
    participant p24 as service.task_to_response
    participant p25 as self.db.execute (backend/app/services/iter…IterationService.get_by_id)
    participant p26 as select(…).options(…).where
    participant p27 as select(…).options
    participant p28 as select (backend/app/services/iter…IterationService.get_by_id)
    participant p29 as selectinload
    p0->>p1: _not_found_detail
    p0->>p2: IterationService
    p0->>p3: IterationService.get_by_id
    p1->>p4: resolve_runtime_ui_language
    p1->>p5: entity_not_found_message
    p4->>p6: RuntimeSettingsService.get_app_settings
    p5->>p7: localized
    p4->>p8: get_settings
    p6->>p9: RuntimeSettingsService.resolve
    p9->>p10: RuntimeSettingsService._definition
    p9->>p11: RuntimeSettingsService._decrypt_secret
    p9->>p12: RuntimeSettingsService._coerce
    p4->>p13: normalize_language
    p4->>p14: RuntimeSettingsService
    p8->>p15: Settings
    p9->>p16: RuntimeSettingsService._row
    p9->>p17: RuntimeSettingsService._env_value
    p10->>p18: RuntimeSettingsError
    p11->>p19: RuntimeSettingsService._fernet
    p11->>p20: RuntimeSettingsEncryptionError
    p12->>p21: normalize_provider_api_url
    p0-->>p22: HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)
    p0-->>p23: service.get_by_iteration(iteration_id)
    p0-->>p24: service.task_to_response(t, iteration.end_date)
    p3-->>p25: self.db.execute (backend/app/services/iter…IterationService.get_by_id)(...)
    p3-->>p26: select(…).options(…).where(...)
    p3-->>p27: select(…).options(selectinload(...), selectinload(...))
    p3-->>p28: select (backend/app/services/iter…IterationService.get_by_id)(Iteration)
    p3-->>p29: selectinload(Iteration.calendar)
    p3-->>p29: selectinload(Iteration.project)
```

> Call sequence diagram shows 30 of 78 interactions; 48 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 4 of 18 (14 omitted); unresolved 5 of 19 (14 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/services/iteration_service.py:IterationService.get_by_id` | 3 | - | unresolved | 1 |
| `backend/app/services/language_service.py:normalize_language` | 14 | - | unresolved | 2 |
| `backend/app/services/language_service.py:normalize_language` | 14 | - | external | 1 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._definition` | 20 | - | unresolved | 1 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._row` | 23 | - | unresolved | 3 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._row` | 23 | - | external | 1 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._decrypt_secret` | 28 | - | unresolved | 3 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._coerce` | 34 | - | external | 8 |
> Omission summary shows 8 of 20 groups; 12 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 42; effect analysis evaluated: 23, partial: 0, unavailable: 19. Counts include steps omitted from the displayed trace.

Collector observations for 23 source steps with known totals: observed: 88, emitted: 88, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `get_tasks` | `available` | `evaluated` | `available` | `5` | `5` | `0` |
| `IterationService` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `IterationService.get_by_id` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `self.db.execute (backend/app/services/iter…IterationService.get_by_id)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select(…).options(…).where` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select(…).options` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select (backend/app/services/iter…IterationService.get_by_id)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `selectinload` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `selectinload` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `result.scalar_one_or_none (backend/app/services/iter…IterationService.get_by_id)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `_not_found_detail` | `available` | `evaluated` | `available` | `4` | `4` | `0` |

```mermaid
flowchart LR
    s1["1. get_tasks"]
    s2["2. IterationService"]
    s3["3. IterationService.get_by_id"]
    s4["4. self.db.execute (backend/app/services/iter…IterationService.get_by_id)"]
    s5["5. select(…).options(…).where"]
    s6["6. select(…).options"]
    s7["7. select (backend/app/services/iter…IterationService.get_by_id)"]
    s8["8. selectinload"]
    s9["9. selectinload"]
    s10["10. result.scalar_one_or_none (backend/app/services/iter…IterationService.get_by_id)"]
    s11["11. HTTPException"]
    s12["12. _not_found_detail"]
    s1 -->|"IterationService(db)"| s2
    s1 -->|"IterationService.get_by_id(iteration_id)"| s3
    s3 -. "self.db.execute (backend/app/services/iter…IterationService.get_by_id)(...)" .-> s4
    s3 -. "select(…).options(…).where(...)" .-> s5
    s3 -. "select(…).options(selectinload(...), selectinload(...))" .-> s6
    s3 -. "select (backend/app/services/iter…IterationService.get_by_id)(Iteration)" .-> s7
    s3 -. "selectinload(Iteration.calendar)" .-> s8
    s3 -. "selectinload(Iteration.project)" .-> s9
    s3 -. "result.scalar_one_or_none (backend/app/services/iter…IterationService.get_by_id)(data not statically known)" .-> s10
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s11
    s1 -->|"_not_found_detail(db, 'iteration', iteration_id)"| s12
    click s1 "../modules/tasks.md"
    click s2 "../modules/iteration_service.md"
    click s3 "../modules/iteration_service.md"
    click s12 "../modules/tasks.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `get_tasks` | `iteration_id: int`, `service: Annotated[TaskService, Depends(get_task_service)]`, `db: Annotated[AsyncSession, Depends(get_db, scope='function')]` | `status` | - | `...` |
| `IterationService` | - | - | - | - |
| `IterationService.get_by_id` | `iteration_id: int` | `Iteration` | - | `result.scalar_one_or_none(...)` |
| `self.db.execute (backend/app/services/iter…IterationService.get_by_id)` | - | - | - | - |
| `select(…).options(…).where` | - | - | - | - |
| `select(…).options` | - | - | - | - |
| `select (backend/app/services/iter…IterationService.get_by_id)` | - | - | - | - |
| `selectinload` | - | - | - | - |
| `selectinload` | - | - | - | - |
| `result.scalar_one_or_none (backend/app/services/iter…IterationService.get_by_id)` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `_not_found_detail` | `db: AsyncSession`, `entity: str`, `entity_id: int` | - | - | `entity_not_found_message(...)` |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| get_tasks | IterationService | 123 | `IterationService(db)` |
| get_tasks | IterationService.get_by_id | 124 | `iteration_service.get_by_id(iteration_id)` |
| IterationService.get_by_id | self.db.execute (backend/app/services/iter…IterationService.get_by_id) | 323 | `self.db.execute(...)` |
| IterationService.get_by_id | select(…).options(…).where | 324 | `select(Iteration).options(selectinload(Iteration.calendar), selectinload(Iteration.project)).where(...)` |
| IterationService.get_by_id | select(…).options | 324 | `select(Iteration).options(selectinload(...), selectinload(...))` |
| IterationService.get_by_id | select (backend/app/services/iter…IterationService.get_by_id) | 324 | `select(Iteration)` |
| IterationService.get_by_id | selectinload | 326 | `selectinload(Iteration.calendar)` |
| IterationService.get_by_id | selectinload | 327 | `selectinload(Iteration.project)` |
| IterationService.get_by_id | result.scalar_one_or_none (backend/app/services/iter…IterationService.get_by_id) | 331 | `result.scalar_one_or_none(data not statically known)` |
| get_tasks | HTTPException | 127 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| get_tasks | _not_found_detail | 129 | `_not_found_detail(db, 'iteration', iteration_id)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `IterationService.get_by_id` | `self.db.execute` | 323 |
| unresolved_call | `IterationService.get_by_id` | `select(Iteration).options(selectinload(Iteration.calendar), selectinload(Iteration.project)).where` | 324 |
| unresolved_call | `IterationService.get_by_id` | `select(Iteration).options` | 324 |
| external_call | `IterationService.get_by_id` | `select` | 324 |
| external_call | `IterationService.get_by_id` | `selectinload` | 326 |
| external_call | `IterationService.get_by_id` | `selectinload` | 327 |
| unresolved_call | `IterationService.get_by_id` | `result.scalar_one_or_none` | 331 |
| external_call | `get_tasks` | `HTTPException` | 127 |
| step_limit | `get_tasks` | `first 12 steps` | 0 |
| truncated_flow | `get_tasks` | `depth limit` | 0 |

## Behavior

This flow starts at `get_tasks` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

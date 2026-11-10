# bulk_update_tasks

**Entry point:** `bulk_update_tasks` (`http`)
**Source:** [tasks](../modules/tasks.md)
**Modules touched:** [config](../modules/config.md), [iteration_service](../modules/iteration_service.md), [language_service](../modules/language_service.md), [schemas_task](../modules/schemas_task.md), and 3 more

**Complete modules touched:**

- [config](../modules/config.md)
- [iteration_service](../modules/iteration_service.md)
- [language_service](../modules/language_service.md)
- [schemas_task](../modules/schemas_task.md)
- [system_settings_service](../modules/system_settings_service.md)
- [tasks](../modules/tasks.md)
- [url_policy](../modules/url_policy.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as bulk_update_tasks
    participant p1 as _not_found_detail
    participant p2 as _localized_detail
    participant p3 as IterationService
    participant p4 as IterationService.get_by_id
    participant p5 as TasksImportResponse
    participant p6 as resolve_runtime_ui_language
    participant p7 as entity_not_found_message
    participant p8 as backend_error_message
    participant p9 as RuntimeSettingsService.get_app_settings
    participant p10 as localized
    participant p11 as get_settings
    participant p12 as scoped_entity_not_found_message
    participant p13 as entity_deleted_message
    participant p14 as RuntimeSettingsService.resolve
    participant p15 as RuntimeSettingsService._definition
    participant p16 as RuntimeSettingsService._decrypt_secret
    participant p17 as RuntimeSettingsService._coerce
    participant p18 as normalize_language
    participant p19 as RuntimeSettingsService
    participant p20 as Settings
    participant p21 as RuntimeSettingsService._row
    participant p22 as RuntimeSettingsService._env_value
    participant p23 as RuntimeSettingsError
    participant p24 as RuntimeSettingsService._fernet
    participant p25 as RuntimeSettingsEncryptionError
    participant p26 as normalize_provider_api_url
    participant p27 as HTTPException
    participant p28 as service.bulk_update_tasks_from_text
    participant p29 as len
    p0->>p1: _not_found_detail
    p0->>p2: _localized_detail
    p0->>p3: IterationService
    p0->>p4: IterationService.get_by_id
    p0->>p5: TasksImportResponse
    p1->>p6: resolve_runtime_ui_language
    p1->>p7: entity_not_found_message
    p2->>p8: backend_error_message
    p6->>p9: RuntimeSettingsService.get_app_settings
    p7->>p10: localized
    p6->>p11: get_settings
    p8->>p12: scoped_entity_not_found_message
    p8->>p13: entity_deleted_message
    p9->>p14: RuntimeSettingsService.resolve
    p14->>p15: RuntimeSettingsService._definition
    p14->>p16: RuntimeSettingsService._decrypt_secret
    p14->>p17: RuntimeSettingsService._coerce
    p6->>p18: normalize_language
    p6->>p19: RuntimeSettingsService
    p11->>p20: Settings
    p14->>p21: RuntimeSettingsService._row
    p14->>p22: RuntimeSettingsService._env_value
    p15->>p23: RuntimeSettingsError
    p16->>p24: RuntimeSettingsService._fernet
    p16->>p25: RuntimeSettingsEncryptionError
    p17->>p26: normalize_provider_api_url
    p0-->>p27: HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)
    p0-->>p28: service.bulk_update_tasks_from_text(iteration_id, data.text, data.destination, expected_revision=data.expected_revision)
    p0-->>p29: len(tasks)
    p0-->>p29: len(triage_items)
```

> Call sequence diagram shows 30 of 181 interactions; 151 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 3 of 54 (51 omitted); unresolved 1 of 76 (75 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/services/iteration_service.py:IterationService.get_by_id` | 3 | - | unresolved | 4 |
| `backend/app/services/iteration_service.py:IterationService.get_by_id` | 3 | - | external | 3 |
| `backend/app/services/language_service.py:normalize_language` | 14 | - | unresolved | 2 |
| `backend/app/services/language_service.py:normalize_language` | 14 | - | external | 1 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._definition` | 20 | - | unresolved | 1 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._row` | 23 | - | unresolved | 3 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._row` | 23 | - | external | 1 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._decrypt_secret` | 28 | - | unresolved | 3 |
> Omission summary shows 8 of 31 groups; 23 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 52; effect analysis evaluated: 31, partial: 1, unavailable: 20. Counts include steps omitted from the displayed trace.

Collector observations for 32 source steps with known totals: observed: 164, emitted: 138, omitted: 26. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector omitted observations before flow assembly; displayed effects are partial.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `bulk_update_tasks` | `available` | `evaluated` | `available` | `7` | `7` | `0` |
| `IterationService` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `IterationService.get_by_id` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `self.db.execute (backend/app/services/iter…terationService.get_by_id)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select(…).options(…).where` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select(…).options` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select (backend/app/services/iter…terationService.get_by_id)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `selectinload` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `selectinload` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `result.scalar_one_or_none (backend/app/services/iter…terationService.get_by_id)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `_not_found_detail` | `available` | `evaluated` | `available` | `4` | `4` | `0` |

```mermaid
flowchart LR
    s1["1. bulk_update_tasks"]
    s2["2. IterationService"]
    s3["3. IterationService.get_by_id"]
    s4["4. self.db.execute (backend/app/services/iter…terationService.get_by_id)"]
    s5["5. select(…).options(…).where"]
    s6["6. select(…).options"]
    s7["7. select (backend/app/services/iter…terationService.get_by_id)"]
    s8["8. selectinload"]
    s9["9. selectinload"]
    s10["10. result.scalar_one_or_none (backend/app/services/iter…terationService.get_by_id)"]
    s11["11. HTTPException"]
    s12["12. _not_found_detail"]
    s1 -->|"IterationService(db)"| s2
    s1 -->|"IterationService.get_by_id(iteration_id)"| s3
    s3 -. "self.db.execute (backend/app/services/iter…terationService.get_by_id)(...)" .-> s4
    s3 -. "select(…).options(…).where(...)" .-> s5
    s3 -. "select(…).options(selectinload(...), selectinload(...))" .-> s6
    s3 -. "select (backend/app/services/iter…terationService.get_by_id)(Iteration)" .-> s7
    s3 -. "selectinload(Iteration.calendar)" .-> s8
    s3 -. "selectinload(Iteration.project)" .-> s9
    s3 -. "result.scalar_one_or_none (backend/app/services/iter…terationService.get_by_id)(data not statically known)" .-> s10
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
| `bulk_update_tasks` | `iteration_id: int`, `data: TasksImportRequest`, `service: Annotated[TaskService, Depends(get_task_service)]`, `db: Annotated[AsyncSession, Depends(get_db, scope='function')]` | `status`, `status` | - | `TasksImportResponse(...)` |
| `IterationService` | - | - | - | - |
| `IterationService.get_by_id` | `iteration_id: int` | `Iteration` | - | `result.scalar_one_or_none(...)` |
| `self.db.execute (backend/app/services/iter…terationService.get_by_id)` | - | - | - | - |
| `select(…).options(…).where` | - | - | - | - |
| `select(…).options` | - | - | - | - |
| `select (backend/app/services/iter…terationService.get_by_id)` | - | - | - | - |
| `selectinload` | - | - | - | - |
| `selectinload` | - | - | - | - |
| `result.scalar_one_or_none (backend/app/services/iter…terationService.get_by_id)` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `_not_found_detail` | `db: AsyncSession`, `entity: str`, `entity_id: int` | - | - | `entity_not_found_message(...)` |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| bulk_update_tasks | IterationService | 867 | `IterationService(db)` |
| bulk_update_tasks | IterationService.get_by_id | 868 | `iteration_service.get_by_id(iteration_id)` |
| IterationService.get_by_id | self.db.execute (backend/app/services/iter…terationService.get_by_id) | 323 | `self.db.execute(...)` |
| IterationService.get_by_id | select(…).options(…).where | 324 | `select(Iteration).options(selectinload(Iteration.calendar), selectinload(Iteration.project)).where(...)` |
| IterationService.get_by_id | select(…).options | 324 | `select(Iteration).options(selectinload(...), selectinload(...))` |
| IterationService.get_by_id | select (backend/app/services/iter…terationService.get_by_id) | 324 | `select(Iteration)` |
| IterationService.get_by_id | selectinload | 326 | `selectinload(Iteration.calendar)` |
| IterationService.get_by_id | selectinload | 327 | `selectinload(Iteration.project)` |
| IterationService.get_by_id | result.scalar_one_or_none (backend/app/services/iter…terationService.get_by_id) | 331 | `result.scalar_one_or_none(data not statically known)` |
| bulk_update_tasks | HTTPException | 871 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| bulk_update_tasks | _not_found_detail | 873 | `_not_found_detail(db, 'iteration', iteration_id)` |

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
| external_call | `bulk_update_tasks` | `HTTPException` | 871 |
| step_limit | `bulk_update_tasks` | `first 12 steps` | 0 |
| truncated_flow | `bulk_update_tasks` | `depth limit` | 0 |

## Behavior

This flow starts at `bulk_update_tasks` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

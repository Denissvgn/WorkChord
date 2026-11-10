# list_project_iterations

**Entry point:** `list_project_iterations` (`http`)
**Source:** [projects](../modules/projects.md)
**Modules touched:** [calendar_service](../modules/calendar_service.md), [config](../modules/config.md), [iteration_service](../modules/iteration_service.md), [language_service](../modules/language_service.md), and 5 more

**Complete modules touched:**

- [calendar_service](../modules/calendar_service.md)
- [config](../modules/config.md)
- [iteration_service](../modules/iteration_service.md)
- [language_service](../modules/language_service.md)
- [projects](../modules/projects.md)
- [schemas_calendar](../modules/schemas_calendar.md)
- [schemas_iteration](../modules/schemas_iteration.md)
- [system_settings_service](../modules/system_settings_service.md)
- [url_policy](../modules/url_policy.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as list_project_iterations
    participant p1 as _not_found_detail
    participant p2 as IterationService.to_response
    participant p3 as IterationService
    participant p4 as resolve_runtime_ui_language
    participant p5 as entity_not_found_message
    participant p6 as CalendarService.calculate_working_days
    participant p7 as RuntimeSettingsService.get_app_settings
    participant p8 as localized
    participant p9 as get_settings
    participant p10 as RuntimeSettingsService.resolve
    participant p11 as RuntimeSettingsService._definition
    participant p12 as RuntimeSettingsService._decrypt_secret
    participant p13 as RuntimeSettingsService._coerce
    participant p14 as CalendarService
    participant p15 as IterationResponse
    participant p16 as IterationService._response_project
    participant p17 as normalize_language
    participant p18 as RuntimeSettingsService
    participant p19 as WorkingDaysResponse
    participant p20 as Settings
    participant p21 as RuntimeSettingsService._row
    participant p22 as RuntimeSettingsService._env_value
    participant p23 as RuntimeSettingsError
    participant p24 as RuntimeSettingsService._fernet
    participant p25 as RuntimeSettingsEncryptionError
    participant p26 as normalize_provider_api_url
    participant p27 as HTTPException
    participant p28 as service.list_iterations
    participant p29 as _RESOURCE_LABELS.get
    participant p30 as set
    p0->>p1: _not_found_detail
    p0->>p2: IterationService.to_response
    p0->>p3: IterationService
    p1->>p4: resolve_runtime_ui_language
    p1->>p5: entity_not_found_message
    p2->>p6: CalendarService.calculate_working_days
    p4->>p7: RuntimeSettingsService.get_app_settings
    p5->>p8: localized
    p4->>p9: get_settings
    p7->>p10: RuntimeSettingsService.resolve
    p10->>p11: RuntimeSettingsService._definition
    p10->>p12: RuntimeSettingsService._decrypt_secret
    p10->>p13: RuntimeSettingsService._coerce
    p2->>p14: CalendarService
    p2->>p15: IterationResponse
    p2->>p16: IterationService._response_project
    p4->>p17: normalize_language
    p4->>p18: RuntimeSettingsService
    p6->>p19: WorkingDaysResponse
    p9->>p20: Settings
    p10->>p21: RuntimeSettingsService._row
    p10->>p22: RuntimeSettingsService._env_value
    p11->>p23: RuntimeSettingsError
    p12->>p24: RuntimeSettingsService._fernet
    p12->>p25: RuntimeSettingsEncryptionError
    p13->>p26: normalize_provider_api_url
    p0-->>p27: HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)
    p0-->>p28: service.list_iterations(project_id)
    p5-->>p29: _RESOURCE_LABELS.get(entity, (...))
    p6-->>p30: set(...)
```

> Call sequence diagram shows 30 of 83 interactions; 53 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 2 of 19 (17 omitted); unresolved 2 of 18 (16 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/services/language_service.py:normalize_language` | 6 | - | unresolved | 2 |
| `backend/app/services/language_service.py:normalize_language` | 6 | - | external | 1 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._definition` | 12 | - | unresolved | 1 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._row` | 15 | - | unresolved | 3 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._row` | 15 | - | external | 1 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._decrypt_secret` | 20 | - | unresolved | 3 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._coerce` | 26 | - | external | 8 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._coerce` | 26 | [backend/app/services/system_settings_service.py](../modules/system_settings_service.md) | internal | 14 |
> Omission summary shows 8 of 21 groups; 13 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 47; effect analysis evaluated: 25, partial: 0, unavailable: 22. Counts include steps omitted from the displayed trace.

Collector observations for 25 source steps with known totals: observed: 96, emitted: 96, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `list_project_iterations` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `service.list_iterations` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `_not_found_detail` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `resolve_runtime_ui_language` | `available` | `evaluated` | `available` | `5` | `5` | `0` |
| `normalize_language` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `str(…).strip().lower` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str(…).strip (backend/app/services/lang…vice.py:normalize_language)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str (backend/app/services/lang…vice.py:normalize_language)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `RuntimeSettingsService.get_app_settings` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `RuntimeSettingsService.resolve` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `RuntimeSettingsService._definition` | `available` | `evaluated` | `available` | `2` | `2` | `0` |

```mermaid
flowchart LR
    s1["1. list_project_iterations"]
    s2["2. service.list_iterations"]
    s3["3. HTTPException"]
    s4["4. _not_found_detail"]
    s5["5. resolve_runtime_ui_language"]
    s6["6. normalize_language"]
    s7["7. str(…).strip().lower"]
    s8["8. str(…).strip (backend/app/services/lang…vice.py:normalize_language)"]
    s9["9. str (backend/app/services/lang…vice.py:normalize_language)"]
    s10["10. RuntimeSettingsService.get_app_settings"]
    s11["11. RuntimeSettingsService.resolve"]
    s12["12. RuntimeSettingsService._definition"]
    s1 -. "service.list_iterations(project_id)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s3
    s1 -->|"_not_found_detail(service, 'project', project_id)"| s4
    s4 -->|"resolve_runtime_ui_language(service.db)"| s5
    s5 -->|"normalize_language(default)"| s6
    s6 -. "str(…).strip().lower(data not statically known)" .-> s7
    s6 -. "str(…).strip (backend/app/services/lang…vice.py:normalize_language)(data not statically known)" .-> s8
    s6 -. "str (backend/app/services/lang…vice.py:normalize_language)(...)" .-> s9
    s5 -->|"RuntimeSettingsService.get_app_settings(data not statically known)"| s10
    s10 -->|"RuntimeSettingsService.resolve('app.ui_language')"| s11
    s11 -->|"RuntimeSettingsService._definition(key)"| s12
    click s1 "../modules/projects.md"
    click s4 "../modules/projects.md"
    click s5 "../modules/language_service.md"
    click s6 "../modules/language_service.md"
    click s10 "../modules/system_settings_service.md"
    click s11 "../modules/system_settings_service.md"
    click s12 "../modules/system_settings_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `list_project_iterations` | `project_id: int`, `service: Annotated[ProjectService, Depends(get_project_service)]` | `status` | - | `...` |
| `service.list_iterations` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `_not_found_detail` | `service: Any`, `entity: str`, `entity_id: int` | - | - | `entity_not_found_message(...)` |
| `resolve_runtime_ui_language` | `db: Any`, `default: LanguageCode \| None` | - | - | `normalize_language(...)`, `normalize_language(...)`, `fallback` |
| `normalize_language` | `value: Any`, `default: LanguageCode` | - | - | `normalized`, `default` |
| `str(…).strip().lower` | - | - | - | - |
| `str(…).strip (backend/app/services/lang…vice.py:normalize_language)` | - | - | - | - |
| `str (backend/app/services/lang…vice.py:normalize_language)` | - | - | - | - |
| `RuntimeSettingsService.get_app_settings` | - | - | - | `SimpleNamespace(...)` |
| `RuntimeSettingsService.resolve` | `key: str` | - | - | `(...)`, `(...)`, `(...)` |
| `RuntimeSettingsService._definition` | `key: str` | - | - | `definition` |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| list_project_iterations | service.list_iterations | 398 | `service.list_iterations(project_id)` |
| list_project_iterations | HTTPException | 400 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| list_project_iterations | _not_found_detail | 402 | `_not_found_detail(service, 'project', project_id)` |
| _not_found_detail | resolve_runtime_ui_language | 73 | `resolve_runtime_ui_language(service.db)` |
| resolve_runtime_ui_language | normalize_language | 406 | `normalize_language(default)` |
| normalize_language | str(…).strip().lower | 35 | `str(value or '').strip().lower(data not statically known)` |
| normalize_language | str(…).strip (backend/app/services/lang…vice.py:normalize_language) | 35 | `str(value or '').strip(data not statically known)` |
| normalize_language | str (backend/app/services/lang…vice.py:normalize_language) | 35 | `str(...)` |
| resolve_runtime_ui_language | RuntimeSettingsService.get_app_settings | 411 | `RuntimeSettingsService(db).get_app_settings(data not statically known)` |
| RuntimeSettingsService.get_app_settings | RuntimeSettingsService.resolve | 337 | `self.resolve('app.ui_language')` |
| RuntimeSettingsService.resolve | RuntimeSettingsService._definition | 284 | `self._definition(key)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `list_project_iterations` | `service.list_iterations` | 398 |
| external_call | `list_project_iterations` | `HTTPException` | 400 |
| unresolved_call | `normalize_language` | `str(value or '').strip().lower` | 35 |
| unresolved_call | `normalize_language` | `str(value or '').strip` | 35 |
| step_limit | `list_project_iterations` | `first 12 steps` | 0 |
| truncated_flow | `list_project_iterations` | `depth limit` | 0 |

## Behavior

This flow starts at `list_project_iterations` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

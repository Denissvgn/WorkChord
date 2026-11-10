# update_project_milestone

**Entry point:** `update_project_milestone` (`http`)
**Source:** [projects](../modules/projects.md)
**Modules touched:** [config](../modules/config.md), [language_service](../modules/language_service.md), [projects](../modules/projects.md), [system_settings_service](../modules/system_settings_service.md), and 1 more

**Complete modules touched:**

- [config](../modules/config.md)
- [language_service](../modules/language_service.md)
- [projects](../modules/projects.md)
- [system_settings_service](../modules/system_settings_service.md)
- [url_policy](../modules/url_policy.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as update_project_milestone
    participant p1 as _scoped_not_found_detail
    participant p2 as resolve_runtime_ui_language
    participant p3 as scoped_entity_not_found_message
    participant p4 as RuntimeSettingsService.get_app_settings
    participant p5 as localized
    participant p6 as get_settings
    participant p7 as RuntimeSettingsService.resolve
    participant p8 as RuntimeSettingsService._definition
    participant p9 as RuntimeSettingsService._decrypt_secret
    participant p10 as RuntimeSettingsService._coerce
    participant p11 as normalize_language
    participant p12 as RuntimeSettingsService
    participant p13 as Settings
    participant p14 as RuntimeSettingsService._row
    participant p15 as RuntimeSettingsService._env_value
    participant p16 as RuntimeSettingsError
    participant p17 as RuntimeSettingsService._fernet
    participant p18 as RuntimeSettingsEncryptionError
    participant p19 as normalize_provider_api_url
    participant p20 as HTTPException
    participant p21 as service.update_milestone
    participant p22 as _RESOURCE_LABELS.get
    participant p23 as scope_en.lower
    participant p24 as getattr (backend/app/services/lang…esolve_runtime_ui_language)
    participant p25 as scope_ru.lower
    participant p26 as logger.warning
    participant p27 as str(…).strip().lower
    p0->>p1: _scoped_not_found_detail
    p1->>p2: resolve_runtime_ui_language
    p1->>p3: scoped_entity_not_found_message
    p2->>p4: RuntimeSettingsService.get_app_settings
    p3->>p5: localized
    p2->>p6: get_settings
    p4->>p7: RuntimeSettingsService.resolve
    p7->>p8: RuntimeSettingsService._definition
    p7->>p9: RuntimeSettingsService._decrypt_secret
    p7->>p10: RuntimeSettingsService._coerce
    p2->>p11: normalize_language
    p2->>p12: RuntimeSettingsService
    p6->>p13: Settings
    p7->>p14: RuntimeSettingsService._row
    p7->>p15: RuntimeSettingsService._env_value
    p8->>p16: RuntimeSettingsError
    p9->>p17: RuntimeSettingsService._fernet
    p9->>p18: RuntimeSettingsEncryptionError
    p10->>p19: normalize_provider_api_url
    p0-->>p20: HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)
    p0-->>p21: service.update_milestone(project_id, milestone_id, data)
    p3-->>p22: _RESOURCE_LABELS.get(entity, (...))
    p3-->>p22: _RESOURCE_LABELS.get(scope, (...))
    p3-->>p23: scope_en.lower
    p2-->>p24: getattr (backend/app/services/lang…esolve_runtime_ui_language)(settings, 'app_ui_language', None)
    p3-->>p25: scope_ru.lower
    p2-->>p26: logger.warning('Unable to resolve DB-backed runtime UI language using fallback', exc_info=True)
    p2-->>p24: getattr (backend/app/services/lang…esolve_runtime_ui_language)(get_settings(...), 'app_ui_language', None)
    p2-->>p26: logger.warning('Unable to resolve environment-backed UI language using fallback', exc_info=True)
    p11-->>p27: str(…).strip().lower
```

> Call sequence diagram shows 30 of 71 interactions; 41 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 3 of 15 (12 omitted); unresolved 8 of 17 (9 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/services/language_service.py:normalize_language` | 6 | - | unresolved | 1 |
| `backend/app/services/language_service.py:normalize_language` | 6 | - | external | 1 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._definition` | 12 | - | unresolved | 1 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._row` | 15 | - | unresolved | 3 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._row` | 15 | - | external | 1 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._decrypt_secret` | 20 | - | unresolved | 3 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._coerce` | 26 | - | external | 8 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._coerce` | 26 | [backend/app/services/system_settings_service.py](../modules/system_settings_service.md) | internal | 14 |
> Omission summary shows 8 of 16 groups; 8 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 40; effect analysis evaluated: 22, partial: 0, unavailable: 18. Counts include steps omitted from the displayed trace.

Collector observations for 22 source steps with known totals: observed: 90, emitted: 90, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `update_project_milestone` | `available` | `evaluated` | `available` | `6` | `6` | `0` |
| `service.update_milestone` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `_scoped_not_found_detail` | `available` | `evaluated` | `available` | `6` | `6` | `0` |
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
    s1["1. update_project_milestone"]
    s2["2. service.update_milestone"]
    s3["3. HTTPException"]
    s4["4. _scoped_not_found_detail"]
    s5["5. resolve_runtime_ui_language"]
    s6["6. normalize_language"]
    s7["7. str(…).strip().lower"]
    s8["8. str(…).strip (backend/app/services/lang…vice.py:normalize_language)"]
    s9["9. str (backend/app/services/lang…vice.py:normalize_language)"]
    s10["10. RuntimeSettingsService.get_app_settings"]
    s11["11. RuntimeSettingsService.resolve"]
    s12["12. RuntimeSettingsService._definition"]
    s1 -. "service.update_milestone(project_id, milestone_id, data)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s3
    s1 -->|"_scoped_not_found_detail(service, 'milestone', milestone_id, 'project', project_id)"| s4
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
| `update_project_milestone` | `project_id: int`, `milestone_id: int`, `data: ProjectMilestoneUpdate`, `service: Annotated[ProjectService, Depends(get_project_service)]` | `status` | - | `milestone` |
| `service.update_milestone` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `_scoped_not_found_detail` | `service: Any`, `entity: str`, `entity_id: int`, `scope: str`, `scope_id: int` | - | - | `scoped_entity_not_found_message(...)` |
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
| update_project_milestone | service.update_milestone | 356 | `service.update_milestone(project_id, milestone_id, data)` |
| update_project_milestone | HTTPException | 358 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| update_project_milestone | _scoped_not_found_detail | 360 | `_scoped_not_found_detail(service, 'milestone', milestone_id, 'project', project_id)` |
| _scoped_not_found_detail | resolve_runtime_ui_language | 84 | `resolve_runtime_ui_language(service.db)` |
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
| unresolved_call | `update_project_milestone` | `service.update_milestone` | 356 |
| external_call | `update_project_milestone` | `HTTPException` | 358 |
| unresolved_call | `normalize_language` | `str(value or '').strip().lower` | 35 |
| unresolved_call | `normalize_language` | `str(value or '').strip` | 35 |
| step_limit | `update_project_milestone` | `first 12 steps` | 0 |
| truncated_flow | `update_project_milestone` | `depth limit` | 0 |

## Behavior

This flow starts at `update_project_milestone` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

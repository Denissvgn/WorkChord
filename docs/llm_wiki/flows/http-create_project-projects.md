# create_project

**Entry point:** `create_project` (`http`)
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
    participant p0 as create_project
    participant p1 as _localized_detail
    participant p2 as resolve_runtime_ui_language
    participant p3 as backend_error_message
    participant p4 as RuntimeSettingsService.get_app_settings
    participant p5 as entity_not_found_message
    participant p6 as get_settings
    participant p7 as scoped_entity_not_found_message
    participant p8 as entity_deleted_message
    participant p9 as RuntimeSettingsService.resolve
    participant p10 as localized
    participant p11 as RuntimeSettingsService._definition
    participant p12 as RuntimeSettingsService._decrypt_secret
    participant p13 as RuntimeSettingsService._coerce
    participant p14 as normalize_language
    participant p15 as RuntimeSettingsService
    participant p16 as Settings
    participant p17 as RuntimeSettingsService._row
    participant p18 as RuntimeSettingsService._env_value
    participant p19 as RuntimeSettingsError
    participant p20 as RuntimeSettingsService._fernet
    participant p21 as RuntimeSettingsEncryptionError
    participant p22 as normalize_provider_api_url
    participant p23 as HTTPException
    participant p24 as service.create
    participant p25 as str (backend/app/routers/projects.py:create_project)
    participant p26 as message.lower
    participant p27 as re.fullmatch
    participant p28 as match.groups
    participant p29 as getattr (backend/app/services/lang…solve_runtime_ui_language)
    participant p30 as label.strip().lower().replace
    p0->>p1: _localized_detail
    p1->>p2: resolve_runtime_ui_language
    p1->>p3: backend_error_message
    p2->>p4: RuntimeSettingsService.get_app_settings
    p3->>p5: entity_not_found_message
    p2->>p6: get_settings
    p3->>p7: scoped_entity_not_found_message
    p3->>p8: entity_deleted_message
    p4->>p9: RuntimeSettingsService.resolve
    p5->>p10: localized
    p9->>p11: RuntimeSettingsService._definition
    p9->>p12: RuntimeSettingsService._decrypt_secret
    p9->>p13: RuntimeSettingsService._coerce
    p2->>p14: normalize_language
    p2->>p15: RuntimeSettingsService
    p6->>p16: Settings
    p9->>p17: RuntimeSettingsService._row
    p9->>p18: RuntimeSettingsService._env_value
    p11->>p19: RuntimeSettingsError
    p12->>p20: RuntimeSettingsService._fernet
    p12->>p21: RuntimeSettingsEncryptionError
    p13->>p22: normalize_provider_api_url
    p0-->>p23: HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=...)
    p0-->>p24: service.create(data)
    p0-->>p25: str (backend/app/routers/projects.py:create_project)(e)
    p3-->>p26: message.lower
    p3-->>p27: re.fullmatch('(.+) with id ([^ ]+) not found', message)
    p3-->>p28: match.groups
    p2-->>p29: getattr (backend/app/services/lang…solve_runtime_ui_language)(settings, 'app_ui_language', None)
    p3-->>p30: label.strip().lower().replace(' ', '_')
```

> Call sequence diagram shows 30 of 161 interactions; 131 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 4 of 46 (42 omitted); unresolved 4 of 70 (66 omitted). These counts cover the captured static trace.

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
> Omission summary shows 8 of 26 groups; 18 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 46; effect analysis evaluated: 27, partial: 1, unavailable: 18. Counts include steps omitted from the displayed trace.

Collector observations for 28 source steps with known totals: observed: 145, emitted: 119, omitted: 26. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector omitted observations before flow assembly; displayed effects are partial.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `create_project` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `service.create` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `_localized_detail` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `resolve_runtime_ui_language` | `available` | `evaluated` | `available` | `5` | `5` | `0` |
| `normalize_language` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `str(…).strip().lower` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str(…).strip (backend/app/services/lang…ice.py:normalize_language)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str (backend/app/services/lang…ice.py:normalize_language)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `RuntimeSettingsService.get_app_settings` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `RuntimeSettingsService.resolve` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `RuntimeSettingsService._definition` | `available` | `evaluated` | `available` | `2` | `2` | `0` |

```mermaid
flowchart LR
    s1["1. create_project"]
    s2["2. service.create"]
    s3["3. HTTPException"]
    s4["4. _localized_detail"]
    s5["5. resolve_runtime_ui_language"]
    s6["6. normalize_language"]
    s7["7. str(…).strip().lower"]
    s8["8. str(…).strip (backend/app/services/lang…ice.py:normalize_language)"]
    s9["9. str (backend/app/services/lang…ice.py:normalize_language)"]
    s10["10. RuntimeSettingsService.get_app_settings"]
    s11["11. RuntimeSettingsService.resolve"]
    s12["12. RuntimeSettingsService._definition"]
    s1 -. "service.create(data)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=...)" .-> s3
    s1 -->|"_localized_detail(service, str(...))"| s4
    s4 -->|"resolve_runtime_ui_language(service.db)"| s5
    s5 -->|"normalize_language(default)"| s6
    s6 -. "str(…).strip().lower(data not statically known)" .-> s7
    s6 -. "str(…).strip (backend/app/services/lang…ice.py:normalize_language)(data not statically known)" .-> s8
    s6 -. "str (backend/app/services/lang…ice.py:normalize_language)(...)" .-> s9
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
| `create_project` | `data: ProjectCreate`, `service: Annotated[ProjectService, Depends(get_project_service)]` | `status` | - | `...` |
| `service.create` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `_localized_detail` | `service: Any`, `message: str` | - | - | `backend_error_message(...)` |
| `resolve_runtime_ui_language` | `db: Any`, `default: LanguageCode \| None` | - | - | `normalize_language(...)`, `normalize_language(...)`, `fallback` |
| `normalize_language` | `value: Any`, `default: LanguageCode` | - | - | `normalized`, `default` |
| `str(…).strip().lower` | - | - | - | - |
| `str(…).strip (backend/app/services/lang…ice.py:normalize_language)` | - | - | - | - |
| `str (backend/app/services/lang…ice.py:normalize_language)` | - | - | - | - |
| `RuntimeSettingsService.get_app_settings` | - | - | - | `SimpleNamespace(...)` |
| `RuntimeSettingsService.resolve` | `key: str` | - | - | `(...)`, `(...)`, `(...)` |
| `RuntimeSettingsService._definition` | `key: str` | - | - | `definition` |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| create_project | service.create | 218 | `service.create(data)` |
| create_project | HTTPException | 220 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=...)` |
| create_project | _localized_detail | 222 | `_localized_detail(service, str(...))` |
| _localized_detail | resolve_runtime_ui_language | 68 | `resolve_runtime_ui_language(service.db)` |
| resolve_runtime_ui_language | normalize_language | 406 | `normalize_language(default)` |
| normalize_language | str(…).strip().lower | 35 | `str(value or '').strip().lower(data not statically known)` |
| normalize_language | str(…).strip (backend/app/services/lang…ice.py:normalize_language) | 35 | `str(value or '').strip(data not statically known)` |
| normalize_language | str (backend/app/services/lang…ice.py:normalize_language) | 35 | `str(...)` |
| resolve_runtime_ui_language | RuntimeSettingsService.get_app_settings | 411 | `RuntimeSettingsService(db).get_app_settings(data not statically known)` |
| RuntimeSettingsService.get_app_settings | RuntimeSettingsService.resolve | 337 | `self.resolve('app.ui_language')` |
| RuntimeSettingsService.resolve | RuntimeSettingsService._definition | 284 | `self._definition(key)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `create_project` | `service.create` | 218 |
| external_call | `create_project` | `HTTPException` | 220 |
| unresolved_call | `normalize_language` | `str(value or '').strip().lower` | 35 |
| unresolved_call | `normalize_language` | `str(value or '').strip` | 35 |
| step_limit | `create_project` | `first 12 steps` | 0 |
| truncated_flow | `create_project` | `depth limit` | 0 |

## Behavior

This flow starts at `create_project` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

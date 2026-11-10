# get_template

**Entry point:** `get_template` (`http`)
**Source:** [templates](../modules/templates.md)
**Modules touched:** [config](../modules/config.md), [language_service](../modules/language_service.md), [system_settings_service](../modules/system_settings_service.md), [templates](../modules/templates.md), and 1 more

**Complete modules touched:**

- [config](../modules/config.md)
- [language_service](../modules/language_service.md)
- [system_settings_service](../modules/system_settings_service.md)
- [templates](../modules/templates.md)
- [url_policy](../modules/url_policy.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as get_template
    participant p1 as resolve_runtime_ui_language
    participant p2 as entity_not_found_message
    participant p3 as RuntimeSettingsService.get_app_settings
    participant p4 as localized
    participant p5 as RuntimeSettingsService.resolve
    participant p6 as RuntimeSettingsService._definition
    participant p7 as RuntimeSettingsService._decrypt_secret
    participant p8 as RuntimeSettingsService._coerce
    participant p9 as RuntimeSettingsService._fernet
    participant p10 as normalize_provider_api_url
    participant p11 as normalize_language
    participant p12 as RuntimeSettingsService
    participant p13 as get_settings
    participant p14 as RuntimeSettingsService._row
    participant p15 as RuntimeSettingsService._env_value
    participant p16 as RuntimeSettingsError
    participant p17 as RuntimeSettingsEncryptionError
    participant p18 as normalize_external_http_url
    participant p19 as HTTPException
    participant p20 as service.get_by_id
    participant p21 as _RESOURCE_LABELS.get
    participant p22 as getattr (backend/app/services/lang…esolve_runtime_ui_language)
    participant p23 as logger.warning
    participant p24 as str(…).strip().lower
    participant p25 as str(…).strip (backend/app/services/lang…vice.py:normalize_language)
    participant p26 as str (backend/app/services/lang…vice.py:normalize_language)
    participant p27 as SimpleNamespace
    participant p28 as SETTING_DEFINITIONS.get
    p0->>p1: resolve_runtime_ui_language
    p0->>p2: entity_not_found_message
    p1->>p3: RuntimeSettingsService.get_app_settings
    p2->>p4: localized
    p3->>p5: RuntimeSettingsService.resolve
    p5->>p6: RuntimeSettingsService._definition
    p5->>p7: RuntimeSettingsService._decrypt_secret
    p5->>p8: RuntimeSettingsService._coerce
    p7->>p9: RuntimeSettingsService._fernet
    p8->>p10: normalize_provider_api_url
    p1->>p11: normalize_language
    p1->>p12: RuntimeSettingsService
    p1->>p13: get_settings
    p5->>p14: RuntimeSettingsService._row
    p5->>p15: RuntimeSettingsService._env_value
    p6->>p16: RuntimeSettingsError
    p7->>p17: RuntimeSettingsEncryptionError
    p10->>p18: normalize_external_http_url
    p0-->>p19: HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=entity_not_found_message(...))
    p0-->>p20: service.get_by_id(template_id)
    p2-->>p21: _RESOURCE_LABELS.get(entity, (...))
    p1-->>p22: getattr (backend/app/services/lang…esolve_runtime_ui_language)(settings, 'app_ui_language', None)
    p1-->>p23: logger.warning('Unable to resolve DB-backed runtime UI language using fallback', exc_info=True)
    p1-->>p22: getattr (backend/app/services/lang…esolve_runtime_ui_language)(get_settings(...), 'app_ui_language', None)
    p1-->>p23: logger.warning('Unable to resolve environment-backed UI language using fallback', exc_info=True)
    p11-->>p24: str(…).strip().lower
    p11-->>p25: str(…).strip (backend/app/services/lang…vice.py:normalize_language)
    p11-->>p26: str (backend/app/services/lang…vice.py:normalize_language)(...)
    p3-->>p27: SimpleNamespace(app_ui_language=ui_language, ai_language_mode=ai_language_mode)
    p6-->>p28: SETTING_DEFINITIONS.get(key)
```

> Call sequence diagram shows 30 of 72 interactions; 42 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 5 of 17 (12 omitted); unresolved 7 of 14 (7 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._row` | 13 | - | unresolved | 3 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._row` | 13 | - | external | 1 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._decrypt_secret` | 18 | - | unresolved | 3 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._fernet` | 21 | - | external | 2 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._fernet` | 21 | [backend/app/services/system_settings_service.py](../modules/system_settings_service.md) | internal | 2 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._coerce` | 28 | - | external | 8 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._coerce` | 28 | [backend/app/services/system_settings_service.py](../modules/system_settings_service.md) | internal | 14 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._coerce` | 28 | - | unresolved | 1 |
> Omission summary shows 8 of 15 groups; 7 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 42; effect analysis evaluated: 23, partial: 0, unavailable: 19. Counts include steps omitted from the displayed trace.

Collector observations for 23 source steps with known totals: observed: 87, emitted: 87, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `get_template` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `service.get_by_id` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `resolve_runtime_ui_language` | `available` | `evaluated` | `available` | `5` | `5` | `0` |
| `normalize_language` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `str(…).strip().lower` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str(…).strip (backend/app/services/lang…vice.py:normalize_language)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str (backend/app/services/lang…vice.py:normalize_language)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `RuntimeSettingsService.get_app_settings` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `RuntimeSettingsService.resolve` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `RuntimeSettingsService._definition` | `available` | `evaluated` | `available` | `2` | `2` | `0` |
| `SETTING_DEFINITIONS.get` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `RuntimeSettingsError` | `unavailable` | `unavailable` | `unavailable` | — | — | — |

```mermaid
flowchart LR
    s1["1. get_template"]
    s2["2. service.get_by_id"]
    s3["3. resolve_runtime_ui_language"]
    s4["4. normalize_language"]
    s5["5. str(…).strip().lower"]
    s6["6. str(…).strip (backend/app/services/lang…vice.py:normalize_language)"]
    s7["7. str (backend/app/services/lang…vice.py:normalize_language)"]
    s8["8. RuntimeSettingsService.get_app_settings"]
    s9["9. RuntimeSettingsService.resolve"]
    s10["10. RuntimeSettingsService._definition"]
    s11["11. SETTING_DEFINITIONS.get"]
    s12["12. RuntimeSettingsError"]
    s1 -. "service.get_by_id(template_id)" .-> s2
    s1 -->|"resolve_runtime_ui_language(service.db)"| s3
    s3 -->|"normalize_language(default)"| s4
    s4 -. "str(…).strip().lower(data not statically known)" .-> s5
    s4 -. "str(…).strip (backend/app/services/lang…vice.py:normalize_language)(data not statically known)" .-> s6
    s4 -. "str (backend/app/services/lang…vice.py:normalize_language)(...)" .-> s7
    s3 -->|"RuntimeSettingsService.get_app_settings(data not statically known)"| s8
    s8 -->|"RuntimeSettingsService.resolve('app.ui_language')"| s9
    s9 -->|"RuntimeSettingsService._definition(key)"| s10
    s10 -. "SETTING_DEFINITIONS.get(key)" .-> s11
    s10 -->|"RuntimeSettingsError(...)"| s12
    click s1 "../modules/templates.md"
    click s3 "../modules/language_service.md"
    click s4 "../modules/language_service.md"
    click s8 "../modules/system_settings_service.md"
    click s9 "../modules/system_settings_service.md"
    click s10 "../modules/system_settings_service.md"
    click s12 "../modules/system_settings_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `get_template` | `template_id: int`, `service: Annotated[TemplateService, Depends(get_template_service)]` | `status` | - | `template` |
| `service.get_by_id` | - | - | - | - |
| `resolve_runtime_ui_language` | `db: Any`, `default: LanguageCode \| None` | - | - | `normalize_language(...)`, `normalize_language(...)`, `fallback` |
| `normalize_language` | `value: Any`, `default: LanguageCode` | - | - | `normalized`, `default` |
| `str(…).strip().lower` | - | - | - | - |
| `str(…).strip (backend/app/services/lang…vice.py:normalize_language)` | - | - | - | - |
| `str (backend/app/services/lang…vice.py:normalize_language)` | - | - | - | - |
| `RuntimeSettingsService.get_app_settings` | - | - | - | `SimpleNamespace(...)` |
| `RuntimeSettingsService.resolve` | `key: str` | - | - | `(...)`, `(...)`, `(...)` |
| `RuntimeSettingsService._definition` | `key: str` | - | - | `definition` |
| `SETTING_DEFINITIONS.get` | - | - | - | - |
| `RuntimeSettingsError` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| get_template | service.get_by_id | 59 | `service.get_by_id(template_id)` |
| get_template | resolve_runtime_ui_language | 61 | `resolve_runtime_ui_language(service.db)` |
| resolve_runtime_ui_language | normalize_language | 406 | `normalize_language(default)` |
| normalize_language | str(…).strip().lower | 35 | `str(value or '').strip().lower(data not statically known)` |
| normalize_language | str(…).strip (backend/app/services/lang…vice.py:normalize_language) | 35 | `str(value or '').strip(data not statically known)` |
| normalize_language | str (backend/app/services/lang…vice.py:normalize_language) | 35 | `str(...)` |
| resolve_runtime_ui_language | RuntimeSettingsService.get_app_settings | 411 | `RuntimeSettingsService(db).get_app_settings(data not statically known)` |
| RuntimeSettingsService.get_app_settings | RuntimeSettingsService.resolve | 337 | `self.resolve('app.ui_language')` |
| RuntimeSettingsService.resolve | RuntimeSettingsService._definition | 284 | `self._definition(key)` |
| RuntimeSettingsService._definition | SETTING_DEFINITIONS.get | 154 | `SETTING_DEFINITIONS.get(key)` |
| RuntimeSettingsService._definition | RuntimeSettingsError | 156 | `RuntimeSettingsError(...)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `get_template` | `service.get_by_id` | 59 |
| unresolved_call | `normalize_language` | `str(value or '').strip().lower` | 35 |
| unresolved_call | `normalize_language` | `str(value or '').strip` | 35 |
| unresolved_call | `RuntimeSettingsService._definition` | `SETTING_DEFINITIONS.get` | 154 |
| step_limit | `get_template` | `first 12 steps` | 0 |
| truncated_flow | `get_template` | `depth limit` | 0 |

## Behavior

This flow starts at `get_template` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

# update_label

**Entry point:** `update_label` (`http`)
**Source:** [labels](../modules/labels.md)
**Modules touched:** [config](../modules/config.md), [labels](../modules/labels.md), [language_service](../modules/language_service.md), [system_settings_service](../modules/system_settings_service.md), and 1 more

**Complete modules touched:**

- [config](../modules/config.md)
- [labels](../modules/labels.md)
- [language_service](../modules/language_service.md)
- [system_settings_service](../modules/system_settings_service.md)
- [url_policy](../modules/url_policy.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as update_label
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
    participant p20 as service.update_label
    participant p21 as str (backend/app/routers/labels.py:update_label)
    participant p22 as _RESOURCE_LABELS.get
    participant p23 as getattr (backend/app/services/lang…esolve_runtime_ui_language)
    participant p24 as logger.warning
    participant p25 as str(…).strip().lower
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
    p0-->>p19: HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(...))
    p0-->>p20: service.update_label(label_id, data)
    p0-->>p21: str (backend/app/routers/labels.py:update_label)(exc)
    p0-->>p19: HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))
    p0-->>p21: str (backend/app/routers/labels.py:update_label)(exc)
    p0-->>p19: HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=entity_not_found_message(...))
    p2-->>p22: _RESOURCE_LABELS.get(entity, (...))
    p1-->>p23: getattr (backend/app/services/lang…esolve_runtime_ui_language)(settings, 'app_ui_language', None)
    p1-->>p24: logger.warning('Unable to resolve DB-backed runtime UI language using fallback', exc_info=True)
    p1-->>p23: getattr (backend/app/services/lang…esolve_runtime_ui_language)(get_settings(...), 'app_ui_language', None)
    p1-->>p24: logger.warning('Unable to resolve environment-backed UI language using fallback', exc_info=True)
    p11-->>p25: str(…).strip().lower
```

> Call sequence diagram shows 30 of 76 interactions; 46 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 7 of 21 (14 omitted); unresolved 5 of 14 (9 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/services/language_service.py:normalize_language` | 8 | - | unresolved | 1 |
| `backend/app/services/language_service.py:normalize_language` | 8 | - | external | 1 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._definition` | 14 | - | unresolved | 1 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._row` | 17 | - | unresolved | 3 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._row` | 17 | - | external | 1 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._decrypt_secret` | 22 | - | unresolved | 3 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._fernet` | 25 | - | external | 2 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._fernet` | 25 | [backend/app/services/system_settings_service.py](../modules/system_settings_service.md) | internal | 2 |
> Omission summary shows 8 of 19 groups; 11 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 42; effect analysis evaluated: 23, partial: 0, unavailable: 19. Counts include steps omitted from the displayed trace.

Collector observations for 23 source steps with known totals: observed: 91, emitted: 91, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `update_label` | `available` | `evaluated` | `available` | `8` | `8` | `0` |
| `service.update_label` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str (backend/app/routers/labels.py:update_label)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str (backend/app/routers/labels.py:update_label)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `resolve_runtime_ui_language` | `available` | `evaluated` | `available` | `5` | `5` | `0` |
| `normalize_language` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `str(…).strip().lower` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str(…).strip (backend/app/services/lang…vice.py:normalize_language)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str (backend/app/services/lang…vice.py:normalize_language)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `RuntimeSettingsService.get_app_settings` | `available` | `evaluated` | `available` | `1` | `1` | `0` |

```mermaid
flowchart LR
    s1["1. update_label"]
    s2["2. service.update_label"]
    s3["3. HTTPException"]
    s4["4. str (backend/app/routers/labels.py:update_label)"]
    s5["5. HTTPException"]
    s6["6. str (backend/app/routers/labels.py:update_label)"]
    s7["7. resolve_runtime_ui_language"]
    s8["8. normalize_language"]
    s9["9. str(…).strip().lower"]
    s10["10. str(…).strip (backend/app/services/lang…vice.py:normalize_language)"]
    s11["11. str (backend/app/services/lang…vice.py:normalize_language)"]
    s12["12. RuntimeSettingsService.get_app_settings"]
    s1 -. "service.update_label(label_id, data)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(...))" .-> s3
    s1 -. "str (backend/app/routers/labels.py:update_label)(exc)" .-> s4
    s1 -. "HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))" .-> s5
    s1 -. "str (backend/app/routers/labels.py:update_label)(exc)" .-> s6
    s1 -->|"resolve_runtime_ui_language(service.db)"| s7
    s7 -->|"normalize_language(default)"| s8
    s8 -. "str(…).strip().lower(data not statically known)" .-> s9
    s8 -. "str(…).strip (backend/app/services/lang…vice.py:normalize_language)(data not statically known)" .-> s10
    s8 -. "str (backend/app/services/lang…vice.py:normalize_language)(...)" .-> s11
    s7 -->|"RuntimeSettingsService.get_app_settings(data not statically known)"| s12
    click s1 "../modules/labels.md"
    click s7 "../modules/language_service.md"
    click s8 "../modules/language_service.md"
    click s12 "../modules/system_settings_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `update_label` | `label_id: int`, `data: LabelUpdate`, `service: Annotated[LabelService, Depends(get_label_service)]` | `LabelConflictError`, `status`, `status`, `status` | - | `label` |
| `service.update_label` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str (backend/app/routers/labels.py:update_label)` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str (backend/app/routers/labels.py:update_label)` | - | - | - | - |
| `resolve_runtime_ui_language` | `db: Any`, `default: LanguageCode \| None` | - | - | `normalize_language(...)`, `normalize_language(...)`, `fallback` |
| `normalize_language` | `value: Any`, `default: LanguageCode` | - | - | `normalized`, `default` |
| `str(…).strip().lower` | - | - | - | - |
| `str(…).strip (backend/app/services/lang…vice.py:normalize_language)` | - | - | - | - |
| `str (backend/app/services/lang…vice.py:normalize_language)` | - | - | - | - |
| `RuntimeSettingsService.get_app_settings` | - | - | - | `SimpleNamespace(...)` |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| update_label | service.update_label | 116 | `service.update_label(label_id, data)` |
| update_label | HTTPException | 118 | `HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(...))` |
| update_label | str (backend/app/routers/labels.py:update_label) | 118 | `str(exc)` |
| update_label | HTTPException | 120 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))` |
| update_label | str (backend/app/routers/labels.py:update_label) | 120 | `str(exc)` |
| update_label | resolve_runtime_ui_language | 123 | `resolve_runtime_ui_language(service.db)` |
| resolve_runtime_ui_language | normalize_language | 406 | `normalize_language(default)` |
| normalize_language | str(…).strip().lower | 35 | `str(value or '').strip().lower(data not statically known)` |
| normalize_language | str(…).strip (backend/app/services/lang…vice.py:normalize_language) | 35 | `str(value or '').strip(data not statically known)` |
| normalize_language | str (backend/app/services/lang…vice.py:normalize_language) | 35 | `str(...)` |
| resolve_runtime_ui_language | RuntimeSettingsService.get_app_settings | 411 | `RuntimeSettingsService(db).get_app_settings(data not statically known)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `update_label` | `service.update_label` | 116 |
| external_call | `update_label` | `HTTPException` | 118 |
| external_call | `update_label` | `HTTPException` | 120 |
| unresolved_call | `normalize_language` | `str(value or '').strip().lower` | 35 |
| unresolved_call | `normalize_language` | `str(value or '').strip` | 35 |
| step_limit | `update_label` | `first 12 steps` | 0 |
| truncated_flow | `update_label` | `depth limit` | 0 |

## Behavior

This flow starts at `update_label` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

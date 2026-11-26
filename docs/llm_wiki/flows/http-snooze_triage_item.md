# snooze_triage_item

**Entry point:** `snooze_triage_item` (`http`)
**Source:** [routers_triage](../modules/routers_triage.md)
**Modules touched:** [config](../modules/config.md), [language_service](../modules/language_service.md), [routers_triage](../modules/routers_triage.md), [system_settings_service](../modules/system_settings_service.md), and 1 more

**Complete modules touched:**

- [config](../modules/config.md)
- [language_service](../modules/language_service.md)
- [routers_triage](../modules/routers_triage.md)
- [system_settings_service](../modules/system_settings_service.md)
- [url_policy](../modules/url_policy.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as snooze_triage_item
    participant p1 as _bad_request
    participant p2 as _not_found_detail
    participant p3 as resolve_runtime_ui_language
    participant p4 as backend_error_message
    participant p5 as RuntimeSettingsService.get_app_settings
    participant p6 as entity_not_found_message
    participant p7 as get_settings
    participant p8 as scoped_entity_not_found_message
    participant p9 as entity_deleted_message
    participant p10 as RuntimeSettingsService.resolve
    participant p11 as localized
    participant p12 as RuntimeSettingsService._definition
    participant p13 as RuntimeSettingsService._decrypt_secret
    participant p14 as RuntimeSettingsService._coerce
    participant p15 as normalize_language
    participant p16 as RuntimeSettingsService
    participant p17 as Settings
    participant p18 as RuntimeSettingsService._row
    participant p19 as RuntimeSettingsService._env_value
    participant p20 as RuntimeSettingsError
    participant p21 as RuntimeSettingsService._fernet
    participant p22 as RuntimeSettingsEncryptionError
    participant p23 as normalize_provider_api_url
    participant p24 as HTTPException (backend/app/routers/triage.py:snooze_triage_item)
    participant p25 as service.snooze
    participant p26 as isinstance (backend/app/routers/triage.py:_bad_request)
    participant p27 as HTTPException (backend/app/routers/triage.py:_bad_request)
    participant p28 as error.detail
    participant p29 as str (backend/app/routers/triage.py:_bad_request)
    p0->>p1: _bad_request
    p0->>p2: _not_found_detail
    p1->>p3: resolve_runtime_ui_language
    p1->>p4: backend_error_message
    p3->>p5: RuntimeSettingsService.get_app_settings
    p4->>p6: entity_not_found_message
    p3->>p7: get_settings
    p4->>p8: scoped_entity_not_found_message
    p4->>p9: entity_deleted_message
    p5->>p10: RuntimeSettingsService.resolve
    p6->>p11: localized
    p10->>p12: RuntimeSettingsService._definition
    p10->>p13: RuntimeSettingsService._decrypt_secret
    p10->>p14: RuntimeSettingsService._coerce
    p3->>p15: normalize_language
    p3->>p16: RuntimeSettingsService
    p7->>p17: Settings
    p10->>p18: RuntimeSettingsService._row
    p10->>p19: RuntimeSettingsService._env_value
    p12->>p20: RuntimeSettingsError
    p13->>p21: RuntimeSettingsService._fernet
    p13->>p22: RuntimeSettingsEncryptionError
    p14->>p23: normalize_provider_api_url
    p0-->>p24: HTTPException (backend/app/routers/triage.py:snooze_triage_item)(status_code=status.HTTP_404_NOT_FOUND, detail=...)
    p0-->>p25: service.snooze(triage_item_id, data)
    p1-->>p26: isinstance (backend/app/routers/triage.py:_bad_request)(error, SourceLinkRefused)
    p1-->>p27: HTTPException (backend/app/routers/triage.py:_bad_request)(status_code=status.HTTP_400_BAD_REQUEST, detail=error.detail(...))
    p1-->>p28: error.detail
    p1-->>p27: HTTPException (backend/app/routers/triage.py:_bad_request)(status_code=status.HTTP_400_BAD_REQUEST, detail=backend_error_message(...))
    p1-->>p29: str (backend/app/routers/triage.py:_bad_request)(error)
```

> Call sequence diagram shows 30 of 168 interactions; 138 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 5 of 49 (44 omitted); unresolved 2 of 71 (69 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/services/language_service.py:normalize_language` | 8 | - | unresolved | 2 |
| `backend/app/services/language_service.py:normalize_language` | 8 | - | external | 1 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._definition` | 14 | - | unresolved | 1 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._row` | 17 | - | unresolved | 3 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._row` | 17 | - | external | 1 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._decrypt_secret` | 22 | - | unresolved | 3 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._coerce` | 28 | - | external | 8 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._coerce` | 28 | [backend/app/services/system_settings_service.py](../modules/system_settings_service.md) | internal | 14 |
> Omission summary shows 8 of 27 groups; 19 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 49; effect analysis evaluated: 30, partial: 1, unavailable: 18. Counts include steps omitted from the displayed trace.

Collector observations for 31 source steps with known totals: observed: 162, emitted: 136, omitted: 26. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector omitted observations before flow assembly; displayed effects are partial.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `snooze_triage_item` | `available` | `evaluated` | `available` | `5` | `5` | `0` |
| `service.snooze` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `_bad_request` | `available` | `evaluated` | `available` | `7` | `7` | `0` |
| `isinstance (backend/app/routers/triage.py:_bad_request)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException (backend/app/routers/triage.py:_bad_request)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `error.detail` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `resolve_runtime_ui_language` | `available` | `evaluated` | `available` | `5` | `5` | `0` |
| `normalize_language` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `str(…).strip().lower` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str(…).strip (backend/app/services/lang…ice.py:normalize_language)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str (backend/app/services/lang…ice.py:normalize_language)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `RuntimeSettingsService.get_app_settings` | `available` | `evaluated` | `available` | `1` | `1` | `0` |

```mermaid
flowchart LR
    s1["1. snooze_triage_item"]
    s2["2. service.snooze"]
    s3["3. _bad_request"]
    s4["4. isinstance (backend/app/routers/triage.py:_bad_request)"]
    s5["5. HTTPException (backend/app/routers/triage.py:_bad_request)"]
    s6["6. error.detail"]
    s7["7. resolve_runtime_ui_language"]
    s8["8. normalize_language"]
    s9["9. str(…).strip().lower"]
    s10["10. str(…).strip (backend/app/services/lang…ice.py:normalize_language)"]
    s11["11. str (backend/app/services/lang…ice.py:normalize_language)"]
    s12["12. RuntimeSettingsService.get_app_settings"]
    s1 -. "service.snooze(triage_item_id, data)" .-> s2
    s1 -->|"_bad_request(service, e)"| s3
    s3 -. "isinstance (backend/app/routers/triage.py:_bad_request)(error, SourceLinkRefused)" .-> s4
    s3 -. "HTTPException (backend/app/routers/triage.py:_bad_request)(status_code=status.HTTP_400_BAD_REQUEST, detail=error.detail(...))" .-> s5
    s3 -. "error.detail(data not statically known)" .-> s6
    s3 -->|"resolve_runtime_ui_language(service.db)"| s7
    s7 -->|"normalize_language(default)"| s8
    s8 -. "str(…).strip().lower(data not statically known)" .-> s9
    s8 -. "str(…).strip (backend/app/services/lang…ice.py:normalize_language)(data not statically known)" .-> s10
    s8 -. "str (backend/app/services/lang…ice.py:normalize_language)(...)" .-> s11
    s7 -->|"RuntimeSettingsService.get_app_settings(data not statically known)"| s12
    click s1 "../modules/routers_triage.md"
    click s3 "../modules/routers_triage.md"
    click s7 "../modules/language_service.md"
    click s8 "../modules/language_service.md"
    click s12 "../modules/system_settings_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `snooze_triage_item` | `triage_item_id: int`, `data: TriageSnoozeRequest`, `service: Annotated[TriageService, Depends(get_triage_service)]` | `status` | - | `item` |
| `service.snooze` | - | - | - | - |
| `_bad_request` | `service`, `error: ValueError` | `SourceLinkRefused`, `status`, `status` | - | `HTTPException(...)`, `HTTPException(...)` |
| `isinstance (backend/app/routers/triage.py:_bad_request)` | - | - | - | - |
| `HTTPException (backend/app/routers/triage.py:_bad_request)` | - | - | - | - |
| `error.detail` | - | - | - | - |
| `resolve_runtime_ui_language` | `db: Any`, `default: LanguageCode \| None` | - | - | `normalize_language(...)`, `normalize_language(...)`, `fallback` |
| `normalize_language` | `value: Any`, `default: LanguageCode` | - | - | `normalized`, `default` |
| `str(…).strip().lower` | - | - | - | - |
| `str(…).strip (backend/app/services/lang…ice.py:normalize_language)` | - | - | - | - |
| `str (backend/app/services/lang…ice.py:normalize_language)` | - | - | - | - |
| `RuntimeSettingsService.get_app_settings` | - | - | - | `SimpleNamespace(...)` |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| snooze_triage_item | service.snooze | 318 | `service.snooze(triage_item_id, data)` |
| snooze_triage_item | _bad_request | 320 | `_bad_request(service, e)` |
| _bad_request | isinstance (backend/app/routers/triage.py:_bad_request) | 67 | `isinstance(error, SourceLinkRefused)` |
| _bad_request | HTTPException (backend/app/routers/triage.py:_bad_request) | 68 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error.detail(...))` |
| _bad_request | error.detail | 68 | `error.detail(data not statically known)` |
| _bad_request | resolve_runtime_ui_language | 69 | `resolve_runtime_ui_language(service.db)` |
| resolve_runtime_ui_language | normalize_language | 406 | `normalize_language(default)` |
| normalize_language | str(…).strip().lower | 35 | `str(value or '').strip().lower(data not statically known)` |
| normalize_language | str(…).strip (backend/app/services/lang…ice.py:normalize_language) | 35 | `str(value or '').strip(data not statically known)` |
| normalize_language | str (backend/app/services/lang…ice.py:normalize_language) | 35 | `str(...)` |
| resolve_runtime_ui_language | RuntimeSettingsService.get_app_settings | 411 | `RuntimeSettingsService(db).get_app_settings(data not statically known)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `snooze_triage_item` | `service.snooze` | 318 |
| external_call | `_bad_request` | `isinstance` | 67 |
| external_call | `_bad_request` | `HTTPException` | 68 |
| unresolved_call | `_bad_request` | `error.detail` | 68 |
| unresolved_call | `normalize_language` | `str(value or '').strip().lower` | 35 |
| unresolved_call | `normalize_language` | `str(value or '').strip` | 35 |
| step_limit | `snooze_triage_item` | `first 12 steps` | 0 |
| truncated_flow | `snooze_triage_item` | `depth limit` | 0 |

## Behavior

This flow starts at `snooze_triage_item` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

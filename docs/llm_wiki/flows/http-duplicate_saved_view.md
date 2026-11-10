# duplicate_saved_view

**Entry point:** `duplicate_saved_view` (`http`)
**Source:** [saved_views](../modules/saved_views.md)
**Modules touched:** [config](../modules/config.md), [language_service](../modules/language_service.md), [saved_views](../modules/saved_views.md), [system_settings_service](../modules/system_settings_service.md), and 1 more

**Complete modules touched:**

- [config](../modules/config.md)
- [language_service](../modules/language_service.md)
- [saved_views](../modules/saved_views.md)
- [system_settings_service](../modules/system_settings_service.md)
- [url_policy](../modules/url_policy.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as duplicate_saved_view
    participant p1 as raise_saved_view_http_error
    participant p2 as resolve_runtime_ui_language
    participant p3 as entity_not_found_message
    participant p4 as backend_error_message
    participant p5 as RuntimeSettingsService.get_app_settings
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
    participant p23 as HTTPException (backend/app/routers/saved…s.py:duplicate_saved_view)
    participant p24 as service.duplicate_for_session
    participant p25 as str (backend/app/routers/saved…ise_saved_view_http_error)
    participant p26 as isinstance (backend/app/routers/saved…ise_saved_view_http_error)
    participant p27 as HTTPException (backend/app/routers/saved…ise_saved_view_http_error)
    participant p28 as message.lower
    p0->>p1: raise_saved_view_http_error
    p0->>p2: resolve_runtime_ui_language
    p0->>p3: entity_not_found_message
    p1->>p4: backend_error_message
    p2->>p5: RuntimeSettingsService.get_app_settings
    p2->>p6: get_settings
    p4->>p7: scoped_entity_not_found_message
    p4->>p8: entity_deleted_message
    p5->>p9: RuntimeSettingsService.resolve
    p3->>p10: localized
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
    p0-->>p23: HTTPException (backend/app/routers/saved…s.py:duplicate_saved_view)(status_code=status.HTTP_404_NOT_FOUND, detail=entity_not_found_message(...))
    p0-->>p24: service.duplicate_for_session(view_id, data, current_session.id)
    p1-->>p25: str (backend/app/routers/saved…ise_saved_view_http_error)(exc)
    p1-->>p26: isinstance (backend/app/routers/saved…ise_saved_view_http_error)(exc, SavedViewPermissionError)
    p1-->>p27: HTTPException (backend/app/routers/saved…ise_saved_view_http_error)(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
    p1-->>p26: isinstance (backend/app/routers/saved…ise_saved_view_http_error)(exc, (...))
    p1-->>p27: HTTPException (backend/app/routers/saved…ise_saved_view_http_error)(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
    p4-->>p28: message.lower
```

> Call sequence diagram shows 30 of 167 interactions; 137 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 6 of 50 (44 omitted); unresolved 2 of 70 (68 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/routers/saved_views.py:raise_saved_view_http_error` | 3 | [backend/app/services/language_service.py](../modules/language_service.md) | internal | 1 |
| `backend/app/services/language_service.py:normalize_language` | 5 | - | unresolved | 2 |
| `backend/app/services/language_service.py:normalize_language` | 5 | - | external | 1 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._definition` | 11 | - | unresolved | 1 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._row` | 14 | - | unresolved | 3 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._row` | 14 | - | external | 1 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._decrypt_secret` | 19 | - | unresolved | 3 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._coerce` | 25 | - | external | 8 |
> Omission summary shows 8 of 27 groups; 19 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 48; effect analysis evaluated: 29, partial: 1, unavailable: 18. Counts include steps omitted from the displayed trace.

Collector observations for 30 source steps with known totals: observed: 160, emitted: 134, omitted: 26. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector omitted observations before flow assembly; displayed effects are partial.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `duplicate_saved_view` | `available` | `evaluated` | `available` | `6` | `6` | `0` |
| `service.duplicate_for_session` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `raise_saved_view_http_error` | `available` | `evaluated` | `available` | `7` | `7` | `0` |
| `resolve_runtime_ui_language` | `available` | `evaluated` | `available` | `5` | `5` | `0` |
| `normalize_language` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `str(…).strip().lower` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str(…).strip (backend/app/services/lang…ice.py:normalize_language)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str (backend/app/services/lang…ice.py:normalize_language)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `RuntimeSettingsService.get_app_settings` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `RuntimeSettingsService.resolve` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `RuntimeSettingsService._definition` | `available` | `evaluated` | `available` | `2` | `2` | `0` |
| `SETTING_DEFINITIONS.get` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. duplicate_saved_view"]
    s2["2. service.duplicate_for_session"]
    s3["3. raise_saved_view_http_error"]
    s4["4. resolve_runtime_ui_language"]
    s5["5. normalize_language"]
    s6["6. str(…).strip().lower"]
    s7["7. str(…).strip (backend/app/services/lang…ice.py:normalize_language)"]
    s8["8. str (backend/app/services/lang…ice.py:normalize_language)"]
    s9["9. RuntimeSettingsService.get_app_settings"]
    s10["10. RuntimeSettingsService.resolve"]
    s11["11. RuntimeSettingsService._definition"]
    s12["12. SETTING_DEFINITIONS.get"]
    s1 -. "service.duplicate_for_session(view_id, data, current_session.id)" .-> s2
    s1 -->|"raise_saved_view_http_error(service, exc)"| s3
    s3 -->|"resolve_runtime_ui_language(service.db)"| s4
    s4 -->|"normalize_language(default)"| s5
    s5 -. "str(…).strip().lower(data not statically known)" .-> s6
    s5 -. "str(…).strip (backend/app/services/lang…ice.py:normalize_language)(data not statically known)" .-> s7
    s5 -. "str (backend/app/services/lang…ice.py:normalize_language)(...)" .-> s8
    s4 -->|"RuntimeSettingsService.get_app_settings(data not statically known)"| s9
    s9 -->|"RuntimeSettingsService.resolve('app.ui_language')"| s10
    s10 -->|"RuntimeSettingsService._definition(key)"| s11
    s11 -. "SETTING_DEFINITIONS.get(key)" .-> s12
    click s1 "../modules/saved_views.md"
    click s3 "../modules/saved_views.md"
    click s4 "../modules/language_service.md"
    click s5 "../modules/language_service.md"
    click s9 "../modules/system_settings_service.md"
    click s10 "../modules/system_settings_service.md"
    click s11 "../modules/system_settings_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `duplicate_saved_view` | `view_id: int`, `data: SavedViewDuplicateRequest`, `service: Annotated[SavedViewService, Depends(get_saved_view_service)]`, `current_session: Annotated[UserSession, Depends(session_service.get_current_session)]` | `status` | - | `view` |
| `service.duplicate_for_session` | - | - | - | - |
| `raise_saved_view_http_error` | `service: SavedViewService`, `exc: Exception` | `SavedViewPermissionError`, `status`, `SavedViewValidationError`, `ValidationError`, `status` | - | - |
| `resolve_runtime_ui_language` | `db: Any`, `default: LanguageCode \| None` | - | - | `normalize_language(...)`, `normalize_language(...)`, `fallback` |
| `normalize_language` | `value: Any`, `default: LanguageCode` | - | - | `normalized`, `default` |
| `str(…).strip().lower` | - | - | - | - |
| `str(…).strip (backend/app/services/lang…ice.py:normalize_language)` | - | - | - | - |
| `str (backend/app/services/lang…ice.py:normalize_language)` | - | - | - | - |
| `RuntimeSettingsService.get_app_settings` | - | - | - | `SimpleNamespace(...)` |
| `RuntimeSettingsService.resolve` | `key: str` | - | - | `(...)`, `(...)`, `(...)` |
| `RuntimeSettingsService._definition` | `key: str` | - | - | `definition` |
| `SETTING_DEFINITIONS.get` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| duplicate_saved_view | service.duplicate_for_session | 171 | `service.duplicate_for_session(view_id, data, current_session.id)` |
| duplicate_saved_view | raise_saved_view_http_error | 173 | `raise_saved_view_http_error(service, exc)` |
| raise_saved_view_http_error | resolve_runtime_ui_language | 44 | `resolve_runtime_ui_language(service.db)` |
| resolve_runtime_ui_language | normalize_language | 406 | `normalize_language(default)` |
| normalize_language | str(…).strip().lower | 35 | `str(value or '').strip().lower(data not statically known)` |
| normalize_language | str(…).strip (backend/app/services/lang…ice.py:normalize_language) | 35 | `str(value or '').strip(data not statically known)` |
| normalize_language | str (backend/app/services/lang…ice.py:normalize_language) | 35 | `str(...)` |
| resolve_runtime_ui_language | RuntimeSettingsService.get_app_settings | 411 | `RuntimeSettingsService(db).get_app_settings(data not statically known)` |
| RuntimeSettingsService.get_app_settings | RuntimeSettingsService.resolve | 337 | `self.resolve('app.ui_language')` |
| RuntimeSettingsService.resolve | RuntimeSettingsService._definition | 284 | `self._definition(key)` |
| RuntimeSettingsService._definition | SETTING_DEFINITIONS.get | 154 | `SETTING_DEFINITIONS.get(key)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `duplicate_saved_view` | `service.duplicate_for_session` | 171 |
| unresolved_call | `normalize_language` | `str(value or '').strip().lower` | 35 |
| unresolved_call | `normalize_language` | `str(value or '').strip` | 35 |
| unresolved_call | `RuntimeSettingsService._definition` | `SETTING_DEFINITIONS.get` | 154 |
| step_limit | `duplicate_saved_view` | `first 12 steps` | 0 |
| truncated_flow | `duplicate_saved_view` | `depth limit` | 0 |

## Behavior

This flow starts at `duplicate_saved_view` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

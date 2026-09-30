# update_release

**Entry point:** `update_release` (`http`)
**Source:** [projects](../modules/projects.md)
**Modules touched:** [config](../modules/config.md), [language_service](../modules/language_service.md), [projects](../modules/projects.md), [system_settings_service](../modules/system_settings_service.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as update_release
    participant p1 as service.update
    participant p2 as HTTPException
    participant p3 as _localized_detail
    participant p4 as resolve_runtime_ui_language
    participant p5 as normalize_language
    participant p6 as str(…).strip().lower
    participant p7 as str(…).strip
    participant p8 as str (backend/app/services/lang…ice.py:normalize_language)
    participant p9 as RuntimeSettingsService(…).get_app_settings
    participant p10 as RuntimeSettingsService
    participant p11 as getattr
    participant p12 as logger.warning
    participant p13 as get_settings
    participant p14 as Settings
    participant p15 as backend_error_message
    participant p16 as message.lower
    participant p17 as re.fullmatch
    participant p18 as match.groups
    participant p19 as label.strip().lower().replace
    participant p20 as label.strip().lower
    participant p21 as label.strip
    participant p22 as entity_not_found_message
    participant p23 as _RESOURCE_LABELS.get (backend/app/services/lang…:entity_not_found_message)
    participant p24 as localized
    p0-->>p1: service.update
    p0-->>p2: HTTPException
    p0->>p3: _localized_detail
    p3->>p4: resolve_runtime_ui_language
    p4->>p5: normalize_language
    p5-->>p6: str(…).strip().lower
    p5-->>p7: str(…).strip
    p5-->>p8: str (backend/app/services/lang…ice.py:normalize_language)
    p4-->>p9: RuntimeSettingsService(…).get_app_settings
    p4->>p10: RuntimeSettingsService
    p4->>p5: normalize_language
    p4-->>p11: getattr
    p4-->>p12: logger.warning
    p4->>p5: normalize_language
    p4-->>p11: getattr
    p4->>p13: get_settings
    p13->>p14: Settings
    p4-->>p12: logger.warning
    p3->>p15: backend_error_message
    p15->>p5: normalize_language
    p15-->>p16: message.lower
    p15-->>p17: re.fullmatch
    p15-->>p18: match.groups
    p15-->>p19: label.strip().lower().replace
    p15-->>p20: label.strip().lower
    p15-->>p21: label.strip
    p15->>p22: entity_not_found_message
    p22-->>p23: _RESOURCE_LABELS.get (backend/app/services/lang…:entity_not_found_message)
    p22->>p24: localized
    p24->>p5: normalize_language
```

> Call sequence diagram shows 30 of 119 interactions; 89 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. update_release"]
    s2["2. service.update"]
    s3["3. HTTPException"]
    s4["4. _localized_detail"]
    s5["5. resolve_runtime_ui_language"]
    s6["6. normalize_language"]
    s7["7. str(…).strip().lower"]
    s8["8. str(…).strip"]
    s9["9. str (backend/app/services/lang…ice.py:normalize_language)"]
    s10["10. RuntimeSettingsService(…).get_app_settings"]
    s11["11. RuntimeSettingsService"]
    s12["12. normalize_language"]
    s1 -. "service.update(release_id, data)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=...)" .-> s3
    s1 -->|"_localized_detail(service, str(...))"| s4
    s4 -->|"resolve_runtime_ui_language(service.db)"| s5
    s5 -->|"normalize_language(default)"| s6
    s6 -. "str(…).strip().lower(data not statically known)" .-> s7
    s6 -. "str(…).strip(data not statically known)" .-> s8
    s6 -. "str (backend/app/services/lang…ice.py:normalize_language)(...)" .-> s9
    s5 -. "RuntimeSettingsService(…).get_app_settings(data not statically known)" .-> s10
    s5 -->|"RuntimeSettingsService(db)"| s11
    s5 -->|"normalize_language(getattr(...), default=fallback)"| s12
    b0["mutation service.update"]
    s1 -. "mutation service.update" .-> b0
    click s1 "../modules/projects.md"
    click s4 "../modules/projects.md"
    click s5 "../modules/language_service.md"
    click s6 "../modules/language_service.md"
    click s11 "../modules/system_settings_service.md"
    click s12 "../modules/language_service.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `update_release` | `release_id: int`, `data: ReleaseUpdateRequest`, `service: Annotated[ReleaseService, Depends(get_release_service)]` | `status`, `status` | - | `release` |
| `service.update` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `_localized_detail` | `service: Any`, `message: str` | - | - | `backend_error_message(...)` |
| `resolve_runtime_ui_language` | `db: Any`, `default: LanguageCode \| None` | - | - | `normalize_language(...)`, `normalize_language(...)`, `fallback` |
| `normalize_language` | `value: Any`, `default: LanguageCode` | - | - | `normalized`, `default` |
| `str(…).strip().lower` | - | - | - | - |
| `str(…).strip` | - | - | - | - |
| `str (backend/app/services/lang…ice.py:normalize_language)` | - | - | - | - |
| `RuntimeSettingsService(…).get_app_settings` | - | - | - | - |
| `RuntimeSettingsService` | - | - | - | - |
| `normalize_language` | `value: Any`, `default: LanguageCode` | - | - | `normalized`, `default` |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| update_release | service.update | 462 | `service.update(release_id, data)` |
| update_release | HTTPException | 464 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=...)` |
| update_release | _localized_detail | 466 | `_localized_detail(service, str(...))` |
| _localized_detail | resolve_runtime_ui_language | 66 | `resolve_runtime_ui_language(service.db)` |
| resolve_runtime_ui_language | normalize_language | 406 | `normalize_language(default)` |
| normalize_language | str(…).strip().lower | 35 | `str(value or '').strip().lower(data not statically known)` |
| normalize_language | str(…).strip | 35 | `str(value or '').strip(data not statically known)` |
| normalize_language | str (backend/app/services/lang…ice.py:normalize_language) | 35 | `str(...)` |
| resolve_runtime_ui_language | RuntimeSettingsService(…).get_app_settings | 411 | `RuntimeSettingsService(db).get_app_settings(data not statically known)` |
| resolve_runtime_ui_language | RuntimeSettingsService | 411 | `RuntimeSettingsService(db)` |
| resolve_runtime_ui_language | normalize_language | 412 | `normalize_language(getattr(...), default=fallback)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `service.update` | `update_release` | 462 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `update_release` | `HTTPException` | 464 |
| unresolved_call | `normalize_language` | `str(value or '').strip().lower` | 35 |
| unresolved_call | `normalize_language` | `str(value or '').strip` | 35 |
| unresolved_call | `resolve_runtime_ui_language` | `RuntimeSettingsService(db).get_app_settings` | 411 |
| step_limit | `update_release` | `first 12 steps` | 0 |

## Behavior

This flow starts at `update_release` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

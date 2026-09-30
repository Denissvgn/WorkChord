# duplicate_saved_view

**Entry point:** `duplicate_saved_view` (`http`)
**Source:** [saved_views](../modules/saved_views.md)
**Modules touched:** [config](../modules/config.md), [language_service](../modules/language_service.md), [saved_views](../modules/saved_views.md), [system_settings_service](../modules/system_settings_service.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as duplicate_saved_view
    participant p1 as service.duplicate_for_session
    participant p2 as raise_saved_view_http_error
    participant p3 as resolve_runtime_ui_language
    participant p4 as normalize_language
    participant p5 as str(…).strip().lower
    participant p6 as str(…).strip
    participant p7 as str (backend/app/services/lang…ice.py:normalize_language)
    participant p8 as RuntimeSettingsService(…).get_app_settings
    participant p9 as RuntimeSettingsService
    participant p10 as getattr
    participant p11 as logger.warning
    participant p12 as get_settings
    participant p13 as Settings
    participant p14 as backend_error_message
    participant p15 as message.lower
    participant p16 as re.fullmatch
    participant p17 as match.groups
    participant p18 as label.strip().lower().replace
    participant p19 as label.strip().lower
    participant p20 as label.strip
    participant p21 as entity_not_found_message
    participant p22 as _RESOURCE_LABELS.get (backend/app/services/lang…:entity_not_found_message)
    participant p23 as localized
    p0-->>p1: service.duplicate_for_session
    p0->>p2: raise_saved_view_http_error
    p2->>p3: resolve_runtime_ui_language
    p3->>p4: normalize_language
    p4-->>p5: str(…).strip().lower
    p4-->>p6: str(…).strip
    p4-->>p7: str (backend/app/services/lang…ice.py:normalize_language)
    p3-->>p8: RuntimeSettingsService(…).get_app_settings
    p3->>p9: RuntimeSettingsService
    p3->>p4: normalize_language
    p3-->>p10: getattr
    p3-->>p11: logger.warning
    p3->>p4: normalize_language
    p3-->>p10: getattr
    p3->>p12: get_settings
    p12->>p13: Settings
    p3-->>p11: logger.warning
    p2->>p14: backend_error_message
    p14->>p4: normalize_language
    p14-->>p15: message.lower
    p14-->>p16: re.fullmatch
    p14-->>p17: match.groups
    p14-->>p18: label.strip().lower().replace
    p14-->>p19: label.strip().lower
    p14-->>p20: label.strip
    p14->>p21: entity_not_found_message
    p21-->>p22: _RESOURCE_LABELS.get (backend/app/services/lang…:entity_not_found_message)
    p21->>p23: localized
    p23->>p4: normalize_language
    p14-->>p16: re.fullmatch
```

> Call sequence diagram shows 30 of 121 interactions; 91 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. duplicate_saved_view"]
    s2["2. service.duplicate_for_session"]
    s3["3. raise_saved_view_http_error"]
    s4["4. resolve_runtime_ui_language"]
    s5["5. normalize_language"]
    s6["6. str(…).strip().lower"]
    s7["7. str(…).strip"]
    s8["8. str (backend/app/services/lang…ice.py:normalize_language)"]
    s9["9. RuntimeSettingsService(…).get_app_settings"]
    s10["10. RuntimeSettingsService"]
    s11["11. normalize_language"]
    s12["12. getattr"]
    s1 -. "service.duplicate_for_session(view_id, data, current_session.id)" .-> s2
    s1 -->|"raise_saved_view_http_error(service, exc)"| s3
    s3 -->|"resolve_runtime_ui_language(service.db)"| s4
    s4 -->|"normalize_language(default)"| s5
    s5 -. "str(…).strip().lower(data not statically known)" .-> s6
    s5 -. "str(…).strip(data not statically known)" .-> s7
    s5 -. "str (backend/app/services/lang…ice.py:normalize_language)(...)" .-> s8
    s4 -. "RuntimeSettingsService(…).get_app_settings(data not statically known)" .-> s9
    s4 -->|"RuntimeSettingsService(db)"| s10
    s4 -->|"normalize_language(getattr(...), default=fallback)"| s11
    s4 -. "getattr(settings, 'app_ui_language', None)" .-> s12
    click s1 "../modules/saved_views.md"
    click s3 "../modules/saved_views.md"
    click s4 "../modules/language_service.md"
    click s5 "../modules/language_service.md"
    click s10 "../modules/system_settings_service.md"
    click s11 "../modules/language_service.md"
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
| `str(…).strip` | - | - | - | - |
| `str (backend/app/services/lang…ice.py:normalize_language)` | - | - | - | - |
| `RuntimeSettingsService(…).get_app_settings` | - | - | - | - |
| `RuntimeSettingsService` | - | - | - | - |
| `normalize_language` | `value: Any`, `default: LanguageCode` | - | - | `normalized`, `default` |
| `getattr` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| duplicate_saved_view | service.duplicate_for_session | 171 | `service.duplicate_for_session(view_id, data, current_session.id)` |
| duplicate_saved_view | raise_saved_view_http_error | 173 | `raise_saved_view_http_error(service, exc)` |
| raise_saved_view_http_error | resolve_runtime_ui_language | 44 | `resolve_runtime_ui_language(service.db)` |
| resolve_runtime_ui_language | normalize_language | 406 | `normalize_language(default)` |
| normalize_language | str(…).strip().lower | 35 | `str(value or '').strip().lower(data not statically known)` |
| normalize_language | str(…).strip | 35 | `str(value or '').strip(data not statically known)` |
| normalize_language | str (backend/app/services/lang…ice.py:normalize_language) | 35 | `str(...)` |
| resolve_runtime_ui_language | RuntimeSettingsService(…).get_app_settings | 411 | `RuntimeSettingsService(db).get_app_settings(data not statically known)` |
| resolve_runtime_ui_language | RuntimeSettingsService | 411 | `RuntimeSettingsService(db)` |
| resolve_runtime_ui_language | normalize_language | 412 | `normalize_language(getattr(...), default=fallback)` |
| resolve_runtime_ui_language | getattr | 412 | `getattr(settings, 'app_ui_language', None)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `duplicate_saved_view` | `service.duplicate_for_session` | 171 |
| unresolved_call | `normalize_language` | `str(value or '').strip().lower` | 35 |
| unresolved_call | `normalize_language` | `str(value or '').strip` | 35 |
| unresolved_call | `resolve_runtime_ui_language` | `RuntimeSettingsService(db).get_app_settings` | 411 |
| external_call | `resolve_runtime_ui_language` | `getattr` | 412 |
| step_limit | `duplicate_saved_view` | `first 12 steps` | 0 |

## Behavior

This flow starts at `duplicate_saved_view` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

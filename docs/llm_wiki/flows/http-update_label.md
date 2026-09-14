# update_label

**Entry point:** `update_label` (`http`)
**Source:** [labels](../modules/labels.md)
**Modules touched:** [config](../modules/config.md), [labels](../modules/labels.md), [language_service](../modules/language_service.md), [system_settings_service](../modules/system_settings_service.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as update_label
    participant p1 as service.update_label
    participant p2 as HTTPException
    participant p3 as str (backend/app/routers/labels.py:update_label)
    participant p4 as resolve_runtime_ui_language
    participant p5 as normalize_language
    participant p6 as str(…).strip().lower
    participant p7 as str(…).strip
    participant p8 as str (backend/app/services/lang…vice.py:normalize_language)
    participant p9 as RuntimeSettingsService(…).get_app_settings
    participant p10 as RuntimeSettingsService
    participant p11 as getattr
    participant p12 as logger.warning
    participant p13 as get_settings
    participant p14 as Settings
    participant p15 as entity_not_found_message
    participant p16 as _RESOURCE_LABELS.get
    participant p17 as localized
    p0-->>p1: service.update_label
    p0-->>p2: HTTPException
    p0-->>p3: str (backend/app/routers/labels.py:update_label)
    p0-->>p2: HTTPException
    p0-->>p3: str (backend/app/routers/labels.py:update_label)
    p0->>p4: resolve_runtime_ui_language
    p4->>p5: normalize_language
    p5-->>p6: str(…).strip().lower
    p5-->>p7: str(…).strip
    p5-->>p8: str (backend/app/services/lang…vice.py:normalize_language)
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
    p0-->>p2: HTTPException
    p0->>p15: entity_not_found_message
    p15-->>p16: _RESOURCE_LABELS.get
    p15->>p17: localized
    p17->>p5: normalize_language
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
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
    s10["10. str(…).strip"]
    s11["11. str (backend/app/services/lang…vice.py:normalize_language)"]
    s12["12. RuntimeSettingsService(…).get_app_settings"]
    s1 -. "service.update_label(label_id, data)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(...))" .-> s3
    s1 -. "str (backend/app/routers/labels.py:update_label)(exc)" .-> s4
    s1 -. "HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))" .-> s5
    s1 -. "str (backend/app/routers/labels.py:update_label)(exc)" .-> s6
    s1 -->|"resolve_runtime_ui_language(service.db)"| s7
    s7 -->|"normalize_language(default)"| s8
    s8 -. "str(…).strip().lower(data not statically known)" .-> s9
    s8 -. "str(…).strip(data not statically known)" .-> s10
    s8 -. "str (backend/app/services/lang…vice.py:normalize_language)(...)" .-> s11
    s7 -. "RuntimeSettingsService(…).get_app_settings(data not statically known)" .-> s12
    click s1 "../modules/labels.md"
    click s7 "../modules/language_service.md"
    click s8 "../modules/language_service.md"
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
| `str(…).strip` | - | - | - | - |
| `str (backend/app/services/lang…vice.py:normalize_language)` | - | - | - | - |
| `RuntimeSettingsService(…).get_app_settings` | - | - | - | - |

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
| normalize_language | str(…).strip | 35 | `str(value or '').strip(data not statically known)` |
| normalize_language | str (backend/app/services/lang…vice.py:normalize_language) | 35 | `str(...)` |
| resolve_runtime_ui_language | RuntimeSettingsService(…).get_app_settings | 411 | `RuntimeSettingsService(db).get_app_settings(data not statically known)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `update_label` | `service.update_label` | 116 |
| external_call | `update_label` | `HTTPException` | 118 |
| external_call | `update_label` | `HTTPException` | 120 |
| unresolved_call | `normalize_language` | `str(value or '').strip().lower` | 35 |
| unresolved_call | `normalize_language` | `str(value or '').strip` | 35 |
| unresolved_call | `resolve_runtime_ui_language` | `RuntimeSettingsService(db).get_app_settings` | 411 |
| step_limit | `update_label` | `first 12 steps` | 0 |

## Behavior

This flow starts at `update_label` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

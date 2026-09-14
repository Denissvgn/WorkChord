# get_triage_duplicate_suggestions

**Entry point:** `get_triage_duplicate_suggestions` (`http`)
**Source:** [routers_triage](../modules/routers_triage.md)
**Modules touched:** [config](../modules/config.md), [language_service](../modules/language_service.md), [routers_triage](../modules/routers_triage.md), [system_settings_service](../modules/system_settings_service.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as get_triage_duplicate_suggestions
    participant p1 as service.get_duplicate_suggestions
    participant p2 as HTTPException
    participant p3 as _not_found_detail
    participant p4 as resolve_runtime_ui_language
    participant p5 as normalize_language
    participant p6 as str(…).strip().lower
    participant p7 as str(…).strip
    participant p8 as str
    participant p9 as RuntimeSettingsService(…).get_app_settings
    participant p10 as RuntimeSettingsService
    participant p11 as getattr
    participant p12 as logger.warning
    participant p13 as get_settings
    participant p14 as Settings
    participant p15 as entity_not_found_message
    participant p16 as _RESOURCE_LABELS.get
    participant p17 as localized
    p0-->>p1: service.get_duplicate_suggestions
    p0-->>p2: HTTPException
    p0->>p3: _not_found_detail
    p3->>p4: resolve_runtime_ui_language
    p4->>p5: normalize_language
    p5-->>p6: str(…).strip().lower
    p5-->>p7: str(…).strip
    p5-->>p8: str
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
    p3->>p15: entity_not_found_message
    p15-->>p16: _RESOURCE_LABELS.get
    p15->>p17: localized
    p17->>p5: normalize_language
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. get_triage_duplicate_suggestions"]
    s2["2. service.get_duplicate_suggestions"]
    s3["3. HTTPException"]
    s4["4. _not_found_detail"]
    s5["5. resolve_runtime_ui_language"]
    s6["6. normalize_language"]
    s7["7. str(…).strip().lower"]
    s8["8. str(…).strip"]
    s9["9. str"]
    s10["10. RuntimeSettingsService(…).get_app_settings"]
    s11["11. RuntimeSettingsService"]
    s12["12. normalize_language"]
    s1 -. "service.get_duplicate_suggestions(triage_item_id, limit_per_type=limit_per_type, min_score=min_score)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s3
    s1 -->|"_not_found_detail(service, triage_item_id)"| s4
    s4 -->|"resolve_runtime_ui_language(service.db)"| s5
    s5 -->|"normalize_language(default)"| s6
    s6 -. "str(…).strip().lower(data not statically known)" .-> s7
    s6 -. "str(…).strip(data not statically known)" .-> s8
    s6 -. "str(...)" .-> s9
    s5 -. "RuntimeSettingsService(…).get_app_settings(data not statically known)" .-> s10
    s5 -->|"RuntimeSettingsService(db)"| s11
    s5 -->|"normalize_language(getattr(...), default=fallback)"| s12
    click s1 "../modules/routers_triage.md"
    click s4 "../modules/routers_triage.md"
    click s5 "../modules/language_service.md"
    click s6 "../modules/language_service.md"
    click s11 "../modules/system_settings_service.md"
    click s12 "../modules/language_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `get_triage_duplicate_suggestions` | `triage_item_id: int`, `service: Annotated[TriageService, Depends(get_triage_service)]`, `limit_per_type: int`, `min_score: float` | `status` | - | `suggestions` |
| `service.get_duplicate_suggestions` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `_not_found_detail` | `service`, `triage_item_id: int` | - | - | `entity_not_found_message(...)` |
| `resolve_runtime_ui_language` | `db: Any`, `default: LanguageCode \| None` | - | - | `normalize_language(...)`, `normalize_language(...)`, `fallback` |
| `normalize_language` | `value: Any`, `default: LanguageCode` | - | - | `normalized`, `default` |
| `str(…).strip().lower` | - | - | - | - |
| `str(…).strip` | - | - | - | - |
| `str` | - | - | - | - |
| `RuntimeSettingsService(…).get_app_settings` | - | - | - | - |
| `RuntimeSettingsService` | - | - | - | - |
| `normalize_language` | `value: Any`, `default: LanguageCode` | - | - | `normalized`, `default` |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| get_triage_duplicate_suggestions | service.get_duplicate_suggestions | 139 | `service.get_duplicate_suggestions(triage_item_id, limit_per_type=limit_per_type, min_score=min_score)` |
| get_triage_duplicate_suggestions | HTTPException | 145 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| get_triage_duplicate_suggestions | _not_found_detail | 147 | `_not_found_detail(service, triage_item_id)` |
| _not_found_detail | resolve_runtime_ui_language | 72 | `resolve_runtime_ui_language(service.db)` |
| resolve_runtime_ui_language | normalize_language | 406 | `normalize_language(default)` |
| normalize_language | str(…).strip().lower | 35 | `str(value or '').strip().lower(data not statically known)` |
| normalize_language | str(…).strip | 35 | `str(value or '').strip(data not statically known)` |
| normalize_language | str | 35 | `str(...)` |
| resolve_runtime_ui_language | RuntimeSettingsService(…).get_app_settings | 411 | `RuntimeSettingsService(db).get_app_settings(data not statically known)` |
| resolve_runtime_ui_language | RuntimeSettingsService | 411 | `RuntimeSettingsService(db)` |
| resolve_runtime_ui_language | normalize_language | 412 | `normalize_language(getattr(...), default=fallback)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `get_triage_duplicate_suggestions` | `service.get_duplicate_suggestions` | 139 |
| external_call | `get_triage_duplicate_suggestions` | `HTTPException` | 145 |
| unresolved_call | `normalize_language` | `str(value or '').strip().lower` | 35 |
| unresolved_call | `normalize_language` | `str(value or '').strip` | 35 |
| unresolved_call | `resolve_runtime_ui_language` | `RuntimeSettingsService(db).get_app_settings` | 411 |
| step_limit | `get_triage_duplicate_suggestions` | `first 12 steps` | 0 |

## Behavior

This flow starts at `get_triage_duplicate_suggestions` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

# create_project_milestone

**Entry point:** `create_project_milestone` (`http`)
**Source:** [projects](../modules/projects.md)
**Modules touched:** [config](../modules/config.md), [language_service](../modules/language_service.md), [projects](../modules/projects.md), [system_settings_service](../modules/system_settings_service.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as create_project_milestone
    participant p1 as service.create_milestone
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
    p0-->>p1: service.create_milestone
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
    s1["1. create_project_milestone"]
    s2["2. service.create_milestone"]
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
    s1 -. "service.create_milestone(project_id, data)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s3
    s1 -->|"_not_found_detail(service, 'project', project_id)"| s4
    s4 -->|"resolve_runtime_ui_language(service.db)"| s5
    s5 -->|"normalize_language(default)"| s6
    s6 -. "str(…).strip().lower(data not statically known)" .-> s7
    s6 -. "str(…).strip(data not statically known)" .-> s8
    s6 -. "str(...)" .-> s9
    s5 -. "RuntimeSettingsService(…).get_app_settings(data not statically known)" .-> s10
    s5 -->|"RuntimeSettingsService(db)"| s11
    s5 -->|"normalize_language(getattr(...), default=fallback)"| s12
    click s1 "../modules/projects.md"
    click s4 "../modules/projects.md"
    click s5 "../modules/language_service.md"
    click s6 "../modules/language_service.md"
    click s11 "../modules/system_settings_service.md"
    click s12 "../modules/language_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `create_project_milestone` | `project_id: int`, `data: ProjectMilestoneCreateRequest`, `service: Annotated[ProjectService, Depends(get_project_service)]` | `status` | - | `milestone` |
| `service.create_milestone` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `_not_found_detail` | `service: Any`, `entity: str`, `entity_id: int` | - | - | `entity_not_found_message(...)` |
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
| create_project_milestone | service.create_milestone | 336 | `service.create_milestone(project_id, data)` |
| create_project_milestone | HTTPException | 338 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| create_project_milestone | _not_found_detail | 340 | `_not_found_detail(service, 'project', project_id)` |
| _not_found_detail | resolve_runtime_ui_language | 73 | `resolve_runtime_ui_language(service.db)` |
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
| unresolved_call | `create_project_milestone` | `service.create_milestone` | 336 |
| external_call | `create_project_milestone` | `HTTPException` | 338 |
| unresolved_call | `normalize_language` | `str(value or '').strip().lower` | 35 |
| unresolved_call | `normalize_language` | `str(value or '').strip` | 35 |
| unresolved_call | `resolve_runtime_ui_language` | `RuntimeSettingsService(db).get_app_settings` | 411 |
| step_limit | `create_project_milestone` | `first 12 steps` | 0 |

## Behavior

This flow starts at `create_project_milestone` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

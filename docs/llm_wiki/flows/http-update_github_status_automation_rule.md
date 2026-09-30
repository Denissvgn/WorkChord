# update_github_status_automation_rule

**Entry point:** `update_github_status_automation_rule` (`http`)
**Source:** [routers_github](../modules/routers_github.md)
**Modules touched:** [config](../modules/config.md), [language_service](../modules/language_service.md), [routers_github](../modules/routers_github.md), [system_settings_service](../modules/system_settings_service.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as update_github_status_automation_rule
    participant p1 as GitHubStatusAutomationRuleUpdate.model_validate
    participant p2 as HTTPException
    participant p3 as str (backend/app/routers/githu…hub_status_automation_rule)
    participant p4 as service.update_rule
    participant p5 as resolve_runtime_ui_language
    participant p6 as normalize_language
    participant p7 as str(…).strip().lower
    participant p8 as str(…).strip
    participant p9 as str (backend/app/services/lang…vice.py:normalize_language)
    participant p10 as RuntimeSettingsService(…).get_app_settings
    participant p11 as RuntimeSettingsService
    participant p12 as getattr
    participant p13 as logger.warning
    participant p14 as get_settings
    participant p15 as Settings
    participant p16 as entity_not_found_message
    participant p17 as _RESOURCE_LABELS.get
    participant p18 as localized
    p0-->>p1: GitHubStatusAutomationRuleUpdate.model_validate
    p0-->>p2: HTTPException
    p0-->>p3: str (backend/app/routers/githu…hub_status_automation_rule)
    p0-->>p4: service.update_rule
    p0->>p5: resolve_runtime_ui_language
    p5->>p6: normalize_language
    p6-->>p7: str(…).strip().lower
    p6-->>p8: str(…).strip
    p6-->>p9: str (backend/app/services/lang…vice.py:normalize_language)
    p5-->>p10: RuntimeSettingsService(…).get_app_settings
    p5->>p11: RuntimeSettingsService
    p5->>p6: normalize_language
    p5-->>p12: getattr
    p5-->>p13: logger.warning
    p5->>p6: normalize_language
    p5-->>p12: getattr
    p5->>p14: get_settings
    p14->>p15: Settings
    p5-->>p13: logger.warning
    p0-->>p2: HTTPException
    p0->>p16: entity_not_found_message
    p16-->>p17: _RESOURCE_LABELS.get
    p16->>p18: localized
    p18->>p6: normalize_language
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. update_github_status_automation_rule"]
    s2["2. GitHubStatusAutomationRuleUpdate.model_validate"]
    s3["3. HTTPException"]
    s4["4. str (backend/app/routers/githu…hub_status_automation_rule)"]
    s5["5. service.update_rule"]
    s6["6. resolve_runtime_ui_language"]
    s7["7. normalize_language"]
    s8["8. str(…).strip().lower"]
    s9["9. str(…).strip"]
    s10["10. str (backend/app/services/lang…vice.py:normalize_language)"]
    s11["11. RuntimeSettingsService(…).get_app_settings"]
    s12["12. RuntimeSettingsService"]
    s1 -. "GitHubStatusAutomationRuleUpdate.model_validate(raw_data)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))" .-> s3
    s1 -. "str (backend/app/routers/githu…hub_status_automation_rule)(exc)" .-> s4
    s1 -. "service.update_rule(rule_id, data)" .-> s5
    s1 -->|"resolve_runtime_ui_language(service.db)"| s6
    s6 -->|"normalize_language(default)"| s7
    s7 -. "str(…).strip().lower(data not statically known)" .-> s8
    s7 -. "str(…).strip(data not statically known)" .-> s9
    s7 -. "str (backend/app/services/lang…vice.py:normalize_language)(...)" .-> s10
    s6 -. "RuntimeSettingsService(…).get_app_settings(data not statically known)" .-> s11
    s6 -->|"RuntimeSettingsService(db)"| s12
    click s1 "../modules/routers_github.md"
    click s6 "../modules/language_service.md"
    click s7 "../modules/language_service.md"
    click s12 "../modules/system_settings_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `update_github_status_automation_rule` | `rule_id: int`, `raw_data: Annotated[dict, Body(...)]`, `service: Annotated[GitHubStatusAutomationService, Depends(get_github_status_automation_service)]` | `ValidationError`, `status`, `status` | - | `rule` |
| `GitHubStatusAutomationRuleUpdate.model_validate` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str (backend/app/routers/githu…hub_status_automation_rule)` | - | - | - | - |
| `service.update_rule` | - | - | - | - |
| `resolve_runtime_ui_language` | `db: Any`, `default: LanguageCode \| None` | - | - | `normalize_language(...)`, `normalize_language(...)`, `fallback` |
| `normalize_language` | `value: Any`, `default: LanguageCode` | - | - | `normalized`, `default` |
| `str(…).strip().lower` | - | - | - | - |
| `str(…).strip` | - | - | - | - |
| `str (backend/app/services/lang…vice.py:normalize_language)` | - | - | - | - |
| `RuntimeSettingsService(…).get_app_settings` | - | - | - | - |
| `RuntimeSettingsService` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| update_github_status_automation_rule | GitHubStatusAutomationRuleUpdate.model_validate | 98 | `GitHubStatusAutomationRuleUpdate.model_validate(raw_data)` |
| update_github_status_automation_rule | HTTPException | 100 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))` |
| update_github_status_automation_rule | str (backend/app/routers/githu…hub_status_automation_rule) | 102 | `str(exc)` |
| update_github_status_automation_rule | service.update_rule | 105 | `service.update_rule(rule_id, data)` |
| update_github_status_automation_rule | resolve_runtime_ui_language | 107 | `resolve_runtime_ui_language(service.db)` |
| resolve_runtime_ui_language | normalize_language | 406 | `normalize_language(default)` |
| normalize_language | str(…).strip().lower | 35 | `str(value or '').strip().lower(data not statically known)` |
| normalize_language | str(…).strip | 35 | `str(value or '').strip(data not statically known)` |
| normalize_language | str (backend/app/services/lang…vice.py:normalize_language) | 35 | `str(...)` |
| resolve_runtime_ui_language | RuntimeSettingsService(…).get_app_settings | 411 | `RuntimeSettingsService(db).get_app_settings(data not statically known)` |
| resolve_runtime_ui_language | RuntimeSettingsService | 411 | `RuntimeSettingsService(db)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `update_github_status_automation_rule` | `GitHubStatusAutomationRuleUpdate.model_validate` | 98 |
| external_call | `update_github_status_automation_rule` | `HTTPException` | 100 |
| unresolved_call | `update_github_status_automation_rule` | `service.update_rule` | 105 |
| unresolved_call | `normalize_language` | `str(value or '').strip().lower` | 35 |
| unresolved_call | `normalize_language` | `str(value or '').strip` | 35 |
| unresolved_call | `resolve_runtime_ui_language` | `RuntimeSettingsService(db).get_app_settings` | 411 |
| step_limit | `update_github_status_automation_rule` | `first 12 steps` | 0 |

## Behavior

This flow starts at `update_github_status_automation_rule` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

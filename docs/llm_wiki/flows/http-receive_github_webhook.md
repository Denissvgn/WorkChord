# receive_github_webhook

**Entry point:** `receive_github_webhook` (`http`)
**Source:** [routers_github](../modules/routers_github.md)
**Modules touched:** [authority](../modules/authority.md), [config](../modules/config.md), [identity_service](../modules/identity_service.md), [language_service](../modules/language_service.md), and 2 more

**Complete modules touched:**

- [authority](../modules/authority.md)
- [config](../modules/config.md)
- [identity_service](../modules/identity_service.md)
- [language_service](../modules/language_service.md)
- [routers_github](../modules/routers_github.md)
- [system_settings_service](../modules/system_settings_service.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as receive_github_webhook
    participant p1 as resolve_runtime_ui_language
    participant p2 as normalize_language
    participant p3 as str(…).strip().lower
    participant p4 as str(…).strip
    participant p5 as str (backend/app/services/lang…ice.py:normalize_language)
    participant p6 as RuntimeSettingsService(…).get_app_settings
    participant p7 as RuntimeSettingsService
    participant p8 as getattr
    participant p9 as logger.warning
    participant p10 as get_settings
    participant p11 as Settings
    participant p12 as HTTPException
    participant p13 as backend_error_message
    participant p14 as message.lower
    participant p15 as re.fullmatch
    participant p16 as match.groups
    participant p17 as label.strip().lower().replace
    participant p18 as label.strip().lower
    participant p19 as label.strip
    participant p20 as entity_not_found_message
    participant p21 as _RESOURCE_LABELS.get (backend/app/services/lang…:entity_not_found_message)
    participant p22 as localized
    p0->>p1: resolve_runtime_ui_language
    p1->>p2: normalize_language
    p2-->>p3: str(…).strip().lower
    p2-->>p4: str(…).strip
    p2-->>p5: str (backend/app/services/lang…ice.py:normalize_language)
    p1-->>p6: RuntimeSettingsService(…).get_app_settings
    p1->>p7: RuntimeSettingsService
    p1->>p2: normalize_language
    p1-->>p8: getattr
    p1-->>p9: logger.warning
    p1->>p2: normalize_language
    p1-->>p8: getattr
    p1->>p10: get_settings
    p10->>p11: Settings
    p1-->>p9: logger.warning
    p0-->>p12: HTTPException
    p0->>p13: backend_error_message
    p13->>p2: normalize_language
    p13-->>p14: message.lower
    p13-->>p15: re.fullmatch
    p13-->>p16: match.groups
    p13-->>p17: label.strip().lower().replace
    p13-->>p18: label.strip().lower
    p13-->>p19: label.strip
    p13->>p20: entity_not_found_message
    p20-->>p21: _RESOURCE_LABELS.get (backend/app/services/lang…:entity_not_found_message)
    p20->>p22: localized
    p22->>p2: normalize_language
    p13-->>p15: re.fullmatch
    p13-->>p16: match.groups
```

> Call sequence diagram shows 30 of 138 interactions; 108 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. receive_github_webhook"]
    s2["2. resolve_runtime_ui_language"]
    s3["3. normalize_language"]
    s4["4. str(…).strip().lower"]
    s5["5. str(…).strip"]
    s6["6. str (backend/app/services/lang…ice.py:normalize_language)"]
    s7["7. RuntimeSettingsService(…).get_app_settings"]
    s8["8. RuntimeSettingsService"]
    s9["9. normalize_language"]
    s10["10. getattr"]
    s11["11. logger.warning"]
    s12["12. normalize_language"]
    s1 -->|"resolve_runtime_ui_language(service.db)"| s2
    s2 -->|"normalize_language(default)"| s3
    s3 -. "str(…).strip().lower(data not statically known)" .-> s4
    s3 -. "str(…).strip(data not statically known)" .-> s5
    s3 -. "str (backend/app/services/lang…ice.py:normalize_language)(...)" .-> s6
    s2 -. "RuntimeSettingsService(…).get_app_settings(data not statically known)" .-> s7
    s2 -->|"RuntimeSettingsService(db)"| s8
    s2 -->|"normalize_language(getattr(...), default=fallback)"| s9
    s2 -. "getattr(settings, 'app_ui_language', None)" .-> s10
    s2 -. "logger.warning('Unable to resolve DB-backed runtime UI language; using fallback', exc_info=True)" .-> s11
    s2 -->|"normalize_language(getattr(...), default=fallback)"| s12
    click s1 "../modules/routers_github.md"
    click s2 "../modules/language_service.md"
    click s3 "../modules/language_service.md"
    click s8 "../modules/system_settings_service.md"
    click s9 "../modules/language_service.md"
    click s12 "../modules/language_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `receive_github_webhook` | `request: Request`, `service: Annotated[GitHubWebhookService, Depends(get_github_webhook_service)]`, `github_event: Annotated[Optional[str], Header(alias='X-GitHub-Event')]`, `github_delivery: Annotated[Optional[str], Header(alias='X-GitHub-Delivery')]`, `github_signature: Annotated[Optional[str], Header(alias='X-Hub-Signature-256')]` | `status`, `GitHubWebhookConfigurationError`, `status`, `GitHubWebhookSignatureError`, `status`, `GitHubWebhookPayloadError`, `status` | - | `...` |
| `resolve_runtime_ui_language` | `db: Any`, `default: LanguageCode \| None` | - | - | `normalize_language(...)`, `normalize_language(...)`, `fallback` |
| `normalize_language` | `value: Any`, `default: LanguageCode` | - | - | `normalized`, `default` |
| `str(…).strip().lower` | - | - | - | - |
| `str(…).strip` | - | - | - | - |
| `str (backend/app/services/lang…ice.py:normalize_language)` | - | - | - | - |
| `RuntimeSettingsService(…).get_app_settings` | - | - | - | - |
| `RuntimeSettingsService` | - | - | - | - |
| `normalize_language` | `value: Any`, `default: LanguageCode` | - | - | `normalized`, `default` |
| `getattr` | - | - | - | - |
| `logger.warning` | - | - | - | - |
| `normalize_language` | `value: Any`, `default: LanguageCode` | - | - | `normalized`, `default` |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| receive_github_webhook | resolve_runtime_ui_language | 151 | `resolve_runtime_ui_language(service.db)` |
| resolve_runtime_ui_language | normalize_language | 406 | `normalize_language(default)` |
| normalize_language | str(…).strip().lower | 35 | `str(value or '').strip().lower(data not statically known)` |
| normalize_language | str(…).strip | 35 | `str(value or '').strip(data not statically known)` |
| normalize_language | str (backend/app/services/lang…ice.py:normalize_language) | 35 | `str(...)` |
| resolve_runtime_ui_language | RuntimeSettingsService(…).get_app_settings | 411 | `RuntimeSettingsService(db).get_app_settings(data not statically known)` |
| resolve_runtime_ui_language | RuntimeSettingsService | 411 | `RuntimeSettingsService(db)` |
| resolve_runtime_ui_language | normalize_language | 412 | `normalize_language(getattr(...), default=fallback)` |
| resolve_runtime_ui_language | getattr | 412 | `getattr(settings, 'app_ui_language', None)` |
| resolve_runtime_ui_language | logger.warning | 415 | `logger.warning('Unable to resolve DB-backed runtime UI language; using fallback', exc_info=True)` |
| resolve_runtime_ui_language | normalize_language | 422 | `normalize_language(getattr(...), default=fallback)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `normalize_language` | `str(value or '').strip().lower` | 35 |
| unresolved_call | `normalize_language` | `str(value or '').strip` | 35 |
| unresolved_call | `resolve_runtime_ui_language` | `RuntimeSettingsService(db).get_app_settings` | 411 |
| external_call | `resolve_runtime_ui_language` | `getattr` | 412 |
| unresolved_call | `resolve_runtime_ui_language` | `logger.warning` | 415 |
| step_limit | `receive_github_webhook` | `first 12 steps` | 0 |

## Behavior

This flow starts at `receive_github_webhook` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

# delete_github_status_automation_rule

**Entry point:** `delete_github_status_automation_rule` (`http`)
**Source:** [routers_github](../modules/routers_github.md)
**Modules touched:** [config](../modules/config.md), [language_service](../modules/language_service.md), [routers_github](../modules/routers_github.md), [schemas_common](../modules/schemas_common.md), and 2 more

**Complete modules touched:**

- [config](../modules/config.md)
- [language_service](../modules/language_service.md)
- [routers_github](../modules/routers_github.md)
- [schemas_common](../modules/schemas_common.md)
- [system_settings_service](../modules/system_settings_service.md)
- [url_policy](../modules/url_policy.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as delete_github_status_automation_rule
    participant p1 as resolve_runtime_ui_language
    participant p2 as entity_not_found_message
    participant p3 as entity_deleted_message
    participant p4 as MessageResponse
    participant p5 as RuntimeSettingsService.get_app_settings
    participant p6 as localized
    participant p7 as RuntimeSettingsService.resolve
    participant p8 as RuntimeSettingsService._definition
    participant p9 as RuntimeSettingsService._decrypt_secret
    participant p10 as RuntimeSettingsService._coerce
    participant p11 as RuntimeSettingsService._fernet
    participant p12 as normalize_provider_api_url
    participant p13 as normalize_language
    participant p14 as RuntimeSettingsService
    participant p15 as get_settings
    participant p16 as RuntimeSettingsService._row
    participant p17 as RuntimeSettingsService._env_value
    participant p18 as RuntimeSettingsError
    participant p19 as RuntimeSettingsEncryptionError
    participant p20 as normalize_external_http_url
    participant p21 as HTTPException
    participant p22 as service.delete_rule
    participant p23 as _RESOURCE_LABELS.get
    participant p24 as _DELETED_LABELS.get
    participant p25 as getattr (backend/app/services/lang…esolve_runtime_ui_language)
    participant p26 as logger.warning
    participant p27 as str(…).strip().lower
    participant p28 as str(…).strip (backend/app/services/lang…vice.py:normalize_language)
    p0->>p1: resolve_runtime_ui_language
    p0->>p2: entity_not_found_message
    p0->>p3: entity_deleted_message
    p0->>p4: MessageResponse
    p1->>p5: RuntimeSettingsService.get_app_settings
    p2->>p6: localized
    p5->>p7: RuntimeSettingsService.resolve
    p7->>p8: RuntimeSettingsService._definition
    p7->>p9: RuntimeSettingsService._decrypt_secret
    p7->>p10: RuntimeSettingsService._coerce
    p9->>p11: RuntimeSettingsService._fernet
    p10->>p12: normalize_provider_api_url
    p1->>p13: normalize_language
    p1->>p14: RuntimeSettingsService
    p1->>p15: get_settings
    p7->>p16: RuntimeSettingsService._row
    p7->>p17: RuntimeSettingsService._env_value
    p8->>p18: RuntimeSettingsError
    p9->>p19: RuntimeSettingsEncryptionError
    p12->>p20: normalize_external_http_url
    p0-->>p21: HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=entity_not_found_message(...))
    p0-->>p22: service.delete_rule(rule_id)
    p2-->>p23: _RESOURCE_LABELS.get(entity, (...))
    p3-->>p24: _DELETED_LABELS.get(entity, (...))
    p1-->>p25: getattr (backend/app/services/lang…esolve_runtime_ui_language)(settings, 'app_ui_language', None)
    p1-->>p26: logger.warning('Unable to resolve DB-backed runtime UI language using fallback', exc_info=True)
    p1-->>p25: getattr (backend/app/services/lang…esolve_runtime_ui_language)(get_settings(...), 'app_ui_language', None)
    p1-->>p26: logger.warning('Unable to resolve environment-backed UI language using fallback', exc_info=True)
    p13-->>p27: str(…).strip().lower
    p13-->>p28: str(…).strip (backend/app/services/lang…vice.py:normalize_language)
```

> Call sequence diagram shows 30 of 77 interactions; 47 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 3 of 17 (14 omitted); unresolved 7 of 15 (8 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/services/language_service.py:normalize_language` | 4 | - | external | 1 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._definition` | 10 | - | unresolved | 1 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._row` | 13 | - | unresolved | 3 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._row` | 13 | - | external | 1 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._decrypt_secret` | 18 | - | unresolved | 3 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._fernet` | 21 | - | external | 2 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._fernet` | 21 | [backend/app/services/system_settings_service.py](../modules/system_settings_service.md) | internal | 2 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._coerce` | 28 | - | external | 8 |
> Omission summary shows 8 of 20 groups; 12 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 46; effect analysis evaluated: 26, partial: 0, unavailable: 20. Counts include steps omitted from the displayed trace.

Collector observations for 26 source steps with known totals: observed: 100, emitted: 100, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `delete_github_status_automation_rule` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `service.delete_rule` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `resolve_runtime_ui_language` | `available` | `evaluated` | `available` | `5` | `5` | `0` |
| `normalize_language` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `str(…).strip().lower` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str(…).strip (backend/app/services/lang…vice.py:normalize_language)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str (backend/app/services/lang…vice.py:normalize_language)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `RuntimeSettingsService.get_app_settings` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `RuntimeSettingsService.resolve` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `RuntimeSettingsService._definition` | `available` | `evaluated` | `available` | `2` | `2` | `0` |
| `SETTING_DEFINITIONS.get` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `RuntimeSettingsError` | `unavailable` | `unavailable` | `unavailable` | — | — | — |

```mermaid
flowchart LR
    s1["1. delete_github_status_automation_rule"]
    s2["2. service.delete_rule"]
    s3["3. resolve_runtime_ui_language"]
    s4["4. normalize_language"]
    s5["5. str(…).strip().lower"]
    s6["6. str(…).strip (backend/app/services/lang…vice.py:normalize_language)"]
    s7["7. str (backend/app/services/lang…vice.py:normalize_language)"]
    s8["8. RuntimeSettingsService.get_app_settings"]
    s9["9. RuntimeSettingsService.resolve"]
    s10["10. RuntimeSettingsService._definition"]
    s11["11. SETTING_DEFINITIONS.get"]
    s12["12. RuntimeSettingsError"]
    s1 -. "service.delete_rule(rule_id)" .-> s2
    s1 -->|"resolve_runtime_ui_language(service.db)"| s3
    s3 -->|"normalize_language(default)"| s4
    s4 -. "str(…).strip().lower(data not statically known)" .-> s5
    s4 -. "str(…).strip (backend/app/services/lang…vice.py:normalize_language)(data not statically known)" .-> s6
    s4 -. "str (backend/app/services/lang…vice.py:normalize_language)(...)" .-> s7
    s3 -->|"RuntimeSettingsService.get_app_settings(data not statically known)"| s8
    s8 -->|"RuntimeSettingsService.resolve('app.ui_language')"| s9
    s9 -->|"RuntimeSettingsService._definition(key)"| s10
    s10 -. "SETTING_DEFINITIONS.get(key)" .-> s11
    s10 -->|"RuntimeSettingsError(...)"| s12
    click s1 "../modules/routers_github.md"
    click s3 "../modules/language_service.md"
    click s4 "../modules/language_service.md"
    click s8 "../modules/system_settings_service.md"
    click s9 "../modules/system_settings_service.md"
    click s10 "../modules/system_settings_service.md"
    click s12 "../modules/system_settings_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `delete_github_status_automation_rule` | `rule_id: int`, `service: Annotated[GitHubStatusAutomationService, Depends(get_github_status_automation_service)]` | `status` | - | `MessageResponse(...)` |
| `service.delete_rule` | - | - | - | - |
| `resolve_runtime_ui_language` | `db: Any`, `default: LanguageCode \| None` | - | - | `normalize_language(...)`, `normalize_language(...)`, `fallback` |
| `normalize_language` | `value: Any`, `default: LanguageCode` | - | - | `normalized`, `default` |
| `str(…).strip().lower` | - | - | - | - |
| `str(…).strip (backend/app/services/lang…vice.py:normalize_language)` | - | - | - | - |
| `str (backend/app/services/lang…vice.py:normalize_language)` | - | - | - | - |
| `RuntimeSettingsService.get_app_settings` | - | - | - | `SimpleNamespace(...)` |
| `RuntimeSettingsService.resolve` | `key: str` | - | - | `(...)`, `(...)`, `(...)` |
| `RuntimeSettingsService._definition` | `key: str` | - | - | `definition` |
| `SETTING_DEFINITIONS.get` | - | - | - | - |
| `RuntimeSettingsError` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| delete_github_status_automation_rule | service.delete_rule | 127 | `service.delete_rule(rule_id)` |
| delete_github_status_automation_rule | resolve_runtime_ui_language | 129 | `resolve_runtime_ui_language(service.db)` |
| resolve_runtime_ui_language | normalize_language | 406 | `normalize_language(default)` |
| normalize_language | str(…).strip().lower | 35 | `str(value or '').strip().lower(data not statically known)` |
| normalize_language | str(…).strip (backend/app/services/lang…vice.py:normalize_language) | 35 | `str(value or '').strip(data not statically known)` |
| normalize_language | str (backend/app/services/lang…vice.py:normalize_language) | 35 | `str(...)` |
| resolve_runtime_ui_language | RuntimeSettingsService.get_app_settings | 411 | `RuntimeSettingsService(db).get_app_settings(data not statically known)` |
| RuntimeSettingsService.get_app_settings | RuntimeSettingsService.resolve | 337 | `self.resolve('app.ui_language')` |
| RuntimeSettingsService.resolve | RuntimeSettingsService._definition | 284 | `self._definition(key)` |
| RuntimeSettingsService._definition | SETTING_DEFINITIONS.get | 154 | `SETTING_DEFINITIONS.get(key)` |
| RuntimeSettingsService._definition | RuntimeSettingsError | 156 | `RuntimeSettingsError(...)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `delete_github_status_automation_rule` | `service.delete_rule` | 127 |
| unresolved_call | `normalize_language` | `str(value or '').strip().lower` | 35 |
| unresolved_call | `normalize_language` | `str(value or '').strip` | 35 |
| unresolved_call | `RuntimeSettingsService._definition` | `SETTING_DEFINITIONS.get` | 154 |
| step_limit | `delete_github_status_automation_rule` | `first 12 steps` | 0 |
| truncated_flow | `delete_github_status_automation_rule` | `depth limit` | 0 |

## Behavior

This flow starts at `delete_github_status_automation_rule` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

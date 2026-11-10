# delete_project

**Entry point:** `delete_project` (`http`)
**Source:** [projects](../modules/projects.md)
**Modules touched:** [config](../modules/config.md), [language_service](../modules/language_service.md), [projects](../modules/projects.md), [schemas_common](../modules/schemas_common.md), and 2 more

**Complete modules touched:**

- [config](../modules/config.md)
- [language_service](../modules/language_service.md)
- [projects](../modules/projects.md)
- [schemas_common](../modules/schemas_common.md)
- [system_settings_service](../modules/system_settings_service.md)
- [url_policy](../modules/url_policy.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as delete_project
    participant p1 as _not_found_detail
    participant p2 as _localized_detail
    participant p3 as resolve_runtime_ui_language
    participant p4 as MessageResponse
    participant p5 as entity_deleted_message
    participant p6 as entity_not_found_message
    participant p7 as backend_error_message
    participant p8 as RuntimeSettingsService.get_app_settings
    participant p9 as localized
    participant p10 as get_settings
    participant p11 as scoped_entity_not_found_message
    participant p12 as RuntimeSettingsService.resolve
    participant p13 as RuntimeSettingsService._definition
    participant p14 as RuntimeSettingsService._decrypt_secret
    participant p15 as RuntimeSettingsService._coerce
    participant p16 as normalize_language
    participant p17 as RuntimeSettingsService
    participant p18 as Settings
    participant p19 as RuntimeSettingsService._row
    participant p20 as RuntimeSettingsService._env_value
    participant p21 as RuntimeSettingsError
    participant p22 as RuntimeSettingsService._fernet
    participant p23 as RuntimeSettingsEncryptionError
    participant p24 as normalize_provider_api_url
    participant p25 as HTTPException
    participant p26 as service.delete
    participant p27 as _RESOURCE_LABELS.get (backend/app/services/lang…:entity_not_found_message)
    participant p28 as message.lower
    participant p29 as re.fullmatch
    p0->>p1: _not_found_detail
    p0->>p2: _localized_detail
    p0->>p3: resolve_runtime_ui_language
    p0->>p4: MessageResponse
    p0->>p5: entity_deleted_message
    p1->>p6: entity_not_found_message
    p2->>p7: backend_error_message
    p3->>p8: RuntimeSettingsService.get_app_settings
    p6->>p9: localized
    p3->>p10: get_settings
    p7->>p11: scoped_entity_not_found_message
    p8->>p12: RuntimeSettingsService.resolve
    p12->>p13: RuntimeSettingsService._definition
    p12->>p14: RuntimeSettingsService._decrypt_secret
    p12->>p15: RuntimeSettingsService._coerce
    p3->>p16: normalize_language
    p3->>p17: RuntimeSettingsService
    p10->>p18: Settings
    p12->>p19: RuntimeSettingsService._row
    p12->>p20: RuntimeSettingsService._env_value
    p13->>p21: RuntimeSettingsError
    p14->>p22: RuntimeSettingsService._fernet
    p14->>p23: RuntimeSettingsEncryptionError
    p15->>p24: normalize_provider_api_url
    p0-->>p25: HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)
    p0-->>p26: service.delete(project_id, detach_tasks=detach_tasks)
    p0-->>p25: HTTPException(status_code=status.HTTP_409_CONFLICT, detail={...})
    p6-->>p27: _RESOURCE_LABELS.get (backend/app/services/lang…:entity_not_found_message)(entity, (...))
    p7-->>p28: message.lower
    p7-->>p29: re.fullmatch('(.+) with id ([^ ]+) not found', message)
```

> Call sequence diagram shows 30 of 167 interactions; 137 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 3 of 46 (43 omitted); unresolved 3 of 70 (67 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/routers/projects.py:_not_found_detail` | 4 | [backend/app/services/language_service.py](../modules/language_service.md) | internal | 1 |
| `backend/app/services/language_service.py:normalize_language` | 6 | - | unresolved | 2 |
| `backend/app/services/language_service.py:normalize_language` | 6 | - | external | 1 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._definition` | 12 | - | unresolved | 1 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._row` | 15 | - | unresolved | 3 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._row` | 15 | - | external | 1 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._decrypt_secret` | 20 | - | unresolved | 3 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._coerce` | 26 | - | external | 8 |
> Omission summary shows 8 of 27 groups; 19 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 52; effect analysis evaluated: 32, partial: 1, unavailable: 19. Counts include steps omitted from the displayed trace.

Collector observations for 33 source steps with known totals: observed: 169, emitted: 143, omitted: 26. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector omitted observations before flow assembly; displayed effects are partial.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `delete_project` | `available` | `evaluated` | `available` | `6` | `6` | `0` |
| `service.delete` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `_not_found_detail` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `resolve_runtime_ui_language` | `available` | `evaluated` | `available` | `5` | `5` | `0` |
| `normalize_language` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `str(…).strip().lower` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str(…).strip (backend/app/services/lang…ice.py:normalize_language)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str (backend/app/services/lang…ice.py:normalize_language)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `RuntimeSettingsService.get_app_settings` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `RuntimeSettingsService.resolve` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `RuntimeSettingsService._definition` | `available` | `evaluated` | `available` | `2` | `2` | `0` |

```mermaid
flowchart LR
    s1["1. delete_project"]
    s2["2. service.delete"]
    s3["3. HTTPException"]
    s4["4. _not_found_detail"]
    s5["5. resolve_runtime_ui_language"]
    s6["6. normalize_language"]
    s7["7. str(…).strip().lower"]
    s8["8. str(…).strip (backend/app/services/lang…ice.py:normalize_language)"]
    s9["9. str (backend/app/services/lang…ice.py:normalize_language)"]
    s10["10. RuntimeSettingsService.get_app_settings"]
    s11["11. RuntimeSettingsService.resolve"]
    s12["12. RuntimeSettingsService._definition"]
    s1 -. "service.delete(project_id, detach_tasks=detach_tasks)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s3
    s1 -->|"_not_found_detail(service, 'project', project_id)"| s4
    s4 -->|"resolve_runtime_ui_language(service.db)"| s5
    s5 -->|"normalize_language(default)"| s6
    s6 -. "str(…).strip().lower(data not statically known)" .-> s7
    s6 -. "str(…).strip (backend/app/services/lang…ice.py:normalize_language)(data not statically known)" .-> s8
    s6 -. "str (backend/app/services/lang…ice.py:normalize_language)(...)" .-> s9
    s5 -->|"RuntimeSettingsService.get_app_settings(data not statically known)"| s10
    s10 -->|"RuntimeSettingsService.resolve('app.ui_language')"| s11
    s11 -->|"RuntimeSettingsService._definition(key)"| s12
    click s1 "../modules/projects.md"
    click s4 "../modules/projects.md"
    click s5 "../modules/language_service.md"
    click s6 "../modules/language_service.md"
    click s10 "../modules/system_settings_service.md"
    click s11 "../modules/system_settings_service.md"
    click s12 "../modules/system_settings_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `delete_project` | `project_id: int`, `service: Annotated[ProjectService, Depends(get_project_service)]`, `detach_tasks: bool` | `status`, `status` | - | `MessageResponse(...)` |
| `service.delete` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `_not_found_detail` | `service: Any`, `entity: str`, `entity_id: int` | - | - | `entity_not_found_message(...)` |
| `resolve_runtime_ui_language` | `db: Any`, `default: LanguageCode \| None` | - | - | `normalize_language(...)`, `normalize_language(...)`, `fallback` |
| `normalize_language` | `value: Any`, `default: LanguageCode` | - | - | `normalized`, `default` |
| `str(…).strip().lower` | - | - | - | - |
| `str(…).strip (backend/app/services/lang…ice.py:normalize_language)` | - | - | - | - |
| `str (backend/app/services/lang…ice.py:normalize_language)` | - | - | - | - |
| `RuntimeSettingsService.get_app_settings` | - | - | - | `SimpleNamespace(...)` |
| `RuntimeSettingsService.resolve` | `key: str` | - | - | `(...)`, `(...)`, `(...)` |
| `RuntimeSettingsService._definition` | `key: str` | - | - | `definition` |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| delete_project | service.delete | 499 | `service.delete(project_id, detach_tasks=detach_tasks)` |
| delete_project | HTTPException | 501 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| delete_project | _not_found_detail | 503 | `_not_found_detail(service, 'project', project_id)` |
| _not_found_detail | resolve_runtime_ui_language | 73 | `resolve_runtime_ui_language(service.db)` |
| resolve_runtime_ui_language | normalize_language | 406 | `normalize_language(default)` |
| normalize_language | str(…).strip().lower | 35 | `str(value or '').strip().lower(data not statically known)` |
| normalize_language | str(…).strip (backend/app/services/lang…ice.py:normalize_language) | 35 | `str(value or '').strip(data not statically known)` |
| normalize_language | str (backend/app/services/lang…ice.py:normalize_language) | 35 | `str(...)` |
| resolve_runtime_ui_language | RuntimeSettingsService.get_app_settings | 411 | `RuntimeSettingsService(db).get_app_settings(data not statically known)` |
| RuntimeSettingsService.get_app_settings | RuntimeSettingsService.resolve | 337 | `self.resolve('app.ui_language')` |
| RuntimeSettingsService.resolve | RuntimeSettingsService._definition | 284 | `self._definition(key)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `delete_project` | `service.delete` | 499 |
| external_call | `delete_project` | `HTTPException` | 501 |
| unresolved_call | `normalize_language` | `str(value or '').strip().lower` | 35 |
| unresolved_call | `normalize_language` | `str(value or '').strip` | 35 |
| step_limit | `delete_project` | `first 12 steps` | 0 |
| truncated_flow | `delete_project` | `depth limit` | 0 |

## Behavior

This flow starts at `delete_project` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

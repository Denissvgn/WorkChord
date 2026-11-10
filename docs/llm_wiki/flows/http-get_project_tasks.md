# get_project_tasks

**Entry point:** `get_project_tasks` (`http`)
**Source:** [projects](../modules/projects.md)
**Modules touched:** [agent_readiness](../modules/agent_readiness.md), [commands](../modules/commands.md), [config](../modules/config.md), [external_link_service](../modules/external_link_service.md), and 10 more

**Complete modules touched:**

- [agent_readiness](../modules/agent_readiness.md)
- [commands](../modules/commands.md)
- [config](../modules/config.md)
- [external_link_service](../modules/external_link_service.md)
- [language_service](../modules/language_service.md)
- [projects](../modules/projects.md)
- [schemas_external_link](../modules/schemas_external_link.md)
- [schemas_task](../modules/schemas_task.md)
- [services_work_metrics](../modules/services_work_metrics.md)
- [system_settings_service](../modules/system_settings_service.md)
- [task_brief_service](../modules/task_brief_service.md)
- [task_service](../modules/task_service.md)
- [time](../modules/time.md)
- [url_policy](../modules/url_policy.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as get_project_tasks
    participant p1 as _not_found_detail
    participant p2 as TaskService.task_to_response
    participant p3 as TaskService
    participant p4 as resolve_runtime_ui_language
    participant p5 as entity_not_found_message
    participant p6 as task_signals
    participant p7 as evaluate_agent_readiness
    participant p8 as ExternalLinkService.task_links_to_response
    participant p9 as working_today
    participant p10 as ExternalLinkService.link_to_response
    participant p11 as RuntimeSettingsService.get_app_settings
    participant p12 as localized
    participant p13 as ExternalLinkService.legacy_task_link_response
    participant p14 as _add_criterion
    participant p15 as get_settings
    participant p16 as RuntimeSettingsService.resolve
    participant p17 as RuntimeSettingsService._definition
    participant p18 as RuntimeSettingsService._decrypt_secret
    participant p19 as RuntimeSettingsService._coerce
    participant p20 as current_command
    participant p21 as TaskAssignee
    participant p22 as TaskProject
    participant p23 as TaskMilestone
    participant p24 as TaskClaimedBy
    participant p25 as TaskResponse
    participant p26 as ExternalLinkService
    participant p27 as normalize_language
    participant p28 as utc_now
    participant p29 as HTTPException
    participant p30 as service.get_tasks
    p0->>p1: _not_found_detail
    p0->>p2: TaskService.task_to_response
    p0->>p3: TaskService
    p1->>p4: resolve_runtime_ui_language
    p1->>p5: entity_not_found_message
    p2->>p6: task_signals
    p2->>p7: evaluate_agent_readiness
    p2->>p8: ExternalLinkService.task_links_to_response
    p6->>p9: working_today
    p8->>p10: ExternalLinkService.link_to_response
    p4->>p11: RuntimeSettingsService.get_app_settings
    p5->>p12: localized
    p8->>p13: ExternalLinkService.legacy_task_link_response
    p7->>p14: _add_criterion
    p4->>p15: get_settings
    p11->>p16: RuntimeSettingsService.resolve
    p16->>p17: RuntimeSettingsService._definition
    p16->>p18: RuntimeSettingsService._decrypt_secret
    p16->>p19: RuntimeSettingsService._coerce
    p2->>p20: current_command
    p2->>p21: TaskAssignee
    p2->>p22: TaskProject
    p2->>p23: TaskMilestone
    p2->>p24: TaskClaimedBy
    p2->>p25: TaskResponse
    p2->>p26: ExternalLinkService
    p4->>p27: normalize_language
    p7->>p28: utc_now
    p0-->>p29: HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)
    p0-->>p30: service.get_tasks(project_id)
```

> Call sequence diagram shows 30 of 185 interactions; 155 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 1 of 52 (51 omitted); unresolved 1 of 55 (54 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/services/language_service.py:normalize_language` | 6 | - | unresolved | 2 |
| `backend/app/services/language_service.py:normalize_language` | 6 | - | external | 1 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._definition` | 12 | - | unresolved | 1 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._definition` | 12 | [backend/app/services/system_settings_service.py](../modules/system_settings_service.md) | internal | 1 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService.resolve` | 11 | [backend/app/services/system_settings_service.py](../modules/system_settings_service.md) | internal | 3 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._row` | 15 | - | unresolved | 3 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._row` | 15 | - | external | 1 |
| `backend/app/services/system_settings_service.py:RuntimeSettingsService._decrypt_secret` | 20 | - | unresolved | 3 |
> Omission summary shows 8 of 56 groups; 48 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 79; effect analysis evaluated: 49, partial: 0, unavailable: 30. Counts include steps omitted from the displayed trace.

Collector observations for 49 source steps with known totals: observed: 235, emitted: 235, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `get_project_tasks` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `service.get_tasks` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
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
    s1["1. get_project_tasks"]
    s2["2. service.get_tasks"]
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
    s1 -. "service.get_tasks(project_id)" .-> s2
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
| `get_project_tasks` | `project_id: int`, `service: Annotated[ProjectService, Depends(get_project_service)]` | `status` | - | `...` |
| `service.get_tasks` | - | - | - | - |
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
| get_project_tasks | service.get_tasks | 521 | `service.get_tasks(project_id)` |
| get_project_tasks | HTTPException | 523 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| get_project_tasks | _not_found_detail | 525 | `_not_found_detail(service, 'project', project_id)` |
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
| unresolved_call | `get_project_tasks` | `service.get_tasks` | 521 |
| external_call | `get_project_tasks` | `HTTPException` | 523 |
| unresolved_call | `normalize_language` | `str(value or '').strip().lower` | 35 |
| unresolved_call | `normalize_language` | `str(value or '').strip` | 35 |
| step_limit | `get_project_tasks` | `first 12 steps` | 0 |
| truncated_flow | `get_project_tasks` | `depth limit` | 0 |

## Behavior

This flow starts at `get_project_tasks` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

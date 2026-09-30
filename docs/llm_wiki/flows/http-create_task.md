# create_task

**Entry point:** `create_task` (`http`)
**Source:** [tasks](../modules/tasks.md)
**Modules touched:** [config](../modules/config.md), [iteration_service](../modules/iteration_service.md), [language_service](../modules/language_service.md), [system_settings_service](../modules/system_settings_service.md), and 1 more

**Complete modules touched:**

- [config](../modules/config.md)
- [iteration_service](../modules/iteration_service.md)
- [language_service](../modules/language_service.md)
- [system_settings_service](../modules/system_settings_service.md)
- [tasks](../modules/tasks.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as create_task
    participant p1 as IterationService
    participant p2 as iteration_service.get_by_id
    participant p3 as HTTPException
    participant p4 as service.create
    participant p5 as _localized_detail
    participant p6 as resolve_runtime_ui_language
    participant p7 as normalize_language
    participant p8 as str(…).strip().lower
    participant p9 as str(…).strip
    participant p10 as str (backend/app/services/lang…ice.py:normalize_language)
    participant p11 as RuntimeSettingsService(…).get_app_settings
    participant p12 as RuntimeSettingsService
    participant p13 as getattr
    participant p14 as logger.warning
    participant p15 as get_settings
    participant p16 as Settings
    participant p17 as backend_error_message
    participant p18 as message.lower
    participant p19 as re.fullmatch
    participant p20 as match.groups
    participant p21 as label.strip().lower().replace
    participant p22 as label.strip().lower
    participant p23 as label.strip
    participant p24 as entity_not_found_message
    p0->>p1: IterationService
    p0-->>p2: iteration_service.get_by_id
    p0-->>p3: HTTPException
    p0-->>p4: service.create
    p0-->>p3: HTTPException
    p0->>p5: _localized_detail
    p5->>p6: resolve_runtime_ui_language
    p6->>p7: normalize_language
    p7-->>p8: str(…).strip().lower
    p7-->>p9: str(…).strip
    p7-->>p10: str (backend/app/services/lang…ice.py:normalize_language)
    p6-->>p11: RuntimeSettingsService(…).get_app_settings
    p6->>p12: RuntimeSettingsService
    p6->>p7: normalize_language
    p6-->>p13: getattr
    p6-->>p14: logger.warning
    p6->>p7: normalize_language
    p6-->>p13: getattr
    p6->>p15: get_settings
    p15->>p16: Settings
    p6-->>p14: logger.warning
    p5->>p17: backend_error_message
    p17->>p7: normalize_language
    p17-->>p18: message.lower
    p17-->>p19: re.fullmatch
    p17-->>p20: match.groups
    p17-->>p21: label.strip().lower().replace
    p17-->>p22: label.strip().lower
    p17-->>p23: label.strip
    p17->>p24: entity_not_found_message
```

> Call sequence diagram shows 30 of 119 interactions; 89 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. create_task"]
    s2["2. IterationService"]
    s3["3. iteration_service.get_by_id"]
    s4["4. HTTPException"]
    s5["5. service.create"]
    s6["6. HTTPException"]
    s7["7. _localized_detail"]
    s8["8. resolve_runtime_ui_language"]
    s9["9. normalize_language"]
    s10["10. str(…).strip().lower"]
    s11["11. str(…).strip"]
    s12["12. str (backend/app/services/lang…ice.py:normalize_language)"]
    s1 -->|"IterationService(db)"| s2
    s1 -. "iteration_service.get_by_id(iteration_id)" .-> s3
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s4
    s1 -. "service.create(iteration_id, data)" .-> s5
    s1 -. "HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=...)" .-> s6
    s1 -->|"_localized_detail(db, str(...))"| s7
    s7 -->|"resolve_runtime_ui_language(db)"| s8
    s8 -->|"normalize_language(default)"| s9
    s9 -. "str(…).strip().lower(data not statically known)" .-> s10
    s9 -. "str(…).strip(data not statically known)" .-> s11
    s9 -. "str (backend/app/services/lang…ice.py:normalize_language)(...)" .-> s12
    click s1 "../modules/tasks.md"
    click s2 "../modules/iteration_service.md"
    click s7 "../modules/tasks.md"
    click s8 "../modules/language_service.md"
    click s9 "../modules/language_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `create_task` | `iteration_id: int`, `data: TaskCreate`, `service: Annotated[TaskService, Depends(get_task_service)]`, `db: Annotated[AsyncSession, Depends(get_db, scope='function')]` | `status`, `status` | - | `service.task_to_response(...)` |
| `IterationService` | - | - | - | - |
| `iteration_service.get_by_id` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `service.create` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `_localized_detail` | `db: AsyncSession`, `message: str` | - | - | `backend_error_message(...)` |
| `resolve_runtime_ui_language` | `db: Any`, `default: LanguageCode \| None` | - | - | `normalize_language(...)`, `normalize_language(...)`, `fallback` |
| `normalize_language` | `value: Any`, `default: LanguageCode` | - | - | `normalized`, `default` |
| `str(…).strip().lower` | - | - | - | - |
| `str(…).strip` | - | - | - | - |
| `str (backend/app/services/lang…ice.py:normalize_language)` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| create_task | IterationService | 145 | `IterationService(db)` |
| create_task | iteration_service.get_by_id | 146 | `iteration_service.get_by_id(iteration_id)` |
| create_task | HTTPException | 149 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| create_task | service.create | 155 | `service.create(iteration_id, data)` |
| create_task | HTTPException | 157 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=...)` |
| create_task | _localized_detail | 159 | `_localized_detail(db, str(...))` |
| _localized_detail | resolve_runtime_ui_language | 63 | `resolve_runtime_ui_language(db)` |
| resolve_runtime_ui_language | normalize_language | 406 | `normalize_language(default)` |
| normalize_language | str(…).strip().lower | 35 | `str(value or '').strip().lower(data not statically known)` |
| normalize_language | str(…).strip | 35 | `str(value or '').strip(data not statically known)` |
| normalize_language | str (backend/app/services/lang…ice.py:normalize_language) | 35 | `str(...)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `create_task` | `iteration_service.get_by_id` | 146 |
| external_call | `create_task` | `HTTPException` | 149 |
| unresolved_call | `create_task` | `service.create` | 155 |
| external_call | `create_task` | `HTTPException` | 157 |
| unresolved_call | `normalize_language` | `str(value or '').strip().lower` | 35 |
| unresolved_call | `normalize_language` | `str(value or '').strip` | 35 |
| step_limit | `create_task` | `first 12 steps` | 0 |

## Behavior

This flow starts at `create_task` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

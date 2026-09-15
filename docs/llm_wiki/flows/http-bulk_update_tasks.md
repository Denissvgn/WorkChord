# bulk_update_tasks

**Entry point:** `bulk_update_tasks` (`http`)
**Source:** [tasks](../modules/tasks.md)
**Modules touched:** [config](../modules/config.md), [iteration_service](../modules/iteration_service.md), [language_service](../modules/language_service.md), [schemas_task](../modules/schemas_task.md), and 2 more

**Complete modules touched:**

- [config](../modules/config.md)
- [iteration_service](../modules/iteration_service.md)
- [language_service](../modules/language_service.md)
- [schemas_task](../modules/schemas_task.md)
- [system_settings_service](../modules/system_settings_service.md)
- [tasks](../modules/tasks.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as bulk_update_tasks
    participant p1 as IterationService
    participant p2 as iteration_service.get_by_id
    participant p3 as HTTPException
    participant p4 as _not_found_detail
    participant p5 as resolve_runtime_ui_language
    participant p6 as normalize_language
    participant p7 as str(…).strip().lower
    participant p8 as str(…).strip
    participant p9 as str (backend/app/services/lang…ice.py:normalize_language)
    participant p10 as RuntimeSettingsService(…).get_app_settings
    participant p11 as RuntimeSettingsService
    participant p12 as getattr
    participant p13 as logger.warning
    participant p14 as get_settings
    participant p15 as Settings
    participant p16 as entity_not_found_message
    participant p17 as _RESOURCE_LABELS.get (backend/app/services/lang…:entity_not_found_message)
    participant p18 as localized
    participant p19 as service.bulk_update_tasks_from_text
    participant p20 as TasksImportResponse
    participant p21 as len
    participant p22 as service.task_to_response
    p0->>p1: IterationService
    p0-->>p2: iteration_service.get_by_id
    p0-->>p3: HTTPException
    p0->>p4: _not_found_detail
    p4->>p5: resolve_runtime_ui_language
    p5->>p6: normalize_language
    p6-->>p7: str(…).strip().lower
    p6-->>p8: str(…).strip
    p6-->>p9: str (backend/app/services/lang…ice.py:normalize_language)
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
    p4->>p16: entity_not_found_message
    p16-->>p17: _RESOURCE_LABELS.get (backend/app/services/lang…:entity_not_found_message)
    p16->>p18: localized
    p18->>p6: normalize_language
    p0-->>p19: service.bulk_update_tasks_from_text
    p0->>p20: TasksImportResponse
    p0-->>p21: len
    p0-->>p21: len
    p0-->>p21: len
    p0-->>p21: len
    p0-->>p22: service.task_to_response
```

> Call sequence diagram shows 30 of 128 interactions; 98 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. bulk_update_tasks"]
    s2["2. IterationService"]
    s3["3. iteration_service.get_by_id"]
    s4["4. HTTPException"]
    s5["5. _not_found_detail"]
    s6["6. resolve_runtime_ui_language"]
    s7["7. normalize_language"]
    s8["8. str(…).strip().lower"]
    s9["9. str(…).strip"]
    s10["10. str (backend/app/services/lang…ice.py:normalize_language)"]
    s11["11. RuntimeSettingsService(…).get_app_settings"]
    s12["12. RuntimeSettingsService"]
    s1 -->|"IterationService(db)"| s2
    s1 -. "iteration_service.get_by_id(iteration_id)" .-> s3
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s4
    s1 -->|"_not_found_detail(db, 'iteration', iteration_id)"| s5
    s5 -->|"resolve_runtime_ui_language(db)"| s6
    s6 -->|"normalize_language(default)"| s7
    s7 -. "str(…).strip().lower(data not statically known)" .-> s8
    s7 -. "str(…).strip(data not statically known)" .-> s9
    s7 -. "str (backend/app/services/lang…ice.py:normalize_language)(...)" .-> s10
    s6 -. "RuntimeSettingsService(…).get_app_settings(data not statically known)" .-> s11
    s6 -->|"RuntimeSettingsService(db)"| s12
    click s1 "../modules/tasks.md"
    click s2 "../modules/iteration_service.md"
    click s5 "../modules/tasks.md"
    click s6 "../modules/language_service.md"
    click s7 "../modules/language_service.md"
    click s12 "../modules/system_settings_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `bulk_update_tasks` | `iteration_id: int`, `data: TasksImportRequest`, `service: Annotated[TaskService, Depends(get_task_service)]`, `db: Annotated[AsyncSession, Depends(get_db, scope='function')]` | `status`, `status` | - | `TasksImportResponse(...)` |
| `IterationService` | - | - | - | - |
| `iteration_service.get_by_id` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `_not_found_detail` | `db: AsyncSession`, `entity: str`, `entity_id: int` | - | - | `entity_not_found_message(...)` |
| `resolve_runtime_ui_language` | `db: Any`, `default: LanguageCode \| None` | - | - | `normalize_language(...)`, `normalize_language(...)`, `fallback` |
| `normalize_language` | `value: Any`, `default: LanguageCode` | - | - | `normalized`, `default` |
| `str(…).strip().lower` | - | - | - | - |
| `str(…).strip` | - | - | - | - |
| `str (backend/app/services/lang…ice.py:normalize_language)` | - | - | - | - |
| `RuntimeSettingsService(…).get_app_settings` | - | - | - | - |
| `RuntimeSettingsService` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| bulk_update_tasks | IterationService | 838 | `IterationService(db)` |
| bulk_update_tasks | iteration_service.get_by_id | 839 | `iteration_service.get_by_id(iteration_id)` |
| bulk_update_tasks | HTTPException | 842 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| bulk_update_tasks | _not_found_detail | 844 | `_not_found_detail(db, 'iteration', iteration_id)` |
| _not_found_detail | resolve_runtime_ui_language | 66 | `resolve_runtime_ui_language(db)` |
| resolve_runtime_ui_language | normalize_language | 406 | `normalize_language(default)` |
| normalize_language | str(…).strip().lower | 35 | `str(value or '').strip().lower(data not statically known)` |
| normalize_language | str(…).strip | 35 | `str(value or '').strip(data not statically known)` |
| normalize_language | str (backend/app/services/lang…ice.py:normalize_language) | 35 | `str(...)` |
| resolve_runtime_ui_language | RuntimeSettingsService(…).get_app_settings | 411 | `RuntimeSettingsService(db).get_app_settings(data not statically known)` |
| resolve_runtime_ui_language | RuntimeSettingsService | 411 | `RuntimeSettingsService(db)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `bulk_update_tasks` | `iteration_service.get_by_id` | 839 |
| external_call | `bulk_update_tasks` | `HTTPException` | 842 |
| unresolved_call | `normalize_language` | `str(value or '').strip().lower` | 35 |
| unresolved_call | `normalize_language` | `str(value or '').strip` | 35 |
| unresolved_call | `resolve_runtime_ui_language` | `RuntimeSettingsService(db).get_app_settings` | 411 |
| step_limit | `bulk_update_tasks` | `first 12 steps` | 0 |

## Behavior

This flow starts at `bulk_update_tasks` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

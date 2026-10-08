# import_iteration

**Entry point:** `import_iteration` (`http`)
**Source:** [export](../modules/export.md)
**Modules touched:** [authority](../modules/authority.md), [commands](../modules/commands.md), [config](../modules/config.md), [delivery_dependency_service](../modules/delivery_dependency_service.md), and 13 more

**Complete modules touched:**

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [config](../modules/config.md)
- [delivery_dependency_service](../modules/delivery_dependency_service.md)
- [discussion_service](../modules/discussion_service.md)
- [export](../modules/export.md)
- [import_parser](../modules/import_parser.md)
- [iteration_service](../modules/iteration_service.md)
- [models_task](../modules/models_task.md)
- [mutation_versions](../modules/mutation_versions.md)
- [planning_input_context](../modules/planning_input_context.md)
- [schemas_common](../modules/schemas_common.md)
- [schemas_task](../modules/schemas_task.md)
- [schemas_team](../modules/schemas_team.md)
- [snapshot_service](../modules/snapshot_service.md)
- [task_service](../modules/task_service.md)
- [team_service](../modules/team_service.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as import_iteration
    participant p1 as _read_json_upload
    participant p2 as file.read
    participant p3 as len (backend/app/routers/export.py:_read_json_upload)
    participant p4 as HTTPException (backend/app/routers/export.py:_read_json_upload)
    participant p5 as json.loads
    participant p6 as content.decode
    participant p7 as str (backend/app/routers/export.py:_read_json_upload)
    participant p8 as isinstance (backend/app/routers/export.py:_read_json_upload)
    participant p9 as IterationService
    participant p10 as iteration_service.get_by_id
    participant p11 as HTTPException (backend/app/routers/export.py:import_iteration)
    participant p12 as _validate_import_data
    participant p13 as data.get (backend/app/routers/export.py:_validate_import_data)
    participant p14 as isinstance (backend/app/routers/export.py:_validate_import_data)
    participant p15 as HTTPException (backend/app/routers/export.py:_validate_import_data)
    participant p16 as _validate_import_task_tree
    participant p17 as stack.pop (backend/app/routers/expor…validate_import_task_tree)
    participant p18 as isinstance (backend/app/routers/expor…validate_import_task_tree)
    participant p19 as ValueError (backend/app/routers/expor…validate_import_task_tree)
    participant p20 as current.get
    participant p21 as stack.extend
    participant p22 as reversed (backend/app/routers/expor…validate_import_task_tree)
    participant p23 as len (backend/app/routers/export.py:_validate_import_data)
    p0->>p1: _read_json_upload
    p1-->>p2: file.read
    p1-->>p3: len (backend/app/routers/export.py:_read_json_upload)
    p1-->>p4: HTTPException (backend/app/routers/export.py:_read_json_upload)
    p1-->>p5: json.loads
    p1-->>p6: content.decode
    p1-->>p4: HTTPException (backend/app/routers/export.py:_read_json_upload)
    p1-->>p7: str (backend/app/routers/export.py:_read_json_upload)
    p1-->>p8: isinstance (backend/app/routers/export.py:_read_json_upload)
    p1-->>p4: HTTPException (backend/app/routers/export.py:_read_json_upload)
    p0->>p9: IterationService
    p0-->>p10: iteration_service.get_by_id
    p0-->>p11: HTTPException (backend/app/routers/export.py:import_iteration)
    p0->>p12: _validate_import_data
    p12-->>p13: data.get (backend/app/routers/export.py:_validate_import_data)
    p12-->>p14: isinstance (backend/app/routers/export.py:_validate_import_data)
    p12-->>p15: HTTPException (backend/app/routers/export.py:_validate_import_data)
    p12->>p16: _validate_import_task_tree
    p16-->>p17: stack.pop (backend/app/routers/expor…validate_import_task_tree)
    p16-->>p18: isinstance (backend/app/routers/expor…validate_import_task_tree)
    p16-->>p19: ValueError (backend/app/routers/expor…validate_import_task_tree)
    p16-->>p19: ValueError (backend/app/routers/expor…validate_import_task_tree)
    p16-->>p20: current.get
    p16-->>p18: isinstance (backend/app/routers/expor…validate_import_task_tree)
    p16-->>p19: ValueError (backend/app/routers/expor…validate_import_task_tree)
    p16-->>p21: stack.extend
    p16-->>p22: reversed (backend/app/routers/expor…validate_import_task_tree)
    p12-->>p13: data.get (backend/app/routers/export.py:_validate_import_data)
    p12-->>p14: isinstance (backend/app/routers/export.py:_validate_import_data)
    p12-->>p23: len (backend/app/routers/export.py:_validate_import_data)
```

> Call sequence diagram shows 30 of 397 interactions; 367 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. import_iteration"]
    s2["2. _read_json_upload"]
    s3["3. file.read"]
    s4["4. len (backend/app/routers/export.py:_read_json_upload)"]
    s5["5. HTTPException (backend/app/routers/export.py:_read_json_upload)"]
    s6["6. json.loads"]
    s7["7. content.decode"]
    s8["8. HTTPException (backend/app/routers/export.py:_read_json_upload)"]
    s9["9. str (backend/app/routers/export.py:_read_json_upload)"]
    s10["10. isinstance (backend/app/routers/export.py:_read_json_upload)"]
    s11["11. HTTPException (backend/app/routers/export.py:_read_json_upload)"]
    s12["12. IterationService"]
    s1 -->|"_read_json_upload(file)"| s2
    s2 -. "file.read(...)" .-> s3
    s2 -. "len (backend/app/routers/export.py:_read_json_upload)(content)" .-> s4
    s2 -. "HTTPException (backend/app/routers/export.py:_read_json_upload)(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail='Import file is too large')" .-> s5
    s2 -. "json.loads(content.decode(...))" .-> s6
    s2 -. "content.decode('utf-8')" .-> s7
    s2 -. "HTTPException (backend/app/routers/export.py:_read_json_upload)(status_code=status.HTTP_400_BAD_REQUEST, detail=...)" .-> s8
    s2 -. "str (backend/app/routers/export.py:_read_json_upload)(e)" .-> s9
    s2 -. "isinstance (backend/app/routers/export.py:_read_json_upload)(data, dict)" .-> s10
    s2 -. "HTTPException (backend/app/routers/export.py:_read_json_upload)(status_code=status.HTTP_400_BAD_REQUEST, detail='Import file must contain a JSON object')" .-> s11
    s1 -->|"IterationService(db)"| s12
    click s1 "../modules/export.md"
    click s2 "../modules/export.md"
    click s12 "../modules/iteration_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `import_iteration` | `iteration_id: int`, `file: Annotated[UploadFile, File(...)]`, `db: Annotated[AsyncSession, Depends(get_db, scope='function')]` | `status`, `status` | - | `...` |
| `_read_json_upload` | `file: UploadFile` | `MAX_JSON_IMPORT_BYTES`, `MAX_JSON_IMPORT_BYTES`, `status`, `json`, `status`, `status` | - | `data` |
| `file.read` | - | - | - | - |
| `len (backend/app/routers/export.py:_read_json_upload)` | - | - | - | - |
| `HTTPException (backend/app/routers/export.py:_read_json_upload)` | - | - | - | - |
| `json.loads` | - | - | - | - |
| `content.decode` | - | - | - | - |
| `HTTPException (backend/app/routers/export.py:_read_json_upload)` | - | - | - | - |
| `str (backend/app/routers/export.py:_read_json_upload)` | - | - | - | - |
| `isinstance (backend/app/routers/export.py:_read_json_upload)` | - | - | - | - |
| `HTTPException (backend/app/routers/export.py:_read_json_upload)` | - | - | - | - |
| `IterationService` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| import_iteration | _read_json_upload | 419 | `_read_json_upload(file)` |
| _read_json_upload | file.read | 38 | `file.read(...)` |
| _read_json_upload | len (backend/app/routers/export.py:_read_json_upload) | 39 | `len(content)` |
| _read_json_upload | HTTPException (backend/app/routers/export.py:_read_json_upload) | 40 | `HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail='Import file is too large')` |
| _read_json_upload | json.loads | 45 | `json.loads(content.decode(...))` |
| _read_json_upload | content.decode | 45 | `content.decode('utf-8')` |
| _read_json_upload | HTTPException (backend/app/routers/export.py:_read_json_upload) | 47 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=...)` |
| _read_json_upload | str (backend/app/routers/export.py:_read_json_upload) | 49 | `str(e)` |
| _read_json_upload | isinstance (backend/app/routers/export.py:_read_json_upload) | 51 | `isinstance(data, dict)` |
| _read_json_upload | HTTPException (backend/app/routers/export.py:_read_json_upload) | 52 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Import file must contain a JSON object')` |
| import_iteration | IterationService | 421 | `IterationService(db)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `_read_json_upload` | `file.read` | 38 |
| external_call | `_read_json_upload` | `HTTPException` | 40 |
| external_call | `_read_json_upload` | `json.loads` | 45 |
| unresolved_call | `_read_json_upload` | `content.decode` | 45 |
| external_call | `_read_json_upload` | `HTTPException` | 47 |
| external_call | `_read_json_upload` | `isinstance` | 51 |
| external_call | `_read_json_upload` | `HTTPException` | 52 |
| step_limit | `import_iteration` | `first 12 steps` | 0 |

## Behavior

This flow starts at `import_iteration` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

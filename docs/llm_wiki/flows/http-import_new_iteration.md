# import_new_iteration

**Entry point:** `import_new_iteration` (`http`)
**Source:** [export](../modules/export.md)
**Modules touched:** [agent_routing_policy](../modules/agent_routing_policy.md), [agent_routing_service](../modules/agent_routing_service.md), [agent_team_setup](../modules/agent_team_setup.md), and 32 more

**Complete modules touched:**

- [agent_routing_policy](../modules/agent_routing_policy.md)
- [agent_routing_service](../modules/agent_routing_service.md)
- [agent_team_setup](../modules/agent_team_setup.md)
- [agent_team_setup_service](../modules/agent_team_setup_service.md)
- [authority](../modules/authority.md)
- [calendar_rules](../modules/calendar_rules.md)
- [calendar_service](../modules/calendar_service.md)
- [commands](../modules/commands.md)
- [config](../modules/config.md)
- [delivery_dependency_service](../modules/delivery_dependency_service.md)
- [discussion_service](../modules/discussion_service.md)
- [execution_planning_window](../modules/execution_planning_window.md)
- [execution_reconciliation](../modules/execution_reconciliation.md)
- [export](../modules/export.md)
- [identity_service](../modules/identity_service.md)
- [import_parser](../modules/import_parser.md)
- [iteration_service](../modules/iteration_service.md)
- [models_agent](../modules/models_agent.md)
- [models_calendar](../modules/models_calendar.md)
- [models_outbound_webhook](../modules/models_outbound_webhook.md)
- [models_task](../modules/models_task.md)
- [mutation_versions](../modules/mutation_versions.md)
- [planning_input_context](../modules/planning_input_context.md)
- [review_provenance](../modules/review_provenance.md)
- [schemas_common](../modules/schemas_common.md)
- [schemas_iteration](../modules/schemas_iteration.md)
- [schemas_task](../modules/schemas_task.md)
- [schemas_team](../modules/schemas_team.md)
- [snapshot_service](../modules/snapshot_service.md)
- [sql_semantics](../modules/sql_semantics.md)
- [task_brief_service](../modules/task_brief_service.md)
- [task_service](../modules/task_service.md)
- [team_member](../modules/team_member.md)
- [team_service](../modules/team_service.md)
- [time](../modules/time.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as import_new_iteration
    participant p1 as _validate_import_data
    participant p2 as command_transaction
    participant p3 as planning_input_reservation
    participant p4 as _process_import
    participant p5 as _read_json_upload
    participant p6 as IterationCreate
    participant p7 as _optional_int
    participant p8 as IterationService
    participant p9 as lock_iterations
    participant p10 as affected_iteration_ids
    participant p11 as DeliveryDependencyService.reconcile
    participant p12 as DiscussionService.enqueue
    participant p13 as _import_task
    participant p14 as reserve_iteration_annuals
    participant p15 as task_context
    participant p16 as current_window
    participant p17 as make_window
    participant p18 as seal_authority
    participant p19 as TaskService.record_task_event
    participant p20 as assignment_context
    participant p21 as original_ownership
    participant p22 as _import_task_record
    participant p23 as authority_stamp
    participant p24 as AnnualCalendars.for_iteration
    participant p25 as require_operator
    participant p26 as IterationService.changed_calendar_selection
    participant p27 as require_project
    participant p28 as DeliveryDependencyService.validate_cycles
    participant p29 as HTTPException (backend/app/routers/export.py:import_new_iteration)
    participant p30 as iter_data.get
    p0->>p1: _validate_import_data
    p0->>p2: command_transaction
    p0->>p3: planning_input_reservation
    p0->>p4: _process_import
    p0->>p5: _read_json_upload
    p0->>p6: IterationCreate
    p0->>p7: _optional_int
    p0->>p8: IterationService
    p0->>p9: lock_iterations
    p3->>p10: affected_iteration_ids
    p2->>p11: DeliveryDependencyService.reconcile
    p2->>p12: DiscussionService.enqueue
    p4->>p13: _import_task
    p3->>p14: reserve_iteration_annuals
    p3->>p15: task_context
    p3->>p16: current_window
    p3->>p17: make_window
    p3->>p18: seal_authority
    p3->>p19: TaskService.record_task_event
    p17->>p20: assignment_context
    p18->>p21: original_ownership
    p13->>p22: _import_task_record
    p18->>p23: authority_stamp
    p14->>p24: AnnualCalendars.for_iteration
    p10->>p25: require_operator
    p14->>p26: IterationService.changed_calendar_selection
    p10->>p27: require_project
    p11->>p28: DeliveryDependencyService.validate_cycles
    p0-->>p29: HTTPException (backend/app/routers/export.py:import_new_iteration)(status_code=status.HTTP_400_BAD_REQUEST, detail='Missing iteration data in export file')
    p0-->>p30: iter_data.get('calendar_id')
```

> Call sequence diagram shows 30 of 934 interactions; 904 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 1 of 271 (270 omitted); unresolved 1 of 490 (489 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/routers/export.py:_read_json_upload` | 2 | - | unresolved | 2 |
| `backend/app/routers/export.py:_read_json_upload` | 2 | - | external | 7 |
| `backend/app/routers/export.py:_validate_import_data` | 12 | - | unresolved | 2 |
| `backend/app/routers/export.py:_validate_import_data` | 12 | - | external | 9 |
| `backend/app/routers/export.py:_validate_import_data` | 12 | [backend/app/routers/export.py](../modules/export.md) | internal | 1 |
| `backend/app/routers/export.py:_validate_import_task_tree` | 16 | - | unresolved | 3 |
| `backend/app/routers/export.py:_validate_import_task_tree` | 16 | - | external | 6 |
| `backend/app/commands.py:command_transaction` | 34 | [backend/app/commands.py](../modules/commands.md) | internal | 2 |
> Omission summary shows 8 of 194 groups; 186 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 174; effect analysis evaluated: 113, partial: 5, unavailable: 56. Counts include steps omitted from the displayed trace.

Collector observations for 118 source steps with known totals: observed: 568, emitted: 542, omitted: 26. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector omitted observations before flow assembly; displayed effects are partial.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `import_new_iteration` | `available` | `evaluated` | `available` | `7` | `7` | `0` |
| `_read_json_upload` | `available` | `evaluated` | `available` | `8` | `8` | `0` |
| `file.read` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `len (backend/app/routers/export.py:_read_json_upload)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException (backend/app/routers/export.py:_read_json_upload)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `json.loads (backend/app/routers/export.py:_read_json_upload)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `content.decode` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException (backend/app/routers/export.py:_read_json_upload)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str (backend/app/routers/export.py:_read_json_upload)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `isinstance (backend/app/routers/export.py:_read_json_upload)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException (backend/app/routers/export.py:_read_json_upload)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `_validate_import_data` | `available` | `evaluated` | `available` | `1` | `1` | `0` |

```mermaid
flowchart LR
    s1["1. import_new_iteration"]
    s2["2. _read_json_upload"]
    s3["3. file.read"]
    s4["4. len (backend/app/routers/export.py:_read_json_upload)"]
    s5["5. HTTPException (backend/app/routers/export.py:_read_json_upload)"]
    s6["6. json.loads (backend/app/routers/export.py:_read_json_upload)"]
    s7["7. content.decode"]
    s8["8. HTTPException (backend/app/routers/export.py:_read_json_upload)"]
    s9["9. str (backend/app/routers/export.py:_read_json_upload)"]
    s10["10. isinstance (backend/app/routers/export.py:_read_json_upload)"]
    s11["11. HTTPException (backend/app/routers/export.py:_read_json_upload)"]
    s12["12. _validate_import_data"]
    s1 -->|"_read_json_upload(file)"| s2
    s2 -. "file.read(...)" .-> s3
    s2 -. "len (backend/app/routers/export.py:_read_json_upload)(content)" .-> s4
    s2 -. "HTTPException (backend/app/routers/export.py:_read_json_upload)(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail='Import file is too large')" .-> s5
    s2 -. "json.loads (backend/app/routers/export.py:_read_json_upload)(content.decode(...))" .-> s6
    s2 -. "content.decode('utf-8')" .-> s7
    s2 -. "HTTPException (backend/app/routers/export.py:_read_json_upload)(status_code=status.HTTP_400_BAD_REQUEST, detail=...)" .-> s8
    s2 -. "str (backend/app/routers/export.py:_read_json_upload)(e)" .-> s9
    s2 -. "isinstance (backend/app/routers/export.py:_read_json_upload)(data, dict)" .-> s10
    s2 -. "HTTPException (backend/app/routers/export.py:_read_json_upload)(status_code=status.HTTP_400_BAD_REQUEST, detail='Import file must contain a JSON object')" .-> s11
    s1 -->|"_validate_import_data(data)"| s12
    b0["mutation owned_scope.add"]
    s1 -. "mutation owned_scope.add" .-> b0
    click s1 "../modules/export.md"
    click s2 "../modules/export.md"
    click s12 "../modules/export.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `import_new_iteration` | `file: Annotated[UploadFile, File(...)]`, `db: Annotated[AsyncSession, Depends(get_db, scope='function')]` | `status`, `status`, `status` | - | `...` |
| `_read_json_upload` | `file: UploadFile` | `MAX_JSON_IMPORT_BYTES`, `MAX_JSON_IMPORT_BYTES`, `status`, `json`, `status`, `status` | - | `data` |
| `file.read` | - | - | - | - |
| `len (backend/app/routers/export.py:_read_json_upload)` | - | - | - | - |
| `HTTPException (backend/app/routers/export.py:_read_json_upload)` | - | - | - | - |
| `json.loads (backend/app/routers/export.py:_read_json_upload)` | - | - | - | - |
| `content.decode` | - | - | - | - |
| `HTTPException (backend/app/routers/export.py:_read_json_upload)` | - | - | - | - |
| `str (backend/app/routers/export.py:_read_json_upload)` | - | - | - | - |
| `isinstance (backend/app/routers/export.py:_read_json_upload)` | - | - | - | - |
| `HTTPException (backend/app/routers/export.py:_read_json_upload)` | - | - | - | - |
| `_validate_import_data` | `data` | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| import_new_iteration | _read_json_upload | 276 | `_read_json_upload(file)` |
| _read_json_upload | file.read | 38 | `file.read(...)` |
| _read_json_upload | len (backend/app/routers/export.py:_read_json_upload) | 39 | `len(content)` |
| _read_json_upload | HTTPException (backend/app/routers/export.py:_read_json_upload) | 40 | `HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail='Import file is too large')` |
| _read_json_upload | json.loads (backend/app/routers/export.py:_read_json_upload) | 45 | `json.loads(content.decode(...))` |
| _read_json_upload | content.decode | 45 | `content.decode('utf-8')` |
| _read_json_upload | HTTPException (backend/app/routers/export.py:_read_json_upload) | 47 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=...)` |
| _read_json_upload | str (backend/app/routers/export.py:_read_json_upload) | 49 | `str(e)` |
| _read_json_upload | isinstance (backend/app/routers/export.py:_read_json_upload) | 51 | `isinstance(data, dict)` |
| _read_json_upload | HTTPException (backend/app/routers/export.py:_read_json_upload) | 52 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Import file must contain a JSON object')` |
| import_new_iteration | _validate_import_data | 278 | `_validate_import_data(data)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `owned_scope.add` | `import_new_iteration` | 314 |

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
| step_limit | `import_new_iteration` | `first 12 steps` | 0 |
| truncated_flow | `import_new_iteration` | `depth limit` | 0 |

## Behavior

This flow starts at `import_new_iteration` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

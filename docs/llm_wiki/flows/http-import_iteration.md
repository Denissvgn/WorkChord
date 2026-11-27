# import_iteration

**Entry point:** `import_iteration` (`http`)
**Source:** [export](../modules/export.md)
**Modules touched:** [allocation_removal](../modules/allocation_removal.md), [authority](../modules/authority.md), [calendar_rules](../modules/calendar_rules.md), [capacity_transfers](../modules/capacity_transfers.md), and 26 more

**Complete modules touched:**

- [allocation_removal](../modules/allocation_removal.md)
- [authority](../modules/authority.md)
- [calendar_rules](../modules/calendar_rules.md)
- [capacity_transfers](../modules/capacity_transfers.md)
- [commands](../modules/commands.md)
- [config](../modules/config.md)
- [delivery_dependency_service](../modules/delivery_dependency_service.md)
- [discussion_service](../modules/discussion_service.md)
- [execution_planning_window](../modules/execution_planning_window.md)
- [export](../modules/export.md)
- [import_parser](../modules/import_parser.md)
- [import_planning_service](../modules/import_planning_service.md)
- [import_review_service](../modules/import_review_service.md)
- [iteration_service](../modules/iteration_service.md)
- [models_agent](../modules/models_agent.md)
- [models_outbound_webhook](../modules/models_outbound_webhook.md)
- [models_task](../modules/models_task.md)
- [mutation_versions](../modules/mutation_versions.md)
- [planning_input_context](../modules/planning_input_context.md)
- [schemas_common](../modules/schemas_common.md)
- [schemas_iteration](../modules/schemas_iteration.md)
- [schemas_team](../modules/schemas_team.md)
- [snapshot_service](../modules/snapshot_service.md)
- [sql_semantics](../modules/sql_semantics.md)
- [task_brief_service](../modules/task_brief_service.md)
- [task_reactivation_service](../modules/task_reactivation_service.md)
- [task_service](../modules/task_service.md)
- [team_member](../modules/team_member.md)
- [team_service](../modules/team_service.md)
- [time](../modules/time.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as import_iteration
    participant p1 as _validate_import_data
    participant p2 as apply_reviewed_import
    participant p3 as _read_json_upload
    participant p4 as IterationService
    participant p5 as IterationService.get_by_id
    participant p6 as write_iteration_import
    participant p7 as import_scope_revisions
    participant p8 as target_sha256
    participant p9 as run_import_with_changes
    participant p10 as changes_sha256
    participant p11 as affected_iteration_ids
    participant p12 as _sha256
    participant p13 as write_new_iteration_import
    participant p14 as capture_import_state
    participant p15 as diff_import_state
    participant p16 as command_transaction
    participant p17 as planning_input_reservation
    participant p18 as get_settings
    participant p19 as require_operator
    participant p20 as require_project
    participant p21 as _process_import
    participant p22 as prospective_member_profiles
    participant p23 as _sort_key
    participant p24 as inspect_allocation_history
    participant p25 as lock_planning
    participant p26 as transfer_iteration_ids
    participant p27 as process_reactivation_checks
    participant p28 as DeliveryDependencyService.reconcile
    participant p29 as HTTPException (backend/app/routers/export.py:import_iteration)
    participant p30 as file.read
    p0->>p1: _validate_import_data
    p0->>p2: apply_reviewed_import
    p0->>p3: _read_json_upload
    p0->>p4: IterationService
    p0->>p5: IterationService.get_by_id
    p0->>p6: write_iteration_import
    p2->>p7: import_scope_revisions
    p2->>p8: target_sha256
    p2->>p9: run_import_with_changes
    p2->>p10: changes_sha256
    p7->>p11: affected_iteration_ids
    p8->>p12: _sha256
    p9->>p13: write_new_iteration_import
    p9->>p14: capture_import_state
    p9->>p15: diff_import_state
    p13->>p16: command_transaction
    p13->>p17: planning_input_reservation
    p11->>p18: get_settings
    p11->>p19: require_operator
    p11->>p20: require_project
    p13->>p21: _process_import
    p11->>p22: prospective_member_profiles
    p15->>p23: _sort_key
    p17->>p24: inspect_allocation_history
    p17->>p25: lock_planning
    p17->>p26: transfer_iteration_ids
    p16->>p27: process_reactivation_checks
    p16->>p28: DeliveryDependencyService.reconcile
    p0-->>p29: HTTPException (backend/app/routers/export.py:import_iteration)(status_code=status.HTTP_404_NOT_FOUND, detail=...)
    p3-->>p30: file.read(...)
```

> Call sequence diagram shows 30 of 805 interactions; 775 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 1 of 244 (243 omitted); unresolved 1 of 374 (373 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/routers/export.py:_read_json_upload` | 2 | - | external | 7 |
| `backend/app/routers/export.py:_read_json_upload` | 2 | - | unresolved | 1 |
| `backend/app/services/iteration_service.py:IterationService.get_by_id` | 13 | - | unresolved | 4 |
| `backend/app/services/iteration_service.py:IterationService.get_by_id` | 13 | - | external | 3 |
| `backend/app/routers/export.py:_validate_import_data` | 22 | - | unresolved | 2 |
| `backend/app/routers/export.py:_validate_import_data` | 22 | - | external | 9 |
| `backend/app/routers/export.py:_validate_import_data` | 22 | [backend/app/routers/export.py](../modules/export.md) | internal | 1 |
| `backend/app/routers/export.py:_validate_import_task_tree` | 26 | - | unresolved | 3 |
> Omission summary shows 8 of 174 groups; 166 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 188; effect analysis evaluated: 120, partial: 8, unavailable: 60. Counts include steps omitted from the displayed trace.

Collector observations for 128 source steps with known totals: observed: 687, emitted: 655, omitted: 32. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector omitted observations before flow assembly; displayed effects are partial.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `import_iteration` | `available` | `evaluated` | `available` | `7` | `7` | `0` |
| `_read_json_upload` | `available` | `evaluated` | `available` | `8` | `8` | `0` |
| `file.read` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `len (backend/app/routers/export.py:_read_json_upload)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException (backend/app/routers/export.py:_read_json_upload)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `json.loads` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `content.decode` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException (backend/app/routers/export.py:_read_json_upload)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str (backend/app/routers/export.py:_read_json_upload)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `isinstance (backend/app/routers/export.py:_read_json_upload)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException (backend/app/routers/export.py:_read_json_upload)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `IterationService` | `unavailable` | `unavailable` | `unavailable` | — | — | — |

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
| `import_iteration` | `iteration_id: int`, `file: Annotated[UploadFile, File(...)]`, `db: Annotated[AsyncSession, Depends(get_db, scope='function')]`, `review_digest: Annotated[str \| None, Form()]` | `status` | - | `...`, `...` |
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
| import_iteration | _read_json_upload | 441 | `_read_json_upload(file)` |
| _read_json_upload | file.read | 38 | `file.read(...)` |
| _read_json_upload | len (backend/app/routers/export.py:_read_json_upload) | 39 | `len(content)` |
| _read_json_upload | HTTPException (backend/app/routers/export.py:_read_json_upload) | 40 | `HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail='Import file is too large')` |
| _read_json_upload | json.loads | 45 | `json.loads(content.decode(...))` |
| _read_json_upload | content.decode | 45 | `content.decode('utf-8')` |
| _read_json_upload | HTTPException (backend/app/routers/export.py:_read_json_upload) | 47 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=...)` |
| _read_json_upload | str (backend/app/routers/export.py:_read_json_upload) | 49 | `str(e)` |
| _read_json_upload | isinstance (backend/app/routers/export.py:_read_json_upload) | 51 | `isinstance(data, dict)` |
| _read_json_upload | HTTPException (backend/app/routers/export.py:_read_json_upload) | 52 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Import file must contain a JSON object')` |
| import_iteration | IterationService | 443 | `IterationService(db)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

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
| truncated_flow | `import_iteration` | `depth limit` | 0 |

## Behavior

This flow starts at `import_iteration` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

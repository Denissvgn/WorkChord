# human_my_work

**Entry point:** `human_my_work` (`http`)
**Source:** [routers_task_domain](../modules/routers_task_domain.md)
**Modules touched:** [agent_routing_policy](../modules/agent_routing_policy.md), [agent_routing_rollout](../modules/agent_routing_rollout.md), [agent_service](../modules/agent_service.md), and 30 more

**Complete modules touched:**

- [agent_routing_policy](../modules/agent_routing_policy.md)
- [agent_routing_rollout](../modules/agent_routing_rollout.md)
- [agent_service](../modules/agent_service.md)
- [agent_team_setup_service](../modules/agent_team_setup_service.md)
- [agent_work_service](../modules/agent_work_service.md)
- [authority](../modules/authority.md)
- [autonomy_canonical](../modules/autonomy_canonical.md)
- [commands](../modules/commands.md)
- [config](../modules/config.md)
- [delivery_dependency_service](../modules/delivery_dependency_service.md)
- [execution_planning_window](../modules/execution_planning_window.md)
- [github_links](../modules/github_links.md)
- [github_reconciliation_service](../modules/github_reconciliation_service.md)
- [identity_service](../modules/identity_service.md)
- [manual_provenance_service](../modules/manual_provenance_service.md)
- [planning_window_reconciliation](../modules/planning_window_reconciliation.md)
- [refusal_next_steps](../modules/refusal_next_steps.md)
- [retained_planning_output](../modules/retained_planning_output.md)
- [review_provenance](../modules/review_provenance.md)
- [routers_task_domain](../modules/routers_task_domain.md)
- [schemas_task_domain](../modules/schemas_task_domain.md)
- [services_work_metrics](../modules/services_work_metrics.md)
- [sql_semantics](../modules/sql_semantics.md)
- [task_brief_service](../modules/task_brief_service.md)
- [task_detail](../modules/task_detail.md)
- [task_detail_service](../modules/task_detail_service.md)
- [task_display_state](../modules/task_display_state.md)
- [task_domain_service](../modules/task_domain_service.md)
- [task_postponement_service](../modules/task_postponement_service.md)
- [task_replacement_service](../modules/task_replacement_service.md)
- [task_service](../modules/task_service.md)
- [time](../modules/time.md)
- [url_policy](../modules/url_policy.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as human_my_work
    participant p1 as TaskDetailService.my_work
    participant p2 as TaskDetailService
    participant p3 as local_work_profile
    participant p4 as TaskDetailService.references
    participant p5 as require_project
    participant p6 as TaskDetailService.page
    participant p7 as TaskDetailService._policy_flags
    participant p8 as TaskDomainService.allowed_actions
    participant p9 as TaskDomainService._policy_task
    participant p10 as get_settings
    participant p11 as displayed_state_expression
    participant p12 as DeliveryDependencyService.ready
    participant p13 as action_projection
    participant p14 as replaced_by
    participant p15 as replacing
    participant p16 as TaskBriefService.require_review
    participant p17 as postponement_actions
    participant p18 as AgentWorkService._start_blockers
    participant p19 as provenance_blockers
    participant p20 as next_step_for
    participant p21 as window_authority_matches
    participant p22 as require_provenance_recorder
    participant p23 as DeliveryDependencyService.projection
    participant p24 as require_acceptable
    participant p25 as different_publisher_required
    participant p26 as recovery_attestation_hint
    participant p27 as ManualProvenanceService._require_no_recorded_execution
    participant p28 as AgentWorkService._resolve_rollout
    participant p29 as HTTPException
    participant p30 as self.db.info.get (backend/app/services/task…TaskDetailService.my_work)
    p0->>p1: TaskDetailService.my_work
    p0->>p2: TaskDetailService
    p1->>p3: local_work_profile
    p1->>p4: TaskDetailService.references
    p1->>p5: require_project
    p1->>p6: TaskDetailService.page
    p1->>p7: TaskDetailService._policy_flags
    p1->>p8: TaskDomainService.allowed_actions
    p8->>p9: TaskDomainService._policy_task
    p5->>p10: get_settings
    p4->>p11: displayed_state_expression
    p8->>p12: DeliveryDependencyService.ready
    p8->>p13: action_projection
    p8->>p14: replaced_by
    p8->>p15: replacing
    p8->>p16: TaskBriefService.require_review
    p8->>p17: postponement_actions
    p8->>p18: AgentWorkService._start_blockers
    p8->>p19: provenance_blockers
    p8->>p20: next_step_for
    p18->>p21: window_authority_matches
    p19->>p22: require_provenance_recorder
    p12->>p23: DeliveryDependencyService.projection
    p16->>p24: require_acceptable
    p16->>p25: different_publisher_required
    p18->>p26: recovery_attestation_hint
    p19->>p27: ManualProvenanceService._require_no_recorded_execution
    p18->>p28: AgentWorkService._resolve_rollout
    p0-->>p29: HTTPException(422, detail=[...])
    p1-->>p30: self.db.info.get (backend/app/services/task…TaskDetailService.my_work)('authority')
```

> Call sequence diagram shows 30 of 903 interactions; 873 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 1 of 218 (217 omitted); unresolved 1 of 467 (466 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/services/identity_service.py:local_work_profile` | 4 | [backend/app/authority.py](../modules/authority.md) | internal | 1 |
| `backend/app/authority.py:internal_authority` | 5 | - | unresolved | 1 |
| `backend/app/services/identity_service.py:local_work_profile` | 4 | - | unresolved | 1 |
| `backend/app/services/task_detail_service.py:TaskDetailService.my_work` | 2 | - | unresolved | 31 |
| `backend/app/services/task_detail_service.py:TaskDetailService.my_work` | 2 | - | external | 8 |
| `backend/app/services/task_detail_service.py:TaskDetailService.references` | 13 | - | unresolved | 10 |
| `backend/app/services/task_detail_service.py:TaskDetailService.references` | 13 | - | external | 2 |
| `backend/app/services/task_display_state.py:displayed_state_expression` | 18 | - | external | 1 |
> Omission summary shows 8 of 190 groups; 182 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 219; effect analysis evaluated: 155, partial: 8, unavailable: 56. Counts include steps omitted from the displayed trace.

Collector observations for 163 source steps with known totals: observed: 1021, emitted: 964, omitted: 57. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector omitted observations before flow assembly; displayed effects are partial.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `human_my_work` | `available` | `evaluated` | `available` | `7` | `7` | `0` |
| `TaskDetailService.my_work` | `available` | `partial` | `available` | `23` | `19` | `4` |
| `self.db.info.get (backend/app/services/task…TaskDetailService.my_work)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `local_work_profile` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `internal_authority` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `db.info.get (backend/app/authority.py:internal_authority)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `db.get (backend/app/services/iden…ice.py:local_work_profile)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select(…).where (backend/app/services/task…TaskDetailService.my_work)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select (backend/app/services/task…TaskDetailService.my_work)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `or_ (backend/app/services/task…TaskDetailService.my_work)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `Task.assignee_id.in_` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `self.references().where` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. human_my_work"]
    s2["2. TaskDetailService.my_work"]
    s3["3. self.db.info.get (backend/app/services/task…TaskDetailService.my_work)"]
    s4["4. local_work_profile"]
    s5["5. internal_authority"]
    s6["6. db.info.get (backend/app/authority.py:internal_authority)"]
    s7["7. db.get (backend/app/services/iden…ice.py:local_work_profile)"]
    s8["8. select(…).where (backend/app/services/task…TaskDetailService.my_work)"]
    s9["9. select (backend/app/services/task…TaskDetailService.my_work)"]
    s10["10. or_ (backend/app/services/task…TaskDetailService.my_work)"]
    s11["11. Task.assignee_id.in_"]
    s12["12. self.references().where"]
    s1 -->|"TaskDetailService.my_work(limit=limit, after_id=after_id, project_id=project_id, iteration_id=iteration_id, backlog_only=backlog_only)"| s2
    s2 -. "self.db.info.get (backend/app/services/task…TaskDetailService.my_work)('authority')" .-> s3
    s2 -->|"local_work_profile(self.db, authority.profile_id)"| s4
    s4 -->|"internal_authority(db)"| s5
    s5 -. "db.info.get (backend/app/authority.py:internal_authority)('authority_internal', False)" .-> s6
    s4 -. "db.get (backend/app/services/iden…ice.py:local_work_profile)(TeamMemberProfile, profile_id)" .-> s7
    s2 -. "select(…).where (backend/app/services/task…TaskDetailService.my_work)(...)" .-> s8
    s2 -. "select (backend/app/services/task…TaskDetailService.my_work)(TeamMember.id)" .-> s9
    s2 -. "or_ (backend/app/services/task…TaskDetailService.my_work)(..., Task.assignee_id.in_(...))" .-> s10
    s2 -. "Task.assignee_id.in_(capacity_rows)" .-> s11
    s2 -. "self.references().where(mine, or_(...), ..., Task.canceled_at.is_(...), Task.is_summary.is_(...))" .-> s12
    b0["mutation stopped.append"]
    s2 -. "mutation stopped.append" .-> b0
    click s1 "../modules/routers_task_domain.md"
    click s2 "../modules/task_detail_service.md"
    click s4 "../modules/identity_service.md"
    click s5 "../modules/authority.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `human_my_work` | `db: DB`, `limit: int`, `after_id: int`, `project_id: int \| None`, `iteration_id: int \| None`, `backlog_only: bool` | - | - | `...` |
| `TaskDetailService.my_work` | `limit`, `after_id`, `project_id`, `iteration_id`, `backlog_only` | `self.db`, `Task`, `Task`, `Task`, `Task`, `self.db`, `Task`, `Task` | `item.reviewer_name` | `unlinked`, `unlinked`, `{...}`, `{...}` |
| `self.db.info.get (backend/app/services/task…TaskDetailService.my_work)` | - | - | - | - |
| `local_work_profile` | `db`, `profile_id` | - | - | `None`, `...` |
| `internal_authority` | `db` | - | `db.info[...]`, `db.info[...]` | - |
| `db.info.get (backend/app/authority.py:internal_authority)` | - | - | - | - |
| `db.get (backend/app/services/iden…ice.py:local_work_profile)` | - | - | - | - |
| `select(…).where (backend/app/services/task…TaskDetailService.my_work)` | - | - | - | - |
| `select (backend/app/services/task…TaskDetailService.my_work)` | - | - | - | - |
| `or_ (backend/app/services/task…TaskDetailService.my_work)` | - | - | - | - |
| `Task.assignee_id.in_` | - | - | - | - |
| `self.references().where` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| human_my_work | TaskDetailService.my_work | 164 | `TaskDetailService(db).my_work(limit=limit, after_id=after_id, project_id=project_id, iteration_id=iteration_id, backlog_only=backlog_only)` |
| TaskDetailService.my_work | self.db.info.get (backend/app/services/task…TaskDetailService.my_work) | 118 | `self.db.info.get('authority')` |
| TaskDetailService.my_work | local_work_profile | 126 | `local_work_profile(self.db, authority.profile_id)` |
| local_work_profile | internal_authority | 59 | `internal_authority(db)` |
| internal_authority | db.info.get (backend/app/authority.py:internal_authority) | 114 | `db.info.get('authority_internal', False)` |
| local_work_profile | db.get (backend/app/services/iden…ice.py:local_work_profile) | 60 | `db.get(TeamMemberProfile, profile_id)` |
| TaskDetailService.my_work | select(…).where (backend/app/services/task…TaskDetailService.my_work) | 132 | `select(TeamMember.id).where(...)` |
| TaskDetailService.my_work | select (backend/app/services/task…TaskDetailService.my_work) | 132 | `select(TeamMember.id)` |
| TaskDetailService.my_work | or_ (backend/app/services/task…TaskDetailService.my_work) | 133 | `or_(..., Task.assignee_id.in_(...))` |
| TaskDetailService.my_work | Task.assignee_id.in_ | 133 | `Task.assignee_id.in_(capacity_rows)` |
| TaskDetailService.my_work | self.references().where | 135 | `self.references().where(mine, or_(...), ..., Task.canceled_at.is_(...), Task.is_summary.is_(...))` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `stopped.append` | `TaskDetailService.my_work` | 159 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `TaskDetailService.my_work` | `self.db.info.get` | 118 |
| unresolved_call | `internal_authority` | `db.info.get` | 114 |
| unresolved_call | `local_work_profile` | `db.get` | 60 |
| unresolved_call | `TaskDetailService.my_work` | `select(TeamMember.id).where` | 132 |
| external_call | `TaskDetailService.my_work` | `select` | 132 |
| external_call | `TaskDetailService.my_work` | `or_` | 133 |
| unresolved_call | `TaskDetailService.my_work` | `Task.assignee_id.in_` | 133 |
| unresolved_call | `TaskDetailService.my_work` | `self.references().where` | 135 |
| step_limit | `human_my_work` | `first 12 steps` | 0 |
| truncated_flow | `human_my_work` | `depth limit` | 0 |

## Behavior

Returns authenticated ownership queues across visible projects, including nested/backlog work. Optional project, iteration and backlog filters apply before cursor pagination; incompatible iteration/backlog selection fails explicitly. Missing profile or membership is explicit. Page cursors are live observations rather than a frozen complete inventory.

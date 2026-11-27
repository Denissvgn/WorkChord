# AgentTeamSetupService

**Location:** `backend/app/services/agent_team_setup_service.py:231`
**Kind:** Class
**Bases:** —
**Module:** [agent_team_setup_service](../modules/agent_team_setup_service.md)

## Description

Reconcile one portable topology without making the UI a control plane.

Uses the bundle service's deployed, integrity-validated catalog for role-package compatibility. An unavailable or invalid release fails closed with the existing setup conflict code, including when the application is installed as a wheel without a source checkout.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(db: AsyncSession, *, credential_sink: AgentTeamCredentialSink \| None = None, skill_bundle_service: AgentSkillBundleService \| None = None)` | — | — |
| `_require_operator` | `(actor: AgentActor) -> None` | `@staticmethod` | — |
| `_principal_key` | `(actor: AgentActor) -> str` | `@staticmethod` | — |
| `_supported_features` | `() -> frozenset[str]` | `@staticmethod` | — |
| `_skill_catalog` | `() -> SkillBundleCatalogResponse` | — | — |
| `_compatibility_blockers` | *(async)* `(manifest: AgentTeamMaster) -> tuple[str, ...]` | — | — |
| `validate` | *(async)* `(actor: AgentActor, request: AgentTeamManifestRequest) -> AgentTeamValidateResponse` | — | Validate canonical bytes plus current server/package compatibility. |
| `_topology` | *(async)* `(topology_key: str, *, for_update: bool = False, load_members: bool = False) -> AgentTeamTopology \| None` | — | — |
| `_current_snapshot` | *(async)* `(manifest: AgentTeamMaster) -> AgentTeamCurrentSnapshot` | — | — |
| `_action_with` | `(action: AgentTeamPlanAction, **updates: Any) -> AgentTeamPlanAction` | `@staticmethod` | — |
| `_actor_by_name` | *(async)* `(name: str) -> AgentActor \| None` | — | — |
| `_actual_member_drift` | `(actor: AgentActor, desired: AgentTeamMemberSpec) -> tuple[tuple[str, ...], bool]` | `@staticmethod` | — |
| `plan` | *(async)* `(actor: AgentActor, request: AgentTeamPlanRequest) -> AgentTeamReconciliationPlan` | — | Return the exact current redacted plan without mutating any object. |
| `_find_apply_run` | *(async)* `(*, principal_key: str, idempotency_key: str) -> AgentTeamApplyRun \| None` | — | — |
| `_apply_request_digest` | `(request: AgentTeamApplyRequest, command: AgentPlanningCommandContext) -> str` | `@staticmethod` | — |
| `_receipt_from_record` | `(record: AgentTeamActionReceiptRecord) -> AgentTeamActionReceipt` | `@staticmethod` | — |
| `_replay_apply` | *(async)* `(run: AgentTeamApplyRun, *, request_digest: str) -> AgentTeamApplyResponse \| None` | — | — |
| `_ensure_topology_for_apply` | *(async)* `(manifest: AgentTeamMaster, run: AgentTeamApplyRun) -> tuple[AgentTeamTopology, bool]` | — | — |
| `_resolve_profile` | *(async)* `(member: AgentTeamMemberSpec) -> TeamMemberProfile` | — | — |
| `_catalog_entries` | *(async)* `(member: AgentTeamMemberSpec) -> dict[str, AgentModelCatalogEntry]` | — | — |
| `_reconcile_bindings` | *(async)* `(*, topology: AgentTeamTopology, actor: AgentActor, member: AgentTeamMemberSpec, entries: dict[str, AgentModelCatalogEntry], allow_binding_replacement: bool = False) -> dict[str, int]` | — | — |
| `_upsert_managed_object` | *(async)* `(*, topology: AgentTeamTopology, object_type: str, logical_key: str, object_id: int, object_revision: int, desired_digest: str, allow_object_replacement: bool = False) -> None` | — | — |
| `_set_member_contract` | `(record: AgentTeamTopologyMember, member: AgentTeamMemberSpec) -> None` | `@staticmethod` | — |
| `_member_record` | *(async)* `(topology_id: int, actor_key: str, *, for_update: bool = False) -> AgentTeamTopologyMember \| None` | — | — |
| `_stage_event` | *(async)* `(*, event_type: str, actor_id: int \| None, correlation_id: str, idempotency_key: str \| None, payload: dict[str, Any]) -> None` | — | — |
| `_apply_create_or_update` | *(async)* `(*, topology: AgentTeamTopology, member: AgentTeamMemberSpec, action: AgentTeamPlanAction, run: AgentTeamApplyRun) -> tuple[AgentTeamActionReceipt, bool]` | — | — |
| `_apply_identity_replacement` | *(async)* `(*, topology: AgentTeamTopology, member: AgentTeamMemberSpec, action: AgentTeamPlanAction, run: AgentTeamApplyRun) -> tuple[AgentTeamActionReceipt, bool]` | — | — |
| `_apply_replace_recovery` | *(async)* `(*, topology: AgentTeamTopology, member: AgentTeamMemberSpec, action: AgentTeamPlanAction, run: AgentTeamApplyRun) -> tuple[AgentTeamActionReceipt, bool]` | — | — |
| `_apply_disable` | *(async)* `(*, topology: AgentTeamTopology, action: AgentTeamPlanAction, run: AgentTeamApplyRun) -> tuple[AgentTeamActionReceipt, bool]` | — | — |
| `_record_action_receipt` | *(async)* `(run: AgentTeamApplyRun, receipt: AgentTeamActionReceipt) -> None` | — | — |
| `_execute_action` | *(async)* `(*, manifest: AgentTeamMaster, action: AgentTeamPlanAction, run: AgentTeamApplyRun, confirmed_action_ids: set[str]) -> tuple[AgentTeamActionReceipt, bool, bool]` | — | — |
| `_profile_revision` | *(async)* `(actor: AgentActor) -> str` | — | — |
| `_binding_revisions` | *(async)* `(actor: AgentActor) -> dict[str, int]` | — | — |
| `_unverified_tool_tags` | *(async)* `(actor: AgentActor \| None, member: AgentTeamMemberSpec) -> dict[str, tuple[str, ...]]` | — | Declared tool tags the binding does not carry yet, per binding key. |
| `_tool_capability_action` | `(gaps: dict[str, tuple[str, ...]]) -> str \| None` | `@staticmethod` | — |
| `_runtime_identity_status` | `(record: AgentTeamTopologyMember, *, expected_instance_id: str, acknowledgement: dict[str, Any]) -> AgentTeamRuntimeIdentityStatus` | `@staticmethod` | Read the acknowledging identity from the acknowledgement, and any change or refusal from stored state. |
| `_handoff` | *(async)* `(*, topology: AgentTeamTopology, manifest: AgentTeamMaster, member_record: AgentTeamTopologyMember, member: AgentTeamMemberSpec) -> AgentTeamRuntimeHandoff \| None` | — | — |
| `_refresh_handoffs` | *(async)* `(topology: AgentTeamTopology, manifest: AgentTeamMaster) -> None` | — | — |
| `apply` | *(async)* `(actor: AgentActor, request: AgentTeamApplyRequest, *, command: AgentPlanningCommandContext) -> AgentTeamApplyResponse` | — | Apply only exact approved action IDs and persist resumable receipts. |
| `_select_status_topology` | *(async)* `(actor: AgentActor, topology_key: str \| None) -> tuple[AgentTeamTopology \| None, bool]` | — | — |
| `_absent_steps` | `() -> tuple[AgentTeamSetupStep, ...]` | `@staticmethod` | — |
| `starting_points` | *(async)* `(actor: AgentActor, *, server_url: str) -> dict[str, Any]` | — | Two places to start editing: the applied manifest, and a template. |
| `status` | *(async)* `(actor: AgentActor, *, topology_key: str \| None = None) -> AgentTeamStatusResponse` | — | Return backend-derived secret-free setup and runtime readiness. |
| `topology` | *(async)* `(actor: AgentActor \| None, *, topology_key: str \| None = None) -> AgentTeamTopologyResponse` | — | Who is on the team, and which runtime reference runs each member. |
| `report` | *(async)* `(actor: AgentActor, *, topology_key: str \| None = None) -> AgentTeamSetupReport` | — | Return a bounded redacted report without availability overclaims. |
| `_status_for_topology` | *(async)* `(topology: AgentTeamTopology, *, can_mutate: bool, persist_state: bool) -> AgentTeamStatusResponse` | — | — |
| `_count_ack_attempt` | `(member: AgentTeamTopologyMember) -> None` | `@staticmethod` | — |
| `_increment_ack_attempt` | *(async)* `(member: AgentTeamTopologyMember) -> None` | — | — |
| `_refuse_foreign_runtime_instance` | *(async)* `(actor: AgentActor, supplied_instance_id: str \| None) -> None` | — | Turn away an acknowledgement that returns an identity other than the issued one, and record it. |
| `acknowledge_runtime` | *(async)* `(api_key: str, acknowledgement: AgentTeamRuntimeAcknowledgement) -> AgentTeamRuntimeAcknowledgementResponse` | — | Accept only the exact restricted onboarding handoff acknowledgement. |
| `membership_boundary` | *(async)* `(actor_id: int) -> AgentTeamMembershipBoundary \| None` | — | Return the live, drift-aware topology boundary for one bound actor. |
| `require_dispatch_member` | *(async)* `(principal: AgentActor, target_actor_id: int) -> AgentTeamMembershipBoundary \| None` | — | Fail closed when a bound caller selects outside its active roster. |
| `_project_allows` | `(project_id: int \| None, action: str) -> bool` | — | Whether the caller's authority covers the project, without raising. |
| `_whole_team_readiness` | `(boundary: AgentTeamMembershipBoundary) -> AgentRoutingTopologyReadiness` | `@staticmethod` | — |
| `readiness_gate` | *(async)* `(principal: AgentActor, *, verifier_actor_id: int \| None = None, project_id: int \| None = None, action: str = 'manage', observed_boundaries: dict[int, AgentTeamMembershipBoundary \| None] \| None = None) -> tuple[AgentRoutingTopologyReadiness, dict[str, Any]]` | — | Judge routing readiness and say who is missing when it is not met. |
| `routing_readiness` | *(async)* `(actor: AgentActor, *, observed_boundaries: dict[int, AgentTeamMembershipBoundary \| None] \| None = None) -> AgentRoutingTopologyReadiness` | — | Project authoritative setup state into the rollout readiness hook. |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentTeamSetupService (backend/app/services/agent_team_setup_service.py)"]
    n1["get_agent_capabilities (backend/app/mcp_agent_tools.py)"]
    n2["get_agent_team_setup_status (backend/app/mcp_agent_tools.py)"]
    n3["get_agent_team_topology (backend/app/mcp_agent_tools.py)"]
    n4["acknowledge_agent_team_runtime (backend/app/routers/agent.py)"]
    n5["apply_agent_team_reconciliation (backend/app/routers/agent.py)"]
    n6["get_agent_capabilities (backend/app/routers/agent.py)"]
    n7["get_agent_team_setup_report (backend/app/routers/agent.py)"]
    n8["get_agent_team_setup_service (backend/app/routers/agent.py)"]
    n9["get_agent_team_setup_status (backend/app/routers/agent.py)"]
    n10["get_agent_team_starting_points (backend/app/routers/agent.py)"]
    n11["get_agent_team_topology (backend/app/routers/agent.py)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    n10 --> n0
    n11 --> n0
    click n0 "../modules/agent_team_setup_service.md"
    click n1 "../modules/mcp_agent_tools.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/mcp_agent_tools.md"
    click n4 "../modules/routers_agent.md"
    click n5 "../modules/routers_agent.md"
    click n6 "../modules/routers_agent.md"
    click n7 "../modules/routers_agent.md"
    click n8 "../modules/routers_agent.md"
    click n9 "../modules/routers_agent.md"
    click n10 "../modules/routers_agent.md"
    click n11 "../modules/routers_agent.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_team_setup_service](../modules/agent_team_setup_service.md) | 56 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `get_agent_capabilities` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 1 |
| `get_agent_team_setup_status` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 1 |
| `get_agent_team_topology` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 1 |
| `acknowledge_agent_team_runtime` | type_reference | [routers_agent](../modules/routers_agent.md) | — |
| `apply_agent_team_reconciliation` | type_reference | [routers_agent](../modules/routers_agent.md) | — |
| `get_agent_capabilities` | call | [routers_agent](../modules/routers_agent.md) | 1 |
| `get_agent_team_setup_report` | type_reference | [routers_agent](../modules/routers_agent.md) | — |
| `get_agent_team_setup_service` | call | [routers_agent](../modules/routers_agent.md) | 1 |
| `get_agent_team_setup_service` | type_reference | [routers_agent](../modules/routers_agent.md) | — |
| `get_agent_team_setup_status` | type_reference | [routers_agent](../modules/routers_agent.md) | — |
| `get_agent_team_starting_points` | type_reference | [routers_agent](../modules/routers_agent.md) | — |
| `get_agent_team_topology` | type_reference | [routers_agent](../modules/routers_agent.md) | — |

> References: showing 12 of 59 logical references; 47 omitted by the 12-row generated summary limit.

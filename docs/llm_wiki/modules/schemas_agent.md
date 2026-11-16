# agent Module

**Path:** `backend/app/schemas/agent.py`

## Description

Agent task context retains its legacy Markdown projection for compatibility. The derived `brief_source` identifies `task.brief` as authoritative whenever it exists, including criterion identities and revisions; it does not duplicate mutable brief content.

Agent integration API schemas.

Run and begin metadata may carry an actor-declared `harness` object with a short lowercase runtime `kind` and the runtime's `session_id`; its shape is checked (no paths, no credential-shaped values) and its value is stored without verification.

## Imports

| Source | Symbols |
|--------|---------|
| `app.autonomy.canonical` | `ensure_secret_free` |
| `app.schemas.agent_routing` | `AgentModelBindingResponse` |
| `app.schemas.project` | `ProjectHealth`, `ProjectUpdateEntryResponse` |
| `app.schemas.request_source` | `RequestSourceLinkWithSourceResponse` |
| `app.schemas.task` | `TaskCreate`, `TaskResponse`, `TaskStatus`, `TaskUpdate` |
| `app.schemas.task_brief` | `CriterionProgress` |
| `app.schemas.triage` | `TriageItemResponse` |
| `app.services.agent_routing_policy` | `SERVER_OWNED_ROUTING_SNAPSHOT_SCHEMAS`, `assignment_intent`, `validate_routing_packet_size` |
| `app.utils.url_policy` | `URLPolicyError`, `normalize_stored_display_url` |
| `datetime` | `datetime` |
| `json` | `json` |
| `pydantic` | `BaseModel`, `ConfigDict`, `Field`, `computed_field`, `field_validator`, `model_validator` |
| `re` | `re` |
| `typing` | `Any`, `Literal`, `Optional` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/app/schemas/agent.py"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/schemas_agent.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (27) |
| Outbound | `backend` (9) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

> All 36 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [AgentActorModelBindingCreate](../entities/AgentActorModelBindingCreate.md) | Pydantic model | 148 | `BaseModel` | Secret-free model binding optionally created with a new actor. |
| [AgentActorCreate](../entities/AgentActorCreate.md) | Pydantic model | 186 | `BaseModel` | Request for creating an agent actor. |
| [AgentActorUpdate](../entities/AgentActorUpdate.md) | Pydantic model | 209 | `BaseModel` | Administrative update for a provisioned actor. |
| [AgentActorResponse](../entities/AgentActorResponse.md) | Pydantic model | 250 | `BaseModel` | Agent actor response. |
| [AgentActorCreatedResponse](../entities/AgentActorCreatedResponse.md) | Pydantic model | 267 | `AgentActorResponse` | Agent actor creation response including the one-time API key. |
| [AgentTaskCreate](../entities/AgentTaskCreate.md) | Pydantic model | 276 | `TaskCreate` | Agent task creation request. |
| [AgentTaskPatch](../entities/AgentTaskPatch.md) | Pydantic model | 281 | `TaskUpdate` | Agent task patch request with optimistic concurrency. |
| [TaskClaimRequest](../entities/TaskClaimRequest.md) | Pydantic model | 288 | `BaseModel` | Request to claim or renew a task lease. |
| [TaskClaimResponse](../entities/TaskClaimResponse.md) | Pydantic model | 298 | `BaseModel` | Response for task lease operations. |
| [TaskEventCreate](../entities/TaskEventCreate.md) | Pydantic model | 306 | `BaseModel` | Request to append a task event. |
| [TaskEventResponse](../entities/TaskEventResponse.md) | Pydantic model | 337 | `BaseModel` | Task event response. |
| [AgentRunCreate](../entities/AgentRunCreate.md) | Pydantic model | 352 | `BaseModel` | Request to start an agent run. |
| [AgentRunEventCreate](../entities/AgentRunEventCreate.md) | Pydantic model | 385 | `BaseModel` | Request to append an agent run event. |
| [AgentRunFinish](../entities/AgentRunFinish.md) | Pydantic model | 409 | `BaseModel` | Request to finish an agent run. |
| [AgentRunEventResponse](../entities/AgentRunEventResponse.md) | Pydantic model | 431 | `BaseModel` | Agent run event response. |
| [AgentRunResponse](../entities/AgentRunResponse.md) | Pydantic model | 445 | `BaseModel` | Agent run response. |
| [TaskTimelineItem](../entities/schemas_agent_TaskTimelineItem.md) | Pydantic model | 486 | `BaseModel` | Merged timeline item for a task. |
| [TaskTimelineResponse](../entities/schemas_agent_TaskTimelineResponse.md) | Pydantic model | 498 | `BaseModel` | Merged task timeline response. |
| [TaskTimelinePageItem](../entities/TaskTimelinePageItem.md) | Pydantic model | 504 | `TaskTimelineItem` | — |
| [TaskTimelinePage](../entities/TaskTimelinePage.md) | Pydantic model | 508 | `BaseModel` | — |
| [AgentPipelineResponse](../entities/AgentPipelineResponse.md) | Pydantic model | 517 | `BaseModel` | Agent supervision pipeline; every open task appears in exactly one stage. |
| [AgentRunDetailResponse](../entities/AgentRunDetailResponse.md) | Pydantic model | 531 | `AgentRunResponse` | Full detail of an agent run including its list of chronological trace events. |
| [AgentAssignmentPurpose](../entities/schemas_agent_AgentAssignmentPurpose.md) | Type alias | 538 | `Literal['execution', 'verification']` | — |
| [AgentAssignmentQueueClass](../entities/schemas_agent_AgentAssignmentQueueClass.md) | Type alias | 539 | `Literal['normal', 'rework', 'recovery']` | — |
| [AgentAssignmentState](../entities/schemas_agent_AgentAssignmentState.md) | Type alias | 540 | `Literal['queued', 'accepted', 'fulfilled', 'cancelled']` | — |
| [AgentTaskAssignmentCreate](../entities/AgentTaskAssignmentCreate.md) | Pydantic model | 543 | `BaseModel` | PM command to dispatch a task to an exact actor. |
| [ModelAwareAgentTaskAssignmentCreate](../entities/schemas_agent_ModelAwareAgentTaskAssignmentCreate.md) | Pydantic model | 590 | `BaseModel` | PM command to dispatch one preview-selected actor/model binding. |
| [AgentTaskAssignmentUpdate](../entities/AgentTaskAssignmentUpdate.md) | Pydantic model | 635 | `BaseModel` | PM command to reorder, reassign, or cancel a queued assignment. |
| [ModelAwareAgentTaskAssignmentUpdate](../entities/schemas_agent_ModelAwareAgentTaskAssignmentUpdate.md) | Pydantic model | 649 | `BaseModel` | PM command to reroute queued work through a fresh routing preview. |
| [AgentTaskAssignmentResponse](../entities/AgentTaskAssignmentResponse.md) | Pydantic model | 684 | `BaseModel` | Durable agent task assignment response. |
| [AgentAssignmentActorSummary](../entities/AgentAssignmentActorSummary.md) | Pydantic model | 714 | `BaseModel` | The actor an assignment names, so a person can tell who holds the work. |
| [AgentAssignmentModelSummary](../entities/AgentAssignmentModelSummary.md) | Pydantic model | 723 | `BaseModel` | The model an assignment's binding declares; a declaration, not an attestation. |
| [AgentAssignmentReadItem](../entities/schemas_agent_AgentAssignmentReadItem.md) | Pydantic model | 731 | `BaseModel` | An assignment as a person reads it: who holds which task, for what, and on which model. |
| [AgentRoutingTopologyReadinessResponse](../entities/AgentRoutingTopologyReadinessResponse.md) | Pydantic model | 763 | `BaseModel` | Bounded server-owned topology readiness exposed to agent clients. |
| [AgentRoutingRolloutStatusResponse](../entities/AgentRoutingRolloutStatusResponse.md) | Pydantic model | 781 | `BaseModel` | Explicit configured and effective model-aware routing rollout state. |
| [AgentCapabilitiesResponse](../entities/AgentCapabilitiesResponse.md) | Pydantic model | 793 | `BaseModel` | Authenticated compatibility and actor capability handshake. |
| [AgentActorRosterProfileSkill](../entities/schemas_agent_AgentActorRosterProfileSkill.md) | Pydantic model | 817 | `BaseModel` | Bounded capability evidence attached to one roster profile. |
| [AgentActorRosterProfile](../entities/schemas_agent_AgentActorRosterProfile.md) | Pydantic model | 830 | `BaseModel` | Secret-free profile projection used for exact-actor routing. |
| [AgentActorRosterItem](../entities/schemas_agent_AgentActorRosterItem.md) | Pydantic model | 843 | `AgentActorResponse` | Secret-free actor dispatch roster item. |
| [AgentDependencyContext](../entities/AgentDependencyContext.md) | Pydantic model | 857 | `BaseModel` | Dependency state returned in complete worker context. |
| [AgentTaskContextResponse](../entities/AgentTaskContextResponse.md) | Pydantic model | 866 | `BaseModel` | Complete task context for an assigned worker. |
| [AgentWorkItem](../entities/AgentWorkItem.md) | Pydantic model | 892 | `BaseModel` | One ordered assigned-work item. |
| [AgentPaginationMetadata](../entities/AgentPaginationMetadata.md) | Pydantic model | 905 | `BaseModel` | Opaque snapshot-bound pagination metadata shared by REST and MCP. |
| [AgentCollectionPageMetadata](../entities/AgentCollectionPageMetadata.md) | Pydantic model | 915 | `BaseModel` | Per-collection counts for compound assigned-work pages. |
| [AgentWorkPaginationMetadata](../entities/AgentWorkPaginationMetadata.md) | Pydantic model | 922 | `AgentPaginationMetadata` | Pagination metadata for ready and blocked assigned-work collections. |
| [AgentWorkDecisionResponse](../entities/AgentWorkDecisionResponse.md) | Pydantic model | 929 | `BaseModel` | Server-authoritative current/next work decision. |
| [AgentReviewQueueResponse](../entities/AgentReviewQueueResponse.md) | Pydantic model | 947 | `BaseModel` | Paginated verifier queue projection. |
| [AgentWorkBegin](../entities/AgentWorkBegin.md) | Pydantic model | 954 | `BaseModel` | Atomically accept and start a server-selected work assignment. |
| [ModelAwareAgentWorkBegin](../entities/ModelAwareAgentWorkBegin.md) | Pydantic model | 975 | `BaseModel` | Atomically begin only the model binding selected by routing. |
| [AgentWorkBeginResponse](../entities/AgentWorkBeginResponse.md) | Pydantic model | 1006 | `BaseModel` | Atomic begin result containing all new authoritative state. |
| [AgentWorkRenew](../entities/AgentWorkRenew.md) | Pydantic model | 1018 | `BaseModel` | Renew the live fence for one accepted assignment and running run. |
| [AgentWorkSubmit](../entities/AgentWorkSubmit.md) | Pydantic model | 1034 | `BaseModel` | Atomically submit an active assignment for verification. |
| [AgentWorkTerminal](../entities/AgentWorkTerminal.md) | Pydantic model | 1071 | `BaseModel` | Atomically fail or cancel an active assignment. |
| [AgentWorkTerminalResponse](../entities/AgentWorkTerminalResponse.md) | Pydantic model | 1094 | `BaseModel` | Atomic submit/fail result. |
| [AgentReviewVerdict](../entities/AgentReviewVerdict.md) | Pydantic model | 1103 | `BaseModel` | Verifier-scoped pass or rejection command. |
| [AgentReviewVerdictResponse](../entities/AgentReviewVerdictResponse.md) | Pydantic model | 1125 | `BaseModel` | Verification result plus optional rework assignment. |
| [AgentRecoveryRequeue](../entities/AgentRecoveryRequeue.md) | Pydantic model | 1133 | `BaseModel` | PM command to replace stale execution ownership with recovery work. |
| [AgentRecoveryItem](../entities/AgentRecoveryItem.md) | Pydantic model | 1147 | `BaseModel` | Typed PM recovery diagnosis and optimistic ownership tuple. |
| [AgentRecoveryListResponse](../entities/AgentRecoveryListResponse.md) | Pydantic model | 1162 | `BaseModel` | Paginated PM recovery projection. |
| [AgentRecoveryRequeueResponse](../entities/AgentRecoveryRequeueResponse.md) | Pydantic model | 1169 | `BaseModel` | Authoritative result of stale-work reconciliation and requeue. |
| [AgentProjectUpdateCreate](../entities/AgentProjectUpdateCreate.md) | Pydantic model | 1178 | `BaseModel` | Agent-authored append-only project status report. |
| [AgentProjectUpdateResponse](../entities/AgentProjectUpdateResponse.md) | Pydantic model | 1202 | `ProjectUpdateEntryResponse` | Agent project-update response with attribution and evidence. |
| [AgentDiscoveryTriageCreate](../entities/AgentDiscoveryTriageCreate.md) | Pydantic model | 1206 | `BaseModel` | Claim-bound report of work discovered outside the assigned scope. |
| [AgentDiscoveryTriageResponse](../entities/AgentDiscoveryTriageResponse.md) | Pydantic model | 1231 | `TriageItemResponse` | Created discovery Triage item with source linkage metadata. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_validate_actor_scopes` | `(value: list[str]) -> list[str]` | — | — |
| `_validate_harness_metadata` | `(value: dict[str, Any]) -> dict[str, Any]` | — | Check the optional harness session an actor declares when it begins work. |
| `declared_harness` | `(metadata: dict[str, Any]) -> tuple[str \| None, str \| None]` | — | (kind, session_id) from already validated run metadata, or (None, None). |
| `check_harness_identity` | `(kind: Any, session_id: Any, *, label: str) -> None` | — | A short lowercase runtime name and the runtime's own session identifier, never a path or secret. |
| `_validate_bounded_json` | `(value: dict[str, Any], *, label: str) -> dict[str, Any]` | — | Reject persistence packets that can amplify storage and webhook payloads. |
| `_normalize_optional_url` | `(value: Optional[str]) -> Optional[str]` | — | — |
| `_normalize_url_list` | `(values: list[str]) -> list[str]` | — | — |
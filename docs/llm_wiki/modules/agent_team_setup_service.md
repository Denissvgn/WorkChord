# agent_team_setup_service Module

**Path:** `backend/app/services/agent_team_setup_service.py`

## Description

Operator-only agent-team validation, reconciliation, setup, and readiness.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app.agent_contract` | `AGENT_CONTRACT_FEATURES`, `AGENT_TEAM_MASTER_FEATURE`, `MODEL_AWARE_ROUTING_FEATURE` |
| `app.config` | `get_settings` |
| `app.models.agent` | `AgentActor`, `AgentModelBinding`, `AgentModelCatalogEntry`, `AgentRun`, `AgentTeamActionReceipt`, `AgentTeamApplyRun`, `AgentTeamManagedObject`, `AgentTeamTopology`, `AgentTeamTopologyMember`, `AgentTaskAssignment`, `TaskEvent` |
| `app.models.team_member` | `TeamMemberProfile` |
| `app.schemas.agent_planning` | `AgentPlanningCommandContext` |
| `app.schemas.agent_skill_bundle` | `SkillBundleCatalogResponse` |
| `app.schemas.agent_team_setup` | `AGENT_TEAM_PLAN_SCHEMA_VERSION`, `MAX_AGENT_TEAM_ACTIONS`, `ROLE_SCOPE_PRESETS`, `AgentTeamActionReceipt`, `AgentTeamActionStatus`, `AgentTeamApplyRequest`, `AgentTeamApplyResponse`, `AgentTeamCurrentMember`, `AgentTeamCurrentSnapshot`, `AgentTeamManifestRequest`, `AgentTeamMaster`, `AgentTeamMemberLifecycle`, `AgentTeamMemberSpec`, `AgentTeamMemberStatus`, `AgentTeamPlanAction`, `AgentTeamPlanRequest`, `AgentTeamReconciliationClass`, `AgentTeamReconciliationPlan`, `AgentTeamRuntimeAcknowledgement`, `AgentTeamRuntimeAcknowledgementResponse`, `AgentTeamRuntimeHandoff`, `AgentTeamDispatchAvailability`, `AgentTeamSetupReport`, `AgentTeamSetupReportCounts`, `AgentTeamSetupReportEvidence`, `AgentTeamSetupStep`, `AgentTeamSkillPackage`, `AgentTeamStatusResponse`, `AgentTeamValidateResponse`, `ensure_agent_team_secret_free`, `parse_agent_team_master`, `reconcile_agent_team_master` |
| `app.services.agent_profile_catalog_service` | `ALL_PROFILE_PRESETS`, `AgentProfileCatalogService` |
| `app.services.agent_routing_rollout` | `AgentRoutingTopologyReadiness` |
| `app.services.agent_service` | `AgentConflictError`, `AgentPermissionError`, `AgentService`, `actor_scopes`, `hash_api_key`, `require_scope`, `validate_idempotency_key` |
| `app.utils.time` | `as_utc`, `utc_now` |
| `dataclasses` | `dataclass` |
| `datetime` | `timedelta` |
| `hashlib` | `hashlib` |
| `json` | `json` |
| `os` | `os` |
| `pathlib` | `Path` |
| `secrets` | `secrets` |
| `sqlalchemy` | `func`, `or_`, `select`, `text` |
| `sqlalchemy.exc` | `IntegrityError` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |
| `sqlalchemy.orm` | `selectinload` |
| `stat` | `stat` |
| `typing` | `Any`, `Protocol` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/app/services/agent_team_setup_service.py"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/agent_team_setup_service.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (5) |
| Outbound | `backend` (11) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

> All 16 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [AgentTeamSetupConflictError](../entities/AgentTeamSetupConflictError.md) | 98 | `AgentConflictError` | Stable conflict envelope shared by setup REST and MCP reads. |
| [CredentialDeliveryError](../entities/CredentialDeliveryError.md) | 111 | `RuntimeError` | Raised when a one-time actor key did not reach the approved sink. |
| [AgentTeamCredentialSink](../entities/AgentTeamCredentialSink.md) | 115 | `Protocol` | One-way sink boundary; implementations never return credential material. |
| [FilesystemAgentTeamCredentialSink](../entities/FilesystemAgentTeamCredentialSink.md) | 135 | — | Write one-time credentials to an operator-owned mode-0700 directory. |
| [AgentTeamMembershipBoundary](../entities/AgentTeamMembershipBoundary.md) | 230 | — | Current topology/revision and active member set for exact-actor routing. |
| [AgentTeamSetupService](../entities/AgentTeamSetupService.md) | 264 | — | Reconcile one portable topology without making the UI a control plane. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_json_loads` | `(value: str \| None, fallback: Any) -> Any` | — | — |
| `_canonical_json` | `(value: Any) -> str` | — | — |
| `_digest` | `(value: Any) -> str` | — | — |

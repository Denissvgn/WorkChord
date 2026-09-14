# autonomy_work_package_service Module

**Path:** `backend/app/services/autonomy_work_package_service.py`

## Description

Fenced, package-level autonomous verification lifecycle service.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app.autonomy.canonical` | `sha256_hex` |
| `app.models.agent` | `AgentActor` |
| `app.models.autonomy` | `AgentAutonomyTopology`, `AgentAutonomyTopologyMember`, `AgentVerificationEvent`, `AgentVerificationRequirement`, `AgentWorkPackage` |
| `app.schemas.autonomy` | `AgentWorkPackageCreate`, `AgentWorkPackageResponse`, `ResolvedVerifierLease`, `VerificationBeginRequest`, `VerificationClaimRequest`, `VerificationRenewRequest`, `VerificationRequirementResponse`, `VerificationSubmitRequest`, `VerificationTransitionResponse` |
| `app.services.agent_service` | `AgentConflictError`, `AgentPermissionError`, `actor_has_scope`, `validate_idempotency_key` |
| `app.utils.time` | `as_utc`, `utc_now` |
| `datetime` | `datetime` |
| `sqlalchemy` | `select` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |
| `sqlalchemy.orm` | `selectinload` |
| `typing` | `Any` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/autonomy/canonical.py"]
    n1["backend/app/models/agent.py"]
    n2["backend/app/models/autonomy.py"]
    n3["backend/app/schemas/autonomy.py"]
    n4["backend/app/services/agent_service.py"]
    n5["backend/app/services/autonomy_work_package_service.py"]
    n6["backend/app/utils/time.py"]
    n7["backend/tests/autonomy/test_work_package_service.py"]
    n1 --> n6
    n2 --> n6
    n4 --> n1
    n4 --> n6
    n5 --> n0
    n5 --> n1
    n5 --> n2
    n5 --> n3
    n5 --> n4
    n5 --> n6
    n7 --> n1
    n7 --> n2
    n7 --> n3
    n7 --> n4
    n7 --> n5
    click n0 "../modules/autonomy_canonical.md"
    click n1 "../modules/models_agent.md"
    click n2 "../modules/models_autonomy.md"
    click n3 "../modules/schemas_autonomy.md"
    click n4 "../modules/agent_service.md"
    click n5 "../modules/autonomy_work_package_service.md"
    click n6 "../modules/time.md"
    click n7 "../modules/test_work_package_service.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [test_work_package_service](../modules/test_work_package_service.md) |
| Outbound | [autonomy_canonical](../modules/autonomy_canonical.md) |
| Outbound | [models_agent](../modules/models_agent.md) |
| Outbound | [models_autonomy](../modules/models_autonomy.md) |
| Outbound | [schemas_autonomy](../modules/schemas_autonomy.md) |
| Outbound | [agent_service](../modules/agent_service.md) |
| Outbound | [time](../modules/time.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [AutonomyWorkPackageService](../entities/AutonomyWorkPackageService.md) | 44 | — | Mirror external-journal decisions without letting Task.status accept work. |

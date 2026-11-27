# AgentTeamMembershipBoundary

**Location:** `backend/app/services/agent_team_setup_service.py:133`
**Kind:** Class
**Bases:** —
**Module:** [agent_team_setup_service](../modules/agent_team_setup_service.md)

**Decorators:** `@dataclass(frozen=True)`

## Description

Current topology/revision and active member set for exact-actor routing.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `topology_id` | `int` | *required* | — |
| `topology_key` | `str` | *required* | — |
| `topology_revision` | `int` | *required* | — |
| `primary_actor_id` | `int \| None` | *required* | — |
| `member_actor_ids` | `frozenset[int]` | *required* | — |
| `runtime_ready_actor_ids` | `frozenset[int]` | *required* | — |
| `non_ready_actors` | `tuple[dict[str, Any], ...]` | `()` | — |
| `maximum_runtime_staleness_seconds` | `int \| None` | `None` | — |
| `topology_runtime_ready` | `bool` | `False` | — |
| `topology_blocker_codes` | `tuple[str, ...]` | `()` | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentTeamMembershipBoundary (backend/app/services/agent_team_setup_service.py)"]
    n1["AgentTeamSetupService._whole_team_readiness (backend/app/services/agent_team_setup_service.py)"]
    n2["AgentTeamSetupService.membership_boundary (backend/app/services/agent_team_setup_service.py)"]
    n3["AgentTeamSetupService.readiness_gate (backend/app/services/agent_team_setup_service.py)"]
    n4["AgentTeamSetupService.require_dispatch_member (backend/app/services/agent_team_setup_service.py)"]
    n5["AgentTeamSetupService.routing_readiness (backend/app/services/agent_team_setup_service.py)"]
    n6["readiness_refusal_context (backend/app/services/agent_team_setup_service.py)"]
    n7["backend/app/services/agent_work_service.py"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    click n0 "../modules/agent_team_setup_service.md"
    click n1 "../modules/agent_team_setup_service.md"
    click n2 "../modules/agent_team_setup_service.md"
    click n3 "../modules/agent_team_setup_service.md"
    click n4 "../modules/agent_team_setup_service.md"
    click n5 "../modules/agent_team_setup_service.md"
    click n6 "../modules/agent_team_setup_service.md"
    click n7 "../modules/agent_work_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_team_setup_service](../modules/agent_team_setup_service.md) | 0 | `maximum_runtime_staleness_seconds`, `member_actor_ids`, `non_ready_actors`, `primary_actor_id`, `runtime_ready_actor_ids`, `topology_blocker_codes`, `topology_id`, `topology_key`, `topology_revision`, `topology_runtime_ready` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `AgentTeamSetupService._whole_team_readiness` | type_reference | [agent_team_setup_service](../modules/agent_team_setup_service.md) | — |
| `AgentTeamSetupService.membership_boundary` | call | [agent_team_setup_service](../modules/agent_team_setup_service.md) | 1 |
| `AgentTeamSetupService.membership_boundary` | type_reference | [agent_team_setup_service](../modules/agent_team_setup_service.md) | — |
| `AgentTeamSetupService.readiness_gate` | type_reference | [agent_team_setup_service](../modules/agent_team_setup_service.md) | — |
| `AgentTeamSetupService.require_dispatch_member` | type_reference | [agent_team_setup_service](../modules/agent_team_setup_service.md) | — |
| `AgentTeamSetupService.routing_readiness` | type_reference | [agent_team_setup_service](../modules/agent_team_setup_service.md) | — |
| `readiness_refusal_context` | type_reference | [agent_team_setup_service](../modules/agent_team_setup_service.md) | — |
| `agent_work_service` | import | [agent_work_service](../modules/agent_work_service.md) | — |

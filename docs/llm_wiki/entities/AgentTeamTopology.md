# AgentTeamTopology

**Location:** `backend/app/models/agent.py:284`
**Kind:** Class
**Bases:** `Base`
**Module:** [models_agent](../modules/models_agent.md)

## Description

Applied portable agent-team manifest and authoritative readiness state.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `Mapped[int]` | `mapped_column(Integer, primary_key=True, autoincrement=True)` | — |
| `topology_key` | `Mapped[str]` | `mapped_column(String(100), unique=True, nullable=False)` | — |
| `revision` | `Mapped[int]` | `mapped_column(Integer, default=1, nullable=False)` | — |
| `manifest_digest` | `Mapped[str]` | `mapped_column(String(64), nullable=False)` | — |
| `manifest_payload` | `Mapped[str]` | `mapped_column(Text, nullable=False)` | — |
| `primary_actor_id` | `Mapped[Optional[int]]` | `mapped_column(Integer, ForeignKey('agent_actors.id', ondelete='RESTRICT'), unique=True, nullable=True)` | — |
| `state` | `Mapped[str]` | `mapped_column(String(30), default='configured', nullable=False)` | — |
| `blocker_codes` | `Mapped[str]` | `mapped_column(Text, default='[]', nullable=False)` | — |
| `created_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), default=utc_now, nullable=False)` | — |
| `updated_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), default=utc_now, onupdate=utc_now, nullable=False)` | — |
| `primary_actor` | `Mapped[Optional['AgentActor']]` | `relationship('AgentActor', foreign_keys=[primary_actor_id])` | — |
| `members` | `Mapped[list['AgentTeamTopologyMember']]` | `relationship('AgentTeamTopologyMember', back_populates='topology', passive_deletes=True, order_by='AgentTeamTopologyMember.actor_key')` | — |
| `managed_objects` | `Mapped[list['AgentTeamManagedObject']]` | `relationship('AgentTeamManagedObject', back_populates='topology', passive_deletes=True)` | — |
| `apply_runs` | `Mapped[list['AgentTeamApplyRun']]` | `relationship('AgentTeamApplyRun', back_populates='topology', passive_deletes=True)` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentTeamTopology (backend/app/models/agent.py)"]
    n1["Base (backend/app/database.py)"]
    n2["backend/app/models/__init__.py"]
    n3["AgentTeamSetupService._apply_create_or_update (backend/app/services/agent_team_setup_service.py)"]
    n4["AgentTeamSetupService._apply_disable (backend/app/services/agent_team_setup_service.py)"]
    n5["AgentTeamSetupService._apply_identity_replacement (backend/app/services/agent_team_setup_service.py)"]
    n6["AgentTeamSetupService._apply_replace_recovery (backend/app/services/agent_team_setup_service.py)"]
    n7["AgentTeamSetupService._ensure_topology_for_apply (backend/app/services/agent_team_setup_service.py)"]
    n8["AgentTeamSetupService._handoff (backend/app/services/agent_team_setup_service.py)"]
    n9["AgentTeamSetupService._increment_ack_attempt (backend/app/services/agent_team_setup_service.py)"]
    n10["AgentTeamSetupService._member_record (backend/app/services/agent_team_setup_service.py)"]
    n11["AgentTeamSetupService._reconcile_bindings (backend/app/services/agent_team_setup_service.py)"]
    n12["AgentTeamSetupService._refresh_handoffs (backend/app/services/agent_team_setup_service.py)"]
    n0 --> n1
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
    n12 --> n0
    click n0 "../modules/models_agent.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/models___init__.md"
    click n3 "../modules/agent_team_setup_service.md"
    click n4 "../modules/agent_team_setup_service.md"
    click n5 "../modules/agent_team_setup_service.md"
    click n6 "../modules/agent_team_setup_service.md"
    click n7 "../modules/agent_team_setup_service.md"
    click n8 "../modules/agent_team_setup_service.md"
    click n9 "../modules/agent_team_setup_service.md"
    click n10 "../modules/agent_team_setup_service.md"
    click n11 "../modules/agent_team_setup_service.md"
    click n12 "../modules/agent_team_setup_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [models_agent](../modules/models_agent.md) | 0 | `apply_runs`, `blocker_codes`, `created_at`, `id`, `managed_objects`, `manifest_digest`, `manifest_payload`, `members`, `primary_actor`, `primary_actor_id`, `revision`, `state` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Base` | [app_database](../modules/app_database.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `AgentTeamSetupService._apply_create_or_update` | type_reference | [agent_team_setup_service](../modules/agent_team_setup_service.md) | — |
| `AgentTeamSetupService._apply_disable` | type_reference | [agent_team_setup_service](../modules/agent_team_setup_service.md) | — |
| `AgentTeamSetupService._apply_identity_replacement` | type_reference | [agent_team_setup_service](../modules/agent_team_setup_service.md) | — |
| `AgentTeamSetupService._apply_replace_recovery` | type_reference | [agent_team_setup_service](../modules/agent_team_setup_service.md) | — |
| `AgentTeamSetupService._ensure_topology_for_apply` | call | [agent_team_setup_service](../modules/agent_team_setup_service.md) | 1 |
| `AgentTeamSetupService._ensure_topology_for_apply` | type_reference | [agent_team_setup_service](../modules/agent_team_setup_service.md) | — |
| `AgentTeamSetupService._handoff` | type_reference | [agent_team_setup_service](../modules/agent_team_setup_service.md) | — |
| `AgentTeamSetupService._increment_ack_attempt` | type_reference | [agent_team_setup_service](../modules/agent_team_setup_service.md) | — |
| `AgentTeamSetupService._member_record` | type_reference | [agent_team_setup_service](../modules/agent_team_setup_service.md) | — |
| `AgentTeamSetupService._reconcile_bindings` | type_reference | [agent_team_setup_service](../modules/agent_team_setup_service.md) | — |
| `AgentTeamSetupService._refresh_handoffs` | type_reference | [agent_team_setup_service](../modules/agent_team_setup_service.md) | — |

> References: showing 12 of 18 logical references; 6 omitted by the 12-row generated summary limit.

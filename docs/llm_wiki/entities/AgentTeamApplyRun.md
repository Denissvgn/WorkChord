# AgentTeamApplyRun

**Location:** `backend/app/models/agent.py:555`
**Kind:** Class
**Bases:** `Base`
**Module:** [models_agent](../modules/models_agent.md)

## Description

Replay-safe setup command receipt with a resumable action plan.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `Mapped[int]` | `mapped_column(Integer, primary_key=True, autoincrement=True)` | — |
| `apply_id` | `Mapped[str]` | `mapped_column(String(32), unique=True, nullable=False)` | — |
| `topology_id` | `Mapped[Optional[int]]` | `mapped_column(Integer, ForeignKey('agent_team_topologies.id', ondelete='SET NULL'), nullable=True)` | — |
| `topology_key` | `Mapped[str]` | `mapped_column(String(100), nullable=False)` | — |
| `principal_key` | `Mapped[str]` | `mapped_column(String(160), nullable=False)` | — |
| `principal_actor_id` | `Mapped[Optional[int]]` | `mapped_column(Integer, ForeignKey('agent_actors.id', ondelete='SET NULL'), nullable=True)` | — |
| `idempotency_key` | `Mapped[str]` | `mapped_column(String(255), nullable=False)` | — |
| `request_digest` | `Mapped[str]` | `mapped_column(String(64), nullable=False)` | — |
| `manifest_digest` | `Mapped[str]` | `mapped_column(String(64), nullable=False)` | — |
| `plan_digest` | `Mapped[str]` | `mapped_column(String(64), nullable=False)` | — |
| `expected_topology_revision` | `Mapped[int]` | `mapped_column(Integer, nullable=False)` | — |
| `resulting_topology_revision` | `Mapped[int]` | `mapped_column(Integer, default=0, nullable=False)` | — |
| `approved_action_ids` | `Mapped[str]` | `mapped_column(Text, nullable=False)` | — |
| `confirmed_action_ids` | `Mapped[str]` | `mapped_column(Text, nullable=False)` | — |
| `plan_payload` | `Mapped[str]` | `mapped_column(Text, nullable=False)` | — |
| `rationale` | `Mapped[str]` | `mapped_column(String(2000), nullable=False)` | — |
| `correlation_id` | `Mapped[str]` | `mapped_column(String(255), nullable=False)` | — |
| `status` | `Mapped[str]` | `mapped_column(String(30), default='running', nullable=False)` | — |
| `blocker_codes` | `Mapped[str]` | `mapped_column(Text, default='[]', nullable=False)` | — |
| `response_payload` | `Mapped[Optional[str]]` | `mapped_column(Text, nullable=True)` | — |
| `created_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), default=utc_now, nullable=False)` | — |
| `updated_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), default=utc_now, onupdate=utc_now, nullable=False)` | — |
| `topology` | `Mapped[Optional['AgentTeamTopology']]` | `relationship('AgentTeamTopology', back_populates='apply_runs')` | — |
| `principal_actor` | `Mapped[Optional['AgentActor']]` | `relationship('AgentActor', foreign_keys=[principal_actor_id])` | — |
| `action_receipts` | `Mapped[list['AgentTeamActionReceipt']]` | `relationship('AgentTeamActionReceipt', back_populates='apply_run', passive_deletes=True, order_by='AgentTeamActionReceipt.id')` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentTeamApplyRun (backend/app/models/agent.py)"]
    n1["Base (backend/app/database.py)"]
    n2["backend/app/models/__init__.py"]
    n3["AgentTeamSetupService._apply_create_or_update (backend/app/services/agent_team_setup_service.py)"]
    n4["AgentTeamSetupService._apply_disable (backend/app/services/agent_team_setup_service.py)"]
    n5["AgentTeamSetupService._apply_identity_replacement (backend/app/services/agent_team_setup_service.py)"]
    n6["AgentTeamSetupService._apply_replace_recovery (backend/app/services/agent_team_setup_service.py)"]
    n7["AgentTeamSetupService._ensure_topology_for_apply (backend/app/services/agent_team_setup_service.py)"]
    n8["AgentTeamSetupService._execute_action (backend/app/services/agent_team_setup_service.py)"]
    n9["AgentTeamSetupService._find_apply_run (backend/app/services/agent_team_setup_service.py)"]
    n10["AgentTeamSetupService._record_action_receipt (backend/app/services/agent_team_setup_service.py)"]
    n11["AgentTeamSetupService._replay_apply (backend/app/services/agent_team_setup_service.py)"]
    n12["AgentTeamSetupService.apply (backend/app/services/agent_team_setup_service.py)"]
    n13["backend/tests/test_agent_team_setup_qualification.py"]
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
    n13 --> n0
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
    click n13 "../modules/test_agent_team_setup_qualification.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [models_agent](../modules/models_agent.md) | 0 | `action_receipts`, `apply_id`, `approved_action_ids`, `blocker_codes`, `confirmed_action_ids`, `correlation_id`, `created_at`, `expected_topology_revision`, `id`, `idempotency_key`, `manifest_digest`, `plan_digest` |

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
| `AgentTeamSetupService._ensure_topology_for_apply` | type_reference | [agent_team_setup_service](../modules/agent_team_setup_service.md) | — |
| `AgentTeamSetupService._execute_action` | type_reference | [agent_team_setup_service](../modules/agent_team_setup_service.md) | — |
| `AgentTeamSetupService._find_apply_run` | type_reference | [agent_team_setup_service](../modules/agent_team_setup_service.md) | — |
| `AgentTeamSetupService._record_action_receipt` | type_reference | [agent_team_setup_service](../modules/agent_team_setup_service.md) | — |
| `AgentTeamSetupService._replay_apply` | type_reference | [agent_team_setup_service](../modules/agent_team_setup_service.md) | — |
| `AgentTeamSetupService.apply` | call | [agent_team_setup_service](../modules/agent_team_setup_service.md) | 1 |
| `test_agent_team_setup_qualification` | import | [test_agent_team_setup_qualification](../modules/test_agent_team_setup_qualification.md) | — |

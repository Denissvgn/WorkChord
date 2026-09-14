# AgentIdempotencyRecord

**Location:** `backend/app/models/agent.py:955`
**Kind:** Class
**Bases:** `Base`
**Module:** [models_agent](../modules/models_agent.md)

## Description

Replay-safe record for agent and PM mutations.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `Mapped[int]` | `mapped_column(Integer, primary_key=True, autoincrement=True)` | — |
| `actor_id` | `Mapped[int]` | `mapped_column(Integer, ForeignKey('agent_actors.id', ondelete='CASCADE'), nullable=False, index=True)` | — |
| `operation` | `Mapped[str]` | `mapped_column(String(100), nullable=False)` | — |
| `target_type` | `Mapped[str]` | `mapped_column(String(50), nullable=False)` | — |
| `target_id` | `Mapped[int]` | `mapped_column(Integer, nullable=False)` | — |
| `idempotency_key` | `Mapped[str]` | `mapped_column(String(255), nullable=False)` | — |
| `request_hash` | `Mapped[str]` | `mapped_column(String(64), nullable=False)` | — |
| `response_payload` | `Mapped[str]` | `mapped_column(Text, default='{}', nullable=False)` | — |
| `created_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), default=utc_now, nullable=False, index=True)` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentIdempotencyRecord (backend/app/models/agent.py)"]
    n1["Base (backend/app/database.py)"]
    n2["_stage_triage_command_receipt (backend/app/mcp_agent_tools.py)"]
    n3["backend/app/models/__init__.py"]
    n4["AgentModelCatalogService._execute (backend/app/services/agent_model_catalog_service.py)"]
    n5["AgentPlanningService._execute (backend/app/services/agent_planning_service.py)"]
    n6["AgentRoutingService.create_assessment (backend/app/services/agent_routing_service.py)"]
    n7["AgentService._record_command_receipt (backend/app/services/agent_service.py)"]
    n8["AgentWorkService._record_idempotency (backend/app/services/agent_work_service.py)"]
    n9["_record_planning_command (backend/tests/database/test_postgresql_concurrency.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    click n0 "../modules/models_agent.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/models___init__.md"
    click n4 "../modules/agent_model_catalog_service.md"
    click n5 "../modules/agent_planning_service.md"
    click n6 "../modules/agent_routing_service.md"
    click n7 "../modules/agent_service.md"
    click n8 "../modules/agent_work_service.md"
    click n9 "../modules/test_postgresql_concurrency.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [models_agent](../modules/models_agent.md) | 0 | `actor_id`, `created_at`, `id`, `idempotency_key`, `operation`, `request_hash`, `response_payload`, `target_id`, `target_type` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Base` | [app_database](../modules/app_database.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `_stage_triage_command_receipt` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 1 |
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `AgentModelCatalogService._execute` | call | [agent_model_catalog_service](../modules/agent_model_catalog_service.md) | 1 |
| `AgentPlanningService._execute` | call | [agent_planning_service](../modules/agent_planning_service.md) | 1 |
| `AgentRoutingService.create_assessment` | call | [agent_routing_service](../modules/agent_routing_service.md) | 1 |
| `AgentService._record_command_receipt` | call | [agent_service](../modules/agent_service.md) | 1 |
| `AgentWorkService._record_idempotency` | call | [agent_work_service](../modules/agent_work_service.md) | 1 |
| `_record_planning_command` | call | [test_postgresql_concurrency](../modules/test_postgresql_concurrency.md) | 1 |

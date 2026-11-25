# MaintenanceWindowConflict

**Location:** `backend/app/services/maintenance_window_service.py:41`
**Kind:** Class
**Bases:** `AgentRoutingConflictError`
**Module:** [maintenance_window_service](../modules/maintenance_window_service.md)

## Description

A stable, structured maintenance refusal shared by REST and MCP.

## Attributes

*No annotated attributes found.*

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["MaintenanceWindowConflict (backend/app/services/maintenance_window_service.py)"]
    n1["AgentRoutingConflictError (backend/app/services/agent_routing_service.py)"]
    n2["backend/app/routers/maintenance_windows.py"]
    n3["MaintenanceWindowService._require_state (backend/app/services/maintenance_window_service.py)"]
    n4["MaintenanceWindowService.acknowledge (backend/app/services/maintenance_window_service.py)"]
    n5["MaintenanceWindowService.announce (backend/app/services/maintenance_window_service.py)"]
    n6["MaintenanceWindowService.begin (backend/app/services/maintenance_window_service.py)"]
    n7["MaintenanceWindowService.record_own_notice (backend/app/services/maintenance_window_service.py)"]
    n8["require_start_admission (backend/app/services/maintenance_window_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    click n0 "../modules/maintenance_window_service.md"
    click n1 "../modules/agent_routing_service.md"
    click n2 "../modules/maintenance_windows.md"
    click n3 "../modules/maintenance_window_service.md"
    click n4 "../modules/maintenance_window_service.md"
    click n5 "../modules/maintenance_window_service.md"
    click n6 "../modules/maintenance_window_service.md"
    click n7 "../modules/maintenance_window_service.md"
    click n8 "../modules/maintenance_window_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [maintenance_window_service](../modules/maintenance_window_service.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `AgentRoutingConflictError` | [agent_routing_service](../modules/agent_routing_service.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `maintenance_windows` | import | [maintenance_windows](../modules/maintenance_windows.md) | — |
| `MaintenanceWindowService._require_state` | call | [maintenance_window_service](../modules/maintenance_window_service.md) | 1 |
| `MaintenanceWindowService.acknowledge` | call | [maintenance_window_service](../modules/maintenance_window_service.md) | 2 |
| `MaintenanceWindowService.announce` | call | [maintenance_window_service](../modules/maintenance_window_service.md) | 2 |
| `MaintenanceWindowService.begin` | call | [maintenance_window_service](../modules/maintenance_window_service.md) | 1 |
| `MaintenanceWindowService.record_own_notice` | call | [maintenance_window_service](../modules/maintenance_window_service.md) | 1 |
| `require_start_admission` | call | [maintenance_window_service](../modules/maintenance_window_service.md) | 1 |

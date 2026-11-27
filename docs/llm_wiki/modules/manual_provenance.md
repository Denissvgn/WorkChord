# manual_provenance Module

**Path:** `backend/app/schemas/manual_provenance.py`

## Description

Attributable execution provenance for resolved work that never ran through recorded runs.

## Imports

| Source | Symbols |
|--------|---------|
| `datetime` | `datetime` |
| `pydantic` | `BaseModel`, `ConfigDict`, `Field`, `field_validator`, `model_validator` |
| `typing` | `Literal` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/mcp_agent_tools.py"]
    n1["backend/app/routers/agent_planning.py"]
    n2["backend/app/routers/task_domain.py"]
    n3["backend/app/schemas/manual_provenance.py"]
    n4["backend/app/services/agent_planning_service.py"]
    n5["backend/tests/test_manual_provenance_record.py"]
    n0 --> n3
    n0 --> n4
    n1 --> n0
    n1 --> n3
    n1 --> n4
    n2 --> n3
    n4 --> n3
    n5 --> n3
    click n0 "../modules/mcp_agent_tools.md"
    click n1 "../modules/routers_agent_planning.md"
    click n2 "../modules/routers_task_domain.md"
    click n3 "../modules/manual_provenance.md"
    click n4 "../modules/agent_planning_service.md"
    click n5 "../modules/test_manual_provenance_record.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [mcp_agent_tools](../modules/mcp_agent_tools.md) |
| Inbound | [routers_agent_planning](../modules/routers_agent_planning.md) |
| Inbound | [routers_task_domain](../modules/routers_task_domain.md) |
| Inbound | [agent_planning_service](../modules/agent_planning_service.md) |
| Inbound | [test_manual_provenance_record](../modules/test_manual_provenance_record.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [ManualProvenanceExecutor](../entities/manual_provenance_ManualProvenanceExecutor.md) | 9 | `BaseModel` | The human or agent that actually executed the work. |
| [ManualProvenanceWrite](../entities/manual_provenance_ManualProvenanceWrite.md) | 29 | `BaseModel` | Record who executed one resolved task and the exact repository candidate they delivered. |
| [ManualProvenanceExecutorRecord](../entities/ManualProvenanceExecutorRecord.md) | 80 | `BaseModel` | — |
| [ManualProvenanceResponse](../entities/ManualProvenanceResponse.md) | 90 | `BaseModel` | The recorded provenance as it appears on the task timeline. |

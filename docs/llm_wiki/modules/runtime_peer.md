# runtime_peer Module

**Path:** `backend/tests/support/runtime_peer.py`

## Description

This test-only peer reads a disposable database request from standard input and opens a fresh process, engine and command transaction for every operation. Worker, PM and verifier use separate scoped credentials. It exercises protocol state and idempotent receipts, with no provider runtime or pilot qualification claim.

Disposable protocol peer: each invocation uses a new process and connection.

## Imports

| Source | Symbols |
|--------|---------|
| `app.commands` | `command_transaction` |
| `app.schemas.agent` | `AgentRecoveryRequeue`, `AgentReviewVerdict`, `AgentTaskAssignmentCreate`, `AgentTaskAssignmentUpdate`, `AgentWorkBegin`, `AgentWorkRenew`, `AgentWorkSubmit`, `AgentWorkTerminal` |
| `app.services.agent_service` | `AgentService` |
| `app.services.agent_work_service` | `AgentWorkService` |
| `asyncio` | `asyncio` |
| `json` | `json` |
| `os` | `os` |
| `sqlalchemy` | `event` |
| `sqlalchemy.ext.asyncio` | `async_sessionmaker`, `create_async_engine` |
| `sys` | `sys` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/commands.py"]
    n1["backend/app/schemas/agent.py"]
    n2["backend/app/services/agent_service.py"]
    n3["backend/app/services/agent_work_service.py"]
    n4["backend/tests/support/runtime_peer.py"]
    n2 --> n0
    n2 --> n1
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n4 --> n0
    n4 --> n1
    n4 --> n2
    n4 --> n3
    click n0 "../modules/commands.md"
    click n1 "../modules/schemas_agent.md"
    click n2 "../modules/agent_service.md"
    click n3 "../modules/agent_work_service.md"
    click n4 "../modules/runtime_peer.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [commands](../modules/commands.md) |
| Outbound | [schemas_agent](../modules/schemas_agent.md) |
| Outbound | [agent_service](../modules/agent_service.md) |
| Outbound | [agent_work_service](../modules/agent_work_service.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `execute` | *(async)* `(packet)` | — | — |

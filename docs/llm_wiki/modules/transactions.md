# transactions Module

**Path:** `backend/tests/support/transactions.py`

## Description

Explicit persisted-state reads after rollback in multi-command scenarios.

## Imports

| Source | Symbols |
|--------|---------|
| `sqlalchemy` | `inspect` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/tests/support/transactions.py"]
    n1["backend/tests/test_agent_routing_service.py"]
    n2["backend/tests/test_agent_routing_wave6_qualification.py"]
    n3["backend/tests/test_agent_team_setup_qualification.py"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n3 --> n2
    click n0 "../modules/transactions.md"
    click n1 "../modules/test_agent_routing_service.md"
    click n2 "../modules/test_agent_routing_wave6_qualification.md"
    click n3 "../modules/test_agent_team_setup_qualification.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [test_agent_routing_service](../modules/test_agent_routing_service.md) |
| Inbound | [test_agent_routing_wave6_qualification](../modules/test_agent_routing_wave6_qualification.md) |
| Inbound | [test_agent_team_setup_qualification](../modules/test_agent_team_setup_qualification.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `reload_session_fixture` | *(async)* `(db)` | — | Reload retained fixture objects instead of triggering async lazy I/O in assertions. |

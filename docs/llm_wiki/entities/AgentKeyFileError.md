# AgentKeyFileError

**Location:** `backend/app/agent_key_file.py:14`
**Kind:** Class
**Bases:** `ValueError`
**Module:** [agent_key_file](../modules/agent_key_file.md)

## Description

Raised when a key file is missing, unsafe, or malformed.

Messages name the path and the problem only; they never include file content.

## Attributes

*No annotated attributes found.*

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentKeyFileError (backend/app/agent_key_file.py)"]
    n1["ValueError"]
    n2["read_agent_key_file (backend/app/agent_key_file.py)"]
    n3["backend/app/mcp_server.py"]
    n4["backend/tests/test_agent_key_delivery.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/agent_key_file.md"
    click n2 "../modules/agent_key_file.md"
    click n3 "../modules/mcp_server.md"
    click n4 "../modules/test_agent_key_delivery.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_key_file](../modules/agent_key_file.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `ValueError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `read_agent_key_file` | call | [agent_key_file](../modules/agent_key_file.md) | 6 |
| `mcp_server` | import | [mcp_server](../modules/mcp_server.md) | — |
| `test_agent_key_delivery` | import | [test_agent_key_delivery](../modules/test_agent_key_delivery.md) | — |

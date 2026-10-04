# mutation_versions Module

**Path:** `backend/app/mutation_versions.py`

## Description

The server-controlled strict flag rejects missing optimistic inputs with an actionable resource/field error. Missing observations are deduplicated per command, resource and field. Preview transactions remain rollback-only. Ordinary operator credentials receive no bypass; dedicated offline migration/repair process roles retain their existing authorization and capacity rules.

Server-controlled version rollout with explicit offline repair separation.

## Imports

| Source | Symbols |
|--------|---------|
| `app.config` | `get_settings` |
| `app.runtime_telemetry` | `metrics` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/commands.py"]
    n1["backend/app/config.py"]
    n2["backend/app/main.py"]
    n3["backend/app/mcp_agent_tools.py"]
    n4["backend/app/mcp_server.py"]
    n5["backend/app/mutation_versions.py"]
    n6["backend/app/runtime_telemetry.py"]
    n7["backend/tests/test_mutation_versions.py"]
    n0 --> n5
    n0 --> n6
    n2 --> n0
    n2 --> n1
    n2 --> n4
    n2 --> n5
    n2 --> n6
    n3 --> n0
    n3 --> n1
    n3 --> n5
    n4 --> n0
    n4 --> n1
    n4 --> n3
    n4 --> n5
    n5 --> n1
    n5 --> n6
    n7 --> n0
    n7 --> n1
    n7 --> n2
    n7 --> n3
    n7 --> n4
    n7 --> n5
    click n0 "../modules/commands.md"
    click n1 "../modules/config.md"
    click n2 "../modules/app_main.md"
    click n3 "../modules/mcp_agent_tools.md"
    click n4 "../modules/mcp_server.md"
    click n5 "../modules/mutation_versions.md"
    click n6 "../modules/runtime_telemetry.md"
    click n7 "../modules/test_mutation_versions.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [commands](../modules/commands.md) |
| Inbound | [app_main](../modules/app_main.md) |
| Inbound | [mcp_agent_tools](../modules/mcp_agent_tools.md) |
| Inbound | [mcp_server](../modules/mcp_server.md) |
| Inbound | [test_mutation_versions](../modules/test_mutation_versions.md) |
| Outbound | [config](../modules/config.md) |
| Outbound | [runtime_telemetry](../modules/runtime_telemetry.md) |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [MissingMutationRevision](../entities/MissingMutationRevision.md) | 7 | `RuntimeError` | A supported command omitted its optimistic input revision. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `require_mutation_revision` | `(db, value, *, field: str, resource: str, resource_id: int)` | — | Keep missing inputs observable; ordinary operators receive no bypass. |

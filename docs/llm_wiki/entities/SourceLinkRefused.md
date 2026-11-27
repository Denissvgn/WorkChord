# SourceLinkRefused

**Location:** `backend/app/utils/source_link_policy.py:35`
**Kind:** Class
**Bases:** `ValueError`
**Module:** [source_link_policy](../modules/source_link_policy.md)

## Description

Raised when a source link breaks the policy; carries a stable, named error.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(reason: str) -> None` | — | — |
| `detail` | `() -> dict[str, str]` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["SourceLinkRefused (backend/app/utils/source_link_policy.py)"]
    n1["ValueError"]
    n2["backend/app/mcp_server.py"]
    n3["backend/app/routers/agent_planning.py"]
    n4["backend/app/routers/intake.py"]
    n5["backend/app/routers/triage.py"]
    n6["backend/app/schemas/task.py"]
    n7["normalize_source_link (backend/app/utils/source_link_policy.py)"]
    n8["backend/tests/test_intake_source_link.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    click n0 "../modules/source_link_policy.md"
    click n2 "../modules/mcp_server.md"
    click n3 "../modules/routers_agent_planning.md"
    click n4 "../modules/routers_intake.md"
    click n5 "../modules/routers_triage.md"
    click n6 "../modules/schemas_task.md"
    click n7 "../modules/source_link_policy.md"
    click n8 "../modules/test_intake_source_link.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [source_link_policy](../modules/source_link_policy.md) | 2 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `ValueError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `mcp_server` | import | [mcp_server](../modules/mcp_server.md) | — |
| `agent_planning` | import | [routers_agent_planning](../modules/routers_agent_planning.md) | — |
| `intake` | import | [routers_intake](../modules/routers_intake.md) | — |
| `triage` | import | [routers_triage](../modules/routers_triage.md) | — |
| `task` | import | [schemas_task](../modules/schemas_task.md) | — |
| `normalize_source_link` | call | [source_link_policy](../modules/source_link_policy.md) | 1 |
| `test_intake_source_link` | import | [test_intake_source_link](../modules/test_intake_source_link.md) | — |

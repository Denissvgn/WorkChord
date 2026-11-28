# DeliveryDependencyInput

**Location:** `backend/app/schemas/delivery_dependency.py:8`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_delivery_dependency](../modules/schemas_delivery_dependency.md)

## Description

Record a task or milestone prerequisite, optionally on a target branch.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `kind` | `Literal['task', 'milestone']` | `kind` | Yes | No | — | — | — | — |
| `target_id` | `int` | `target_id` | Yes | No | — | gt=0 | — | — |
| `expected_version` | `int` | `expected_version` | Yes | No | — | gt=0 | — | — |
| `target_branch` | `str \| None` | `target_branch` | No | Yes | `None` | max_length=255 | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["DeliveryDependencyInput (backend/app/schemas/delivery_dependency.py)"]
    n1["BaseModel"]
    n2["backend/app/mcp_agent_tools.py"]
    n3["add_delivery_dependency (backend/app/routers/delivery_dependencies.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/schemas_delivery_dependency.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/delivery_dependencies.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_delivery_dependency](../modules/schemas_delivery_dependency.md) | 0 | `expected_version`, `kind`, `target_branch`, `target_id` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `mcp_agent_tools` | import | [mcp_agent_tools](../modules/mcp_agent_tools.md) | — |
| `add_delivery_dependency` | type_reference | [delivery_dependencies](../modules/delivery_dependencies.md) | — |

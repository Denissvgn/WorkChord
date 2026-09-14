# generate_agent_team_contract Module

**Path:** `scripts/generate_agent_team_contract.py`

## Description

Generate the published JSON Schema for the portable agent-team master.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app.schemas.agent_team_setup` | `AgentTeamMaster` |
| `argparse` | `argparse` |
| `json` | `json` |
| `pathlib` | `Path` |
| `sys` | `sys` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/schemas/agent_team_setup.py"]
    n1["scripts/generate_agent_team_contract.py"]
    n1 --> n0
    click n0 "../modules/agent_team_setup.md"
    click n1 "../modules/generate_agent_team_contract.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [agent_team_setup](../modules/agent_team_setup.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 1 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `parse_args` | `() -> argparse.Namespace` | — | — |
| `rendered_schema` | `() -> bytes` | — | — |
| `main` | `() -> int` | — | — |

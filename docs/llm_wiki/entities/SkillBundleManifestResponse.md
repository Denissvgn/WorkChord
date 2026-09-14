# SkillBundleManifestResponse

**Location:** `backend/app/schemas/agent_skill_bundle.py:80`
**Kind:** Pydantic model
**Bases:** `StrictBundleModel`
**Module:** [agent_skill_bundle](../modules/agent_skill_bundle.md)

## Description

Exact-version manifest projected from the canonical catalog.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `schema_version` | `Literal['workchord-agent-skill-manifest/v1']` | `schema_version` | Yes | No | — | — | — | — |
| `entry_revision` | `str` | `entry_revision` | Yes | No | — | pattern=unknown (SOURCE_REVISION_PATTERN) | — | — |
| `skill` | `SkillBundleCatalogEntry` | `skill` | Yes | No | — | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["SkillBundleManifestResponse (backend/app/schemas/agent_skill_bundle.py)"]
    n1["StrictBundleModel (backend/app/schemas/agent_skill_bundle.py)"]
    n2["backend/app/mcp_agent_tools.py"]
    n3["get_agent_skill_bundle_manifest (backend/app/routers/agent_skill_bundles.py)"]
    n4["AgentSkillBundleService.manifest_payload (backend/app/services/agent_skill_bundle_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/agent_skill_bundle.md"
    click n1 "../modules/agent_skill_bundle.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/agent_skill_bundles.md"
    click n4 "../modules/agent_skill_bundle_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_skill_bundle](../modules/agent_skill_bundle.md) | 0 | `entry_revision`, `schema_version`, `skill` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `StrictBundleModel` | [agent_skill_bundle](../modules/agent_skill_bundle.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `mcp_agent_tools` | import | [mcp_agent_tools](../modules/mcp_agent_tools.md) | — |
| `get_agent_skill_bundle_manifest` | type_reference | [agent_skill_bundles](../modules/agent_skill_bundles.md) | — |
| `AgentSkillBundleService.manifest_payload` | call | [agent_skill_bundle_service](../modules/agent_skill_bundle_service.md) | 1 |

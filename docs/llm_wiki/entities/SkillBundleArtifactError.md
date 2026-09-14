# SkillBundleArtifactError

**Location:** `backend/app/services/agent_skill_bundle_service.py:44`
**Kind:** Class
**Bases:** `RuntimeError`
**Module:** [agent_skill_bundle_service](../modules/agent_skill_bundle_service.md)

## Description

Raised when deployed build artifacts fail their integrity contract.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["SkillBundleArtifactError (backend/app/services/agent_skill_bundle_service.py)"]
    n1["RuntimeError"]
    n2["backend/app/mcp_agent_tools.py"]
    n3["backend/app/routers/agent.py"]
    n4["backend/app/routers/agent_skill_bundles.py"]
    n5["AgentSkillBundleService._index_unique_records (backend/app/services/agent_skill_bundle_service.py)"]
    n6["AgentSkillBundleService._load_release (backend/app/services/agent_skill_bundle_service.py)"]
    n7["AgentSkillBundleService._read_artifact (backend/app/services/agent_skill_bundle_service.py)"]
    n8["AgentSkillBundleService._release_identity (backend/app/services/agent_skill_bundle_service.py)"]
    n9["AgentSkillBundleService._validate_artifact_name (backend/app/services/agent_skill_bundle_service.py)"]
    n10["AgentSkillBundleService._validate_release (backend/app/services/agent_skill_bundle_service.py)"]
    n11["AgentSkillBundleService._validate_skill_entry (backend/app/services/agent_skill_bundle_service.py)"]
    n12["AgentSkillBundleService.file_payload (backend/app/services/agent_skill_bundle_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    n10 --> n0
    n11 --> n0
    n12 --> n0
    click n0 "../modules/agent_skill_bundle_service.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/routers_agent.md"
    click n4 "../modules/agent_skill_bundles.md"
    click n5 "../modules/agent_skill_bundle_service.md"
    click n6 "../modules/agent_skill_bundle_service.md"
    click n7 "../modules/agent_skill_bundle_service.md"
    click n8 "../modules/agent_skill_bundle_service.md"
    click n9 "../modules/agent_skill_bundle_service.md"
    click n10 "../modules/agent_skill_bundle_service.md"
    click n11 "../modules/agent_skill_bundle_service.md"
    click n12 "../modules/agent_skill_bundle_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_skill_bundle_service](../modules/agent_skill_bundle_service.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `RuntimeError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `mcp_agent_tools` | import | [mcp_agent_tools](../modules/mcp_agent_tools.md) | — |
| `agent` | import | [routers_agent](../modules/routers_agent.md) | — |
| `agent_skill_bundles` | import | [agent_skill_bundles](../modules/agent_skill_bundles.md) | — |
| `AgentSkillBundleService._index_unique_records` | call | [agent_skill_bundle_service](../modules/agent_skill_bundle_service.md) | 1 |
| `AgentSkillBundleService._load_release` | call | [agent_skill_bundle_service](../modules/agent_skill_bundle_service.md) | 1 |
| `AgentSkillBundleService._read_artifact` | call | [agent_skill_bundle_service](../modules/agent_skill_bundle_service.md) | 7 |
| `AgentSkillBundleService._release_identity` | call | [agent_skill_bundle_service](../modules/agent_skill_bundle_service.md) | 6 |
| `AgentSkillBundleService._validate_artifact_name` | call | [agent_skill_bundle_service](../modules/agent_skill_bundle_service.md) | 1 |
| `AgentSkillBundleService._validate_release` | call | [agent_skill_bundle_service](../modules/agent_skill_bundle_service.md) | 16 |
| `AgentSkillBundleService._validate_skill_entry` | call | [agent_skill_bundle_service](../modules/agent_skill_bundle_service.md) | 11 |
| `AgentSkillBundleService.file_payload` | call | [agent_skill_bundle_service](../modules/agent_skill_bundle_service.md) | 5 |

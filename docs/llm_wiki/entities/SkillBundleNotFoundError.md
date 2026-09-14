# SkillBundleNotFoundError

**Location:** `backend/app/services/agent_skill_bundle_service.py:40`
**Kind:** Class
**Bases:** `LookupError`
**Module:** [agent_skill_bundle_service](../modules/agent_skill_bundle_service.md)

## Description

Raised when a requested exact skill, version, format, or file is absent.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["SkillBundleNotFoundError (backend/app/services/agent_skill_bundle_service.py)"]
    n1["LookupError"]
    n2["backend/app/mcp_agent_tools.py"]
    n3["backend/app/routers/agent_skill_bundles.py"]
    n4["AgentSkillBundleService._find_archive (backend/app/services/agent_skill_bundle_service.py)"]
    n5["AgentSkillBundleService._find_skill (backend/app/services/agent_skill_bundle_service.py)"]
    n6["AgentSkillBundleService._validate_skill_file_path (backend/app/services/agent_skill_bundle_service.py)"]
    n7["AgentSkillBundleService.file_payload (backend/app/services/agent_skill_bundle_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    click n0 "../modules/agent_skill_bundle_service.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/agent_skill_bundles.md"
    click n4 "../modules/agent_skill_bundle_service.md"
    click n5 "../modules/agent_skill_bundle_service.md"
    click n6 "../modules/agent_skill_bundle_service.md"
    click n7 "../modules/agent_skill_bundle_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_skill_bundle_service](../modules/agent_skill_bundle_service.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `LookupError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `mcp_agent_tools` | import | [mcp_agent_tools](../modules/mcp_agent_tools.md) | — |
| `agent_skill_bundles` | import | [agent_skill_bundles](../modules/agent_skill_bundles.md) | — |
| `AgentSkillBundleService._find_archive` | call | [agent_skill_bundle_service](../modules/agent_skill_bundle_service.md) | 1 |
| `AgentSkillBundleService._find_skill` | call | [agent_skill_bundle_service](../modules/agent_skill_bundle_service.md) | 1 |
| `AgentSkillBundleService._validate_skill_file_path` | call | [agent_skill_bundle_service](../modules/agent_skill_bundle_service.md) | 1 |
| `AgentSkillBundleService.file_payload` | call | [agent_skill_bundle_service](../modules/agent_skill_bundle_service.md) | 1 |

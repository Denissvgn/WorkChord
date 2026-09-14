# StrictBundleModel

**Location:** `backend/app/schemas/agent_skill_bundle.py:13`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [agent_skill_bundle](../modules/agent_skill_bundle.md)

## Description

Reject undeclared build metadata instead of serving it accidentally.

## Model Configuration

| Setting | Value | Source |
|---------|-------|--------|
| `extra` | `'forbid'` | model_config |

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["StrictBundleModel (backend/app/schemas/agent_skill_bundle.py)"]
    n1["BaseModel"]
    n2["SkillBundleArchiveRecord (backend/app/schemas/agent_skill_bundle.py)"]
    n3["SkillBundleCatalogEntry (backend/app/schemas/agent_skill_bundle.py)"]
    n4["SkillBundleCatalogResponse (backend/app/schemas/agent_skill_bundle.py)"]
    n5["SkillBundleDiscoveryResponse (backend/app/schemas/agent_skill_bundle.py)"]
    n6["SkillBundleFileRecord (backend/app/schemas/agent_skill_bundle.py)"]
    n7["SkillBundleManifestResponse (backend/app/schemas/agent_skill_bundle.py)"]
    n8["SkillBundleReleaseArtifact (backend/app/schemas/agent_skill_bundle.py)"]
    n9["SkillBundleReleaseIndex (backend/app/schemas/agent_skill_bundle.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    click n0 "../modules/agent_skill_bundle.md"
    click n2 "../modules/agent_skill_bundle.md"
    click n3 "../modules/agent_skill_bundle.md"
    click n4 "../modules/agent_skill_bundle.md"
    click n5 "../modules/agent_skill_bundle.md"
    click n6 "../modules/agent_skill_bundle.md"
    click n7 "../modules/agent_skill_bundle.md"
    click n8 "../modules/agent_skill_bundle.md"
    click n9 "../modules/agent_skill_bundle.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_skill_bundle](../modules/agent_skill_bundle.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |
| Subclass | `SkillBundleArchiveRecord` | [agent_skill_bundle](../modules/agent_skill_bundle.md) |
| Subclass | `SkillBundleCatalogEntry` | [agent_skill_bundle](../modules/agent_skill_bundle.md) |
| Subclass | `SkillBundleCatalogResponse` | [agent_skill_bundle](../modules/agent_skill_bundle.md) |
| Subclass | `SkillBundleDiscoveryResponse` | [agent_skill_bundle](../modules/agent_skill_bundle.md) |
| Subclass | `SkillBundleFileRecord` | [agent_skill_bundle](../modules/agent_skill_bundle.md) |
| Subclass | `SkillBundleManifestResponse` | [agent_skill_bundle](../modules/agent_skill_bundle.md) |
| Subclass | `SkillBundleReleaseArtifact` | [agent_skill_bundle](../modules/agent_skill_bundle.md) |
| Subclass | `SkillBundleReleaseIndex` | [agent_skill_bundle](../modules/agent_skill_bundle.md) |

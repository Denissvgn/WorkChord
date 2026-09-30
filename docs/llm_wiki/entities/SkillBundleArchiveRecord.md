# SkillBundleArchiveRecord

**Location:** `backend/app/schemas/agent_skill_bundle.py:27`
**Kind:** Pydantic model
**Bases:** `StrictBundleModel`
**Module:** [agent_skill_bundle](../modules/agent_skill_bundle.md)

## Description

One exact downloadable archive representation of a role skill.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `format` | `Literal['zip', 'tar.gz']` | `format` | Yes | No | — | — | — | — |
| `path` | `str` | `path` | Yes | No | — | min_length=1 | — | — |
| `sha256` | `str` | `sha256` | Yes | No | — | pattern=unknown (SHA256_PATTERN) | — | — |
| `size` | `int` | `size` | Yes | No | — | ge=0 | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["SkillBundleArchiveRecord (backend/app/schemas/agent_skill_bundle.py)"]
    n1["StrictBundleModel (backend/app/schemas/agent_skill_bundle.py)"]
    n2["AgentSkillBundleService._find_archive (backend/app/services/agent_skill_bundle_service.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/agent_skill_bundle.md"
    click n1 "../modules/agent_skill_bundle.md"
    click n2 "../modules/agent_skill_bundle_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_skill_bundle](../modules/agent_skill_bundle.md) | 0 | `format`, `path`, `sha256`, `size` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `StrictBundleModel` | [agent_skill_bundle](../modules/agent_skill_bundle.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `AgentSkillBundleService._find_archive` | type_reference | [agent_skill_bundle_service](../modules/agent_skill_bundle_service.md) | — |

# SkillBundlePayload

**Location:** `backend/app/services/agent_skill_bundle_service.py:49`
**Kind:** Class
**Bases:** —
**Module:** [agent_skill_bundle_service](../modules/agent_skill_bundle_service.md)

**Decorators:** `@dataclass(frozen=True)`

## Description

Exact response bytes and their transport integrity metadata.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `content` | `bytes` | *required* | — |
| `media_type` | `str` | *required* | — |
| `etag` | `str` | *required* | — |
| `content_digest` | `str` | *required* | — |
| `cache_control` | `str` | *required* | — |
| `filename` | `str \| None` | `None` | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `from_bytes` | `(content: bytes, *, media_type: str, cache_control: str, filename: str \| None = None) -> 'SkillBundlePayload'` | `@classmethod` | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["SkillBundlePayload (backend/app/services/agent_skill_bundle_service.py)"]
    n1["_resolve_payload (backend/app/routers/agent_skill_bundles.py)"]
    n2["_response (backend/app/routers/agent_skill_bundles.py)"]
    n3["AgentSkillBundleService.archive_payload (backend/app/services/agent_skill_bundle_service.py)"]
    n4["AgentSkillBundleService.catalog_payload (backend/app/services/agent_skill_bundle_service.py)"]
    n5["AgentSkillBundleService.discovery_payload (backend/app/services/agent_skill_bundle_service.py)"]
    n6["AgentSkillBundleService.file_payload (backend/app/services/agent_skill_bundle_service.py)"]
    n7["AgentSkillBundleService.manifest_payload (backend/app/services/agent_skill_bundle_service.py)"]
    n8["SkillBundlePayload.from_bytes (backend/app/services/agent_skill_bundle_service.py)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    click n0 "../modules/agent_skill_bundle_service.md"
    click n1 "../modules/agent_skill_bundles.md"
    click n2 "../modules/agent_skill_bundles.md"
    click n3 "../modules/agent_skill_bundle_service.md"
    click n4 "../modules/agent_skill_bundle_service.md"
    click n5 "../modules/agent_skill_bundle_service.md"
    click n6 "../modules/agent_skill_bundle_service.md"
    click n7 "../modules/agent_skill_bundle_service.md"
    click n8 "../modules/agent_skill_bundle_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_skill_bundle_service](../modules/agent_skill_bundle_service.md) | 1 | `cache_control`, `content`, `content_digest`, `etag`, `filename`, `media_type` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `_resolve_payload` | type_reference | [agent_skill_bundles](../modules/agent_skill_bundles.md) | — |
| `_response` | type_reference | [agent_skill_bundles](../modules/agent_skill_bundles.md) | — |
| `AgentSkillBundleService.archive_payload` | type_reference | [agent_skill_bundle_service](../modules/agent_skill_bundle_service.md) | — |
| `AgentSkillBundleService.catalog_payload` | type_reference | [agent_skill_bundle_service](../modules/agent_skill_bundle_service.md) | — |
| `AgentSkillBundleService.discovery_payload` | type_reference | [agent_skill_bundle_service](../modules/agent_skill_bundle_service.md) | — |
| `AgentSkillBundleService.file_payload` | type_reference | [agent_skill_bundle_service](../modules/agent_skill_bundle_service.md) | — |
| `AgentSkillBundleService.manifest_payload` | type_reference | [agent_skill_bundle_service](../modules/agent_skill_bundle_service.md) | — |
| `SkillBundlePayload.from_bytes` | call | [agent_skill_bundle_service](../modules/agent_skill_bundle_service.md) | 1 |
| `SkillBundlePayload.from_bytes` | type_reference | [agent_skill_bundle_service](../modules/agent_skill_bundle_service.md) | — |

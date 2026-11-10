# agent_skill_bundle_service Module

**Path:** `backend/app/services/agent_skill_bundle_service.py`

## Description

Read-only delivery of deterministic agent role-skill build artifacts.

The typed `catalog()` accessor gives team setup a defensive copy of the same validated release used by delivery payloads. Both interfaces retain deployment path resolution, release integrity checks, cache invalidation and configured trust-pin enforcement; caller mutations cannot alter the shared cached catalog.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app.schemas.agent_skill_bundle` | `SkillBundleArchiveRecord`, `SkillBundleCatalogEntry`, `SkillBundleCatalogResponse`, `SkillBundleDiscoveryResponse`, `SkillBundleManifestResponse`, `SkillBundleReleaseIndex` |
| `base64` | `base64` |
| `collections` | `Counter` |
| `dataclasses` | `dataclass` |
| `hashlib` | `hashlib` |
| `io` | `BytesIO` |
| `json` | `json` |
| `logging` | `logging` |
| `os` | `os` |
| `pathlib` | `Path`, `PurePosixPath` |
| `pydantic` | `ValidationError` |
| `re` | `re` |
| `stat` | `stat` |
| `threading` | `threading` |
| `typing` | `Any`, `Literal` |
| `zipfile` | `zipfile` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/mcp_agent_tools.py"]
    n1["backend/app/routers/agent.py"]
    n2["backend/app/routers/agent_skill_bundles.py"]
    n3["backend/app/schemas/agent_skill_bundle.py"]
    n4["backend/app/services/agent_skill_bundle_service.py"]
    n5["backend/app/services/agent_team_setup_service.py"]
    n6["backend/tests/conftest.py"]
    n7["backend/tests/test_agent_routing_rollout.py"]
    n8["backend/tests/test_agent_team_catalog.py"]
    n0 --> n3
    n0 --> n4
    n0 --> n5
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n1 --> n5
    n2 --> n3
    n2 --> n4
    n4 --> n3
    n5 --> n3
    n5 --> n4
    n6 --> n4
    n7 --> n0
    n7 --> n1
    n7 --> n4
    n8 --> n3
    n8 --> n4
    n8 --> n5
    click n0 "../modules/mcp_agent_tools.md"
    click n1 "../modules/routers_agent.md"
    click n2 "../modules/agent_skill_bundles.md"
    click n3 "../modules/agent_skill_bundle.md"
    click n4 "../modules/agent_skill_bundle_service.md"
    click n5 "../modules/agent_team_setup_service.md"
    click n6 "../modules/conftest.md"
    click n7 "../modules/test_agent_routing_rollout.md"
    click n8 "../modules/test_agent_team_catalog.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [mcp_agent_tools](../modules/mcp_agent_tools.md) |
| Inbound | [routers_agent](../modules/routers_agent.md) |
| Inbound | [agent_skill_bundles](../modules/agent_skill_bundles.md) |
| Inbound | [agent_team_setup_service](../modules/agent_team_setup_service.md) |
| Inbound | [conftest](../modules/conftest.md) |
| Inbound | [test_agent_routing_rollout](../modules/test_agent_routing_rollout.md) |
| Inbound | [test_agent_team_catalog](../modules/test_agent_team_catalog.md) |
| Outbound | [agent_skill_bundle](../modules/agent_skill_bundle.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [SkillBundleNotFoundError](../entities/SkillBundleNotFoundError.md) | 40 | `LookupError` | Raised when a requested exact skill, version, format, or file is absent. |
| [SkillBundleArtifactError](../entities/SkillBundleArtifactError.md) | 44 | `RuntimeError` | Raised when deployed build artifacts fail their integrity contract. |
| [SkillBundlePayload](../entities/SkillBundlePayload.md) | 49 | — | Exact response bytes and their transport integrity metadata. |
| [_LoadedRelease](../entities/LoadedRelease.md) | 81 | — | — |
| [_ReleaseLimits](../entities/ReleaseLimits.md) | 89 | — | — |
| [_CachedRelease](../entities/CachedRelease.md) | 98 | — | — |
| [AgentSkillBundleService](../entities/AgentSkillBundleService.md) | 114 | — | Validate and serve only files emitted by the deterministic skill build. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `default_skill_bundle_artifact_root` | `() -> Path` | — | Resolve the deployed artifact directory without reading application data. |

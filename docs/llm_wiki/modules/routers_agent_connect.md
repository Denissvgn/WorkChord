# agent_connect Module

**Path:** `backend/app/routers/agent_connect.py`

## Description

Public, secret-free hint telling an agent how to connect and obtain a key.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app.config` | `get_settings` |
| `app.schemas.agent_connect` | `AgentConnectCredential`, `AgentConnectResponse`, `AgentConnectRole` |
| `app.schemas.agent_skill_bundle` | `SkillBundleCatalogResponse` |
| `app.services.agent_skill_bundle_service` | `AgentSkillBundleService`, `SkillBundleArtifactError`, `SkillBundleNotFoundError` |
| `fastapi` | `APIRouter`, `Depends` |
| `typing` | `Annotated` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/config.py"]
    n1["backend/app/main.py"]
    n2["backend/app/routers/agent_connect.py"]
    n3["backend/app/schemas/agent_connect.py"]
    n4["backend/app/schemas/agent_skill_bundle.py"]
    n5["backend/app/services/agent_skill_bundle_service.py"]
    n6["backend/tests/test_agent_key_delivery.py"]
    n1 --> n0
    n1 --> n2
    n2 --> n0
    n2 --> n3
    n2 --> n4
    n2 --> n5
    n5 --> n0
    n5 --> n4
    n6 --> n1
    n6 --> n2
    n6 --> n5
    click n0 "../modules/config.md"
    click n1 "../modules/app_main.md"
    click n2 "../modules/routers_agent_connect.md"
    click n3 "../modules/schemas_agent_connect.md"
    click n4 "../modules/agent_skill_bundle.md"
    click n5 "../modules/agent_skill_bundle_service.md"
    click n6 "../modules/test_agent_key_delivery.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [app_main](../modules/app_main.md) |
| Inbound | [test_agent_key_delivery](../modules/test_agent_key_delivery.md) |
| Outbound | [config](../modules/config.md) |
| Outbound | [schemas_agent_connect](../modules/schemas_agent_connect.md) |
| Outbound | [agent_skill_bundle](../modules/agent_skill_bundle.md) |
| Outbound | [agent_skill_bundle_service](../modules/agent_skill_bundle_service.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `get_agent_connect_bundle_service` | *(async)* `() -> AgentSkillBundleService` | — | Read role scopes from the same deployed catalog the skill routes serve. |
| `_roles` | `(service: AgentSkillBundleService) -> list[AgentConnectRole]` | — | — |
| `get_agent_connect_hint` | *(async)* `(service: Annotated[AgentSkillBundleService, Depends(get_agent_connect_bundle_service)]) -> AgentConnectResponse` | `@router.get('/.well-known/workchord/agent-connect.json', response_model=AgentConnectResponse)` | Tell an unauthenticated agent where to connect and what key it needs. |

# external_link Module

**Path:** `backend/app/schemas/external_link.py`

## Description

External link schemas.

## Imports

| Source | Symbols |
|--------|---------|
| `app.utils.url_policy` | `URLPolicyError`, `normalize_loopback_display_url`, `normalize_stored_display_url` |
| `datetime` | `datetime` |
| `enum` | `Enum` |
| `pydantic` | `BaseModel`, `ConfigDict`, `Field`, `ValidationInfo`, `field_validator` |
| `typing` | `Any`, `Optional` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/routers/tasks.py"]
    n1["backend/app/schemas/__init__.py"]
    n2["backend/app/schemas/external_link.py"]
    n3["backend/app/schemas/task.py"]
    n4["backend/app/services/external_link_service.py"]
    n5["backend/app/utils/url_policy.py"]
    n6["backend/tests/test_agdash_link_provider.py"]
    n7["backend/tests/test_server_features.py"]
    n0 --> n2
    n0 --> n3
    n0 --> n4
    n1 --> n2
    n1 --> n3
    n2 --> n5
    n3 --> n2
    n4 --> n2
    n6 --> n2
    n7 --> n2
    click n0 "../modules/tasks.md"
    click n1 "../modules/schemas___init__.md"
    click n2 "../modules/schemas_external_link.md"
    click n3 "../modules/schemas_task.md"
    click n4 "../modules/external_link_service.md"
    click n5 "../modules/url_policy.md"
    click n6 "../modules/test_agdash_link_provider.md"
    click n7 "../modules/test_server_features.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [tasks](../modules/tasks.md) |
| Inbound | [schemas___init__](../modules/schemas___init__.md) |
| Inbound | [schemas_task](../modules/schemas_task.md) |
| Inbound | [external_link_service](../modules/external_link_service.md) |
| Inbound | [test_agdash_link_provider](../modules/test_agdash_link_provider.md) |
| Inbound | [test_server_features](../modules/test_server_features.md) |
| Outbound | [url_policy](../modules/url_policy.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [ExternalLinkEntityType](../entities/schemas_external_link_ExternalLinkEntityType.md) | Enum | 31 | `str`, `Enum` | Supported internal entity types for external links. |
| [ExternalLinkProvider](../entities/schemas_external_link_ExternalLinkProvider.md) | Enum | 38 | `str`, `Enum` | Supported external link providers. |
| [ExternalLinkFields](../entities/ExternalLinkFields.md) | Pydantic model | 49 | `BaseModel` | Shared external link fields. |
| [ExternalLinkCreate](../entities/schemas_external_link_ExternalLinkCreate.md) | Pydantic model | 74 | `ExternalLinkFields` | Schema for creating a generic external link. |
| [TaskExternalLinkCreate](../entities/TaskExternalLinkCreate.md) | Pydantic model | 82 | `ExternalLinkFields` | Schema for creating an external link on a task. |
| [GitHubExternalLinkCreate](../entities/schemas_external_link_GitHubExternalLinkCreate.md) | Pydantic model | 87 | `BaseModel` | Schema for manually linking a GitHub artifact to a task. |
| [ExternalLinkUpdate](../entities/schemas_external_link_ExternalLinkUpdate.md) | Pydantic model | 102 | `BaseModel` | Schema for updating an external link. |
| [ExternalLinkResponse](../entities/ExternalLinkResponse.md) | Pydantic model | 130 | `BaseModel` | Schema for external link responses, including synthetic legacy links. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_provider_value` | `(provider) -> Optional[str]` | — | — |
| `normalize_link_url` | `(value: Optional[str], provider = None) -> Optional[str]` | — | Normalize a display link; an agdash session link may use a loopback host. |
| `_normalize_optional_url` | `(value: Optional[str]) -> Optional[str]` | — | — |

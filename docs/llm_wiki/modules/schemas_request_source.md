# request_source Module

**Path:** `backend/app/schemas/request_source.py`

## Description

Request source schemas.

## Imports

| Source | Symbols |
|--------|---------|
| `app.utils.url_policy` | `URLPolicyError`, `normalize_stored_display_url` |
| `datetime` | `datetime` |
| `enum` | `Enum` |
| `pydantic` | `BaseModel`, `ConfigDict`, `Field`, `field_validator`, `model_validator` |
| `typing` | `Optional` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/mcp_agent_tools.py"]
    n1["backend/app/routers/request_sources.py"]
    n2["backend/app/schemas/__init__.py"]
    n3["backend/app/schemas/agent.py"]
    n4["backend/app/schemas/request_source.py"]
    n5["backend/app/services/request_source_service.py"]
    n6["backend/app/utils/url_policy.py"]
    n0 --> n3
    n0 --> n4
    n0 --> n5
    n1 --> n4
    n1 --> n5
    n2 --> n4
    n3 --> n4
    n3 --> n6
    n4 --> n6
    n5 --> n4
    click n0 "../modules/mcp_agent_tools.md"
    click n1 "../modules/request_sources.md"
    click n2 "../modules/schemas___init__.md"
    click n3 "../modules/schemas_agent.md"
    click n4 "../modules/schemas_request_source.md"
    click n5 "../modules/request_source_service.md"
    click n6 "../modules/url_policy.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [mcp_agent_tools](../modules/mcp_agent_tools.md) |
| Inbound | [request_sources](../modules/request_sources.md) |
| Inbound | [schemas___init__](../modules/schemas___init__.md) |
| Inbound | [schemas_agent](../modules/schemas_agent.md) |
| Inbound | [request_source_service](../modules/request_source_service.md) |
| Outbound | [url_policy](../modules/url_policy.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [RequestSourceType](../entities/schemas_request_source_RequestSourceType.md) | Enum | 20 | `str`, `Enum` | Supported lightweight request intake source types. |
| [RequestSourceTargetType](../entities/schemas_request_source_RequestSourceTargetType.md) | Enum | 31 | `str`, `Enum` | Supported request-source link target types. |
| [RequestSourceCreate](../entities/schemas_request_source_RequestSourceCreate.md) | Pydantic model | 39 | `BaseModel` | Schema for creating a request source. |
| [RequestSourceUpdate](../entities/RequestSourceUpdate.md) | Pydantic model | 58 | `BaseModel` | Schema for updating a request source. |
| [RequestSourceResponse](../entities/RequestSourceResponse.md) | Pydantic model | 77 | `BaseModel` | Schema for request source responses. |
| [RequestSourceLinkCreate](../entities/schemas_request_source_RequestSourceLinkCreate.md) | Pydantic model | 93 | `BaseModel` | Schema for linking one request source to one target. |
| [RequestSourceLinkResponse](../entities/RequestSourceLinkResponse.md) | Pydantic model | 115 | `BaseModel` | Schema for request source link responses. |
| [RequestSourceLinkCreateRequest](../entities/RequestSourceLinkCreateRequest.md) | Pydantic model | 128 | `BaseModel` | API request for linking an existing or new request source to a target. |
| [RequestSourceLinkWithSourceResponse](../entities/RequestSourceLinkWithSourceResponse.md) | Pydantic model | 148 | `RequestSourceLinkResponse` | Request-source link response with embedded source details. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_normalize_optional_url` | `(value: Optional[str]) -> Optional[str]` | — | — |

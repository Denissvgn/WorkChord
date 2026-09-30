# ExternalLinkFields

**Location:** `backend/app/schemas/external_link.py:36`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_external_link](../modules/schemas_external_link.md)

## Description

Shared external link fields.

## Validators

| Method | Scope | Fields | Mode | Options |
|--------|-------|--------|------|---------|
| `validate_url` | field | url | after | — |
| `validate_metadata_json` | field | metadata_json | before | — |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `provider` | `ExternalLinkProvider` | `provider` | Yes | No | — | — | — | — |
| `external_key` | `Optional[str]` | `external_key` | No | Yes | `None` | max_length=255 | — | — |
| `url` | `Optional[str]` | `url` | No | Yes | `None` | max_length=1000 | — | — |
| `title` | `Optional[str]` | `title` | No | Yes | `None` | max_length=500 | — | — |
| `status` | `Optional[str]` | `status` | No | Yes | `None` | max_length=100 | — | — |
| `metadata_json` | `dict[str, Any]` | `metadata_json` | No | No | factory: `dict` | — | — | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `validate_url` | `(value: Optional[str]) -> Optional[str]` | `@field_validator('url')`, `@classmethod` | — |
| `validate_metadata_json` | `(value)` | `@field_validator('metadata_json', mode='before')`, `@classmethod` | Require metadata_json to be a JSON object. |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ExternalLinkFields (backend/app/schemas/external_link.py)"]
    n1["BaseModel"]
    n2["ExternalLinkCreate (backend/app/schemas/external_link.py)"]
    n3["TaskExternalLinkCreate (backend/app/schemas/external_link.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/schemas_external_link.md"
    click n2 "../modules/schemas_external_link.md"
    click n3 "../modules/schemas_external_link.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_external_link](../modules/schemas_external_link.md) | 2 | `external_key`, `metadata_json`, `provider`, `status`, `title`, `url` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |
| Subclass | `ExternalLinkCreate` | [schemas_external_link](../modules/schemas_external_link.md) |
| Subclass | `TaskExternalLinkCreate` | [schemas_external_link](../modules/schemas_external_link.md) |

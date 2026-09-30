# TestEmailRequest

**Location:** `backend/app/schemas/email_settings.py:32`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_email_settings](../modules/schemas_email_settings.md)

## Description

Schema for test email request.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `recipient` | `EmailStr` | `recipient` | Yes | No | — | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TestEmailRequest (backend/app/schemas/email_settings.py)"]
    n1["BaseModel"]
    n2["test_email_settings (backend/app/routers/email_settings.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/schemas_email_settings.md"
    click n2 "../modules/routers_email_settings.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_email_settings](../modules/schemas_email_settings.md) | 0 | `recipient` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `test_email_settings` | type_reference | [routers_email_settings](../modules/routers_email_settings.md) | — |

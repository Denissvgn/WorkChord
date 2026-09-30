# WebIntakeConfigurationError

**Location:** `backend/app/services/web_intake_service.py:17`
**Kind:** Class
**Bases:** `RuntimeError`
**Module:** [web_intake_service](../modules/web_intake_service.md)

## Description

Raised when the intake endpoint is not configured.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["WebIntakeConfigurationError (backend/app/services/web_intake_service.py)"]
    n1["RuntimeError"]
    n2["backend/app/routers/intake.py"]
    n3["WebIntakeService.verify_authorization (backend/app/services/web_intake_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/web_intake_service.md"
    click n2 "../modules/routers_intake.md"
    click n3 "../modules/web_intake_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [web_intake_service](../modules/web_intake_service.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `RuntimeError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `intake` | import | [routers_intake](../modules/routers_intake.md) | — |
| `WebIntakeService.verify_authorization` | call | [web_intake_service](../modules/web_intake_service.md) | 1 |

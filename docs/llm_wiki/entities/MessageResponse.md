# MessageResponse

**Location:** `backend/app/schemas/common.py:18`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_common](../modules/schemas_common.md)

## Description

Simple message response.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `message` | `str` | `message` | Yes | No | — | — | — | — |
| `success` | `bool` | `success` | No | No | `True` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["MessageResponse (backend/app/schemas/common.py)"]
    n1["BaseModel"]
    n2["backend/app/routers/agent.py"]
    n3["delete_calendar (backend/app/routers/calendars.py)"]
    n4["_process_import (backend/app/routers/export.py)"]
    n5["delete_github_status_automation_rule (backend/app/routers/github.py)"]
    n6["delete_iteration (backend/app/routers/iterations.py)"]
    n7["delete_outbound_webhook_target (backend/app/routers/outbound_webhooks.py)"]
    n8["revoke_plan_share (backend/app/routers/plan_shares.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    click n0 "../modules/schemas_common.md"
    click n2 "../modules/routers_agent.md"
    click n3 "../modules/calendars.md"
    click n4 "../modules/export.md"
    click n5 "../modules/routers_github.md"
    click n6 "../modules/iterations.md"
    click n7 "../modules/outbound_webhooks.md"
    click n8 "../modules/plan_shares.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_common](../modules/schemas_common.md) | 0 | `message`, `success` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `agent` | import | [routers_agent](../modules/routers_agent.md) | — |
| `delete_calendar` | call | [calendars](../modules/calendars.md) | 1 |
| `delete_calendar` | type_reference | [calendars](../modules/calendars.md) | — |
| `_process_import` | call | [export](../modules/export.md) | 1 |
| `delete_github_status_automation_rule` | call | [routers_github](../modules/routers_github.md) | 1 |
| `delete_github_status_automation_rule` | type_reference | [routers_github](../modules/routers_github.md) | — |
| `delete_iteration` | call | [iterations](../modules/iterations.md) | 1 |
| `delete_iteration` | type_reference | [iterations](../modules/iterations.md) | — |
| `delete_outbound_webhook_target` | call | [outbound_webhooks](../modules/outbound_webhooks.md) | 1 |
| `delete_outbound_webhook_target` | type_reference | [outbound_webhooks](../modules/outbound_webhooks.md) | — |
| `revoke_plan_share` | call | [plan_shares](../modules/plan_shares.md) | 1 |
| `revoke_plan_share` | type_reference | [plan_shares](../modules/plan_shares.md) | — |

> References: showing 12 of 42 logical references; 30 omitted by the 12-row generated summary limit.

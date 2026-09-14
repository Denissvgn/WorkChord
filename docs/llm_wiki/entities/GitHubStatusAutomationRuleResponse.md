# GitHubStatusAutomationRuleResponse

**Location:** `backend/app/schemas/github.py:50`
**Kind:** Pydantic model
**Bases:** `GitHubStatusAutomationRuleBase`
**Module:** [schemas_github](../modules/schemas_github.md)

## Description

Response for one GitHub status automation rule.

## Model Configuration

| Setting | Value | Source |
|---------|-------|--------|
| `from_attributes` | `True` | config_class |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `id` | `int` | `id` | Yes | No | — | — | — | — |
| `created_at` | `datetime` | `created_at` | Yes | No | — | — | — | — |
| `updated_at` | `datetime` | `updated_at` | Yes | No | — | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["GitHubStatusAutomationRuleResponse (backend/app/schemas/github.py)"]
    n1["GitHubStatusAutomationRuleBase (backend/app/schemas/github.py)"]
    n2["create_github_status_automation_rule (backend/app/routers/github.py)"]
    n3["list_github_status_automation_rules (backend/app/routers/github.py)"]
    n4["update_github_status_automation_rule (backend/app/routers/github.py)"]
    n5["backend/app/schemas/__init__.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/schemas_github.md"
    click n1 "../modules/schemas_github.md"
    click n2 "../modules/routers_github.md"
    click n3 "../modules/routers_github.md"
    click n4 "../modules/routers_github.md"
    click n5 "../modules/schemas___init__.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_github](../modules/schemas_github.md) | 0 | `created_at`, `id`, `updated_at` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `GitHubStatusAutomationRuleBase` | [schemas_github](../modules/schemas_github.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `create_github_status_automation_rule` | type_reference | [routers_github](../modules/routers_github.md) | — |
| `list_github_status_automation_rules` | type_reference | [routers_github](../modules/routers_github.md) | — |
| `update_github_status_automation_rule` | type_reference | [routers_github](../modules/routers_github.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |

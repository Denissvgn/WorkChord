# GitHubStatusAutomationRuleCreate

**Location:** `backend/app/schemas/github.py:33`
**Kind:** Pydantic model
**Bases:** `GitHubStatusAutomationRuleBase`
**Module:** [schemas_github](../modules/schemas_github.md)

## Description

Create a GitHub status automation rule.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["GitHubStatusAutomationRuleCreate (backend/app/schemas/github.py)"]
    n1["GitHubStatusAutomationRuleBase (backend/app/schemas/github.py)"]
    n2["backend/app/routers/github.py"]
    n3["backend/app/schemas/__init__.py"]
    n4["GitHubStatusAutomationService.create_rule (backend/app/services/github_status_automation_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/schemas_github.md"
    click n1 "../modules/schemas_github.md"
    click n2 "../modules/routers_github.md"
    click n3 "../modules/schemas___init__.md"
    click n4 "../modules/github_status_automation_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_github](../modules/schemas_github.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `GitHubStatusAutomationRuleBase` | [schemas_github](../modules/schemas_github.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `github` | import | [routers_github](../modules/routers_github.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `GitHubStatusAutomationService.create_rule` | type_reference | [github_status_automation_service](../modules/github_status_automation_service.md) | — |

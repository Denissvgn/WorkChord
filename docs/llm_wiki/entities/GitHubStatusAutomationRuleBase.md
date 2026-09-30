# GitHubStatusAutomationRuleBase

**Location:** `backend/app/schemas/github.py:20`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_github](../modules/schemas_github.md)

## Description

Shared GitHub status automation rule fields.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `name` | `str` | `name` | Yes | No | — | max_length=255; min_length=1 | — | — |
| `description` | `Optional[str]` | `description` | No | Yes | `None` | — | — | — |
| `enabled` | `bool` | `enabled` | No | No | `False` | — | — | — |
| `github_event_type` | `GitHubAutomationEventType` | `github_event_type` | Yes | No | — | — | — | — |
| `from_status` | `Optional[GitHubAutomationFromStatus]` | `from_status` | No | Yes | `None` | — | — | — |
| `target_status` | `GitHubAutomationTargetStatus` | `target_status` | Yes | No | — | — | — | — |
| `reason_template` | `Optional[str]` | `reason_template` | No | Yes | `None` | — | — | — |
| `sort_order` | `int` | `sort_order` | No | No | `0` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["GitHubStatusAutomationRuleBase (backend/app/schemas/github.py)"]
    n1["BaseModel"]
    n2["GitHubStatusAutomationRuleCreate (backend/app/schemas/github.py)"]
    n3["GitHubStatusAutomationRuleResponse (backend/app/schemas/github.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/schemas_github.md"
    click n2 "../modules/schemas_github.md"
    click n3 "../modules/schemas_github.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_github](../modules/schemas_github.md) | 0 | `description`, `enabled`, `from_status`, `github_event_type`, `name`, `reason_template`, `sort_order`, `target_status` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |
| Subclass | `GitHubStatusAutomationRuleCreate` | [schemas_github](../modules/schemas_github.md) |
| Subclass | `GitHubStatusAutomationRuleResponse` | [schemas_github](../modules/schemas_github.md) |

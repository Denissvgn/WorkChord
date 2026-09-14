# TriageItemCreate

**Location:** `backend/app/schemas/triage.py:21`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_triage](../modules/schemas_triage.md)

## Description

Schema for creating a triage item.

## Model Configuration

| Setting | Value | Source |
|---------|-------|--------|
| `extra` | `'forbid'` | model_config |

## Validators

| Method | Scope | Fields | Mode | Options |
|--------|-------|--------|------|---------|
| `validate_duplicate_target` | model | — | after | — |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `title` | `str` | `title` | Yes | No | — | min_length=1; max_length=500 | — | — |
| `description` | `Optional[str]` | `description` | No | Yes | `None` | — | — | — |
| `source` | `Optional[str]` | `source` | No | Yes | `None` | max_length=100 | — | — |
| `source_url` | `Optional[str]` | `source_url` | No | Yes | `None` | max_length=1000 | — | — |
| `external_key` | `Optional[str]` | `external_key` | No | Yes | `None` | max_length=255 | — | — |
| `status` | `TriageItemStatus` | `status` | No | No | `TriageItemStatus.NEW` | — | — | — |
| `priority_hint` | `Optional[int]` | `priority_hint` | No | Yes | `None` | ge=1; le=10 | — | — |
| `assignee_hint` | `Optional[str]` | `assignee_hint` | No | Yes | `None` | max_length=255 | — | — |
| `project_hint_id` | `Optional[int]` | `project_hint_id` | No | Yes | `None` | — | — | — |
| `iteration_hint_id` | `Optional[int]` | `iteration_hint_id` | No | Yes | `None` | — | — | — |
| `labels` | `list[str]` | `labels` | No | No | factory: `list` | — | — | — |
| `metadata_json` | `dict[str, Any]` | `metadata_json` | No | No | factory: `dict` | — | — | — |
| `snoozed_until` | `Optional[datetime]` | `snoozed_until` | No | Yes | `None` | — | — | — |
| `duplicate_of_id` | `Optional[int]` | `duplicate_of_id` | No | Yes | `None` | — | — | — |
| `duplicate_task_id` | `Optional[int]` | `duplicate_task_id` | No | Yes | `None` | — | — | — |
| `converted_task_id` | `Optional[int]` | `converted_task_id` | No | Yes | `None` | — | — | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `validate_duplicate_target` | `()` | `@model_validator(mode='after')` | Reject ambiguous duplicate targets. |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TriageItemCreate (backend/app/schemas/triage.py)"]
    n1["BaseModel"]
    n2["create_triage_item (backend/app/mcp_agent_tools.py)"]
    n3["create_planning_triage_item (backend/app/routers/agent_planning.py)"]
    n4["create_triage_item (backend/app/routers/triage.py)"]
    n5["backend/app/schemas/__init__.py"]
    n6["AgentWorkService.report_discovery (backend/app/services/agent_work_service.py)"]
    n7["GitHubWebhookService._create_or_get_triage_item (backend/app/services/github_webhook_service.py)"]
    n8["TriageService.create (backend/app/services/triage_service.py)"]
    n9["WebIntakeService.create_triage_item (backend/app/services/web_intake_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    click n0 "../modules/schemas_triage.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/routers_agent_planning.md"
    click n4 "../modules/routers_triage.md"
    click n5 "../modules/schemas___init__.md"
    click n6 "../modules/agent_work_service.md"
    click n7 "../modules/github_webhook_service.md"
    click n8 "../modules/triage_service.md"
    click n9 "../modules/web_intake_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_triage](../modules/schemas_triage.md) | 1 | `assignee_hint`, `converted_task_id`, `description`, `duplicate_of_id`, `duplicate_task_id`, `external_key`, `iteration_hint_id`, `labels`, `metadata_json`, `priority_hint`, `project_hint_id`, `snoozed_until` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `create_triage_item` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 1 |
| `create_planning_triage_item` | type_reference | [routers_agent_planning](../modules/routers_agent_planning.md) | — |
| `create_triage_item` | type_reference | [routers_triage](../modules/routers_triage.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `AgentWorkService.report_discovery` | call | [agent_work_service](../modules/agent_work_service.md) | 1 |
| `GitHubWebhookService._create_or_get_triage_item` | call | [github_webhook_service](../modules/github_webhook_service.md) | 1 |
| `TriageService.create` | type_reference | [triage_service](../modules/triage_service.md) | — |
| `WebIntakeService.create_triage_item` | call | [web_intake_service](../modules/web_intake_service.md) | 1 |

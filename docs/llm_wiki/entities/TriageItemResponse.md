# TriageItemResponse

**Location:** `backend/app/schemas/triage.py:79`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_triage](../modules/schemas_triage.md)

## Description

Schema for triage item response.

## Model Configuration

| Setting | Value | Source |
|---------|-------|--------|
| `from_attributes` | `True` | config_class |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `id` | `int` | `id` | Yes | No | — | — | — | — |
| `title` | `str` | `title` | Yes | No | — | — | — | — |
| `description` | `Optional[str]` | `description` | No | Yes | `None` | — | — | — |
| `source` | `Optional[str]` | `source` | No | Yes | `None` | — | — | — |
| `source_url` | `Optional[str]` | `source_url` | No | Yes | `None` | — | — | — |
| `external_key` | `Optional[str]` | `external_key` | No | Yes | `None` | — | — | — |
| `status` | `str` | `status` | Yes | No | — | — | — | — |
| `priority_hint` | `Optional[int]` | `priority_hint` | No | Yes | `None` | — | — | — |
| `assignee_hint` | `Optional[str]` | `assignee_hint` | No | Yes | `None` | — | — | — |
| `project_hint_id` | `Optional[int]` | `project_hint_id` | No | Yes | `None` | — | — | — |
| `iteration_hint_id` | `Optional[int]` | `iteration_hint_id` | No | Yes | `None` | — | — | — |
| `labels` | `list[str]` | `labels` | No | No | factory: `list` | — | — | — |
| `metadata_json` | `dict[str, Any]` | `metadata_json` | No | No | factory: `dict` | — | — | — |
| `snoozed_until` | `Optional[datetime]` | `snoozed_until` | No | Yes | `None` | — | — | — |
| `duplicate_of_id` | `Optional[int]` | `duplicate_of_id` | No | Yes | `None` | — | — | — |
| `duplicate_task_id` | `Optional[int]` | `duplicate_task_id` | No | Yes | `None` | — | — | — |
| `converted_task_id` | `Optional[int]` | `converted_task_id` | No | Yes | `None` | — | — | — |
| `request_count` | `int` | `request_count` | No | No | `0` | — | — | — |
| `created_at` | `datetime` | `created_at` | Yes | No | — | — | — | — |
| `updated_at` | `datetime` | `updated_at` | Yes | No | — | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TriageItemResponse (backend/app/schemas/triage.py)"]
    n1["BaseModel"]
    n2["AgentDiscoveryTriageResponse (backend/app/schemas/agent.py)"]
    n3["backend/app/mcp_agent_tools.py"]
    n4["accept_planning_triage_item (backend/app/routers/agent_planning.py)"]
    n5["create_planning_triage_item (backend/app/routers/agent_planning.py)"]
    n6["decline_planning_triage_item (backend/app/routers/agent_planning.py)"]
    n7["mark_planning_triage_item_duplicate (backend/app/routers/agent_planning.py)"]
    n8["snooze_planning_triage_item (backend/app/routers/agent_planning.py)"]
    n9["update_planning_triage_item (backend/app/routers/agent_planning.py)"]
    n10["create_web_intake_item (backend/app/routers/intake.py)"]
    n11["accept_triage_item (backend/app/routers/triage.py)"]
    n12["create_triage_item (backend/app/routers/triage.py)"]
    n13["decline_triage_item (backend/app/routers/triage.py)"]
    n14["get_triage_item (backend/app/routers/triage.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    n10 --> n0
    n11 --> n0
    n12 --> n0
    n13 --> n0
    n14 --> n0
    click n0 "../modules/schemas_triage.md"
    click n2 "../modules/schemas_agent.md"
    click n3 "../modules/mcp_agent_tools.md"
    click n4 "../modules/routers_agent_planning.md"
    click n5 "../modules/routers_agent_planning.md"
    click n6 "../modules/routers_agent_planning.md"
    click n7 "../modules/routers_agent_planning.md"
    click n8 "../modules/routers_agent_planning.md"
    click n9 "../modules/routers_agent_planning.md"
    click n10 "../modules/routers_intake.md"
    click n11 "../modules/routers_triage.md"
    click n12 "../modules/routers_triage.md"
    click n13 "../modules/routers_triage.md"
    click n14 "../modules/routers_triage.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_triage](../modules/schemas_triage.md) | 0 | `assignee_hint`, `converted_task_id`, `created_at`, `description`, `duplicate_of_id`, `duplicate_task_id`, `external_key`, `id`, `iteration_hint_id`, `labels`, `metadata_json`, `priority_hint` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |
| Subclass | `AgentDiscoveryTriageResponse` | [schemas_agent](../modules/schemas_agent.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `mcp_agent_tools` | import | [mcp_agent_tools](../modules/mcp_agent_tools.md) | — |
| `accept_planning_triage_item` | type_reference | [routers_agent_planning](../modules/routers_agent_planning.md) | — |
| `create_planning_triage_item` | type_reference | [routers_agent_planning](../modules/routers_agent_planning.md) | — |
| `decline_planning_triage_item` | type_reference | [routers_agent_planning](../modules/routers_agent_planning.md) | — |
| `mark_planning_triage_item_duplicate` | type_reference | [routers_agent_planning](../modules/routers_agent_planning.md) | — |
| `snooze_planning_triage_item` | type_reference | [routers_agent_planning](../modules/routers_agent_planning.md) | — |
| `update_planning_triage_item` | type_reference | [routers_agent_planning](../modules/routers_agent_planning.md) | — |
| `create_web_intake_item` | type_reference | [routers_intake](../modules/routers_intake.md) | — |
| `accept_triage_item` | type_reference | [routers_triage](../modules/routers_triage.md) | — |
| `create_triage_item` | type_reference | [routers_triage](../modules/routers_triage.md) | — |
| `decline_triage_item` | type_reference | [routers_triage](../modules/routers_triage.md) | — |
| `get_triage_item` | type_reference | [routers_triage](../modules/routers_triage.md) | — |

> References: showing 12 of 18 logical references; 6 omitted by the 12-row generated summary limit.

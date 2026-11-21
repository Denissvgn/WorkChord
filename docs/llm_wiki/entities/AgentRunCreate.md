# AgentRunCreate

**Location:** `backend/app/schemas/agent.py:368`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_agent](../modules/schemas_agent.md)

## Description

Request to start an agent run.

## Validators

| Method | Scope | Fields | Mode | Options |
|--------|-------|--------|------|---------|
| `validate_artifact_links` | field | artifact_links | after | — |
| `validate_urls` | field | commit_url, pr_url | after | — |
| `validate_metadata_size` | field | metadata | after | — |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `task_id` | `Optional[int]` | `task_id` | No | Yes | `None` | — | — | — |
| `assignment_id` | `Optional[int]` | `assignment_id` | No | Yes | `None` | — | — | — |
| `claim_generation` | `Optional[int]` | `claim_generation` | No | Yes | `None` | ge=1 | — | — |
| `trace_id` | `Optional[str]` | `trace_id` | No | Yes | `None` | max_length=255 | — | — |
| `model` | `Optional[str]` | `model` | No | Yes | `None` | max_length=255 | — | — |
| `tool_name` | `Optional[str]` | `tool_name` | No | Yes | `None` | max_length=255 | — | — |
| `metadata` | `dict[str, Any]` | `metadata` | No | No | factory: `dict` | max_length=unknown (MAX_AGENT_JSON_FIELDS) | — | — |
| `artifact_links` | `list[str]` | `artifact_links` | No | No | factory: `list` | max_length=unknown (MAX_AGENT_ARTIFACT_LINKS) | — | — |
| `commit_url` | `Optional[str]` | `commit_url` | No | Yes | `None` | max_length=1000 | — | — |
| `pr_url` | `Optional[str]` | `pr_url` | No | Yes | `None` | max_length=1000 | — | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `validate_artifact_links` | `(value: list[str]) -> list[str]` | `@field_validator('artifact_links')`, `@classmethod` | — |
| `validate_urls` | `(value: Optional[str]) -> Optional[str]` | `@field_validator('commit_url', 'pr_url')`, `@classmethod` | — |
| `validate_metadata_size` | `(value: dict[str, Any]) -> dict[str, Any]` | `@field_validator('metadata')`, `@classmethod` | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentRunCreate (backend/app/schemas/agent.py)"]
    n1["BaseModel"]
    n2["start_agent_run (backend/app/mcp_agent_tools.py)"]
    n3["start_agent_run (backend/app/routers/agent.py)"]
    n4["AgentService.start_run (backend/app/services/agent_service.py)"]
    n5["test_legacy_run_start_classifies_reported_model_evidence (backend/tests/test_agent_run_trust_compatibility.py)"]
    n6["begins (backend/tests/test_harness_session_metadata.py)"]
    n7["test_a_started_run_keeps_its_declared_harness_session (backend/tests/test_person_run_reads.py)"]
    n8["test_the_declared_harness_is_read_from_validated_metadata (backend/tests/test_person_run_reads.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    click n0 "../modules/schemas_agent.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/routers_agent.md"
    click n4 "../modules/agent_service.md"
    click n5 "../modules/test_agent_run_trust_compatibility.md"
    click n6 "../modules/test_harness_session_metadata.md"
    click n7 "../modules/test_person_run_reads.md"
    click n8 "../modules/test_person_run_reads.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_agent](../modules/schemas_agent.md) | 3 | `artifact_links`, `assignment_id`, `claim_generation`, `commit_url`, `metadata`, `model`, `pr_url`, `task_id`, `tool_name`, `trace_id` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `start_agent_run` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 1 |
| `start_agent_run` | type_reference | [routers_agent](../modules/routers_agent.md) | — |
| `AgentService.start_run` | type_reference | [agent_service](../modules/agent_service.md) | — |
| `test_legacy_run_start_classifies_reported_model_evidence` | call | [test_agent_run_trust_compatibility](../modules/test_agent_run_trust_compatibility.md) | 1 |
| `begins` | call | [test_harness_session_metadata](../modules/test_harness_session_metadata.md) | 1 |
| `test_a_started_run_keeps_its_declared_harness_session` | call | [test_person_run_reads](../modules/test_person_run_reads.md) | 1 |
| `test_the_declared_harness_is_read_from_validated_metadata` | call | [test_person_run_reads](../modules/test_person_run_reads.md) | 1 |

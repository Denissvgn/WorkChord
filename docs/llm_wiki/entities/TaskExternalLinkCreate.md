# TaskExternalLinkCreate

**Location:** `backend/app/schemas/external_link.py:82`
**Kind:** Pydantic model
**Bases:** `ExternalLinkFields`
**Module:** [schemas_external_link](../modules/schemas_external_link.md)

## Description

Schema for creating an external link on a task.

## Model Configuration

| Setting | Value | Source |
|---------|-------|--------|
| `extra` | `'forbid'` | model_config |

## Attributes

*No annotated attributes found.*

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskExternalLinkCreate (backend/app/schemas/external_link.py)"]
    n1["ExternalLinkFields (backend/app/schemas/external_link.py)"]
    n2["backend/app/routers/tasks.py"]
    n3["backend/app/schemas/__init__.py"]
    n4["ExternalLinkService.create_task_github_link (backend/app/services/external_link_service.py)"]
    n5["ExternalLinkService.create_task_link (backend/app/services/external_link_service.py)"]
    n6["test_an_agdash_link_may_open_on_the_observing_machine (backend/tests/test_agdash_link_provider.py)"]
    n7["test_an_agdash_link_still_refuses_private_networks_credentials_and_other_schemes (backend/tests/test_agdash_link_provider.py)"]
    n8["test_other_providers_keep_refusing_loopback_links (backend/tests/test_agdash_link_provider.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    click n0 "../modules/schemas_external_link.md"
    click n1 "../modules/schemas_external_link.md"
    click n2 "../modules/tasks.md"
    click n3 "../modules/schemas___init__.md"
    click n4 "../modules/external_link_service.md"
    click n5 "../modules/external_link_service.md"
    click n6 "../modules/test_agdash_link_provider.md"
    click n7 "../modules/test_agdash_link_provider.md"
    click n8 "../modules/test_agdash_link_provider.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_external_link](../modules/schemas_external_link.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `ExternalLinkFields` | [schemas_external_link](../modules/schemas_external_link.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `tasks` | import | [tasks](../modules/tasks.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `ExternalLinkService.create_task_github_link` | call | [external_link_service](../modules/external_link_service.md) | 1 |
| `ExternalLinkService.create_task_link` | type_reference | [external_link_service](../modules/external_link_service.md) | — |
| `test_an_agdash_link_may_open_on_the_observing_machine` | call | [test_agdash_link_provider](../modules/test_agdash_link_provider.md) | 1 |
| `test_an_agdash_link_still_refuses_private_networks_credentials_and_other_schemes` | call | [test_agdash_link_provider](../modules/test_agdash_link_provider.md) | 1 |
| `test_other_providers_keep_refusing_loopback_links` | call | [test_agdash_link_provider](../modules/test_agdash_link_provider.md) | 1 |

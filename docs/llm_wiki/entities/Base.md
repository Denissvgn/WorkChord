# Base

**Location:** `backend/app/database.py:36`
**Kind:** Class
**Bases:** `DeclarativeBase`
**Module:** [app_database](../modules/app_database.md)

## Description

Base class for all models.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["Base (backend/app/database.py)"]
    n1["DeclarativeBase"]
    n2["AgentActor (backend/app/models/agent.py)"]
    n3["AgentIdempotencyRecord (backend/app/models/agent.py)"]
    n4["AgentModelBinding (backend/app/models/agent.py)"]
    n5["AgentModelCatalogEntry (backend/app/models/agent.py)"]
    n6["AgentRun (backend/app/models/agent.py)"]
    n7["AgentRunEvent (backend/app/models/agent.py)"]
    n8["AgentTaskAssignment (backend/app/models/agent.py)"]
    n9["AgentTeamActionReceipt (backend/app/models/agent.py)"]
    n10["AgentTeamApplyRun (backend/app/models/agent.py)"]
    n11["AgentTeamManagedObject (backend/app/models/agent.py)"]
    n12["AgentTeamTopology (backend/app/models/agent.py)"]
    n13["AgentTeamTopologyMember (backend/app/models/agent.py)"]
    n14["backend/app/database_migration/catalog.py"]
    n15["backend/app/migrations/env.py"]
    n16["backend/app/models/agent.py"]
    n17["backend/app/models/autonomy.py"]
    n18["backend/app/models/calendar.py"]
    n19["backend/app/models/database_migration.py"]
    n20["backend/app/models/external_link.py"]
    n21["backend/app/models/github.py"]
    n22["backend/app/models/iteration.py"]
    n23["backend/app/models/label.py"]
    n24["backend/app/models/outbound_webhook.py"]
    n25["backend/app/models/plan_share.py"]
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
    n15 --> n0
    n16 --> n0
    n17 --> n0
    n18 --> n0
    n19 --> n0
    n20 --> n0
    n21 --> n0
    n22 --> n0
    n23 --> n0
    n24 --> n0
    n25 --> n0
    click n0 "../modules/app_database.md"
    click n2 "../modules/models_agent.md"
    click n3 "../modules/models_agent.md"
    click n4 "../modules/models_agent.md"
    click n5 "../modules/models_agent.md"
    click n6 "../modules/models_agent.md"
    click n7 "../modules/models_agent.md"
    click n8 "../modules/models_agent.md"
    click n9 "../modules/models_agent.md"
    click n10 "../modules/models_agent.md"
    click n11 "../modules/models_agent.md"
    click n12 "../modules/models_agent.md"
    click n13 "../modules/models_agent.md"
    click n14 "../modules/catalog.md"
    click n15 "../modules/migrations_env.md"
    click n16 "../modules/models_agent.md"
    click n17 "../modules/models_autonomy.md"
    click n18 "../modules/models_calendar.md"
    click n19 "../modules/models_database_migration.md"
    click n20 "../modules/models_external_link.md"
    click n21 "../modules/models_github.md"
    click n22 "../modules/models_iteration.md"
    click n23 "../modules/models_label.md"
    click n24 "../modules/models_outbound_webhook.md"
    click n25 "../modules/models_plan_share.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [app_database](../modules/app_database.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `DeclarativeBase` | — |
| Subclass | `AgentActor` | [models_agent](../modules/models_agent.md) |
| Subclass | `AgentIdempotencyRecord` | [models_agent](../modules/models_agent.md) |
| Subclass | `AgentModelBinding` | [models_agent](../modules/models_agent.md) |
| Subclass | `AgentModelCatalogEntry` | [models_agent](../modules/models_agent.md) |
| Subclass | `AgentRun` | [models_agent](../modules/models_agent.md) |
| Subclass | `AgentRunEvent` | [models_agent](../modules/models_agent.md) |
| Subclass | `AgentTaskAssignment` | [models_agent](../modules/models_agent.md) |
| Subclass | `AgentTeamActionReceipt` | [models_agent](../modules/models_agent.md) |
| Subclass | `AgentTeamApplyRun` | [models_agent](../modules/models_agent.md) |
| Subclass | `AgentTeamManagedObject` | [models_agent](../modules/models_agent.md) |
| Subclass | `AgentTeamTopology` | [models_agent](../modules/models_agent.md) |
| Subclass | `AgentTeamTopologyMember` | [models_agent](../modules/models_agent.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `catalog` | import | [catalog](../modules/catalog.md) | — |
| `env` | import | [migrations_env](../modules/migrations_env.md) | — |
| `agent` | import | [models_agent](../modules/models_agent.md) | — |
| `autonomy` | import | [models_autonomy](../modules/models_autonomy.md) | — |
| `calendar` | import | [models_calendar](../modules/models_calendar.md) | — |
| `database_migration` | import | [models_database_migration](../modules/models_database_migration.md) | — |
| `external_link` | import | [models_external_link](../modules/models_external_link.md) | — |
| `github` | import | [models_github](../modules/models_github.md) | — |
| `iteration` | import | [models_iteration](../modules/models_iteration.md) | — |
| `label` | import | [models_label](../modules/models_label.md) | — |
| `outbound_webhook` | import | [models_outbound_webhook](../modules/models_outbound_webhook.md) | — |
| `plan_share` | import | [models_plan_share](../modules/models_plan_share.md) | — |

> References: showing 12 of 29 logical references; 17 omitted by the 12-row generated summary limit.

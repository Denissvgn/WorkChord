# UTCDateTime

**Location:** `backend/app/utils/time.py:28`
**Kind:** Class
**Bases:** `TypeDecorator[datetime]`
**Module:** [time](../modules/time.md)

## Description

Persist UTC datetimes and always return aware UTC values.

SQLite drops timezone offsets from its datetime representation, so values
are stored there as naive UTC and normalized on read. Dialects with native
timezone support receive aware UTC values and a timezone-aware column type.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `load_dialect_impl` | `(dialect: Dialect) -> Any` | — | — |
| `process_bind_param` | `(value: datetime \| None, dialect: Dialect) -> datetime \| None` | — | — |
| `process_result_value` | `(value: datetime \| None, _dialect: Dialect) -> datetime \| None` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["UTCDateTime (backend/app/utils/time.py)"]
    n1["TypeDecorator[datetime]"]
    n2["backend/app/models/agent.py"]
    n3["backend/app/models/autonomy.py"]
    n4["backend/app/models/database_migration.py"]
    n5["backend/app/models/delivery_observation.py"]
    n6["backend/app/models/discussion.py"]
    n7["backend/app/models/execution_usage.py"]
    n8["backend/app/models/external_link.py"]
    n9["backend/app/models/github.py"]
    n10["backend/app/models/identity.py"]
    n11["backend/app/models/label.py"]
    n12["backend/app/models/native_connection.py"]
    n13["backend/app/models/outbound_webhook.py"]
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
    click n0 "../modules/time.md"
    click n2 "../modules/models_agent.md"
    click n3 "../modules/models_autonomy.md"
    click n4 "../modules/models_database_migration.md"
    click n5 "../modules/delivery_observation.md"
    click n6 "../modules/models_discussion.md"
    click n7 "../modules/models_execution_usage.md"
    click n8 "../modules/models_external_link.md"
    click n9 "../modules/models_github.md"
    click n10 "../modules/models_identity.md"
    click n11 "../modules/models_label.md"
    click n12 "../modules/native_connection.md"
    click n13 "../modules/models_outbound_webhook.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [time](../modules/time.md) | 3 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `TypeDecorator[datetime]` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `agent` | import | [models_agent](../modules/models_agent.md) | — |
| `autonomy` | import | [models_autonomy](../modules/models_autonomy.md) | — |
| `database_migration` | import | [models_database_migration](../modules/models_database_migration.md) | — |
| `delivery_observation` | import | [delivery_observation](../modules/delivery_observation.md) | — |
| `discussion` | import | [models_discussion](../modules/models_discussion.md) | — |
| `execution_usage` | import | [models_execution_usage](../modules/models_execution_usage.md) | — |
| `external_link` | import | [models_external_link](../modules/models_external_link.md) | — |
| `github` | import | [models_github](../modules/models_github.md) | — |
| `identity` | import | [models_identity](../modules/models_identity.md) | — |
| `label` | import | [models_label](../modules/models_label.md) | — |
| `native_connection` | import | [native_connection](../modules/native_connection.md) | — |
| `outbound_webhook` | import | [models_outbound_webhook](../modules/models_outbound_webhook.md) | — |

> References: showing 12 of 27 logical references; 15 omitted by the 12-row generated summary limit.

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
    n2["upgrade (backend/app/migrations/versions/20260718_0032_add_database_migration_gate.py)"]
    n3["upgrade (backend/app/migrations/versions/20260719_0033_add_autonomy_control_plane.py)"]
    n4["upgrade (backend/app/migrations/versions/20260728_0035_add_agent_team_setup.py)"]
    n5["upgrade (backend/app/migrations/versions/20260802_0036_add_plan_shares.py)"]
    n6["backend/app/models/agent.py"]
    n7["backend/app/models/autonomy.py"]
    n8["backend/app/models/database_migration.py"]
    n9["backend/app/models/external_link.py"]
    n10["backend/app/models/github.py"]
    n11["backend/app/models/label.py"]
    n12["backend/app/models/outbound_webhook.py"]
    n13["backend/app/models/plan_share.py"]
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
    click n2 "../modules/20260718_0032_add_database_migration_gate.md"
    click n3 "../modules/20260719_0033_add_autonomy_control_plane.md"
    click n4 "../modules/20260728_0035_add_agent_team_setup.md"
    click n5 "../modules/20260802_0036_add_plan_shares.md"
    click n6 "../modules/models_agent.md"
    click n7 "../modules/models_autonomy.md"
    click n8 "../modules/models_database_migration.md"
    click n9 "../modules/models_external_link.md"
    click n10 "../modules/models_github.md"
    click n11 "../modules/models_label.md"
    click n12 "../modules/models_outbound_webhook.md"
    click n13 "../modules/models_plan_share.md"
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
| `upgrade` | call | [20260718_0032_add_database_migration_gate](../modules/20260718_0032_add_database_migration_gate.md) | 2 |
| `upgrade` | call | [20260719_0033_add_autonomy_control_plane](../modules/20260719_0033_add_autonomy_control_plane.md) | 16 |
| `upgrade` | call | [20260728_0035_add_agent_team_setup](../modules/20260728_0035_add_agent_team_setup.md) | 11 |
| `upgrade` | call | [20260802_0036_add_plan_shares](../modules/20260802_0036_add_plan_shares.md) | 2 |
| `agent` | import | [models_agent](../modules/models_agent.md) | — |
| `autonomy` | import | [models_autonomy](../modules/models_autonomy.md) | — |
| `database_migration` | import | [models_database_migration](../modules/models_database_migration.md) | — |
| `external_link` | import | [models_external_link](../modules/models_external_link.md) | — |
| `github` | import | [models_github](../modules/models_github.md) | — |
| `label` | import | [models_label](../modules/models_label.md) | — |
| `outbound_webhook` | import | [models_outbound_webhook](../modules/models_outbound_webhook.md) | — |
| `plan_share` | import | [models_plan_share](../modules/models_plan_share.md) | — |

> References: showing 12 of 23 logical references; 11 omitted by the 12-row generated summary limit.

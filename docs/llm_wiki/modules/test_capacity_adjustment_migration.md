# test_capacity_adjustment_migration Module

**Path:** `backend/tests/migrations/test_capacity_adjustment_migration.py`

## Description

Dated capacity adjustments migrate reversibly and keep existing capacity rows unchanged.

## Imports

| Source | Symbols |
|--------|---------|
| `alembic` | `command` |
| `app.models.calendar` | `Calendar` |
| `app.models.iteration` | `Iteration` |
| `app.models.team_member` | `TeamMember`, `TeamMemberCapacityAdjustment` |
| `app.services.upgrade_service` | `alembic_config` |
| `datetime` | `date`, `datetime`, `timezone` |
| `pytest` | `pytest` |
| `sqlalchemy` | `create_engine`, `event`, `inspect`, `select` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/models/calendar.py"]
    n1["backend/app/models/iteration.py"]
    n2["backend/app/models/team_member.py"]
    n3["backend/app/services/upgrade_service.py"]
    n4["backend/tests/migrations/test_capacity_adjustment_migration.py"]
    n0 --> n1
    n1 --> n0
    n1 --> n2
    n2 --> n1
    n4 --> n0
    n4 --> n1
    n4 --> n2
    n4 --> n3
    click n0 "../modules/models_calendar.md"
    click n1 "../modules/models_iteration.md"
    click n2 "../modules/team_member.md"
    click n3 "../modules/upgrade_service.md"
    click n4 "../modules/test_capacity_adjustment_migration.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [models_calendar](../modules/models_calendar.md) |
| Outbound | [models_iteration](../modules/models_iteration.md) |
| Outbound | [team_member](../modules/team_member.md) |
| Outbound | [upgrade_service](../modules/upgrade_service.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 3 | 1 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `test_adjustment_migration_preserves_rows_and_refuses_losing_active_adjustments` | `(dialect, request, tmp_path, configure_database)` | `@pytest.mark.parametrize('dialect', [pytest.param('sqlite', marks=pytest.mark.sqlite), pytest.param('postgresql', marks=[pytest.mark.postgresql, pytest.mark.integration, pytest.mark.allow_network])])` | — |

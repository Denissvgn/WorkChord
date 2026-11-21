# test_annual_calendar_migration Module

**Path:** `backend/tests/migrations/test_annual_calendar_migration.py`

## Description

Annual selections are explicit and reversibly migrate from the actual predecessor.

## Imports

| Source | Symbols |
|--------|---------|
| `alembic` | `command` |
| `app.models.calendar` | `Calendar`, `iteration_annual_calendars`, `profile_annual_calendars` |
| `app.models.capacity` | `ProfileAvailability` |
| `app.models.iteration` | `Iteration` |
| `app.models.team_member` | `TeamMemberProfile` |
| `app.services.upgrade_service` | `alembic_config` |
| `datetime` | `date` |
| `pytest` | `pytest` |
| `sqlalchemy` | `create_engine`, `inspect`, `select` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/models/calendar.py"]
    n1["backend/app/models/capacity.py"]
    n2["backend/app/models/iteration.py"]
    n3["backend/app/models/team_member.py"]
    n4["backend/app/services/upgrade_service.py"]
    n5["backend/tests/migrations/test_annual_calendar_migration.py"]
    n0 --> n2
    n1 --> n0
    n2 --> n0
    n2 --> n3
    n3 --> n2
    n5 --> n0
    n5 --> n1
    n5 --> n2
    n5 --> n3
    n5 --> n4
    click n0 "../modules/models_calendar.md"
    click n1 "../modules/models_capacity.md"
    click n2 "../modules/models_iteration.md"
    click n3 "../modules/team_member.md"
    click n4 "../modules/upgrade_service.md"
    click n5 "../modules/test_annual_calendar_migration.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [models_calendar](../modules/models_calendar.md) |
| Outbound | [models_capacity](../modules/models_capacity.md) |
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
| `test_annual_migration_preserves_existing_owners_and_refuses_loss` | `(dialect, request, tmp_path, configure_database)` | `@pytest.mark.parametrize('dialect', [pytest.param('sqlite', marks=pytest.mark.sqlite), pytest.param('postgresql', marks=[pytest.mark.postgresql, pytest.mark.integration, pytest.mark.allow_network])])` | — |

# test_profile_capacity_migrations Module

**Path:** `backend/tests/test_profile_capacity_migrations.py`

## Description

Preserve legacy absence identities and report conflicting person calendars.

## Imports

| Source | Symbols |
|--------|---------|
| `alembic` | `command` |
| `app.models.calendar` | `Calendar` |
| `app.models.iteration` | `Iteration` |
| `app.models.team_member` | `TeamMember`, `TeamMemberProfile`, `Vacation` |
| `app.services.upgrade_service` | `alembic_config` |
| `datetime` | `date` |
| `pytest` | `pytest` |
| `sqlalchemy` | `MetaData`, `Table`, `create_engine`, `select` |
| `sqlalchemy.engine` | `make_url` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/models/calendar.py"]
    n1["backend/app/models/iteration.py"]
    n2["backend/app/models/team_member.py"]
    n3["backend/app/services/upgrade_service.py"]
    n4["backend/tests/test_profile_capacity_migrations.py"]
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
    click n4 "../modules/test_profile_capacity_migrations.md"
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
| `test_legacy_backfill_retains_ids_deduplicates_and_reports_conflict` | `(dialect, request, tmp_path, configure_database)` | `@pytest.mark.parametrize('dialect', [pytest.param('sqlite', marks=pytest.mark.sqlite), pytest.param('postgresql', marks=[pytest.mark.postgresql, pytest.mark.allow_network])])` | — |

# ProfileAvailability

**Location:** `backend/app/models/capacity.py:20`
**Kind:** Class
**Bases:** `Base`
**Module:** [models_capacity](../modules/models_capacity.md)

## Description

Profile-owned calendar selection with a version, backfill provenance and unresolved legacy calendar IDs. An explicit selection reconciles the current calendar; allocation calendar differences remain visible to the person or operator.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `profile_id` | `Mapped[int]` | `mapped_column(ForeignKey('team_member_profiles.id', ondelete='CASCADE'), primary_key=True)` | — |
| `calendar_id` | `Mapped[int \| None]` | `mapped_column(ForeignKey('calendars.id', ondelete='RESTRICT'))` | — |
| `version` | `Mapped[int]` | `mapped_column(Integer, nullable=False, default=1)` | — |
| `provenance` | `Mapped[str]` | `mapped_column(String(40), nullable=False, default='explicit')` | — |
| `calendar_conflicts` | `Mapped[list]` | `mapped_column(JSON, nullable=False, default=list)` | — |
| `additional_calendars` | `Mapped[list[Calendar]]` | `relationship(Calendar, secondary=profile_annual_calendars, lazy='selectin', order_by=Calendar.year)` | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ProfileAvailability (backend/app/models/capacity.py)"]
    n1["Base (backend/app/database.py)"]
    n2["backend/app/models/__init__.py"]
    n3["backend/app/services/calendar_service.py"]
    n4["CapacityService.set_calendar (backend/app/services/capacity_service.py)"]
    n5["backend/app/services/planning_input_context.py"]
    n6["backend/tests/migrations/test_annual_calendar_migration.py"]
    n7["test_hidden_person_protects_shared_master_without_leaking_their_identity (backend/tests/test_annual_calendar_coverage.py)"]
    n8["test_single_year_apply_protects_accepted_work_even_with_personal_annuals (backend/tests/test_annual_calendar_coverage.py)"]
    n9["test_postgres_dispatch_serializes_with_supplemental_policy_replacement (backend/tests/test_annual_calendar_work_control.py)"]
    n10["backend/tests/test_planning_input_context.py"]
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
    click n0 "../modules/models_capacity.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/models___init__.md"
    click n3 "../modules/calendar_service.md"
    click n4 "../modules/capacity_service.md"
    click n5 "../modules/planning_input_context.md"
    click n6 "../modules/test_annual_calendar_migration.md"
    click n7 "../modules/test_annual_calendar_coverage.md"
    click n8 "../modules/test_annual_calendar_coverage.md"
    click n9 "../modules/test_annual_calendar_work_control.md"
    click n10 "../modules/test_planning_input_context.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [models_capacity](../modules/models_capacity.md) | 0 | `additional_calendars`, `calendar_conflicts`, `calendar_id`, `profile_id`, `provenance`, `version` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Base` | [app_database](../modules/app_database.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `calendar_service` | import | [calendar_service](../modules/calendar_service.md) | — |
| `CapacityService.set_calendar` | call | [capacity_service](../modules/capacity_service.md) | 1 |
| `planning_input_context` | import | [planning_input_context](../modules/planning_input_context.md) | — |
| `test_annual_calendar_migration` | import | [test_annual_calendar_migration](../modules/test_annual_calendar_migration.md) | — |
| `test_hidden_person_protects_shared_master_without_leaking_their_identity` | call | [test_annual_calendar_coverage](../modules/test_annual_calendar_coverage.md) | 1 |
| `test_single_year_apply_protects_accepted_work_even_with_personal_annuals` | call | [test_annual_calendar_coverage](../modules/test_annual_calendar_coverage.md) | 1 |
| `test_postgres_dispatch_serializes_with_supplemental_policy_replacement` | call | [test_annual_calendar_work_control](../modules/test_annual_calendar_work_control.md) | 1 |
| `test_planning_input_context` | import | [test_planning_input_context](../modules/test_planning_input_context.md) | — |

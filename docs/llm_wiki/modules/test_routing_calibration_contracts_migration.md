# test_routing_calibration_contracts_migration Module

**Path:** `backend/tests/migrations/test_routing_calibration_contracts_migration.py`

## Description

The calibration contract upgrade adds governed tables and never drops a submitted contract.

## Imports

| Source | Symbols |
|--------|---------|
| `alembic` | `command` |
| `alembic.script` | `ScriptDirectory` |
| `app.services.upgrade_service` | `alembic_config` |
| `pytest` | `pytest` |
| `sqlalchemy` | `create_engine`, `inspect`, `text` |
| `sqlalchemy.exc` | `IntegrityError` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/services/upgrade_service.py"]
    n1["backend/tests/migrations/test_routing_calibration_contracts_migration.py"]
    n1 --> n0
    click n0 "../modules/upgrade_service.md"
    click n1 "../modules/test_routing_calibration_contracts_migration.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [upgrade_service](../modules/upgrade_service.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 3 | 1 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_row` | `(key: str, *, state: str = 'submitted', approved: bool = False, digest: str = DIGEST) -> dict` | — | — |
| `test_upgrade_adds_contract_tables_and_downgrade_refuses_to_lose_a_contract` | `(dialect, request, tmp_path, configure_database)` | `@pytest.mark.parametrize('dialect', [pytest.param('sqlite', marks=pytest.mark.sqlite), pytest.param('postgresql', marks=[pytest.mark.postgresql, pytest.mark.integration, pytest.mark.allow_network])])` | — |

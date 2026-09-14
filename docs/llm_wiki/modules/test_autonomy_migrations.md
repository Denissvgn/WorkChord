# test_autonomy_migrations Module

**Path:** `backend/tests/autonomy/test_autonomy_migrations.py`

## Description

Dual-dialect migration coverage for the autonomous control-plane mirror.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `alembic` | `command` |
| `alembic.script` | `ScriptDirectory` |
| `app.config` | `get_settings` |
| `app.models.autonomy` | `AgentAutonomyTopologyMember`, `AgentObservationJob`, `AgentVerificationEvent`, `AgentVerificationRequirement` |
| `app.services.upgrade_service` | `alembic_config` |
| `pathlib` | `Path` |
| `pytest` | `pytest` |
| `sqlalchemy` | `create_engine`, `inspect`, `text` |
| `sqlalchemy.dialects` | `postgresql` |
| `sqlalchemy.schema` | `CreateTable` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/config.py"]
    n1["backend/app/models/autonomy.py"]
    n2["backend/app/services/upgrade_service.py"]
    n3["backend/tests/autonomy/test_autonomy_migrations.py"]
    n2 --> n0
    n3 --> n0
    n3 --> n1
    n3 --> n2
    click n0 "../modules/config.md"
    click n1 "../modules/models_autonomy.md"
    click n2 "../modules/upgrade_service.md"
    click n3 "../modules/test_autonomy_migrations.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [config](../modules/config.md) |
| Outbound | [models_autonomy](../modules/models_autonomy.md) |
| Outbound | [upgrade_service](../modules/upgrade_service.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 3 | 1 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `autonomy_migration_config` | `(tmp_path: Path, monkeypatch: pytest.MonkeyPatch)` | `@pytest.fixture` | — |
| `test_autonomy_projection_upgrade_downgrade_upgrade` | `(autonomy_migration_config) -> None` | `@pytest.mark.sqlite` | — |
| `test_autonomy_projection_postgresql_ddl_preserves_fences` | `() -> None` | `@pytest.mark.contract` | — |
| `test_autonomy_migration_chain_has_one_head` | `() -> None` | `@pytest.mark.contract` | — |

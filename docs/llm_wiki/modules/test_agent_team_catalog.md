# test_agent_team_catalog Module

**Path:** `backend/tests/test_agent_team_catalog.py`

## Description

Team setup shares deployed bundle identities and integrity failures.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app.config` | `get_settings` |
| `app.models.agent` | `AgentActor`, `AgentModelCatalogEntry` |
| `app.schemas.agent_skill_bundle` | `SkillBundleCatalogResponse` |
| `app.schemas.agent_team_setup` | `AgentTeamManifestRequest`, `AgentTeamMaster`, `AgentTeamPlanRequest` |
| `app.services.agent_skill_bundle_service` | `AgentSkillBundleService`, `SkillBundleArtifactError` |
| `app.services.agent_team_setup_service` | `AgentTeamSetupConflictError`, `AgentTeamSetupService` |
| `app.utils.time` | `utc_now` |
| `collections.abc` | `Iterator` |
| `json` | `json` |
| `pathlib` | `Path` |
| `pytest` | `pytest` |
| `shutil` | `shutil` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/config.py"]
    n1["backend/app/models/agent.py"]
    n2["backend/app/schemas/agent_skill_bundle.py"]
    n3["backend/app/schemas/agent_team_setup.py"]
    n4["backend/app/services/agent_skill_bundle_service.py"]
    n5["backend/app/services/agent_team_setup_service.py"]
    n6["backend/app/utils/time.py"]
    n7["backend/tests/test_agent_team_catalog.py"]
    n1 --> n6
    n4 --> n2
    n5 --> n0
    n5 --> n1
    n5 --> n2
    n5 --> n3
    n5 --> n4
    n5 --> n6
    n7 --> n0
    n7 --> n1
    n7 --> n2
    n7 --> n3
    n7 --> n4
    n7 --> n5
    n7 --> n6
    click n0 "../modules/config.md"
    click n1 "../modules/models_agent.md"
    click n2 "../modules/agent_skill_bundle.md"
    click n3 "../modules/agent_team_setup.md"
    click n4 "../modules/agent_skill_bundle_service.md"
    click n5 "../modules/agent_team_setup_service.md"
    click n6 "../modules/time.md"
    click n7 "../modules/test_agent_team_catalog.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [config](../modules/config.md) |
| Outbound | [models_agent](../modules/models_agent.md) |
| Outbound | [agent_skill_bundle](../modules/agent_skill_bundle.md) |
| Outbound | [agent_team_setup](../modules/agent_team_setup.md) |
| Outbound | [agent_skill_bundle_service](../modules/agent_skill_bundle_service.md) |
| Outbound | [agent_team_setup_service](../modules/agent_team_setup_service.md) |
| Outbound | [time](../modules/time.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 1 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `deployed_release` | `(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, agent_skill_artifact_root: Path) -> Iterator[Path]` | `@pytest.fixture` | — |
| `test_setup_uses_the_delivery_catalog_and_returns_independent_copies` | `(deployed_release: Path) -> None` | — | — |
| `test_setup_uses_an_explicit_release_service` | `(deployed_release: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None` | — | — |
| `test_setup_and_delivery_fail_closed_on_damaged_release` | `(deployed_release: Path, monkeypatch: pytest.MonkeyPatch, damage: str) -> None` | `@pytest.mark.parametrize('damage', ['missing-directory', 'missing-checksums', 'invalid-catalog', 'invalid-checksums', 'archive', 'trust-pin'])` | — |
| `test_setup_revalidates_an_archive_changed_after_cache_population` | `(deployed_release: Path) -> None` | — | — |
| `test_deployed_catalog_supports_validation_and_bound_planning` | *(async)* `(deployed_release: Path, db_session: AsyncSession, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None` | `@pytest.mark.asyncio` | — |

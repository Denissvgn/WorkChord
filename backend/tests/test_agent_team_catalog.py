"""Team setup shares deployed bundle identities and integrity failures."""

from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path
import shutil

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.models.agent import AgentActor, AgentModelCatalogEntry
from app.schemas.agent_skill_bundle import SkillBundleCatalogResponse
from app.schemas.agent_team_setup import (
    AgentTeamManifestRequest,
    AgentTeamMaster,
    AgentTeamPlanRequest,
)
from app.services.agent_skill_bundle_service import (
    AgentSkillBundleService,
    SkillBundleArtifactError,
)
from app.services.agent_team_setup_service import (
    AgentTeamSetupConflictError,
    AgentTeamSetupService,
)
from app.utils.time import utc_now


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def deployed_release(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, agent_skill_artifact_root: Path,
) -> Iterator[Path]:
    release = tmp_path / "role-artifacts"
    shutil.copytree(agent_skill_artifact_root, release)
    monkeypatch.setenv("WORKCHORD_AGENT_SKILL_ARTIFACTS_DIR", str(release))
    monkeypatch.setenv("AGENT_SKILL_BUNDLES_PUBLIC", "false")
    monkeypatch.setenv("AGENT_SKILL_BUNDLE_TRUSTED_CHECKSUMS_SHA256", "")
    get_settings.cache_clear()
    AgentSkillBundleService.clear_cache()
    yield release
    AgentSkillBundleService.clear_cache()
    get_settings.cache_clear()


def test_setup_uses_the_delivery_catalog_and_returns_independent_copies(
    deployed_release: Path,
) -> None:
    delivery = AgentSkillBundleService()
    setup = AgentTeamSetupService(None)
    served = SkillBundleCatalogResponse.model_validate_json(
        delivery.catalog_payload().content
    )
    selected = setup._skill_catalog()
    assert setup.skill_bundle_service.artifact_root == deployed_release
    assert selected == served
    selected.skills.clear()
    assert setup._skill_catalog() == served
    assert delivery.catalog() == served


def test_setup_uses_an_explicit_release_service(
    deployed_release: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    delivery = AgentSkillBundleService(artifact_root=deployed_release)
    monkeypatch.setenv("WORKCHORD_AGENT_SKILL_ARTIFACTS_DIR", str(tmp_path / "unavailable"))
    setup = AgentTeamSetupService(None, skill_bundle_service=delivery)
    assert setup.skill_bundle_service is delivery
    assert setup._skill_catalog() == delivery.catalog()


@pytest.mark.parametrize(
    "damage",
    ["missing-directory", "missing-checksums", "invalid-catalog", "invalid-checksums", "archive", "trust-pin"],
)
def test_setup_and_delivery_fail_closed_on_damaged_release(
    deployed_release: Path,
    monkeypatch: pytest.MonkeyPatch,
    damage: str,
) -> None:
    if damage == "missing-directory":
        deployed_release.rename(deployed_release.with_name("unavailable"))
    elif damage == "missing-checksums":
        (deployed_release / "checksums.json").unlink()
    elif damage in {"invalid-catalog", "invalid-checksums"}:
        name = "catalog.json" if damage == "invalid-catalog" else "checksums.json"
        (deployed_release / name).write_text("{}", encoding="utf-8")
    elif damage == "archive":
        archive = next(deployed_release.glob("*.zip"))
        archive.write_bytes(archive.read_bytes() + b"corrupt")
    else:
        monkeypatch.setenv("AGENT_SKILL_BUNDLE_TRUSTED_CHECKSUMS_SHA256", "0" * 64)
        get_settings.cache_clear()

    with pytest.raises(SkillBundleArtifactError):
        AgentSkillBundleService().catalog_payload()
    with pytest.raises(AgentTeamSetupConflictError) as failure:
        AgentTeamSetupService(None)._skill_catalog()
    assert failure.value.code == "agent_team_skill_catalog_unavailable"
    assert isinstance(failure.value.__cause__, SkillBundleArtifactError)


def test_setup_revalidates_an_archive_changed_after_cache_population(
    deployed_release: Path,
) -> None:
    setup = AgentTeamSetupService(None)
    setup._skill_catalog()
    archive = next(deployed_release.glob("*.zip"))
    archive.write_bytes(archive.read_bytes() + b"corrupt")
    with pytest.raises(AgentTeamSetupConflictError) as failure:
        setup._skill_catalog()
    assert failure.value.code == "agent_team_skill_catalog_unavailable"


@pytest.mark.asyncio
async def test_deployed_catalog_supports_validation_and_bound_planning(
    deployed_release: Path,
    db_session: AsyncSession,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    manifest = AgentTeamMaster.model_validate_json(
        (REPOSITORY_ROOT / "config/examples/agent-team-master.json").read_text()
    )
    for key in {member.default_model_binding_key for member in manifest.all_members}:
        db_session.add(AgentModelCatalogEntry(
            key=key, provider="local", configured_model_alias=key,
            reasoning_tier=2, context_tier="medium", modality_tags=["text"],
            cost_tier="low", latency_tier="balanced", enabled=True, revision=1,
        ))
    await db_session.commit()
    sink = tmp_path / "credentials"
    sink.mkdir(mode=0o700)
    monkeypatch.setenv("AGENT_TEAM_CREDENTIAL_SINK_DIR", str(sink))
    get_settings.cache_clear()
    service = AgentTeamSetupService(db_session)
    actor = AgentActor(
        id=0, name="admin-api-key", display_name="Operator",
        api_key_hash="admin", scopes=json.dumps(["admin"]), enabled=True,
        lifecycle_state="active", role="pm", created_at=utc_now(),
    )
    validation = await service.validate(actor, AgentTeamManifestRequest(manifest=manifest))
    assert validation.valid
    assert not validation.blocker_codes
    request = AgentTeamPlanRequest(manifest=manifest, expected_topology_revision=0)
    plan = await service.plan(actor, request)
    assert not plan.blocker_codes
    assert plan.expected_topology_revision == 0
    assert plan.manifest_digest == manifest.digest()
    assert len(plan.plan_digest) == 64
    assert all(action.operation == "create_member" for action in plan.actions)
    assert plan == await service.plan(actor, request)

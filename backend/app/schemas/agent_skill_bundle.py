"""Schemas for immutable, distributable agent role-skill bundles."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


SHA256_PATTERN = r"^[0-9a-f]{64}$"
SOURCE_REVISION_PATTERN = r"^sha256:[0-9a-f]{64}$"


class StrictBundleModel(BaseModel):
    """Reject undeclared build metadata instead of serving it accidentally."""

    model_config = ConfigDict(extra="forbid")


class SkillBundleFileRecord(StrictBundleModel):
    """One allow-listed file in an independently installable role skill."""

    path: str = Field(..., min_length=1)
    sha256: str = Field(..., pattern=SHA256_PATTERN)
    size: int = Field(..., ge=0)


class SkillBundleArchiveRecord(StrictBundleModel):
    """One exact downloadable archive representation of a role skill."""

    format: Literal["zip", "tar.gz"]
    path: str = Field(..., min_length=1)
    sha256: str = Field(..., pattern=SHA256_PATTERN)
    size: int = Field(..., ge=0)


class SkillBundleCatalogEntry(StrictBundleModel):
    """Versioned compatibility and integrity manifest for one role skill."""

    name: str = Field(..., pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    role: Literal["pm", "worker"]
    version: str = Field(..., pattern=r"^\d+\.\d+\.\d+$")
    path: str = Field(..., min_length=1)
    entrypoint: Literal["SKILL.md"]
    license: str = Field(..., min_length=1)
    api_contract: str = Field(..., min_length=1)
    server_compatibility: str = Field(..., min_length=1)
    required_features: list[str]
    required_scopes: list[str]
    optional_scopes: list[str]
    files: list[SkillBundleFileRecord]
    archives: list[SkillBundleArchiveRecord]


class SkillBundleCatalogResponse(StrictBundleModel):
    """Canonical catalog emitted by the deterministic skill build."""

    schema_version: Literal["workchord-agent-skills/v1"]
    catalog_version: str = Field(..., pattern=r"^\d+\.\d+\.\d+$")
    source_revision: str = Field(..., pattern=SOURCE_REVISION_PATTERN)
    api_contract: str = Field(..., min_length=1)
    skills: list[SkillBundleCatalogEntry]


class SkillBundleReleaseArtifact(StrictBundleModel):
    """Whole-file checksum for one release artifact."""

    path: str = Field(..., min_length=1)
    sha256: str = Field(..., pattern=SHA256_PATTERN)
    size: int = Field(..., ge=0)


class SkillBundleReleaseIndex(StrictBundleModel):
    """Checksum index emitted beside the catalog and role archives."""

    schema_version: Literal["workchord-agent-skills-release/v1"]
    catalog: SkillBundleReleaseArtifact
    artifacts: list[SkillBundleReleaseArtifact]


class SkillBundleManifestResponse(StrictBundleModel):
    """Exact-version manifest projected from the canonical catalog."""

    schema_version: Literal["workchord-agent-skill-manifest/v1"]
    entry_revision: str = Field(..., pattern=SOURCE_REVISION_PATTERN)
    skill: SkillBundleCatalogEntry


class SkillBundleDiscoveryResponse(StrictBundleModel):
    """Stable well-known pointer to the mutable catalog URL."""

    schema_version: Literal["workchord-agent-skills-discovery/v1"]
    catalog_url: str
    catalog_version: str
    source_revision: str
    api_contract: str

"""Read-only delivery of deterministic agent role-skill build artifacts."""
from __future__ import annotations

import base64
import hashlib
import json
import logging
import os
import re
import stat
import threading
import zipfile
from collections import Counter
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path, PurePosixPath
from typing import Any, Literal

from pydantic import ValidationError

from app.schemas.agent_skill_bundle import (
    SkillBundleArchiveRecord,
    SkillBundleCatalogEntry,
    SkillBundleCatalogResponse,
    SkillBundleDiscoveryResponse,
    SkillBundleManifestResponse,
    SkillBundleReleaseIndex,
)


CATALOG_FILENAME = "catalog.json"
CHECKSUMS_FILENAME = "checksums.json"
IMMUTABLE_CACHE_CONTROL = "public, max-age=31536000, immutable, no-transform"
CATALOG_CACHE_CONTROL = "public, max-age=60, must-revalidate, no-transform"
DISCOVERY_CACHE_CONTROL = "public, max-age=300, must-revalidate, no-transform"
REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
logger = logging.getLogger(__name__)


class SkillBundleNotFoundError(LookupError):
    """Raised when a requested exact skill, version, format, or file is absent."""


class SkillBundleArtifactError(RuntimeError):
    """Raised when deployed build artifacts fail their integrity contract."""


@dataclass(frozen=True)
class SkillBundlePayload:
    """Exact response bytes and their transport integrity metadata."""

    content: bytes
    media_type: str
    etag: str
    content_digest: str
    cache_control: str
    filename: str | None = None

    @classmethod
    def from_bytes(
        cls,
        content: bytes,
        *,
        media_type: str,
        cache_control: str,
        filename: str | None = None,
    ) -> "SkillBundlePayload":
        digest = hashlib.sha256(content).digest()
        digest_hex = digest.hex()
        return cls(
            content=content,
            media_type=media_type,
            etag=f'"{digest_hex}"',
            content_digest=f"sha-256=:{base64.b64encode(digest).decode('ascii')}:",
            cache_control=cache_control,
            filename=filename,
        )


@dataclass(frozen=True)
class _LoadedRelease:
    catalog: SkillBundleCatalogResponse
    catalog_bytes: bytes
    skills: dict[tuple[str, str], SkillBundleCatalogEntry]
    artifact_bytes: dict[str, bytes]


@dataclass(frozen=True)
class _ReleaseLimits:
    max_artifacts: int
    max_artifact_bytes: int
    max_total_bytes: int
    max_metadata_bytes: int
    max_file_bytes: int


@dataclass(frozen=True)
class _CachedRelease:
    identity: tuple[Any, ...]
    release: _LoadedRelease


def default_skill_bundle_artifact_root() -> Path:
    """Resolve the deployed artifact directory without reading application data."""
    configured = os.getenv("WORKCHORD_AGENT_SKILL_ARTIFACTS_DIR")
    if configured:
        return Path(configured)
    container_path = Path("/app/agent-skill-artifacts")
    if container_path.is_dir():
        return container_path
    return REPOSITORY_ROOT / "dist" / "agent-skills"


class AgentSkillBundleService:
    """Validate and serve only files emitted by the deterministic skill build."""

    _cache_lock = threading.RLock()
    _release_cache: dict[tuple[Any, ...], _CachedRelease] = {}
    _cache_metrics: Counter[str] = Counter()

    def __init__(self, artifact_root: Path | None = None):
        from app.config import get_settings

        settings = get_settings()
        self.artifact_root = (
            artifact_root or default_skill_bundle_artifact_root()
        ).resolve()
        self.public_delivery = settings.agent_skill_bundles_public
        self.trusted_checksums_sha256 = (
            settings.agent_skill_bundle_trusted_checksums_sha256
        )
        self.limits = _ReleaseLimits(
            max_artifacts=settings.agent_skill_bundle_max_artifacts,
            max_artifact_bytes=settings.agent_skill_bundle_max_artifact_bytes,
            max_total_bytes=settings.agent_skill_bundle_max_total_bytes,
            max_metadata_bytes=settings.agent_skill_bundle_max_metadata_bytes,
            max_file_bytes=settings.agent_skill_bundle_max_file_bytes,
        )

    @classmethod
    def cache_metrics(cls) -> dict[str, int]:
        """Return process-local validation/cache counters for health exporters."""
        with cls._cache_lock:
            return dict(cls._cache_metrics)

    @classmethod
    def clear_cache(cls) -> None:
        """Clear validated snapshots; intended for deterministic test isolation."""
        with cls._cache_lock:
            cls._release_cache.clear()
            cls._cache_metrics.clear()

    @classmethod
    def _record_cache_event(cls, event: str) -> None:
        cls._cache_metrics[event] += 1
        logger.info("Agent skill bundle cache event: %s", event)

    @staticmethod
    def _sha256(content: bytes) -> str:
        return hashlib.sha256(content).hexdigest()

    @staticmethod
    def _json_bytes(value: dict[str, Any]) -> bytes:
        return (
            json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
            + "\n"
        ).encode("utf-8")

    @staticmethod
    def _validate_artifact_name(path: str) -> str:
        pure = PurePosixPath(path)
        if (
            not path
            or len(path) > 1024
            or "\\" in path
            or pure.is_absolute()
            or len(pure.parts) != 1
            or pure.as_posix() != path
            or pure.parts[0] in {".", ".."}
            or re.fullmatch(r"[A-Za-z0-9._-]+", path) is None
            or path.endswith((".", " "))
        ):
            raise SkillBundleArtifactError("Artifact index contains an unsafe path")
        return path

    @staticmethod
    def _validate_skill_file_path(path: str) -> str:
        pure = PurePosixPath(path)
        if (
            not path
            or "\\" in path
            or pure.is_absolute()
            or pure.as_posix() != path
            or any(part in {"", ".", ".."} for part in pure.parts)
            or any(
                len(part) > 255
                or ":" in part
                or part.endswith((".", " "))
                or any(ord(character) < 32 or ord(character) == 127 for character in part)
                for part in pure.parts
            )
        ):
            raise SkillBundleNotFoundError("Skill file is not allow-listed")
        return path

    def _read_artifact(self, filename: str, *, max_bytes: int) -> bytes:
        safe_name = self._validate_artifact_name(filename)
        path = self.artifact_root / safe_name
        flags = (
            os.O_RDONLY
            | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0)
        )
        try:
            descriptor = os.open(path, flags)
            with os.fdopen(descriptor, "rb") as stream:
                before = os.fstat(stream.fileno())
                if not stat.S_ISREG(before.st_mode):
                    raise SkillBundleArtifactError(
                        "Required skill artifact is unavailable"
                    )
                if before.st_size > max_bytes:
                    raise SkillBundleArtifactError(
                        "Skill artifact exceeds its size limit"
                    )
                content = stream.read(max_bytes + 1)
                after = os.fstat(stream.fileno())
            if len(content) > max_bytes:
                raise SkillBundleArtifactError("Skill artifact exceeds its size limit")
            if (
                before.st_dev,
                before.st_ino,
                before.st_size,
                before.st_mtime_ns,
                before.st_ctime_ns,
            ) != (
                after.st_dev,
                after.st_ino,
                after.st_size,
                after.st_mtime_ns,
                after.st_ctime_ns,
            ):
                raise SkillBundleArtifactError("Skill artifact changed while being read")
            if len(content) != before.st_size:
                raise SkillBundleArtifactError("Unable to read complete skill artifact")
            return content
        except SkillBundleArtifactError:
            raise
        except OSError as exc:
            if path.is_symlink():
                raise SkillBundleArtifactError("Required skill artifact is unavailable")
            raise SkillBundleArtifactError("Unable to read skill artifact") from exc

    def _release_identity(self) -> tuple[Any, ...]:
        """Fingerprint release metadata and bounded root entry identities."""
        try:
            root_stat = self.artifact_root.stat()
            if not stat.S_ISDIR(root_stat.st_mode):
                raise SkillBundleArtifactError("Skill artifact directory is unavailable")
            entries: list[tuple[Any, ...]] = []
            total_bytes = 0
            with os.scandir(self.artifact_root) as scanned:
                for entry in scanned:
                    if len(entries) >= self.limits.max_artifacts + 2:
                        raise SkillBundleArtifactError(
                            "Skill artifact count exceeds its configured limit"
                        )
                    entry_stat = entry.stat(follow_symlinks=False)
                    if entry.is_symlink() or not stat.S_ISREG(entry_stat.st_mode):
                        raise SkillBundleArtifactError(
                            "Skill artifact directory contains an unsafe entry"
                        )
                    self._validate_artifact_name(entry.name)
                    limit = (
                        self.limits.max_metadata_bytes
                        if entry.name in {CATALOG_FILENAME, CHECKSUMS_FILENAME}
                        else self.limits.max_artifact_bytes
                    )
                    if entry_stat.st_size > limit:
                        raise SkillBundleArtifactError(
                            "Skill artifact exceeds its size limit"
                        )
                    total_bytes += entry_stat.st_size
                    if total_bytes > self.limits.max_total_bytes:
                        raise SkillBundleArtifactError(
                            "Skill artifact release exceeds its total size limit"
                        )
                    entries.append(
                        (
                            entry.name,
                            entry_stat.st_dev,
                            entry_stat.st_ino,
                            entry_stat.st_size,
                            entry_stat.st_mtime_ns,
                            entry_stat.st_ctime_ns,
                        )
                    )
        except SkillBundleArtifactError:
            raise
        except OSError as exc:
            raise SkillBundleArtifactError(
                "Unable to inspect skill artifact directory"
            ) from exc

        catalog_bytes = self._read_artifact(
            CATALOG_FILENAME, max_bytes=self.limits.max_metadata_bytes
        )
        checksum_bytes = self._read_artifact(
            CHECKSUMS_FILENAME, max_bytes=self.limits.max_metadata_bytes
        )
        return (
            root_stat.st_dev,
            root_stat.st_ino,
            tuple(sorted(entries)),
            self._sha256(catalog_bytes),
            self._sha256(checksum_bytes),
        )

    @staticmethod
    def _index_unique_records(
        records: list[Any], *, label: str
    ) -> dict[str, Any]:
        indexed: dict[str, Any] = {}
        for record in records:
            if record.path in indexed:
                raise SkillBundleArtifactError(f"Duplicate {label} path")
            indexed[record.path] = record
        return indexed

    def _validate_skill_entry(self, skill: SkillBundleCatalogEntry) -> None:
        if skill.path != skill.name:
            raise SkillBundleArtifactError("Skill path does not match its name")
        if len(skill.files) == 0:
            raise SkillBundleArtifactError("Skill manifest has no files")
        if len(skill.files) > self.limits.max_artifacts:
            raise SkillBundleArtifactError(
                "Skill file count exceeds its configured limit"
            )
        file_records: dict[str, Any] = {}
        for record in skill.files:
            try:
                safe_path = self._validate_skill_file_path(record.path)
            except SkillBundleNotFoundError as exc:
                raise SkillBundleArtifactError(
                    "Skill manifest contains an unsafe path"
                ) from exc
            if safe_path in file_records:
                raise SkillBundleArtifactError(
                    "Skill manifest contains a duplicate path"
                )
            if record.size > self.limits.max_file_bytes:
                raise SkillBundleArtifactError("Skill file exceeds its size limit")
            file_records[safe_path] = record
        if skill.entrypoint not in file_records:
            raise SkillBundleArtifactError("Skill entrypoint is not allow-listed")
        for values in (
            skill.required_features,
            skill.required_scopes,
            skill.optional_scopes,
        ):
            if len(values) != len(set(values)) or any(not value for value in values):
                raise SkillBundleArtifactError("Skill requirements contain invalid values")

        archive_records = self._index_unique_records(skill.archives, label="archive")
        if {record.format for record in archive_records.values()} != {"zip", "tar.gz"}:
            raise SkillBundleArtifactError("Skill must publish zip and tar.gz archives")
        expected_archive_names = {
            f"{skill.name}-{skill.version}.zip",
            f"{skill.name}-{skill.version}.tar.gz",
        }
        if set(archive_records) != expected_archive_names:
            raise SkillBundleArtifactError("Skill archive name does not match its exact version")
        for archive_path in archive_records:
            self._validate_artifact_name(archive_path)

        if any(
            record.size > self.limits.max_artifact_bytes
            for record in archive_records.values()
        ):
            raise SkillBundleArtifactError("Skill archive exceeds its size limit")

    def _validate_release(self) -> _LoadedRelease:
        try:
            if not self.artifact_root.is_dir():
                raise SkillBundleArtifactError("Skill artifact directory is unavailable")
            catalog_bytes = self._read_artifact(
                CATALOG_FILENAME, max_bytes=self.limits.max_metadata_bytes
            )
            checksum_bytes = self._read_artifact(
                CHECKSUMS_FILENAME, max_bytes=self.limits.max_metadata_bytes
            )
            checksum_digest = self._sha256(checksum_bytes)
            if self.public_delivery and not self.trusted_checksums_sha256:
                raise SkillBundleArtifactError(
                    "Public skill bundle delivery requires a trusted release pin"
                )
            if (
                self.trusted_checksums_sha256
                and checksum_digest != self.trusted_checksums_sha256
            ):
                raise SkillBundleArtifactError("Skill release trust pin does not match")
            catalog = SkillBundleCatalogResponse.model_validate_json(catalog_bytes)
            release_index = SkillBundleReleaseIndex.model_validate_json(checksum_bytes)
        except (json.JSONDecodeError, ValidationError, UnicodeDecodeError) as exc:
            raise SkillBundleArtifactError("Skill artifact metadata is invalid") from exc

        if release_index.catalog.path != CATALOG_FILENAME:
            raise SkillBundleArtifactError("Release index points to an unexpected catalog")
        if (
            release_index.catalog.size != len(catalog_bytes)
            or release_index.catalog.sha256 != self._sha256(catalog_bytes)
        ):
            raise SkillBundleArtifactError("Catalog integrity check failed")

        skills: dict[tuple[str, str], SkillBundleCatalogEntry] = {}
        catalog_archives: dict[str, SkillBundleArchiveRecord] = {}
        for skill in catalog.skills:
            self._validate_skill_entry(skill)
            key = (skill.name, skill.version)
            if key in skills:
                raise SkillBundleArtifactError("Catalog contains a duplicate skill version")
            skills[key] = skill
            for archive in skill.archives:
                if archive.path in catalog_archives:
                    raise SkillBundleArtifactError("Catalog reuses an archive path")
                catalog_archives[archive.path] = archive

        indexed_release = self._index_unique_records(
            release_index.artifacts, label="release artifact"
        )
        if len(indexed_release) > self.limits.max_artifacts:
            raise SkillBundleArtifactError(
                "Skill artifact count exceeds its configured limit"
            )
        if set(indexed_release) != set(catalog_archives):
            raise SkillBundleArtifactError("Catalog and release artifact sets differ")

        total_release_bytes = len(catalog_bytes) + len(checksum_bytes)
        for release_record in indexed_release.values():
            if release_record.size > self.limits.max_artifact_bytes:
                raise SkillBundleArtifactError("Skill archive exceeds its size limit")
            total_release_bytes += release_record.size
        if total_release_bytes > self.limits.max_total_bytes:
            raise SkillBundleArtifactError(
                "Skill artifact release exceeds its total size limit"
            )

        expected_root_entries = {
            CATALOG_FILENAME,
            CHECKSUMS_FILENAME,
            *catalog_archives.keys(),
        }
        try:
            actual_root_entries = {entry.name for entry in os.scandir(self.artifact_root)}
        except OSError as exc:
            raise SkillBundleArtifactError("Unable to inspect skill artifact directory") from exc
        if actual_root_entries != expected_root_entries:
            raise SkillBundleArtifactError("Skill artifact directory contains unlisted entries")

        artifact_bytes: dict[str, bytes] = {}
        for path, catalog_record in catalog_archives.items():
            release_record = indexed_release[path]
            if (
                release_record.sha256 != catalog_record.sha256
                or release_record.size != catalog_record.size
            ):
                raise SkillBundleArtifactError("Catalog and release checksums differ")
            content = self._read_artifact(
                path, max_bytes=self.limits.max_artifact_bytes
            )
            if (
                len(content) != catalog_record.size
                or self._sha256(content) != catalog_record.sha256
            ):
                raise SkillBundleArtifactError("Role archive integrity check failed")
            artifact_bytes[path] = content

        return _LoadedRelease(
            catalog=catalog,
            catalog_bytes=catalog_bytes,
            skills=skills,
            artifact_bytes=artifact_bytes,
        )

    def _load_release(self) -> _LoadedRelease:
        """Return one atomically validated snapshot shared by REST and MCP callers."""
        cache_key = (
            self.artifact_root,
            self.public_delivery,
            self.trusted_checksums_sha256,
            self.limits,
        )
        with self._cache_lock:
            try:
                identity = self._release_identity()
                cached = self._release_cache.get(cache_key)
                if cached is not None and cached.identity == identity:
                    self._record_cache_event("hit")
                    return cached.release
                if cached is not None:
                    self._release_cache.pop(cache_key, None)
                    self._record_cache_event("invalidation")
                else:
                    self._record_cache_event("miss")

                release = self._validate_release()
                if self._release_identity() != identity:
                    raise SkillBundleArtifactError(
                        "Skill artifact release changed during validation"
                    )
                self._release_cache[cache_key] = _CachedRelease(
                    identity=identity,
                    release=release,
                )
                self._record_cache_event("validation")
                return release
            except SkillBundleArtifactError:
                self._record_cache_event("failure")
                raise

    @staticmethod
    def _find_skill(
        release: _LoadedRelease, skill_name: str, version: str
    ) -> SkillBundleCatalogEntry:
        skill = release.skills.get((skill_name, version))
        if skill is None:
            raise SkillBundleNotFoundError("Unknown skill bundle or version")
        return skill

    @staticmethod
    def _find_archive(
        skill: SkillBundleCatalogEntry, archive_format: Literal["zip", "tar.gz"]
    ) -> SkillBundleArchiveRecord:
        matches = [
            archive for archive in skill.archives if archive.format == archive_format
        ]
        if len(matches) != 1:
            raise SkillBundleNotFoundError("Requested archive format is unavailable")
        return matches[0]

    def catalog_payload(self) -> SkillBundlePayload:
        """Return the byte-exact mutable catalog build artifact."""
        release = self._load_release()
        return SkillBundlePayload.from_bytes(
            release.catalog_bytes,
            media_type="application/json",
            cache_control=CATALOG_CACHE_CONTROL,
        )

    def discovery_payload(self, catalog_url: str) -> SkillBundlePayload:
        """Return the well-known pointer plus current catalog identity."""
        release = self._load_release()
        response = SkillBundleDiscoveryResponse(
            schema_version="workchord-agent-skills-discovery/v1",
            catalog_url=catalog_url,
            catalog_version=release.catalog.catalog_version,
            source_revision=release.catalog.source_revision,
            api_contract=release.catalog.api_contract,
        )
        return SkillBundlePayload.from_bytes(
            self._json_bytes(response.model_dump(mode="json")),
            media_type="application/json",
            cache_control=DISCOVERY_CACHE_CONTROL,
        )

    def manifest_payload(self, skill_name: str, version: str) -> SkillBundlePayload:
        """Return a role-local manifest whose bytes cannot drift with other roles."""
        release = self._load_release()
        skill = self._find_skill(release, skill_name, version)
        skill_payload = skill.model_dump(mode="json")
        response = SkillBundleManifestResponse(
            schema_version="workchord-agent-skill-manifest/v1",
            entry_revision=f"sha256:{self._sha256(self._json_bytes(skill_payload))}",
            skill=skill,
        )
        return SkillBundlePayload.from_bytes(
            self._json_bytes(response.model_dump(mode="json")),
            media_type="application/json",
            cache_control=IMMUTABLE_CACHE_CONTROL,
        )

    def archive_payload(
        self,
        skill_name: str,
        version: str,
        archive_format: Literal["zip", "tar.gz"],
    ) -> SkillBundlePayload:
        """Return one immutable archive after release-wide checksum validation."""
        release = self._load_release()
        skill = self._find_skill(release, skill_name, version)
        archive = self._find_archive(skill, archive_format)
        media_type = "application/zip" if archive_format == "zip" else "application/gzip"
        return SkillBundlePayload.from_bytes(
            release.artifact_bytes[archive.path],
            media_type=media_type,
            cache_control=IMMUTABLE_CACHE_CONTROL,
            filename=archive.path,
        )

    def file_payload(
        self, skill_name: str, version: str, requested_path: str
    ) -> SkillBundlePayload:
        """Inspect one allow-listed file directly from the validated zip artifact."""
        release = self._load_release()
        skill = self._find_skill(release, skill_name, version)
        safe_path = self._validate_skill_file_path(requested_path)
        file_records = {record.path: record for record in skill.files}
        record = file_records.get(safe_path)
        if record is None:
            raise SkillBundleNotFoundError("Skill file is not allow-listed")
        archive = self._find_archive(skill, "zip")
        member_name = f"{skill.name}/{safe_path}"
        try:
            with zipfile.ZipFile(BytesIO(release.artifact_bytes[archive.path])) as zip_archive:
                members = zip_archive.infolist()
                if len(members) > self.limits.max_artifacts + 1:
                    raise SkillBundleArtifactError(
                        "Skill archive member count exceeds its configured limit"
                    )
                matches = [info for info in members if info.filename == member_name]
                if len(matches) != 1:
                    raise SkillBundleArtifactError(
                        "Skill archive member set is inconsistent"
                    )
                info = matches[0]
                mode = (info.external_attr >> 16) & 0o170000
                if (
                    info.is_dir()
                    or mode == stat.S_IFLNK
                    or mode not in {0, stat.S_IFREG}
                    or info.file_size != record.size
                ):
                    raise SkillBundleArtifactError("Skill archive member is unsafe")
                content = zip_archive.read(info)
        except (OSError, zipfile.BadZipFile, RuntimeError) as exc:
            raise SkillBundleArtifactError("Unable to inspect role archive") from exc
        if len(content) != record.size or self._sha256(content) != record.sha256:
            raise SkillBundleArtifactError("Skill file integrity check failed")

        if safe_path.endswith(".md"):
            media_type = "text/markdown; charset=utf-8"
        elif safe_path.endswith((".yaml", ".yml")):
            media_type = "application/yaml"
        else:
            media_type = "application/octet-stream"
        return SkillBundlePayload.from_bytes(
            content,
            media_type=media_type,
            cache_control=IMMUTABLE_CACHE_CONTROL,
        )

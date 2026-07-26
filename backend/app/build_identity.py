"""Revision-bound identity baked into WorkChord container images."""

from __future__ import annotations

import argparse
import json
from hashlib import sha256
from pathlib import Path
from typing import Literal

from pydantic import Field

from app.autonomy.canonical import StrictContractModel


BUILD_IDENTITY_PATH = Path("/app/workchord-build.json")
REVISION_PATTERN = r"^(?:[0-9a-f]{40,64}|unknown)$"
SHA256_PATTERN = r"^[0-9a-f]{64}$"


class BuildIdentity(StrictContractModel):
    """Content identity written while an image is built."""

    schema_version: Literal["workchord-build-identity-v1"] = (
        "workchord-build-identity-v1"
    )
    component: Literal["backend", "frontend"]
    source_revision: str = Field(pattern=REVISION_PATTERN)
    artifact_digest: str = Field(pattern=SHA256_PATTERN)


class BackendBuildIdentity(BuildIdentity):
    """Backend package identity plus its independently built gateway digest."""

    component: Literal["backend"] = "backend"
    expected_frontend_artifact_digest: str = Field(pattern=SHA256_PATTERN)


def load_backend_build_identity(
    path: Path = BUILD_IDENTITY_PATH,
) -> BackendBuildIdentity:
    """Read the backend image identity from its fixed filesystem location."""

    return BackendBuildIdentity.model_validate_json(path.read_text(encoding="utf-8"))


def package_artifact_digest(package_root: Path) -> str:
    """Hash stable package paths and bytes, excluding interpreter caches."""

    digest = sha256()
    members = sorted(
        path
        for path in package_root.rglob("*")
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.suffix not in {".pyc", ".pyo"}
    )
    if not members:
        raise ValueError("Backend package contains no identity members")
    for member in members:
        relative = member.relative_to(package_root).as_posix().encode("utf-8")
        digest.update(relative)
        digest.update(b"\0")
        digest.update(sha256(member.read_bytes()).digest())
        digest.update(b"\n")
    return digest.hexdigest()


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write the immutable backend container build identity."
    )
    parser.add_argument("--source-revision", required=True)
    parser.add_argument("--frontend-identity", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    package_root = Path(__file__).resolve().parent
    frontend_identity = BuildIdentity.model_validate_json(
        args.frontend_identity.read_text(encoding="utf-8")
    )
    if frontend_identity.component != "frontend":
        raise ValueError("Expected a frontend build identity")
    if frontend_identity.source_revision != args.source_revision:
        raise ValueError("Frontend and backend source revisions differ")
    identity = BackendBuildIdentity(
        source_revision=args.source_revision,
        artifact_digest=package_artifact_digest(package_root),
        expected_frontend_artifact_digest=frontend_identity.artifact_digest,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(identity.model_dump(mode="json"), sort_keys=True) + "\n",
        encoding="utf-8",
    )
    args.output.chmod(0o444)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

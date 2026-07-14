"""Read-only HTTP delivery for immutable agent role-skill artifacts."""
from __future__ import annotations

from typing import Annotated, Callable, Literal

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database import get_db
from app.schemas.agent_skill_bundle import (
    SkillBundleCatalogResponse,
    SkillBundleDiscoveryResponse,
    SkillBundleManifestResponse,
)
from app.services.agent_skill_bundle_service import (
    AgentSkillBundleService,
    SkillBundleArtifactError,
    SkillBundleNotFoundError,
    SkillBundlePayload,
)
from app.services.agent_service import AgentService, actor_has_scope


router = APIRouter()
well_known_router = APIRouter()


async def get_agent_skill_bundle_service() -> AgentSkillBundleService:
    """Create a service against the configured code-owned artifact directory."""
    return AgentSkillBundleService()


async def require_agent_skill_bundle_access(
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    """Require skills:read unless public code-artifact delivery is explicit."""
    if get_settings().agent_skill_bundles_public:
        return
    api_key = request.headers.get("X-Agent-API-Key")
    authorization = request.headers.get("Authorization")
    if api_key is None and authorization:
        scheme, separator, token = authorization.partition(" ")
        if separator and scheme.lower() == "bearer" and token:
            api_key = token
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Agent skill bundle access requires authentication.",
        )
    actor = await AgentService(db).authenticate(api_key)
    if actor is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or disabled agent API key.",
        )
    if not actor_has_scope(actor, "skills:read"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Missing required scope: skills:read",
        )


def _resolve_payload(action: Callable[[], SkillBundlePayload]) -> SkillBundlePayload:
    try:
        return action()
    except SkillBundleNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill bundle resource not found.",
        ) from exc
    except SkillBundleArtifactError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Skill bundle artifacts are unavailable.",
        ) from exc


def _etag_matches(if_none_match: str | None, etag: str) -> bool:
    if not if_none_match:
        return False
    for candidate in if_none_match.split(","):
        value = candidate.strip()
        if value == "*" or value == etag or value.removeprefix("W/") == etag:
            return True
    return False


def _response(payload: SkillBundlePayload, request: Request) -> Response:
    cache_control = payload.cache_control
    if not get_settings().agent_skill_bundles_public:
        cache_control = cache_control.replace("public,", "private,", 1)
    headers = {
        "ETag": payload.etag,
        "Content-Digest": payload.content_digest,
        "Cache-Control": cache_control,
        "X-Content-Type-Options": "nosniff",
    }
    if payload.filename is not None:
        headers["Content-Disposition"] = f'attachment; filename="{payload.filename}"'
    if _etag_matches(request.headers.get("if-none-match"), payload.etag):
        return Response(status_code=status.HTTP_304_NOT_MODIFIED, headers=headers)
    return Response(content=payload.content, media_type=payload.media_type, headers=headers)


@well_known_router.get(
    "/.well-known/workchord-agent-skills.json",
    response_model=SkillBundleDiscoveryResponse,
)
async def discover_agent_skill_bundles(
    request: Request,
    service: Annotated[AgentSkillBundleService, Depends(get_agent_skill_bundle_service)],
    _access: Annotated[None, Depends(require_agent_skill_bundle_access)],
) -> Response:
    """Advertise the current catalog URL without embedding instance data."""
    api_prefix = get_settings().api_prefix.rstrip("/")
    payload = _resolve_payload(
        lambda: service.discovery_payload(f"{api_prefix}/agent/skill-bundles")
    )
    return _response(payload, request)


@router.get("/agent/skill-bundles", response_model=SkillBundleCatalogResponse)
async def list_agent_skill_bundles(
    request: Request,
    service: Annotated[AgentSkillBundleService, Depends(get_agent_skill_bundle_service)],
    _access: Annotated[None, Depends(require_agent_skill_bundle_access)],
) -> Response:
    """Serve the byte-exact mutable catalog emitted by the build."""
    return _response(_resolve_payload(service.catalog_payload), request)


@router.get(
    "/agent/skill-bundles/{skill_name}/{version}/manifest",
    response_model=SkillBundleManifestResponse,
)
async def get_agent_skill_bundle_manifest(
    skill_name: str,
    version: str,
    request: Request,
    service: Annotated[AgentSkillBundleService, Depends(get_agent_skill_bundle_service)],
    _access: Annotated[None, Depends(require_agent_skill_bundle_access)],
) -> Response:
    """Serve one immutable exact-version role manifest."""
    payload = _resolve_payload(lambda: service.manifest_payload(skill_name, version))
    return _response(payload, request)


@router.get(
    "/agent/skill-bundles/{skill_name}/{version}/download",
    responses={
        status.HTTP_200_OK: {
            "content": {"application/zip": {}, "application/gzip": {}}
        }
    },
)
async def download_agent_skill_bundle(
    skill_name: str,
    version: str,
    request: Request,
    service: Annotated[AgentSkillBundleService, Depends(get_agent_skill_bundle_service)],
    _access: Annotated[None, Depends(require_agent_skill_bundle_access)],
    archive_format: Annotated[
        Literal["zip", "tar.gz"], Query(alias="format")
    ] = "zip",
) -> Response:
    """Download an immutable zip or tar.gz role archive."""
    payload = _resolve_payload(
        lambda: service.archive_payload(skill_name, version, archive_format)
    )
    return _response(payload, request)


@router.get(
    "/agent/skill-bundles/{skill_name}/{version}/files/{file_path:path}",
    responses={
        status.HTTP_200_OK: {
            "content": {
                "text/markdown": {},
                "application/yaml": {},
                "application/octet-stream": {},
            }
        }
    },
)
async def inspect_agent_skill_bundle_file(
    skill_name: str,
    version: str,
    file_path: str,
    request: Request,
    service: Annotated[AgentSkillBundleService, Depends(get_agent_skill_bundle_service)],
    _access: Annotated[None, Depends(require_agent_skill_bundle_access)],
) -> Response:
    """Inspect one catalog-allow-listed file from the immutable role archive."""
    payload = _resolve_payload(
        lambda: service.file_payload(skill_name, version, file_path)
    )
    return _response(payload, request)

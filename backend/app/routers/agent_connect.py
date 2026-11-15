"""Public, secret-free hint telling an agent how to connect and obtain a key."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from app.config import get_settings
from app.schemas.agent_connect import (
    AgentConnectCredential,
    AgentConnectResponse,
    AgentConnectRole,
)
from app.schemas.agent_skill_bundle import SkillBundleCatalogResponse
from app.services.agent_skill_bundle_service import (
    AgentSkillBundleService,
    SkillBundleArtifactError,
    SkillBundleNotFoundError,
)


router = APIRouter()

KEY_SOURCES = [
    "AGENT_API_KEY",
    "AGENT_API_KEY_FILE",
    "${XDG_CONFIG_HOME:-~/.config}/workchord/<role-skill>.key",
]
MCP_STDIO_KEY_SOURCES = ["MCP_AGENT_API_KEY", "MCP_AGENT_API_KEY_FILE"]
DEFAULT_KEY_FILE = "${XDG_CONFIG_HOME:-~/.config}/workchord/<role-skill>.key"
PROVISIONING = [
    "An operator creates one agent actor per agent, with the role and scopes listed for its role skill.",
    "The operator stores the actor's one-time key where the agent runtime reads it: "
    "a key variable, a key file named by AGENT_API_KEY_FILE, the default key file, "
    "or the MCP client's bearer-token setting.",
    "A key file holds only the key, is readable by its owner only (chmod 600), "
    "and lives outside every repository.",
    "Agents never ask for a key in chat and never use the bootstrap or admin key.",
]


async def get_agent_connect_bundle_service() -> AgentSkillBundleService:
    """Read role scopes from the same deployed catalog the skill routes serve."""
    return AgentSkillBundleService()


def _roles(service: AgentSkillBundleService) -> list[AgentConnectRole]:
    try:
        payload = service.catalog_payload()
        catalog = SkillBundleCatalogResponse.model_validate_json(payload.content)
    except (SkillBundleArtifactError, SkillBundleNotFoundError, ValueError):
        # The hint stays useful when release artifacts were not deployed.
        return []
    return [
        AgentConnectRole(
            skill=entry.name,
            skill_version=entry.version,
            actor_role=entry.role,
            required_scopes=entry.required_scopes,
            optional_scopes=entry.optional_scopes,
        )
        for entry in catalog.skills
    ]


@router.get("/.well-known/workchord/agent-connect.json", response_model=AgentConnectResponse)
async def get_agent_connect_hint(
    service: Annotated[AgentSkillBundleService, Depends(get_agent_connect_bundle_service)],
) -> AgentConnectResponse:
    """Tell an unauthenticated agent where to connect and what key it needs."""
    settings = get_settings()
    prefix = settings.api_prefix.rstrip("/")
    return AgentConnectResponse(
        auth_mode=settings.workchord_auth_mode,
        api_prefix=prefix or "/",
        capabilities_path=f"{prefix}/agent/capabilities",
        mcp_http_path=f"{prefix}/mcp",
        skill_discovery_path="/.well-known/workchord-agent-skills.json",
        credential=AgentConnectCredential(
            key_sources=KEY_SOURCES,
            mcp_stdio_key_sources=MCP_STDIO_KEY_SOURCES,
            default_key_file=DEFAULT_KEY_FILE,
        ),
        roles=_roles(service),
        provisioning=PROVISIONING,
    )

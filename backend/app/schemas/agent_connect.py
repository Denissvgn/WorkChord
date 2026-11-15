"""Secret-free connection hint for agents that do not yet hold a key."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict


class AgentConnectModel(BaseModel):
    """Reject undeclared fields so nothing extra is ever published here."""

    model_config = ConfigDict(extra="forbid")


class AgentConnectCredential(AgentConnectModel):
    """Where an agent sends its key and where its runtime may read it from."""

    rest_header: Literal["X-Agent-API-Key"] = "X-Agent-API-Key"
    mcp_http_authorization_scheme: Literal["Bearer"] = "Bearer"
    key_sources: list[str]
    mcp_stdio_key_sources: list[str]
    default_key_file: str
    anonymous_agent_access: Literal[False] = False


class AgentConnectRole(AgentConnectModel):
    """The actor role and scopes an operator provisions for one role skill."""

    skill: str
    skill_version: str
    actor_role: Literal["pm", "worker", "verifier"]
    required_scopes: list[str]
    optional_scopes: list[str]


class AgentConnectResponse(AgentConnectModel):
    """How to reach this server as an agent; never holds credentials or instance data."""

    schema_version: Literal["workchord-agent-connect/v1"] = "workchord-agent-connect/v1"
    auth_mode: Literal["managed", "trusted_local"]
    api_prefix: str
    capabilities_path: str
    mcp_http_path: str
    skill_discovery_path: str
    credential: AgentConnectCredential
    roles: list[AgentConnectRole]
    provisioning: list[str]

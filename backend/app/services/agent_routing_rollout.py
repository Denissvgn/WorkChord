"""Fail-closed rollout controls for model-aware agent routing."""

from __future__ import annotations

from dataclasses import dataclass
from contextvars import ContextVar, Token
from enum import StrEnum
import re
from typing import Any

from app.config import get_settings


TOPOLOGY_READINESS_SCHEMA_VERSION = (
    "model-aware-routing-topology-readiness-v1"
)
MAX_READINESS_BLOCKER_CODES = 20
_BLOCKER_CODE_PATTERN = re.compile(r"^[a-z][a-z0-9_]{0,63}$")
_TOPOLOGY_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,99}$")


class AgentRoutingRolloutMode(StrEnum):
    """Deployment-owned model-aware routing rollout modes."""

    OFF = "off"
    SHADOW = "shadow"
    ENFORCED = "enforced"


class AgentRoutingTopologyReadinessStatus(StrEnum):
    """Closed readiness states supplied by the setup authority."""

    UNAVAILABLE = "unavailable"
    NOT_READY = "not_ready"
    READY = "ready"


class AgentRoutingTopologyReadinessSource(StrEnum):
    """Closed authorities allowed to supply topology readiness."""

    UNAVAILABLE = "unavailable"
    AGENT_TEAM_MASTER = "agent-team-master-v1"


@dataclass(frozen=True)
class AgentRoutingTopologyReadiness:
    """Narrow, secret-free input supplied by a server-side topology authority."""

    schema_version: str = TOPOLOGY_READINESS_SCHEMA_VERSION
    status: AgentRoutingTopologyReadinessStatus = (
        AgentRoutingTopologyReadinessStatus.UNAVAILABLE
    )
    source: AgentRoutingTopologyReadinessSource = (
        AgentRoutingTopologyReadinessSource.UNAVAILABLE
    )
    topology_id: str | None = None
    topology_revision: int | None = None
    blocker_codes: tuple[str, ...] = ("topology_readiness_unavailable",)

    def __post_init__(self) -> None:
        if self.schema_version != TOPOLOGY_READINESS_SCHEMA_VERSION:
            raise ValueError("Unsupported topology-readiness schema version")

        try:
            status = AgentRoutingTopologyReadinessStatus(self.status)
            source = AgentRoutingTopologyReadinessSource(self.source)
        except ValueError as exc:
            raise ValueError("Unsupported topology-readiness state") from exc
        object.__setattr__(self, "status", status)
        object.__setattr__(self, "source", source)

        if self.topology_id is not None and (
            not isinstance(self.topology_id, str)
            or _TOPOLOGY_ID_PATTERN.fullmatch(self.topology_id) is None
        ):
            raise ValueError("topology_id must be a bounded stable identifier or null")
        if self.topology_revision is not None and (
            isinstance(self.topology_revision, bool)
            or not isinstance(self.topology_revision, int)
            or self.topology_revision < 1
        ):
            raise ValueError(
                "topology_revision must be a positive integer or null"
            )

        normalized_codes = tuple(sorted(set(self.blocker_codes)))
        if len(normalized_codes) > MAX_READINESS_BLOCKER_CODES:
            raise ValueError("Topology readiness has too many blocker codes")
        if any(
            not isinstance(code, str)
            or _BLOCKER_CODE_PATTERN.fullmatch(code) is None
            for code in normalized_codes
        ):
            raise ValueError("Topology readiness blocker codes are invalid")
        object.__setattr__(self, "blocker_codes", normalized_codes)

        if status == AgentRoutingTopologyReadinessStatus.UNAVAILABLE:
            if (
                source != AgentRoutingTopologyReadinessSource.UNAVAILABLE
                or self.topology_id is not None
                or self.topology_revision is not None
                or normalized_codes != ("topology_readiness_unavailable",)
            ):
                raise ValueError(
                    "Unavailable topology readiness must use the unavailable "
                    "source and canonical blocker"
                )
            return

        if source != AgentRoutingTopologyReadinessSource.AGENT_TEAM_MASTER:
            raise ValueError(
                "Available topology readiness must come from "
                "agent-team-master-v1"
            )
        if self.topology_id is None or self.topology_revision is None:
            raise ValueError(
                "Available topology readiness requires topology identity and revision"
            )
        if status == AgentRoutingTopologyReadinessStatus.READY:
            if normalized_codes:
                raise ValueError("Ready topology readiness cannot have blockers")
        elif not normalized_codes:
            raise ValueError("Not-ready topology readiness requires blockers")

    @classmethod
    def unavailable(cls) -> "AgentRoutingTopologyReadiness":
        """Return the pre-setup fail-closed readiness input."""

        return cls()

    @classmethod
    def not_ready(
        cls,
        *,
        topology_id: str,
        topology_revision: int,
        blocker_codes: tuple[str, ...],
    ) -> "AgentRoutingTopologyReadiness":
        """Return an authoritative but unsatisfied topology input."""

        return cls(
            status=AgentRoutingTopologyReadinessStatus.NOT_READY,
            source=AgentRoutingTopologyReadinessSource.AGENT_TEAM_MASTER,
            topology_id=topology_id,
            topology_revision=topology_revision,
            blocker_codes=blocker_codes,
        )

    @classmethod
    def ready(
        cls,
        *,
        topology_id: str,
        topology_revision: int,
    ) -> "AgentRoutingTopologyReadiness":
        """Return a satisfied topology input from the setup authority."""

        return cls(
            status=AgentRoutingTopologyReadinessStatus.READY,
            source=AgentRoutingTopologyReadinessSource.AGENT_TEAM_MASTER,
            topology_id=topology_id,
            topology_revision=topology_revision,
            blocker_codes=(),
        )

    def as_dict(self) -> dict[str, Any]:
        """Project the bounded input into the public capability status."""

        return {
            "schema_version": self.schema_version,
            "status": self.status.value,
            "source": self.source.value,
            "topology_id": self.topology_id,
            "topology_revision": self.topology_revision,
            "blocker_codes": list(self.blocker_codes),
        }


_topology_readiness_context: ContextVar[
    AgentRoutingTopologyReadiness | None
] = ContextVar(
    "workchord_agent_routing_topology_readiness",
    default=None,
)


def set_agent_routing_topology_readiness(
    readiness: AgentRoutingTopologyReadiness,
) -> Token[AgentRoutingTopologyReadiness | None]:
    """Inject server-derived readiness for the current request/task context."""

    return _topology_readiness_context.set(readiness)


def reset_agent_routing_topology_readiness(
    token: Token[AgentRoutingTopologyReadiness | None],
) -> None:
    """Restore the prior request/task readiness input."""

    _topology_readiness_context.reset(token)


@dataclass(frozen=True)
class AgentRoutingRolloutStatus:
    """Effective server state after applying fail-closed readiness controls."""

    configured_mode: AgentRoutingRolloutMode
    effective_mode: AgentRoutingRolloutMode
    feature_advertised: bool
    blocker_codes: tuple[str, ...]
    topology_readiness: AgentRoutingTopologyReadiness

    def as_dict(self) -> dict[str, Any]:
        """Return the secret-free REST/MCP capability projection."""

        return {
            "configured_mode": self.configured_mode.value,
            "effective_mode": self.effective_mode.value,
            "feature_advertised": self.feature_advertised,
            "blocker_codes": list(self.blocker_codes),
            "topology_readiness": self.topology_readiness.as_dict(),
        }


class AgentRoutingRolloutError(RuntimeError):
    """Typed guard failure for preview or enforced dispatch."""

    def __init__(self, code: str, status: AgentRoutingRolloutStatus):
        self.code = code
        self.status = status
        super().__init__(code)


class AgentRoutingRolloutService:
    """Resolve deployment mode against authoritative topology readiness."""

    def __init__(
        self,
        *,
        settings_override: Any | None = None,
        topology_readiness: AgentRoutingTopologyReadiness | None = None,
    ):
        self.settings = settings_override or get_settings()
        self.topology_readiness = (
            topology_readiness
            or _topology_readiness_context.get()
            or AgentRoutingTopologyReadiness.unavailable()
        )

    def status(self) -> AgentRoutingRolloutStatus:
        """Return the effective mode, failing closed until topology is ready."""

        configured = AgentRoutingRolloutMode(
            self.settings.model_aware_routing_mode
        )
        readiness = self.topology_readiness
        if configured == AgentRoutingRolloutMode.OFF:
            return AgentRoutingRolloutStatus(
                configured_mode=configured,
                effective_mode=AgentRoutingRolloutMode.OFF,
                feature_advertised=False,
                blocker_codes=("model_aware_routing_disabled",),
                topology_readiness=readiness,
            )
        if readiness.status != AgentRoutingTopologyReadinessStatus.READY:
            return AgentRoutingRolloutStatus(
                configured_mode=configured,
                effective_mode=AgentRoutingRolloutMode.OFF,
                feature_advertised=False,
                blocker_codes=("model_aware_routing_topology_not_ready",),
                topology_readiness=readiness,
            )
        return AgentRoutingRolloutStatus(
            configured_mode=configured,
            effective_mode=configured,
            feature_advertised=True,
            blocker_codes=(),
            topology_readiness=readiness,
        )

    def require_preview(self) -> AgentRoutingRolloutStatus:
        """Permit model-aware previews only in effective shadow/enforced modes."""

        status = self.status()
        if status.effective_mode == AgentRoutingRolloutMode.OFF:
            raise AgentRoutingRolloutError(
                "model_aware_routing_preview_unavailable",
                status,
            )
        return status

    def require_enforced_dispatch(self) -> AgentRoutingRolloutStatus:
        """Permit enforced dispatch only in the effective enforced mode."""

        status = self.status()
        if status.effective_mode == AgentRoutingRolloutMode.SHADOW:
            raise AgentRoutingRolloutError(
                "model_aware_routing_shadow_only",
                status,
            )
        if status.effective_mode != AgentRoutingRolloutMode.ENFORCED:
            raise AgentRoutingRolloutError(
                "model_aware_routing_enforcement_unavailable",
                status,
            )
        return status

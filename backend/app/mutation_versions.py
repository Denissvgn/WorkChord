"""Server-controlled version rollout with explicit offline repair separation."""

from app.config import get_settings
from app.runtime_telemetry import metrics


class MissingMutationRevision(RuntimeError):
    """A supported command omitted its optimistic input revision."""

    def __init__(self, field: str, resource: str, resource_id: int):
        self.field, self.resource, self.resource_id = field, resource, resource_id
        super().__init__("Reload the current resource and resend the command with its observed revision. Upgrade clients that cannot supply this field.")

    def detail(self):
        return {"code": "mutation_revision_required", "field": self.field,
                "resource": self.resource, "resource_id": self.resource_id,
                "message": str(self), "capabilities": f"{get_settings().api_prefix}/tasks/capabilities"}


def require_mutation_revision(db, value, *, field: str, resource: str, resource_id: int):
    """Keep missing inputs observable; ordinary operators receive no bypass."""
    if value is not None:
        return
    command = db.info.get("command")
    observation = (field, resource, resource_id)
    if command is None or observation not in command.missing_revision_observations:
        metrics.increment("workchord_missing_mutation_revision_total", labels={"field": field})
        if command is not None:
            command.missing_revision_observations.add(observation)
    settings = get_settings()
    if not settings.strict_mutation_versions:
        return
    if settings.database_process_role in {"migration", "repair"}:
        # Web startup rejects these process roles; no request or actor field can
        # select them. Dedicated offline commands retain their own authorization.
        metrics.increment("workchord_offline_version_repairs_total", labels={"role": settings.database_process_role})
        return
    if command is not None and command.mode == "preview":
        return
    raise MissingMutationRevision(field, resource, resource_id)

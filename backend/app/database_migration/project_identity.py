"""Read-only project identity qualification and retained allocation floors."""

from datetime import UTC, datetime
import json

from sqlalchemy import MetaData, String, Table, cast, func, inspect, select, text


class ProjectIdentityError(RuntimeError):
    """Refuse an ambiguous identity without changing historical associations."""

    def __init__(self, code, diagnostics=(), *, truncated=False):
        self.code = code
        self.diagnostics = list(diagnostics)[:100]
        self.truncated = truncated or len(diagnostics) > 100
        super().__init__(json.dumps(self.detail(), sort_keys=True))

    def detail(self):
        return {"code": self.code, "diagnostics": self.diagnostics,
                "truncated": self.truncated, "data_changed": False}


def _utc(value):
    if value is None:
        return None
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
    if not isinstance(value, datetime):
        return None
    return value.replace(tzinfo=UTC) if value.tzinfo is None else value.astimezone(UTC)


def _project_ids(value):
    pending = [value]
    while pending:
        item = pending.pop()
        if isinstance(item, list):
            pending.extend(item)
        elif isinstance(item, dict):
            for key, child in item.items():
                if key.endswith("project_id") and isinstance(child, int) and not isinstance(child, bool):
                    yield child
                if key == "project" and isinstance(child, dict) and isinstance(child.get("id"), int) and not isinstance(child["id"], bool):
                    yield child["id"]
                if isinstance(child, (list, dict)):
                    pending.append(child)


def inspect_project_identity(connection, *, max_history_rows=10000, max_history_bytes=256 * 1024 * 1024):
    """Bound diagnostics and historical JSON scans; never inspect private text fields."""
    inspector = inspect(connection)
    names = set(inspector.get_table_names())
    if "projects" not in names:
        return {"allocation_floor": 0, "history_rows_checked": 0, "diagnostics": []}
    metadata = MetaData()
    tables = {}

    def table(name):
        if name not in tables:
            tables[name] = Table(name, metadata, autoload_with=connection)
        return tables[name]

    projects = table("projects")
    floor = int(connection.scalar(select(func.max(projects.c.id))) or 0)
    diagnostics = []
    checked = total_bytes = 0
    creation_cache = {}
    for name in sorted(names - {"sqlite_sequence", "alembic_version"}):
        columns = {c["name"] for c in inspector.get_columns(name)}
        for column in sorted(columns & {"project_id", "original_project_id", "project_hint_id", "suggested_project_id"}):
            maximum = connection.scalar(select(func.max(table(name).c[column])))
            floor = max(floor, int(maximum or 0))
    for name, column, timestamp in [
        ("time_entries", "project_id", "created_at"),
        ("time_entry_revisions", "project_id", "created_at"),
        ("delivery_observations", "original_project_id", "observed_at"),
        ("execution_usage_records", "original_project_id", "reported_at"),
    ]:
        if name not in names:
            continue
        history = table(name)
        if timestamp not in history.c or "created_at" not in projects.c:
            raise ProjectIdentityError("project_history_schema_incompatible", [{"table": name}])
        query = select(history.c.id, history.c[column], cast(history.c[timestamp], String), cast(projects.c.created_at, String)).join(
            projects, history.c[column] == projects.c.id).order_by(history.c.id).limit(max_history_rows + 1)
        for row in connection.execute(query):
            checked += 1
            if checked > max_history_rows:
                raise ProjectIdentityError("project_history_scan_limit", [{"table": name}], truncated=True)
            observed, created = _utc(row[2]), _utc(row[3])
            if observed is None or created is None or observed < created:
                diagnostics.append({"table": name, "record_id": row[0], "project_id": row[1],
                                    "reason": "retained_history_predates_current_identity"})
    if {"time_entries", "time_entry_revisions"} <= names:
        entries, revisions = table("time_entries"), table("time_entry_revisions")
        query = select(revisions.c.id, revisions.c.project_id).outerjoin(entries, revisions.c.entry_id == entries.c.id).join(
            projects, revisions.c.project_id == projects.c.id).where(
                entries.c.id.is_(None) | (entries.c.project_id != revisions.c.project_id)).limit(101)
        diagnostics.extend({"table": "time_entry_revisions", "record_id": row[0], "project_id": row[1],
                            "reason": "recording_scope_provenance_incomplete"} for row in connection.execute(query))
    if "outbound_webhook_events" in names:
        events = table("outbound_webhook_events")
        floor = max(floor, int(connection.scalar(select(func.max(events.c.entity_id)).where(events.c.entity_type == "project")) or 0))
        query = select(events.c.id, events.c.entity_id).join(projects, projects.c.id == events.c.entity_id).where(
            events.c.entity_type == "project", events.c.event_type == "project.deleted").limit(101)
        diagnostics.extend({"table": "outbound_webhook_events", "record_id": row[0], "project_id": row[1],
                            "reason": "deleted_identity_is_live"} for row in connection.execute(query))
    if diagnostics:
        raise ProjectIdentityError("project_identity_ambiguous", diagnostics)

    for name, column, timestamp in [
        ("application_snapshots", "payload", "created_at"),
        ("command_audit", "details", "created_at"),
        ("outbound_webhook_events", "payload_json", "occurred_at"),
        ("task_events", "payload", "created_at"),
        ("agent_run_events", "payload", "created_at"),
        ("agent_runs", "run_metadata", None),
        ("agent_idempotency_records", "response_payload", "created_at"),
    ]:
        if name not in names or column not in table(name).c:
            continue
        history = table(name)
        selected = [history.c.id, func.length(cast(history.c[column], String))]
        if timestamp and timestamp in history.c:
            selected.append(history.c[timestamp])
        if name == "command_audit":
            selected.append(history.c.action)
        query = select(*selected).order_by(history.c.id).execution_options(stream_results=True)
        for row in connection.execute(query):
            checked += 1
            total_bytes += int(row[1] or 0)
            if checked > max_history_rows or total_bytes > max_history_bytes or int(row[1] or 0) > 16 * 1024 * 1024:
                raise ProjectIdentityError("project_history_scan_limit", [{"table": name, "record_id": row[0]}], truncated=True)
            try:
                value = connection.scalar(select(history.c[column]).where(history.c.id == row[0]))
                encoded = value if isinstance(value, str) else json.dumps(value)
                payload = json.loads(encoded)
            except (ValueError, TypeError):
                raise ProjectIdentityError("project_history_invalid", [{"table": name, "record_id": row[0]}]) from None
            ids = set(_project_ids(payload))
            if name == "command_audit" and row[-1].startswith("projects:") and isinstance(payload, dict):
                value = payload.get("entity_id")
                if isinstance(value, int) and not isinstance(value, bool):
                    ids.add(value)
            for project_id in ids:
                floor = max(floor, project_id)
                if project_id not in creation_cache:
                    creation_cache[project_id] = connection.scalar(select(projects.c.created_at).where(projects.c.id == project_id))
                created = creation_cache[project_id]
                observed = _utc(row[2]) if timestamp and timestamp in history.c else None
                if created is not None and observed is not None and _utc(created) is not None and observed < _utc(created):
                    diagnostics.append({"table": name, "record_id": row[0], "project_id": project_id,
                                        "reason": "retained_history_predates_current_identity"})
                    if len(diagnostics) > 100:
                        raise ProjectIdentityError("project_identity_ambiguous", diagnostics, truncated=True)
    if diagnostics:
        raise ProjectIdentityError("project_identity_ambiguous", diagnostics)
    if connection.dialect.name == "sqlite" and connection.scalar(text("SELECT 1 FROM sqlite_master WHERE name='sqlite_sequence'")):
        floor = max(floor, int(connection.scalar(text("SELECT seq FROM sqlite_sequence WHERE name='projects'")) or 0))
    return {"allocation_floor": floor, "history_rows_checked": checked, "diagnostics": []}


def project_allocation_floor(connection):
    """Require identity qualification before returning a safe allocation floor."""
    return inspect_project_identity(connection)["allocation_floor"]

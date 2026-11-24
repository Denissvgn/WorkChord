"""Read-only project identity qualification and retained allocation floors."""

from datetime import UTC, datetime
import json
import sqlite3
from urllib.parse import quote

from sqlalchemy import JSON, MetaData, String, Table, cast, create_engine, func, inspect, select, text
from sqlalchemy.pool import NullPool

# The scan reads every retained history row. These bound what it holds at once, not
# how much it reads: rows per keyset page, and encoded JSON characters per value fetch.
HISTORY_PAGE_ROWS = 1000
HISTORY_BATCH_CHARACTERS = 32 * 1024 * 1024
# One retained JSON value larger than this is refused instead of being loaded.
HISTORY_VALUE_CHARACTERS = 16 * 1024 * 1024


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


def _pages(connection, history, columns, *, page_rows, joined=None):
    """Yield one history table's rows in id order, a bounded keyset page at a time."""
    last = None
    while True:
        query = select(history.c.id, *columns)
        if joined is not None:
            query = query.select_from(joined)
        if last is not None:
            query = query.where(history.c.id > last)
        rows = connection.execute(query.order_by(history.c.id).limit(page_rows)).all()
        if rows:
            yield rows
        if len(rows) < page_rows:
            return
        last = rows[-1][0]


def decode_history_value(column, value):
    """Decode one encoded value from ``history_values`` the way the checks have always read it.

    A JSON column whose stored value is itself a JSON string holds an encoded payload, so
    that string is decoded once more. Text columns are decoded once. Raises ``ValueError``
    or ``TypeError`` when either decode fails.
    """
    if value is None:
        return None
    payload = json.loads(value)
    if isinstance(payload, str) and isinstance(column.type, JSON):
        payload = json.loads(payload)
    return payload


def history_values(connection, history, column, columns=(), *, admit, page_rows=HISTORY_PAGE_ROWS):
    """Yield ``(row, encoded value)`` for every row of one history table, in id order.

    ``row`` is ``(id, encoded length, *columns)``. ``admit(row, length)`` sees each row before
    its value is loaded and raises to refuse it. Rows are read in keyset pages and values in
    batches of at most ``HISTORY_BATCH_CHARACTERS``, so memory never grows with the history.
    """
    encoded = cast(history.c[column], String)

    def load(batch):
        values = dict(connection.execute(select(history.c.id, encoded).where(
            history.c.id >= batch[0][0], history.c.id <= batch[-1][0])).all())
        return [(row, values.get(row[0])) for row in batch]

    for rows in _pages(connection, history, [func.length(encoded), *columns], page_rows=page_rows):
        batch, characters = [], 0
        for row in rows:
            size = int(row[1] or 0)
            admit(row, size)
            if batch and characters + size > HISTORY_BATCH_CHARACTERS:
                yield from load(batch)
                batch, characters = [], 0
            batch.append(row)
            characters += size
        if batch:
            yield from load(batch)


def inspect_project_identity(connection, *, max_history_rows=None, max_history_bytes=None,
                             page_rows=HISTORY_PAGE_ROWS):
    """Check every retained history row in bounded pages; never inspect private text fields.

    The scan is complete however much history a deployment retains, and its memory does
    not grow with that history. ``max_history_rows`` and ``max_history_bytes`` are optional
    caller limits that refuse with ``project_history_scan_limit`` once exceeded.
    """
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

    def count(name, record_id, size=0):
        nonlocal checked, total_bytes
        checked += 1
        total_bytes += size
        if (max_history_rows is not None and checked > max_history_rows) or (
                max_history_bytes is not None and total_bytes > max_history_bytes):
            raise ProjectIdentityError("project_history_scan_limit", [{"table": name, "record_id": record_id}],
                                       truncated=True)

    def report(diagnostic):
        diagnostics.append(diagnostic)
        if len(diagnostics) > 100:
            raise ProjectIdentityError("project_identity_ambiguous", diagnostics, truncated=True)

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
        selected = [history.c[column], cast(history.c[timestamp], String), cast(projects.c.created_at, String)]
        joined = history.join(projects, history.c[column] == projects.c.id)
        for rows in _pages(connection, history, selected, page_rows=page_rows, joined=joined):
            for row in rows:
                count(name, row[0])
                observed, created = _utc(row[2]), _utc(row[3])
                if observed is None or created is None or observed < created:
                    report({"table": name, "record_id": row[0], "project_id": row[1],
                            "reason": "retained_history_predates_current_identity"})
    if {"time_entries", "time_entry_revisions"} <= names:
        entries, revisions = table("time_entries"), table("time_entry_revisions")
        query = select(revisions.c.id, revisions.c.project_id).outerjoin(entries, revisions.c.entry_id == entries.c.id).join(
            projects, revisions.c.project_id == projects.c.id).where(
                entries.c.id.is_(None) | (entries.c.project_id != revisions.c.project_id)).limit(101)
        for row in connection.execute(query):
            report({"table": "time_entry_revisions", "record_id": row[0], "project_id": row[1],
                    "reason": "recording_scope_provenance_incomplete"})
    if "outbound_webhook_events" in names:
        events = table("outbound_webhook_events")
        floor = max(floor, int(connection.scalar(select(func.max(events.c.entity_id)).where(events.c.entity_type == "project")) or 0))
        query = select(events.c.id, events.c.entity_id).join(projects, projects.c.id == events.c.entity_id).where(
            events.c.entity_type == "project", events.c.event_type == "project.deleted").limit(101)
        for row in connection.execute(query):
            report({"table": "outbound_webhook_events", "record_id": row[0], "project_id": row[1],
                    "reason": "deleted_identity_is_live"})
    if diagnostics:
        raise ProjectIdentityError("project_identity_ambiguous", diagnostics)

    # Creation times are the only per-identity state the JSON checks need, so what the
    # scan keeps grows with the number of projects, never with the retained history.
    created_at = {row[0]: _utc(row[1]) for row in connection.execute(select(projects.c.id, projects.c.created_at))}
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
        stamped = bool(timestamp) and timestamp in history.c
        selected = []
        if stamped:
            selected.append(history.c[timestamp])
        if name == "command_audit":
            selected.append(history.c.action)

        def admit(row, size, name=name):
            count(name, row[0], size)
            if size > HISTORY_VALUE_CHARACTERS:
                raise ProjectIdentityError("project_history_scan_limit", [{"table": name, "record_id": row[0]}],
                                           truncated=True)

        for row, value in history_values(connection, history, column, selected, admit=admit, page_rows=page_rows):
            try:
                payload = decode_history_value(history.c[column], value)
            except (ValueError, TypeError):
                raise ProjectIdentityError("project_history_invalid", [{"table": name, "record_id": row[0]}]) from None
            ids = set(_project_ids(payload))
            if name == "command_audit" and row[-1].startswith("projects:") and isinstance(payload, dict):
                entity = payload.get("entity_id")
                if isinstance(entity, int) and not isinstance(entity, bool):
                    ids.add(entity)
            observed = _utc(row[2]) if stamped else None
            for project_id in ids:
                floor = max(floor, project_id)
                created = created_at.get(project_id)
                if created is not None and observed is not None and observed < created:
                    report({"table": name, "record_id": row[0], "project_id": project_id,
                            "reason": "retained_history_predates_current_identity"})
    if diagnostics:
        raise ProjectIdentityError("project_identity_ambiguous", diagnostics)
    if connection.dialect.name == "sqlite" and connection.scalar(text("SELECT 1 FROM sqlite_master WHERE name='sqlite_sequence'")):
        floor = max(floor, int(connection.scalar(text("SELECT seq FROM sqlite_sequence WHERE name='projects'")) or 0))
    return {"allocation_floor": floor, "history_rows_checked": checked, "diagnostics": []}


def project_allocation_floor(connection):
    """Require identity qualification before returning a safe allocation floor."""
    return inspect_project_identity(connection)["allocation_floor"]


def sqlite_project_allocation_floor(path):
    """Qualify one immutable SQLite source through a separately owned read-only handle."""
    uri = f"file:{quote(str(path.resolve(strict=True)), safe='/')}?mode=ro"
    engine = create_engine("sqlite://", creator=lambda: sqlite3.connect(uri, uri=True), poolclass=NullPool)
    try:
        with engine.connect() as connection:
            connection.exec_driver_sql("PRAGMA query_only=ON")
            return project_allocation_floor(connection)
    finally:
        engine.dispose()

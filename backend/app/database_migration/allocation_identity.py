"""Reserve numeric allocation identities retained by immutable recovery history."""

import json

from sqlalchemy import MetaData, Table, cast, String, func, inspect, select, text


def allocation_floor(connection):
    inspector = inspect(connection)
    metadata = MetaData()
    members = Table("team_members", metadata, autoload_with=connection)
    floor = int(connection.scalar(select(func.max(members.c.id))) or 0)
    for name in inspector.get_table_names():
        for foreign in inspector.get_foreign_keys(name):
            if foreign["referred_table"] == "team_members":
                table = Table(name, metadata, autoload_with=connection, extend_existing=True)
                for column in foreign["constrained_columns"]:
                    floor = max(floor, int(connection.scalar(select(func.max(table.c[column]))) or 0))
    scanned_rows = scanned_bytes = 0
    surfaces = [("application_snapshots", "payload"), ("command_audit", "details"),
                ("task_events", "payload"), ("agent_run_events", "payload"),
                ("agent_runs", "run_metadata"), ("agent_idempotency_records", "response_payload")]
    for name, column in surfaces:
        if name not in inspector.get_table_names():continue
        table = Table(name, metadata, autoload_with=connection, extend_existing=True)
        if column not in table.c:continue
        rows = connection.execute(select(table.c.id, func.length(cast(table.c[column], String))).order_by(table.c.id).execution_options(stream_results=True))
        for identifier, size in rows:
            scanned_rows += 1
            scanned_bytes += int(size or 0)
            if scanned_rows > 10000 or scanned_bytes > 256 * 1024 * 1024 or int(size or 0) > 16 * 1024 * 1024:
                raise RuntimeError("Allocation recovery history exceeds the bounded identity scan")
            payload = connection.scalar(select(table.c[column]).where(table.c.id == identifier))
            payload = json.loads(payload) if isinstance(payload, str) else payload
            if payload is None:continue
            if name == "command_audit":
                action = connection.scalar(select(table.c.action).where(table.c.id == identifier))
                if action.startswith("team_members:") and isinstance(payload, dict):
                    value = payload.get("entity_id")
                    if type(value) is int and value > 0:floor = max(floor, value)
            pending = [payload]
            while pending:
                item = pending.pop()
                if isinstance(item, list):pending.extend(item)
                elif isinstance(item, dict):
                    for key, value in item.items():
                        if key in {"assignee_id", "team_member_id", "allocation_id", "owner_id", "suggested_assignee_id"} and type(value) is int and value > 0:
                            floor = max(floor, value)
                        elif key in {"assignee_id", "team_member_id", "allocation_id", "owner_id", "suggested_assignee_id"} and isinstance(value, dict):
                            for retained in value.values():
                                if type(retained) is int and retained > 0:floor = max(floor, retained)
                        if key == "team_members" and isinstance(value, list):
                            for member in value:
                                identifier = member.get("id") if isinstance(member, dict) else None
                                if type(identifier) is not int or identifier < 1:raise RuntimeError("Allocation recovery identity is invalid")
                                floor = max(floor, identifier)
                        if isinstance(value, (dict, list)):pending.append(value)
    if connection.dialect.name == "sqlite" and connection.scalar(text("SELECT 1 FROM sqlite_master WHERE name='sqlite_sequence'")):
        floor = max(floor, int(connection.scalar(text("SELECT seq FROM sqlite_sequence WHERE name='team_members'")) or 0))
    return floor

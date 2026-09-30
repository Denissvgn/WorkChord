"""Explicit persisted-state reads after rollback in multi-command scenarios."""

from sqlalchemy import inspect


async def reload_session_fixture(db):
    """Reload retained fixture objects instead of triggering async lazy I/O in assertions."""
    for instance in list(db.identity_map.values()):
        state = inspect(instance)
        if not state.persistent or not state.expired_attributes:
            continue
        await db.refresh(instance, attribute_names=[attribute.key for attribute in state.mapper.column_attrs])
        for relationship in ("profile", "model_catalog"):
            if relationship in state.mapper.relationships:
                await db.refresh(instance, attribute_names=[relationship])

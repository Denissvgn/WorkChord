"""Shared finite ID-window reads; the caller supplies its authorized projection."""
from sqlalchemy import select


async def scope_page(db, model, query, *, limit=100, after_id=0, upper_id=None):
    if not 1 <= limit <= 100 or after_id < 0 or upper_id is not None and upper_id < 0:
        raise ValueError("Use a bounded scope page with nonnegative cursors")
    if upper_id is None:
        upper_id = await db.scalar(select(model.id).order_by(model.id.desc()).limit(1)) or 0
    rows = list((await db.scalars(query.where(model.id > after_id, model.id <= upper_id)
        .order_by(model.id).limit(limit + 1))).all())
    more = len(rows) > limit
    return dict(items=rows[:limit], has_more=more, next_after_id=rows[limit-1].id if more else None, upper_id=upper_id)

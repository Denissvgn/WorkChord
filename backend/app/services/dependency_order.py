"""Saved dependency order: dependents whose persisted dates start before their prerequisite ends.

The scheduler places a dependent on the day after its predecessor's end date
(``end_date`` is inclusive), so a saved start on or before that end date breaks
the order. Only planned leaf work is judged: started or finished work carries
actual dates, work that is deferred, canceled or inside a deferred branch is
backlog, and a prerequisite that is already resolved, closed or canceled no
longer constrains anything. Edges to work outside the iteration are ignored.

This module only reads. Correcting the dates is a schedule preview followed by
an explicit apply.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task, TaskDependency, TaskStatus
from app.schemas.iteration import InvertedDependency


async def inverted_saved_dependencies(db: AsyncSession, iteration_id: int) -> list[InvertedDependency]:
    """List the dependency pairs of one iteration whose saved dates are inverted."""
    from app.commands import PlanningConflict
    from app.services.work_metrics import included_work_ids

    try:
        included = await included_work_ids(db, {iteration_id})
    except PlanningConflict:
        # Incomplete work ancestry is reported elsewhere; no pair can be judged safely.
        return []
    # Core table aliases: the id sets already scope the rows to this iteration.
    dependent, prerequisite = Task.__table__.alias("dependent"), Task.__table__.alias("prerequisite")
    link = TaskDependency.__table__
    rows = (await db.execute(
        select(dependent.c.id, dependent.c.title, dependent.c.start_date,
               prerequisite.c.id, prerequisite.c.title, prerequisite.c.end_date)
        .select_from(link)
        .join(dependent, dependent.c.id == link.c.task_id)
        .join(prerequisite, prerequisite.c.id == link.c.depends_on_id)
        .where(
            dependent.c.iteration_id == iteration_id,
            prerequisite.c.iteration_id == iteration_id,
            dependent.c.id.in_(included),
            prerequisite.c.id.in_(included),
            dependent.c.status == TaskStatus.PLANNED.value,
            prerequisite.c.status.in_([TaskStatus.PLANNED.value, TaskStatus.ACTIVE.value]),
            dependent.c.start_date.is_not(None),
            prerequisite.c.end_date.is_not(None),
            dependent.c.start_date <= prerequisite.c.end_date,
        )
        .order_by(dependent.c.start_date, dependent.c.id, prerequisite.c.id)
    )).all()
    return [InvertedDependency(task_id=row[0], task_title=row[1], task_start_date=row[2],
                               prerequisite_id=row[3], prerequisite_title=row[4], prerequisite_end_date=row[5])
            for row in rows]

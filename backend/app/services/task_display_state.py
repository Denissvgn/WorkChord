"""The state a task is shown in: its stored status, or the terminal state of withdrawn work.

Canceled work keeps the status it had when it was canceled (the stored column never changes), so any
count or filter that read that status would show it as planned, active or resolved. The displayed
state is derived instead, from ``canceled_at`` and the replacement records:

- ``canceled``: canceled work with no task delivering it instead.
- ``superseded``: canceled work whose deliverable another task carries. A clean replacement is
  labelled superseded too, with the replacement as its successor; ``successor_kind`` tells the two
  dispositions apart (``replacement`` or ``supersession``).

Postponed stays a stored status of its own.
"""

from sqlalchemy import and_, case, exists, select

from app.models.task import TaskStatus

CANCELED, SUPERSEDED = "canceled", "superseded"
TERMINAL_STATES = (CANCELED, SUPERSEDED)
STORED_STATES = tuple(status.value for status in TaskStatus)
DISPLAYED_STATES = (*STORED_STATES, *TERMINAL_STATES)


def validate_state_filter(state):
    """A displayed state a task list can be filtered by."""
    if state not in DISPLAYED_STATES:
        raise ValueError("Select a supported task status: " + ", ".join(DISPLAYED_STATES))
    return state


def withdrawn_by_successor(id_column):
    """SQL: a replacement record names another task as delivering this one's work."""
    from app.models.task_replacement import TaskReplacement
    table = TaskReplacement.__table__
    return exists(select(table.c.id).where(table.c.original_task_id == id_column).correlate_except(table))


def state_clause(state, *, id_column, status_column, canceled_at_column):
    """SQL predicate: the task is shown in this displayed state."""
    validate_state_filter(state)
    if state == CANCELED:
        return and_(canceled_at_column.is_not(None), ~withdrawn_by_successor(id_column))
    if state == SUPERSEDED:
        return and_(canceled_at_column.is_not(None), withdrawn_by_successor(id_column))
    return and_(canceled_at_column.is_(None), status_column == state)


def displayed_state_expression(*, id_column, status_column, canceled_at_column):
    """SQL expression of the displayed state, for lists that show it beside the stored status."""
    return case((canceled_at_column.is_(None), status_column),
                (withdrawn_by_successor(id_column), SUPERSEDED), else_=CANCELED)


def task_state_clause(state):
    """The state predicate for a query over the Task entity."""
    from app.models.task import Task
    return state_clause(state, id_column=Task.id, status_column=Task.status, canceled_at_column=Task.canceled_at)

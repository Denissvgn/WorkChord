"""DBM-PERF-001 bounded graph and aggregate-summary tests."""

from __future__ import annotations

from datetime import date
from typing import Any

import pytest
from sqlalchemy import event, insert
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from app.models.calendar import Calendar
from app.models.iteration import Iteration
from app.models.project import Project
from app.models.task import Task
from app.query_limits import CollectionLimitExceededError
from app.services.iteration_service import IterationService
from app.services.project_service import ProjectService
from app.services.task_service import TaskService


async def _workspace_seed(
    db: AsyncSession,
    *,
    project_count: int = 1,
) -> tuple[int, int]:
    calendar = Calendar(name="Boundary calendar", year=2026)
    db.add(calendar)
    await db.flush()
    projects = [Project(name=f"Project {index}") for index in range(project_count)]
    db.add_all(projects)
    await db.flush()
    iteration = Iteration(
        name="Boundary iteration",
        start_date=date(2026, 1, 1),
        end_date=date(2026, 1, 14),
        calendar_id=calendar.id,
        project_id=projects[0].id,
    )
    db.add(iteration)
    await db.commit()
    return projects[0].id, iteration.id


async def _insert_tasks(
    db: AsyncSession,
    *,
    iteration_id: int,
    project_id: int,
    start: int,
    count: int,
) -> None:
    await db.execute(
        insert(Task),
        [
            {
                "title": f"Boundary task {index}",
                "iteration_id": iteration_id,
                "project_id": project_id,
                "sort_order": index,
            }
            for index in range(start, start + count)
        ],
    )
    await db.commit()


@pytest.mark.sqlite
@pytest.mark.asyncio
async def test_iteration_tree_refuses_max_plus_one_without_truncation(
    db_session: AsyncSession,
) -> None:
    project_id, iteration_id = await _workspace_seed(db_session)
    await _insert_tasks(
        db_session,
        iteration_id=iteration_id,
        project_id=project_id,
        start=0,
        count=4,
    )

    with pytest.raises(CollectionLimitExceededError) as error:
        await TaskService(db_session).get_by_iteration(iteration_id, max_tasks=3)

    assert error.value.maximum == 3
    assert error.value.detail()["code"] == "collection_limit_exceeded"


@pytest.mark.sqlite
@pytest.mark.asyncio
async def test_project_tree_and_list_refuse_max_plus_one(
    db_session: AsyncSession,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("app.services.project_service.MAX_PROJECT_TREE_TASKS", 3)
    monkeypatch.setattr("app.services.project_service.MAX_PROJECT_LIST_ITEMS", 3)
    project_id, iteration_id = await _workspace_seed(db_session, project_count=4)
    await _insert_tasks(
        db_session,
        iteration_id=iteration_id,
        project_id=project_id,
        start=0,
        count=4,
    )

    service = ProjectService(db_session)
    with pytest.raises(CollectionLimitExceededError, match="project list"):
        await service.list_projects()
    with pytest.raises(CollectionLimitExceededError, match="project task tree"):
        await service.get_tasks(project_id)


@pytest.mark.sqlite
@pytest.mark.asyncio
async def test_iteration_list_uses_stable_explicit_keyset_pages(
    db_session: AsyncSession,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("app.services.iteration_service.MAX_ITERATION_LIST_ITEMS", 3)
    project_id, first_iteration_id = await _workspace_seed(db_session)
    first = await db_session.get(Iteration, first_iteration_id)
    assert first is not None
    db_session.add_all(
        [
            Iteration(
                name=f"Boundary iteration {index}",
                start_date=first.start_date,
                end_date=first.end_date,
                calendar_id=first.calendar_id,
                project_id=project_id,
            )
            for index in range(1, 4)
        ]
    )
    await db_session.commit()

    service = IterationService(db_session)
    with pytest.raises(CollectionLimitExceededError, match="iteration list"):
        await service.get_all()

    first_page = list(await service.get_page(limit=2))
    second_page = list(
        await service.get_page(
            limit=2,
            cursor_start_date=first_page[-1].start_date,
            cursor_id=first_page[-1].id,
        )
    )

    ids = [iteration.id for iteration in [*first_page, *second_page]]
    assert len(ids) == 4
    assert len(set(ids)) == 4
    assert ids == sorted(ids, reverse=True)


@pytest.mark.sqlite
@pytest.mark.asyncio
async def test_iteration_summary_aggregates_without_loading_task_objects(
    db_session: AsyncSession,
) -> None:
    project_id, iteration_id = await _workspace_seed(db_session)
    await _insert_tasks(
        db_session,
        iteration_id=iteration_id,
        project_id=project_id,
        start=0,
        count=100,
    )
    db_session.expunge_all()

    summary = await IterationService(db_session).get_summary(iteration_id)

    assert summary is not None
    assert summary.total_tasks == 100
    assert not any(isinstance(value, Task) for value in db_session.identity_map.values())


async def _summary_query_count(
    factory: async_sessionmaker[AsyncSession],
    engine: AsyncEngine,
    project_id: int,
) -> tuple[int, int, bool]:
    query_count = 0

    def count_query(*_args: Any) -> None:
        nonlocal query_count
        query_count += 1

    event.listen(engine.sync_engine, "before_cursor_execute", count_query)
    try:
        async with factory() as db:
            summary = await ProjectService(db).get_summary(project_id)
            assert summary is not None
            loaded_task = any(isinstance(value, Task) for value in db.identity_map.values())
            return query_count, summary.total_tasks, loaded_task
    finally:
        event.remove(engine.sync_engine, "before_cursor_execute", count_query)


@pytest.mark.sqlite
@pytest.mark.asyncio
async def test_project_summary_query_count_and_identity_map_are_cardinality_constant(
    db_session_factory: async_sessionmaker[AsyncSession],
    sqlite_engine: AsyncEngine,
) -> None:
    async with db_session_factory() as db:
        project_id, iteration_id = await _workspace_seed(db)
        await _insert_tasks(
            db,
            iteration_id=iteration_id,
            project_id=project_id,
            start=0,
            count=1,
        )

    small_queries, small_total, small_loaded_tasks = await _summary_query_count(
        db_session_factory,
        sqlite_engine,
        project_id,
    )

    async with db_session_factory() as db:
        await _insert_tasks(
            db,
            iteration_id=iteration_id,
            project_id=project_id,
            start=1,
            count=100,
        )

    large_queries, large_total, large_loaded_tasks = await _summary_query_count(
        db_session_factory,
        sqlite_engine,
        project_id,
    )

    assert small_total == 1
    assert large_total == 101
    assert large_queries == small_queries
    assert large_queries <= 12
    assert small_loaded_tasks is False
    assert large_loaded_tasks is False

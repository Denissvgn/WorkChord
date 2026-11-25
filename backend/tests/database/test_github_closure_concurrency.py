"""A GitHub merge or closure observed by racing catch-ups and webhooks is recorded once on PostgreSQL."""

from __future__ import annotations

import asyncio
from datetime import date

import httpx
import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.authority import Authority
from app.config import get_settings
from app.database_config import parse_database_configuration
from app.models.agent import TaskEvent
from app.models.calendar import Calendar
from app.models.external_link import ExternalLink
from app.models.iteration import Iteration
from app.models.project import Project
from app.models.task import Task
from app.services.external_link_service import ExternalLinkService
from app.services.github_status_service import GitHubStatusService
from app.services.github_webhook_service import GitHubWebhookService
from app.services.upgrade_service import bootstrap_database_schema
from tests.support import AsyncBarrier

REPO = "https://github.com/example/project"
HEAD = "a" * 40
MERGE = "c" * 40
CLOSED_AT = "2026-07-01T12:00:00Z"

pytestmark = [pytest.mark.postgresql, pytest.mark.integration, pytest.mark.allow_network, pytest.mark.asyncio]


@pytest_asyncio.fixture
async def factory(postgres_database, configure_database) -> async_sessionmaker[AsyncSession]:
    configure_database(postgres_database.url)
    bootstrap_database_schema()
    configuration = parse_database_configuration(get_settings())
    options = configuration.async_engine_kwargs()
    options.update(pool_size=6, max_overflow=0)
    engine: AsyncEngine = create_async_engine(configuration.async_url, **options)
    try:
        yield async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    finally:
        await engine.dispose()
        get_settings.cache_clear()


def _pull(number: int, *, merged: bool) -> dict:
    return {
        "number": number, "title": "Add export", "state": "closed", "draft": False, "merged": merged,
        "merged_at": CLOSED_AT if merged else None, "closed_at": CLOSED_AT, "updated_at": CLOSED_AT,
        "merge_commit_sha": MERGE, "head": {"sha": HEAD, "ref": "feature"}, "base": {"ref": "main"},
    }


def _session(factory, project_id: int) -> AsyncSession:
    db = factory()
    db.info["authority"] = Authority(None, "human", projects={project_id: "manager"})
    return db


async def _seed(factory, number: int) -> tuple[int, int, int]:
    """An open pull request linked to a task, as the last observation left it."""
    async with factory() as db:
        project = Project(name=f"Race project {number}")
        calendar = Calendar(name=f"Race calendar {number}", year=2026)
        db.add_all([project, calendar])
        await db.flush()
        iteration = Iteration(name=f"Race iteration {number}", start_date=date(2026, 7, 1),
                              end_date=date(2026, 7, 14), calendar_id=calendar.id, project_id=project.id)
        db.add(iteration)
        await db.flush()
        task = Task(title=f"Race task {number}", iteration_id=iteration.id, project_id=project.id)
        db.add(task)
        await db.flush()
        db.info["authority"] = Authority(None, "human", projects={project.id: "manager"})
        link = await ExternalLinkService(db).create_task_github_link(task.id, f"{REPO}/pull/{number}", commit=False)
        link.status = "open"
        await db.commit()
        return project.id, task.id, link.id


def _transport(pull: dict, barrier: AsyncBarrier) -> httpx.MockTransport:
    async def respond(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/check-runs"):
            # Every racer has fetched the pull request and read nothing locked yet.
            await barrier.wait()
            return httpx.Response(200, json={"total_count": 0, "check_runs": []})
        return httpx.Response(200, json=pull)

    return httpx.MockTransport(respond)


async def _catch_up(factory, project_id: int, link_id: int, pull: dict, barrier: AsyncBarrier) -> None:
    async with _session(factory, project_id) as db:
        service = GitHubStatusService(db, transport=_transport(pull, barrier))
        await service.refresh_pull_request_status(link_id)


async def _webhook(factory, project_id: int, pull: dict, barrier: AsyncBarrier, delivery_id: str) -> None:
    async with _session(factory, project_id) as db:
        settings = get_settings().model_copy(update={"github_webhook_secret": "s"})
        hook = GitHubWebhookService(db, settings_override=settings)
        await barrier.wait()
        await hook.process("pull_request", delivery_id, {
            "action": "closed", "pull_request": pull, "repository": {"full_name": "example/project"},
            "sender": {"login": "octo"},
        })


async def _closure_events(factory, task_id: int) -> list[str]:
    async with factory() as db:
        rows = await db.scalars(select(TaskEvent.event_type).where(
            TaskEvent.task_id == task_id, TaskEvent.event_type.in_(["github_pr_merged", "github_pr_closed"])))
        return list(rows.all())


@pytest.mark.parametrize("merged", [True, False], ids=["merge", "unmerged-closure"])
async def test_two_racing_catch_ups_record_the_closure_once(factory, merged) -> None:
    for round_number in range(3):
        project_id, task_id, link_id = await _seed(factory, 100 + round_number)
        pull = _pull(100 + round_number, merged=merged)
        barrier = AsyncBarrier(2)
        await asyncio.gather(
            _catch_up(factory, project_id, link_id, pull, barrier),
            _catch_up(factory, project_id, link_id, pull, barrier),
        )
        expected = "github_pr_merged" if merged else "github_pr_closed"
        assert await _closure_events(factory, task_id) == [expected]
        async with factory() as db:
            assert (await db.get(ExternalLink, link_id)).status == ("merged" if merged else "closed")


@pytest.mark.parametrize("merged", [True, False], ids=["merge", "unmerged-closure"])
async def test_a_catch_up_racing_the_closure_webhook_records_the_closure_once(factory, merged) -> None:
    for round_number in range(4):
        number = 200 + round_number
        project_id, task_id, link_id = await _seed(factory, number)
        pull = _pull(number, merged=merged)
        barrier = AsyncBarrier(2)
        racers = [
            _catch_up(factory, project_id, link_id, pull, barrier),
            _webhook(factory, project_id, pull, barrier, f"delivery-{number}"),
        ]
        # Start either side first so both lock orders are exercised.
        await asyncio.gather(*(racers if round_number % 2 == 0 else reversed(racers)))
        expected = "github_pr_merged" if merged else "github_pr_closed"
        assert await _closure_events(factory, task_id) == [expected]
        async with factory() as db:
            assert (await db.get(ExternalLink, link_id)).status == ("merged" if merged else "closed")
        # A redelivery of the same closure adds nothing either.
        await _webhook(factory, project_id, pull, AsyncBarrier(1), f"delivery-{number}")
        assert await _closure_events(factory, task_id) == [expected]

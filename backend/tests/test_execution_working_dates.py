"""Agent start decisions use the same declared working day as human work."""

from datetime import UTC, date, datetime, timedelta

import httpx
import pytest

from app.main import app
from app.models.agent import AgentActor
from app.models.project import Project
from app.models.task import Task
from app.schemas.task import TaskCreate
from app.schemas.task_domain import TaskActionRequest
from app.services import agent_work_service, backlog_snapshot_service, work_metrics
from app.services.task_domain_service import TaskDomainService
from app.services.task_service import TaskService
from tests.test_agent_runtime_recovery import seed_work
from tests.test_delivery_scenarios import delivery_store


@pytest.mark.parametrize(('zone', 'instant', 'future'), [
    ('Asia/Tokyo', '2026-01-20T23:30:00+00:00', False),
    ('America/Los_Angeles', '2026-01-21T00:30:00+00:00', False),
    ('America/Los_Angeles', '2026-03-08T09:59:00+00:00', False),
    ('America/Los_Angeles', '2026-03-09T06:30:00+00:00', False),
    ('Asia/Tokyo', '2026-01-20T23:30:00+00:00', True),
    ('America/Los_Angeles', '2026-01-21T00:30:00+00:00', True),
    ('America/Los_Angeles', '2026-03-09T06:30:00+00:00', True),
])
async def test_scheduled_agent_start_and_human_dates_reconcile(delivery_store, monkeypatch, zone, instant, future):
    from app.utils import time
    factory, scenario, _ = delivery_store
    now = datetime.fromisoformat(instant)
    local_day = work_metrics.working_today(zone, now)
    # Snapshot filenames retain a progressing clock independently of this working-day fixture.
    monkeypatch.setattr(backlog_snapshot_service, 'utc_now', time.utc_now)

    class ServerDate(date):
        @classmethod
        def today(cls):
            return now.astimezone(UTC).date()

    monkeypatch.setattr(agent_work_service, 'date', ServerDate, raising=False)
    monkeypatch.setattr(agent_work_service, 'utc_now', lambda: now)
    monkeypatch.setattr(work_metrics, 'utc_now', lambda: now)
    monkeypatch.setattr(time, 'utc_now', lambda: now)
    task_id, assignment_id = await seed_work(factory, scenario)
    async with factory() as db:
        project = await db.get(Project, scenario.projects[0])
        project.timezone = zone
        task = await db.get(Task, task_id)
        task.start_date = local_day + timedelta(days=int(future))
        task.end_date = task.start_date + timedelta(days=1)
        await db.commit()
        actor = await db.get(AgentActor, scenario.actors[0])
        body = {'assignment_id': assignment_id, 'queue_revision': actor.queue_revision, 'lease_seconds': 60}
        before = (task.status, task.version, task.claim_generation)
    headers = {'X-Agent-API-Key': scenario.actor_keys[0], 'Idempotency-Key': 'working-day-start'}
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        work = await client.get('/api/agent/me/work', headers=headers)
        assert work.status_code == 200, work.text
        assert work.json()['state'] == ('wait' if future else 'start_assigned'), work.text
        begun = await client.post('/api/agent/me/work/begin', headers=headers, json=body)
        assert begun.status_code == (409 if future else 200), begun.text
    async with factory() as db:
        task = await db.get(Task, task_id)
        if future:
            assert (task.status, task.version, task.claim_generation) == before
        else:
            assert task.status == 'active'
        manual = await TaskService(db).create(None, TaskCreate(title='Manual boundary work', project_id=scenario.projects[0]))
        started = await TaskDomainService(db).command(manual.id, TaskActionRequest(
            action='start_manual', expected_version=manual.version, reason='Start on declared working day'))
        assert started.actual_start_date == local_day

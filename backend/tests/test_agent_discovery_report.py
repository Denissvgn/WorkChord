"""A worker with an accepted assignment can report out-of-scope work to triage, and nothing more."""

from datetime import UTC, date, datetime, timedelta

import httpx
import pytest
from sqlalchemy import select

from app.authority import AuthorityError
from app.main import app
from app.models.agent import AgentActor, TaskEvent
from app.models.project import Project
from app.models.task import Task
from app.models.triage import TriageItem
from app.services import agent_work_service, backlog_snapshot_service, work_metrics
from app.services.identity_service import IdentityService
from tests.test_agent_runtime_recovery import seed_work
from tests.test_delivery_scenarios import delivery_store


ZONE = 'UTC'
NOW = datetime.fromisoformat('2026-01-20T10:00:00+00:00')
WORKER_SCOPES = ["assignments:read", "events:write", "runs:write", "skills:read", "triage:write", "work:execute"]


@pytest.fixture
def frozen_working_day(monkeypatch):
    from app.utils import time

    class ServerDate(date):
        @classmethod
        def today(cls):
            return NOW.astimezone(UTC).date()

    monkeypatch.setattr(backlog_snapshot_service, 'utc_now', time.utc_now)
    monkeypatch.setattr(agent_work_service, 'date', ServerDate, raising=False)
    monkeypatch.setattr(agent_work_service, 'utc_now', lambda: NOW)
    monkeypatch.setattr(work_metrics, 'utc_now', lambda: NOW)
    monkeypatch.setattr(time, 'utc_now', lambda: NOW)
    return work_metrics.working_today(ZONE, NOW)


async def begin_as_worker(factory, scenario, today, client, headers):
    import json
    task_id, assignment_id = await seed_work(factory, scenario)
    async with factory() as db:
        (await db.get(Project, scenario.projects[0])).timezone = ZONE
        task = await db.get(Task, task_id)
        task.start_date, task.end_date = today, today + timedelta(days=1)
        actor = await db.get(AgentActor, scenario.actors[0])
        actor.scopes = json.dumps(WORKER_SCOPES)
        await db.commit()
        revision = actor.queue_revision
    begun = await client.post('/api/agent/me/work/begin', headers={**headers, 'Idempotency-Key': 'discovery-begin'},
                              json={'assignment_id': assignment_id, 'queue_revision': revision, 'lease_seconds': 60})
    assert begun.status_code == 200, begun.text
    return begun.json()


def discovery_body(begun, **changes):
    body = {
        'task_id': begun['task']['id'], 'assignment_id': begun['assignment']['id'], 'run_id': begun['run']['id'],
        'claim_id': begun['claim_id'], 'claim_generation': begun['claim_generation'],
        'expected_task_version': begun['task']['version'],
        'title': 'Neighbouring module needs a fix', 'description': 'Found while working; outside this assignment.',
        'blocking': False, 'evidence': {'path': 'src/neighbour.py'}, 'suggested_labels': ['follow-up'], 'priority_hint': 4,
    }
    body.update(changes)
    return body


async def test_worker_reports_a_discovery_from_its_accepted_assignment(delivery_store, frozen_working_day):
    factory, scenario, _ = delivery_store
    headers = {'X-Agent-API-Key': scenario.actor_keys[0]}
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        begun = await begin_as_worker(factory, scenario, frozen_working_day, client, headers)
        reported = await client.post('/api/agent/discoveries', headers={**headers, 'Idempotency-Key': 'discovery-one'},
                                     json=discovery_body(begun))
        assert reported.status_code == 201, reported.text
        again = await client.post('/api/agent/discoveries', headers={**headers, 'Idempotency-Key': 'discovery-one'},
                                  json=discovery_body(begun))
        assert again.status_code == 201 and again.json()['id'] == reported.json()['id'], again.text
    async with factory() as db:
        items = (await db.scalars(select(TriageItem))).all()
        assert len(items) == 1
        item = items[0]
        assert (item.source, item.project_hint_id, item.title) == (
            'agent-discovery', scenario.projects[0], 'Neighbouring module needs a fix')
        assert 'agent-discovery' in item.labels and 'follow-up' in item.labels
        events = (await db.scalars(select(TaskEvent).where(
            TaskEvent.task_id == begun['task']['id'], TaskEvent.event_type == 'agent.discovery_reported'))).all()
        assert len(events) == 1


async def test_worker_cannot_create_triage_items_any_other_way(delivery_store, frozen_working_day):
    """The discovery command is the only door: the general triage route stays closed to a worker."""
    factory, scenario, _ = delivery_store
    headers = {'X-Agent-API-Key': scenario.actor_keys[0]}
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        await begin_as_worker(factory, scenario, frozen_working_day, client, headers)
        direct = await client.post('/api/triage', headers=headers,
                                   json={'title': 'Slipped in', 'project_hint_id': scenario.projects[0]})
        assert direct.status_code in {401, 403}, direct.text
    async with factory() as db:
        assert (await db.scalars(select(TriageItem))).all() == []


@pytest.mark.parametrize('case', ['unmarked', 'other_source', 'other_project', 'second_item'])
async def test_guard_admits_only_the_discovery_the_command_announced(delivery_store, frozen_working_day, case):
    factory, scenario, _ = delivery_store
    headers = {'X-Agent-API-Key': scenario.actor_keys[0]}
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        begun = await begin_as_worker(factory, scenario, frozen_working_day, client, headers)
    async with factory() as db:
        actor = await db.get(AgentActor, scenario.actors[0])
        db.info['authority'] = await IdentityService(db).actor_context(actor, source='agent_rest')
        if case != 'unmarked':
            task = await db.get(Task, begun['task']['id'])
            db.info['claim_bound_discovery'] = {'actor_id': actor.id, 'project_hint_id': task.project_id,
                                                'iteration_hint_id': task.iteration_id, 'remaining': 1}
        task = await db.get(Task, begun['task']['id'])
        project = scenario.projects[1] if case == 'other_project' else task.project_id
        source = 'manual' if case == 'other_source' else 'agent-discovery'
        db.add(TriageItem(title='Not announced', source=source, status='new', project_hint_id=project,
                          iteration_hint_id=task.iteration_id, labels=[], metadata_json={}))
        if case == 'second_item':
            db.add(TriageItem(title='One too many', source='agent-discovery', status='new',
                              project_hint_id=task.project_id, iteration_hint_id=task.iteration_id,
                              labels=[], metadata_json={}))
        with pytest.raises(AuthorityError):
            await db.flush()
        await db.rollback()
    async with factory() as db:
        assert (await db.scalars(select(TriageItem))).all() == []

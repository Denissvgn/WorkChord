"""Report scopes aggregate recorded facts and retain legacy query behavior."""

from datetime import timedelta
from decimal import Decimal

import httpx
import pytest
import pytest_asyncio

from app.authority import Authority
from app.main import app
from app.models.agent import AgentActor, AgentRun
from app.models.delivery_observation import DeliveryObservation
from app.models.task import Task
from app.schemas.execution_usage import ExecutionUsageWrite
from app.services.delivery_metrics_service import DeliveryMetricsService
from app.services.execution_usage_service import ExecutionUsageService
from app.utils.time import utc_now
from tests.test_delivery_scenarios import delivery_store


@pytest_asyncio.fixture
async def report_store(delivery_store, monkeypatch):
    factory, scenario, _ = delivery_store
    now = utc_now() + timedelta(minutes=1)
    monkeypatch.setattr('app.services.delivery_metrics_service.utc_now', lambda: now)
    monkeypatch.setattr('app.services.execution_usage_service.utc_now', lambda: now)
    task_ids = []
    async with factory() as db:
        actor = await db.get(AgentActor, scenario.actors[0])
        actor.scopes = '["runs:write","tasks:read"]'
        for project_id, iteration_id, days in [
            (scenario.projects[0], None, 1), (scenario.projects[0], None, 2),
            (scenario.projects[0], None, 3), (scenario.projects[1], None, 20),
            (scenario.projects[0], scenario.iterations[0], 10),
        ]:
            task = Task(title=f'Recorded work {days}', project_id=project_id, iteration_id=iteration_id,
                        status='resolved', resolved_at=now - timedelta(hours=2))
            db.add(task)
            await db.flush()
            task_ids.append(task.id)
            for version, (kind, at) in enumerate([
                ('captured', now - timedelta(days=days, hours=1)),
                ('started', now - timedelta(days=days, hours=1)),
                ('resolved', now - timedelta(hours=2)), ('accepted', now - timedelta(hours=1)),
            ], 10):
                db.add(DeliveryObservation(original_task_id=task.id, project_id=project_id,
                    iteration_id=iteration_id, task_version=version, kind=kind,
                    source='recorded_workflow', observed_at=at))
            run = AgentRun(task_id=task.id, actor_id=actor.id, status='succeeded',
                           started_at=now - timedelta(days=1), ended_at=now - timedelta(hours=1))
            db.add(run)
            await db.commit()
            payload = ExecutionUsageWrite(report_id='total', source='provider', provenance='provider_reported',
                reporting_mode='attempt_total', coverage='complete', reported_cost=Decimal(days), currency='USD',
                quantities={'input_tokens': Decimal(days * 10), 'output_tokens': Decimal(0)},
                interval_start=now - timedelta(hours=2), interval_end=now - timedelta(hours=1))
            first = await ExecutionUsageService(db).write(actor, run.id, payload)
            if days == 1:
                await ExecutionUsageService(db).write(actor, run.id, payload.model_copy(update={
                    'report_id': 'corrected', 'expected_previous_digest': first.digest,
                    'reported_cost': Decimal(4),
                }))
        db.add(AgentRun(task_id=scenario.tasks['other_project'], actor_id=actor.id,
                       status='running', started_at=now - timedelta(hours=1)))
        await db.commit()
    return factory, scenario, task_ids


@pytest.mark.parametrize('scope,accepted,median_days,cost,runs,missing', [
    ('backlog', 3, 2, 9, 3, 0), ('all', 5, 3, 39, 6, 1),
    ('project', 4, 2.5, 19, 4, 0), ('iteration', 1, 10, 10, 1, 0),
    ('both', 1, 10, 10, 1, 0),
])
async def test_reports_aggregate_matching_scope_and_preserve_existing_parameters(
    report_store, scope, accepted, median_days, cost, runs, missing,
):
    _, scenario, task_ids = report_store
    params = {'lookback_days': 30}
    if scope in {'backlog', 'project', 'both'}:
        params['project_id'] = scenario.projects[0]
    if scope in {'iteration', 'both'}:
        params['iteration_id'] = scenario.iterations[0]
    if scope == 'backlog':
        params['backlog'] = True
    if scope == 'all':
        params['all_projects'] = True
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        delivery = await client.get('/api/tasks/delivery-metrics', params=params)
        assert delivery.status_code == 200, delivery.text
        data = delivery.json()
        assert data['accepted_leaf_tasks'] == data['acceptance_events'] == accepted
        assert data['lead_time']['median'] == median_days * 86400
        assert data['lead_time']['sample_count'] == accepted
        assert data['scope_basis'] == 'scope_at_observation'
        if scope == 'backlog':
            assert {item['task_id'] for item in data['review_queue']} == set(task_ids[:3])
            assert data['coverage']['current_leaf_tasks'] == 3
        usage = await client.get('/api/tasks/execution-usage', params={**params,
            'budget_amount': '100', 'budget_currency': 'USD'})
        assert usage.status_code == 200, usage.text
        data = usage.json()
        assert data['expected_runs'] == runs and data['unreported_runs'] == missing
        assert data['reported_runs'] == accepted
        assert Decimal(data['provider_reported_cost']['USD']) == cost
        assert data['accepted_task_identities'] == data['reports_linked_to_accepted_tasks'] == accepted
        assert data['linked_delivery']['review_delay']['sample_count'] == accepted
        assert data['linked_delivery']['review_delay']['median'] == 3600
        assert Decimal(data['advisory_budget']['known_reported_cost']) == cost
        if scope in {'project', 'iteration', 'both'}:
            for route, original, extra in [
                ('delivery-metrics', delivery, {}),
                ('execution-usage', usage, {'budget_amount': '100', 'budget_currency': 'USD'}),
            ]:
                explicit_defaults = await client.get(f'/api/tasks/{route}', params={
                    **params, **extra, 'backlog': False, 'all_projects': False,
                })
                assert explicit_defaults.json() == original.json()


async def test_workspace_reports_keep_authorization_and_recorded_backlog_scope(report_store):
    factory, scenario, task_ids = report_store
    async with factory() as db:
        task = await db.get(Task, task_ids[0])
        task.iteration_id = scenario.iterations[0]
        await db.commit()
        db.info['authority'] = Authority(1, 'human', projects={scenario.projects[0]: 'viewer'})
        for service, method in [(DeliveryMetricsService(db), 'report'), (ExecutionUsageService(db), 'summary')]:
            read = getattr(service, method)
            workspace = await read(all_projects=True)
            project = await read(project_id=scenario.projects[0])
            assert workspace.model_dump() == project.model_dump()
            backlog = await read(project_id=scenario.projects[0], backlog=True)
            if method == 'report':
                assert backlog.accepted_leaf_tasks == 3
                assert {item.task_id for item in backlog.review_queue} == set(task_ids[1:3])
            else:
                assert backlog.reported_runs == 3
                assert backlog.provider_reported_cost == {'USD': Decimal(9)}


@pytest.mark.parametrize('params', [
    {}, {'backlog': True}, {'backlog': True, 'project_id': 1, 'iteration_id': 1},
    {'all_projects': True, 'project_id': 1}, {'all_projects': True, 'iteration_id': 1},
    {'all_projects': True, 'backlog': True},
])
async def test_report_reads_reject_missing_or_conflicting_scope(delivery_store, params):
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        for route in ('delivery-metrics', 'execution-usage'):
            response = await client.get(f'/api/tasks/{route}', params=params)
            assert response.status_code == 422, response.text


async def test_workspace_reports_preserve_window_and_empty_backlog(delivery_store, monkeypatch):
    factory, scenario, _ = delivery_store
    now = utc_now() + timedelta(minutes=1)
    monkeypatch.setattr('app.services.delivery_metrics_service.utc_now', lambda: now)
    monkeypatch.setattr('app.services.execution_usage_service.utc_now', lambda: now)
    async with factory() as db:
        for service, method in [(DeliveryMetricsService(db), 'report'), (ExecutionUsageService(db), 'summary')]:
            read = getattr(service, method)
            empty = await read(project_id=scenario.projects[0], backlog=True, lookback_days=90)
            assert empty.window_end - empty.window_start == timedelta(days=90)
            if method == 'report':
                assert empty.accepted_leaf_tasks == 0 and empty.lead_time.median is None
                assert empty.review_queue == [] and empty.recovery_queue == []
            else:
                assert empty.expected_runs == empty.reported_runs == 0
                assert empty.provider_reported_cost == {}
            for days in (0, 367):
                with pytest.raises(ValueError, match='window'):
                    await read(all_projects=True, lookback_days=days)


async def test_deleted_iteration_history_does_not_become_backlog(delivery_store):
    from sqlalchemy import delete
    from app.models.execution_usage import ExecutionUsageRecord
    from app.models.iteration import Iteration

    factory, scenario, _ = delivery_store
    now = utc_now() - timedelta(minutes=1)
    async with factory() as db:
        source = await db.get(Iteration, scenario.iterations[0])
        archived = Iteration(name='Removed iteration', project_id=scenario.projects[0],
            calendar_id=source.calendar_id, start_date=source.start_date, end_date=source.end_date)
        db.add(archived)
        await db.flush()
        db.add(DeliveryObservation(original_task_id=10000, task_version=1,
            project_id=scenario.projects[0], iteration_id=archived.id, original_iteration_id=archived.id,
            kind='accepted', source='recorded_workflow', observed_at=now))
        payload = ExecutionUsageWrite(report_id='retained', source='provider', provenance='provider_reported',
            reporting_mode='attempt_total', coverage='complete', reported_cost=Decimal(7), currency='USD',
            interval_start=now, interval_end=now)
        db.add(ExecutionUsageRecord(original_run_id=10000, original_task_id=10000,
            run_identity='archived-attempt', report_id='retained', sequence=1, digest='a' * 64,
            project_id=scenario.projects[0], iteration_id=archived.id, original_iteration_id=archived.id,
            payload=payload.model_dump(mode='json'), reported_at=now))
        await db.commit()
        await db.execute(delete(Iteration).where(Iteration.id == archived.id))
        await db.commit()
        assert (await DeliveryMetricsService(db).report(all_projects=True)).accepted_leaf_tasks == 1
        assert (await ExecutionUsageService(db).summary(all_projects=True)).reported_runs == 1
        delivery = await DeliveryMetricsService(db).report(project_id=scenario.projects[0], backlog=True)
        usage = await ExecutionUsageService(db).summary(project_id=scenario.projects[0], backlog=True)
        assert delivery.accepted_leaf_tasks == 0
        assert usage.reported_runs == usage.accepted_task_identities == 0
        assert usage.provider_reported_cost == {}

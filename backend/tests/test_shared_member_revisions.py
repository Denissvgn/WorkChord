"""Shared-input scopes and destructive writes retain initial aggregate guards."""
from datetime import date
import pytest
from app.config import get_settings
from app.mutation_versions import MissingMutationRevision
from app.models.iteration import Iteration
from app.models.team_member import TeamMember
from sqlalchemy import select
from app.services.iteration_service import IterationService
from app.services.planning_input_context import observe_planning_input
from tests.test_delivery_scenarios import delivery_store
from tests.test_managed_authority import managed_store

async def test_shared_member_initial_map_covers_other_allocations(delivery_store):
 factory,scenario,_=delivery_store
 async with factory() as db:
  observed=await observe_planning_input(db,'member',await db.scalar(select(TeamMember.id).where(TeamMember.profile_id==scenario.profile).order_by(TeamMember.id).limit(1)))
  assert set(observed['expected_revisions'])==set(scenario.iterations)

async def test_iteration_delete_requires_observed_revision(delivery_store,monkeypatch):
 factory,scenario,_=delivery_store
 monkeypatch.setenv('STRICT_MUTATION_VERSIONS','true');get_settings.cache_clear()
 try:
  async with factory() as db:
   original=await db.get(Iteration,scenario.iterations[0])
   empty=Iteration(name='Disposable delete context',calendar_id=original.calendar_id,project_id=original.project_id,start_date=date(2026,1,1),end_date=date(2026,1,31))
   db.add(empty);await db.commit()
   with pytest.raises(MissingMutationRevision): await IterationService(db).delete(empty.id)
 finally:get_settings.cache_clear()

async def test_vacation_preview_and_nested_import_retain_complete_shared_map(delivery_store, monkeypatch):
    import httpx
    import json
    from app.main import app
    factory, scenario, _ = delivery_store
    monkeypatch.setenv('STRICT_MUTATION_VERSIONS', 'true'); get_settings.cache_clear()
    try:
        csv_text = f'member_id,start_date,end_date\n{scenario.capacity_rows[0]},2026-01-22,2026-01-23'
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
            observed = await client.post(f'/api/tasks/planning-inputs/member/{scenario.iterations[0]}/context',
                params={'creating_member': True}, json={'csv_text': csv_text})
            assert observed.status_code == 200, observed.text
            revisions = observed.json()['expected_revisions']
            assert set(map(int, revisions)) == set(scenario.iterations)
            path = f'/api/iterations/{scenario.iterations[0]}/team/vacations/import'
            missing = await client.post(path, json={'csv_text': csv_text})
            assert missing.status_code == 422, missing.text
            saved = await client.post(path, json={'csv_text': csv_text}, headers={'X-Expected-Revisions': json.dumps(revisions)})
            assert saved.status_code == 200 and saved.json()['imported_count'] == 1, saved.text
            stale = await client.post(path, json={'csv_text': csv_text}, headers={'X-Expected-Revisions': json.dumps(revisions)})
            assert stale.status_code == 409, stale.text
    finally: get_settings.cache_clear()


async def test_json_import_preview_is_strict_atomic_and_retains_stale_conflict(managed_store, monkeypatch):
    import httpx
    import json
    from app.main import app
    factory, scenario, _, _ = managed_store
    monkeypatch.setenv('STRICT_MUTATION_VERSIONS', 'true')
    get_settings.cache_clear()
    try:
        files = {'file': ('input.json', json.dumps({'tasks': [{'title': 'Observed JSON task', 'project_id': scenario.projects[0], 'effort_hours': 2}]}), 'application/json')}
        path = f'/api/iterations/{scenario.iterations[0]}/import'
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='https://test', headers={'X-Admin-API-Key': 'managed-operator-fixture'}) as client:
            observed = await client.post(path + '-context', files=files)
            assert observed.status_code == 200 and observed.json()['complete'], observed.text
            headers = {'X-Expected-Revisions': json.dumps(observed.json()['expected_revisions'])}
            missing = await client.post(path, files=files)
            assert missing.status_code == 422, missing.text
            saved = await client.post(path, files=files, headers=headers)
            assert saved.status_code == 200, saved.text
            stale = await client.post(path, files=files, headers=headers)
            assert stale.status_code == 409, stale.text
            new_files = {'file': ('new.json', json.dumps({'iteration': {'name': 'Owned import', 'start_date': '2026-01-05',
                'end_date': '2026-01-30', 'project_id': scenario.projects[0]}, 'tasks': [{'title': 'Fresh owned task', 'effort_hours': 2}]}), 'application/json')}
            new_context = await client.post('/api/iterations/import-context', files=new_files)
            assert new_context.status_code == 200 and new_context.json()['expected_revisions'] == {}, new_context.text
            created = await client.post('/api/iterations/import', files=new_files, headers={'X-Expected-Revisions': '{}'})
            assert created.status_code == 200, created.text
    finally: get_settings.cache_clear()

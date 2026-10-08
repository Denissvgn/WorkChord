"""Operator caller observations are enforced in both dialects and sampled explicitly."""
import json
from datetime import date, datetime, timezone
import httpx
import pytest
from sqlalchemy import select
from app.config import get_settings
from app.main import app
from app.models.iteration import Iteration
from app.models.calendar import Calendar
from app.models.team_member import TeamMemberProfileSkill, Vacation
from app.runtime_telemetry import metrics
from tests.test_managed_authority import managed_store
from tests.test_delivery_scenarios import delivery_store

ROWS = ['calendar_edit', 'holiday_public', 'holiday_csv', 'profile_edit', 'skill_create', 'skill_edit', 'skill_delete',
    'profile_delete', 'project_edit', 'iteration_edit', 'member_create', 'member_edit', 'member_delete', 'vacation_create',
    'vacation_delete', 'member_text_import', 'vacation_csv_import', 'json_import']


def missing_count():
    return sum(float(line.split()[-1]) for line in metrics.render_prometheus().splitlines()
        if line.startswith('workchord_missing_mutation_revision_total'))


@pytest.mark.parametrize('row', ROWS)
async def test_operator_caller_matrix(managed_store, monkeypatch, request, row):
    factory, scenario, _, _ = managed_store
    monkeypatch.setenv('STRICT_MUTATION_VERSIONS', 'true'); get_settings.cache_clear()
    samples = []
    try:
        async with factory() as db:
            calendar_id = (await db.get(Iteration, scenario.iterations[0])).calendar_id
            skill = TeamMemberProfileSkill(profile_id=scenario.profile, skill_key='matrix-skill', skill_name='Matrix skill')
            vacation = Vacation(team_member_id=scenario.capacity_rows[0], start_date=date(2026, 1, 22), end_date=date(2026, 1, 23))
            db.add_all([skill, vacation]); await db.commit()
            skill_id, vacation_id = skill.id, vacation.id
        kind, identifier, method, path, body = {
            'calendar_edit': ('calendar', calendar_id, 'PUT', f'/api/calendars/{calendar_id}', {'name': 'Observed calendar'}),
            'holiday_public': ('calendar', calendar_id, 'POST', f'/api/calendars/{calendar_id}/import-holidays', {'source': 'public', 'country': 'US', 'year': 2026}),
            'holiday_csv': ('calendar', calendar_id, 'POST', f'/api/calendars/{calendar_id}/import-holidays', {'source': 'csv', 'csv_text': 'date\n2026-12-31'}),
            'profile_edit': ('profile', scenario.profile, 'PUT', f'/api/team-member-profiles/{scenario.profile}', {'display_name': 'Observed profile'}),
            'skill_create': ('profile', scenario.profile, 'POST', f'/api/team-member-profiles/{scenario.profile}/skills', {'skill_key': 'new-matrix-skill', 'skill_name': 'New matrix skill'}),
            'skill_edit': ('profile', scenario.profile, 'PUT', f'/api/team-member-profiles/{scenario.profile}/skills/{skill_id}', {'level': 4}),
            'skill_delete': ('profile', scenario.profile, 'DELETE', f'/api/team-member-profiles/{scenario.profile}/skills/{skill_id}', None),
            'profile_delete': ('profile', scenario.profile, 'DELETE', f'/api/team-member-profiles/{scenario.profile}', None),
            'project_edit': ('project', scenario.projects[0], 'PUT', f'/api/projects/{scenario.projects[0]}', {'description': 'Observed project draft'}),
            'iteration_edit': ('iteration', scenario.iterations[0], 'PUT', f'/api/iterations/{scenario.iterations[0]}', {'name': 'Observed period'}),
            'member_create': ('member', scenario.iterations[0], 'POST', f'/api/iterations/{scenario.iterations[0]}/team', {'name': 'Independent person', 'position': 'Developer'}),
            'member_edit': ('member', scenario.capacity_rows[0], 'PUT', f'/api/team-members/{scenario.capacity_rows[0]}', {'availability_percent': 90}),
            'member_delete': ('member', scenario.capacity_rows[0], 'DELETE', f'/api/team-members/{scenario.capacity_rows[0]}', None),
            'vacation_create': ('member', scenario.capacity_rows[0], 'POST', f'/api/team-members/{scenario.capacity_rows[0]}/vacations', {'start_date': '2026-01-26', 'end_date': '2026-01-27'}),
            'vacation_delete': ('vacation', vacation_id, 'DELETE', f'/api/vacations/{vacation_id}', None),
            'member_text_import': ('member', scenario.iterations[0], 'POST', f'/api/iterations/{scenario.iterations[0]}/team/import', {'text': '-- "Imported matrix person" Developer 100 1.0 20'}),
            'vacation_csv_import': ('member', scenario.iterations[0], 'POST', f'/api/iterations/{scenario.iterations[0]}/team/vacations/import', {'csv_text': f'member_id,start_date,end_date\n{scenario.capacity_rows[0]},2026-01-26,2026-01-27'}),
            'json_import': ('iteration', scenario.iterations[0], 'POST', f'/api/iterations/{scenario.iterations[0]}/import', {'tasks': [{'title': 'Observed matrix import', 'effort_hours': 2}]}),
        }[row]
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='https://test', headers={'X-Admin-API-Key': 'managed-operator-fixture'}) as client:
            async def observe():
                if row == 'json_import':
                    result = await client.post(path + '-context', files={'file': ('matrix.json', json.dumps(body), 'application/json')})
                elif row in {'member_create', 'member_text_import', 'vacation_csv_import'}:
                    result = await client.post(f'/api/tasks/planning-inputs/member/{identifier}/context', params={'creating_member': True}, json=body)
                else: result = await client.get(f'/api/tasks/planning-inputs/{kind}/{identifier}/context')
                assert result.status_code == 200, result.text
                assert result.json()['complete'] is True
                return result.json()['expected_revisions']
            async def write(revisions=None):
                options = {'headers': {'X-Expected-Revisions': json.dumps(revisions)}} if revisions is not None else {}
                if row == 'json_import': options['files'] = {'file': ('matrix.json', json.dumps(body), 'application/json')}
                elif body is not None: options['json'] = body
                return await client.request(method, path, **options)
            initial = await observe()
            negative = await write()
            assert negative.status_code == 422 and negative.json()['detail']['code'] == 'mutation_revision_required', negative.text
            # A separately authenticated request changes an observed aggregate before the original caller writes.
            task_path = f"/api/tasks/{scenario.tasks['planned']}"
            current = (await client.get(task_path)).json()
            start, baseline = datetime.now(timezone.utc).isoformat(), missing_count()
            peer = await client.put(task_path, json={'title': 'Peer scope change', 'expected_version': current['version']})
            assert peer.status_code == 200, peer.text
            assert missing_count() == baseline
            samples.append({'phase': 'positive_peer', 'window_start': start, 'window_end': datetime.now(timezone.utc).isoformat(), 'missing_delta': 0, 'sampled_writes': 1})
            stale = await write(initial)
            assert stale.status_code == 409, stale.text
            current_context = await observe()
            start, baseline = datetime.now(timezone.utc).isoformat(), missing_count()
            positive = await write(current_context)
            assert positive.status_code in {200, 201}, positive.text
            assert missing_count() == baseline
            samples.append({'phase': 'positive_caller', 'window_start': start, 'window_end': datetime.now(timezone.utc).isoformat(), 'missing_delta': 0, 'sampled_writes': 1})
            request.node.user_properties.append(('caller_telemetry', json.dumps({'row': row, 'positive_windows': samples,
                'negative_cases': ['deliberate_missing', 'deliberate_stale'], 'deployed_traffic': 'unknown'})))
    finally: get_settings.cache_clear()


async def test_structural_commands_replays_and_rollback_keep_identity_and_versions(managed_store, monkeypatch, request):
    factory, scenario, _, principal_ids = managed_store
    monkeypatch.setenv('STRICT_MUTATION_VERSIONS', 'true'); get_settings.cache_clear()
    try:
        from app.models.identity import PrincipalProfileLink
        async with factory() as db:
            db.add(PrincipalProfileLink(principal_id=principal_ids[0], profile_id=scenario.profile, linked_by_principal_id=principal_ids[0])); await db.commit()
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='https://test', headers={'X-Admin-API-Key': 'managed-operator-fixture'}) as client:
            created = await client.post(f'/api/projects/{scenario.projects[0]}/backlog', json={'title': 'Bounded command work', 'effort_hours': 2,
                'owner_profile_id': scenario.profile, 'brief': {'schema_version': 1, 'goal': 'Deliver bounded work', 'acceptance_criteria': []}})
            assert created.status_code == 201, created.text
            task = created.json(); task_id = task['id']
            for action in ['commit', 'uncommit']:
                context = (await client.get(f'/api/tasks/planning-inputs/iteration/{scenario.iterations[0]}/context')).json()
                revisions = context['expected_revisions']
                payload = {'action': action, 'expected_version': task['version'], 'reason': 'Apply observed structural intent',
                    **({'iteration_id': scenario.iterations[0]} if action == 'commit' else {})}
                missing = await client.post(f'/api/tasks/{task_id}/commands', json=payload)
                assert missing.status_code == 422 and missing.json()['detail']['code'] == 'mutation_revision_required', missing.text
                peer = (await client.get(f"/api/tasks/{scenario.tasks['planned']}")).json()
                changed = await client.put(f"/api/tasks/{peer['id']}", json={'title': 'Peer planning change', 'expected_version': peer['version']})
                assert changed.status_code == 200, changed.text
                stale = await client.post(f'/api/tasks/{task_id}/commands', json={**payload, 'expected_revisions': revisions})
                assert stale.status_code == 409, stale.text
                revisions = (await client.get(f'/api/tasks/planning-inputs/iteration/{scenario.iterations[0]}/context')).json()['expected_revisions']
                before = missing_count(); start = datetime.now(timezone.utc).isoformat()
                applied = await client.post(f'/api/tasks/{task_id}/commands', json={**payload, 'expected_revisions': revisions})
                assert applied.status_code == 200, applied.text
                assert missing_count() == before
                request.node.user_properties.append(('caller_telemetry', json.dumps({'row': action, 'positive_windows': [{'phase': 'positive_caller',
                    'window_start': start, 'window_end': datetime.now(timezone.utc).isoformat(), 'missing_delta': 0, 'sampled_writes': 1}], 'negative_cases': ['missing', 'stale', 'replay'], 'deployed_traffic': 'unknown'})))
                replay = await client.post(f'/api/tasks/{task_id}/commands', json={**payload, 'expected_revisions': revisions})
                assert replay.status_code == 409, replay.text
                task = applied.json()
            monkeypatch.setenv('STRICT_MUTATION_VERSIONS', 'false'); get_settings.cache_clear()
            compatible = await client.put(f'/api/tasks/{task_id}', json={'priority': 6})
            assert compatible.status_code == 200, compatible.text
            supplied_stale = await client.put(f'/api/tasks/{task_id}', json={'title': 'Stale after rollback', 'expected_version': task['version']})
            assert supplied_stale.status_code == 409, supplied_stale.text
            unauthenticated = await httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='https://test').put(f'/api/tasks/{task_id}', json={'title': 'No identity'})
            assert unauthenticated.status_code == 401, unauthenticated.text
    finally: get_settings.cache_clear()


async def test_empty_calendar_scope_detects_new_allocation_before_delete(managed_store, monkeypatch):
    factory, scenario, _, _ = managed_store
    monkeypatch.setenv('STRICT_MUTATION_VERSIONS', 'true'); get_settings.cache_clear()
    try:
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='https://test', headers={'X-Admin-API-Key': 'managed-operator-fixture'}) as client:
            created = await client.post('/api/calendars', json={'name': 'Unused authoritative scope', 'year': 2026})
            assert created.status_code == 201, created.text
            identifier = created.json()['id']
            observed = (await client.get(f'/api/tasks/planning-inputs/calendar/{identifier}/context')).json()
            assert observed['expected_revisions'] == {}
            missing = await client.delete(f'/api/calendars/{identifier}')
            assert missing.status_code == 422, missing.text
            async with factory() as db:
                changed = Iteration(name='New affected scope', calendar_id=identifier, project_id=scenario.projects[0], start_date=date(2026,1,1), end_date=date(2026,1,31))
                db.add(changed); await db.commit(); new_id = changed.id
            stale = await client.delete(f'/api/calendars/{identifier}', headers={'X-Expected-Revisions': '{}'})
            assert stale.status_code == 409 and stale.json()['detail']['code'] == 'planning_scope_changed', stale.text
            async with factory() as db:
                original_calendar = (await db.get(Iteration, scenario.iterations[0])).calendar_id
                changed = await db.get(Iteration, new_id); changed.calendar_id = original_calendar; await db.commit()
            removed = await client.delete(f'/api/calendars/{identifier}', headers={'X-Expected-Revisions': '{}'})
            assert removed.status_code == 200, removed.text
    finally: get_settings.cache_clear()


async def test_snapshot_restore_observes_revision_and_keeps_history(managed_store, monkeypatch):
    from app.services.snapshot_service import SnapshotService
    from app.authority import Authority
    factory, scenario, _, _ = managed_store
    monkeypatch.setenv('STRICT_MUTATION_VERSIONS', 'true'); get_settings.cache_clear()
    try:
        async with factory() as db:
            db.info['authority'] = Authority(None, 'system', workspace_role='operator')
            filename = await SnapshotService(db).create_snapshot(scenario.iterations[0], 'observed_restore')
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='https://test', headers={'X-Admin-API-Key': 'managed-operator-fixture'}) as client:
            path = f'/api/iterations/{scenario.iterations[0]}/snapshots/{filename}/restore'
            initial = (await client.get(f'/api/tasks/planning-inputs/iteration/{scenario.iterations[0]}/context')).json()['expected_revisions'][str(scenario.iterations[0])]
            missing = await client.post(path, json={'confirm': True})
            assert missing.status_code == 422, missing.text
            peer = (await client.get(f"/api/tasks/{scenario.tasks['planned']}")).json()
            changed = await client.put(f"/api/tasks/{peer['id']}", json={'priority': 8, 'expected_version': peer['version']})
            assert changed.status_code == 200, changed.text
            stale = await client.post(path, json={'confirm': True, 'expected_revision': initial})
            assert stale.status_code == 409, stale.text
            current = (await client.get(f'/api/tasks/planning-inputs/iteration/{scenario.iterations[0]}/context')).json()['expected_revisions'][str(scenario.iterations[0])]
            before = missing_count()
            restored = await client.post(path, json={'confirm': True, 'expected_revision': current})
            assert restored.status_code == 200 and restored.json()['audit_event_id'], restored.text
            assert missing_count() == before
    finally: get_settings.cache_clear()


async def test_mcp_positive_missing_and_stale_versions_share_policy(delivery_store, monkeypatch):
    from app.models.agent import AgentActor
    from app.models.task import Task
    from app import mcp_agent_tools
    from app.mutation_versions import MissingMutationRevision
    from app.services.task_service import TaskVersionConflictError
    factory, scenario, _ = delivery_store
    monkeypatch.setenv('STRICT_MUTATION_VERSIONS', 'true'); get_settings.cache_clear()
    try:
        async with factory() as db:
            actor = await db.get(AgentActor, scenario.actors[0]); actor.role = 'pm'; actor.scopes = '["tasks:write","tasks:read"]'; await db.commit()
            task = await db.get(Task, scenario.tasks['planned']); version = task.version
            with pytest.raises(MissingMutationRevision):
                await mcp_agent_tools.update_task(db, actor, task.id, {'priority': 7})
            before = missing_count()
            updated = await mcp_agent_tools.update_task(db, actor, task.id, {'priority': 7, 'expected_version': version})
            assert updated['version'] > version and missing_count() == before
            with pytest.raises(TaskVersionConflictError):
                await mcp_agent_tools.update_task(db, actor, task.id, {'priority': 8, 'expected_version': version})
    finally: get_settings.cache_clear()


@pytest.mark.parametrize('kind', ['project', 'iteration'])
async def test_destructive_confirmation_preserves_original_scope(managed_store, monkeypatch, kind):
    from app.models.project import Project
    factory, scenario, _, _ = managed_store
    monkeypatch.setenv('STRICT_MUTATION_VERSIONS', 'true'); get_settings.cache_clear()
    try:
        async with factory() as db:
            project = Project(name='Disposable confirmation scope'); db.add(project); await db.flush()
            calendar_id = (await db.get(Iteration, scenario.iterations[0])).calendar_id
            iteration = Iteration(name='Disposable confirmation window', project_id=project.id, calendar_id=calendar_id,
                start_date=date(2026,1,1), end_date=date(2026,1,31)); db.add(iteration); await db.commit()
            project_id, iteration_id = project.id, iteration.id
        identifier = project_id if kind == 'project' else iteration_id
        path = f'/api/{"projects" if kind == "project" else "iterations"}/{identifier}'
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='https://test', headers={'X-Admin-API-Key': 'managed-operator-fixture'}) as client:
            context_path = f'/api/tasks/planning-inputs/{kind}/{identifier}/context'
            initial = (await client.get(context_path)).json()['expected_revisions']
            missing = await client.delete(path)
            assert missing.status_code == 422, missing.text
            peer = await client.put(f'/api/iterations/{iteration_id}', json={'name': 'Peer confirmation change'}, headers={'X-Expected-Revisions': json.dumps(initial)})
            assert peer.status_code == 200, peer.text
            stale = await client.delete(path, headers={'X-Expected-Revisions': json.dumps(initial)})
            assert stale.status_code == 409, stale.text
            current = (await client.get(context_path)).json()['expected_revisions']
            before = missing_count()
            removed = await client.delete(path, headers={'X-Expected-Revisions': json.dumps(current)})
            assert removed.status_code == 200 and missing_count() == before, removed.text
    finally: get_settings.cache_clear()

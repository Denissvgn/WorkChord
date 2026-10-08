"""Runtime configuration preserves supplied conflicts in either rollout mode."""

import httpx
from app.config import get_settings
from app.main import app
from tests.test_delivery_scenarios import delivery_store


async def test_effective_policy_and_compatibility_conflicts(delivery_store):
    _, scenario, _ = delivery_store
    strict = get_settings().strict_mutation_versions
    path = f"/api/tasks/{scenario.tasks['planned']}"
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        capabilities = await client.get('/api/tasks/capabilities')
        assert capabilities.status_code == 200, capabilities.text
        assert capabilities.json()['aggregate_revisions_required'] is strict
        before = (await client.get(path)).json()
        missing = await client.put(path, json={'title': 'Runtime policy edit'})
        assert missing.status_code == (422 if strict else 200), missing.text
        if strict:
            assert missing.json()['detail']['code'] == 'mutation_revision_required'
        current = (await client.get(path)).json()
        saved = await client.put(path, json={'title': 'Observed runtime edit', 'expected_version': current['version']})
        assert saved.status_code == 200, saved.text
        stale = await client.put(path, json={'title': 'Supplied stale edit', 'expected_version': before['version']})
        assert stale.status_code == 409, stale.text
        denied = await client.put(path, json={'title': 'Unauthorized edit', 'expected_version': saved.json()['version']},
            headers={'X-Agent-API-Key': scenario.actor_keys[0]})
        assert denied.status_code == 403, denied.text

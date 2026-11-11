"""People without the admin key read settings and the pipeline; changes keep the key."""

from app.config import get_settings
from app.models.identity import Principal, WorkspaceAuthorityState
from app.models.outbound_webhook import OutboundWebhookTarget
from tests.test_delivery_scenarios import delivery_store
from tests.test_managed_authority import client

KEY = "settings-read-fixture-key"


async def test_settings_are_readable_without_the_key_and_sensitive_values_are_withheld(delivery_store, monkeypatch):
    monkeypatch.setenv("WORKCHORD_ADMIN_API_KEY", KEY)
    get_settings.cache_clear()
    factory, _, _ = delivery_store
    async with factory() as db:
        if await db.get(WorkspaceAuthorityState, 1) is None:
            system = Principal(kind="system", display_name="Operator API")
            db.add(system)
            await db.flush()
            db.add(WorkspaceAuthorityState(id=1, operator_principal_id=system.id))
        db.add(OutboundWebhookTarget(name="Ops", url="https://hooks.example.com/T0/private-path?token=abc", secret="signing-secret",
                                     headers_json={"Authorization": "Bearer private"}, subscribed_events_json=["task.created"], enabled=True))
        await db.commit()

    async with client() as reader:
        system = await reader.get("/api/system-settings")
        assert system.status_code == 200, system.text
        assert {"llm.api_url", "github.api_url"} <= set(system.json()["redacted_fields"])
        assert "/" not in system.json()["llm"]["api_url"]
        email = (await reader.get("/api/email-settings")).json()
        assert (email["smtp_host"], email["smtp_user"]) == ("", "")
        assert "password" not in email
        assert (await reader.get("/api/scheduling-rules")).status_code == 200
        targets = (await reader.get("/api/outbound-webhooks/targets")).json()
        assert [(item["url"], item["headers_json"], item["has_secret"]) for item in targets] == [("hooks.example.com", {"Authorization": ""}, True)]
        assert "private" not in str(targets) and "signing-secret" not in str(targets)
        assert (await reader.get("/api/outbound-webhooks/deliveries")).status_code == 200
        assert (await reader.get("/api/github/status-automation-rules")).status_code == 200
        assert (await reader.get("/api/agent/pipeline")).status_code == 200
        assert (await reader.post("/api/scheduling-rules/reset")).status_code == 403
        assert (await reader.delete(f"/api/outbound-webhooks/targets/{targets[0]['id']}")).status_code == 403

    async with client(**{"X-Admin-API-Key": KEY}) as operator:
        targets = (await operator.get("/api/outbound-webhooks/targets")).json()
        assert targets[0]["url"] == "https://hooks.example.com/T0/private-path?token=abc"
        assert targets[0]["redacted_fields"] == []

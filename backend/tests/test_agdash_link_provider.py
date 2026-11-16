"""agdash session links: a named provider, loopback display URLs for it alone, and no duplicates."""

import pytest
from pydantic import ValidationError

from app.schemas.external_link import ExternalLinkUpdate, TaskExternalLinkCreate
from tests.test_delivery_scenarios import delivery_store
from tests.test_observer_sessions import local_store
from tests.test_managed_authority import client


SESSION = {"provider": "agdash", "external_key": "claude-code:7f3c", "url": "http://127.0.0.1:8730/sessions/7f3c",
           "title": "Claude Code session"}


@pytest.mark.parametrize("url", ["http://127.0.0.1:8730/s/1", "http://localhost:8730/s/1", "http://[::1]:8730/s/1",
                                 "https://agdash.example/s/1"])
def test_an_agdash_link_may_open_on_the_observing_machine(url):
    assert TaskExternalLinkCreate(provider="agdash", url=url).url == url


@pytest.mark.parametrize("url", ["http://192.168.1.20:8730/s/1", "http://user:secret@127.0.0.1/s/1", "file:///tmp/s"])
def test_an_agdash_link_still_refuses_private_networks_credentials_and_other_schemes(url):
    with pytest.raises(ValidationError):
        TaskExternalLinkCreate(provider="agdash", url=url)


def test_other_providers_keep_refusing_loopback_links():
    with pytest.raises(ValidationError):
        TaskExternalLinkCreate(provider="custom", url="http://127.0.0.1:8730/s/1")
    with pytest.raises(ValidationError):
        ExternalLinkUpdate(provider="custom", url="http://127.0.0.1:8730/s/1")


async def test_a_session_link_is_created_once_and_updates_keep_the_url_rule(local_store):
    _, scenario, _ = local_store
    task = scenario.tasks["planned"]
    async with client() as browser:
        created = await browser.post(f"/api/tasks/{task}/external-links", json=SESSION)
        assert created.status_code == 201, created.text
        assert created.json()["provider"] == "agdash" and created.json()["url"] == SESSION["url"]
        again = await browser.post(f"/api/tasks/{task}/external-links", json={**SESSION, "title": "Retried publish"})
        assert again.status_code == 201 and again.json()["id"] == created.json()["id"]
        links = (await browser.get(f"/api/tasks/{task}/external-links")).json()
        assert [link["provider"] for link in links if link["provider"] == "agdash"] == ["agdash"]
        link_id = created.json()["id"]
        moved = await browser.put(f"/api/external-links/{link_id}", json={"url": "http://localhost:8731/sessions/7f3c"})
        assert moved.status_code == 200, moved.text
        # Changing the provider would leave a loopback URL on a provider that refuses it.
        refused = await browser.put(f"/api/external-links/{link_id}", json={"provider": "custom"})
        assert refused.status_code == 400, refused.text
        custom = await browser.post(f"/api/tasks/{task}/external-links",
                                    json={"provider": "custom", "url": "http://127.0.0.1:8730/s/1"})
        assert custom.status_code == 400
        other = await browser.post(f"/api/tasks/{task}/external-links", json={"provider": "custom", "url": "https://example.com/a"})
        assert other.status_code == 201
        custom_loopback = await browser.put(f"/api/external-links/{other.json()['id']}", json={"url": "http://127.0.0.1:9/x"})
        assert custom_loopback.status_code == 400

"""A task's first rung, escalation and reviewer stay consistent with its assignee and review policy."""

import httpx
import pytest
from sqlalchemy import select, update

from app.main import app
from app.models.agent import AgentActor, AgentModelBinding, AgentModelCatalogEntry
from app.models.project import Project
from app.models.task import Task
from app.models.team_member import TeamMember, TeamMemberProfile
from app.services.task_routing_service import parse_text_routing
from tests.test_delivery_scenarios import delivery_store

__all__ = ["delivery_store"]

CATALOG = (
    # key, publisher, alias, reasoning tier, effort
    ("openai.gpt-sol.high", "openai", "gpt-sol", 2, "high"),
    ("openai.gpt-astra.high", "openai", "gpt-astra", 3, "high"),
    ("anthropic.claude-sonnet.high", "anthropic", "claude-sonnet", 2, "high"),
    ("anthropic.claude-opus.medium", "anthropic", "claude-opus", 3, "medium"),
    ("google.gemini-argon.default", "google", "gemini-argon", 2, "unknown"),
)
INSTRUCTIONS = "each acceptance criterion is checked against its evidence"


def _client():
    return httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test")


async def routing_scope(factory, scenario, *, policy=True, mode="refuse"):
    """Two worker rows from two vendors and one verifier per vendor, in the scenario's first iteration."""
    async with factory() as db:
        await db.execute(update(Project).where(Project.id == scenario.projects[0])
                         .values(require_different_review_publisher=policy, routing_conflict_mode=mode))
        entries = {}
        for key, publisher, alias, tier, effort in CATALOG:
            entries[key] = AgentModelCatalogEntry(key=key, provider=publisher, publisher_key=publisher, configured_model_alias=alias,
                                                  reasoning_tier=tier, effort=effort, context_tier="large", modality_tags=["text"],
                                                  cost_tier="medium", latency_tier="balanced")
        db.add_all(entries.values())
        profiles, members = {}, {}
        for name, mode_name, key in (("gpt", "execution", "openai.gpt-sol.high"), ("sonnet", "execution", "anthropic.claude-sonnet.high"),
                                     ("opus-review", "verification", "anthropic.claude-opus.medium"),
                                     ("astra-review", "verification", "openai.gpt-astra.high")):
            profile = TeamMemberProfile(seed_key=f"routing-{name}", display_name=name, profile_kind="agent",
                                        automation_enabled=True, assignment_modes=[mode_name])
            actor = AgentActor(name=f"routing-{name}", display_name=name, api_key_hash=f"routing-{name}-hash",
                               role="verifier" if mode_name == "verification" else "worker", scopes='["tasks:read"]', profile=profile)
            db.add_all([profile, actor])
            await db.flush()
            db.add(AgentModelBinding(actor_id=actor.id, model_catalog_id=entries[key].id, is_default=True))
            profiles[name] = profile
            if mode_name == "execution":
                members[name] = TeamMember(name=f"{name} row", position="Agent", profile=profile, iteration_id=scenario.iterations[0])
                db.add(members[name])
        await db.commit()
        return {name: member.id for name, member in members.items()}, {name: profile.id for name, profile in profiles.items()}


def gpt_routing(profiles):
    return {"first_rung": {"catalog_key": "openai.gpt-sol.high", "harness": "Codex"},
            "escalation": [{"catalog_key": "openai.gpt-astra.high", "harness": "Codex"}],
            "after_last_rung": "the owner decides",
            "reviewer": {"catalog_key": "anthropic.claude-opus.medium", "profile_id": profiles["opus-review"], "instructions": INSTRUCTIONS},
            "notes": "A provider outage or a rate limit is not a reason to escalate."}


def brief(routing=None, **fields):
    body = {"goal": "Ship the change", "scope": "The change", "acceptance_criteria": [{"text": "It works"}],
            "verification": "Run the tests.", **fields}
    if routing is not None:
        body["routing"] = routing
    return body


async def create_task(client, scenario, assignee_id, routing, title="Routed work"):
    response = await client.post(f"/api/iterations/{scenario.iterations[0]}/tasks",
                                 json={"title": title, "assignee_id": assignee_id, "effort_hours": 4, "brief": brief(routing)})
    assert response.status_code == 201, response.text
    return response.json()


async def test_routing_is_validated_structure_and_the_brief_renders_it(delivery_store):
    factory, scenario, _ = delivery_store
    members, profiles = await routing_scope(factory, scenario)
    async with _client() as client:
        created = await create_task(client, scenario, members["gpt"], gpt_routing(profiles))
        routing = created["brief"]["routing"]
        assert routing["first_rung"] == {"catalog_key": "openai.gpt-sol.high", "harness": "Codex", "effort": "high",
                                         "publisher_key": "openai", "configured_model_alias": "gpt-sol"}
        assert routing["reviewer"]["publisher_key"] == "anthropic"
        assert created["routing_check"]["consistent"] is True and created["routing_check"]["issues"] == []
        description = created["description"]
        assert "## Routing\nFirst rung: openai.gpt-sol.high at high effort in Codex." in description
        assert ("Escalation after 2 failed acceptance runs: openai.gpt-astra.high at high effort in Codex; "
                "then the owner decides.") in description
        assert (f"Reviewer: anthropic.claude-opus.medium at medium effort, publisher anthropic, reviewer profile {profiles['opus-review']}."
                in description)
        assert f"Independent review by anthropic.claude-opus.medium: {INSTRUCTIONS}" in description
        assert description.index("## Verification") < description.index("## Routing")

        unknown = await client.put(f"/api/tasks/{created['id']}", json={"expected_version": created["version"],
            "brief": brief({**gpt_routing(profiles), "reviewer": {"catalog_key": "unknown.model"}})})
        assert unknown.status_code == 400 and "unknown model catalog entry unknown.model" in unknown.text

        # A writer that does not send routing keeps it.
        kept = await client.put(f"/api/tasks/{created['id']}", json={"expected_version": created["version"],
            "brief": brief(goal="Ship the reviewed change")})
        assert kept.status_code == 200, kept.text
        assert kept.json()["brief"]["routing"] == routing and kept.json()["routing_check"] is None

    async with factory() as db:
        task = await db.get(Task, created["id"])
        assert "routing" in task.brief and task.brief["routing"]["first_rung"]["effort"] == "high"
        plain = await db.get(Task, scenario.tasks["planned"])
        assert plain.brief is None


async def test_reassignment_to_another_vendor_is_refused_with_a_consistent_routing(delivery_store):
    factory, scenario, _ = delivery_store
    members, profiles = await routing_scope(factory, scenario)
    async with _client() as client:
        created = await create_task(client, scenario, members["gpt"], gpt_routing(profiles))
        path = f"/api/tasks/{created['id']}"
        refused = await client.put(path, json={"assignee_id": members["sonnet"], "expected_version": created["version"]})
        assert refused.status_code == 409, refused.text
        detail = refused.json()["detail"]
        assert detail["code"] == "routing_inconsistent"
        check = detail["routing_check"]
        assert check["different_publisher_required"] is True and check["conflict_mode"] == "refuse"
        assert check["assignee_publishers"] == ["anthropic"]
        assert {issue["code"] for issue in check["issues"] if issue["severity"] == "conflict"} == {
            "first_rung_not_assignee_model", "reviewer_shares_assignee_publisher"}
        suggestion = check["suggestion"]
        assert suggestion["first_rung"]["catalog_key"] == "anthropic.claude-sonnet.high"
        assert [rung["catalog_key"] for rung in suggestion["escalation"]] == ["anthropic.claude-opus.medium"]
        assert suggestion["reviewer"]["catalog_key"] == "openai.gpt-astra.high"
        assert suggestion["reviewer"]["profile_id"] == profiles["astra-review"]
        assert suggestion["reviewer"]["instructions"] == INSTRUCTIONS
        assert check["suggested_reviewer"] == suggestion["reviewer"]
        unchanged = (await client.get(path)).json()
        assert unchanged["version"] == created["version"] and unchanged["assignee"]["id"] == members["gpt"]

        # A reviewer change that shares the assignee's publisher is refused the same way.
        same_vendor = {**gpt_routing(profiles), "escalation": [],
                       "reviewer": {"catalog_key": "openai.gpt-astra.high", "profile_id": profiles["astra-review"]}}
        reviewer = await client.put(path, json={"expected_version": created["version"], "brief": brief(same_vendor)})
        assert reviewer.status_code == 409, reviewer.text
        assert [issue["code"] for issue in reviewer.json()["detail"]["routing_check"]["issues"]] == ["reviewer_shares_assignee_publisher"]
        assert reviewer.json()["detail"]["routing_check"]["suggested_reviewer"]["publisher_key"] in {"anthropic", "google"}

        preview = await client.get(f"{path}/routing/check", params={"assignee_id": members["sonnet"]})
        assert preview.status_code == 200 and preview.json()["suggestion"] == suggestion

        applied = await client.put(path, json={"assignee_id": members["sonnet"], "expected_version": created["version"],
                                               "routing_resolution": "apply_suggestion"})
        assert applied.status_code == 200, applied.text
        body = applied.json()
        assert body["assignee"]["id"] == members["sonnet"]
        assert body["routing_check"]["applied"] is True and body["routing_check"]["consistent"] is True
        assert body["brief"]["routing"]["first_rung"]["catalog_key"] == "anthropic.claude-sonnet.high"
        assert body["brief"]["routing"]["reviewer"]["catalog_key"] == "openai.gpt-astra.high"
        assert body["brief"]["routing"]["notes"] == gpt_routing(profiles)["notes"]
        assert "First rung: anthropic.claude-sonnet.high at high effort." in body["description"]
        assert "Independent review by openai.gpt-astra.high" in body["description"]
        assert "gpt-sol" not in body["description"]
        assert body["brief_revision"] == created["brief_revision"] + 1


async def test_warn_mode_saves_the_reassignment_and_answers_with_the_suggestion(delivery_store):
    factory, scenario, _ = delivery_store
    members, profiles = await routing_scope(factory, scenario, mode="warn")
    async with _client() as client:
        created = await create_task(client, scenario, members["gpt"], gpt_routing(profiles))
        warned = await client.put(f"/api/tasks/{created['id']}", json={"assignee_id": members["sonnet"], "expected_version": created["version"]})
        assert warned.status_code == 200, warned.text
        body = warned.json()
        assert body["assignee"]["id"] == members["sonnet"]
        assert body["brief"]["routing"] == created["brief"]["routing"]
        check = body["routing_check"]
        assert check["conflict_mode"] == "warn" and check["consistent"] is False and check["applied"] is False
        assert check["suggested_reviewer"]["catalog_key"] == "openai.gpt-astra.high"


async def test_without_the_publisher_policy_only_the_first_rung_must_follow_the_assignee(delivery_store):
    factory, scenario, _ = delivery_store
    members, profiles = await routing_scope(factory, scenario, policy=False)
    async with _client() as client:
        created = await create_task(client, scenario, members["gpt"], {**gpt_routing(profiles), "reviewer": {"catalog_key": "openai.gpt-astra.high"}})
        assert created["routing_check"]["consistent"] is True
        refused = await client.put(f"/api/tasks/{created['id']}", json={"assignee_id": members["sonnet"], "expected_version": created["version"]})
        assert refused.status_code == 409
        assert [issue["code"] for issue in refused.json()["detail"]["routing_check"]["issues"]] == ["first_rung_not_assignee_model"]
        suggestion = refused.json()["detail"]["routing_check"]["suggestion"]
        # Without the policy the reviewer is kept.
        assert suggestion["reviewer"]["catalog_key"] == "openai.gpt-astra.high"


async def test_bulk_cross_vendor_reassignment_leaves_every_task_consistent(delivery_store):
    factory, scenario, _ = delivery_store
    members, profiles = await routing_scope(factory, scenario)
    path = "/api/tasks/bulk-operations"
    async with _client() as client:
        tasks = [await create_task(client, scenario, members["gpt"], gpt_routing(profiles), title=f"Routed work {index}") for index in range(3)]
        ids = [task["id"] for task in tasks]
        request = {"task_ids": ids, "action": "set_assignee", "payload": {"assignee_id": members["sonnet"]}}

        refused = await client.post(path, json=request)
        assert refused.status_code == 200, refused.text
        assert {item["outcome"] for item in refused.json()["results"]} == {"failed"}
        assert all(item["routing_check"]["suggestion"] for item in refused.json()["results"])

        request["payload"]["routing_resolution"] = "apply_suggestion"
        preview = await client.post(path, json=request)
        assert preview.status_code == 200, preview.text
        assert {item["outcome"] for item in preview.json()["results"]} == {"would_update"}
        assert all(item["routing_check"]["consistent"] for item in preview.json()["results"])

        applied = await client.post(path, json={**request, "dry_run": False, "expected_versions": preview.json()["task_versions"],
                                                "expected_revisions": preview.json()["input_revisions"]})
        assert applied.status_code == 200, applied.text
        assert {item["outcome"] for item in applied.json()["results"]} == {"updated"}
        for task_id in ids:
            task = (await client.get(f"/api/tasks/{task_id}")).json()
            routing = task["brief"]["routing"]
            assert task["assignee"]["id"] == members["sonnet"]
            assert routing["first_rung"]["publisher_key"] == "anthropic"
            assert all(rung["publisher_key"] == "anthropic" for rung in routing["escalation"])
            assert routing["reviewer"]["publisher_key"] == "openai"
            check = (await client.get(f"/api/tasks/{task_id}/routing/check")).json()
            assert check["consistent"] is True and check["issues"] == [], check

        # Moving them back restores a consistent routing for the first vendor.
        versions = {str(task_id): (await client.get(f"/api/tasks/{task_id}")).json()["version"] for task_id in ids}
        back = {"task_ids": ids, "action": "set_assignee",
                "payload": {"assignee_id": members["gpt"], "routing_resolution": "apply_suggestion"}}
        preview = await client.post(path, json=back)
        applied = await client.post(path, json={**back, "dry_run": False, "expected_versions": versions,
                                                "expected_revisions": preview.json()["input_revisions"]})
        assert applied.status_code == 200, applied.text
        for task_id in ids:
            routing = (await client.get(f"/api/tasks/{task_id}")).json()["brief"]["routing"]
            assert routing["first_rung"]["catalog_key"] == "openai.gpt-sol.high"
            assert routing["reviewer"]["publisher_key"] == "anthropic"
            assert (await client.get(f"/api/tasks/{task_id}/routing/check")).json()["consistent"] is True


TEXT_CONTEXT = (
    "Background.\n\n### Difficulty and routing requirements\nAxes 2, 1, 3, 2, 2; band advanced. "
    "First rung: gpt-sol at high effort in Codex. Review mode: independent.\n\n"
    "### Handoff and escalation\nReviewer: Claude Code Opus (claude-opus) at medium effort, from a different vendor than the implementer. "
    "Submit for review with evidence for each criterion. After two failed acceptance runs the task moves to Codex GPT-Astra. "
    "A provider outage or a rate limit is not a reason to escalate."
)
TEXT_VERIFICATION = f"Run the tests. Independent review by Claude Code Opus at medium effort: {INSTRUCTIONS}."
SENTENCES = (
    "First rung: gpt-sol at high effort in Codex.",
    "Reviewer: Claude Code Opus (claude-opus) at medium effort, from a different vendor than the implementer.",
    "After two failed acceptance runs the task moves to Codex GPT-Astra.",
    f"Independent review by Claude Code Opus at medium effort: {INSTRUCTIONS}.",
)


async def test_text_routing_converts_without_loss(delivery_store):
    factory, scenario, _ = delivery_store
    members, profiles = await routing_scope(factory, scenario)
    async with _client() as client:
        created = await create_task(client, scenario, members["gpt"], None)
        path = f"/api/tasks/{created['id']}"
        written = await client.put(path, json={"expected_version": created["version"],
                                               "brief": brief(context=TEXT_CONTEXT, verification=TEXT_VERIFICATION)})
        assert written.status_code == 200, written.text
        version = written.json()["version"]
        # Text routing keeps working and is reported, not refused, on a reassignment check.
        check = (await client.get(f"{path}/routing/check", params={"assignee_id": members["sonnet"]})).json()
        assert check["structured"] is False and check["text_routing"] is True
        assert [issue["code"] for issue in check["issues"]] == ["routing_in_text"]

        preview = await client.post(f"{path}/routing/convert", json={"expected_version": version})
        assert preview.status_code == 200, preview.text
        result = preview.json()
        assert result["applied"] is False and result["unresolved"] == []
        assert sorted(result["removed"]) == sorted(SENTENCES)
        routing = result["routing"]
        assert routing["first_rung"]["catalog_key"] == "openai.gpt-sol.high" and routing["first_rung"]["harness"] == "Codex"
        assert [rung["catalog_key"] for rung in routing["escalation"]] == ["openai.gpt-astra.high"]
        assert routing["escalate_after_failed_runs"] == 2
        assert routing["reviewer"]["catalog_key"] == "anthropic.claude-opus.medium"
        assert routing["reviewer"]["instructions"] == INSTRUCTIONS
        assert result["check"]["consistent"] is True
        assert (await client.get(path)).json()["brief"].get("routing") is None

        applied = await client.post(f"{path}/routing/convert", json={"expected_version": version, "apply": True})
        assert applied.status_code == 200, applied.text
        task = (await client.get(path)).json()
        stored = task["brief"]
        assert stored["routing"]["source_text"] == result["removed"]
        for sentence in SENTENCES:
            assert sentence not in stored["context"] + stored["verification"]
        assert "Review mode: independent." in stored["context"]
        assert "A provider outage or a rate limit is not a reason to escalate." in stored["context"]
        assert stored["verification"] == "Run the tests."
        assert "## Routing\nFirst rung: openai.gpt-sol.high at high effort in Codex." in task["description"]

        again = await client.post(f"{path}/routing/convert", json={"expected_version": task["version"]})
        assert again.json()["already_structured"] is True

        # The converted routing now follows a reassignment.
        moved = await client.put(path, json={"assignee_id": members["sonnet"], "expected_version": task["version"],
                                             "routing_resolution": "apply_suggestion"})
        assert moved.status_code == 200, moved.text
        assert moved.json()["brief"]["routing"]["source_text"] == result["removed"]


async def test_ambiguous_text_routing_stays_as_text_until_the_caller_settles_it(delivery_store):
    factory, scenario, _ = delivery_store
    members, profiles = await routing_scope(factory, scenario)
    async with factory() as db:
        db.add(AgentModelCatalogEntry(key="openai.gpt-astra.xhigh", provider="openai", publisher_key="openai",
                                      configured_model_alias="gpt-astra", reasoning_tier=3, effort="xhigh", context_tier="large",
                                      modality_tags=["text"], cost_tier="high", latency_tier="slow"))
        await db.commit()
    async with _client() as client:
        created = await create_task(client, scenario, members["gpt"], None)
        path = f"/api/tasks/{created['id']}"
        written = await client.put(path, json={"expected_version": created["version"],
                                               "brief": brief(context=TEXT_CONTEXT, verification=TEXT_VERIFICATION)})
        version = written.json()["version"]
        preview = (await client.post(f"{path}/routing/convert", json={"expected_version": version})).json()
        assert preview["unresolved"] == ["After two failed acceptance runs the task moves to Codex GPT-Astra."]
        assert preview["routing"]["escalation"] == []
        assert preview["unresolved"][0] in preview["brief"]["context"]

        settled = {**preview["routing"], "escalation": [{"catalog_key": "openai.gpt-astra.xhigh"}], "source_text": []}
        applied = await client.post(f"{path}/routing/convert", json={"expected_version": version, "apply": True, "routing": settled})
        assert applied.status_code == 200, applied.text
        stored = (await client.get(path)).json()["brief"]
        assert "moves to Codex GPT-Astra" not in stored["context"]
        assert sorted(stored["routing"]["source_text"]) == sorted(SENTENCES)
        assert stored["routing"]["escalation"][0]["effort"] == "xhigh"


def test_parser_reads_the_inline_ladder_format():
    entries = [AgentModelCatalogEntry(id=index, key=key, provider=publisher, publisher_key=publisher, configured_model_alias=alias,
                                      reasoning_tier=tier, effort=effort, enabled=True)
               for index, (key, publisher, alias, tier, effort) in enumerate(CATALOG, start=1)]
    text = ("Read the merged code first. Routing: band standard; first rung claude-sonnet @ high; "
            "escalation gpt-astra @ high -> claude-opus @ medium; after the last rung the task is blocked and the owner decides. "
            "Paths: the runner checks them.")
    routing, cleaned, removed, unresolved = parse_text_routing({"context": text, "verification": ""}, entries)
    assert unresolved == []
    assert routing["first_rung"]["catalog_key"] == "anthropic.claude-sonnet.high"
    assert [rung["catalog_key"] for rung in routing["escalation"]] == ["openai.gpt-astra.high", "anthropic.claude-opus.medium"]
    assert routing["after_last_rung"] == "after the last rung the task is blocked and the owner decides"
    assert cleaned["context"] == "Read the merged code first. Routing: band standard. Paths: the runner checks them."
    assert len(removed) == 1


async def test_routing_conflict_mode_is_an_operator_setting(delivery_store):
    factory, scenario, _ = delivery_store
    async with _client() as client:
        current = (await client.get(f"/api/projects/{scenario.projects[0]}")).json()
        assert current["routing_conflict_mode"] == "refuse"
    async with factory() as db:
        assert (await db.scalar(select(Project.routing_conflict_mode).where(Project.id == scenario.projects[0]))) == "refuse"


async def test_mcp_tools_check_and_convert_routing(delivery_store):
    from app import mcp_agent_tools
    factory, scenario, _ = delivery_store
    members, profiles = await routing_scope(factory, scenario)
    async with _client() as client:
        created = await create_task(client, scenario, members["gpt"], None)
        written = await client.put(f"/api/tasks/{created['id']}", json={"expected_version": created["version"],
                                   "brief": brief(context=TEXT_CONTEXT, verification=TEXT_VERIFICATION)})
        version = written.json()["version"]
    async with factory() as db:
        actor = await db.get(AgentActor, scenario.actors[0])
        converted = await mcp_agent_tools.convert_task_routing(db, actor, created["id"], {"expected_version": version, "apply": True})
        assert converted["applied"] is True and converted["routing"]["first_rung"]["catalog_key"] == "openai.gpt-sol.high"
    async with factory() as db:
        actor = await db.get(AgentActor, scenario.actors[0])
        check = await mcp_agent_tools.check_task_routing(db, actor, created["id"], members["sonnet"])
        assert check["structured"] is True and check["consistent"] is False
        assert check["suggested_reviewer"]["publisher_key"] == "openai"
    from app.mcp_server import mcp
    tools = {tool.name: tool for tool in await mcp.list_tools()}
    assert tools["agent_get_task_routing_check"].annotations.readOnlyHint is True
    assert tools["agent_convert_task_routing"].annotations.readOnlyHint is False

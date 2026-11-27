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
        # A routing-only change keeps the brief revision that evidence binds to.
        assert body["brief_revision"] == created["brief_revision"]


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
        for item in preview.json()["results"]:
            assert item["routing_check"]["consistent"] and item["routing_check"]["applied"]
            # The preview names the routing it would save next to the assignee change.
            assert item["changes"]["assignee_id"]["new"] == members["sonnet"]
            assert item["changes"]["routing"]["old"]["first_rung"]["catalog_key"] == "openai.gpt-sol.high"
            assert item["changes"]["routing"]["new"]["first_rung"]["catalog_key"] == "anthropic.claude-sonnet.high"
        async with factory() as db:
            assert {task.assignee_id for task in (await db.scalars(select(Task).where(Task.id.in_(ids)))).all()} == {members["gpt"]}

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
    "Submit for review with evidence for each criterion. After two failed acceptance runs the task moves to gpt-astra. "
    "A provider outage or a rate limit is not a reason to escalate."
)
TEXT_VERIFICATION = f"Run the tests. Independent review by claude-opus at medium effort: {INSTRUCTIONS}."
SENTENCES = (
    "First rung: gpt-sol at high effort in Codex.",
    "Reviewer: Claude Code Opus (claude-opus) at medium effort, from a different vendor than the implementer.",
    "After two failed acceptance runs the task moves to gpt-astra.",
    f"Independent review by claude-opus at medium effort: {INSTRUCTIONS}.",
)


async def write_text_brief(client, scenario, members, context=TEXT_CONTEXT, verification=TEXT_VERIFICATION):
    created = await create_task(client, scenario, members["gpt"], None)
    written = await client.put(f"/api/tasks/{created['id']}", json={"expected_version": created["version"],
                               "brief": brief(context=context, verification=verification)})
    assert written.status_code == 200, written.text
    return written.json()


async def test_text_routing_converts_without_loss(delivery_store):
    factory, scenario, _ = delivery_store
    members, profiles = await routing_scope(factory, scenario)
    async with _client() as client:
        written = await write_text_brief(client, scenario, members)
        path, version = f"/api/tasks/{written['id']}", written["version"]
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
        assert routing["reviewer"]["instructions"] == f"{INSTRUCTIONS}."
        assert result["check"]["consistent"] is True
        assert (await client.get(path)).json()["brief"].get("routing") is None

        applied = await client.post(f"{path}/routing/convert", json={"expected_version": version, "apply": True})
        assert applied.status_code == 200, applied.text
        task = (await client.get(path)).json()
        stored = task["brief"]
        assert stored["routing"]["source_text"] == result["removed"]
        for sentence in SENTENCES:
            assert sentence not in stored["context"] + stored["verification"]
        assert "band advanced. Review mode: independent." in stored["context"]
        assert "A provider outage or a rate limit is not a reason to escalate." in stored["context"]
        assert stored["verification"] == "Run the tests."
        assert "## Routing\nFirst rung: openai.gpt-sol.high at high effort in Codex." in task["description"]
        assert f"Independent review by anthropic.claude-opus.medium: {INSTRUCTIONS}." in task["description"]

        again = await client.post(f"{path}/routing/convert", json={"expected_version": task["version"]})
        assert again.json()["already_structured"] is True and again.json()["applied"] is False
        assert (await client.get(path)).json()["version"] == task["version"]

        # The converted routing now follows a reassignment.
        moved = await client.put(path, json={"assignee_id": members["sonnet"], "expected_version": task["version"],
                                             "routing_resolution": "apply_suggestion"})
        assert moved.status_code == 200, moved.text
        assert moved.json()["brief"]["routing"]["source_text"] == result["removed"]


async def test_conversion_without_routing_text_changes_nothing(delivery_store):
    factory, scenario, _ = delivery_store
    members, _ = await routing_scope(factory, scenario)
    async with _client() as client:
        written = await write_text_brief(client, scenario, members, context="Plain background.", verification="Run the tests.")
        path = f"/api/tasks/{written['id']}"
        for apply in (False, True):
            response = await client.post(f"{path}/routing/convert", json={"expected_version": written["version"], "apply": apply})
            assert response.status_code == 200, response.text
            assert response.json()["applied"] is False and response.json()["routing"] is None
            assert response.json()["removed"] == []
        after = (await client.get(path)).json()
        assert after["version"] == written["version"] and after["brief_revision"] == written["brief_revision"]
        assert "routing" not in after["brief"] or after["brief"]["routing"] is None
        empty = await client.post(f"{path}/routing/convert", json={"expected_version": written["version"], "apply": True,
                                                                    "routing": {"notes": "Nothing else"}})
        assert empty.status_code == 422 and "nothing would be stored" in empty.text


async def test_ambiguous_text_routing_stays_as_text_until_the_caller_settles_it(delivery_store):
    factory, scenario, _ = delivery_store
    members, profiles = await routing_scope(factory, scenario)
    async with factory() as db:
        db.add(AgentModelCatalogEntry(key="openai.gpt-astra.xhigh", provider="openai", publisher_key="openai",
                                      configured_model_alias="gpt-astra", reasoning_tier=3, effort="xhigh", context_tier="large",
                                      modality_tags=["text"], cost_tier="high", latency_tier="slow"))
        await db.commit()
    async with _client() as client:
        written = await write_text_brief(client, scenario, members)
        path, version = f"/api/tasks/{written['id']}", written["version"]
        preview = (await client.post(f"{path}/routing/convert", json={"expected_version": version})).json()
        assert preview["unresolved"] == ["After two failed acceptance runs the task moves to gpt-astra."]
        assert preview["routing"]["escalation"] == []
        assert preview["unresolved"][0] in preview["brief"]["context"]

        settled = {**preview["routing"], "escalation": [{"catalog_key": "openai.gpt-astra.xhigh"}], "source_text": []}
        applied = await client.post(f"{path}/routing/convert", json={"expected_version": version, "apply": True, "routing": settled})
        assert applied.status_code == 200, applied.text
        stored = (await client.get(path)).json()["brief"]
        assert "moves to gpt-astra" not in stored["context"]
        assert sorted(stored["routing"]["source_text"]) == sorted(SENTENCES)
        assert stored["routing"]["escalation"][0]["effort"] == "xhigh"


async def test_remaining_routing_text_is_converted_into_an_existing_routing(delivery_store):
    factory, scenario, _ = delivery_store
    members, profiles = await routing_scope(factory, scenario)
    async with factory() as db:
        db.add(AgentModelCatalogEntry(key="openai.gpt-astra.xhigh", provider="openai", publisher_key="openai",
                                      configured_model_alias="gpt-astra", reasoning_tier=3, effort="xhigh", context_tier="large",
                                      modality_tags=["text"], cost_tier="high", latency_tier="slow"))
        await db.commit()
    async with _client() as client:
        written = await write_text_brief(client, scenario, members)
        path = f"/api/tasks/{written['id']}"
        first = await client.post(f"{path}/routing/convert", json={"expected_version": written["version"], "apply": True})
        assert first.json()["unresolved"] == ["After two failed acceptance runs the task moves to gpt-astra."]
        task = (await client.get(path)).json()
        # The owner settles the ambiguity in the text; the next conversion fills only the empty ladder.
        context = task["brief"]["context"].replace("moves to gpt-astra.", "moves to gpt-astra at xhigh effort.")
        edited = await client.put(path, json={"expected_version": task["version"], "brief": {**task["brief"], "context": context}})
        assert edited.status_code == 200, edited.text
        again = await client.post(f"{path}/routing/convert", json={"expected_version": edited.json()["version"], "apply": True})
        assert again.status_code == 200, again.text
        result = again.json()
        assert result["applied"] is True and result["already_structured"] is False
        assert result["removed"] == ["After two failed acceptance runs the task moves to gpt-astra at xhigh effort."]
        stored = (await client.get(path)).json()["brief"]
        assert [rung["catalog_key"] for rung in stored["routing"]["escalation"]] == ["openai.gpt-astra.xhigh"]
        assert stored["routing"]["first_rung"]["catalog_key"] == "openai.gpt-sol.high"
        assert "moves to gpt-astra" not in stored["context"]


def catalog_entries_for_parser(*extra):
    rows = CATALOG + extra
    return [AgentModelCatalogEntry(id=index, key=key, provider=publisher, publisher_key=publisher, configured_model_alias=alias,
                                   reasoning_tier=tier, effort=effort, enabled=True)
            for index, (key, publisher, alias, tier, effort) in enumerate(rows, start=1)]


def test_parser_reads_the_inline_ladder_format():
    text = ("Read the merged code first. Routing: band standard; first rung claude-sonnet @ high; "
            "escalation gpt-astra @ high -> claude-opus @ medium; after the last rung the task is blocked and the owner decides. "
            "Paths: the runner checks them.")
    routing, cleaned, removed, unresolved = parse_text_routing({"context": text, "verification": ""}, catalog_entries_for_parser())
    assert unresolved == []
    assert routing["first_rung"]["catalog_key"] == "anthropic.claude-sonnet.high"
    assert [rung["catalog_key"] for rung in routing["escalation"]] == ["openai.gpt-astra.high", "anthropic.claude-opus.medium"]
    assert routing["after_last_rung"] == "after the last rung the task is blocked and the owner decides"
    assert cleaned["context"] == "Read the merged code first. Routing: band standard. Paths: the runner checks them."
    assert len(removed) == 1


def test_parser_matches_only_an_exact_key_or_alias_at_its_stated_effort():
    entries = catalog_entries_for_parser(("openai.gpt-5.high", "openai", "gpt-5", 2, "high"))
    context = ("First rung: GPT-5 mini at high effort in Codex.\n"
               "Reviewer: Antigravity Gemini (gemini-argon) at high effort, a different vendor.\n"
               "After two failed acceptance runs the task moves to Claude Code Opus.")
    routing, cleaned, removed, unresolved = parse_text_routing({"context": context, "verification": ""}, entries)
    # A longer name is not the model it contains, and an entry with an unknown effort is not "high".
    assert removed == [] and len(unresolved) == 3
    assert "first_rung" not in routing and "reviewer" not in routing and routing["escalation"] == []
    assert cleaned["context"] == context
    exact, _, removed, unresolved = parse_text_routing(
        {"context": "First rung: GPT-5 at high effort in Codex. Reviewer: Gemini (gemini-argon) at default effort, other vendor.",
         "verification": ""}, entries)
    assert unresolved == [] and exact["first_rung"]["catalog_key"] == "openai.gpt-5.high"
    assert exact["reviewer"]["catalog_key"] == "google.gemini-argon.default"


def test_parser_tidies_only_the_line_a_sentence_left():
    context = ("Notes before.\n"
               "- item one\n"
               "    -  nested   item  kept\n"
               "```\n"
               "code    block   spacing\n"
               "```\n"
               "  Indented line. First rung: gpt-sol at high effort in Codex.   Tail  stays.\n"
               "Last line.")
    routing, cleaned, removed, _ = parse_text_routing({"context": context, "verification": ""}, catalog_entries_for_parser())
    assert removed == ["First rung: gpt-sol at high effort in Codex."]
    assert cleaned["context"] == ("Notes before.\n"
                                  "- item one\n"
                                  "    -  nested   item  kept\n"
                                  "```\n"
                                  "code    block   spacing\n"
                                  "```\n"
                                  "  Indented line. Tail stays.\n"
                                  "Last line.")


async def record_manual_provenance(factory, task_id, executor):
    import json
    from app.models.agent import TaskEvent
    from app.services.manual_provenance_service import EVENT_TYPE, SCHEMA
    async with factory() as db:
        task = await db.get(Task, task_id)
        record = {"schema": SCHEMA, "version": task.version, "brief_revision": task.brief_revision,
                  "artifact_revision": task.artifact_revision, "executor": executor, "commit_urls": [],
                  "head_commit_url": "https://github.com/example/repo/commit/" + "a" * 40}
        db.add(TaskEvent(task_id=task_id, event_type=EVENT_TYPE, payload=json.dumps(record)))
        await db.commit()


async def current_provenance(factory, task_id):
    from app.services.manual_provenance_service import recorded_provenances
    async with factory() as db:
        return (await recorded_provenances(db, await db.get(Task, task_id)))[1]


async def test_routing_changes_keep_progress_and_evidence_of_resolved_work(delivery_store):
    factory, scenario, _ = delivery_store
    members, profiles = await routing_scope(factory, scenario)
    async with _client() as client:
        created = await create_task(client, scenario, members["gpt"], gpt_routing(profiles))
        path = f"/api/tasks/{created['id']}"
        criterion = created["brief"]["acceptance_criteria"][0]
        progress = await client.post(f"{path}/progress", json={"expected_version": created["version"], "criteria": [
            {"criterion_id": criterion["id"], "criterion_revision": criterion["revision"], "state": "completed", "evidence": "Tests pass"}],
            "artifacts": ["https://github.com/example/repo/commit/" + "a" * 40]})
        assert progress.status_code == 200, progress.text
    async with factory() as db:
        await db.execute(update(Task).where(Task.id == created["id"]).values(status="resolved"))
        await db.commit()
    await record_manual_provenance(factory, created["id"], {"kind": "human", "principal_id": 1, "profile_ids": []})
    assert await current_provenance(factory, created["id"]) is not None
    async with _client() as client:
        before = (await client.get(path)).json()
        assert before["progress"] is not None
        moved = await client.put(path, json={"assignee_id": members["sonnet"], "expected_version": before["version"],
                                             "routing_resolution": "apply_suggestion"})
        assert moved.status_code == 200, moved.text
        after = moved.json()
        assert after["brief"]["routing"]["first_rung"]["catalog_key"] == "anthropic.claude-sonnet.high"
        assert after["progress"] == before["progress"]
        assert (after["brief_revision"], after["artifact_revision"]) == (before["brief_revision"], before["artifact_revision"])
        assert await current_provenance(factory, created["id"]) is not None

        # A routing-only brief edit keeps them too, and the timeline keeps both routings.
        edited = await client.put(path, json={"expected_version": after["version"],
            "brief": {**after["brief"], "routing": {**after["brief"]["routing"], "notes": "Escalate only after review."}}})
        assert edited.status_code == 200, edited.text
        assert edited.json()["progress"] == before["progress"] and edited.json()["brief_revision"] == before["brief_revision"]
        assert "Escalate only after review." in edited.json()["description"]
        assert await current_provenance(factory, created["id"]) is not None
    from app.models.agent import TaskEvent
    async with factory() as db:
        events = (await db.scalars(select(TaskEvent).where(TaskEvent.task_id == created["id"],
                                                           TaskEvent.event_type == "brief_routing_changed"))).all()
        assert len(events) == 2


async def test_recorded_contributor_publishers_bind_the_reviewer(delivery_store):
    factory, scenario, _ = delivery_store
    members, profiles = await routing_scope(factory, scenario)
    async with _client() as client:
        created = await create_task(client, scenario, members["gpt"], gpt_routing(profiles))
    # An agent of the reviewer's publisher already contributed through a manual provenance record.
    await record_manual_provenance(factory, created["id"], {"kind": "agent", "actor_id": scenario.actors[0],
                                                            "profile_id": profiles["sonnet"], "publisher_key": "anthropic"})
    async with _client() as client:
        check = (await client.get(f"/api/tasks/{created['id']}/routing/check")).json()
        assert "reviewer_shares_assignee_publisher" in {issue["code"] for issue in check["issues"] if issue["severity"] == "conflict"}
        # No verifier runs a model outside both publishers, so nothing consistent can be suggested.
        assert check["suggested_reviewer"] is None


async def test_reviewer_without_a_verifier_and_disabled_rungs_are_repaired(delivery_store):
    factory, scenario, _ = delivery_store
    members, profiles = await routing_scope(factory, scenario)
    async with _client() as client:
        unrunnable = {**gpt_routing(profiles), "reviewer": {"catalog_key": "google.gemini-argon.default"}}
        refused = await client.post(f"/api/iterations/{scenario.iterations[0]}/tasks",
                                    json={"title": "Unrunnable review", "assignee_id": members["gpt"], "brief": brief(unrunnable)})
        assert refused.status_code == 409, refused.text
        check = refused.json()["detail"]["routing_check"]
        assert [issue["code"] for issue in check["issues"]] == ["reviewer_has_no_verifier"]
        assert check["suggested_reviewer"]["catalog_key"] == "anthropic.claude-opus.medium"
        created = await create_task(client, scenario, members["gpt"], gpt_routing(profiles))
    async with factory() as db:
        await db.execute(update(AgentModelCatalogEntry).where(AgentModelCatalogEntry.key == "openai.gpt-astra.high").values(enabled=False))
        await db.commit()
    async with _client() as client:
        repaired = await client.put(f"/api/tasks/{created['id']}", json={"expected_version": created["version"],
                                                                         "routing_resolution": "apply_suggestion"})
        assert repaired.status_code == 200, repaired.text
        assert repaired.json()["brief"]["routing"]["escalation"] == []
        assert repaired.json()["routing_check"]["applied"] is True


async def test_suggestion_warns_when_the_new_first_rung_is_weaker(delivery_store):
    factory, scenario, _ = delivery_store
    members, profiles = await routing_scope(factory, scenario)
    async with factory() as db:
        await db.execute(update(AgentModelCatalogEntry).where(AgentModelCatalogEntry.key == "openai.gpt-sol.high")
                         .values(reasoning_tier=3, qualification_keys=["qualified.schema-review"]))
        await db.commit()
    async with _client() as client:
        created = await create_task(client, scenario, members["gpt"], gpt_routing(profiles))
        check = (await client.get(f"/api/tasks/{created['id']}/routing/check", params={"assignee_id": members["sonnet"]})).json()
        codes = {issue["code"] for issue in check["issues"]}
        assert {"suggested_first_rung_lower", "suggested_first_rung_missing_qualifications"} <= codes


async def test_removing_routing_during_a_reassignment_is_an_issue_under_the_policy(delivery_store):
    factory, scenario, _ = delivery_store
    members, profiles = await routing_scope(factory, scenario)
    async with _client() as client:
        created = await create_task(client, scenario, members["gpt"], gpt_routing(profiles))
        removed = await client.put(f"/api/tasks/{created['id']}", json={
            "expected_version": created["version"], "assignee_id": members["sonnet"], "brief": brief(None) | {"routing": None}})
        assert removed.status_code == 409, removed.text
        assert [issue["code"] for issue in removed.json()["detail"]["routing_check"]["issues"]] == ["routing_removed"]
        # Without a reassignment, removing the routing is an ordinary edit.
        cleared = await client.put(f"/api/tasks/{created['id']}", json={"expected_version": created["version"],
                                                                        "brief": brief(None) | {"routing": None}})
        assert cleared.status_code == 200 and cleared.json()["brief"]["routing"] is None


async def test_routing_conflict_mode_is_an_operator_setting(delivery_store):
    from app.authority import Authority, AuthorityError
    factory, scenario, _ = delivery_store
    async with _client() as client:
        current = (await client.get(f"/api/projects/{scenario.projects[0]}")).json()
        assert current["routing_conflict_mode"] == "refuse"
    editor = Authority(1, "human", projects={scenario.projects[0]: "manager"})
    async with factory() as db:
        db.info["authority"] = editor
        project = await db.get(Project, scenario.projects[0])
        project.routing_conflict_mode = "warn"
        with pytest.raises(AuthorityError, match="operator"):
            await db.flush()
        await db.rollback()
        db.add(Project(name="Relaxed project", routing_conflict_mode="warn"))
        with pytest.raises(AuthorityError, match="operator"):
            await db.flush()
        await db.rollback()
        with pytest.raises(AuthorityError, match="operator"):
            await db.execute(update(Project).where(Project.id == scenario.projects[0]).values(routing_conflict_mode="warn"))
        await db.rollback()
        assert Project(name="Default").routing_conflict_mode == "refuse"
    async with factory() as db:
        assert (await db.scalar(select(Project.routing_conflict_mode).where(Project.id == scenario.projects[0]))) == "refuse"


async def test_mcp_tools_check_and_convert_routing(delivery_store):
    from app import mcp_agent_tools
    factory, scenario, _ = delivery_store
    members, profiles = await routing_scope(factory, scenario)
    async with _client() as client:
        written = await write_text_brief(client, scenario, members)
    async with factory() as db:
        actor = await db.get(AgentActor, scenario.actors[0])
        converted = await mcp_agent_tools.convert_task_routing(db, actor, written["id"], {"expected_version": written["version"], "apply": True})
        assert converted["applied"] is True and converted["routing"]["first_rung"]["catalog_key"] == "openai.gpt-sol.high"
    async with factory() as db:
        actor = await db.get(AgentActor, scenario.actors[0])
        check = await mcp_agent_tools.check_task_routing(db, actor, written["id"], members["sonnet"])
        assert check["structured"] is True and check["consistent"] is False
        assert check["suggested_reviewer"]["publisher_key"] == "openai"
    from app.mcp_server import mcp
    tools = {tool.name: tool for tool in await mcp.list_tools()}
    assert tools["agent_get_task_routing_check"].annotations.readOnlyHint is True
    assert tools["agent_convert_task_routing"].annotations.readOnlyHint is False

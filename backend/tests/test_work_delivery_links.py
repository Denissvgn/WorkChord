"""A task records where its code went: branch, commits and pull request, and a release its merge PR or tag."""

from datetime import date

import pytest
from pydantic import ValidationError
from sqlalchemy import select

from app.mcp_agent_tools import create_release_github_link
from app.models.agent import AgentActor
from app.models.external_link import ExternalLink
from app.models.release import Release
from app.models.task import Task
from app.schemas.agent import AgentWorkBegin, AgentWorkSubmit, ModelAwareAgentWorkBegin
from app.services.agent_work_service import AgentConflictError
from app.utils.github_links import GitHubLinkError, parse_github_url
from tests.test_delivery_scenarios import delivery_store  # noqa: F401
from tests.test_schedule_follows_actual_dates import (
    _begin_next,
    _client,
    _headers,
    _seed,
    fixed_clock,  # noqa: F401
)

SHA_A = "0123456789abcdef0123456789abcdef01234567"
SHA_B = "fedcba9876543210fedcba9876543210fedcba98"
REPO = "https://github.com/example-org/example-repo"
BRANCH = f"{REPO}/tree/feature/wc-1-add-export"


def test_commit_urls_are_normalized_to_one_full_sha_spelling():
    direct = parse_github_url(f"{REPO}/commit/{SHA_A.upper()}")
    from_pr = parse_github_url(f"{REPO}/pull/7/commits/{SHA_A}")
    assert direct == from_pr
    assert direct.github_type == "commit"
    assert direct.url == f"{REPO}/commit/{SHA_A}"
    assert direct.external_key == f"example-org/example-repo@{SHA_A}"
    assert direct.metadata_json["sha"] == SHA_A


def test_a_short_commit_sha_is_refused():
    with pytest.raises(GitHubLinkError, match="full commit SHA"):
        parse_github_url(f"{REPO}/commit/0123456")


def test_release_tags_and_existing_link_kinds_parse():
    tag = parse_github_url(f"{REPO}/releases/tag/v1.4.0")
    assert (tag.github_type, tag.tag, tag.external_key) == (
        "tag", "v1.4.0", "example-org/example-repo@refs/tags/v1.4.0",
    )
    assert parse_github_url(f"{REPO}/pull/12").external_key == "example-org/example-repo#12"
    assert parse_github_url(BRANCH).branch == "feature/wc-1-add-export"
    with pytest.raises(GitHubLinkError):
        parse_github_url("https://gitlab.example.invalid/group/repo/-/commit/" + SHA_A)


def _submit_body(**links):
    return dict(
        assignment_id=1, run_id=1, claim_id="c" * 16, claim_generation=1, expected_task_version=1,
        summary="Done", evidence={"check": "ok"}, **links,
    )


def test_begin_accepts_only_a_branch_url():
    for build in (
        lambda url: AgentWorkBegin(assignment_id=1, queue_revision=1, branch_url=url),
        lambda url: ModelAwareAgentWorkBegin(assignment_id=1, queue_revision=1, model_binding_id=1,
                                             model_binding_revision=1, resolved_model_id="m", branch_url=url),
    ):
        assert build(BRANCH).branch_url == BRANCH
        with pytest.raises(ValidationError, match="branch"):
            build(f"{REPO}/pull/3")


def test_submit_commit_urls_must_be_commits_and_repeat_once():
    body = AgentWorkSubmit(**_submit_body(commit_urls=[
        f"{REPO}/commit/{SHA_A}", f"{REPO}/commit/{SHA_A.upper()}", f"{REPO}/commit/{SHA_B}",
    ]))
    assert body.commit_urls == [f"{REPO}/commit/{SHA_A}", f"{REPO}/commit/{SHA_B}"]
    with pytest.raises(ValidationError, match="commit"):
        AgentWorkSubmit(**_submit_body(commit_urls=[f"{REPO}/pull/3"]))


async def _task_links(factory, task_id):
    async with factory() as db:
        links = (await db.scalars(select(ExternalLink).where(
            ExternalLink.entity_type == "task", ExternalLink.entity_id == task_id,
        ).order_by(ExternalLink.id))).all()
        return [(link.provider, link.metadata_json["github_type"], link.url) for link in links]


async def test_begin_and_submit_link_the_branch_commits_and_pull_request(delivery_store, fixed_clock):
    factory, scenario, _ = delivery_store
    ids = await _seed(factory, scenario, {"only": (date(2026, 1, 20), date(2026, 1, 20), (), 1, True)})
    async with _client() as client:
        work = (await client.get("/api/agent/me/work", headers=_headers(scenario, "poll"))).json()
        begun = await client.post("/api/agent/me/work/begin", headers=_headers(scenario, "begin"), json={
            "assignment_id": work["next"]["assignment"]["id"], "queue_revision": work["queue_revision"],
            "lease_seconds": 60, "branch_url": BRANCH,
        })
        assert begun.status_code == 200, begun.text
        receipt = begun.json()
        assert [link["url"] for link in receipt["task"]["external_links"]] == [BRANCH]
        assert receipt["assignment"]["task_version"] == receipt["task"]["version"]

        body = dict(
            assignment_id=receipt["assignment"]["id"], run_id=receipt["run"]["id"],
            claim_id=receipt["claim_id"], claim_generation=receipt["claim_generation"],
            expected_task_version=receipt["task"]["version"],
            summary="Implemented result", evidence={"inspection": "Worker observation"},
            criterion_progress=[dict(criterion_id="result", criterion_revision=1, state="completed",
                                     evidence="Artifact inspected")],
            branch_url=BRANCH,
            commit_urls=[f"{REPO}/commit/{SHA_A}", f"{REPO}/commit/{SHA_B}"],
            # The older single field still takes any reviewable URL; only a GitHub one is linked.
            commit_url="https://ci.example.invalid/build/42",
            pr_url=f"{REPO}/pull/12",
        )
        submitted = await client.post("/api/agent/me/work/submit", headers=_headers(scenario, "submit"), json=body)
        assert submitted.status_code == 200, submitted.text
        assert submitted.json()["task"]["status"] == "resolved"
        replay = await client.post("/api/agent/me/work/submit", headers=_headers(scenario, "submit"), json=body)
        assert replay.status_code == 200, replay.text

    expected = [
        ("github", "branch", BRANCH),
        ("github", "commit", f"{REPO}/commit/{SHA_A}"),
        ("github", "commit", f"{REPO}/commit/{SHA_B}"),
        ("github", "pull_request", f"{REPO}/pull/12"),
    ]
    assert await _task_links(factory, ids["only"]) == expected
    assert [(link["metadata_json"]["github_type"], link["url"])
            for link in submitted.json()["task"]["external_links"]] == [item[1:] for item in expected]


async def test_a_submit_without_links_records_none(delivery_store, fixed_clock):
    factory, scenario, _ = delivery_store
    ids = await _seed(factory, scenario, {"only": (date(2026, 1, 20), date(2026, 1, 20), (), 1, True)})
    async with _client() as client:
        receipt = await _begin_next(client, scenario, "begin")
        submitted = await client.post("/api/agent/me/work/submit", headers=_headers(scenario, "submit"), json=dict(
            assignment_id=receipt["assignment"]["id"], run_id=receipt["run"]["id"],
            claim_id=receipt["claim_id"], claim_generation=receipt["claim_generation"],
            expected_task_version=receipt["task"]["version"],
            summary="Decision recorded", evidence={"decision": "No code change"},
            criterion_progress=[dict(criterion_id="result", criterion_revision=1, state="completed",
                                     evidence="Decision note")],
        ))
        assert submitted.status_code == 200, submitted.text
    assert await _task_links(factory, ids["only"]) == []
    async with factory() as db:
        assert (await db.get(Task, ids["only"])).status == "resolved"


async def test_a_pm_links_a_release_to_its_merge_pull_request_and_tag(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        release = Release(project_id=scenario.projects[0], name="Spring release")
        db.add(release)
        await db.commit()
        release_id = release.id
    command = dict(rationale="Trace the release to the code it shipped.", correlation_id="release-trace")
    async with factory() as db:
        pm = await db.get(AgentActor, scenario.actors[0])
        first = await create_release_github_link(db, pm, release_id, f"{REPO}/pull/40",
                                                 idempotency_key="release-pr", **command)
    async with factory() as db:
        pm = await db.get(AgentActor, scenario.actors[0])
        again = await create_release_github_link(db, pm, release_id, f"{REPO}/pull/40",
                                                 idempotency_key="release-pr", **command)
        assert again == first
    async with factory() as db:
        pm = await db.get(AgentActor, scenario.actors[0])
        await create_release_github_link(db, pm, release_id, f"{REPO}/releases/tag/v2.0.0",
                                         idempotency_key="release-tag", **command)
    async with factory() as db:
        pm = await db.get(AgentActor, scenario.actors[0])
        with pytest.raises(AgentConflictError, match="already exists"):
            await create_release_github_link(db, pm, release_id, f"{REPO}/pull/40",
                                             idempotency_key="release-pr-twice", **command)
    async with factory() as db:
        pm = await db.get(AgentActor, scenario.actors[0])
        assert await create_release_github_link(db, pm, release_id + 999, f"{REPO}/pull/40",
                                                idempotency_key="missing", **command) is None
        links = (await db.scalars(select(ExternalLink).where(
            ExternalLink.entity_type == "release", ExternalLink.entity_id == release_id,
        ).order_by(ExternalLink.id))).all()
        assert [(link.metadata_json["github_type"], link.url) for link in links] == [
            ("pull_request", f"{REPO}/pull/40"),
            ("tag", f"{REPO}/releases/tag/v2.0.0"),
        ]
    assert first["entity_type"] == "release" and first["external_key"] == "example-org/example-repo#40"

#!/usr/bin/env python3
"""Export deterministic mobile examples through the backend's canonical schemas."""

import argparse
from datetime import UTC, datetime
import json
from pathlib import Path

from starlette.responses import Response

from app.schemas.task import TaskResponse, TaskStatusChangeResponse, CascadeUpdateInfo
from app.schemas.task_brief import TaskBrief, BriefCriterion, TaskReviewResponse
from app.schemas.task_detail import TaskDetailResponse, TaskReference, TaskReferencePage
from app.schemas.task_domain import TaskActionsResponse, TaskActionAvailability
from app.services.session_service import _cookie_options
from app.services.task_service import TaskVersionConflictError
from generate_client_contract import build_contract

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "android-companion/app/src/test/resources/mobile-contract-v1.json"


def build_examples():
    brief = TaskBrief(goal="Deliver a reviewed outline", context="Coordinate with the team", scope="Write the outline",
        exclusions="Publishing", verification="Read the saved artifact", artifact_expectations="A versioned outline",
        acceptance_criteria=[BriefCriterion(id="outline", revision=2, text="The outline identifies the next delivery", verification="Open the saved outline")])
    leaf = TaskResponse(id=72, title="Review the outline", iteration_id=None, project_id=9, parent_id=71,
        description="Legacy text is retained independently", priority=3, effort_days=None, effort_hours=None,
        start_date=None, end_date=None, status="active", version=7, owner_profile_id=4, blocked_reason="Waiting for feedback",
        execution_mode="manual", brief=brief, brief_revision=3, artifact_revision=2,
        progress={"criteria": [{"criterion_id": "outline", "criterion_revision": 2, "state": "completed", "evidence": "Outline revision abc123"}],
                  "artifacts": [], "brief_revision": 3, "artifact_revision": 2})
    parent = leaf.model_copy(update={"id": 71, "title": "Delivery outline", "parent_id": None, "is_composite": True,
        "children": [leaf], "brief": None, "progress": None, "effort_hours": 1.5, "effort_days": 0.25,
        "nominal_day_hours": 6, "estimate_provenance": "estimated"})
    reference = TaskReference(id=72, title=leaf.title, version=7, status="active", project_id=9,
        iteration_id=None, parent_id=71, owner_profile_id=4, project_name="Shared delivery", iteration_name=None,
        blocked_reason=leaf.blocked_reason)
    page = TaskReferencePage(items=[reference], has_more=True, next_after_id=72, limit=1)
    empty = TaskReferencePage(items=[], has_more=False, next_after_id=None, limit=1)
    detail = TaskDetailResponse(task=leaf, ancestors=[reference.model_copy(update={"id": 71, "title": parent.title, "parent_id": None})],
        ancestors_complete=True, children=empty, dependencies=page)
    actions = TaskActionsResponse(task_id=72, version=7, claim_generation=0, running_run_ids=[], live_assignment_ids=[],
        actions=[TaskActionAvailability(action="resolve_manual", allowed=False, blockers=[{"code": "dependencies_incomplete", "message": "The prerequisite is not accepted"}]),
                 TaskActionAvailability(action="block", allowed=True)])
    changed = leaf.model_copy(update={"version": 8, "status": "resolved"})
    status = TaskStatusChangeResponse(task=changed, cascade_updates=[CascadeUpdateInfo(task_id=73, task_title="Follow-up",
        old_start_date=None, old_end_date=None, new_start_date="2026-10-05", new_end_date="2026-10-06")], notifications_sent=False)
    review = TaskReviewResponse(id=12, task_version=8, brief_revision=3, artifact_revision=2, principal_id=19,
        verdict="reject", reason="The artifact needs more detail", evidence="Independent review of abc123", created_at=datetime(2026, 10, 3, 12, tzinfo=UTC))
    legacy = leaf.model_dump(mode="json")
    for field in ("brief", "progress", "brief_revision", "artifact_revision", "blocked_reason", "execution_mode", "owner_profile_id", "owner", "estimate_provenance", "ownership_provenance", "nominal_day_hours"):
        legacy.pop(field, None)
    legacy.update(id=21, title="Legacy scheduled work", iteration_id=5, parent_id=None,
        description="## Acceptance criteria\n- [x] Legacy text alone is not execution evidence", status="planned")
    response = Response()
    cookie = _cookie_options()
    response.set_cookie(value="opaque-contract-example", **cookie)
    return {"schema_version": 1, "contract": build_contract(), "examples": {
        "nested_task": parent.model_dump(mode="json"), "backlog_task": leaf.model_dump(mode="json"),
        "legacy_task": legacy, "detail": detail.model_dump(mode="json"), "actions": actions.model_dump(mode="json"),
        "status_change": status.model_dump(mode="json"), "review": review.model_dump(mode="json"),
        "conflict": {"detail": TaskVersionConflictError(7, changed.model_dump(mode="json")).detail()},
        "cookie": {"name": cookie["key"], "header": response.headers["set-cookie"]}}}


def serialized_examples():
    return json.dumps(build_examples(), ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = serialized_examples()
    if args.check:
        if not args.output.exists() or args.output.read_text() != expected:
            parser.exit(1, "Mobile examples differ; regenerate and review consumer compatibility.\n")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(expected)


if __name__ == "__main__":
    main()

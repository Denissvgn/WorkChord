#!/usr/bin/env python3
"""Export a deterministic client contract from the registered backend schemas."""

import argparse
import json
from pathlib import Path

from app.main import app


CLIENT_PATHS = (
    "/api/auth/me", "/api/auth/logout", "/api/auth/native-token", "/api/auth/native-connections/start",
    "/api/auth/native-connections/exchange", "/api/auth/native-connections/{request_id}",
    "/api/auth/native-connections/{request_id}/approve", "/api/tasks/capabilities", "/api/tasks/my-work",
    "/api/tasks/review-queue", "/api/tasks/{task_id}/reviews", "/api/tasks/{task_id}/reviews/current", "/api/projects", "/api/iterations",
    "/api/session/whoami", "/api/iterations/{iteration_id}/tasks", "/api/tasks/{task_id}",
    "/api/tasks/{task_id}/status", "/api/tasks/{task_id}/move",
    "/api/triage/{triage_item_id}/convert-to-task",
    "/api/triage/{triage_item_id}/convert-to-backlog", "/api/projects/{project_id}/backlog",
    "/api/tasks/{task_id}/actions", "/api/tasks/{task_id}/commands", "/api/tasks/{task_id}/brief",
    "/api/tasks/{task_id}/brief/convert", "/api/tasks/{task_id}/progress", "/api/tasks/{task_id}/review",
    "/api/tasks/{task_id}/detail", "/api/tasks/lookup",
)
DEFAULT_OUTPUT = Path(__file__).resolve().parents[1] / "backend/tests/fixtures/client-contract-v1.json"


def build_contract():
    schema = app.openapi()
    missing = set(CLIENT_PATHS) - schema["paths"].keys()
    if missing:
        raise ValueError(f"Client routes no longer registered: {sorted(missing)}")
    paths = {path: schema["paths"][path] for path in CLIENT_PATHS}
    components = {}

    def collect(value):
        if isinstance(value, dict):
            ref = value.get("$ref", "")
            if ref.startswith("#/components/schemas/"):
                name = ref.removeprefix("#/components/schemas/")
                if name not in components:
                    components[name] = schema["components"]["schemas"][name]
                    collect(components[name])
            for child in value.values():
                collect(child)
        elif isinstance(value, list):
            for child in value:
                collect(child)

    collect(paths)
    task_fields = components["TaskResponse"]["properties"]
    return {
        "schema_version": 1,
        "api_version": app.version,
        "openapi": schema["openapi"],
        "paths": paths,
        "components": {"schemas": components},
        "schema_capabilities": {
            "task_allowed_actions": "/api/tasks/{task_id}/actions" in paths,
            "task_aggregate_revision": "iteration_revision" in task_fields,
            "canonical_work_metrics": "metric_contract_version" in task_fields,
            "task_structured_acceptance_criteria": "brief" in task_fields and "acceptance_criteria" in components["TaskBrief"]["properties"],
            "triage_explicit_destination": "/api/triage/{triage_item_id}/convert-to-backlog" in paths,
            "task_update_version_required": "expected_version" in components["TaskUpdate"].get("required", []),
        },
    }


def serialized_contract():
    return json.dumps(build_contract(), ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = serialized_contract()
    if args.check:
        if not args.output.exists() or args.output.read_text() != expected:
            parser.exit(1, "Client contract differs; regenerate and review consumer compatibility.\n")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(expected)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Validate, plan, apply, and inspect a WorkChord agent-team master."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import secrets
import sys
from typing import Any
from urllib import error, parse, request


def normalize_base_url(value: str) -> str:
    normalized = value.strip().rstrip("/")
    if not normalized:
        raise SystemExit("Base URL cannot be blank")
    return normalized


def normalize_api_prefix(value: str) -> str:
    return "/" + (value.strip() or "/api").strip("/")


def endpoint(base_url: str, api_prefix: str, operation: str) -> str:
    return (
        f"{normalize_base_url(base_url)}"
        f"{normalize_api_prefix(api_prefix)}"
        f"/agent/team-setup/{operation}"
    )


def load_object(path: Path, *, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise SystemExit(f"Cannot read {label}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{label} is not valid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise SystemExit(f"{label} must contain one JSON object")
    return value


def call_api(
    *,
    url: str,
    admin_key: str,
    method: str,
    payload: dict[str, Any] | None,
    timeout: float,
    headers: dict[str, str] | None = None,
) -> dict[str, Any]:
    if not admin_key:
        raise SystemExit(
            "WORKCHORD_ADMIN_API_KEY or --admin-key is required"
        )
    body = (
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode(
            "utf-8"
        )
        if payload is not None
        else None
    )
    request_headers = {
        "Accept": "application/json",
        "X-Admin-API-Key": admin_key,
    }
    if body is not None:
        request_headers["Content-Type"] = "application/json"
    if headers:
        request_headers.update(headers)
    req = request.Request(
        url,
        data=body,
        method=method,
        headers=request_headers,
    )
    try:
        with request.urlopen(req, timeout=timeout) as response:
            response_body = response.read().decode("utf-8")
    except error.HTTPError as exc:
        response_body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(
            f"Agent-team request failed: HTTP {exc.code}: {response_body}"
        ) from exc
    except error.URLError as exc:
        raise SystemExit(f"Agent-team request failed: {exc.reason}") from exc
    try:
        value = json.loads(response_body)
    except json.JSONDecodeError as exc:
        raise SystemExit(
            "Agent-team endpoint returned invalid JSON"
        ) from exc
    if not isinstance(value, dict):
        raise SystemExit("Agent-team endpoint returned a non-object response")
    return value


def common_payload(args: argparse.Namespace) -> dict[str, Any]:
    manifest = load_object(args.manifest, label="manifest")
    return {"manifest": manifest}


def run_validate(args: argparse.Namespace) -> dict[str, Any]:
    return call_api(
        url=endpoint(args.base_url, args.api_prefix, "validate"),
        admin_key=args.admin_key,
        method="POST",
        payload=common_payload(args),
        timeout=args.timeout,
    )


def run_plan(args: argparse.Namespace) -> dict[str, Any]:
    payload = common_payload(args)
    payload["expected_topology_revision"] = args.expected_revision
    return call_api(
        url=endpoint(args.base_url, args.api_prefix, "plan"),
        admin_key=args.admin_key,
        method="POST",
        payload=payload,
        timeout=args.timeout,
    )


def run_apply(args: argparse.Namespace) -> dict[str, Any]:
    plan = load_object(args.plan, label="plan")
    plan_action_ids = {
        str(action.get("action_id"))
        for action in plan.get("actions", [])
        if isinstance(action, dict) and action.get("action_id")
    }
    approved = tuple(dict.fromkeys(args.approve))
    confirmed = tuple(dict.fromkeys(args.confirm))
    unknown = sorted(set(approved).difference(plan_action_ids))
    if unknown:
        raise SystemExit(
            "Approved action IDs are not present in the plan: "
            + ", ".join(unknown)
        )
    if not approved:
        raise SystemExit("At least one exact --approve action ID is required")
    if not set(confirmed).issubset(approved):
        raise SystemExit("Every --confirm action ID must also be approved")
    payload = common_payload(args)
    payload.update(
        {
            "expected_topology_revision": plan[
                "expected_topology_revision"
            ],
            "plan_digest": plan["plan_digest"],
            "approved_action_ids": list(approved),
            "confirmed_action_ids": list(confirmed),
        }
    )
    return call_api(
        url=endpoint(args.base_url, args.api_prefix, "apply"),
        admin_key=args.admin_key,
        method="POST",
        payload=payload,
        timeout=args.timeout,
        headers={
            "Idempotency-Key": args.idempotency_key,
            "X-Agent-Rationale": args.rationale,
            "X-Correlation-ID": args.correlation_id,
        },
    )


def run_status(args: argparse.Namespace) -> dict[str, Any]:
    url = endpoint(args.base_url, args.api_prefix, "status")
    if args.topology_key:
        url += "?" + parse.urlencode({"topology_key": args.topology_key})
    return call_api(
        url=url,
        admin_key=args.admin_key,
        method="GET",
        payload=None,
        timeout=args.timeout,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Operate the digest-bound agent-team setup API without handling "
            "runtime credentials."
        )
    )
    parser.add_argument(
        "--base-url",
        default=os.getenv("WORKCHORD_BASE_URL", "http://localhost:8001"),
    )
    parser.add_argument(
        "--api-prefix",
        default=os.getenv("WORKCHORD_API_PREFIX", "/api"),
    )
    parser.add_argument(
        "--admin-key",
        default=os.getenv("WORKCHORD_ADMIN_API_KEY", ""),
        help="Defaults to WORKCHORD_ADMIN_API_KEY and is never printed.",
    )
    parser.add_argument("--timeout", type=float, default=15.0)
    commands = parser.add_subparsers(dest="command", required=True)

    validate = commands.add_parser("validate")
    validate.add_argument("manifest", type=Path)
    validate.set_defaults(handler=run_validate)

    plan = commands.add_parser("plan")
    plan.add_argument("manifest", type=Path)
    plan.add_argument("--expected-revision", type=int, required=True)
    plan.set_defaults(handler=run_plan)

    apply = commands.add_parser("apply")
    apply.add_argument("manifest", type=Path)
    apply.add_argument("--plan", type=Path, required=True)
    apply.add_argument("--approve", action="append", default=[])
    apply.add_argument("--confirm", action="append", default=[])
    apply.add_argument(
        "--idempotency-key",
        default=f"agent-team-{secrets.token_hex(12)}",
    )
    apply.add_argument(
        "--rationale",
        default="Apply approved agent-team reconciliation actions",
    )
    apply.add_argument(
        "--correlation-id",
        default=f"agent-team-cli-{secrets.token_hex(8)}",
    )
    apply.set_defaults(handler=run_apply)

    status = commands.add_parser("status")
    status.add_argument("--topology-key")
    status.set_defaults(handler=run_status)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    value = args.handler(args)
    json.dump(value, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

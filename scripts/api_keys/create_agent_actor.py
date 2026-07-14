#!/usr/bin/env python3
"""Provision a WorkChord AgentActor through the REST Agent API."""

from __future__ import annotations

import argparse
import json
import os
import shlex
import sys
from typing import Any
from urllib import error, request


ROLE_SCOPES = {
    "worker": [
        "assignments:read",
        "events:write",
        "runs:write",
        "skills:read",
        "triage:write",
        "work:execute",
    ],
    "pm": [
        "assignments:read",
        "assignments:write",
        "planning:read",
        "planning:write",
        "recovery:read",
        "recovery:write",
        "reports:write",
        "skills:read",
        "tasks:read",
        "team:read",
        "team:write",
    ],
    "verifier": [
        "assignments:read",
        "skills:read",
        "verification:read",
        "verification:write",
    ],
}
DEFAULT_SCOPES = ROLE_SCOPES["worker"]
ALLOWED_SCOPES = [
    "admin",
    "tasks:read",
    "tasks:write",
    "events:write",
    "runs:write",
    "triage:write",
    "skills:read",
    "planning:read",
    "planning:write",
    "team:read",
    "team:write",
    "assignments:read",
    "assignments:write",
    "work:execute",
    "verification:read",
    "verification:write",
    "reports:write",
    "recovery:read",
    "recovery:write",
]


def normalize_base_url(value: str) -> str:
    """Return a base URL without trailing slash."""
    text = value.strip().rstrip("/")
    if not text:
        raise SystemExit("Base URL cannot be blank")
    return text


def normalize_api_prefix(value: str) -> str:
    """Return an API prefix beginning with one slash and without trailing slash."""
    text = value.strip() or "/api"
    return "/" + text.strip("/")


def actor_url(base_url: str, api_prefix: str) -> str:
    """Build the agent actor creation endpoint URL."""
    return f"{normalize_base_url(base_url)}{normalize_api_prefix(api_prefix)}/agent/actors"


def normalize_scopes(scopes: list[str], admin: bool) -> list[str]:
    """Validate and de-duplicate scopes while preserving caller order."""
    result: list[str] = []
    for scope in scopes:
        normalized = scope.strip()
        if normalized not in ALLOWED_SCOPES:
            allowed = ", ".join(ALLOWED_SCOPES)
            raise SystemExit(f"Unsupported scope {scope!r}. Allowed: {allowed}")
        if normalized not in result:
            result.append(normalized)
    if admin and "admin" not in result:
        result.insert(0, "admin")
    return result


def title_from_name(name: str) -> str:
    """Derive a display name from an actor name."""
    return " ".join(part.capitalize() for part in name.replace("_", "-").split("-") if part)


def create_actor(
    *,
    url: str,
    bootstrap_key: str,
    name: str,
    display_name: str,
    scopes: list[str],
    role: str,
    profile_id: int | None,
    work_policy: str,
    max_parallel_work: int,
    enabled: bool,
    timeout: float,
) -> dict[str, Any]:
    """Call POST /agent/actors and return the response body."""
    payload = {
        "name": name,
        "display_name": display_name,
        "scopes": scopes,
        "role": role,
        "profile_id": profile_id,
        "work_policy": work_policy,
        "max_parallel_work": max_parallel_work,
        "enabled": enabled,
    }
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Agent-API-Key": bootstrap_key,
        },
    )
    try:
        with request.urlopen(req, timeout=timeout) as response:
            response_body = response.read().decode("utf-8")
    except error.HTTPError as exc:
        response_body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Agent actor creation failed: HTTP {exc.code}: {response_body}") from exc
    except error.URLError as exc:
        raise SystemExit(f"Agent actor creation failed: {exc.reason}") from exc

    try:
        data = json.loads(response_body)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Agent actor creation returned invalid JSON: {response_body}") from exc

    if "api_key" not in data:
        raise SystemExit(f"Agent actor creation response did not include api_key: {response_body}")
    return data


def render_env(data: dict[str, Any], *, comments: bool) -> str:
    """Render dotenv-style output for the one-time actor key."""
    lines: list[str] = []
    if comments:
        lines.extend([
            "# Store this one-time agent key securely.",
            "# MCP stdio clients should use MCP_AGENT_API_KEY.",
        ])
    lines.extend([
        f"AGENT_ACTOR_ID={data['id']}",
        f"AGENT_ACTOR_NAME={data['name']}",
        f"AGENT_API_KEY={data['api_key']}",
        f"MCP_AGENT_API_KEY={data['api_key']}",
    ])
    return "\n".join(lines)


def render_shell(data: dict[str, Any], *, comments: bool) -> str:
    """Render shell export output for the one-time actor key."""
    lines: list[str] = []
    if comments:
        lines.append("# Source this file only in trusted shells.")
    lines.extend([
        f"export AGENT_ACTOR_ID={shlex.quote(str(data['id']))}",
        f"export AGENT_ACTOR_NAME={shlex.quote(str(data['name']))}",
        f"export AGENT_API_KEY={shlex.quote(str(data['api_key']))}",
        f"export MCP_AGENT_API_KEY={shlex.quote(str(data['api_key']))}",
    ])
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a WorkChord agent actor and print its one-time API key.",
    )
    parser.add_argument(
        "--base-url",
        default=os.getenv("WORKCHORD_BASE_URL", "http://localhost:8001"),
        help="WorkChord backend base URL. Defaults to WORKCHORD_BASE_URL or http://localhost:8001.",
    )
    parser.add_argument(
        "--api-prefix",
        default=os.getenv("WORKCHORD_API_PREFIX", "/api"),
        help="Backend API prefix. Defaults to WORKCHORD_API_PREFIX or /api.",
    )
    parser.add_argument(
        "--bootstrap-key",
        default=os.getenv("AGENT_BOOTSTRAP_API_KEY", ""),
        help="Bootstrap key. Defaults to AGENT_BOOTSTRAP_API_KEY.",
    )
    parser.add_argument("--name", default="codex-worker", help="Stable unique actor name.")
    parser.add_argument("--display-name", help="Human-readable actor display name.")
    parser.add_argument(
        "--role",
        choices=sorted(ROLE_SCOPES),
        default="worker",
        help="Actor role and default least-privilege scope preset.",
    )
    parser.add_argument("--profile-id", type=int, help="Optional capability profile binding.")
    parser.add_argument(
        "--work-policy",
        choices=["assigned_only"],
        default="assigned_only",
        help="Server work-acquisition policy. Defaults to assigned_only.",
    )
    parser.add_argument(
        "--max-parallel-work",
        type=int,
        choices=[1],
        default=1,
        metavar="1",
        help="Maximum current assignments. Assigned-work v1 currently supports one.",
    )
    parser.add_argument(
        "--scope",
        action="append",
        help="Actor scope. Repeat to override the selected role's scope preset.",
    )
    parser.add_argument("--admin", action="store_true", help="Also grant admin scope.")
    parser.add_argument("--disabled", action="store_true", help="Create the actor disabled.")
    parser.add_argument("--timeout", type=float, default=10.0, help="Request timeout in seconds.")
    parser.add_argument(
        "--format",
        choices=["env", "json", "shell"],
        default="env",
        help="Output format. Defaults to dotenv env lines.",
    )
    parser.add_argument("--no-comments", action="store_true", help="Suppress explanatory comments.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.bootstrap_key:
        raise SystemExit("Missing bootstrap key. Set AGENT_BOOTSTRAP_API_KEY or pass --bootstrap-key.")

    name = args.name.strip()
    if not name:
        raise SystemExit("Actor name cannot be blank")

    scopes = normalize_scopes(args.scope or ROLE_SCOPES[args.role], args.admin)
    data = create_actor(
        url=actor_url(args.base_url, args.api_prefix),
        bootstrap_key=args.bootstrap_key,
        name=name,
        display_name=args.display_name or title_from_name(name) or name,
        scopes=scopes,
        role=args.role,
        profile_id=args.profile_id,
        work_policy=args.work_policy,
        max_parallel_work=args.max_parallel_work,
        enabled=not args.disabled,
        timeout=args.timeout,
    )

    if args.format == "json":
        print(json.dumps(data, indent=2, sort_keys=True))
    elif args.format == "shell":
        print(render_shell(data, comments=not args.no_comments))
    else:
        print(render_env(data, comments=not args.no_comments))

    print(
        "The api_key is returned once; store it securely before closing this terminal.",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()

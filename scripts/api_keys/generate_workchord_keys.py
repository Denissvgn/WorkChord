#!/usr/bin/env python3
"""Generate local secrets consumed by WorkChord.

This script creates only secrets that WorkChord owns locally. External
provider credentials such as LLM API keys, GitHub PATs, SMTP passwords, and
third-party webhook URLs must still be created in their source systems.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import secrets
import shlex
from collections.abc import Callable
from datetime import UTC, datetime


def generate_fernet_key() -> str:
    """Return a Fernet-compatible base64url-encoded 32-byte key."""
    return base64.urlsafe_b64encode(os.urandom(32)).decode("ascii")


def generate_prefixed_token(prefix: str) -> str:
    """Return a high-entropy URL-safe token with a human-readable prefix."""
    return f"{prefix}_{secrets.token_urlsafe(32)}"


KEY_GENERATORS: dict[str, Callable[[], str]] = {
    "SETTINGS_ENCRYPTION_KEY": generate_fernet_key,
    "WORKCHORD_ADMIN_API_KEY": lambda: generate_prefixed_token("wcadmin"),
    "AGENT_BOOTSTRAP_API_KEY": lambda: generate_prefixed_token("wcboot"),
    "WEB_INTAKE_TOKEN": lambda: generate_prefixed_token("wcweb"),
    "GITHUB_WEBHOOK_SECRET": lambda: generate_prefixed_token("wcghwh"),
    "OUTBOUND_WEBHOOK_SIGNING_SECRET": lambda: generate_prefixed_token("wcoutwh"),
}

ENV_CONSUMED_KEYS = {
    "SETTINGS_ENCRYPTION_KEY",
    "WORKCHORD_ADMIN_API_KEY",
    "AGENT_BOOTSTRAP_API_KEY",
    "WEB_INTAKE_TOKEN",
    "GITHUB_WEBHOOK_SECRET",
}

KEY_DESCRIPTIONS = {
    "SETTINGS_ENCRYPTION_KEY": "Fernet key for encrypting runtime secrets saved in Settings UI.",
    "WORKCHORD_ADMIN_API_KEY": "Startup-only admin key for protected Settings and control-plane APIs.",
    "AGENT_BOOTSTRAP_API_KEY": "Startup-only key used to provision real agent actors through /api/agent/actors.",
    "WEB_INTAKE_TOKEN": "Bearer token for controlled POST /api/intake/web requests.",
    "GITHUB_WEBHOOK_SECRET": "Shared secret for validating inbound GitHub webhooks.",
    "OUTBOUND_WEBHOOK_SIGNING_SECRET": "Per-target signing secret for outbound webhook target payloads.",
}


def selected_keys(raw_keys: list[str] | None, include_outbound: bool) -> list[str]:
    """Resolve requested keys in stable output order."""
    if raw_keys:
        keys = []
        for raw_key in raw_keys:
            key = raw_key.upper()
            if key not in KEY_GENERATORS:
                allowed = ", ".join(KEY_GENERATORS)
                raise SystemExit(f"Unsupported key {raw_key!r}. Allowed: {allowed}")
            if key not in keys:
                keys.append(key)
        return keys

    keys = [
        "SETTINGS_ENCRYPTION_KEY",
        "WORKCHORD_ADMIN_API_KEY",
        "AGENT_BOOTSTRAP_API_KEY",
        "WEB_INTAKE_TOKEN",
        "GITHUB_WEBHOOK_SECRET",
    ]
    if include_outbound:
        keys.append("OUTBOUND_WEBHOOK_SIGNING_SECRET")
    return keys


def build_payload(keys: list[str]) -> dict[str, object]:
    """Generate a structured payload for all requested keys."""
    generated_at = datetime.now(UTC).isoformat(timespec="seconds")
    values = {key: KEY_GENERATORS[key]() for key in keys}
    return {
        "generated_at": generated_at,
        "keys": values,
        "notes": {
            key: KEY_DESCRIPTIONS[key]
            for key in keys
        },
        "not_generated": {
            "LLM_API_KEY": "Create this with your LLM provider.",
            "GITHUB_TOKEN": "Create this in GitHub or your GitHub Enterprise instance.",
            "SMTP_PASSWORD": "Create this with your mail provider.",
        },
    }


def render_env(payload: dict[str, object], *, comments: bool) -> str:
    """Render dotenv-style KEY=value lines."""
    values = payload["keys"]
    assert isinstance(values, dict)
    lines: list[str] = []
    if comments:
        lines.extend([
            "# Generated WorkChord local secrets.",
            "# Store securely. Do not commit filled values.",
        ])
    for key, value in values.items():
        if comments:
            lines.append(f"# {KEY_DESCRIPTIONS[key]}")
            if key not in ENV_CONSUMED_KEYS:
                lines.append("# Not an environment setting; paste into the relevant API/UI payload.")
        lines.append(f"{key}={value}")
    if comments:
        lines.extend([
            "",
            "# External provider credentials are not generated locally:",
            "# LLM_API_KEY, GITHUB_TOKEN, SMTP_PASSWORD",
        ])
    return "\n".join(lines)


def render_shell(payload: dict[str, object], *, comments: bool) -> str:
    """Render shell export lines."""
    values = payload["keys"]
    assert isinstance(values, dict)
    lines: list[str] = []
    if comments:
        lines.append("# Source this file only in trusted shells.")
    for key, value in values.items():
        lines.append(f"export {key}={shlex.quote(str(value))}")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate local WorkChord API keys and shared secrets.",
    )
    parser.add_argument(
        "--format",
        choices=["env", "json", "shell"],
        default="env",
        help="Output format. Defaults to dotenv env lines.",
    )
    parser.add_argument(
        "--only",
        action="append",
        metavar="KEY",
        help="Generate only this key. Repeat for multiple keys.",
    )
    parser.add_argument(
        "--include-outbound-webhook",
        action="store_true",
        help="Also generate an outbound webhook target signing secret.",
    )
    parser.add_argument(
        "--no-comments",
        action="store_true",
        help="Suppress explanatory comments in env and shell output.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    keys = selected_keys(args.only, args.include_outbound_webhook)
    payload = build_payload(keys)
    comments = not args.no_comments

    if args.format == "json":
        print(json.dumps(payload, indent=2, sort_keys=True))
    elif args.format == "shell":
        print(render_shell(payload, comments=comments))
    else:
        print(render_env(payload, comments=comments))


if __name__ == "__main__":
    main()

"""Read one agent API key from an owner-only file.

A desktop or sandboxed agent often does not inherit the shell environment the
operator exported a key in. A key file at a known path lets the operator hand
the agent its credential without pasting it into chat or a command line.
"""
from __future__ import annotations

import os
import stat
from pathlib import Path


class AgentKeyFileError(ValueError):
    """Raised when a key file is missing, unsafe, or malformed.

    Messages name the path and the problem only; they never include file content.
    """


def read_agent_key_file(path: str | os.PathLike[str]) -> str:
    """Return the single key stored in ``path``.

    The file must be a regular file holding one non-empty line. On POSIX it must
    not be readable or writable by group or others, matching how SSH treats
    private keys.
    """
    location = Path(path).expanduser()
    try:
        info = location.stat()
    except FileNotFoundError as exc:
        raise AgentKeyFileError(f"Agent key file {location} does not exist") from exc
    except OSError as exc:
        raise AgentKeyFileError(f"Agent key file {location} cannot be read") from exc
    if not stat.S_ISREG(info.st_mode):
        raise AgentKeyFileError(f"Agent key file {location} is not a regular file")
    if os.name == "posix" and info.st_mode & 0o077:
        raise AgentKeyFileError(
            f"Agent key file {location} is accessible by other users; "
            f"run: chmod 600 {location}"
        )
    try:
        text = location.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise AgentKeyFileError(f"Agent key file {location} cannot be read") from exc
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if len(lines) != 1:
        raise AgentKeyFileError(
            f"Agent key file {location} must contain exactly one key on one line"
        )
    return lines[0]

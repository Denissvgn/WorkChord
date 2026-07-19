"""Execution-mode guards shared by legacy and autonomous migration tools."""

from __future__ import annotations

import os


EXECUTION_MODE_ENV = "WORKCHORD_EXECUTION_MODE"
ZERO_HUMAN_EXECUTION_MODE = "zero-human-agent-v1"


def zero_human_execution_enabled() -> bool:
    """Return whether fail-closed autonomous execution rules are active."""

    return os.getenv(EXECUTION_MODE_ENV, "").strip() == ZERO_HUMAN_EXECUTION_MODE


def local_signing_rejection_message() -> str:
    """Return one stable diagnostic used by file-key signing/trust boundaries."""

    return (
        "File private keys and file/embedded trust keys are forbidden in "
        f"{ZERO_HUMAN_EXECUTION_MODE}; use the remote-KMS detached-signature "
        "interface and an externally resolved pinned trust anchor"
    )

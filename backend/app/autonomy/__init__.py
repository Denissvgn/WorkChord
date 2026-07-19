"""Fail-closed primitives for WorkChord autonomous execution.

The package deliberately contains no production credential loader and no local
private-key signer.  Production callers must inject charter-selected remote
services through the protocol boundaries exposed by the submodules.
"""

from app.autonomy.canonical import canonical_json_bytes, sha256_hex

__all__ = ["canonical_json_bytes", "sha256_hex"]

"""One-way credential delivery, independent of setup planning and transactions."""
import hashlib
import json
import os
import stat
from pathlib import Path
from typing import Protocol

class CredentialDeliveryError(RuntimeError):
    """Raised when a one-time actor key did not reach the approved sink."""


class AgentTeamCredentialSink(Protocol):
    """One-way sink boundary; implementations never return credential material."""

    reference: str

    @property
    def available(self) -> bool:
        ...

    async def deliver(
        self,
        *,
        credential_ref: str,
        actor_key: str,
        actor_name: str,
        api_key: str,
    ) -> str:
        """Deliver once and return a non-secret receipt digest."""


class FilesystemAgentTeamCredentialSink:
    """Write one-time credentials to an operator-owned mode-0700 directory."""

    def __init__(self, *, directory: str, reference: str):
        self.directory = Path(directory).expanduser() if directory else None
        self.reference = reference.strip()

    @property
    def available(self) -> bool:
        if self.directory is None or not self.reference:
            return False
        try:
            metadata = self.directory.stat()
        except OSError:
            return False
        return (
            stat.S_ISDIR(metadata.st_mode)
            and stat.S_IMODE(metadata.st_mode) & 0o077 == 0
        )

    async def deliver(
        self,
        *,
        credential_ref: str,
        actor_key: str,
        actor_name: str,
        api_key: str,
    ) -> str:
        if not self.available or self.directory is None:
            raise CredentialDeliveryError(
                "The configured agent-team credential sink is unavailable"
            )
        if not (
            credential_ref == self.reference
            or credential_ref.startswith(f"{self.reference}/")
        ):
            raise CredentialDeliveryError(
                "Manifest credential reference does not use the approved sink"
            )
        filename = (
            hashlib.sha256(credential_ref.encode("utf-8")).hexdigest()[:24]
            + "-"
            + actor_key
            + ".json"
        )
        path = self.directory / filename
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        payload = json.dumps(
            {
                "actor_key": actor_key,
                "actor_name": actor_name,
                "api_key": api_key,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        descriptor: int | None = None
        try:
            descriptor = os.open(path, flags, 0o600)
            if os.fstat(descriptor).st_mode & 0o077:
                raise CredentialDeliveryError(
                    "Credential sink did not create a private file"
                )
            written = 0
            while written < len(payload):
                written += os.write(descriptor, payload[written:])
            os.fsync(descriptor)
        except FileExistsError as exc:
            raise CredentialDeliveryError(
                "Credential reference already has a delivered value"
            ) from exc
        except OSError as exc:
            raise CredentialDeliveryError(
                "Credential sink delivery failed"
            ) from exc
        finally:
            if descriptor is not None:
                os.close(descriptor)
        receipt = {
            "schema_version": "agent-team-credential-delivery-receipt-v1",
            "credential_ref": credential_ref,
            "actor_key": actor_key,
            "sink_reference": self.reference,
            "delivered": True,
        }
        return hashlib.sha256(
            json.dumps(receipt, sort_keys=True, separators=(",", ":")).encode(
                "utf-8"
            )
        ).hexdigest()

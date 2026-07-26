"""Run the bounded self-hosted server acceptance profile."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path

from app.autonomy.server_acceptance import (
    ServerAcceptanceConfig,
    ServerAcceptanceError,
    ServerAcceptanceReceipt,
    build_blocked_result,
    run_server_acceptance,
    verify_receipt_current_build,
    verify_receipt_trusted_signer,
)
from app.build_identity import load_backend_build_identity


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Verify one exact self-hosted WorkChord checkout against its "
            "container-backed PostgreSQL, signer, locked evidence, and CAS services. "
            "A pass is never production autonomy evidence."
        )
    )
    parser.add_argument(
        "--deployment-environment",
        default=os.getenv("DEPLOYMENT_ENVIRONMENT", "development"),
    )
    parser.add_argument(
        "--backend-url",
        default=os.getenv("AUTONOMY_BACKEND_URL", "http://backend:8001"),
    )
    parser.add_argument(
        "--gateway-url",
        default=os.getenv("AUTONOMY_GATEWAY_URL", "http://frontend"),
    )
    parser.add_argument(
        "--signer-url",
        default=os.getenv("AUTONOMY_SIGNER_URL", "http://openbao:8200"),
    )
    parser.add_argument(
        "--signer-token-file",
        type=Path,
        default=Path(
            os.getenv(
                "AUTONOMY_SIGNER_TOKEN_FILE",
                "/run/workchord-autonomy/openbao-token",
            )
        ),
    )
    parser.add_argument(
        "--signer-key",
        default=os.getenv(
            "AUTONOMY_SIGNER_KEY",
            "workchord-server-acceptance",
        ),
    )
    parser.add_argument(
        "--trusted-signer-public-key-file",
        type=Path,
        default=Path(
            os.getenv(
                "AUTONOMY_TRUSTED_SIGNER_PUBLIC_KEY_FILE",
                "/run/workchord-autonomy/openbao-signer-public-key.b64",
            )
        ),
        help=(
            "Out-of-band Ed25519 public-key pin written by the signer bootstrap."
        ),
    )
    parser.add_argument(
        "--object-store-url",
        default=os.getenv("AUTONOMY_MINIO_ENDPOINT", "http://minio:9000"),
    )
    parser.add_argument(
        "--object-store-access-key",
        default=os.getenv("AUTONOMY_MINIO_ACCESS_KEY"),
    )
    parser.add_argument(
        "--object-store-secret-key",
        default=os.getenv("AUTONOMY_MINIO_SECRET_KEY"),
    )
    parser.add_argument(
        "--object-store-bucket",
        default=os.getenv(
            "AUTONOMY_MINIO_EVIDENCE_BUCKET",
            "workchord-server-acceptance",
        ),
    )
    parser.add_argument(
        "--object-store-region",
        default=os.getenv("AUTONOMY_MINIO_REGION", "us-east-1"),
    )
    parser.add_argument(
        "--valkey-host",
        default=os.getenv("AUTONOMY_VALKEY_HOST", "valkey"),
    )
    parser.add_argument(
        "--valkey-port",
        type=int,
        default=int(os.getenv("AUTONOMY_VALKEY_PORT", "6379")),
    )
    parser.add_argument(
        "--timeout-seconds",
        type=float,
        default=float(os.getenv("AUTONOMY_ACCEPTANCE_TIMEOUT_SECONDS", "10")),
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional path for the secret-free acceptance receipt.",
    )
    parser.add_argument(
        "--verify-receipt",
        type=Path,
        help="Validate an existing receipt and both Ed25519 signatures offline.",
    )
    return parser.parse_args(argv)


def _required(value: str | None, code: str) -> str:
    if value is None or not value.strip():
        raise ServerAcceptanceError(code)
    return value.strip()


def _render(result: object) -> str:
    return (
        json.dumps(
            result.model_dump(mode="json"),  # type: ignore[attr-defined]
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )


def _emit(rendered: str, output: Path | None) -> None:
    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        temporary_path: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=output.parent,
                prefix=f".{output.name}.",
                suffix=".tmp",
                delete=False,
            ) as stream:
                temporary_path = Path(stream.name)
                stream.write(rendered)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary_path, output)
            output.chmod(0o644)
        finally:
            if temporary_path is not None:
                temporary_path.unlink(missing_ok=True)
    print(rendered, end="")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.verify_receipt is not None:
        try:
            trusted_public_key = (
                args.trusted_signer_public_key_file.read_text(encoding="utf-8")
            )
            receipt = ServerAcceptanceReceipt.model_validate(
                json.loads(args.verify_receipt.read_text(encoding="utf-8"))
            )
            verify_receipt_trusted_signer(receipt, trusted_public_key)
            verify_receipt_current_build(
                receipt,
                load_backend_build_identity(),
            )
        except (OSError, ValueError) as exc:
            print(
                json.dumps(
                    {
                        "decision": "SELF-HOSTED-SERVER-RECEIPT-INVALID",
                        "cause_kind": type(exc).__name__,
                    },
                    indent=2,
                    sort_keys=True,
                )
            )
            return 2
        print(
            json.dumps(
                {
                    "decision": "SELF-HOSTED-SERVER-RECEIPT-VERIFIED",
                    "receipt_digest": receipt.receipt_digest,
                    "signer_public_key_sha256": (
                        receipt.candidate.signer.public_key_sha256
                    ),
                    "source_revision": receipt.candidate.source_revision,
                    "valid_until": receipt.valid_until.isoformat(),
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    try:
        source_revision = load_backend_build_identity().source_revision
    except (OSError, ValueError):
        source_revision = "unknown"
    try:
        token = args.signer_token_file.read_text(encoding="utf-8").strip()
        trusted_public_key = (
            args.trusted_signer_public_key_file.read_text(encoding="utf-8").strip()
        )
        config = ServerAcceptanceConfig(
            deployment_environment=args.deployment_environment,
            backend_url=_required(args.backend_url, "backend-url-missing"),
            gateway_url=_required(args.gateway_url, "gateway-url-missing"),
            signer_url=_required(args.signer_url, "signer-url-missing"),
            signer_token=_required(token, "signer-token-missing"),
            signer_key=_required(args.signer_key, "signer-key-missing"),
            trusted_signer_public_key_base64=_required(
                trusted_public_key,
                "trusted-signer-public-key-missing",
            ),
            object_store_url=_required(
                args.object_store_url,
                "object-store-url-missing",
            ),
            object_store_access_key=_required(
                args.object_store_access_key,
                "object-store-access-key-missing",
            ),
            object_store_secret_key=_required(
                args.object_store_secret_key,
                "object-store-secret-key-missing",
            ),
            object_store_bucket=_required(
                args.object_store_bucket,
                "object-store-bucket-missing",
            ),
            object_store_region=_required(
                args.object_store_region,
                "object-store-region-missing",
            ),
            valkey_host=_required(args.valkey_host, "valkey-host-missing"),
            valkey_port=args.valkey_port,
            timeout_seconds=args.timeout_seconds,
        )
        result = run_server_acceptance(config)
    except OSError as exc:
        error = ServerAcceptanceError("signer-token-unreadable", cause=exc)
        result = build_blocked_result(
            source_revision=source_revision,
            error=error,
        )
        _emit(_render(result), args.output)
        return 2
    except ServerAcceptanceError as error:
        result = build_blocked_result(
            source_revision=source_revision,
            error=error,
        )
        _emit(_render(result), args.output)
        return 2
    except Exception as exc:  # pragma: no cover - final fail-closed boundary
        error = ServerAcceptanceError("acceptance-internal-error", cause=exc)
        result = build_blocked_result(
            source_revision=source_revision,
            error=error,
        )
        _emit(_render(result), args.output)
        return 2

    _emit(_render(result), args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Dedicated durable outbound-delivery worker process."""

from __future__ import annotations

import argparse
import asyncio
import signal
import sys
from typing import Optional

from app.config import get_settings
from app.database import close_database, init_db
from app.services.outbound_webhook_service import (
    outbound_delivery_worker_loop,
    run_due_outbound_delivery_jobs,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the WorkChord durable delivery worker.",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Process one bounded batch and exit.",
    )
    return parser


async def _run(*, once: bool) -> int:
    settings = get_settings()
    if settings.database_process_role != "delivery_worker":
        print(
            "DATABASE_PROCESS_ROLE=delivery_worker is required",
            file=sys.stderr,
        )
        return 2
    if not settings.outbound_delivery_worker_enabled:
        print("Outbound delivery worker is disabled", file=sys.stderr)
        return 2
    if settings.maintenance_mode != "off":
        print(
            f"Delivery worker is drained in {settings.maintenance_mode} mode",
            file=sys.stderr,
        )
        return 0

    await init_db()
    try:
        if once:
            completed = await run_due_outbound_delivery_jobs(
                limit=settings.outbound_delivery_batch_size,
            )
            print(f"Processed delivery jobs: {completed}")
            return 0

        stop_event = asyncio.Event()
        loop = asyncio.get_running_loop()
        for signal_name in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.add_signal_handler(signal_name, stop_event.set)
            except NotImplementedError:  # pragma: no cover - Windows fallback
                pass
        await outbound_delivery_worker_loop(
            stop_event,
            poll_seconds=settings.outbound_delivery_poll_seconds,
            batch_size=settings.outbound_delivery_batch_size,
        )
        return 0
    finally:
        await close_database()


def main(argv: Optional[list[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    return asyncio.run(_run(once=args.once))


if __name__ == "__main__":
    raise SystemExit(main())

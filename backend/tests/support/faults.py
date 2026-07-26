"""Clock, concurrency, and deterministic fault-injection helpers."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta


@dataclass
class FrozenClock:
    """A manually advanced UTC clock for lease and expiry tests."""

    current: datetime = datetime(2026, 1, 1, tzinfo=UTC)

    def now(self) -> datetime:
        return self.current

    def advance(self, delta: timedelta) -> datetime:
        if delta.total_seconds() < 0:
            raise ValueError("FrozenClock cannot move backwards")
        self.current += delta
        return self.current


class FailureInjector:
    """Raise an explicit queued failure at a named deterministic checkpoint."""

    def __init__(self) -> None:
        self._failures: dict[str, list[BaseException]] = {}

    def fail_next(self, checkpoint: str, failure: BaseException) -> None:
        self._failures.setdefault(checkpoint, []).append(failure)

    def checkpoint(self, checkpoint: str) -> None:
        queue = self._failures.get(checkpoint)
        if not queue:
            return
        failure = queue.pop(0)
        if not queue:
            self._failures.pop(checkpoint, None)
        raise failure


class AsyncBarrier:
    """Reusable asyncio barrier for controlled concurrency interleavings."""

    def __init__(self, participants: int) -> None:
        if participants < 1:
            raise ValueError("AsyncBarrier needs at least one participant")
        self._participants = participants
        self._arrived = 0
        self._generation = 0
        self._condition = asyncio.Condition()

    async def wait(self) -> None:
        async with self._condition:
            generation = self._generation
            self._arrived += 1
            if self._arrived == self._participants:
                self._arrived = 0
                self._generation += 1
                self._condition.notify_all()
                return
            await self._condition.wait_for(lambda: self._generation != generation)


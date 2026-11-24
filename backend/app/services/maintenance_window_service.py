"""Admit, begin, and close one coordinated control-plane maintenance window.

An announced window closes admission: no new work begins, claims, or starts a
run until the window is closed. Work already holding a live claim keeps
renewing and may finish. The operator can begin the window only when every
live claim's owner has acknowledged it for the claim's current generation, every
such lease outlives the bounded outage plus its margin, no running run lacks a
live claim, and every PM has a notice receipt. A long lease or a pause in a
worker's traffic is never an acknowledgement.
"""

from __future__ import annotations

import secrets
from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.authority import internal_authority
from app.commands import commit_or_flush
from app.models.agent import AgentActor, AgentRun
from app.models.maintenance import MaintenanceWindow, MaintenanceWindowReceipt
from app.models.task import Task
from app.schemas.maintenance import (
    MaintenanceOwnerAcknowledgement,
    MaintenanceWindowClose,
    MaintenanceWindowCreate,
    MaintenanceWindowNotice,
)
from app.services.agent_routing_service import AgentRoutingConflictError
from app.utils import time as clock

OPEN_STATES = ("announced", "in_progress")
MAX_WINDOW = timedelta(hours=24)
LIVE_RUN_STATE = "running"


class MaintenanceWindowConflict(AgentRoutingConflictError):
    """A stable, structured maintenance refusal shared by REST and MCP."""


def _iso(value: datetime | None) -> str | None:
    return value.isoformat() if value is not None else None


def _principal_id(db: AsyncSession) -> int | None:
    authority = db.info.get("authority")
    return getattr(authority, "principal_id", None)


async def open_window(db: AsyncSession, *, lock: bool = False) -> MaintenanceWindow | None:
    statement = select(MaintenanceWindow).where(MaintenanceWindow.active_slot == 1)
    if lock:
        statement = statement.with_for_update()
    return await db.scalar(statement)


async def require_start_admission(db: AsyncSession) -> None:
    """Refuse a new start while a window is announced or in progress."""

    window = await open_window(db)
    if window is None:
        return
    raise MaintenanceWindowConflict(
        "maintenance_window_admission_closed",
        "New work cannot start during a coordinated maintenance window. "
        "Work that already holds a live claim may renew and finish; retry the start after the window closes.",
        maintenance_window_id=window.id,
        maintenance_window_state=window.state,
        planned_end_at=_iso(window.planned_end_at),
    )


def window_view(window: MaintenanceWindow) -> dict[str, Any]:
    return {
        "id": window.id,
        "state": window.state,
        "release_label": window.release_label,
        "reason": window.reason,
        "planned_start_at": _iso(window.planned_start_at),
        "planned_end_at": _iso(window.planned_end_at),
        "max_outage_seconds": window.max_outage_seconds,
        "expiry_margin_seconds": window.expiry_margin_seconds,
        "minimum_lease_seconds": window.max_outage_seconds + window.expiry_margin_seconds,
        "announced_by_principal_id": window.announced_by_principal_id,
        "announced_at": _iso(window.announced_at),
        "started_at": _iso(window.started_at),
        "ended_at": _iso(window.ended_at),
        "outcome": window.outcome,
        "closing_note": window.closing_note,
        "protected_claims": window.protected_claims,
        "resumption": window.resumption,
    }


def receipt_view(receipt: MaintenanceWindowReceipt) -> dict[str, Any]:
    return {
        "id": receipt.id,
        "window_id": receipt.window_id,
        "kind": receipt.kind,
        "source": receipt.source,
        "actor_id": receipt.actor_id,
        "task_id": receipt.task_id,
        "run_id": receipt.run_id,
        "assignment_id": receipt.assignment_id,
        "claim_generation": receipt.claim_generation,
        "claim_expires_at": _iso(receipt.claim_expires_at),
        "channel": receipt.channel,
        "reference": receipt.reference,
        "recorded_at": _iso(receipt.recorded_at),
    }


def _owner_key(actor_id: int, task_id: int, generation: int) -> str:
    return f"owner:{actor_id}:{task_id}:{generation}"


def _pm_key(actor_id: int) -> str:
    return f"pm:{actor_id}"


class MaintenanceWindowService:
    """Operator and agent commands for one coordinated maintenance window."""

    def __init__(self, db: AsyncSession):
        self.db = db

    # -- reads -----------------------------------------------------------

    async def _window(self, window_id: int, *, lock: bool = False) -> MaintenanceWindow:
        statement = select(MaintenanceWindow).where(MaintenanceWindow.id == window_id)
        if lock:
            statement = statement.with_for_update()
        window = await self.db.scalar(statement)
        if window is None:
            raise LookupError("Maintenance window not found")
        return window

    async def _live_claims(self, now: datetime, *, actor_id: int | None = None) -> list[dict[str, Any]]:
        statement = (
            select(Task.id, Task.project_id, Task.claimed_by, Task.claim_generation, Task.claim_expires_at)
            .where(Task.claimed_by.is_not(None), Task.claim_id.is_not(None), Task.claim_expires_at > now)
            .order_by(Task.id)
        )
        if actor_id is not None:
            statement = statement.where(Task.claimed_by == actor_id)
        rows = (await self.db.execute(statement)).all()
        runs = await self._running_runs([row.id for row in rows])
        claims = []
        for row in rows:
            run = next(
                (
                    item for item in runs
                    if item.task_id == row.id
                    and item.actor_id == row.claimed_by
                    and item.claim_generation == row.claim_generation
                ),
                None,
            )
            claims.append({
                "task_id": row.id,
                "project_id": row.project_id,
                "actor_id": row.claimed_by,
                "claim_generation": row.claim_generation,
                "claim_expires_at": _iso(row.claim_expires_at),
                "run_id": run.id if run else None,
                "assignment_id": run.assignment_id if run else None,
            })
        return claims

    async def _running_runs(self, task_ids: list[int] | None = None) -> list[Any]:
        statement = select(
            AgentRun.id, AgentRun.task_id, AgentRun.actor_id, AgentRun.assignment_id, AgentRun.claim_generation,
        ).where(AgentRun.status == LIVE_RUN_STATE).order_by(AgentRun.id)
        if task_ids is not None:
            if not task_ids:
                return []
            statement = statement.where(AgentRun.task_id.in_(task_ids))
        return list((await self.db.execute(statement)).all())

    async def _pm_recipients(self) -> list[AgentActor]:
        return list((await self.db.scalars(
            select(AgentActor)
            .where(AgentActor.role == "pm", AgentActor.enabled.is_(True), AgentActor.lifecycle_state == "active")
            .order_by(AgentActor.id)
        )).all())

    async def _receipts(self, window_id: int) -> dict[str, MaintenanceWindowReceipt]:
        receipts = (await self.db.scalars(
            select(MaintenanceWindowReceipt).where(MaintenanceWindowReceipt.window_id == window_id)
        )).all()
        return {receipt.receipt_key: receipt for receipt in receipts}

    async def evaluate(self, window: MaintenanceWindow, now: datetime | None = None) -> dict[str, Any]:
        """Return what still stands between this window and a safe begin."""

        now = now or clock.utc_now()
        required_until = now + timedelta(seconds=window.max_outage_seconds + window.expiry_margin_seconds)
        receipts = await self._receipts(window.id)
        claims = await self._live_claims(now)
        blockers: list[dict[str, Any]] = []
        if window.state == "announced":
            if now < window.planned_start_at:
                blockers.append({"code": "window_not_started", "planned_start_at": _iso(window.planned_start_at)})
            if now + timedelta(seconds=window.max_outage_seconds) > window.planned_end_at:
                blockers.append({"code": "window_no_longer_fits", "planned_end_at": _iso(window.planned_end_at)})
        for claim in claims:
            receipt = receipts.get(_owner_key(claim["actor_id"], claim["task_id"], claim["claim_generation"]))
            claim["acknowledged"] = receipt is not None
            claim["acknowledgement_id"] = receipt.id if receipt else None
            if receipt is None:
                blockers.append({"code": "owner_acknowledgement_missing", **{
                    key: claim[key] for key in ("task_id", "actor_id", "claim_generation", "run_id")
                }})
            elif window.state == "announced" and datetime.fromisoformat(claim["claim_expires_at"]) < required_until:
                blockers.append({
                    "code": "lease_margin_insufficient", "task_id": claim["task_id"], "actor_id": claim["actor_id"],
                    "claim_expires_at": claim["claim_expires_at"], "required_lease_until": _iso(required_until),
                })
        claimed_runs = {claim["run_id"] for claim in claims if claim["run_id"] is not None}
        unclaimed_runs = [run for run in await self._running_runs() if run.id not in claimed_runs]
        for run in unclaimed_runs:
            blockers.append({
                "code": "running_run_without_live_claim", "run_id": run.id, "task_id": run.task_id,
                "actor_id": run.actor_id, "claim_generation": run.claim_generation,
            })
        recipients = []
        for actor in await self._pm_recipients():
            receipt = receipts.get(_pm_key(actor.id))
            recipients.append({
                "actor_id": actor.id, "name": actor.name, "notified": receipt is not None,
                "source": receipt.source if receipt else None,
            })
            if receipt is None:
                blockers.append({"code": "pm_notice_missing", "actor_id": actor.id})
        protected = {
            (entry["task_id"], entry["actor_id"], entry["claim_generation"])
            for entry in window.protected_claims or []
        }
        unprotected = [
            claim for claim in claims
            if window.state == "in_progress"
            and (claim["task_id"], claim["actor_id"], claim["claim_generation"]) not in protected
        ]
        return {
            "evaluated_at": _iso(now),
            "ready": window.state == "announced" and not blockers,
            "required_lease_until": _iso(required_until),
            "blockers": blockers if window.state == "announced" else [],
            "live_claims": claims,
            "unprotected_live_claims": unprotected,
            "pm_recipients": recipients,
        }

    async def list_windows(self, *, limit: int = 20) -> list[dict[str, Any]]:
        windows = (await self.db.scalars(
            select(MaintenanceWindow).order_by(MaintenanceWindow.id.desc()).limit(limit)
        )).all()
        return [window_view(window) for window in windows]

    async def status(self, window_id: int) -> dict[str, Any]:
        window = await self._window(window_id)
        receipts = await self._receipts(window.id)
        return {
            **window_view(window),
            "receipts": [receipt_view(item) for item in sorted(receipts.values(), key=lambda item: item.id)],
            "readiness": await self.evaluate(window) if window.state in OPEN_STATES else None,
        }

    # -- operator commands -------------------------------------------------

    async def announce(self, data: MaintenanceWindowCreate) -> dict[str, Any]:
        now = clock.utc_now()
        start, end = data.planned_start_at, data.planned_end_at
        if start.tzinfo is None or end.tzinfo is None:
            raise ValueError("Planned window times must include a UTC offset")
        if end <= start:
            raise ValueError("The window must end after it starts")
        if end - start > MAX_WINDOW:
            raise ValueError("A maintenance window can last at most 24 hours")
        if end <= now:
            raise ValueError("The window must end in the future")
        if timedelta(seconds=data.max_outage_seconds) > end - start:
            raise ValueError("The maximum outage must fit inside the window")
        existing = await open_window(self.db, lock=True)
        if existing is not None:
            raise MaintenanceWindowConflict(
                "maintenance_window_already_open", "Close or cancel the open maintenance window first.",
                maintenance_window_id=existing.id, maintenance_window_state=existing.state,
            )
        window = MaintenanceWindow(
            state="announced", active_slot=1, release_label=data.release_label, reason=data.reason,
            planned_start_at=start, planned_end_at=end, max_outage_seconds=data.max_outage_seconds,
            expiry_margin_seconds=data.expiry_margin_seconds, announced_by_principal_id=_principal_id(self.db),
            announced_at=now,
        )
        self.db.add(window)
        try:
            await self.db.flush()
        except IntegrityError as exc:
            raise MaintenanceWindowConflict(
                "maintenance_window_already_open", "Close or cancel the open maintenance window first.",
            ) from exc
        await commit_or_flush(self.db)
        return await self.status(window.id)

    async def record_pm_notice(self, window_id: int, data: MaintenanceWindowNotice) -> dict[str, Any]:
        """Record that a PM was told through another channel. This is never run-owner consent."""

        window = await self._window(window_id, lock=True)
        self._require_state(window, "announced")
        if data.actor_id not in {actor.id for actor in await self._pm_recipients()}:
            raise ValueError("The notice recipient must be an active PM agent")
        receipt = await self._add_receipt(MaintenanceWindowReceipt(
            window_id=window.id, kind="pm_notice", receipt_key=_pm_key(data.actor_id), actor_id=data.actor_id,
            source="operator", channel=data.channel, reference=data.reference,
            recorded_by_principal_id=_principal_id(self.db), recorded_at=clock.utc_now(),
        ))
        return receipt_view(receipt)

    async def begin(self, window_id: int) -> dict[str, Any]:
        window = await self._window(window_id, lock=True)
        self._require_state(window, "announced")
        now = clock.utc_now()
        evaluation = await self.evaluate(window, now)
        if evaluation["blockers"]:
            raise MaintenanceWindowConflict(
                "maintenance_window_not_ready",
                "The window cannot begin until every blocker is resolved. "
                "Only the claim owner's own acknowledgement admits a live claim.",
                maintenance_window_id=window.id,
                blockers=evaluation["blockers"],
            )
        window.state = "in_progress"
        window.started_at = now
        window.protected_claims = [
            {
                key: claim[key]
                for key in (
                    "task_id", "project_id", "actor_id", "claim_generation", "claim_expires_at",
                    "run_id", "assignment_id", "acknowledgement_id",
                )
            }
            for claim in evaluation["live_claims"]
        ]
        await commit_or_flush(self.db)
        return await self.status(window.id)

    async def close(self, window_id: int, data: MaintenanceWindowClose) -> dict[str, Any]:
        window = await self._window(window_id, lock=True)
        self._require_state(window, "in_progress")
        now = clock.utc_now()
        claims = []
        for entry in window.protected_claims or []:
            claims.append({**{key: entry[key] for key in ("task_id", "actor_id", "claim_generation", "run_id")},
                           **await self._resumption(entry, now)})
        evaluation = await self.evaluate(window, now)
        window.resumption = {
            "evaluated_at": _iso(now),
            "claims": claims,
            "unprotected_live_claims": evaluation["unprotected_live_claims"],
        }
        window.state = "completed"
        window.active_slot = None
        window.ended_at = now
        window.outcome = data.outcome
        window.closing_note = data.note
        await commit_or_flush(self.db)
        return await self.status(window.id)

    async def cancel(self, window_id: int, note: str | None) -> dict[str, Any]:
        window = await self._window(window_id, lock=True)
        self._require_state(window, "announced")
        window.state = "canceled"
        window.active_slot = None
        window.ended_at = clock.utc_now()
        window.outcome = "canceled"
        window.closing_note = note
        await commit_or_flush(self.db)
        return await self.status(window.id)

    async def _resumption(self, entry: dict[str, Any], now: datetime) -> dict[str, Any]:
        task = (await self.db.execute(
            select(Task.claimed_by, Task.claim_generation, Task.claim_expires_at).where(Task.id == entry["task_id"])
        )).one_or_none()
        run = None
        if entry.get("run_id") is not None:
            run = (await self.db.execute(
                select(AgentRun.status, AgentRun.claim_generation).where(AgentRun.id == entry["run_id"])
            )).one_or_none()
        if task is None:
            return {"state": "lost", "reason": "task_missing"}
        same_generation = task.claim_generation == entry["claim_generation"]
        if (same_generation and task.claimed_by == entry["actor_id"] and task.claim_expires_at is not None
                and task.claim_expires_at > now and (run is None or run.status == LIVE_RUN_STATE)):
            return {"state": "preserved", "claim_expires_at": _iso(task.claim_expires_at)}
        if same_generation and task.claimed_by is None and run is not None and run.status != LIVE_RUN_STATE:
            return {"state": "finished", "run_status": run.status}
        if not same_generation:
            return {"state": "lost", "reason": "claim_generation_changed"}
        return {"state": "lost", "reason": "lease_expired"}

    # -- agent commands ----------------------------------------------------

    async def current_for_actor(self, actor: AgentActor) -> dict[str, Any]:
        window = await open_window(self.db)
        if window is None:
            return {"window": None, "my_live_claims": [], "pm_notice_required": False, "pm_notice_recorded": False}
        now = clock.utc_now()
        receipts = await self._receipts(window.id)
        claims = await self._live_claims(now, actor_id=actor.id)
        for claim in claims:
            receipt = receipts.get(_owner_key(actor.id, claim["task_id"], claim["claim_generation"]))
            claim["acknowledged"] = receipt is not None
            claim["acknowledgement_id"] = receipt.id if receipt else None
        is_pm = actor.role == "pm" and actor.enabled and actor.lifecycle_state == "active"
        return {
            "window": window_view(window),
            "my_live_claims": claims,
            "pm_notice_required": is_pm,
            "pm_notice_recorded": _pm_key(actor.id) in receipts,
        }

    async def acknowledge(
        self, actor: AgentActor, window_id: int, data: MaintenanceOwnerAcknowledgement,
    ) -> dict[str, Any]:
        """Record the live claim owner's own acknowledgement of the bounded window."""

        window = await self._window(window_id, lock=True)
        self._require_state(window, "announced")
        now = clock.utc_now()
        task = (await self.db.execute(
            select(Task.id, Task.claimed_by, Task.claim_id, Task.claim_generation, Task.claim_expires_at)
            .where(Task.id == data.task_id)
        )).one_or_none()
        if (
            task is None
            or task.claimed_by != actor.id
            or task.claim_id is None
            or not secrets.compare_digest(task.claim_id, data.claim_id)
            or task.claim_generation != data.claim_generation
            or task.claim_expires_at is None
            or task.claim_expires_at <= now
        ):
            raise MaintenanceWindowConflict(
                "maintenance_claim_not_live",
                "Only the owner of a live claim can acknowledge the window for that claim's current fence.",
                task_id=data.task_id,
            )
        runs = [
            run for run in await self._running_runs([task.id])
            if run.actor_id == actor.id and run.claim_generation == task.claim_generation
        ]
        run = runs[0] if runs else None
        if data.run_id is not None and (run is None or run.id != data.run_id):
            raise MaintenanceWindowConflict(
                "maintenance_claim_not_live", "The run is not this claim's live run.", task_id=data.task_id,
                run_id=data.run_id,
            )
        receipt = await self._add_receipt(MaintenanceWindowReceipt(
            window_id=window.id, kind="owner_acknowledgement",
            receipt_key=_owner_key(actor.id, task.id, task.claim_generation), actor_id=actor.id, source="agent",
            task_id=task.id, run_id=run.id if run else None, assignment_id=run.assignment_id if run else None,
            claim_generation=task.claim_generation, claim_expires_at=task.claim_expires_at, recorded_at=now,
        ))
        return {
            "receipt": receipt_view(receipt),
            "window": window_view(window),
            "minimum_lease_seconds": window.max_outage_seconds + window.expiry_margin_seconds,
        }

    async def record_own_notice(self, actor: AgentActor, window_id: int) -> dict[str, Any]:
        window = await self._window(window_id, lock=True)
        self._require_state(window, "announced")
        if not (actor.role == "pm" and actor.enabled and actor.lifecycle_state == "active"):
            raise MaintenanceWindowConflict(
                "maintenance_notice_not_required", "Only an active PM agent records a maintenance notice receipt.",
            )
        receipt = await self._add_receipt(MaintenanceWindowReceipt(
            window_id=window.id, kind="pm_notice", receipt_key=_pm_key(actor.id), actor_id=actor.id,
            source="agent", recorded_at=clock.utc_now(),
        ))
        return {"receipt": receipt_view(receipt), "window": window_view(window)}

    # -- helpers -----------------------------------------------------------

    @staticmethod
    def _require_state(window: MaintenanceWindow, state: str) -> None:
        if window.state != state:
            raise MaintenanceWindowConflict(
                "maintenance_window_state_conflict",
                f"The maintenance window is {window.state}; this step needs it {state}.",
                maintenance_window_id=window.id, maintenance_window_state=window.state,
            )

    async def _add_receipt(self, receipt: MaintenanceWindowReceipt) -> MaintenanceWindowReceipt:
        existing = await self.db.scalar(select(MaintenanceWindowReceipt).where(
            MaintenanceWindowReceipt.window_id == receipt.window_id,
            MaintenanceWindowReceipt.receipt_key == receipt.receipt_key,
        ))
        if existing is not None:
            return existing
        # The caller has verified the recording actor's own claim or role above.
        with internal_authority(self.db):
            self.db.add(receipt)
            await self.db.flush()
        await commit_or_flush(self.db)
        return receipt

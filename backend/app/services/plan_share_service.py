"""Creation, ownership, and revocation of immutable plan shares."""

import secrets

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.plan_share import PlanShare
from app.models.user_session import UserSession
from app.schemas.plan_share import PlanShareResponse
from app.services.snapshot_service import SnapshotService
from app.utils.time import utc_now


class PlanShareService:
    """Persist plan snapshots without exposing mutable planning records."""

    def __init__(self, db: AsyncSession):
        self.db = db

    @staticmethod
    def _query():
        return select(PlanShare).options(
            selectinload(PlanShare.iteration),
            selectinload(PlanShare.created_by_session),
        )

    @staticmethod
    def to_response(share: PlanShare) -> PlanShareResponse:
        return PlanShareResponse(
            id=share.id,
            public_id=share.public_id,
            iteration_id=share.iteration_id,
            iteration_name=share.iteration.name,
            created_by_display=share.created_by_session.display_name,
            snapshot_data=share.snapshot_data,
            created_at=share.created_at,
            revoked_at=share.revoked_at,
        )

    @staticmethod
    def _share_snapshot(snapshot_data: dict) -> dict:
        """Keep token-scoped responses limited to plan-review information."""

        def share_task(task: dict) -> dict:
            return {
                key: task.get(key)
                for key in (
                    "id",
                    "title",
                    "priority",
                    "effort_days",
                    "effort_hours",
                    "status",
                    "assignee_name",
                    "start_date",
                    "end_date",
                    "is_optional",
                    "is_deferred",
                    "tags",
                    "dependencies",
                )
            } | {
                "children": [
                    share_task(child)
                    for child in task.get("children", [])
                    if isinstance(child, dict)
                ],
            }

        iteration = snapshot_data.get("iteration", {})
        return {
            "iteration": {
                key: iteration.get(key)
                for key in ("id", "name", "start_date", "end_date")
            },
            "team_members": [
                {
                    key: member.get(key)
                    for key in ("name", "position", "availability_percent")
                }
                for member in snapshot_data.get("team_members", [])
                if isinstance(member, dict)
            ],
            "tasks": [
                share_task(task)
                for task in snapshot_data.get("tasks", [])
                if isinstance(task, dict)
            ],
            "snapshot_info": snapshot_data.get("snapshot_info", {}),
        }

    async def get_owned_current(
        self,
        iteration_id: int,
        session_id: int,
    ) -> PlanShare | None:
        result = await self.db.execute(
            self._query()
            .where(
                PlanShare.iteration_id == iteration_id,
                PlanShare.created_by_session_id == session_id,
                PlanShare.revoked_at.is_(None),
            )
            .order_by(PlanShare.created_at.desc(), PlanShare.id.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def get_active_by_public_id(self, public_id: str) -> PlanShare | None:
        result = await self.db.execute(
            self._query().where(
                PlanShare.public_id == public_id,
                PlanShare.revoked_at.is_(None),
            )
        )
        return result.scalar_one_or_none()

    async def create(
        self,
        iteration_id: int,
        session: UserSession,
    ) -> PlanShare | None:
        snapshot_data = await SnapshotService(self.db).build_snapshot_data(
            iteration_id,
            "plan_share",
        )
        if snapshot_data is None:
            return None

        created_at = utc_now()
        await self.db.execute(
            update(PlanShare)
            .where(
                PlanShare.iteration_id == iteration_id,
                PlanShare.created_by_session_id == session.id,
                PlanShare.revoked_at.is_(None),
            )
            .values(revoked_at=created_at)
        )

        public_id = secrets.token_urlsafe(24)
        while await self.db.scalar(
            select(PlanShare.id).where(PlanShare.public_id == public_id)
        ) is not None:
            public_id = secrets.token_urlsafe(24)

        share = PlanShare(
            public_id=public_id,
            iteration_id=iteration_id,
            created_by_session_id=session.id,
            snapshot_data=self._share_snapshot(snapshot_data),
            created_at=created_at,
        )
        self.db.add(share)
        try:
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise

        result = await self.db.execute(
            self._query().where(PlanShare.id == share.id)
        )
        return result.scalar_one()

    async def revoke(self, share_id: int, session_id: int) -> bool:
        result = await self.db.execute(
            select(PlanShare).where(
                PlanShare.id == share_id,
                PlanShare.created_by_session_id == session_id,
                PlanShare.revoked_at.is_(None),
            )
        )
        share = result.scalar_one_or_none()
        if share is None:
            return False

        share.revoked_at = utc_now()
        try:
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise
        return True

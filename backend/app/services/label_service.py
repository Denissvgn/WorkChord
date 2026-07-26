"""Service for governed label taxonomy and built-in defaults."""
from typing import Any, Optional, Sequence

from sqlalchemy import Select, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload, with_loader_criteria

from app.models.label import Label, LabelGroup
from app.schemas.label import (
    LabelCreate,
    LabelGroupCreate,
    LabelGroupUpdate,
    LabelUpdate,
)
from app.services.language_service import (
    backend_error_message,
    entity_not_found_message,
    resolve_runtime_ui_language,
)
from app.sql_semantics import portable_contains


DEFAULT_LABEL_GROUP_DEFINITIONS: list[dict[str, Any]] = [
    {
        "seed_key": "group_type",
        "key": "type",
        "name": "Type",
        "description": "Work classification labels.",
        "color": "#2563eb",
        "sort_order": 10,
        "labels": [
            ("feature", "Feature", "#2563eb"),
            ("bug", "Bug", "#dc2626"),
            ("chore", "Chore", "#64748b"),
            ("incident", "Incident", "#f97316"),
            ("research", "Research", "#7c3aed"),
            ("release", "Release", "#16a34a"),
            ("request", "Request", "#0d9488"),
        ],
    },
    {
        "seed_key": "group_area",
        "key": "area",
        "name": "Area",
        "description": "Product or engineering area labels.",
        "color": "#0f766e",
        "sort_order": 20,
        "labels": [
            ("backend", "Backend", "#334155"),
            ("frontend", "Frontend", "#2563eb"),
            ("scheduling", "Scheduling", "#7c3aed"),
            ("analytics", "Analytics", "#0f766e"),
            ("integrations", "Integrations", "#ea580c"),
        ],
    },
    {
        "seed_key": "group_risk",
        "key": "risk",
        "name": "Risk",
        "description": "Delivery risk and review labels.",
        "color": "#dc2626",
        "sort_order": 30,
        "labels": [
            ("blocked", "Blocked", "#dc2626"),
            ("risky", "Risky", "#f59e0b"),
            ("needs-review", "Needs review", "#a855f7"),
        ],
    },
    {
        "seed_key": "group_source",
        "key": "source",
        "name": "Source",
        "description": "Intake origin labels.",
        "color": "#7c3aed",
        "sort_order": 40,
        "labels": [
            ("customer", "Customer", "#0d9488"),
            ("internal", "Internal", "#64748b"),
            ("agent", "Agent", "#2563eb"),
            ("import", "Import", "#475569"),
        ],
    },
    {
        "seed_key": "group_capability",
        "key": "capability",
        "name": "Capability",
        "description": "Agent capability labels.",
        "color": "#0891b2",
        "sort_order": 50,
        "labels": [
            ("cap:docs", "Docs", "#9333ea"),
            ("cap:code", "Code", "#2563eb"),
            ("cap:test", "Test", "#16a34a"),
            ("cap:research", "Research", "#7c3aed"),
        ],
    },
]


class LabelService:
    """Service for label group and label CRUD plus built-in label seeding."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def _handle_integrity_error(self, message: str, exc: IntegrityError):
        """Rollback failed writes and expose a stable conflict message."""
        await self.db.rollback()
        ui_language = await resolve_runtime_ui_language(self.db)
        raise LabelConflictError(backend_error_message(message, ui_language)) from exc

    def _group_query(self) -> Select:
        """Build the base group query."""
        return select(LabelGroup)

    def _label_query(self) -> Select:
        """Build the base label query."""
        return select(Label).options(selectinload(Label.group))

    async def seed_default_labels(self) -> list[LabelGroup | Label]:
        """Insert missing built-in label groups and labels without overwriting edits."""
        created: list[LabelGroup | Label] = []

        result = await self.db.execute(select(LabelGroup))
        groups = result.scalars().all()
        groups_by_seed = {group.seed_key: group for group in groups if group.seed_key}
        groups_by_key = {group.key: group for group in groups}

        for definition in DEFAULT_LABEL_GROUP_DEFINITIONS:
            seed_key = definition["seed_key"]
            key = definition["key"]
            group = groups_by_seed.get(seed_key) or groups_by_key.get(key)
            if group is None:
                group = LabelGroup(
                    seed_key=seed_key,
                    key=key,
                    name=definition["name"],
                    description=definition["description"],
                    color=definition["color"],
                    sort_order=definition["sort_order"],
                )
                self.db.add(group)
                created.append(group)
                groups_by_seed[seed_key] = group
                groups_by_key[key] = group

        if created:
            await self.db.flush()

        result = await self.db.execute(select(Label))
        labels = result.scalars().all()
        labels_by_seed = {label.seed_key: label for label in labels if label.seed_key}
        labels_by_slug = {label.slug: label for label in labels}

        for group_definition in DEFAULT_LABEL_GROUP_DEFINITIONS:
            group = groups_by_seed.get(group_definition["seed_key"]) or groups_by_key[group_definition["key"]]
            for index, (slug, name, color) in enumerate(group_definition["labels"], start=1):
                seed_key = f"label_{slug.replace(':', '_')}"
                if seed_key in labels_by_seed or slug in labels_by_slug:
                    continue
                label = Label(
                    seed_key=seed_key,
                    slug=slug,
                    name=name,
                    group_id=group.id,
                    description=None,
                    color=color,
                    sort_order=index * 10,
                )
                self.db.add(label)
                created.append(label)
                labels_by_seed[seed_key] = label
                labels_by_slug[slug] = label

        if created:
            await self.db.commit()
            for instance in created:
                await self.db.refresh(instance)

        return created

    async def list_groups(self, include_inactive: bool = False) -> Sequence[LabelGroup]:
        """List label groups ordered for filter UI display."""
        query = self._group_query().options(
            selectinload(LabelGroup.labels).selectinload(Label.group)
        )
        if not include_inactive:
            query = query.where(LabelGroup.is_active.is_(True)).options(
                with_loader_criteria(Label, Label.is_active.is_(True), include_aliases=True)
            )

        query = query.order_by(LabelGroup.sort_order, LabelGroup.name, LabelGroup.id)
        result = await self.db.execute(query)
        return result.scalars().unique().all()

    async def list_labels(
        self,
        group_key: Optional[str] = None,
        include_inactive: bool = False,
        q: Optional[str] = None,
    ) -> Sequence[Label]:
        """List governed labels with optional group and text filters."""
        query = self._label_query().join(LabelGroup)
        if group_key:
            query = query.where(LabelGroup.key == group_key)
        if not include_inactive:
            query = query.where(Label.is_active.is_(True), LabelGroup.is_active.is_(True))
        if q:
            query = query.where(
                or_(
                    portable_contains(Label.slug, q),
                    portable_contains(Label.name, q),
                    portable_contains(Label.description, q),
                )
            )

        query = query.order_by(LabelGroup.sort_order, Label.sort_order, Label.name, Label.id)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_group_by_id(self, group_id: int) -> Optional[LabelGroup]:
        """Get a label group by ID."""
        result = await self.db.execute(
            self._group_query()
            .options(selectinload(LabelGroup.labels).selectinload(Label.group))
            .where(LabelGroup.id == group_id)
        )
        return result.scalar_one_or_none()

    async def get_label_by_id(self, label_id: int) -> Optional[Label]:
        """Get a label by ID."""
        result = await self.db.execute(self._label_query().where(Label.id == label_id))
        return result.scalar_one_or_none()

    async def create_group(self, data: LabelGroupCreate) -> LabelGroup:
        """Create a user-managed label group."""
        group = LabelGroup(**data.model_dump())
        self.db.add(group)
        try:
            await self.db.commit()
        except IntegrityError as exc:
            await self._handle_integrity_error("Label group key already exists", exc)
        await self.db.refresh(group)
        return await self.get_group_by_id(group.id) or group

    async def update_group(
        self,
        group_id: int,
        data: LabelGroupUpdate,
    ) -> Optional[LabelGroup]:
        """Apply a partial label group update."""
        group = await self.get_group_by_id(group_id)
        if not group:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(group, field, value)

        try:
            await self.db.commit()
        except IntegrityError as exc:
            await self._handle_integrity_error("Label group key already exists", exc)
        await self.db.refresh(group)
        return await self.get_group_by_id(group.id) or group

    async def create_label(self, data: LabelCreate) -> Label:
        """Create a user-managed label."""
        if not await self.get_group_by_id(data.group_id):
            ui_language = await resolve_runtime_ui_language(self.db)
            raise ValueError(entity_not_found_message("label_group", data.group_id, ui_language))

        label = Label(**data.model_dump())
        self.db.add(label)
        try:
            await self.db.commit()
        except IntegrityError as exc:
            await self._handle_integrity_error("Label slug already exists", exc)
        await self.db.refresh(label)
        return await self.get_label_by_id(label.id) or label

    async def update_label(
        self,
        label_id: int,
        data: LabelUpdate,
    ) -> Optional[Label]:
        """Apply a partial label update."""
        label = await self.get_label_by_id(label_id)
        if not label:
            return None

        update_data = data.model_dump(exclude_unset=True)
        if "group_id" in update_data and not await self.get_group_by_id(update_data["group_id"]):
            ui_language = await resolve_runtime_ui_language(self.db)
            raise ValueError(entity_not_found_message("label_group", update_data["group_id"], ui_language))

        for field, value in update_data.items():
            setattr(label, field, value)

        try:
            await self.db.commit()
        except IntegrityError as exc:
            await self._handle_integrity_error("Label slug already exists", exc)
        await self.db.refresh(label)
        return await self.get_label_by_id(label.id) or label


class LabelConflictError(ValueError):
    """Raised when label taxonomy uniqueness constraints are violated."""

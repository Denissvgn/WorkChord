"""Triage service with inbox, lifecycle, and conversion logic."""
import json
from datetime import datetime
from typing import Any, Optional, Sequence

from sqlalchemy import Select, and_, case, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.iteration import Iteration
from app.models.label import LabelGroup
from app.models.project import Project
from app.models.task import Task
from app.models.team_member import TeamMember, TeamMemberProfile
from app.models.template import TemplateType, WorkTemplate
from app.models.triage import (
    TriageClassificationSuggestion,
    TriageItem,
    TriageItemStatus,
)
from app.schemas.task import TaskCreate
from app.schemas.triage import (
    TriageActionRequest,
    TriageClassificationDraft,
    TriageConvertToTaskRequest,
    TriageDuplicateSuggestion,
    TriageDuplicateSuggestionsResponse,
    TriageDuplicateRequest,
    TriageItemCreate,
    TriageItemUpdate,
    TriageSnoozeRequest,
    TriageTaskDraftRequest,
    TriageTaskDraftResponse,
)
from app.services.task_service import TaskService
from app.services.request_source_service import RequestSourceService
from app.services.outbound_webhook_service import emit_outbound_webhook_event
from app.services.llm_service import LLMService
from app.utils.text_similarity import BM25Similarity, SimilarityDocument, normalize_text
from app.utils.time import as_utc, utc_now


class TriageConflictError(Exception):
    """Raised when a triage action conflicts with current item state."""


class TriageDraftNotFoundError(Exception):
    """Raised when referenced draft context does not exist."""


class TriageService:
    """Service for triage CRUD, inbox filtering, lifecycle actions, and conversion."""

    LIFECYCLE_UPDATE_FIELDS = {
        "status",
        "snoozed_until",
        "duplicate_of_id",
        "duplicate_task_id",
        "converted_task_id",
    }

    def __init__(self, db: AsyncSession):
        self.db = db
        self.task_service = TaskService(db)

    def _enum_value(self, value):
        """Normalize Pydantic enum values before assigning to string columns."""
        return value.value if hasattr(value, "value") else value

    def _query(self) -> Select:
        """Build the base triage query."""
        return select(TriageItem)

    def _response_options(self) -> tuple:
        """Return relationship loading options needed for API responses."""
        return (selectinload(TriageItem.request_source_links),)

    async def _exists(self, model, entity_id: int) -> bool:
        result = await self.db.execute(select(model.id).where(model.id == entity_id))
        return result.scalar_one_or_none() is not None

    async def _require_project_exists(self, project_id: Optional[int]) -> None:
        if project_id is not None and not await self._exists(Project, project_id):
            raise ValueError(f"Project with id {project_id} not found")

    async def _require_iteration_exists(self, iteration_id: Optional[int]) -> None:
        if iteration_id is not None and not await self._exists(Iteration, iteration_id):
            raise ValueError(f"Iteration with id {iteration_id} not found")

    async def _require_plannable_iteration(self, iteration_id: int) -> Iteration:
        """Load the target iteration for conversion, reserving lifecycle checks here."""
        result = await self.db.execute(select(Iteration).where(Iteration.id == iteration_id))
        iteration = result.scalar_one_or_none()
        if iteration is None:
            raise ValueError(f"Iteration with id {iteration_id} not found")
        return iteration

    async def _require_assignee_exists(self, assignee_id: Optional[int]) -> None:
        if assignee_id is not None and not await self._exists(TeamMember, assignee_id):
            raise ValueError(f"Team member with id {assignee_id} not found")

    async def _require_task_exists(self, task_id: Optional[int]) -> None:
        if task_id is not None and not await self._exists(Task, task_id):
            raise ValueError(f"Task with id {task_id} not found")

    async def _require_duplicate_item_exists(
        self,
        triage_item_id: int,
        duplicate_of_id: Optional[int],
    ) -> None:
        if duplicate_of_id is None:
            return
        if duplicate_of_id == triage_item_id:
            raise ValueError("A triage item cannot be a duplicate of itself.")
        if not await self._exists(TriageItem, duplicate_of_id):
            raise ValueError(f"Triage item with id {duplicate_of_id} not found")

    async def _validate_common_references(
        self,
        project_hint_id: Optional[int] = None,
        iteration_hint_id: Optional[int] = None,
        duplicate_of_id: Optional[int] = None,
        duplicate_task_id: Optional[int] = None,
        converted_task_id: Optional[int] = None,
        triage_item_id: Optional[int] = None,
    ) -> None:
        await self._require_project_exists(project_hint_id)
        await self._require_iteration_exists(iteration_hint_id)
        if triage_item_id is not None:
            await self._require_duplicate_item_exists(triage_item_id, duplicate_of_id)
        elif duplicate_of_id is not None and not await self._exists(TriageItem, duplicate_of_id):
            raise ValueError(f"Triage item with id {duplicate_of_id} not found")
        await self._require_task_exists(duplicate_task_id)
        await self._require_task_exists(converted_task_id)

    async def _record_triage_event(
        self,
        event_type: str,
        triage_item_id: int,
        payload: Optional[dict[str, Any]] = None,
    ) -> None:
        await self.task_service.record_task_event(
            None,
            event_type,
            {"triage_item_id": triage_item_id, **(payload or {})},
        )

    def _filtered_list_query(
        self,
        active: Optional[bool] = True,
        statuses: Optional[Sequence[TriageItemStatus | str]] = None,
        q: Optional[str] = None,
        source: Optional[str] = None,
    ) -> Select:
        """Build a triage list query without ordering or pagination."""
        query = self._query()
        now = utc_now()

        if statuses:
            status_values = [self._enum_value(status) for status in statuses]
            query = query.where(TriageItem.status.in_(status_values))
        elif active:
            query = query.where(
                or_(
                    TriageItem.status.in_([
                        TriageItemStatus.NEW.value,
                        TriageItemStatus.ACCEPTED.value,
                    ]),
                    and_(
                        TriageItem.status == TriageItemStatus.SNOOZED.value,
                        TriageItem.snoozed_until <= now,
                    ),
                )
            )

        if q:
            pattern = f"%{q}%"
            query = query.where(
                or_(
                    TriageItem.title.ilike(pattern),
                    TriageItem.description.ilike(pattern),
                    TriageItem.external_key.ilike(pattern),
                    TriageItem.source_url.ilike(pattern),
                )
            )

        if source:
            query = query.where(TriageItem.source == source)

        return query

    async def count_items(
        self,
        active: Optional[bool] = True,
        statuses: Optional[Sequence[TriageItemStatus | str]] = None,
        q: Optional[str] = None,
        source: Optional[str] = None,
    ) -> int:
        """Count triage items using the same filters as the list endpoint."""
        query = self._filtered_list_query(
            active=active,
            statuses=statuses,
            q=q,
            source=source,
        )
        result = await self.db.execute(
            select(func.count()).select_from(query.subquery())
        )
        return int(result.scalar_one())

    async def list_items(
        self,
        active: Optional[bool] = True,
        statuses: Optional[Sequence[TriageItemStatus | str]] = None,
        q: Optional[str] = None,
        source: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[TriageItem]:
        """List triage items with default active inbox filtering."""
        query = self._filtered_list_query(
            active=active,
            statuses=statuses,
            q=q,
            source=source,
        )

        query = query.options(*self._response_options())
        active_order = case(
            (TriageItem.status == TriageItemStatus.NEW.value, 0),
            (TriageItem.status == TriageItemStatus.SNOOZED.value, 1),
            (TriageItem.status == TriageItemStatus.ACCEPTED.value, 2),
            else_=3,
        )
        query = query.order_by(active_order, TriageItem.snoozed_until, TriageItem.created_at.desc())
        query = query.limit(limit).offset(offset)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_id(
        self,
        triage_item_id: int,
        *,
        for_update: bool = False,
    ) -> Optional[TriageItem]:
        """Get a triage item by ID, optionally locking it for a mutation."""
        query = (
            self._query()
            .options(*self._response_options())
            .where(TriageItem.id == triage_item_id)
        )
        if for_update:
            query = query.with_for_update()
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def list_classification_suggestions(
        self,
        triage_item_id: int,
        limit: int = 20,
    ) -> Optional[Sequence[TriageClassificationSuggestion]]:
        """List stored classification suggestions for a triage item."""
        if not await self._exists(TriageItem, triage_item_id):
            return None
        result = await self.db.execute(
            select(TriageClassificationSuggestion)
            .where(TriageClassificationSuggestion.triage_item_id == triage_item_id)
            .order_by(
                TriageClassificationSuggestion.created_at.desc(),
                TriageClassificationSuggestion.id.desc(),
            )
            .limit(limit)
        )
        return result.scalars().all()

    async def classify_item(
        self,
        triage_item_id: int,
        llm_service: Optional[LLMService] = None,
        *,
        commit: bool = True,
    ) -> Optional[TriageClassificationSuggestion]:
        """Create an advisory classification suggestion for a triage item."""
        item = await self._get_classification_item(triage_item_id)
        if not item:
            return None

        label_groups, label_meta = await self._classification_label_context()
        projects = await self._classification_project_context()
        assignees = await self._classification_assignee_context(item.iteration_hint_id)
        duplicate_candidates = await self._classification_duplicate_candidates(item.id)
        service = llm_service or await LLMService.from_runtime(self.db)
        draft = await service.classify_triage_item(
            triage_item=self._triage_item_context(item),
            label_groups=label_groups,
            projects=projects,
            assignees=assignees,
            duplicate_candidates=duplicate_candidates,
        )
        normalized = self._normalize_classification_draft(
            draft=draft,
            label_meta=label_meta,
            projects=projects,
            assignees=assignees,
            duplicate_candidates=duplicate_candidates,
        )

        suggestion = TriageClassificationSuggestion(
            triage_item_id=item.id,
            suggested_type_label_slug=normalized.suggested_type_label_slug,
            suggested_area_label_slug=normalized.suggested_area_label_slug,
            suggested_priority=normalized.suggested_priority,
            suggested_label_slugs=normalized.suggested_label_slugs,
            unmatched_label_text=normalized.unmatched_label_text,
            suggested_assignee_id=normalized.suggested_assignee_id,
            suggested_assignee_hint=normalized.suggested_assignee_hint,
            suggested_project_id=normalized.suggested_project_id,
            duplicate_candidates=normalized.duplicate_candidates,
            confidence=normalized.confidence,
            rationale=normalized.rationale,
            provider=getattr(service, "provider", None),
            model=getattr(service, "model", None),
            is_fallback=normalized.is_fallback,
            raw_response_json=normalized.raw_response_json,
        )
        self.db.add(suggestion)
        try:
            await self.db.flush()
            await emit_outbound_webhook_event(
                self.db,
                commit=False,
                event_type="triage.classification_suggested",
                entity_type="triage_item",
                entity_id=item.id,
                data={
                    "triage_item_id": item.id,
                    "classification_suggestion_id": suggestion.id,
                    "is_fallback": suggestion.is_fallback,
                    "confidence": suggestion.confidence,
                },
            )
            if commit:
                await self.db.commit()
                await self.db.refresh(suggestion)
        except Exception:
            if commit:
                await self.db.rollback()
            raise
        return suggestion

    async def draft_task(
        self,
        triage_item_id: int,
        data: TriageTaskDraftRequest,
        llm_service: Optional[LLMService] = None,
    ) -> Optional[TriageTaskDraftResponse]:
        """Generate transient task details for triage conversion."""
        item = await self._get_classification_item(triage_item_id)
        if not item:
            return None

        template = await self._get_task_draft_template(data.template_id)
        classification = await self._get_task_draft_classification(
            triage_item_id=item.id,
            classification_suggestion_id=data.classification_suggestion_id,
        )
        service = llm_service or await LLMService.from_runtime(self.db)
        draft = await service.draft_triage_task(
            triage_item=self._triage_item_context(item),
            template=self._task_template_context(template) if template else None,
            classification=(
                self._classification_suggestion_context(classification)
                if classification
                else None
            ),
            current_title=data.current_title,
            current_description=data.current_description,
        )
        if draft.provider is None:
            draft.provider = getattr(service, "provider", None)
        if draft.model is None:
            draft.model = getattr(service, "model", None)
        return draft

    async def _get_task_draft_template(
        self,
        template_id: Optional[int],
    ) -> Optional[WorkTemplate]:
        """Load and validate an optional active task template for drafting."""
        if template_id is None:
            return None

        result = await self.db.execute(
            select(WorkTemplate).where(WorkTemplate.id == template_id)
        )
        template = result.scalar_one_or_none()
        if not template:
            raise TriageDraftNotFoundError(f"Template with id {template_id} not found")
        if template.template_type != TemplateType.TASK.value or not template.is_active:
            raise ValueError("Template must be an active task template")
        return template

    async def _get_task_draft_classification(
        self,
        triage_item_id: int,
        classification_suggestion_id: Optional[int],
    ) -> Optional[TriageClassificationSuggestion]:
        """Load an explicit or latest classification suggestion for drafting."""
        if classification_suggestion_id is not None:
            result = await self.db.execute(
                select(TriageClassificationSuggestion)
                .where(TriageClassificationSuggestion.id == classification_suggestion_id)
            )
            suggestion = result.scalar_one_or_none()
            if not suggestion:
                raise TriageDraftNotFoundError(
                    f"Classification suggestion with id {classification_suggestion_id} not found"
                )
            if suggestion.triage_item_id != triage_item_id:
                raise ValueError("Classification suggestion belongs to another triage item")
            return suggestion

        result = await self.db.execute(
            select(TriageClassificationSuggestion)
            .where(TriageClassificationSuggestion.triage_item_id == triage_item_id)
            .order_by(
                TriageClassificationSuggestion.created_at.desc(),
                TriageClassificationSuggestion.id.desc(),
            )
            .limit(1)
        )
        return result.scalar_one_or_none()

    def _task_template_context(self, template: WorkTemplate) -> dict[str, Any]:
        """Return compact template context for task drafting."""
        return {
            "id": template.id,
            "name": template.name,
            "description": template.description,
            "default_title": template.default_title,
            "default_description": template.default_description,
            "default_priority": template.default_priority,
            "default_effort_days": template.default_effort_days,
            "default_labels": template.default_labels or [],
            "default_checklist": template.default_checklist or [],
            "default_payload": template.default_payload or {},
        }

    def _classification_suggestion_context(
        self,
        suggestion: TriageClassificationSuggestion,
    ) -> dict[str, Any]:
        """Return compact classification context for task drafting."""
        return {
            "id": suggestion.id,
            "suggested_type_label_slug": suggestion.suggested_type_label_slug,
            "suggested_area_label_slug": suggestion.suggested_area_label_slug,
            "suggested_priority": suggestion.suggested_priority,
            "suggested_label_slugs": suggestion.suggested_label_slugs or [],
            "unmatched_label_text": suggestion.unmatched_label_text or [],
            "suggested_assignee_id": suggestion.suggested_assignee_id,
            "suggested_assignee_hint": suggestion.suggested_assignee_hint,
            "suggested_project_id": suggestion.suggested_project_id,
            "duplicate_candidates": suggestion.duplicate_candidates or [],
            "confidence": suggestion.confidence,
            "rationale": suggestion.rationale,
            "is_fallback": suggestion.is_fallback,
        }

    async def _get_classification_item(
        self,
        triage_item_id: int,
    ) -> Optional[TriageItem]:
        """Load a triage item with context used by classification."""
        result = await self.db.execute(
            select(TriageItem)
            .options(
                selectinload(TriageItem.project_hint),
                selectinload(TriageItem.iteration_hint),
            )
            .where(TriageItem.id == triage_item_id)
        )
        return result.scalar_one_or_none()

    async def _classification_label_context(
        self,
    ) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        """Return active label context and normalization metadata."""
        result = await self.db.execute(
            select(LabelGroup)
            .options(selectinload(LabelGroup.labels))
            .where(LabelGroup.is_active.is_(True))
            .order_by(LabelGroup.sort_order, LabelGroup.name, LabelGroup.id)
        )
        groups = result.scalars().unique().all()
        context_groups: list[dict[str, Any]] = []
        active_slugs: set[str] = set()
        type_slugs: set[str] = set()
        area_slugs: set[str] = set()

        for group in groups:
            labels = [
                {
                    "id": label.id,
                    "slug": label.slug,
                    "name": label.name,
                    "description": label.description,
                }
                for label in group.labels
                if label.is_active
            ]
            if not labels:
                continue
            context_groups.append(
                {
                    "id": group.id,
                    "key": group.key,
                    "name": group.name,
                    "labels": labels,
                }
            )
            group_slugs = {label["slug"] for label in labels}
            active_slugs.update(group_slugs)
            if group.key == "type":
                type_slugs.update(group_slugs)
            if group.key == "area":
                area_slugs.update(group_slugs)

        return context_groups, {
            "active_slugs": active_slugs,
            "type_slugs": type_slugs,
            "area_slugs": area_slugs,
        }

    async def _classification_project_context(self) -> list[dict[str, Any]]:
        """Return compact project candidates for classification."""
        result = await self.db.execute(
            select(Project).order_by(Project.sort_order, Project.target_date, Project.name, Project.id)
        )
        return [
            {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "status": project.status,
                "health": project.health,
            }
            for project in result.scalars().all()
        ]

    async def _classification_assignee_context(
        self,
        iteration_id: Optional[int],
    ) -> list[dict[str, Any]]:
        """Return iteration team member candidates for classification."""
        if iteration_id is None:
            return []
        result = await self.db.execute(
            select(TeamMember)
            .options(selectinload(TeamMember.profile).selectinload(TeamMemberProfile.skills))
            .where(TeamMember.iteration_id == iteration_id)
            .order_by(TeamMember.name, TeamMember.id)
        )
        members = result.scalars().unique().all()
        assignees: list[dict[str, Any]] = []
        for member in members:
            profile = member.profile
            assignee = {
                "id": member.id,
                "name": member.name,
                "position": member.position,
                "profile": None,
            }
            if profile:
                assignee["profile"] = {
                    "id": profile.id,
                    "display_name": profile.display_name,
                    "headline": profile.headline,
                    "summary": profile.summary,
                    "automation_enabled": profile.automation_enabled,
                    "skills": [
                        {
                            "skill_key": skill.skill_key,
                            "skill_name": skill.skill_name,
                            "category": skill.category,
                            "level": skill.level,
                            "interest": skill.interest,
                            "is_weakness": skill.is_weakness,
                            "keywords_json": skill.keywords_json or [],
                        }
                        for skill in profile.skills
                    ],
                }
            assignees.append(assignee)
        return assignees

    async def _classification_duplicate_candidates(
        self,
        triage_item_id: int,
    ) -> list[dict[str, Any]]:
        """Return flattened duplicate candidates from the existing advisory search."""
        suggestions = await self.get_duplicate_suggestions(
            triage_item_id,
            limit_per_type=5,
            min_score=0.1,
        )
        if not suggestions:
            return []
        candidates = [
            *suggestions.triage_items,
            *suggestions.tasks,
        ]
        return [
            suggestion.model_dump()
            for suggestion in sorted(candidates, key=lambda item: (-item.score, item.target_id))
        ]

    def _triage_item_context(self, item: TriageItem) -> dict[str, Any]:
        """Return compact triage item context for classification."""
        return {
            "id": item.id,
            "title": item.title,
            "description": item.description,
            "source": item.source,
            "source_url": item.source_url,
            "external_key": item.external_key,
            "status": item.status,
            "priority_hint": item.priority_hint,
            "assignee_hint": item.assignee_hint,
            "project_hint_id": item.project_hint_id,
            "project_hint_name": item.project_hint.name if item.project_hint else None,
            "iteration_hint_id": item.iteration_hint_id,
            "iteration_hint_name": item.iteration_hint.name if item.iteration_hint else None,
            "labels": item.labels or [],
        }

    def _normalize_classification_draft(
        self,
        draft: TriageClassificationDraft,
        label_meta: dict[str, Any],
        projects: list[dict[str, Any]],
        assignees: list[dict[str, Any]],
        duplicate_candidates: list[dict[str, Any]],
    ) -> TriageClassificationDraft:
        """Normalize provider/fallback suggestions against current system state."""
        active_slugs = label_meta["active_slugs"]
        type_slugs = label_meta["type_slugs"]
        area_slugs = label_meta["area_slugs"]
        project_ids = {project["id"] for project in projects}
        assignee_ids = {assignee["id"] for assignee in assignees}

        type_slug = self._valid_slug(draft.suggested_type_label_slug, type_slugs)
        area_slug = self._valid_slug(draft.suggested_area_label_slug, area_slugs)

        suggested_label_slugs: list[str] = []
        unmatched_label_text = [
            text for text in self._dedupe_strings(draft.unmatched_label_text)
            if text
        ]
        for raw_slug in [
            *draft.suggested_label_slugs,
            type_slug,
            area_slug,
        ]:
            slug = self._slug_text(raw_slug)
            if not slug:
                continue
            if slug in active_slugs:
                if slug not in suggested_label_slugs:
                    suggested_label_slugs.append(slug)
            elif slug not in unmatched_label_text:
                unmatched_label_text.append(slug)

        suggested_project_id = (
            draft.suggested_project_id
            if draft.suggested_project_id in project_ids
            else None
        )
        suggested_assignee_id = (
            draft.suggested_assignee_id
            if draft.suggested_assignee_id in assignee_ids
            else None
        )
        assignee_hint = self._clean_optional_text(draft.suggested_assignee_hint)

        return TriageClassificationDraft(
            suggested_type_label_slug=type_slug,
            suggested_area_label_slug=area_slug,
            suggested_priority=draft.suggested_priority,
            suggested_label_slugs=suggested_label_slugs,
            unmatched_label_text=unmatched_label_text,
            suggested_assignee_id=suggested_assignee_id,
            suggested_assignee_hint=assignee_hint,
            suggested_project_id=suggested_project_id,
            duplicate_candidates=duplicate_candidates,
            confidence=draft.confidence,
            rationale=self._clean_optional_text(draft.rationale),
            language=draft.language,
            is_fallback=draft.is_fallback,
            raw_response_json=draft.raw_response_json,
        )

    def _slug_text(self, value: Any) -> Optional[str]:
        """Normalize a label slug candidate."""
        if value is None:
            return None
        slug = str(value).strip().lower()
        return slug or None

    def _valid_slug(self, value: Any, valid_slugs: set[str]) -> Optional[str]:
        """Return a slug only when it belongs to the expected label group."""
        slug = self._slug_text(value)
        if slug and slug in valid_slugs:
            return slug
        return None

    def _clean_optional_text(self, value: Optional[str]) -> Optional[str]:
        """Trim optional text fields."""
        if value is None:
            return None
        stripped = str(value).strip()
        return stripped or None

    def _dedupe_strings(self, values: list[str]) -> list[str]:
        """Return non-empty strings without duplicates."""
        result: list[str] = []
        for value in values or []:
            text = str(value).strip()
            if text and text not in result:
                result.append(text)
        return result

    async def create(
        self,
        data: TriageItemCreate,
        *,
        commit: bool = True,
    ) -> TriageItem:
        """Create a triage item."""
        await self._validate_common_references(
            project_hint_id=data.project_hint_id,
            iteration_hint_id=data.iteration_hint_id,
            duplicate_of_id=data.duplicate_of_id,
            duplicate_task_id=data.duplicate_task_id,
            converted_task_id=data.converted_task_id,
        )

        item = TriageItem(
            title=data.title,
            description=data.description,
            source=data.source,
            source_url=data.source_url,
            external_key=data.external_key,
            status=self._enum_value(data.status),
            priority_hint=data.priority_hint,
            assignee_hint=data.assignee_hint,
            project_hint_id=data.project_hint_id,
            iteration_hint_id=data.iteration_hint_id,
            labels=data.labels,
            metadata_json=data.metadata_json,
            snoozed_until=data.snoozed_until,
            duplicate_of_id=data.duplicate_of_id,
            duplicate_task_id=data.duplicate_task_id,
            converted_task_id=data.converted_task_id,
        )
        self.db.add(item)
        try:
            await self.db.flush()
            await self._record_triage_event(
                "triage_item_created",
                item.id,
                {
                    "title": item.title,
                    "status": item.status,
                    "source": item.source,
                    "external_key": item.external_key,
                    "metadata_json": item.metadata_json,
                },
            )
            await emit_outbound_webhook_event(
                self.db,
                commit=False,
                event_type="triage.created",
                entity_type="triage_item",
                entity_id=item.id,
                data={
                    "triage_item_id": item.id,
                    "title": item.title,
                    "status": item.status,
                    "source": item.source,
                    "external_key": item.external_key,
                    "project_hint_id": item.project_hint_id,
                    "iteration_hint_id": item.iteration_hint_id,
                    "metadata_json": item.metadata_json,
                },
            )
            if commit:
                await self.db.commit()
                await self.db.refresh(item)
        except Exception:
            if commit:
                await self.db.rollback()
            raise
        return item

    async def update(
        self,
        triage_item_id: int,
        data: TriageItemUpdate,
        *,
        commit: bool = True,
    ) -> Optional[TriageItem]:
        """Apply editable triage metadata updates."""
        item = await self.get_by_id(triage_item_id)
        if not item:
            return None

        lifecycle_fields = self.LIFECYCLE_UPDATE_FIELDS.intersection(data.model_fields_set)
        if lifecycle_fields:
            fields = ", ".join(sorted(lifecycle_fields))
            raise ValueError(f"Use triage action endpoints to update: {fields}")

        update_data = data.model_dump(exclude_unset=True)
        await self._validate_common_references(
            project_hint_id=update_data.get("project_hint_id"),
            iteration_hint_id=update_data.get("iteration_hint_id"),
            triage_item_id=triage_item_id,
        )

        changed_fields: dict[str, dict[str, Any]] = {}
        for field, value in update_data.items():
            old_value = getattr(item, field)
            value = self._enum_value(value)
            if old_value != value:
                changed_fields[field] = {"old": old_value, "new": value}
                setattr(item, field, value)

        if changed_fields:
            await self._record_triage_event(
                "triage_item_updated",
                item.id,
                {"changes": changed_fields},
            )

        try:
            if changed_fields:
                await emit_outbound_webhook_event(
                    self.db,
                    commit=False,
                    event_type="triage.updated",
                    entity_type="triage_item",
                    entity_id=item.id,
                    data={
                        "triage_item_id": item.id,
                        "title": item.title,
                        "status": item.status,
                        "changes": changed_fields,
                    },
                )
            if commit:
                await self.db.commit()
                await self.db.refresh(item)
        except Exception:
            if commit:
                await self.db.rollback()
            raise
        return item

    async def accept(
        self,
        triage_item_id: int,
        data: Optional[TriageActionRequest] = None,
        *,
        commit: bool = True,
    ) -> Optional[TriageItem]:
        """Accept a triage item into the intake inbox."""
        item = await self.get_by_id(triage_item_id)
        if not item:
            return None
        old_status = item.status
        item.status = TriageItemStatus.ACCEPTED.value
        item.snoozed_until = None
        item.duplicate_of_id = None
        item.duplicate_task_id = None
        await self._record_triage_event(
            "triage_item_accepted",
            item.id,
            {
                "from_status": old_status,
                "to_status": item.status,
                "reason": data.reason if data else None,
            },
        )
        try:
            await emit_outbound_webhook_event(
                self.db,
                commit=False,
                event_type="triage.accepted",
                entity_type="triage_item",
                entity_id=item.id,
                data={
                    "triage_item_id": item.id,
                    "from_status": old_status,
                    "to_status": item.status,
                    "reason": data.reason if data else None,
                },
            )
            if commit:
                await self.db.commit()
                await self.db.refresh(item)
        except Exception:
            if commit:
                await self.db.rollback()
            raise
        return item

    async def decline(
        self,
        triage_item_id: int,
        data: Optional[TriageActionRequest] = None,
        *,
        commit: bool = True,
    ) -> Optional[TriageItem]:
        """Decline a triage item while keeping it searchable."""
        item = await self.get_by_id(triage_item_id)
        if not item:
            return None
        old_status = item.status
        item.status = TriageItemStatus.DECLINED.value
        item.snoozed_until = None
        item.duplicate_of_id = None
        item.duplicate_task_id = None
        await self._record_triage_event(
            "triage_item_declined",
            item.id,
            {
                "from_status": old_status,
                "to_status": item.status,
                "reason": data.reason if data else None,
            },
        )
        try:
            await emit_outbound_webhook_event(
                self.db,
                commit=False,
                event_type="triage.declined",
                entity_type="triage_item",
                entity_id=item.id,
                data={
                    "triage_item_id": item.id,
                    "from_status": old_status,
                    "to_status": item.status,
                    "reason": data.reason if data else None,
                },
            )
            if commit:
                await self.db.commit()
                await self.db.refresh(item)
        except Exception:
            if commit:
                await self.db.rollback()
            raise
        return item

    async def snooze(
        self,
        triage_item_id: int,
        data: TriageSnoozeRequest,
        *,
        commit: bool = True,
    ) -> Optional[TriageItem]:
        """Snooze a triage item until a future time."""
        item = await self.get_by_id(triage_item_id)
        if not item:
            return None
        snoozed_until = as_utc(data.snoozed_until)
        if snoozed_until <= utc_now():
            raise ValueError("snoozed_until must be in the future")

        old_status = item.status
        item.status = TriageItemStatus.SNOOZED.value
        item.snoozed_until = snoozed_until
        item.duplicate_of_id = None
        item.duplicate_task_id = None
        await self._record_triage_event(
            "triage_item_snoozed",
            item.id,
            {
                "from_status": old_status,
                "to_status": item.status,
                "snoozed_until": item.snoozed_until,
                "reason": data.reason,
            },
        )
        try:
            await emit_outbound_webhook_event(
                self.db,
                commit=False,
                event_type="triage.snoozed",
                entity_type="triage_item",
                entity_id=item.id,
                data={
                    "triage_item_id": item.id,
                    "from_status": old_status,
                    "to_status": item.status,
                    "snoozed_until": snoozed_until.isoformat() if snoozed_until else None,
                    "reason": data.reason,
                },
            )
            if commit:
                await self.db.commit()
                await self.db.refresh(item)
        except Exception:
            if commit:
                await self.db.rollback()
            raise
        return item

    async def mark_duplicate(
        self,
        triage_item_id: int,
        data: TriageDuplicateRequest,
        *,
        commit: bool = True,
    ) -> Optional[TriageItem]:
        """Mark a triage item as duplicate of another item or task."""
        item = await self.get_by_id(triage_item_id)
        if not item:
            return None

        await self._require_duplicate_item_exists(triage_item_id, data.duplicate_of_id)
        await self._require_task_exists(data.duplicate_task_id)

        old_status = item.status
        item.status = TriageItemStatus.DUPLICATE.value
        item.snoozed_until = None
        item.duplicate_of_id = data.duplicate_of_id
        item.duplicate_task_id = data.duplicate_task_id
        if data.duplicate_task_id is not None and data.link_request_to_duplicate_task:
            await RequestSourceService(self.db).link_triage_item_as_task_request(
                item,
                data.duplicate_task_id,
            )
        await self._record_triage_event(
            "triage_item_marked_duplicate",
            item.id,
            {
                "from_status": old_status,
                "to_status": item.status,
                "duplicate_of_id": item.duplicate_of_id,
                "duplicate_task_id": item.duplicate_task_id,
                "reason": data.reason,
            },
        )
        try:
            await emit_outbound_webhook_event(
                self.db,
                commit=False,
                event_type="triage.duplicate_marked",
                entity_type="triage_item",
                entity_id=item.id,
                data={
                    "triage_item_id": item.id,
                    "from_status": old_status,
                    "to_status": item.status,
                    "duplicate_of_id": item.duplicate_of_id,
                    "duplicate_task_id": item.duplicate_task_id,
                    "reason": data.reason,
                },
            )
            if commit:
                await self.db.commit()
                await self.db.refresh(item)
        except Exception:
            if commit:
                await self.db.rollback()
            raise
        return item

    def _json_list(self, value: Optional[str]) -> list[str]:
        """Parse JSON list strings used by task tags."""
        if not value:
            return []
        try:
            parsed = json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return []
        if not isinstance(parsed, list):
            return []
        return [str(item) for item in parsed if str(item).strip()]

    def _candidate_text(self, *parts: Any) -> str:
        """Build weighted searchable text from candidate fields."""
        text_parts: list[str] = []
        for part in parts:
            if part is None:
                continue
            if isinstance(part, list):
                text_parts.extend(str(item) for item in part if str(item).strip())
                continue
            value = str(part).strip()
            if value:
                text_parts.append(value)
        return " ".join(text_parts)

    def _triage_item_text(self, item: TriageItem) -> str:
        """Build duplicate-search text for a triage item."""
        return self._candidate_text(
            item.title,
            item.title,
            item.title,
            item.description,
            item.source,
            item.external_key,
            item.source_url,
            item.labels,
            item.assignee_hint,
            item.project_hint.name if item.project_hint else None,
            item.iteration_hint.name if item.iteration_hint else None,
        )

    def _task_text(self, task: Task) -> str:
        """Build duplicate-search text for a task."""
        labels = self._json_list(task.tags)
        return self._candidate_text(
            task.title,
            task.title,
            task.title,
            task.description,
            task.source,
            task.external_key,
            task.source_url,
            labels,
            task.assignee.name if task.assignee else None,
            task.project.name if task.project else None,
            task.iteration.name if task.iteration else None,
        )

    def _score_boosts(
        self,
        source_item: TriageItem,
        candidate_title: str,
        candidate_source: Optional[str],
        candidate_external_key: Optional[str],
        candidate_source_url: Optional[str],
        candidate_labels: list[str],
    ) -> tuple[float, list[str]]:
        """Return deterministic duplicate-match boosts and signals."""
        boost = 0.0
        signals: list[str] = []

        if normalize_text(source_item.title) == normalize_text(candidate_title):
            boost += 5.0
            signals.append("exact title")

        if (
            source_item.source
            and source_item.external_key
            and source_item.source == candidate_source
            and source_item.external_key == candidate_external_key
        ):
            boost += 10.0
            signals.append("same source/external key")

        if (
            source_item.source_url
            and candidate_source_url
            and normalize_text(source_item.source_url) == normalize_text(candidate_source_url)
        ):
            boost += 8.0
            signals.append("same source URL")

        source_labels = {normalize_text(label) for label in source_item.labels if normalize_text(label)}
        labels = {normalize_text(label) for label in candidate_labels if normalize_text(label)}
        shared_labels = sorted(source_labels.intersection(labels))
        if shared_labels:
            boost += min(len(shared_labels), 4) * 0.75
            signals.append(f"shared labels: {', '.join(shared_labels)}")

        return boost, signals

    async def get_duplicate_suggestions(
        self,
        triage_item_id: int,
        limit_per_type: int = 5,
        min_score: float = 0.1,
    ) -> Optional[TriageDuplicateSuggestionsResponse]:
        """Return advisory duplicate candidates for a triage item."""
        source_result = await self.db.execute(
            select(TriageItem)
            .options(
                selectinload(TriageItem.project_hint),
                selectinload(TriageItem.iteration_hint),
            )
            .where(TriageItem.id == triage_item_id)
        )
        source_item = source_result.scalar_one_or_none()
        if not source_item:
            return None

        triage_result = await self.db.execute(
            select(TriageItem)
            .options(
                selectinload(TriageItem.project_hint),
                selectinload(TriageItem.iteration_hint),
            )
            .where(TriageItem.id != triage_item_id)
        )
        task_result = await self.db.execute(
            select(Task).options(
                selectinload(Task.project),
                selectinload(Task.iteration),
                selectinload(Task.assignee),
            )
        )
        triage_candidates = triage_result.scalars().all()
        task_candidates = task_result.scalars().all()

        candidate_records: dict[str, tuple[str, TriageItem | Task]] = {}
        documents: list[SimilarityDocument] = []
        for item in triage_candidates:
            key = f"triage_item:{item.id}"
            candidate_records[key] = ("triage_item", item)
            documents.append(SimilarityDocument(key=key, text=self._triage_item_text(item)))
        for task in task_candidates:
            key = f"task:{task.id}"
            candidate_records[key] = ("task", task)
            documents.append(SimilarityDocument(key=key, text=self._task_text(task)))

        scorer = BM25Similarity()
        scorer.fit(documents)
        bm25_scores = {result.key: result.score for result in scorer.score(self._triage_item_text(source_item))}

        triage_suggestions: list[TriageDuplicateSuggestion] = []
        task_suggestions: list[TriageDuplicateSuggestion] = []
        for key, (target_type, candidate) in candidate_records.items():
            base_score = bm25_scores.get(key, 0.0)
            signals = ["text similarity"] if base_score > 0 else []

            if target_type == "triage_item":
                item = candidate
                assert isinstance(item, TriageItem)
                labels = item.labels or []
                boost, boost_signals = self._score_boosts(
                    source_item,
                    item.title,
                    item.source,
                    item.external_key,
                    item.source_url,
                    labels,
                )
                score = base_score + boost
                if score < min_score:
                    continue
                triage_suggestions.append(
                    TriageDuplicateSuggestion(
                        target_type="triage_item",
                        target_id=item.id,
                        title=item.title,
                        description=item.description,
                        status=item.status,
                        source=item.source,
                        source_url=item.source_url,
                        external_key=item.external_key,
                        labels=labels,
                        project_id=item.project_hint_id,
                        iteration_id=item.iteration_hint_id,
                        score=round(score, 4),
                        signals=[*signals, *boost_signals],
                    )
                )
                continue

            task = candidate
            assert isinstance(task, Task)
            labels = self._json_list(task.tags)
            boost, boost_signals = self._score_boosts(
                source_item,
                task.title,
                task.source,
                task.external_key,
                task.source_url,
                labels,
            )
            score = base_score + boost
            if score < min_score:
                continue
            task_suggestions.append(
                TriageDuplicateSuggestion(
                    target_type="task",
                    target_id=task.id,
                    title=task.title,
                    description=task.description,
                    status=task.status,
                    source=task.source,
                    source_url=task.source_url,
                    external_key=task.external_key,
                    labels=labels,
                    project_id=task.project_id,
                    iteration_id=task.iteration_id,
                    score=round(score, 4),
                    signals=[*signals, *boost_signals],
                )
            )

        sort_key = lambda suggestion: (-suggestion.score, suggestion.target_id)
        return TriageDuplicateSuggestionsResponse(
            triage_item_id=triage_item_id,
            triage_items=sorted(triage_suggestions, key=sort_key)[:limit_per_type],
            tasks=sorted(task_suggestions, key=sort_key)[:limit_per_type],
        )

    async def _require_dependencies_in_iteration(
        self,
        dependency_ids: list[int],
        iteration_id: int,
    ) -> None:
        if not dependency_ids:
            return
        result = await self.db.execute(
            select(Task.id, Task.iteration_id).where(Task.id.in_(dependency_ids))
        )
        rows = result.fetchall()
        found = {row.id: row.iteration_id for row in rows}
        missing = [task_id for task_id in dependency_ids if task_id not in found]
        if missing:
            raise ValueError(f"Task dependency not found: {missing[0]}")
        wrong_iteration = [
            task_id for task_id, dep_iteration_id in found.items()
            if dep_iteration_id != iteration_id
        ]
        if wrong_iteration:
            raise ValueError("Task dependencies must belong to the selected iteration")

    async def convert_to_task(
        self,
        triage_item_id: int,
        data: TriageConvertToTaskRequest,
        *,
        commit: bool = True,
    ) -> Optional[tuple[TriageItem, Task]]:
        """Convert a triage item to a planned task."""
        item = await self.get_by_id(triage_item_id, for_update=True)
        if not item:
            return None
        if item.status == TriageItemStatus.CONVERTED.value or item.converted_task_id is not None:
            raise TriageConflictError("Triage item has already been converted")

        target_iteration = await self._require_plannable_iteration(data.iteration_id)
        iteration_project_id = target_iteration.project_id
        project_id_was_set = "project_id" in data.model_fields_set
        if iteration_project_id is not None:
            if data.project_id is not None and data.project_id != iteration_project_id:
                raise ValueError("Task project must match the scoped iteration project.")
            project_id = iteration_project_id
        else:
            if item.project_hint_id is not None and not project_id_was_set:
                raise ValueError(
                    "Triage conversion into an unscoped iteration requires an explicit project_id or null project_id."
                )
            project_id = data.project_id if project_id_was_set else item.project_hint_id
        await self._require_project_exists(project_id)
        await self.task_service.require_iteration_assignee(data.assignee_id, data.iteration_id)
        await self._require_dependencies_in_iteration(data.depends_on, data.iteration_id)

        description = data.description if data.description is not None else item.description
        structured_fields = (
            data.scope,
            data.out_of_scope,
            data.suggested_checklist,
            data.acceptance_criteria,
            data.verification,
            data.expected_artifacts,
            data.risks,
            data.implementation_notes,
            data.open_questions,
        )
        if any(structured_fields):
            description = self._structured_task_brief(
                title=data.title or item.title,
                context=description,
                source=item.source,
                source_url=item.source_url,
                external_key=item.external_key,
                scope=data.scope,
                out_of_scope=data.out_of_scope,
                checklist=data.suggested_checklist,
                acceptance_criteria=data.acceptance_criteria,
                verification=data.verification,
                expected_artifacts=data.expected_artifacts,
                risks=data.risks,
                implementation_notes=data.implementation_notes,
                open_questions=data.open_questions,
            )

        task_data = TaskCreate(
            title=data.title or item.title,
            description=description,
            priority=data.priority if data.priority is not None else (item.priority_hint or 5),
            effort_days=data.effort_days,
            effort_hours=data.effort_hours,
            assignee_id=data.assignee_id,
            project_id=project_id,
            depends_on=data.depends_on,
            tags=data.tags if data.tags is not None else item.labels,
            external_key=item.external_key,
            source=item.source or "triage",
            source_url=item.source_url,
        )
        try:
            old_status = item.status
            reservation = await self.db.execute(
                update(TriageItem)
                .where(
                    TriageItem.id == item.id,
                    TriageItem.status != TriageItemStatus.CONVERTED.value,
                    TriageItem.converted_task_id.is_(None),
                )
                .values(status=TriageItemStatus.CONVERTED.value)
            )
            if reservation.rowcount != 1:
                raise TriageConflictError("Triage item has already been converted")
            # The guarded update is a cross-database reservation. PostgreSQL's
            # row lock serializes callers; SQLite's atomic write predicate keeps
            # its no-op FOR UPDATE implementation from admitting two tasks.
            item.status = TriageItemStatus.CONVERTED.value

            task = await self.task_service.create(
                data.iteration_id,
                task_data,
                commit=False,
            )
            await RequestSourceService(self.db).copy_triage_links_to_task(item.id, task.id)

            item.converted_task_id = task.id
            item.snoozed_until = None
            item.duplicate_of_id = None
            item.duplicate_task_id = None
            await self._record_triage_event(
                "triage_item_converted",
                item.id,
                {
                    "from_status": old_status,
                    "to_status": item.status,
                    "converted_task_id": task.id,
                },
            )
            await self.task_service.record_task_event(
                task.id,
                "triage_item_converted",
                {
                    "triage_item_id": item.id,
                    "from_status": old_status,
                    "to_status": item.status,
                },
            )
            await emit_outbound_webhook_event(
                self.db,
                commit=False,
                event_type="triage.converted",
                entity_type="triage_item",
                entity_id=item.id,
                data={
                    "triage_item_id": item.id,
                    "converted_task_id": task.id,
                    "from_status": old_status,
                    "to_status": item.status,
                    "iteration_id": data.iteration_id,
                    "project_id": project_id,
                },
            )
            await self.db.flush()
            if commit:
                await self.db.commit()
                await self.db.refresh(item)
        except Exception:
            if commit:
                await self.db.rollback()
            raise
        loaded_task = await self.task_service.get_by_id(task.id)
        return item, loaded_task or task

    @staticmethod
    def _structured_task_brief(
        *,
        title: str,
        context: Optional[str],
        source: Optional[str],
        source_url: Optional[str],
        external_key: Optional[str],
        scope: list[str],
        out_of_scope: list[str],
        checklist: list[str],
        acceptance_criteria: list[str],
        verification: list[str],
        expected_artifacts: list[str],
        risks: list[str],
        implementation_notes: list[str],
        open_questions: list[str],
    ) -> str:
        """Preserve a transient triage draft as a portable Markdown task brief."""

        def bullets(values: list[str]) -> str:
            return "\n".join(f"- {value.strip()}" for value in values if value.strip())

        source_lines = [context.strip()] if context and context.strip() else []
        if source:
            source_lines.append(f"Source: {source}")
        if source_url:
            source_lines.append(f"Source URL: {source_url}")
        if external_key:
            source_lines.append(f"External key: {external_key}")
        sections = [
            ("Goal", title.strip()),
            ("Context and sources", "\n\n".join(source_lines)),
            ("Scope", bullets(scope)),
            ("Out of scope", bullets(out_of_scope)),
            ("Acceptance criteria", bullets(acceptance_criteria)),
            ("Verification", bullets(verification)),
            ("Implementation checklist", bullets(checklist)),
            ("Expected artifacts", bullets(expected_artifacts)),
            ("Risks", bullets(risks)),
            ("Implementation notes", bullets(implementation_notes)),
            ("Open questions", bullets(open_questions)),
        ]
        return "\n\n".join(f"## {heading}\n{body}" for heading, body in sections).rstrip()

"""Explainable assignee recommendations from team capability profiles."""
import json
import re
from dataclasses import dataclass
from datetime import date
from typing import Any, Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.task import Task
from app.models.team_member import TeamMember, TeamMemberProfile, TeamMemberProfileSkill
from app.models.triage import TriageClassificationSuggestion, TriageItem
from app.schemas.team import AssigneeRecommendationResponse
from app.services.team_service import TeamService


TOKEN_PATTERN = re.compile(r"[a-z0-9+#.:-]+")


@dataclass
class RecommendationContext:
    """Normalized work item context for assignee recommendation scoring."""
    title: str
    description: Optional[str] = None
    labels: list[str] | None = None
    source: Optional[str] = None
    external_key: Optional[str] = None
    assignee_hint: Optional[str] = None
    project_name: Optional[str] = None
    priority: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    current_assignee_id: Optional[int] = None


class AssigneeRecommendationService:
    """Rank iteration team members for task and triage assignment."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.team_service = TeamService(db)

    async def recommend_for_triage(
        self,
        triage_item_id: int,
        iteration_id: Optional[int] = None,
    ) -> Optional[list[AssigneeRecommendationResponse]]:
        """Return ranked assignee recommendations for a triage item."""
        result = await self.db.execute(
            select(TriageItem)
            .options(selectinload(TriageItem.project_hint))
            .where(TriageItem.id == triage_item_id)
        )
        item = result.scalar_one_or_none()
        if not item:
            return None

        effective_iteration_id = iteration_id or item.iteration_hint_id
        if effective_iteration_id is None:
            raise ValueError("iteration_id is required when the triage item has no iteration hint")

        latest_classification = await self._latest_classification(item.id)
        labels = list(item.labels or [])
        if latest_classification:
            labels.extend(latest_classification.suggested_label_slugs or [])
            labels.extend([
                value
                for value in [
                    latest_classification.suggested_type_label_slug,
                    latest_classification.suggested_area_label_slug,
                ]
                if value
            ])

        context = RecommendationContext(
            title=item.title,
            description=item.description,
            labels=self._dedupe(labels),
            source=item.source,
            external_key=item.external_key,
            assignee_hint=item.assignee_hint or (
                latest_classification.suggested_assignee_hint
                if latest_classification
                else None
            ),
            project_name=item.project_hint.name if item.project_hint else None,
            priority=item.priority_hint or (
                latest_classification.suggested_priority
                if latest_classification
                else None
            ),
        )
        return await self._rank(effective_iteration_id, context)

    async def recommend_for_task(
        self,
        task_id: int,
    ) -> Optional[list[AssigneeRecommendationResponse]]:
        """Return ranked assignee recommendations for a task."""
        result = await self.db.execute(
            select(Task)
            .options(
                selectinload(Task.project),
                selectinload(Task.assignee),
            )
            .where(Task.id == task_id)
        )
        task = result.scalar_one_or_none()
        if not task:
            return None

        context = RecommendationContext(
            title=task.title,
            description=task.description,
            labels=self._parse_task_tags(task.tags),
            source=task.source,
            external_key=task.external_key,
            assignee_hint=task.assignee.name if task.assignee else None,
            project_name=task.project.name if task.project else None,
            priority=task.priority,
            start_date=task.start_date,
            end_date=task.end_date,
            current_assignee_id=task.assignee_id,
        )
        return await self._rank(task.iteration_id, context)

    async def _latest_classification(
        self,
        triage_item_id: int,
    ) -> Optional[TriageClassificationSuggestion]:
        """Load the latest stored triage classification suggestion."""
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

    async def _rank(
        self,
        iteration_id: int,
        context: RecommendationContext,
    ) -> list[AssigneeRecommendationResponse]:
        """Rank all team members in an iteration against normalized context."""
        result = await self.db.execute(
            select(TeamMember)
            .options(
                selectinload(TeamMember.profile).selectinload(TeamMemberProfile.skills),
                selectinload(TeamMember.vacations),
                selectinload(TeamMember.tasks),
            )
            .where(TeamMember.iteration_id == iteration_id)
            .order_by(TeamMember.name, TeamMember.id)
        )
        candidates = result.scalars().unique().all()
        return sorted(
            [
                await self._score_candidate(candidate, context)
                for candidate in candidates
            ],
            key=lambda item: (-item.score, item.name.lower(), item.team_member_id),
        )

    async def _score_candidate(
        self,
        member: TeamMember,
        context: RecommendationContext,
    ) -> AssigneeRecommendationResponse:
        """Score one candidate and build a readable rationale."""
        score = 20.0
        matched_skills: list[str] = []
        weakness_matches: list[str] = []
        workload_warnings: list[str] = []
        reasons: list[str] = []
        profile = member.profile
        context_text = self._context_text(context)

        if context.current_assignee_id == member.id:
            score += 8
            reasons.append("already assigned")

        if context.assignee_hint and self._normalize(context.assignee_hint) == self._normalize(member.name):
            score += 25
            reasons.append("matches assignee hint")

        if profile and profile.automation_enabled:
            profile_text = " ".join(
                part
                for part in [profile.headline, profile.summary, profile.notes]
                if part
            ).lower()
            if profile_text and any(token in profile_text for token in self._context_tokens(context_text)):
                score += 5
                reasons.append("profile text overlaps with work context")

            for skill in profile.skills:
                if self._skill_matches(skill, context_text):
                    label = skill.skill_name
                    if skill.is_weakness:
                        penalty = 12 + max(0, 4 - skill.level) * 4
                        score -= penalty
                        weakness_matches.append(label)
                    else:
                        boost = 12 + skill.level * 7 + skill.interest * 2
                        score += boost
                        matched_skills.append(label)
        elif profile and not profile.automation_enabled:
            score -= 8
            workload_warnings.append("Profile automation is disabled")
        else:
            score -= 5
            workload_warnings.append("No reusable capability profile is linked")

        workload = await self.team_service.get_workload(member.id)
        if workload:
            if workload.workload_status == "red":
                score -= 25
                workload_warnings.append("Workload is red")
            elif workload.workload_status == "yellow":
                score -= 10
                workload_warnings.append("Workload is near capacity")
            else:
                score += min(12, max(0.0, workload.free_days) * 1.5)
                reasons.append("has available capacity")

        if context.start_date and context.end_date:
            overlapping_vacations = [
                vacation
                for vacation in member.vacations
                if vacation.start_date <= context.end_date and vacation.end_date >= context.start_date
            ]
            if overlapping_vacations:
                score -= 20
                workload_warnings.append("Vacation overlaps scheduled dates")

        if context.priority is not None and context.priority <= 2 and matched_skills:
            score += 5
            reasons.append("strong match for high-priority work")

        score = max(0.0, min(100.0, score))
        confidence = round(score / 100, 2)
        rationale_parts = []
        if matched_skills:
            rationale_parts.append(f"matches {', '.join(matched_skills[:3])}")
        if weakness_matches:
            rationale_parts.append(f"watch {', '.join(weakness_matches[:2])}")
        rationale_parts.extend(reasons[:2])
        if workload_warnings:
            rationale_parts.append(workload_warnings[0].lower())
        rationale = "; ".join(rationale_parts) or "No strong profile match; ranked by capacity and availability."

        return AssigneeRecommendationResponse(
            team_member_id=member.id,
            name=member.name,
            position=member.position,
            profile_id=member.profile_id,
            score=round(score, 1),
            confidence=confidence,
            matched_skills=self._dedupe(matched_skills),
            weakness_matches=self._dedupe(weakness_matches),
            workload_warnings=self._dedupe(workload_warnings),
            rationale=rationale,
        )

    def _skill_matches(self, skill: TeamMemberProfileSkill, context_text: str) -> bool:
        """Return true when a skill record overlaps the work context."""
        terms = [
            skill.skill_key,
            skill.skill_name,
            skill.category,
            skill.notes,
            *(skill.keywords_json or []),
        ]
        for term in terms:
            if not term:
                continue
            normalized = str(term).strip().lower()
            if not normalized:
                continue
            if normalized in context_text:
                return True
            for token in TOKEN_PATTERN.findall(normalized):
                if len(token) >= 3 and token in context_text:
                    return True
        return False

    def _context_text(self, context: RecommendationContext) -> str:
        """Build lowercase searchable text for a work item."""
        parts = [
            context.title,
            context.description,
            context.source,
            context.external_key,
            context.assignee_hint,
            context.project_name,
            " ".join(context.labels or []),
        ]
        return " ".join(str(part).lower() for part in parts if part)

    def _context_tokens(self, text: str) -> set[str]:
        """Return useful tokens from context text."""
        return {token for token in TOKEN_PATTERN.findall(text) if len(token) >= 3}

    def _normalize(self, value: str | None) -> str:
        """Normalize a name or hint for equality checks."""
        return " ".join((value or "").strip().lower().split())

    def _parse_task_tags(self, value: Optional[str]) -> list[str]:
        """Parse task tag JSON safely."""
        if not value:
            return []
        try:
            data = json.loads(value)
        except (TypeError, json.JSONDecodeError):
            return []
        if not isinstance(data, list):
            return []
        return self._dedupe([str(item).strip() for item in data if str(item).strip()])

    def _dedupe(self, values: Sequence[str]) -> list[str]:
        """Preserve first occurrence order while removing duplicates."""
        result: list[str] = []
        for value in values:
            if value and value not in result:
                result.append(value)
        return result

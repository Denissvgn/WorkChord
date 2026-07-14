"""GitHub status automation rule service."""
from collections import defaultdict
from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.agent import TaskEvent
from app.models.github import GitHubStatusAutomationRule
from app.models.task import TaskStatus
from app.schemas.github import (
    GitHubStatusAutomationResult,
    GitHubStatusAutomationRuleCreate,
    GitHubStatusAutomationRuleUpdate,
)
from app.services.language_service import (
    LanguageCode,
    backend_error_message,
    entity_not_found_message,
    invalid_status_transition_message,
    localized,
    resolve_runtime_ui_language,
)
from app.services.task_service import TaskService


DEFAULT_REASON_TEMPLATE = (
    "GitHub automation: {github_event_type} for {repo} PR #{pr_number}"
)


DEFAULT_GITHUB_STATUS_AUTOMATION_RULES = [
    GitHubStatusAutomationRuleCreate(
        name="PR opened starts work",
        description="When a linked pull request opens, move a planned task to active.",
        enabled=False,
        github_event_type="github_pr_opened",
        from_status="planned",
        target_status="active",
        reason_template=DEFAULT_REASON_TEMPLATE,
        sort_order=10,
    ),
    GitHubStatusAutomationRuleCreate(
        name="PR merged resolves work",
        description="When a linked pull request is merged, move an active task to resolved.",
        enabled=False,
        github_event_type="github_pr_merged",
        from_status="active",
        target_status="resolved",
        reason_template=DEFAULT_REASON_TEMPLATE,
        sort_order=20,
    ),
]

DEFAULT_GITHUB_STATUS_AUTOMATION_RULE_TUPLES = {
    (
        rule.name,
        rule.description,
        rule.github_event_type,
        rule.from_status,
        rule.target_status,
        rule.reason_template,
    )
    for rule in DEFAULT_GITHUB_STATUS_AUTOMATION_RULES
}


class _SafeFormatDict(defaultdict):
    """Leave unknown reason-template placeholders readable."""

    def __missing__(self, key):
        return "{" + key + "}"


class GitHubStatusAutomationService:
    """Manage and apply GitHub status automation rules."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.task_service = TaskService(db)

    async def list_rules(self) -> list[GitHubStatusAutomationRule]:
        """List all automation rules in execution order."""
        result = await self.db.execute(
            select(GitHubStatusAutomationRule)
            .order_by(GitHubStatusAutomationRule.sort_order, GitHubStatusAutomationRule.id)
        )
        return list(result.scalars().all())

    async def list_enabled_for_event(self, github_event_type: str) -> list[GitHubStatusAutomationRule]:
        """List enabled rules for one GitHub task event type."""
        result = await self.db.execute(
            select(GitHubStatusAutomationRule)
            .where(
                GitHubStatusAutomationRule.enabled.is_(True),
                GitHubStatusAutomationRule.github_event_type == github_event_type,
            )
            .order_by(GitHubStatusAutomationRule.sort_order, GitHubStatusAutomationRule.id)
        )
        return list(result.scalars().all())

    async def get_rule(self, rule_id: int) -> Optional[GitHubStatusAutomationRule]:
        """Fetch one automation rule by ID."""
        result = await self.db.execute(
            select(GitHubStatusAutomationRule).where(GitHubStatusAutomationRule.id == rule_id)
        )
        return result.scalar_one_or_none()

    async def create_rule(
        self,
        data: GitHubStatusAutomationRuleCreate,
    ) -> GitHubStatusAutomationRule:
        """Create an automation rule."""
        rule = GitHubStatusAutomationRule(**data.model_dump())
        self.db.add(rule)
        await self.db.commit()
        await self.db.refresh(rule)
        return rule

    async def update_rule(
        self,
        rule_id: int,
        data: GitHubStatusAutomationRuleUpdate,
    ) -> Optional[GitHubStatusAutomationRule]:
        """Update an automation rule."""
        rule = await self.get_rule(rule_id)
        if not rule:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(rule, field, value)

        await self.db.commit()
        await self.db.refresh(rule)
        return rule

    async def delete_rule(self, rule_id: int) -> bool:
        """Delete an automation rule."""
        rule = await self.get_rule(rule_id)
        if not rule:
            return False

        await self.db.delete(rule)
        await self.db.commit()
        return True

    async def seed_default_rules(self) -> None:
        """Seed disabled default automation rules without overwriting user edits."""
        existing_result = await self.db.execute(select(GitHubStatusAutomationRule.name))
        existing_names = set(existing_result.scalars().all())

        changed = False
        for default_rule in DEFAULT_GITHUB_STATUS_AUTOMATION_RULES:
            if default_rule.name in existing_names:
                continue
            self.db.add(GitHubStatusAutomationRule(**default_rule.model_dump()))
            changed = True

        if changed:
            await self.db.commit()

    async def _event_exists(self, idempotency_key: Optional[str]) -> bool:
        if not idempotency_key:
            return False
        result = await self.db.execute(
            select(TaskEvent.id).where(TaskEvent.idempotency_key == idempotency_key)
        )
        return result.scalar_one_or_none() is not None

    def _automation_key(self, delivery_id: Optional[str], rule_id: int) -> Optional[str]:
        if not delivery_id:
            return None
        return f"github-status-automation:{delivery_id}:{rule_id}"

    def _render_reason(
        self,
        rule: GitHubStatusAutomationRule,
        context: dict[str, Any],
        ui_language: LanguageCode = "en",
    ) -> str:
        values = _SafeFormatDict(str)
        values.update({
            "rule_id": rule.id,
            "rule_name": rule.name,
            "github_event_type": rule.github_event_type,
            "from_status": rule.from_status or "",
            "target_status": rule.target_status,
            **context,
        })
        template = rule.reason_template or DEFAULT_REASON_TEMPLATE
        default_tuple = (
            rule.name,
            rule.description,
            rule.github_event_type,
            rule.from_status,
            rule.target_status,
            rule.reason_template,
        )
        if default_tuple in DEFAULT_GITHUB_STATUS_AUTOMATION_RULE_TUPLES:
            template = localized(
                ui_language,
                DEFAULT_REASON_TEMPLATE,
                "GitHub automation: {github_event_type} для {repo} PR #{pr_number}",
            )
        return template.format_map(values)

    async def _record_failure_event(
        self,
        *,
        task_id: int,
        rule: GitHubStatusAutomationRule,
        from_status: str,
        reason: str,
        error: str,
        context: dict[str, Any],
        idempotency_key: Optional[str],
        ui_language: LanguageCode,
    ) -> None:
        payload = {
            "summary": localized(
                ui_language,
                f"GitHub status automation failed: {error}",
                f"GitHub status automation не выполнена: {error}",
            ),
            "rule_id": rule.id,
            "rule_name": rule.name,
            "github_event_type": rule.github_event_type,
            "from_status": from_status,
            "target_status": rule.target_status,
            "reason": reason,
            "error": error,
            "delivery_id": context.get("delivery_id"),
            "repo": context.get("repo"),
            "pr_number": context.get("pr_number"),
            "url": context.get("url"),
        }
        if context.get("url"):
            payload["artifact_links"] = [context["url"]]
            payload["artifact_label"] = f"PR #{context.get('pr_number')}"

        await self.task_service.record_task_event(
            task_id,
            "github_status_automation_failed",
            payload,
            actor_type="github",
            idempotency_key=idempotency_key,
        )

    async def apply_rules(
        self,
        *,
        task_id: int,
        github_event_type: str,
        delivery_id: Optional[str],
        context: dict[str, Any],
        commit: bool = True,
    ) -> list[GitHubStatusAutomationResult]:
        """Apply enabled rules for a matched GitHub webhook event."""
        rules = await self.list_enabled_for_event(github_event_type)
        if not rules:
            return []
        ui_language = await resolve_runtime_ui_language(self.db)

        task = await self.task_service.get_by_id(task_id)
        if not task:
            return [
                GitHubStatusAutomationResult(
                    rule_id=rule.id,
                    outcome="failed",
                    from_status="missing",
                    target_status=rule.target_status,
                    error=entity_not_found_message("task", task_id, ui_language),
                )
                for rule in rules
            ]

        results: list[GitHubStatusAutomationResult] = []
        needs_commit = False
        context = {**context, "delivery_id": delivery_id, "github_event_type": github_event_type}

        for rule in rules:
            current_status = task.status
            reason = self._render_reason(rule, context, ui_language)
            idempotency_key = self._automation_key(delivery_id, rule.id)

            if await self._event_exists(idempotency_key):
                results.append(GitHubStatusAutomationResult(
                    rule_id=rule.id,
                    outcome="skipped",
                    from_status=current_status,
                    target_status=rule.target_status,
                    reason=backend_error_message("Automation already processed for this delivery", ui_language),
                ))
                continue

            if rule.from_status and current_status != rule.from_status:
                results.append(GitHubStatusAutomationResult(
                    rule_id=rule.id,
                    outcome="skipped",
                    from_status=current_status,
                    target_status=rule.target_status,
                    reason=backend_error_message("Task status does not match rule from_status", ui_language),
                ))
                continue

            if current_status == rule.target_status:
                results.append(GitHubStatusAutomationResult(
                    rule_id=rule.id,
                    outcome="skipped",
                    from_status=current_status,
                    target_status=rule.target_status,
                    reason=backend_error_message("Task is already at target status", ui_language),
                ))
                continue

            try:
                changed_task, _, _ = await self.task_service.change_status(
                    task_id=task_id,
                    new_status=TaskStatus(rule.target_status),
                    reason=reason,
                    actor_type="github",
                    idempotency_key=idempotency_key,
                    commit=commit,
                )
            except ValueError as exc:
                error = str(exc)
                await self._record_failure_event(
                    task_id=task_id,
                    rule=rule,
                    from_status=current_status,
                    reason=reason,
                    error=error,
                    context=context,
                    idempotency_key=idempotency_key,
                    ui_language=ui_language,
                )
                needs_commit = True
                results.append(GitHubStatusAutomationResult(
                    rule_id=rule.id,
                    outcome="failed",
                    from_status=current_status,
                    target_status=rule.target_status,
                    reason=reason,
                    error=error,
                ))
                continue

            if not changed_task:
                error = (
                    invalid_status_transition_message(current_status, rule.target_status, ui_language)
                )
                await self._record_failure_event(
                    task_id=task_id,
                    rule=rule,
                    from_status=current_status,
                    reason=reason,
                    error=error,
                    context=context,
                    idempotency_key=idempotency_key,
                    ui_language=ui_language,
                )
                needs_commit = True
                results.append(GitHubStatusAutomationResult(
                    rule_id=rule.id,
                    outcome="failed",
                    from_status=current_status,
                    target_status=rule.target_status,
                    reason=reason,
                    error=error,
                ))
                continue

            task = changed_task
            results.append(GitHubStatusAutomationResult(
                rule_id=rule.id,
                outcome="applied",
                from_status=current_status,
                target_status=rule.target_status,
                reason=reason,
            ))

        if needs_commit and commit:
            await self.db.commit()
        elif needs_commit:
            await self.db.flush()

        return results

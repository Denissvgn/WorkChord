"""Deterministic task readiness evaluation for agent handoff."""
import re
from datetime import datetime
from typing import Any, Iterable, Optional, Sequence

from sqlalchemy.orm import attributes

from app.models.task import Task, TaskDependency, TaskStatus
from app.schemas.task import TaskAgentReadiness, TaskAgentReadinessCriterion
from app.services.agent_routing_policy import CAPABILITY_LABEL_SKILL_KEYS
from app.utils.time import as_utc, utc_now


DEFAULT_AGENT_CAPABILITY_SLUGS = frozenset(CAPABILITY_LABEL_SKILL_KEYS)
DESCRIPTION_SIGNAL_PATTERN = re.compile(
    r"\b(acceptance|criteria|checklist|scope|verify|verification|test|tests|expected|output|done)\b",
    re.IGNORECASE,
)
BULLET_PATTERN = re.compile(r"^\s*(?:[-*]|\d+[.)])\s+\S+")


def _dependency_task(dependency: TaskDependency) -> Optional[Task]:
    """Return loaded dependency target without triggering lazy IO."""
    state = attributes.instance_state(dependency)
    return state.dict.get("depends_on")


def _description_is_actionable(description: Optional[str]) -> tuple[bool, str]:
    """Return whether task description gives enough execution/verification context."""
    text = (description or "").strip()
    if len(text) < 80:
        return False, "Description needs at least 80 characters of task context."

    bullet_count = sum(
        1
        for line in text.splitlines()
        if BULLET_PATTERN.match(line)
    )
    if DESCRIPTION_SIGNAL_PATTERN.search(text) or bullet_count >= 2:
        return True, "Description includes actionable scope or verification detail."

    return (
        False,
        "Description needs acceptance, checklist, scope, verification, or at least two bullet points.",
    )


def _add_criterion(
    criteria: list[TaskAgentReadinessCriterion],
    blockers: list[str],
    *,
    key: str,
    label: str,
    passed: bool,
    reason: str,
) -> None:
    """Append one criterion and record failed reasons as blockers."""
    criteria.append(
        TaskAgentReadinessCriterion(
            key=key,
            label=label,
            passed=passed,
            reason=reason,
        )
    )
    if not passed:
        blockers.append(reason)


def evaluate_agent_readiness(
    task: Task,
    *,
    tags: Iterable[str],
    children: Sequence[Task],
    dependencies: Sequence[TaskDependency],
    now: Optional[datetime] = None,
    current_actor_id: Optional[int] = None,
    capability_slugs: Optional[set[str]] = None,
) -> TaskAgentReadiness:
    """Evaluate whether a task is ready for explicit agent execution."""
    now = now or utc_now()
    tag_set = {str(tag).strip() for tag in tags if str(tag).strip()}
    active_capability_slugs = (
        DEFAULT_AGENT_CAPABILITY_SLUGS
        if capability_slugs is None
        else capability_slugs
    )
    criteria: list[TaskAgentReadinessCriterion] = []
    blockers: list[str] = []
    warnings: list[str] = []

    planned_and_available = task.status == TaskStatus.PLANNED.value and not task.is_deferred
    status_reason = (
        "Task is planned and not deferred."
        if planned_and_available
        else "Task must be planned and not deferred."
    )
    _add_criterion(
        criteria,
        blockers,
        key="status",
        label="Planned and available",
        passed=planned_and_available,
        reason=status_reason,
    )

    is_leaf = len(children) == 0
    _add_criterion(
        criteria,
        blockers,
        key="leaf",
        label="Leaf task",
        passed=is_leaf,
        reason="Task has no subtasks." if is_leaf else "Composite tasks must be split before agent handoff.",
    )

    capability_matches = sorted(tag_set.intersection(active_capability_slugs))
    has_agent_labels = "agent" in tag_set and bool(capability_matches)
    if has_agent_labels:
        label_reason = f"Task has agent label and capability: {', '.join(capability_matches)}."
    elif "agent" not in tag_set:
        label_reason = "Task needs the agent label."
    else:
        label_reason = "Task needs at least one active capability label."
    _add_criterion(
        criteria,
        blockers,
        key="labels",
        label="Agent labels",
        passed=has_agent_labels,
        reason=label_reason,
    )

    has_schedule = task.start_date is not None and task.end_date is not None
    _add_criterion(
        criteria,
        blockers,
        key="schedule",
        label="Scheduled",
        passed=has_schedule,
        reason="Task has scheduled start and end dates." if has_schedule else "Task needs scheduled start and end dates.",
    )

    unresolved_dependencies: list[str] = []
    unknown_dependencies: list[int] = []
    for dependency in dependencies:
        dependency_task = _dependency_task(dependency)
        if dependency_task is None:
            unknown_dependencies.append(dependency.depends_on_id)
            continue
        if dependency_task.status not in {TaskStatus.RESOLVED.value, TaskStatus.CLOSED.value}:
            unresolved_dependencies.append(f"{dependency_task.title} ({dependency_task.status})")

    dependencies_ready = not unresolved_dependencies and not unknown_dependencies
    if unresolved_dependencies:
        dependency_reason = f"Unresolved dependencies: {', '.join(unresolved_dependencies)}."
    elif unknown_dependencies:
        dependency_reason = f"Dependency status unavailable for: {', '.join(str(dep_id) for dep_id in unknown_dependencies)}."
    elif dependencies:
        dependency_reason = "All dependencies are resolved or closed."
    else:
        dependency_reason = "Task has no dependencies."
    _add_criterion(
        criteria,
        blockers,
        key="dependencies",
        label="Dependencies complete",
        passed=dependencies_ready,
        reason=dependency_reason,
    )

    claim_expires_at = task.claim_expires_at
    active_claim = (
        task.claimed_by is not None
        and claim_expires_at is not None
        and as_utc(claim_expires_at) > as_utc(now)
        and (current_actor_id is None or task.claimed_by != current_actor_id)
    )
    claim_reason = "Task is not actively claimed."
    if active_claim and claim_expires_at is not None:
        claim_reason = f"Task is claimed until {claim_expires_at.isoformat()}."
    _add_criterion(
        criteria,
        blockers,
        key="claim",
        label="Unclaimed",
        passed=not active_claim,
        reason=claim_reason,
    )

    description_ready, description_reason = _description_is_actionable(task.description)
    _add_criterion(
        criteria,
        blockers,
        key="description",
        label="Actionable description",
        passed=description_ready,
        reason=description_reason,
    )

    effort_priority_ready = task.effort_days > 0 and 1 <= task.priority <= 10
    _add_criterion(
        criteria,
        blockers,
        key="effort_priority",
        label="Effort and priority",
        passed=effort_priority_ready,
        reason=(
            "Effort and priority are set."
            if effort_priority_ready
            else "Task needs positive effort and priority between 1 and 10."
        ),
    )

    failed_keys = [criterion.key for criterion in criteria if not criterion.passed]
    definition_keys = {"status", "leaf", "labels", "description", "effort_priority"}
    definition_ready = not any(key in definition_keys for key in failed_keys)
    start_ready = not blockers
    return TaskAgentReadiness(
        is_ready=start_ready,
        definition_ready=definition_ready,
        start_ready=start_ready,
        blocker_codes=failed_keys,
        blockers=blockers,
        warnings=warnings,
        criteria=criteria,
    )

"""Service for reusable work templates and built-in defaults."""
from typing import Any, Optional, Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.template import TemplateType, WorkTemplate
from app.schemas.template import WorkTemplateCreate, WorkTemplateUpdate


DEFAULT_TEMPLATE_DEFINITIONS: list[dict[str, Any]] = [
    {
        "seed_key": "task_feature",
        "name": "Feature",
        "description": "Default template for new product capability work.",
        "template_type": TemplateType.TASK.value,
        "default_title": "Implement feature",
        "default_description": "Define the user-facing behavior, implement the feature, and verify the outcome.",
        "default_priority": 4,
        "default_effort_days": 2.0,
        "default_labels": ["feature"],
        "default_checklist": [
            "Confirm acceptance criteria",
            "Implement the scoped behavior",
            "Add or update tests",
        ],
        "default_payload": {"is_optional": False, "is_deferred": False},
        "sort_order": 10,
    },
    {
        "seed_key": "task_bug",
        "name": "Bug",
        "description": "Default template for defect investigation and fixes.",
        "template_type": TemplateType.TASK.value,
        "default_title": "Fix bug",
        "default_description": "Reproduce the defect, identify the cause, implement the fix, and verify the regression path.",
        "default_priority": 2,
        "default_effort_days": 1.0,
        "default_labels": ["bug"],
        "default_checklist": ["Reproduce", "Fix", "Verify"],
        "default_payload": {"is_optional": False, "is_deferred": False},
        "sort_order": 20,
    },
    {
        "seed_key": "task_technical_task",
        "name": "Technical task",
        "description": "Default template for maintenance, refactoring, or internal engineering work.",
        "template_type": TemplateType.TASK.value,
        "default_title": "Complete technical task",
        "default_description": "Make the internal change while preserving existing behavior and tests.",
        "default_priority": 5,
        "default_effort_days": 1.0,
        "default_labels": ["chore"],
        "default_checklist": ["Confirm scope", "Make the change", "Run relevant checks"],
        "default_payload": {"is_optional": False, "is_deferred": False},
        "sort_order": 30,
    },
    {
        "seed_key": "task_risk_blocker",
        "name": "Risk / blocker",
        "description": "Default template for urgent work that blocks delivery or reduces major risk.",
        "template_type": TemplateType.TASK.value,
        "default_title": "Resolve blocker",
        "default_description": "Describe the blocked outcome, current impact, mitigation plan, and owner.",
        "default_priority": 1,
        "default_effort_days": 0.5,
        "default_labels": ["blocked", "risky"],
        "default_checklist": ["Identify impacted work", "Choose mitigation", "Confirm unblock criteria"],
        "default_payload": {"is_optional": False, "is_deferred": False},
        "sort_order": 40,
    },
    {
        "seed_key": "task_release_task",
        "name": "Release task",
        "description": "Default template for release preparation and verification.",
        "template_type": TemplateType.TASK.value,
        "default_title": "Prepare release task",
        "default_description": "Complete the release step and verify the release criteria before handoff.",
        "default_priority": 3,
        "default_effort_days": 0.5,
        "default_labels": ["release"],
        "default_checklist": ["Confirm release scope", "Complete release step", "Verify outcome"],
        "default_payload": {"is_optional": False, "is_deferred": False},
        "sort_order": 50,
    },
    {
        "seed_key": "task_agent_ready",
        "name": "Agent-ready task",
        "description": "Default template for scoped work that an agent can execute safely.",
        "template_type": TemplateType.TASK.value,
        "default_title": "Agent-ready task",
        "default_description": """## Goal
State the observable outcome and why it matters.

## Context and sources
Link the request, relevant files or records, prior decisions, and known evidence.

## Scope
List the changes or investigation that belong to this task.

## Out of scope
Name adjacent work the worker must report instead of absorbing.

## Constraints and risks
Record compatibility, security, migration, rollout, timing, and access limits.

## Expected deliverables
Name the files, records, artifacts, or decisions that must exist.

## Acceptance criteria
- State independently checkable completion criteria.

## Verification
List commands, checks, reviewer expectations, and required evidence.

## Dependencies and inputs
Name predecessor tasks, external inputs, and satisfied-state requirements.

## Handoff and escalation
Name the reviewer and conditions that require PM or human input.""",
        "default_priority": 4,
        "default_effort_days": 1.0,
        "default_labels": ["agent", "cap:code", "cap:test"],
        "default_checklist": [
            "Complete every required task-brief section",
            "Confirm definition-ready before assignment",
            "Record reviewer and verification evidence",
        ],
        "default_payload": {"source": "agent", "is_optional": False, "is_deferred": False},
        "sort_order": 60,
    },
    {
        "seed_key": "triage_customer_request",
        "name": "Customer request",
        "description": "Default template for customer-originated intake.",
        "template_type": TemplateType.TRIAGE.value,
        "default_title": "Customer request",
        "default_description": "Capture the customer need, source context, impact, and expected outcome.",
        "default_priority": 4,
        "default_effort_days": None,
        "default_labels": ["customer", "request"],
        "default_checklist": [
            "Link source conversation",
            "Identify affected customer",
            "Clarify expected outcome",
        ],
        "default_payload": {"source": "customer"},
        "sort_order": 10,
    },
]

LEGACY_AGENT_READY_DESCRIPTION = (
    "Provide exact scope, constraints, expected files or modules, and verification commands."
)


class TemplateService:
    """Service for template CRUD and built-in template seeding."""

    def __init__(self, db: AsyncSession):
        self.db = db

    def _enum_value(self, value):
        """Normalize Pydantic enum values before assigning to string columns."""
        return value.value if hasattr(value, "value") else value

    def _query(self) -> Select:
        """Build the base template query."""
        return select(WorkTemplate)

    async def seed_default_templates(self) -> list[WorkTemplate]:
        """Insert missing built-ins and safely upgrade unchanged legacy defaults."""
        result = await self.db.execute(
            select(WorkTemplate).where(WorkTemplate.seed_key.is_not(None))
        )
        existing_templates = {template.seed_key: template for template in result.scalars().all()}
        existing_seed_keys = set(existing_templates)
        templates = [
            WorkTemplate(**definition)
            for definition in DEFAULT_TEMPLATE_DEFINITIONS
            if definition["seed_key"] not in existing_seed_keys
        ]

        agent_definition = next(
            definition
            for definition in DEFAULT_TEMPLATE_DEFINITIONS
            if definition["seed_key"] == "task_agent_ready"
        )
        existing_agent_template = existing_templates.get("task_agent_ready")
        upgraded_existing = False
        if (
            existing_agent_template is not None
            and existing_agent_template.default_description == LEGACY_AGENT_READY_DESCRIPTION
        ):
            existing_agent_template.default_description = agent_definition["default_description"]
            existing_agent_template.default_checklist = agent_definition["default_checklist"]
            upgraded_existing = True

        if not templates and not upgraded_existing:
            return []

        self.db.add_all(templates)
        await self.db.commit()
        for template in templates:
            await self.db.refresh(template)
        return templates

    async def list_templates(
        self,
        template_type: Optional[TemplateType | str] = None,
        include_inactive: bool = False,
    ) -> Sequence[WorkTemplate]:
        """List templates ordered for create-form selection."""
        query = self._query()
        if template_type is not None:
            query = query.where(WorkTemplate.template_type == self._enum_value(template_type))
        if not include_inactive:
            query = query.where(WorkTemplate.is_active.is_(True))

        query = query.order_by(
            WorkTemplate.template_type,
            WorkTemplate.sort_order,
            WorkTemplate.name,
            WorkTemplate.id,
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_id(self, template_id: int) -> Optional[WorkTemplate]:
        """Get a template by ID."""
        result = await self.db.execute(
            self._query().where(WorkTemplate.id == template_id)
        )
        return result.scalar_one_or_none()

    async def create(self, data: WorkTemplateCreate) -> WorkTemplate:
        """Create a user-managed template."""
        template_data = data.model_dump()
        template_data["template_type"] = self._enum_value(template_data["template_type"])
        template = WorkTemplate(**template_data)
        self.db.add(template)
        await self.db.commit()
        await self.db.refresh(template)
        return template

    async def update(
        self,
        template_id: int,
        data: WorkTemplateUpdate,
    ) -> Optional[WorkTemplate]:
        """Apply a partial template update."""
        template = await self.get_by_id(template_id)
        if not template:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(template, field, self._enum_value(value))

        await self.db.commit()
        await self.db.refresh(template)
        return template

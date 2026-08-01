"""Code-owned capability catalog, profile presets, and explainable agent routes."""

from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.team_member import TeamMemberProfile, TeamMemberProfileSkill
from app.services.agent_routing_policy import (
    CAPABILITY_LABEL_SKILL_KEYS,
    ROUTING_SKILL_DEFINITIONS,
)


CAPABILITY_SKILLS: list[dict[str, Any]] = [
    {
        **definition,
        "keywords": list(definition["keywords"]),
    }
    for definition in ROUTING_SKILL_DEFINITIONS
]


PROFILE_PRESETS: list[dict[str, Any]] = [
    {
        "key": "pm-planning-agent",
        "display_name": "PM Planning Agent",
        "headline": "Intake, decomposition, and task-definition controller",
        "summary": "Clarifies requests, controls Triage, and produces definition-ready tasks.",
        "profile_kind": "agent",
        "assignment_modes": ["ownership"],
        "skills": ["planning-intake", "pm-control", "agent-routing", "agent-discovery-triage"],
    },
    {
        "key": "project-control-agent",
        "display_name": "Project Control Agent",
        "headline": "Project health, risk, reporting, and delivery control",
        "summary": "Supervises project outcomes, evidence, risks, and append-only updates.",
        "profile_kind": "agent",
        "assignment_modes": ["ownership", "verification"],
        "skills": ["pm-control", "delivery-forecast", "risk-control", "status-reporting"],
    },
    {
        "key": "iteration-control-agent",
        "display_name": "Iteration Control Agent",
        "headline": "Capacity, assignment, ordering, and schedule controller",
        "summary": "Plans iteration capacity and dispatches feasible, ordered work.",
        "profile_kind": "agent",
        "assignment_modes": ["ownership"],
        "skills": ["iteration-capacity", "schedule-control", "agent-routing", "pm-control"],
    },
    {
        "key": "backend-implementation-agent",
        "display_name": "Backend Implementation Agent",
        "headline": "Python/API/data implementation worker",
        "summary": "Executes assigned backend tasks and reports discoveries through Triage.",
        "profile_kind": "agent",
        "assignment_modes": ["execution"],
        "skills": ["backend-python", "mcp-agent-api", "agent-discovery-triage"],
    },
    {
        "key": "go-rust-agent-developer",
        "display_name": "Go And Rust Systems Agent",
        "headline": "Go/Rust service and systems implementation worker",
        "summary": "Executes assigned systems tasks with concurrency and safety evidence.",
        "profile_kind": "agent",
        "assignment_modes": ["execution"],
        "skills": ["backend-go", "backend-rust", "agent-discovery-triage"],
    },
    {
        "key": "frontend-implementation-agent",
        "display_name": "Frontend Implementation Agent",
        "headline": "React and TypeScript implementation worker",
        "summary": "Executes assigned frontend tasks with responsive and interaction checks.",
        "profile_kind": "agent",
        "assignment_modes": ["execution"],
        "skills": ["frontend-react", "quality-verification", "agent-discovery-triage"],
    },
    {
        "key": "qa-verification-agent",
        "display_name": "QA Verification Agent",
        "headline": "Independent acceptance and regression verifier",
        "summary": "Verifies resolved work independently and records pass/reject evidence.",
        "profile_kind": "agent",
        "assignment_modes": ["verification"],
        "skills": ["quality-verification", "data-integrity-review", "security-review"],
    },
    {
        "key": "docs-wiki-agent",
        "display_name": "Documentation Agent",
        "headline": "Documentation, wiki, and runbook worker",
        "summary": "Produces assigned documentation and maintains architecture/user guidance.",
        "profile_kind": "agent",
        "assignment_modes": ["execution"],
        "skills": ["documentation", "quality-verification", "agent-discovery-triage"],
    },
    {
        "key": "release-ops-agent",
        "display_name": "Release And Operations Agent",
        "headline": "Release, runtime, rollback, and operational worker",
        "summary": "Executes assigned release and operational work under explicit access controls.",
        "profile_kind": "agent",
        "assignment_modes": ["execution", "verification"],
        "skills": ["operations", "risk-control", "security-review"],
    },
    {
        "key": "ux-ui-design-agent",
        "display_name": "UX/UI Design Agent",
        "headline": "Artifact-first product design worker",
        "summary": "Creates inspectable design artifacts and implementation handoffs.",
        "profile_kind": "agent",
        "assignment_modes": ["execution", "design_handoff"],
        "skills": ["design", "quality-verification", "agent-discovery-triage"],
    },
    {
        "key": "delivery-forecast-agent",
        "display_name": "Delivery Forecast Agent",
        "headline": "Forecasting, target-date, and delivery-risk controller",
        "summary": "Reviews evidence and explains forecast movement without changing commitments autonomously.",
        "profile_kind": "agent",
        "assignment_modes": ["ownership"],
        "skills": ["delivery-forecast", "iteration-capacity", "schedule-control", "risk-control"],
    },
    {
        "key": "security-scope-agent",
        "display_name": "Security And Scope Agent",
        "headline": "Permission, secret, scope, and high-risk change reviewer",
        "summary": "Reviews high-risk work and escalates accountable approval decisions.",
        "profile_kind": "agent",
        "assignment_modes": ["verification"],
        "skills": ["security-review", "data-integrity-review", "mcp-agent-api"],
    },
]

for _preset in PROFILE_PRESETS:
    _preset["weaknesses"] = ["human-decision-authority"]


HUMAN_PROFILE_PRESETS: list[dict[str, Any]] = [
    {
        "key": "human-product-project-manager",
        "display_name": "Product / Project Manager",
        "headline": "Outcome, priority, team, and delivery owner",
        "summary": "Starter profile for portfolio, project, iteration, and stakeholder control.",
        "notes": "Starting point only; calibrate authority, availability, skills, and weaknesses for the person.",
        "profile_kind": "human",
        "assignment_modes": ["ownership", "verification"],
        "skills": ["pm-control", "planning-intake", "status-reporting", "risk-control"],
        "weaknesses": ["backend-rust"],
    },
    {
        "key": "human-engineering-lead",
        "display_name": "Engineering Lead",
        "headline": "Technical direction and implementation review lead",
        "summary": "Starter profile for decomposition, engineering oversight, and risk review.",
        "notes": "Starting point only; tune domain depth and hands-on capacity.",
        "profile_kind": "human",
        "assignment_modes": ["ownership", "execution", "verification"],
        "skills": ["backend-python", "data-integrity-review", "quality-verification", "risk-control"],
        "weaknesses": ["design"],
    },
    {
        "key": "human-backend-engineer",
        "display_name": "Backend Engineer",
        "headline": "Python API, service, and data implementation engineer",
        "summary": "Starter profile for backend implementation and verification work.",
        "notes": "Starting point only; add repository-specific runtime and domain skills.",
        "profile_kind": "human",
        "assignment_modes": ["execution", "verification"],
        "skills": ["backend-python", "mcp-agent-api", "data-integrity-review"],
        "weaknesses": ["design"],
    },
    {
        "key": "human-go-rust-systems-developer",
        "display_name": "Go / Rust Systems Developer",
        "headline": "Concurrent service, CLI, and systems implementation engineer",
        "summary": "Starter profile for Go/Rust and reliability-sensitive work.",
        "notes": "Starting point only; record actual language depth and production access separately.",
        "profile_kind": "human",
        "assignment_modes": ["execution", "verification"],
        "skills": ["backend-go", "backend-rust", "data-integrity-review"],
        "weaknesses": ["frontend-react"],
    },
    {
        "key": "human-frontend-engineer",
        "display_name": "Frontend Engineer",
        "headline": "React, TypeScript, responsive UI implementation engineer",
        "summary": "Starter profile for frontend implementation and interaction verification.",
        "notes": "Starting point only; pair with product design when direction is unresolved.",
        "profile_kind": "human",
        "assignment_modes": ["execution", "verification"],
        "skills": ["frontend-react", "quality-verification", "design"],
        "weaknesses": ["backend-rust"],
    },
    {
        "key": "human-ux-ui-designer",
        "display_name": "UX / UI Designer",
        "headline": "Research, interaction, visual design, and handoff owner",
        "summary": "Starter profile for artifact-first product design and critique.",
        "notes": "Starting point only; record research and design-system depth explicitly.",
        "profile_kind": "human",
        "assignment_modes": ["ownership", "design_handoff", "verification"],
        "skills": ["design", "quality-verification", "documentation"],
        "weaknesses": ["backend-python"],
    },
    {
        "key": "human-qa",
        "display_name": "QA Engineer",
        "headline": "Acceptance, regression, and evidence verifier",
        "summary": "Starter profile for independent verification and data-integrity review.",
        "notes": "Starting point only; add product-domain and automation depth.",
        "profile_kind": "human",
        "assignment_modes": ["verification"],
        "skills": ["quality-verification", "data-integrity-review", "security-review"],
        "weaknesses": ["pm-control"],
    },
    {
        "key": "human-technical-writer",
        "display_name": "Technical Writer",
        "headline": "User documentation, wiki, and runbook author",
        "summary": "Starter profile for documentation architecture and release guidance.",
        "notes": "Starting point only; add product and audience expertise.",
        "profile_kind": "human",
        "assignment_modes": ["execution", "verification"],
        "skills": ["documentation", "quality-verification", "status-reporting"],
        "weaknesses": ["operations"],
    },
    {
        "key": "human-devops-runtime-operator",
        "display_name": "DevOps / Runtime Operator",
        "headline": "Runtime, release, deployment, and rollback operator",
        "summary": "Starter profile for controlled operational and release work.",
        "notes": "Starting point only; production access remains an external authorization concern.",
        "profile_kind": "human",
        "assignment_modes": ["execution", "verification"],
        "skills": ["operations", "risk-control", "security-review"],
        "weaknesses": ["design"],
    },
    {
        "key": "human-security-reviewer",
        "display_name": "Security Reviewer",
        "headline": "Authorization, secrets, threat, and scope reviewer",
        "summary": "Starter profile for accountable review of security-sensitive work.",
        "notes": "Starting point only; formal approval authority remains organizational policy.",
        "profile_kind": "human",
        "assignment_modes": ["verification"],
        "skills": ["security-review", "data-integrity-review", "mcp-agent-api"],
        "weaknesses": ["status-reporting"],
    },
]


ALL_PROFILE_PRESETS = PROFILE_PRESETS + HUMAN_PROFILE_PRESETS


AGENT_ROUTES: list[dict[str, Any]] = [
    {
        "agent_key": preset["key"],
        "display_name": preset["display_name"],
        "required_skills": preset["skills"][:1],
        "supporting_skills": preset["skills"][1:],
        "primary_intents": preset["headline"].lower().split(", "),
        "avoid_rules": ["stakeholder decisions without explicit authority", "work outside the assigned task brief"],
        "default_handoff": "qa-verification-agent" if "verification" not in preset["assignment_modes"] else "project-control-agent",
    }
    for preset in PROFILE_PRESETS
]


class AgentProfileCatalogService:
    """Expose and apply stable capability/profile presets without granting permissions."""

    def __init__(self, db: AsyncSession):
        self.db = db

    def catalog(self) -> list[dict[str, Any]]:
        return CAPABILITY_SKILLS

    def capability_label_skill_map(self) -> dict[str, list[str]]:
        """Expose coarse readiness labels as explicit precise-skill choices."""

        return {
            label: sorted(skill_keys)
            for label, skill_keys in CAPABILITY_LABEL_SKILL_KEYS.items()
        }

    def presets(self) -> list[dict[str, Any]]:
        return ALL_PROFILE_PRESETS

    def routes(self) -> list[dict[str, Any]]:
        return AGENT_ROUTES

    async def apply_preset(
        self,
        preset_key: str,
        *,
        commit: bool = True,
    ) -> TeamMemberProfile:
        preset = next((item for item in ALL_PROFILE_PRESETS if item["key"] == preset_key), None)
        if preset is None:
            raise ValueError("Unknown agent profile preset")
        result = await self.db.execute(
            select(TeamMemberProfile)
            .options(selectinload(TeamMemberProfile.skills))
            .where(TeamMemberProfile.seed_key == preset_key)
            .with_for_update()
        )
        profile = result.scalar_one_or_none()
        if profile is None:
            candidate = TeamMemberProfile(
                seed_key=preset_key,
                display_name=preset["display_name"],
                headline=preset["headline"],
                summary=preset["summary"],
                notes=preset.get(
                    "notes", "Code-owned starter preset; customize after applying."
                ),
                automation_enabled=preset["profile_kind"] == "agent",
                profile_kind=preset["profile_kind"],
                assignment_modes=preset["assignment_modes"],
                skills=[],
            )
            try:
                async with self.db.begin_nested():
                    self.db.add(candidate)
                    await self.db.flush()
                profile = candidate
            except IntegrityError:
                result = await self.db.execute(
                    select(TeamMemberProfile)
                    .options(selectinload(TeamMemberProfile.skills))
                    .where(TeamMemberProfile.seed_key == preset_key)
                    .with_for_update()
                )
                profile = result.scalar_one_or_none()
                if profile is None:
                    raise
        existing = {skill.skill_key for skill in profile.skills}
        definitions = {item["skill_key"]: item for item in CAPABILITY_SKILLS}
        for skill_key in preset["skills"]:
            if skill_key in existing:
                continue
            definition = definitions[skill_key]
            self.db.add(
                TeamMemberProfileSkill(
                    profile_id=profile.id,
                    skill_key=definition["skill_key"],
                    skill_name=definition["skill_name"],
                    category=definition["category"],
                    level=4,
                    interest=4,
                    is_weakness=False,
                    keywords_json=definition["keywords"],
                    notes="Applied from the built-in agent profile preset.",
                )
            )
            existing.add(skill_key)
        for skill_key in preset.get("weaknesses", []):
            if skill_key in existing:
                continue
            definition = definitions[skill_key]
            self.db.add(
                TeamMemberProfileSkill(
                    profile_id=profile.id,
                    skill_key=definition["skill_key"],
                    skill_name=definition["skill_name"],
                    category=definition["category"],
                    level=2,
                    interest=2,
                    is_weakness=True,
                    keywords_json=definition["keywords"],
                    notes="Suggested review or handoff gap from the built-in preset.",
                )
            )
            existing.add(skill_key)
        try:
            if commit:
                await self.db.commit()
            else:
                await self.db.flush()
        except IntegrityError as exc:
            if not commit:
                raise
            await self.db.rollback()
            result = await self.db.execute(
                select(TeamMemberProfile)
                .options(selectinload(TeamMemberProfile.skills))
                .where(TeamMemberProfile.seed_key == preset_key)
            )
            profile = result.scalar_one_or_none()
            required_keys = set(preset["skills"]) | set(preset.get("weaknesses", []))
            if profile is None or not required_keys.issubset(
                {skill.skill_key for skill in profile.skills}
            ):
                raise ValueError(
                    "Concurrent preset application did not produce a complete profile"
                ) from exc
            return profile
        result = await self.db.execute(
            select(TeamMemberProfile)
            .options(selectinload(TeamMemberProfile.skills))
            .where(TeamMemberProfile.id == profile.id)
            .execution_options(populate_existing=True)
        )
        return result.scalar_one()

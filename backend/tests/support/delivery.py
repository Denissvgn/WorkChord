"""Deterministic shared delivery graph for database and HTTP scenarios."""

from dataclasses import dataclass
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.agent import AgentActor
from app.models.calendar import Calendar
from app.models.iteration import Iteration
from app.models.project import Project
from app.models.task import Task
from app.models.team_member import TeamMember, TeamMemberProfile
from app.models.user_session import UserSession
from app.services.agent_service import hash_api_key


@dataclass(frozen=True)
class DeliveryScenario:
    projects: tuple[int, int]
    iterations: tuple[int, int]
    profile: int
    capacity_rows: tuple[int, int]
    actors: tuple[int, int]
    actor_keys: tuple[str, str]
    sessions: tuple[int, int]
    tasks: dict[str, int]


async def seed_delivery_scenario(db: AsyncSession) -> DeliveryScenario:
    calendar = Calendar(name="Delivery calendar", year=2026, weekend_days=[5, 6])
    projects = [Project(name=name) for name in ("Orchard", "Harbor")]
    iterations = [
        Iteration(name="January delivery", start_date=date(2026, 1, 5),
                  end_date=date(2026, 1, 30), calendar=calendar, project=project)
        for project in projects
    ]
    profile = TeamMemberProfile(seed_key="shared-delivery-owner", display_name="Shared owner",
                                profile_kind="human", automation_enabled=False)
    members = [TeamMember(name="Shared owner", position="Engineer", profile=profile,
                          iteration=iteration) for iteration in iterations]
    actor_keys = ("delivery-scenario-worker-key", "delivery-scenario-verifier-key")
    actors = [
        AgentActor(name=f"delivery-{role}", display_name=role.title(), role=role,
                   api_key_hash=hash_api_key(key), scopes='["tasks:read"]')
        for role, key in zip(("worker", "verifier"), actor_keys, strict=True)
    ]
    sessions = [UserSession(public_id=f"delivery{i:04d}", ip_address=f"192.0.2.{i}",
                            session_token_hash=str(i) * 64, user_agent="delivery-scenario")
                for i in (1, 2)]
    db.add_all([calendar, *projects, *iterations, profile, *members, *actors, *sessions])
    await db.flush()
    tasks = {}
    for key, state, priority in (
        ("planned", "planned", 2), ("active", "active", 3),
        ("resolved", "resolved", 4), ("closed_urgent", "closed", 1),
        ("closed_low", "closed", 9), ("parent", "planned", 5),
    ):
        tasks[key] = Task(title=key.replace("_", " ").title(), status=state,
                          priority=priority, iteration=iterations[0], project=projects[0],
                          assignee=members[0] if key != "parent" else None,
                          effort_days=1, effort_hours=8,
                          start_date=date(2026, 1, 5), end_date=date(2026, 1, 6))
    db.add_all(tasks.values())
    await db.flush()
    tasks["nested"] = Task(title="Nested leaf", parent_id=tasks["parent"].id,
                           iteration=iterations[0], project=projects[0], assignee=members[0],
                           priority=2, effort_days=1, effort_hours=8)
    tasks["other_project"] = Task(title="Harbor leaf", iteration=iterations[1],
                                  project=projects[1], assignee=members[1],
                                  effort_days=1, effort_hours=8)
    db.add_all([tasks["nested"], tasks["other_project"]])
    await db.commit()
    return DeliveryScenario(tuple(p.id for p in projects), tuple(i.id for i in iterations),
                            profile.id, tuple(m.id for m in members), tuple(a.id for a in actors), actor_keys,
                            tuple(s.id for s in sessions), {key: task.id for key, task in tasks.items()})

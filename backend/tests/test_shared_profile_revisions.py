"""Profile skill writes retain initial complete planning observations."""

import pytest
from sqlalchemy import func, select

from app.commands import AggregateVersionConflict, PlanningConflict
from app.config import get_settings
from app.models.team_member import TeamMemberProfileSkill
from app.schemas.team import TeamMemberProfileSkillCreate
from app.services.planning_input_context import observe_planning_input
from app.services.team_service import TeamService
from tests.test_delivery_scenarios import delivery_store


async def test_skill_create_uses_initial_profile_map_and_exposes_current_skill_resource(delivery_store, monkeypatch):
    factory, scenario, _ = delivery_store
    monkeypatch.setenv('STRICT_MUTATION_VERSIONS', 'true'); get_settings.cache_clear()
    try:
        async with factory() as db:
            observed = await observe_planning_input(db, 'profile', scenario.profile)
            assert set(observed['expected_revisions']) == set(scenario.iterations)
            created = await TeamService(db).add_profile_skill(scenario.profile, TeamMemberProfileSkillCreate(
                skill_key='bounded-review', skill_name='Bounded review', expected_revisions=observed['expected_revisions']))
            assert created is not None
            current = await observe_planning_input(db, 'profile', scenario.profile)
            assert any(row['id'] == created.id for row in current['resource']['skills'])
            with pytest.raises(AggregateVersionConflict):
                await TeamService(db).add_profile_skill(scenario.profile, TeamMemberProfileSkillCreate(
                    skill_key='stale-review', skill_name='Stale review', expected_revisions=observed['expected_revisions']))
        async with factory() as db:
            assert await db.scalar(select(func.count()).select_from(TeamMemberProfileSkill).where(
                TeamMemberProfileSkill.profile_id == scenario.profile, TeamMemberProfileSkill.skill_key == 'stale-review')) == 0
    finally:
        get_settings.cache_clear()


async def test_skill_context_does_not_silently_truncate_large_profiles(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        db.add_all([TeamMemberProfileSkill(profile_id=scenario.profile, skill_key=f'capability-{index}', skill_name=f'Capability {index}') for index in range(501)])
        await db.commit()
        with pytest.raises(PlanningConflict, match='limit'):
            await observe_planning_input(db, 'profile', scenario.profile)

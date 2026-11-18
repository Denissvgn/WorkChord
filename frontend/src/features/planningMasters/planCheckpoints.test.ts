import { describe, expect, it } from 'vitest';
import type { IterationPlanningReadinessSummary } from '../../types/iteration';
import { planCheckpointSections } from './planCheckpoints';
import { PLANNING_STEP_IDS } from './planningReturn';

const summary = (ids: readonly string[]): IterationPlanningReadinessSummary => ({
    iteration_id: 1,
    team_member_count: 1,
    team_capacity_hours: 8,
    team_members_no_capacity: 0,
    task_count: 1,
    tasks_without_assignee: 0,
    tasks_without_effort: 0,
    has_schedule: false,
    risk_count: 0,
    checkpoints: ids.map(id => ({ id, state: 'done', reason_codes: [], counts: {} })),
} as unknown as IterationPlanningReadinessSummary);

describe('plan checkpoint sections', () => {
    it('invents no checkpoint states without an iteration', () => {
        expect(planCheckpointSections(undefined, { hasIteration: false })).toBeNull();
        expect(planCheckpointSections(summary(PLANNING_STEP_IDS), { hasIteration: false })).toBeNull();
    });

    it('invents no checkpoint states without a response or from a partial one', () => {
        expect(planCheckpointSections(undefined, { hasIteration: true })).toBeNull();
        expect(planCheckpointSections(summary(['iteration']), { hasIteration: true })).toBeNull();
    });

    it('returns the six states exactly as the server reported them', () => {
        const sections = planCheckpointSections(summary(PLANNING_STEP_IDS), { hasIteration: true });
        expect(sections?.map(section => section.state)).toEqual(Array(6).fill('done'));
    });
});

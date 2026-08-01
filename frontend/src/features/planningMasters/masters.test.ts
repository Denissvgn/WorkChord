import { describe, expect, it } from 'vitest';
import { deriveStatus, EMPTY_READINESS, nextStep } from './masters';
import type { PlanReadiness } from './masters';

const readinessFixture = (
    overrides: Partial<PlanReadiness> = {},
): PlanReadiness => ({
    ...EMPTY_READINESS,
    iterationCount: 1,
    hasCurrentIteration: true,
    currentIterationName: 'August plan',
    currentIterationStart: '2026-08-03',
    currentIterationEnd: '2026-08-14',
    currentIterationDays: 10,
    teamMemberCount: 1,
    teamCapacity: 64,
    taskCount: 1,
    ...overrides,
});

describe('planning master readiness status', () => {
    it.each([
        {
            name: 'the team is empty',
            overrides: { teamMemberCount: 0, teamCapacity: 0 },
        },
        {
            name: 'work is empty',
            overrides: { taskCount: 0 },
        },
        {
            name: 'the team has no usable capacity',
            overrides: { teamMembersNoCap: 1 },
        },
        {
            name: 'work still has scheduling blockers',
            overrides: { tasksWithoutAssignee: 1 },
        },
    ])('blocks schedule creation when $name', ({ overrides }) => {
        const status = deriveStatus(readinessFixture(overrides));

        expect(status.schedule.state).toBe('blocked');
        expect(status.review.state).toBe('blocked');
    });

    it('distinguishes a buildable plan from one with a saved schedule', () => {
        const buildable = deriveStatus(readinessFixture());
        const scheduled = deriveStatus(readinessFixture({ hasGanttSchedule: true }));

        expect(buildable.schedule.state).toBe('todo');
        expect(scheduled.schedule.state).toBe('done');
        expect(scheduled.review.state).toBe('done');
    });

    it('returns the first incomplete step even when it is blocked', () => {
        const status = deriveStatus(readinessFixture({
            teamMemberCount: 0,
            teamCapacity: 0,
            taskCount: 0,
        }));

        expect(nextStep(status)).toBe('team');
    });
});

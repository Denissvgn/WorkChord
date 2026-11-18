import { describe, expect, it } from 'vitest';
import {
    derivePlanningRecovery,
} from './masters';
import type { PlanReadiness } from './masters';

const readinessFixture = (
    overrides: Partial<PlanReadiness> = {},
): PlanReadiness => ({
    iterationCount: 1,
    hasCurrentIteration: true,
    currentIterationName: 'August plan',
    currentIterationStart: '2026-08-03',
    currentIterationEnd: '2026-08-14',
    currentIterationDays: 10,
    teamMemberCount: 1,
    teamCapacity: 64,
    teamMembersNoCap: 0,
    taskCount: 1,
    tasksWithoutAssignee: 0,
    tasksWithoutEffort: 0,
    hasGanttSchedule: false,
    ganttLastBuilt: '',
    riskCount: 0,
    inboxCount: 0,
    ...overrides,
});

describe('planning recovery', () => {
    it('ranks task recovery by affected count with an assignee-first tie-break', () => {
        expect(derivePlanningRecovery('schedule', readinessFixture({
            tasksWithoutAssignee: 2,
            tasksWithoutEffort: 4,
        }))).toMatchObject({
            kind: 'repair-effort',
            ownerStep: 'blockers',
            count: 4,
            planningIssue: 'missing-effort',
        });

        expect(derivePlanningRecovery('review', readinessFixture({
            tasksWithoutAssignee: 3,
            tasksWithoutEffort: 3,
        }))).toMatchObject({
            kind: 'repair-assignee',
            ownerStep: 'blockers',
            count: 3,
            planningIssue: 'unassigned',
        });
    });

    it('keeps stage precedence ahead of task exception severity', () => {
        expect(derivePlanningRecovery('schedule', readinessFixture({
            teamMemberCount: 0,
            teamCapacity: 0,
            tasksWithoutAssignee: 20,
        }))).toMatchObject({
            kind: 'add-team',
            ownerStep: 'team',
        });
    });
});

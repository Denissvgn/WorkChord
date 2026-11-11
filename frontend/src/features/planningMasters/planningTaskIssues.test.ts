import { describe, expect, it } from 'vitest';
import type { Task } from '../../types/task';
import {
    hasPositivePlanningEffort,
    isAgentWorkingWithoutCapacity,
    isPlanningLeafTask,
    parsePlanningIterationId,
    parsePlanningTaskIssue,
    planningIssueTasksHref,
    taskMatchesPlanningIssue,
} from './planningTaskIssues';

const taskFixture = (overrides: Partial<Task> = {}): Task => ({
    id: 1,
    iteration_id: 7,
    title: 'Planning task',
    priority: 1,
    effort_days: 1,
    effort_hours: 8,
    assignee: { id: 3, name: 'Alex' },
    status: 'planned',
    is_overdue: false,
    is_delayed: false,
    is_composite: false,
    is_optional: false,
    is_deferred: false,
    tags: [],
    sort_order: 0,
    external_links: [],
    request_count: 0,
    agent_readiness: {
        is_ready: true,
        blockers: [],
        warnings: [],
        criteria: [],
    },
    version: 1,
    children: [],
    dependencies: [],
    ...overrides,
});

describe('planning task issue contract', () => {
    it('accepts only exact public issue and positive iteration values', () => {
        expect(parsePlanningTaskIssue('unassigned')).toBe('unassigned');
        expect(parsePlanningTaskIssue('missing-effort')).toBe('missing-effort');
        expect(parsePlanningTaskIssue('any')).toBe('any');
        expect(parsePlanningTaskIssue('Unassigned')).toBeNull();
        expect(parsePlanningTaskIssue('')).toBeNull();
        expect(parsePlanningIterationId('7')).toBe(7);
        expect(parsePlanningIterationId('0')).toBeNull();
        expect(parsePlanningIterationId('7.5')).toBeNull();
    });

    it('uses the same leaf and effort rules as Planning readiness', () => {
        expect(isPlanningLeafTask(taskFixture())).toBe(true);
        expect(isPlanningLeafTask(taskFixture({ is_deferred: true }))).toBe(false);
        expect(isPlanningLeafTask(taskFixture({ is_composite: true }))).toBe(false);
        expect(isPlanningLeafTask(taskFixture({
            children: [taskFixture({ id: 2 })],
        }))).toBe(false);

        expect(hasPositivePlanningEffort(0.25)).toBe(true);
        expect(hasPositivePlanningEffort(0)).toBe(false);
        expect(hasPositivePlanningEffort(-1)).toBe(false);
        expect(hasPositivePlanningEffort(Number.NaN)).toBe(false);
        expect(hasPositivePlanningEffort(Number.POSITIVE_INFINITY)).toBe(false);
    });

    it('matches each exact issue and ORs overlapping blockers once for any', () => {
        const overlapping = taskFixture({
            assignee: null,
            effort_days: 0,
        });
        expect(taskMatchesPlanningIssue(overlapping, 'unassigned')).toBe(true);
        expect(taskMatchesPlanningIssue(overlapping, 'missing-effort')).toBe(true);
        expect(taskMatchesPlanningIssue(overlapping, 'any')).toBe(true);
        expect(taskMatchesPlanningIssue(taskFixture(), 'any')).toBe(false);
        expect(taskMatchesPlanningIssue(
            taskFixture({ assignee: null, is_deferred: true }),
            'unassigned',
        )).toBe(false);
    });

    it('builds a durable exact Tasks URL', () => {
        expect(planningIssueTasksHref({
            issue: 'missing-effort',
            iterationId: 7,
            returnStepId: 'schedule',
        })).toBe(
            '/tasks?planningIssue=missing-effort&iterationId=7&fromPlanStep=schedule',
        );
    });
});

describe('one "needs an assignee" rule', () => {
    const base = { id: 1, title: 'Task', status: 'planned', assignee: null, effort_days: 2, children: [], is_composite: false, is_deferred: false } as unknown as Task;

    it('counts only planned leaves without an assignee', () => {
        expect(taskMatchesPlanningIssue(base, 'unassigned')).toBe(true);
        for (const status of ['active', 'resolved', 'closed'] as const) {
            expect(taskMatchesPlanningIssue({ ...base, status }, 'unassigned')).toBe(false);
        }
        expect(taskMatchesPlanningIssue({ ...base, is_deferred: true }, 'unassigned')).toBe(false);
    });

    it('reports agent-held work separately instead of as unassigned', () => {
        const agentHeld = { ...base, agent_working: true };
        expect(taskMatchesPlanningIssue(agentHeld, 'unassigned')).toBe(false);
        expect(isAgentWorkingWithoutCapacity(agentHeld)).toBe(true);
        expect(isAgentWorkingWithoutCapacity({ ...agentHeld, assignee: { id: 2, name: 'Sam' } })).toBe(false);
    });
});

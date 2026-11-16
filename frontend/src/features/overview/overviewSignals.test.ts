import { describe, expect, it } from 'vitest';
import type { Iteration } from '../../types/iteration';
import type { Task } from '../../types/task';
import {
    iterationsInView,
    listTasks,
    pickAttention,
    pipelineTasksInScope,
    selectWorkNow,
    taskListHref,
    workingDaysLeft,
} from './overviewSignals';
import { filtersFromSearchParams } from '../savedViews/taskViewParams';

const task = (id: number, overrides: Partial<Task> = {}) => ({
    id,
    title: `Task ${id}`,
    status: 'planned',
    priority: 3,
    assignee: { id: 1, name: 'Ada' },
    is_overdue: false,
    is_delayed: false,
    is_composite: false,
    is_optional: false,
    is_deferred: false,
    effort_days: 1,
    start_date: null,
    end_date: null,
    iteration_id: 1,
    project_id: 1,
    children: [],
    tags: [],
    dependencies: [],
    agent_readiness: { is_ready: false, blockers: [], warnings: [], criteria: [] },
    ...overrides,
} as unknown as Task);

const iteration = (id: number, project_id: number, start_date: string, end_date: string, working_days = 10) => ({
    id, name: `Iteration ${id}`, calendar_id: 1, project_id, start_date, end_date, working_days,
} as Iteration);

describe('Overview signals', () => {
    it('orders Work now by delivery risk, then due date and priority, and leaves out finished and deferred work', () => {
        const roots = [
            task(1, { status: 'active' }),
            task(2, { status: 'closed', is_overdue: true }),
            task(3, { blocked_reason: 'Waiting for access' }),
            task(4, { is_delayed: true, end_date: '2026-11-20' }),
            task(5, { is_overdue: true }),
            task(6, { is_delayed: true, end_date: '2026-11-18' }),
            task(7, { is_outside_constraints: true }),
            task(8, { is_deferred: true, is_overdue: true }),
            task(9),
        ];
        const { tasks, openCount } = selectWorkNow(roots, 5);
        expect(tasks.map(item => item.id)).toEqual([5, 6, 4, 7, 3]);
        expect(openCount).toBe(7);
    });

    it('counts the leaves the Tasks list shows, not the parents that hold them', () => {
        const parent = task(10, {
            status: 'closed',
            is_composite: true,
            children: [task(11, { status: 'closed' }), task(12, { status: 'active' })],
        });
        const roots = [parent, task(13, { status: 'closed' })];
        expect(listTasks(roots, 'done').map(item => item.id)).toEqual([11, 13]);
        expect(listTasks(roots, 'total')).toHaveLength(3);
    });

    it('writes each list as Tasks filters that read back to the same conditions', () => {
        const href = taskListHref('atRisk');
        expect(href).toBe('/tasks?planningIssue=at-risk');
        expect(filtersFromSearchParams(new URL(href, 'http://x').searchParams).planningIssue).toBe('at-risk');
        expect(filtersFromSearchParams(new URL(taskListHref('done'), 'http://x').searchParams).status).toBe('closed');
        expect(filtersFromSearchParams(new URL(taskListHref('blocked'), 'http://x').searchParams).isBlocked).toBe(true);
        expect(taskListHref('total')).toBe('/tasks');
        expect(taskListHref('toAssign', { mode: 'bulk' })).toBe('/tasks?planningIssue=unassigned&mode=bulk');
    });

    it('picks the most severe attention item: blocked, then reviews, then tasks to assign, then the plan', () => {
        const a = iteration(1, 1, '2026-11-01', '2026-11-30');
        const b = iteration(2, 2, '2026-11-02', '2026-11-30');
        expect(pickAttention([
            { kind: 'plan', count: 3, iteration: a },
            { kind: 'to-assign', count: 9, iteration: a },
            { kind: 'reviews', count: 1, iteration: b },
            { kind: 'blocked', count: 0, iteration: a },
        ])).toMatchObject({ kind: 'reviews', iteration: b });
        expect(pickAttention([
            { kind: 'blocked', count: 1, iteration: a },
            { kind: 'blocked', count: 2, iteration: b },
        ])).toMatchObject({ kind: 'blocked', count: 2, iteration: b });
        expect(pickAttention([{ kind: 'to-assign', count: 0, iteration: a }])).toBeNull();
    });

    it('counts the iteration in scope, or every open iteration with All projects', () => {
        const iterations = [
            iteration(11, 1, '2026-10-01', '2026-10-31'),
            iteration(12, 1, '2026-11-01', '2026-11-30'),
            iteration(21, 2, '2026-11-10', '2026-12-10'),
            iteration(22, 2, '2027-01-01', '2027-01-31'),
        ];
        const today = '2026-11-16';
        expect(iterationsInView(iterations, 1, 11, today).map(item => item.id)).toEqual([11]);
        expect(iterationsInView(iterations, 'all', 11, today).map(item => item.id)).toEqual([12, 21]);
        expect(iterationsInView(iterations, 'all', 'backlog', today).map(item => item.id)).toEqual([12, 21]);
        expect(iterationsInView(iterations, 1, 'backlog', today)).toEqual([]);
    });

    it('counts working days left after today', () => {
        const item = iteration(1, 1, '2026-11-01', '2026-11-10', 10);
        expect(workingDaysLeft(item, '2026-10-20')).toBe(10);
        expect(workingDaysLeft(item, '2026-11-01')).toBe(9);
        expect(workingDaysLeft(item, '2026-11-10')).toBe(0);
        expect(workingDaysLeft(item, '2026-12-01')).toBe(0);
    });

    it('keeps pipeline tasks of the scope by the pipeline view rule', () => {
        const tasks = [task(1, { project_id: 1, iteration_id: 12 }), task(2, { project_id: 2, iteration_id: 21 }), task(3, { project_id: 1, iteration_id: null })];
        expect(pipelineTasksInScope(tasks, 1, 12).map(item => item.id)).toEqual([1]);
        expect(pipelineTasksInScope(tasks, 'all', 21).map(item => item.id)).toEqual([2]);
        expect(pipelineTasksInScope(tasks, 1, 'backlog').map(item => item.id)).toEqual([3]);
    });
});

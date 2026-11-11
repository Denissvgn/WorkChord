import { describe, expect, it } from 'vitest';
import type { Task } from '../types/task';
import { defaultFilters } from './taskFilterDefaults';
import {
    filterTaskBySearch,
    filterTaskWithChildren,
    taskMatchesFilters,
} from './taskFilters';

const taskFixture = (overrides: Partial<Task> = {}): Task => ({
    id: 1,
    iteration_id: 1,
    title: 'Task',
    priority: 1,
    effort_days: 1,
    effort_hours: 8,
    assignee: { id: 2, name: 'Sam' },
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

describe('Planning readiness task filters', () => {
    it('retains ancestor context while pruning nonmatching siblings', () => {
        const matchingChild = taskFixture({
            id: 2,
            title: 'Needs owner',
            assignee: null,
        });
        const parent = taskFixture({
            id: 10,
            title: 'Parent',
            is_composite: true,
            children: [
                matchingChild,
                taskFixture({ id: 3, title: 'Ready sibling' }),
            ],
        });

        const result = filterTaskWithChildren(parent, {
            ...defaultFilters,
            planningIssue: 'unassigned',
        });

        expect(result?.id).toBe(parent.id);
        expect(result?.children.map(task => task.id)).toEqual([matchingChild.id]);
    });

    it('excludes deferred, composite, and parent rows from exact issue matches', () => {
        const filters = {
            ...defaultFilters,
            planningIssue: 'unassigned' as const,
        };
        expect(taskMatchesFilters(taskFixture({ assignee: null }), filters)).toBe(true);
        expect(taskMatchesFilters(taskFixture({
            assignee: null,
            is_deferred: true,
        }), filters)).toBe(false);
        expect(taskMatchesFilters(taskFixture({
            assignee: null,
            is_composite: true,
        }), filters)).toBe(false);
        expect(taskMatchesFilters(taskFixture({
            assignee: null,
            children: [taskFixture({ id: 2 })],
        }), filters)).toBe(false);
    });

    it.each([0, -1, Number.NaN, Number.POSITIVE_INFINITY])(
        'treats %s as missing effort',
        effortDays => {
            expect(taskMatchesFilters(taskFixture({ effort_days: effortDays }), {
                ...defaultFilters,
                planningIssue: 'missing-effort',
            })).toBe(true);
        },
    );
});

describe('Blocked task filter', () => {
    const blocked = taskFixture({ id: 4, blocked_reason: 'Database credentials are missing' });
    const clear = taskFixture({ id: 5, blocked_reason: null });
    const blank = taskFixture({ id: 6, blocked_reason: '   ' });

    it('matches only tasks with a reported blocker', () => {
        const filters = { ...defaultFilters, isBlocked: true };
        expect([blocked, clear, blank].filter(task => taskMatchesFilters(task, filters)).map(task => task.id)).toEqual([4]);
    });

    it('matches tasks without a blocker when set to not blocked', () => {
        const filters = { ...defaultFilters, isBlocked: false };
        expect([blocked, clear, blank].filter(task => taskMatchesFilters(task, filters)).map(task => task.id)).toEqual([5, 6]);
    });
});

describe('search narrows the task list', () => {
    const child = taskFixture({ id: 21, title: 'Write migration notes' });
    const parent = taskFixture({ id: 20, title: 'Release', is_composite: true, children: [child, taskFixture({ id: 22, title: 'Tag build' })] });

    it('keeps a parent for a matching child and drops non-matching children', () => {
        expect(filterTaskBySearch(parent, 'migration')?.children.map(task => task.id)).toEqual([21]);
    });

    it('matches by #ID and returns nothing when nothing matches', () => {
        expect(filterTaskBySearch(parent, '#22')?.children.map(task => task.id)).toEqual([22]);
        expect(filterTaskBySearch(parent, 'payroll')).toBeNull();
    });
});

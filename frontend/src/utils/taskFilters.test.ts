import { describe, expect, it } from 'vitest';
import type { Task } from '../types/task';
import { defaultFilters } from './taskFilterDefaults';
import {
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

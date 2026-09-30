import { expect, it } from 'vitest';
import type { Task, TaskStatus } from '../types/task';
import { selectVisibleWork } from './visibleWork';
import { defaultFilters } from './taskFilterDefaults';

const leaf = (id: number, status: TaskStatus = 'planned'): Task => ({ id, title: `Work ${id}`, status, iteration_id: 1, is_composite: false,
    children: [], is_deferred: false, is_optional: false, tags: [], dependencies: [], effort_days: 1, effort_hours: 8, priority: 1, is_overdue: false, is_delayed: false, sort_order: 0,
    version: 1, external_links: [], request_count: 0, agent_readiness: { is_ready: false, blockers: [], warnings: [], criteria: [] } });

it('uses the same matching leaf IDs with ancestor context and no unrelated siblings', () => {
    const parent = { ...leaf(1), title: 'Summary', is_composite: true, children: [leaf(2), leaf(3, 'resolved')] };
    const result = selectVisibleWork([parent], { ...defaultFilters, status: 'resolved' });
    expect(result.tree[0].children.map(task => task.id)).toEqual([3]);
    expect(result.leaves.map(task => task.id)).toEqual([3]);
    expect(result.leaves[0].parent_context).toEqual(['Summary']);
});

it('does not turn an empty summary into a deliverable and retains inherited work facets', () => {
    const result = selectVisibleWork([{ ...leaf(1), is_composite: true },
        { ...leaf(2), is_optional: true, is_deferred: true, children: [leaf(3)] }]);
    expect(result.leaves).toHaveLength(1);
    expect(result.leaves[0]).toMatchObject({ id: 3, is_deferred: true, is_optional: true });
});

it('keeps inherited deferred children out of active planning issue filters', () => {
    const parent = { ...leaf(1), is_deferred: true, is_composite: true, children: [leaf(2)] };
    expect(selectVisibleWork([parent], { ...defaultFilters, planningIssue: 'unassigned' }).leaves).toEqual([]);
});

import { describe, expect, it } from 'vitest';
import type { Task } from '../../types/task';
import {
    rankAttentionItems,
    rankAttentionTaskCandidates,
    type RankableAttention,
} from './attentionRanking';

const signal = (
    id: string,
    overrides: Partial<RankableAttention> = {},
): RankableAttention => ({
    id,
    kind: 'intake',
    severity: 'warning',
    urgency: 1,
    magnitude: 1,
    ...overrides,
});

const task = (
    id: number,
    overrides: Partial<Task> = {},
): Task => ({
    id,
    title: `Task ${id}`,
    status: 'planned',
    priority: 3,
    sort_order: 0,
    effort_days: 1,
    effort_hours: 8,
    is_overdue: false,
    is_delayed: false,
    is_composite: false,
    is_optional: false,
    is_deferred: false,
    tags: [],
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
    iteration_id: 1,
    ...overrides,
});

describe('rankAttentionItems', () => {
    it('ranks severity before urgency or source construction order', () => {
        const items = [
            signal('advisory-now', {
                kind: 'unassigned',
                severity: 'advisory',
                urgency: 4,
            }),
            signal('warning-soon', {
                kind: 'intake',
                severity: 'warning',
                urgency: 1,
            }),
            signal('critical-later', {
                kind: 'pace',
                severity: 'critical',
                urgency: 2,
            }),
        ];

        expect(rankAttentionItems(items).map(item => item.id)).toEqual([
            'critical-later',
            'warning-soon',
            'advisory-now',
        ]);
    });

    it('ranks urgency within a severity before deterministic signal-kind ties', () => {
        const items = [
            signal('stale-update', { kind: 'project-update', urgency: 1 }),
            signal('pace', { kind: 'pace', urgency: 2 }),
            signal('project-risk', { kind: 'project-risk', urgency: 3 }),
        ];

        expect(rankAttentionItems(items).map(item => item.id)).toEqual([
            'project-risk',
            'pace',
            'stale-update',
        ]);
    });

    it('produces the same total order for shuffled equal-rank inputs', () => {
        const items = [
            signal('intake-b', { kind: 'intake', magnitude: 2 }),
            signal('update', { kind: 'project-update', magnitude: 9 }),
            signal('intake-a', { kind: 'intake', magnitude: 2 }),
            signal('intake-c', { kind: 'intake', magnitude: 4 }),
        ];
        const expected = ['update', 'intake-c', 'intake-a', 'intake-b'];

        expect(rankAttentionItems(items).map(item => item.id)).toEqual(expected);
        expect(rankAttentionItems([...items].reverse()).map(item => item.id))
            .toEqual(expected);
        expect(rankAttentionItems([items[2], items[0], items[3], items[1]])
            .map(item => item.id))
            .toEqual(expected);
    });
});

describe('rankAttentionTaskCandidates', () => {
    it('chooses a representative task independently of API order', () => {
        const tasks = [
            task(9, { is_overdue: true, status: 'planned', end_date: '2026-08-01' }),
            task(7, { is_overdue: true, status: 'active', end_date: '2026-08-02' }),
            task(8, { is_overdue: true, status: 'active', end_date: '2026-08-01' }),
        ];

        expect(rankAttentionTaskCandidates(tasks).map(item => item.id))
            .toEqual([8, 7, 9]);
        expect(rankAttentionTaskCandidates([...tasks].reverse()).map(item => item.id))
            .toEqual([8, 7, 9]);
    });

    it('uses priority, board order, and id as explicit final task ties', () => {
        const tasks = [
            task(4, { priority: 2, sort_order: 2 }),
            task(2, { priority: 1, sort_order: 3 }),
            task(3, { priority: 1, sort_order: 3 }),
            task(1, { priority: 1, sort_order: 2 }),
        ];

        expect(rankAttentionTaskCandidates(tasks).map(item => item.id))
            .toEqual([1, 2, 3, 4]);
    });
});

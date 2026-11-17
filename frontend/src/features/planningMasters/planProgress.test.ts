import { describe, expect, it } from 'vitest';
import { planProgress } from './usePlanningNavigationSummary';
import { PLANNING_STEP_IDS } from './planningReturn';
import type { Iteration, IterationPlanningReadinessSummary } from '../../types/iteration';

const iteration = { id: 1, name: 'Sprint' } as Iteration;
const response = (
    states: string[],
    counts: { checkpoints_done?: number; checkpoints_total?: number } = {
        checkpoints_done: states.filter(state => state === 'done').length,
        checkpoints_total: 6,
    },
) => ({
    checkpoints: PLANNING_STEP_IDS.slice(0, states.length).map((id, index) => (
        { id, state: states[index], reason_codes: [], counts: {} }
    )),
    ...counts,
}) as unknown as IterationPlanningReadinessSummary;

describe('plan progress', () => {
    it('takes the server count, 6 of 6 for a complete plan', () => {
        const done = Array(6).fill('done');
        expect(planProgress(iteration, response(done))?.ready).toEqual({ done: 6, total: 6, pct: 100 });
        expect(planProgress(iteration, response(['done', 'done', 'todo', 'blocked', 'blocked', 'blocked']))?.nextId)
            .toBe(PLANNING_STEP_IDS[2]);
    });

    it('shows the server count as reported, without counting the checkpoint states again', () => {
        const states = ['done', 'done', 'done', 'todo', 'todo', 'todo'];
        expect(planProgress(iteration, response(states, { checkpoints_done: 2, checkpoints_total: 6 }))?.ready)
            .toEqual({ done: 2, total: 6, pct: 33 });
    });

    it('has no progress without an iteration, without a response or with a partial one', () => {
        const done = Array(6).fill('done');
        expect(planProgress(null, response(done))).toBeNull();
        expect(planProgress(iteration, undefined)).toBeNull();
        expect(planProgress(iteration, response(['done', 'done', 'done']))).toBeNull();
        expect(planProgress(iteration, response(done, {}))).toBeNull();
        expect(planProgress(iteration, response(done, { checkpoints_done: 6 }))).toBeNull();
        expect(planProgress(iteration, response(done, { checkpoints_total: 6 }))).toBeNull();
    });
});

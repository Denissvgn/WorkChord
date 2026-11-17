import { describe, expect, it } from 'vitest';
import { planProgress } from './usePlanningNavigationSummary';
import { PLANNING_STEP_IDS } from './planningReturn';
import type { Iteration, IterationPlanningReadinessSummary } from '../../types/iteration';

const iteration = { id: 1, name: 'Sprint' } as Iteration;
const response = (states: string[]) => ({
    checkpoints: PLANNING_STEP_IDS.slice(0, states.length).map((id, index) => (
        { id, state: states[index], reason_codes: [], counts: {} }
    )),
}) as unknown as IterationPlanningReadinessSummary;

describe('plan progress', () => {
    it('counts the server checkpoints, 6 of 6 for a complete plan', () => {
        const done = Array(6).fill('done');
        expect(planProgress(iteration, response(done))?.ready).toEqual({ done: 6, total: 6, pct: 100 });
        expect(planProgress(iteration, response(['done', 'done', 'todo', 'blocked', 'blocked', 'blocked']))?.nextId)
            .toBe(PLANNING_STEP_IDS[2]);
    });

    it('has no progress without an iteration, without a response or with a partial one', () => {
        expect(planProgress(null, response(Array(6).fill('done')))).toBeNull();
        expect(planProgress(iteration, undefined)).toBeNull();
        expect(planProgress(iteration, response(['done', 'done', 'done']))).toBeNull();
    });
});

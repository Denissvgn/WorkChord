import { describe, expect, it } from 'vitest';
import { pickDefaultIteration } from './iterationStore';

const iteration = (id: number, start_date: string, end_date: string) => ({ id, start_date, end_date });

describe('pickDefaultIteration', () => {
    const past = iteration(1, '2026-09-01', '2026-09-30');
    const current = iteration(2, '2026-11-01', '2026-11-30');
    const upcoming = iteration(3, '2026-12-01', '2026-12-31');
    const later = iteration(4, '2027-01-01', '2027-01-31');

    it('prefers the iteration that covers today', () => {
        expect(pickDefaultIteration([past, upcoming, current], '2026-11-11')).toBe(current);
    });

    it('falls back to the next upcoming iteration', () => {
        expect(pickDefaultIteration([later, past, upcoming], '2026-11-11')).toBe(upcoming);
    });

    it('falls back to the most recent iteration when all are in the past', () => {
        expect(pickDefaultIteration([past, iteration(5, '2026-10-01', '2026-10-31')], '2026-11-11')?.id).toBe(5);
    });

    it('returns nothing for an empty list', () => {
        expect(pickDefaultIteration([], '2026-11-11')).toBeUndefined();
    });
});

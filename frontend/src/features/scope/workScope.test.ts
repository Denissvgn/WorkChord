import { describe, expect, it } from 'vitest';
import { defaultIterationForProject, isScopedPath, resolveWorkScope, scopedLink } from './workScope';

const iteration = (id: number, project_id: number | null, start_date: string, end_date: string) => ({
    id, project_id, start_date, end_date,
});

const TODAY = '2026-11-16';
const ITERATIONS = [
    iteration(11, 1, '2026-10-01', '2026-10-31'),
    iteration(12, 1, '2026-11-01', '2026-11-30'),
    iteration(13, 1, '2026-12-01', '2026-12-31'),
    iteration(21, 2, '2026-09-01', '2026-09-30'),
    iteration(22, 2, '2027-01-01', '2027-01-31'),
    iteration(23, 2, '2027-02-01', '2027-02-28'),
    iteration(31, 3, '2026-06-01', '2026-06-30'),
    iteration(32, 3, '2026-07-01', '2026-07-31'),
    iteration(41, null, '2026-11-10', '2026-11-20'),
];

describe('defaultIterationForProject', () => {
    it('picks the iteration that contains today', () => {
        expect(defaultIterationForProject(ITERATIONS, 1, TODAY)).toBe(12);
    });

    it('picks the next iteration when none contains today', () => {
        expect(defaultIterationForProject(ITERATIONS, 2, TODAY)).toBe(22);
    });

    it('picks the latest iteration when all have ended', () => {
        expect(defaultIterationForProject(ITERATIONS, 3, TODAY)).toBe(32);
    });

    it('opens a project without iterations on its Backlog', () => {
        expect(defaultIterationForProject(ITERATIONS, 9, TODAY)).toBe('backlog');
    });

    it('considers every iteration for All projects', () => {
        expect(defaultIterationForProject(ITERATIONS.filter(item => item.id !== 12), 'all', TODAY)).toBe(41);
    });
});

describe('resolveWorkScope', () => {
    it('keeps a valid primary scope over the fallback', () => {
        expect(resolveWorkScope({ project: 2, iteration: 23 }, { project: 1, iteration: 12 }, ITERATIONS, TODAY))
            .toEqual({ project: 2, iteration: 23 });
    });

    it('accepts All projects and Backlog', () => {
        expect(resolveWorkScope({ project: 'all', iteration: 'backlog' }, {}, ITERATIONS, TODAY))
            .toEqual({ project: 'all', iteration: 'backlog' });
        expect(resolveWorkScope({ project: 'all', iteration: 31 }, {}, ITERATIONS, TODAY))
            .toEqual({ project: 'all', iteration: 31 });
        expect(resolveWorkScope({ project: 3, iteration: 'backlog' }, {}, ITERATIONS, TODAY))
            .toEqual({ project: 3, iteration: 'backlog' });
    });

    it('uses the fallback when the primary scope is empty', () => {
        expect(resolveWorkScope({}, { project: 2, iteration: 21 }, ITERATIONS, TODAY))
            .toEqual({ project: 2, iteration: 21 });
    });

    it('chooses the default with nothing given', () => {
        expect(resolveWorkScope({}, {}, ITERATIONS, TODAY)).toEqual({ project: 1, iteration: 12 });
    });

    it('takes the project of the most recently used iteration', () => {
        expect(resolveWorkScope({}, { iteration: 31 }, ITERATIONS, TODAY)).toEqual({ project: 3, iteration: 31 });
    });

    it('takes the project of an iteration given without one', () => {
        expect(resolveWorkScope({ iteration: 22 }, { project: 1, iteration: 12 }, ITERATIONS, TODAY))
            .toEqual({ project: 2, iteration: 22 });
    });

    it('places an iteration without a project in All projects', () => {
        expect(resolveWorkScope({ iteration: 41 }, {}, ITERATIONS, TODAY)).toEqual({ project: 'all', iteration: 41 });
    });

    it('replaces an iteration of another project by the project default', () => {
        expect(resolveWorkScope({ project: 2, iteration: 12 }, {}, ITERATIONS, TODAY))
            .toEqual({ project: 2, iteration: 22 });
    });

    it('replaces an iteration that does not exist by the project default', () => {
        expect(resolveWorkScope({ project: 1, iteration: 999 }, {}, ITERATIONS, TODAY))
            .toEqual({ project: 1, iteration: 12 });
    });

    it('keeps the remembered iteration when only the project comes first and it fits', () => {
        expect(resolveWorkScope({ project: 1 }, { project: 2, iteration: 13 }, ITERATIONS, TODAY))
            .toEqual({ project: 1, iteration: 13 });
    });

    it('falls back to All projects and Backlog when there are no iterations', () => {
        expect(resolveWorkScope({}, {}, [], TODAY)).toEqual({ project: 'all', iteration: 'backlog' });
    });
});

describe('scopedLink', () => {
    const scope = { project: 2, iteration: 22 } as const;

    it('adds the scope to links that open a scoped page', () => {
        expect(scopedLink('/', scope)).toBe('/?project=2&iteration=22');
        expect(scopedLink('/plan', scope)).toBe('/plan?project=2&iteration=22');
        expect(scopedLink('/gantt', scope)).toBe('/gantt?project=2&iteration=22');
        expect(scopedLink('/analytics', scope)).toBe('/analytics?project=2&iteration=22');
        expect(scopedLink('/plan/master?step=team', scope)).toBe('/plan/master?step=team&project=2&iteration=22');
    });

    it('keeps other parameters and the hash', () => {
        expect(scopedLink('/tasks?view=4&project=1#list', scope)).toBe('/tasks?view=4&project=2&iteration=22#list');
    });

    it('leaves workspace-wide pages and unknown scopes alone', () => {
        expect(scopedLink('/my-work', scope)).toBe('/my-work');
        expect(scopedLink('/triage', scope)).toBe('/triage');
        expect(scopedLink('/plan/share/abc', scope)).toBe('/plan/share/abc');
        expect(scopedLink('/tasks', undefined)).toBe('/tasks');
    });

    it('treats only the scoped destinations and the planning page as scoped pages', () => {
        expect(['/', '/plan', '/plan/master', '/gantt', '/tasks', '/analytics'].every(isScopedPath)).toBe(true);
        expect(['/my-work', '/triage', '/projects', '/team', '/settings', '/plan/share/abc'].some(isScopedPath)).toBe(false);
    });

    it('treats route variants the router opens as the same page', () => {
        expect(['/tasks/', '/Tasks', '/plan/master/', '/gantt//', '//'].every(isScopedPath)).toBe(true);
        expect(['/tasks/extra', '/my-work/', '/plan/share/abc/'].some(isScopedPath)).toBe(false);
        expect(scopedLink('/tasks/', scope)).toBe('/tasks/?project=2&iteration=22');
        expect(scopedLink('/analytics/?range=30#flow', scope)).toBe('/analytics/?range=30&project=2&iteration=22#flow');
        expect(scopedLink('/my-work/', scope)).toBe('/my-work/');
    });
});

import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { createElement, type ReactNode } from 'react';
import { renderHook } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { useIterationStore } from './iterationStore';
import { pickDefaultIteration } from '../features/scope/workScope';
import {
    LEGACY_ITERATION_STORAGE_KEY,
    SCOPE_STORAGE_KEY,
    useScopeStore,
} from '../features/scope/scopeStore';

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

describe('useIterationStore', () => {
    beforeEach(() => {
        useScopeStore.setState({ project: null, iteration: null });
    });

    it('reads the iteration of the work scope', () => {
        useScopeStore.getState().remember({ project: 3, iteration: 8 });
        expect(useIterationStore.getState().selectedIterationId).toBe(8);

        useScopeStore.getState().remember({ project: 3, iteration: 'backlog' });
        expect(useIterationStore.getState().selectedIterationId).toBe(0);
    });

    it('sets the iteration and lets the project follow it', () => {
        useScopeStore.getState().remember({ project: 3, iteration: 8 });

        useIterationStore.getState().setSelectedIterationId(9);

        expect(useScopeStore.getState()).toMatchObject({ project: null, iteration: 9 });
    });

    it('keeps the chosen project when the iteration is cleared', () => {
        useScopeStore.getState().remember({ project: 2, iteration: 999 });

        useIterationStore.getState().setSelectedIterationId(0);

        expect(useScopeStore.getState()).toMatchObject({ project: 2, iteration: null });
    });

    it('stays on All projects when an iteration is set there', () => {
        useScopeStore.getState().remember({ project: 'all', iteration: 8 });

        useIterationStore.setState({ selectedIterationId: 9 });

        expect(useScopeStore.getState()).toMatchObject({ project: 'all', iteration: 9 });
    });

    it('keeps Backlog apart from no iteration chosen', () => {
        useScopeStore.getState().remember({ project: 3, iteration: 'backlog' });
        expect(useIterationStore.getState()).toMatchObject({ selectedIterationId: 0, isBacklog: true });

        useScopeStore.getState().remember({ project: 3, iteration: null });
        expect(useIterationStore.getState()).toMatchObject({ selectedIterationId: 0, isBacklog: false });
    });

    describe('chooseDefaultIteration', () => {
        const scoped = (id: number, project_id: number, start_date: string, end_date: string) => ({
            id, project_id, start_date, end_date,
        });
        const ITERATIONS = [
            scoped(12, 1, '2026-11-01', '2026-11-30'),
            scoped(21, 2, '2026-09-01', '2026-09-30'),
            scoped(22, 2, '2027-01-01', '2027-01-31'),
        ];

        beforeEach(() => {
            vi.useFakeTimers({ toFake: ['Date'] });
            vi.setSystemTime(new Date('2026-11-16T12:00:00Z'));
        });

        afterEach(() => {
            vi.useRealTimers();
        });

        it('keeps Backlog', () => {
            useScopeStore.getState().remember({ project: 2, iteration: 'backlog' });
            useIterationStore.getState().chooseDefaultIteration(ITERATIONS);
            expect(useScopeStore.getState()).toMatchObject({ project: 2, iteration: 'backlog' });
        });

        it('keeps an iteration that exists', () => {
            useScopeStore.getState().remember({ project: 2, iteration: 21 });
            useIterationStore.getState().chooseDefaultIteration(ITERATIONS);
            expect(useScopeStore.getState()).toMatchObject({ project: 2, iteration: 21 });
        });

        it('chooses the default of the chosen project, not of another one', () => {
            useScopeStore.getState().remember({ project: 2, iteration: null });
            useIterationStore.getState().chooseDefaultIteration(ITERATIONS);
            expect(useScopeStore.getState()).toMatchObject({ project: 2, iteration: 22 });
        });

        it('replaces an iteration that no longer exists', () => {
            useScopeStore.getState().remember({ project: 1, iteration: 99 });
            useIterationStore.getState().chooseDefaultIteration(ITERATIONS);
            expect(useScopeStore.getState()).toMatchObject({ project: 1, iteration: 12 });
        });

        it('uses the default rule when nothing is chosen', () => {
            useIterationStore.getState().chooseDefaultIteration(ITERATIONS);
            expect(useScopeStore.getState()).toMatchObject({ project: 1, iteration: 12 });
        });
    });

    it('reads the iteration in the URL before the remembered one', () => {
        useScopeStore.getState().remember({ project: 1, iteration: 12 });
        const at = (entry: string) => renderHook(() => useIterationStore(), {
            wrapper: ({ children }: { children: ReactNode }) => createElement(MemoryRouter, { initialEntries: [entry] }, children),
        }).result.current;

        expect(at('/gantt?project=2&iteration=backlog')).toMatchObject({ selectedIterationId: 0, isBacklog: true });
        expect(at('/gantt?project=2&iteration=21')).toMatchObject({ selectedIterationId: 21, isBacklog: false });
        expect(at('/team')).toMatchObject({ selectedIterationId: 12, isBacklog: false });
    });

    it('remembers the scope under the scope key', () => {
        useScopeStore.getState().remember({ project: 4, iteration: 12 });

        expect(JSON.parse(window.localStorage.getItem(SCOPE_STORAGE_KEY)!).state).toEqual({ project: 4, iteration: 12 });
        expect(window.localStorage.getItem(LEGACY_ITERATION_STORAGE_KEY)).toBeNull();
    });
});

describe('remembered iteration under the old key', () => {
    const loadFreshScopeStore = async () => {
        vi.resetModules();
        return import('../features/scope/scopeStore');
    };

    it('is carried over once and the old key is then removed', async () => {
        window.localStorage.setItem(
            LEGACY_ITERATION_STORAGE_KEY,
            JSON.stringify({ state: { selectedIterationId: 7 }, version: 0 }),
        );

        const first = await loadFreshScopeStore();

        expect(first.useScopeStore.getState()).toMatchObject({ project: null, iteration: 7 });
        expect(window.localStorage.getItem(LEGACY_ITERATION_STORAGE_KEY)).toBeNull();
        expect(JSON.parse(window.localStorage.getItem(SCOPE_STORAGE_KEY)!).state).toEqual({ project: null, iteration: 7 });

        first.useScopeStore.getState().remember({ project: 2, iteration: 5 });
        const second = await loadFreshScopeStore();

        expect(second.useScopeStore.getState()).toMatchObject({ project: 2, iteration: 5 });
        expect(window.localStorage.getItem(LEGACY_ITERATION_STORAGE_KEY)).toBeNull();
    });

    it('does not replace a scope already remembered under the new key', async () => {
        window.localStorage.setItem(SCOPE_STORAGE_KEY, JSON.stringify({ state: { project: 2, iteration: 5 }, version: 0 }));
        window.localStorage.setItem(
            LEGACY_ITERATION_STORAGE_KEY,
            JSON.stringify({ state: { selectedIterationId: 7 }, version: 0 }),
        );

        const { useScopeStore: freshStore } = await loadFreshScopeStore();

        expect(freshStore.getState()).toMatchObject({ project: 2, iteration: 5 });
        expect(window.localStorage.getItem(LEGACY_ITERATION_STORAGE_KEY)).toBeNull();
    });

    it('drops an old value that is not an iteration', async () => {
        window.localStorage.setItem(
            LEGACY_ITERATION_STORAGE_KEY,
            JSON.stringify({ state: { selectedIterationId: 0 }, version: 0 }),
        );

        const { useScopeStore: freshStore } = await loadFreshScopeStore();

        expect(freshStore.getState()).toMatchObject({ project: null, iteration: null });
        expect(window.localStorage.getItem(SCOPE_STORAGE_KEY)).toBeNull();
        expect(window.localStorage.getItem(LEGACY_ITERATION_STORAGE_KEY)).toBeNull();
    });
});

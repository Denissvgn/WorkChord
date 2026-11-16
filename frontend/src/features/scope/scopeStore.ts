import { create } from 'zustand';
import { createJSONStorage, persist } from 'zustand/middleware';
import type { PartialWorkScope, ScopeIteration, ScopeProject } from './workScope';

/** Where this browser remembers the scope. */
export const SCOPE_STORAGE_KEY = 'work-scope';
/** Where older versions remembered only the iteration. */
export const LEGACY_ITERATION_STORAGE_KEY = 'iteration-storage';

export interface RememberedScope {
    project: ScopeProject | null;
    iteration: ScopeIteration | null;
}

interface ScopeStore extends RememberedScope {
    remember: (scope: PartialWorkScope) => void;
}

const isPositiveInteger = (value: unknown): value is number => (
    typeof value === 'number' && Number.isSafeInteger(value) && value > 0
);

const readProject = (value: unknown): ScopeProject | null => (
    value === 'all' || isPositiveInteger(value) ? value : null
);

const readIteration = (value: unknown): ScopeIteration | null => (
    value === 'backlog' || isPositiveInteger(value) ? value : null
);

const browserStorage = (): Storage | undefined => {
    try {
        return typeof window === 'undefined' ? undefined : window.localStorage;
    } catch {
        return undefined;
    }
};

/**
 * Carries the iteration remembered under the old key over to the scope key, then removes
 * the old key. A scope already remembered under the new key is kept. Safe to call again:
 * once the old key is gone there is nothing left to carry over.
 */
export const migrateLegacyIterationStorage = (storage: Storage | undefined = browserStorage()): void => {
    if (!storage) return;
    try {
        const legacy = storage.getItem(LEGACY_ITERATION_STORAGE_KEY);
        if (legacy === null) return;
        if (storage.getItem(SCOPE_STORAGE_KEY) === null) {
            let iteration: ScopeIteration | null = null;
            try {
                iteration = readIteration(JSON.parse(legacy)?.state?.selectedIterationId);
            } catch {
                iteration = null;
            }
            if (iteration !== null) {
                const remembered: RememberedScope = { project: null, iteration };
                storage.setItem(SCOPE_STORAGE_KEY, JSON.stringify({ state: remembered, version: 0 }));
            }
        }
        storage.removeItem(LEGACY_ITERATION_STORAGE_KEY);
    } catch {
        // Storage can be unavailable or full; the scope then falls back to the default rule.
    }
};

migrateLegacyIterationStorage();

/** The scope this browser remembers. Read it through useWorkScope, which puts the URL first. */
export const useScopeStore = create<ScopeStore>()(
    persist(
        (set) => ({
            project: null,
            iteration: null,
            remember: (scope) => set({
                project: readProject(scope.project),
                iteration: readIteration(scope.iteration),
            }),
        }),
        {
            name: SCOPE_STORAGE_KEY,
            storage: createJSONStorage(() => browserStorage() ?? {
                getItem: () => null,
                setItem: () => undefined,
                removeItem: () => undefined,
            }),
            partialize: ({ project, iteration }): RememberedScope => ({ project, iteration }),
            merge: (persisted, current) => {
                const stored = (persisted ?? {}) as Partial<RememberedScope>;
                return {
                    ...current,
                    project: readProject(stored.project),
                    iteration: readIteration(stored.iteration),
                };
            },
        },
    ),
);

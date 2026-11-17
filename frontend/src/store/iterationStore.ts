import { useMemo } from 'react';
import { useLocation } from 'react-router-dom';
import { parseScope } from '../navigation/scopeParams';
import { useScopeStore, type RememberedScope } from '../features/scope/scopeStore';
import { resolveWorkScope, type ScopeIterationRecord } from '../features/scope/workScope';

/**
 * The iteration-only view of the work scope, for pages that still set the iteration with
 * their own control. The scope store holds the value; useWorkScope puts it in the URL.
 * In a component the iteration in the URL comes first, so a page shows the scope of its
 * URL from its first render, before the shell has remembered it.
 */
interface IterationStore {
    /** The selected iteration, or 0 when no iteration is selected or Backlog is chosen. */
    selectedIterationId: number;
    /** True when Backlog is chosen. Backlog is a choice: it is never replaced by a default. */
    isBacklog: boolean;
    setSelectedIterationId: (id: number) => void;
    /**
     * Chooses the scope's default iteration when nothing is chosen or the chosen iteration
     * no longer exists. Backlog and an existing iteration are kept. The project is kept too:
     * the default is the one of the chosen project.
     */
    chooseDefaultIteration: (iterations: readonly ScopeIterationRecord[]) => void;
}

const toIterationId = (iteration: RememberedScope['iteration']): number => (
    typeof iteration === 'number' ? iteration : 0
);

/**
 * Selects an iteration. Within All projects the scope stays on All projects; otherwise the
 * project is left open so the scope takes the project of the chosen iteration. Any id that
 * is not an iteration clears only the iteration: the chosen project is kept, and the scope
 * then falls back to that project's default iteration.
 */
const setSelectedIterationId = (id: number) => {
    const { project, remember } = useScopeStore.getState();
    if (!Number.isSafeInteger(id) || id <= 0) {
        remember({ project, iteration: null });
        return;
    }
    remember({ project: project === 'all' ? 'all' : null, iteration: id });
};

const chooseDefaultIteration = (iterations: readonly ScopeIterationRecord[]) => {
    const { project, iteration, remember } = useScopeStore.getState();
    if (iteration === 'backlog') return;
    if (typeof iteration === 'number' && iterations.some(item => item.id === iteration)) return;
    remember(resolveWorkScope({ project }, {}, iterations));
};

const getState = (): IterationStore => {
    const { iteration } = useScopeStore.getState();
    return {
        selectedIterationId: toIterationId(iteration),
        isBacklog: iteration === 'backlog',
        setSelectedIterationId,
        chooseDefaultIteration,
    };
};

const useIterationStoreHook = (): IterationStore => {
    const { search } = useLocation();
    const urlIteration = useMemo(() => parseScope(search).iteration, [search]);
    const rememberedIteration = useScopeStore(state => state.iteration);
    const iteration = urlIteration ?? rememberedIteration;
    return {
        selectedIterationId: toIterationId(iteration),
        isBacklog: iteration === 'backlog',
        setSelectedIterationId,
        chooseDefaultIteration,
    };
};

export const useIterationStore = Object.assign(useIterationStoreHook, {
    getState,
    setState: (partial: Partial<Pick<IterationStore, 'selectedIterationId'>>) => {
        if (partial.selectedIterationId !== undefined) setSelectedIterationId(partial.selectedIterationId);
    },
});

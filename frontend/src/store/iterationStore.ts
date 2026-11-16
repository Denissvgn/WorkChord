import { useScopeStore, type RememberedScope } from '../features/scope/scopeStore';

export { pickDefaultIteration } from '../features/scope/workScope';

/**
 * The iteration-only view of the work scope, for pages that still set the iteration with
 * their own control. The scope store holds the value; useWorkScope puts it in the URL.
 */
interface IterationStore {
    /** The selected iteration, or 0 when none is selected or Backlog is chosen. */
    selectedIterationId: number;
    setSelectedIterationId: (id: number) => void;
}

const toIterationId = (iteration: RememberedScope['iteration']): number => (
    typeof iteration === 'number' ? iteration : 0
);

/**
 * Selects an iteration. Within All projects the scope stays on All projects; otherwise the
 * project is left open so the scope takes the project of the chosen iteration.
 */
const setSelectedIterationId = (id: number) => {
    const { project, remember } = useScopeStore.getState();
    remember({
        project: project === 'all' ? 'all' : null,
        iteration: Number.isSafeInteger(id) && id > 0 ? id : null,
    });
};

const getState = (): IterationStore => ({
    selectedIterationId: toIterationId(useScopeStore.getState().iteration),
    setSelectedIterationId,
});

const useIterationStoreHook = (): IterationStore => {
    const iteration = useScopeStore(state => state.iteration);
    return { selectedIterationId: toIterationId(iteration), setSelectedIterationId };
};

export const useIterationStore = Object.assign(useIterationStoreHook, {
    getState,
    setState: (partial: Partial<Pick<IterationStore, 'selectedIterationId'>>) => {
        if (partial.selectedIterationId !== undefined) setSelectedIterationId(partial.selectedIterationId);
    },
});

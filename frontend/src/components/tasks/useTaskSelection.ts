import { useCallback, useMemo, useRef, useState } from 'react';

interface TaskSelectionOptions {
    /** Every task that can be ticked, wherever it sits in the list. */
    selectableIds: Set<number>;
    /** The ticked-able tasks in the order a person sees them; a shift-click ticks the range between two. */
    order: number[];
    /**
     * The iteration a task belongs to. Bulk changes apply to one iteration at a time, so once a task
     * is ticked only tasks of its iteration can be added. Left out, every task is in the same scope.
     */
    iterationOf?: (taskId: number) => number | null | undefined;
}

/** Direct row selection: tick any row, shift-click for a range, no mode to enter first. */
export const useTaskSelection = ({ selectableIds, order, iterationOf }: TaskSelectionOptions) => {
    const [ticked, setTicked] = useState<Set<number>>(new Set());
    const anchor = useRef<number | null>(null);

    // Only tasks still in the list count, so a filter change never leaves a hidden task selected.
    const selectedIds = useMemo(() => new Set([...ticked].filter(id => selectableIds.has(id))), [ticked, selectableIds]);
    const scopeId = useMemo(() => {
        const first = [...selectedIds][0];
        return first === undefined ? null : iterationOf?.(first) ?? null;
    }, [selectedIds, iterationOf]);
    const hasScope = selectedIds.size > 0 && iterationOf !== undefined;
    const inScope = useCallback(
        (id: number) => !hasScope || iterationOf?.(id) === scopeId,
        [hasScope, iterationOf, scopeId],
    );

    const toggle = useCallback((taskId: number, shiftKey: boolean) => {
        if (!selectableIds.has(taskId) || !inScope(taskId)) return;
        const next = new Set(selectedIds);
        const from = anchor.current === null ? -1 : order.indexOf(anchor.current);
        const to = order.indexOf(taskId);
        if (shiftKey && from >= 0 && to >= 0) {
            order.slice(Math.min(from, to), Math.max(from, to) + 1).filter(inScope).forEach(id => next.add(id));
        } else if (next.has(taskId)) {
            next.delete(taskId);
        } else {
            next.add(taskId);
        }
        anchor.current = taskId;
        setTicked(next);
    }, [selectableIds, inScope, selectedIds, order]);

    /** The tasks a "Select all" reaches: every selectable task of the selection's iteration. */
    const matchingIds = useMemo(() => [...selectableIds].filter(inScope), [selectableIds, inScope]);
    const replace = useCallback((ids: Iterable<number>) => { anchor.current = null; setTicked(new Set(ids)); }, []);
    const clear = useCallback(() => replace([]), [replace]);

    return {
        selectedIds,
        toggle,
        /** Whether this task can be added to the selection now; false for a task of another iteration. */
        canAdd: (taskId: number) => selectableIds.has(taskId) && inScope(taskId),
        matchingIds,
        selectAll: () => replace(matchingIds),
        replace,
        clear,
    };
};

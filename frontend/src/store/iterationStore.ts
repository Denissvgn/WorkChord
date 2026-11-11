import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface IterationStore {
    selectedIterationId: number;
    setSelectedIterationId: (id: number) => void;
}

export const useIterationStore = create<IterationStore>()(
    persist(
        (set) => ({
            selectedIterationId: 0,
            setSelectedIterationId: (id: number) => set({ selectedIterationId: id }),
        }),
        {
            name: 'iteration-storage',
        }
    )
);

type DatedIteration = { id: number; start_date: string; end_date: string };

/**
 * The one rule every page uses when no valid iteration is selected: the
 * iteration that covers today, else the next upcoming one, else the most
 * recent. Dates are ISO calendar dates, so string comparison orders them.
 */
export const pickDefaultIteration = <T extends DatedIteration>(
    iterations: readonly T[],
    today: string = new Date().toISOString().slice(0, 10),
): T | undefined => {
    if (iterations.length === 0) return undefined;
    const current = iterations.find(item => item.start_date.slice(0, 10) <= today && today <= item.end_date.slice(0, 10));
    if (current) return current;
    const upcoming = iterations
        .filter(item => item.start_date.slice(0, 10) > today)
        .sort((a, b) => a.start_date.localeCompare(b.start_date))[0];
    if (upcoming) return upcoming;
    return [...iterations].sort((a, b) => b.end_date.localeCompare(a.end_date))[0];
};

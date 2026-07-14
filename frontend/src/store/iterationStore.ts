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

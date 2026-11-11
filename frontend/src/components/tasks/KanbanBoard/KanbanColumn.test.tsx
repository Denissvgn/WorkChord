import { describe, expect, it, vi } from 'vitest';
import { screen } from '@testing-library/react';
import type { ReactNode } from 'react';
import type { Task } from '../../../types/task';
import { renderWithProviders } from '../../../test/renderWithProviders';
import { KanbanColumn } from './KanbanColumn';
import { KanbanCard } from './KanbanCard';
import { formatClaimUntil } from './claimTime';

vi.mock('@dnd-kit/core', () => ({ useDroppable: () => ({ setNodeRef: () => undefined, isOver: false }) }));
vi.mock('@dnd-kit/sortable', () => ({
    SortableContext: ({ children }: { children: ReactNode }) => <>{children}</>,
    verticalListSortingStrategy: {},
    useSortable: () => ({ attributes: {}, listeners: {}, setNodeRef: () => undefined, transform: null, transition: undefined, isDragging: false }),
}));

const task = (id: number, extra: Partial<Task> = {}) => ({
    id, iteration_id: 1, title: `Task ${id}`, priority: 5, effort_days: 1, effort_hours: 8, status: 'planned',
    tags: [], children: [], dependencies: [], version: 1, ...extra,
}) as unknown as Task;

describe('Board column', () => {
    it('shows twenty cards and then twenty more on request', async () => {
        const tasks = Array.from({ length: 45 }, (_, index) => task(index + 1));
        const { user } = renderWithProviders(<KanbanColumn id="active" title="Active" tasks={tasks} count={45} tone="blue" />);
        expect(screen.getAllByRole('button', { name: /^Open task/ })).toHaveLength(20);
        await user.click(screen.getByRole('button', { name: 'Show 20 more (25 left)' }));
        expect(screen.getAllByRole('button', { name: /^Open task/ })).toHaveLength(40);
        await user.click(screen.getByRole('button', { name: 'Show 5 more (5 left)' }));
        expect(screen.getAllByRole('button', { name: /^Open task/ })).toHaveLength(45);
        expect(screen.queryByRole('button', { name: /^Show/ })).not.toBeInTheDocument();
    });

    it('folds an empty column to a named drop strip', () => {
        renderWithProviders(<KanbanColumn id="closed" title="Closed" tasks={[]} count={0} tone="gray" />);
        expect(screen.getByRole('region', { name: 'Closed: no tasks. Drop a task here to move it.' })).toBeInTheDocument();
    });
});

describe('Board card', () => {
    it('labels the claim time and says when effort is unknown', () => {
        renderWithProviders(<KanbanCard task={task(7, { effort_days: null, claimed_by: { display_name: 'Agent A' }, claim_expires_at: '2030-01-02T18:42:00Z' } as Partial<Task>)} />);
        expect(screen.getByText(/^Claimed by Agent A, held until /)).toBeInTheDocument();
        expect(screen.getByText('No estimate')).toBeInTheDocument();
        expect(screen.getAllByText(/#7/)).toHaveLength(1);
    });

    it('writes only the time for a claim that ends today', () => {
        const now = new Date(2030, 0, 2, 9, 0);
        expect(formatClaimUntil(new Date(2030, 0, 2, 18, 42).toISOString(), 'en-GB', now)).toMatch(/^18:42 \S+/);
        expect(formatClaimUntil(new Date(2030, 0, 3, 18, 42).toISOString(), 'en-GB', now)).toContain('2030');
        expect(formatClaimUntil('not a date', 'en-GB', now)).toBeNull();
    });
});

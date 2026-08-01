import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen } from '@testing-library/react';
import { useLocation } from 'react-router-dom';
import type { ReactNode } from 'react';
import { renderWithProviders } from '../test/renderWithProviders';
import TasksPage from './TasksPage';

const iterationServiceMock = vi.hoisted(() => ({
    getAll: vi.fn(),
}));

const iterationStoreMock = vi.hoisted(() => ({
    selectedIterationId: 1,
    setSelectedIterationId: vi.fn(),
}));

vi.mock('../services/iterationService', () => ({
    iterationService: iterationServiceMock,
}));

vi.mock('../store/iterationStore', () => ({
    useIterationStore: () => iterationStoreMock,
}));

vi.mock('../components/tasks/TaskList', () => ({
    TaskList: () => <div>Task list</div>,
}));

vi.mock('../components/tasks/KanbanBoard/KanbanBoard', () => ({
    KanbanBoard: () => <div>Board</div>,
}));

vi.mock('../components/tasks/TaskFiltersBar', () => ({
    defaultFilters: {},
    TaskFiltersBar: () => <div>Filters</div>,
}));

vi.mock('../components/tasks/SavedViewsControl', () => ({
    SavedViewsControl: () => <div>Saved views</div>,
}));

vi.mock('../components/iteration/IterationSelector', () => ({
    IterationSelector: () => <div>Iteration selector</div>,
}));

vi.mock('../components/common/Modal', () => ({
    Modal: ({ open, children }: { open: boolean; children: ReactNode }) => open ? <div role="dialog">{children}</div> : null,
}));

vi.mock('../components/tasks/TaskForm', () => ({
    TaskForm: ({ onCancel }: { onCancel: () => void }) => <button type="button" onClick={onCancel}>Cancel draft</button>,
}));

const LocationProbe = () => {
    const location = useLocation();
    return <output data-testid="location-search">{location.search}</output>;
};

describe('TasksPage', () => {
    beforeEach(() => {
        iterationStoreMock.selectedIterationId = 1;
        iterationStoreMock.setSelectedIterationId.mockReset();
        iterationServiceMock.getAll.mockReset();
        iterationServiceMock.getAll.mockResolvedValue([
            { id: 1, name: 'Iteration one', start_date: '2026-01-01', end_date: '2026-01-14' },
        ]);
    });

    it('opens the task creator from the create query and clears the intent when dismissed', async () => {
        const { user } = renderWithProviders(
            <>
                <TasksPage />
                <LocationProbe />
            </>,
            { initialEntries: ['/tasks?create=1'] },
        );

        expect(await screen.findByRole('dialog')).toBeInTheDocument();
        expect(screen.getByRole('button', { name: 'Cancel draft' })).toBeInTheDocument();

        await user.click(screen.getByRole('button', { name: 'Cancel draft' }));

        expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
        expect(screen.getByTestId('location-search')).toHaveTextContent('');
    });
});

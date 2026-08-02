import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, within } from '@testing-library/react';
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
const savedViewServiceMock = vi.hoisted(() => ({
    getAll: vi.fn(),
}));

vi.mock('../services/iterationService', () => ({
    iterationService: iterationServiceMock,
}));
vi.mock('../services/savedViewService', () => ({
    savedViewService: savedViewServiceMock,
}));

vi.mock('../store/iterationStore', () => ({
    useIterationStore: () => iterationStoreMock,
}));

vi.mock('../components/tasks/TaskList', () => ({
    TaskList: ({ requestedMode }: { requestedMode?: string | null }) => (
        <div>Task list{requestedMode ? ` — ${requestedMode}` : ''}</div>
    ),
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
        savedViewServiceMock.getAll.mockReset();
        savedViewServiceMock.getAll.mockResolvedValue([]);
    });

    it('clears create intent while preserving a Plan Master return checkpoint', async () => {
        const { user } = renderWithProviders(
            <>
                <TasksPage />
                <LocationProbe />
            </>,
            { initialEntries: ['/tasks?create=1&fromPlanStep=work'] },
        );

        expect(await screen.findByRole('dialog')).toBeInTheDocument();
        expect(screen.getByRole('button', { name: 'Cancel draft' })).toBeInTheDocument();
        expect(screen.getByRole('link', { name: 'Return to plan' }))
            .toHaveAttribute('href', '/plan/master?step=work');

        await user.click(screen.getByRole('button', { name: 'Cancel draft' }));

        expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
        expect(screen.getByTestId('location-search')).toHaveTextContent('?fromPlanStep=work');
    });

    it('applies a URL-selected saved view and keeps its context visible', async () => {
        savedViewServiceMock.getAll.mockResolvedValue([{
            id: 12,
            name: 'Needs owners',
            description: null,
            seed_key: null,
            view_type: 'tasks',
            scope: 'shared',
            filters_json: { assigneeId: -1 },
            sort_json: { sortKey: 'priority' },
            columns_json: {},
            created_by_session_id: null,
            schema_version: 1,
            is_valid: true,
            invalid_reason: null,
            created_at: '2026-08-01T00:00:00Z',
            updated_at: '2026-08-01T00:00:00Z',
        }]);

        renderWithProviders(<TasksPage />, {
            initialEntries: ['/tasks?view=12'],
        });

        expect(await screen.findByText('Needs owners')).toBeVisible();
        expect(screen.getByText('1 active filter(s)')).toBeVisible();
        expect(screen.getByRole('button', { name: 'Clear view' })).toBeVisible();
        expect(savedViewServiceMock.getAll).toHaveBeenCalledWith({ view_type: 'tasks' });
    });

    it('opens expert task modes from URL commands', async () => {
        const { user } = renderWithProviders(<TasksPage />, {
            initialEntries: ['/tasks?mode=bulk'],
        });

        expect(await screen.findByText('Task list — bulk')).toBeVisible();
        expect(screen.queryByText('How tasks become plan-ready')).not.toBeInTheDocument();

        await user.click(screen.getByRole('button', { name: 'Planning help' }));
        const guide = screen.getByRole('dialog', { name: 'How tasks become plan-ready' });
        expect(guide).toBeVisible();
        expect(within(guide).getByRole('heading', {
            name: 'Required for every planned task',
        })).toBeVisible();
        expect(within(guide).getByRole('heading', {
            name: 'Optional: prepare agent execution',
        })).toBeVisible();
    });

    it('opens filters and board layout from command URLs', async () => {
        renderWithProviders(<TasksPage />, {
            initialEntries: ['/tasks?panel=filters&layout=board'],
        });

        const viewContext = await screen.findByRole('region', { name: 'Task view context' });
        expect(within(viewContext).getByRole('button', { name: 'Board' }))
            .toHaveAttribute('aria-pressed', 'true');
        expect(within(viewContext).getByRole('button', { name: 'Filters' })).toBeVisible();
        expect(within(viewContext).getByRole('button', { name: 'List' })).toBeVisible();
        const newTaskAction = screen.getByRole('button', { name: 'New Task' });
        expect(newTaskAction.closest('.tasks-primary-slot')).not.toBeNull();
        expect(screen.getAllByRole('button', { name: 'New Task' })).toHaveLength(1);
        expect(screen.getByRole('dialog', { name: 'Filters' })).toBeVisible();
    });
});

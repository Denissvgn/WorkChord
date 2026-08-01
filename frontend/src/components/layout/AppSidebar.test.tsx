import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { AppSidebar } from './AppSidebar';
import type { SavedView } from '../../types/savedView';

const savedViewServiceMock = vi.hoisted(() => ({
    getAll: vi.fn(),
}));

const systemTaskView: SavedView = {
    id: 42,
    name: 'My queued tasks',
    seed_key: 'tasks_blocked',
    view_type: 'tasks',
    scope: 'system',
    filters_json: {},
    sort_json: {},
    columns_json: {},
    schema_version: 1,
    is_valid: true,
    created_at: '2026-01-01T00:00:00Z',
    updated_at: '2026-01-01T00:00:00Z',
};

vi.mock('../../services/savedViewService', () => ({
    savedViewService: savedViewServiceMock,
}));

vi.mock('./SidebarIterationCard', () => ({
    SidebarIterationCard: () => <div>Planning summary</div>,
}));

describe('AppSidebar', () => {
    beforeEach(() => {
        savedViewServiceMock.getAll.mockReset();
        savedViewServiceMock.getAll.mockResolvedValue([]);
    });

    it('shows only Planning destinations for a Planning route', () => {
        renderWithProviders(<AppSidebar />, { initialEntries: ['/roadmap'] });

        expect(screen.getByLabelText('Timeline & Planning Primary navigation')).toBeInTheDocument();
        expect(screen.getByRole('link', { name: 'Gantt' })).toBeInTheDocument();
        expect(screen.getByRole('link', { name: 'Roadmap' })).toHaveAttribute('aria-current', 'page');
        expect(screen.queryByRole('link', { name: 'Tasks' })).not.toBeInTheDocument();
        expect(screen.queryByRole('link', { name: 'Team' })).not.toBeInTheDocument();
        expect(savedViewServiceMock.getAll).not.toHaveBeenCalled();
    });

    it('shows only Resource & Settings destinations for a resource route', () => {
        renderWithProviders(<AppSidebar />, { initialEntries: ['/settings'] });

        expect(screen.getByRole('link', { name: 'Team' })).toBeInTheDocument();
        expect(screen.getByRole('link', { name: 'Settings' })).toHaveAttribute('aria-current', 'page');
        expect(screen.queryByRole('link', { name: 'Gantt' })).not.toBeInTheDocument();
        expect(screen.queryByText('Planning summary')).not.toBeInTheDocument();
    });

    it('keeps Delivery views and planning context inside the Delivery workspace', () => {
        renderWithProviders(<AppSidebar />, { initialEntries: ['/tasks'] });

        expect(screen.getByRole('link', { name: 'Tasks' })).toHaveAttribute('aria-current', 'page');
        expect(screen.getByText('Planning summary')).toBeInTheDocument();
        expect(screen.queryByRole('link', { name: 'Gantt' })).not.toBeInTheDocument();
    });

    it('keeps Views open when an in-flight request resolves', async () => {
        let resolveViews!: (views: SavedView[]) => void;
        const pendingViews = new Promise<SavedView[]>(resolve => {
            resolveViews = resolve;
        });
        savedViewServiceMock.getAll.mockReturnValue(pendingViews);

        const { user } = renderWithProviders(<AppSidebar />, { initialEntries: ['/tasks'] });
        const viewsLabel = screen.getByText('Views');
        const disclosure = viewsLabel.closest('details');

        await user.click(viewsLabel);
        expect(disclosure).toHaveAttribute('open');

        resolveViews([]);
        expect(await screen.findByText('No system views')).toBeVisible();
        expect(disclosure).toHaveAttribute('open');
    });

    it('marks only the matching saved view as current when a view query is present', async () => {
        savedViewServiceMock.getAll.mockImplementation(({ view_type }: { view_type: string }) => (
            Promise.resolve(view_type === 'tasks' ? [systemTaskView] : [])
        ));

        renderWithProviders(<AppSidebar />, { initialEntries: ['/tasks?view=42'] });

        const savedViewLink = await screen.findByRole('link', { name: 'My queued tasks' });
        expect(savedViewLink).toHaveAttribute('aria-current', 'page');
        expect(screen.getByRole('link', { name: 'Tasks' })).not.toHaveAttribute('aria-current');
        expect(screen.getAllByRole('link').filter(link => link.getAttribute('aria-current') === 'page')).toHaveLength(1);
    });

    it('names the saved-view recovery action and refetches on retry', async () => {
        savedViewServiceMock.getAll.mockRejectedValue(new Error('offline'));
        const { user } = renderWithProviders(<AppSidebar />, { initialEntries: ['/tasks'] });

        await user.click(screen.getByText('Views'));
        const retry = await screen.findByRole('button', { name: 'Retry saved views' });
        expect(screen.getByRole('status')).toHaveTextContent('Saved views are unavailable.');
        await user.click(retry);

        await waitFor(() => expect(savedViewServiceMock.getAll).toHaveBeenCalledTimes(6));
    });
});

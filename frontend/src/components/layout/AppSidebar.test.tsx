import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { AppSidebar, SidebarContent } from './AppSidebar';
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

const crowdedSystemViews = (count = 7) => Array.from({ length: count }, (_, index): SavedView => ({
    ...systemTaskView,
    id: 100 + index,
    name: `Queue view ${index + 1}`,
    seed_key: `queue_view_${index + 1}`,
}));

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

        expect(screen.getByLabelText('Timeline & Planning destinations')).toBeInTheDocument();
        expect(screen.getByRole('navigation', {
            name: 'Timeline & Planning destinations',
        })).toBeInTheDocument();
        expect(screen.getByRole('link', { name: 'Gantt' })).toBeInTheDocument();
        expect(screen.getByRole('link', { name: 'Plan Work' })).toBeInTheDocument();
        expect(screen.getByRole('link', { name: 'Roadmap' })).toHaveAttribute('aria-current', 'page');
        expect(screen.getByText('Planning summary')).toBeInTheDocument();
        expect(screen.queryByRole('link', { name: 'Tasks' })).not.toBeInTheDocument();
        expect(screen.queryByRole('link', { name: 'Team' })).not.toBeInTheDocument();
        expect(savedViewServiceMock.getAll).not.toHaveBeenCalled();
    });

    it('shows a lone secondary destination directly and preserves its current state', () => {
        const roadmapRender = renderWithProviders(<AppSidebar />, { initialEntries: ['/roadmap'] });

        expect(screen.getByRole('link', { name: 'Calendar' })).toBeVisible();
        expect(screen.queryByText('More')).not.toBeInTheDocument();
        roadmapRender.unmount();

        const calendarRender = renderWithProviders(<AppSidebar />, { initialEntries: ['/calendar'] });
        expect(screen.getByRole('link', { name: 'Calendar' }))
            .toHaveAttribute('aria-current', 'page');
        calendarRender.unmount();

        renderWithProviders(<AppSidebar />, { initialEntries: ['/tasks'] });
        expect(screen.getByRole('link', { name: 'Agent Pipeline' })).toBeVisible();
        expect(screen.queryByText('More')).not.toBeInTheDocument();
    });

    it('shows only Resource & Settings destinations for a resource route', () => {
        renderWithProviders(<AppSidebar />, { initialEntries: ['/settings'] });

        expect(screen.getByRole('link', { name: 'Team' })).toBeInTheDocument();
        expect(screen.getByRole('link', { name: 'Settings' })).toHaveAttribute('aria-current', 'page');
        expect(screen.queryByRole('link', { name: 'Gantt' })).not.toBeInTheDocument();
        expect(screen.queryByText('Planning summary')).not.toBeInTheDocument();
    });

    it('promotes a compact attention action inside the contextual destinations', () => {
        renderWithProviders(
            <SidebarContent
                attentionAction={{
                    to: '/plan/master',
                    label: 'Continue Plan Work (2 remaining)',
                }}
            />,
            { initialEntries: ['/plan'] },
        );

        expect(screen.getByRole('link', { name: 'Continue Plan Work (2 remaining)' }))
            .toHaveAttribute('href', '/plan/master');
    });

    it('keeps Delivery views inside Delivery without planning context', () => {
        renderWithProviders(<AppSidebar />, { initialEntries: ['/tasks'] });

        expect(screen.getByRole('link', { name: 'Tasks' })).toHaveAttribute('aria-current', 'page');
        expect(screen.queryByText('Planning summary')).not.toBeInTheDocument();
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
        expect(screen.getByLabelText('1 saved view')).toBeVisible();
    });

    it('pins a selected saved view beyond the visible limit and announces overflow', async () => {
        const crowdedViews = crowdedSystemViews();
        savedViewServiceMock.getAll.mockImplementation(({ view_type }: { view_type: string }) => (
            Promise.resolve(view_type === 'tasks' ? crowdedViews : [])
        ));

        renderWithProviders(<AppSidebar />, { initialEntries: ['/tasks?view=106'] });

        const selected = await screen.findByRole('link', { name: 'Queue view 7' });
        expect(selected).toHaveAttribute('aria-current', 'page');
        expect(screen.getByLabelText('7 saved views')).toHaveTextContent('5+');
    });

    it('opens a bounded, searchable saved-view browser', async () => {
        const crowdedViews = crowdedSystemViews(10);
        savedViewServiceMock.getAll.mockImplementation(({ view_type }: { view_type: string }) => (
            Promise.resolve(view_type === 'tasks' ? crowdedViews : [])
        ));
        const { user } = renderWithProviders(<AppSidebar />, { initialEntries: ['/tasks'] });

        await user.click(screen.getByText('Views'));
        const viewAll = await screen.findByRole('button', { name: 'Browse 10 saved views' });
        expect(screen.queryByRole('link', { name: 'Queue view 6' })).not.toBeInTheDocument();
        expect(screen.getByLabelText('10 saved views')).toHaveTextContent('5+');

        await user.click(viewAll);
        expect(screen.getByRole('searchbox', { name: 'Search saved views' })).toHaveFocus();
        expect(screen.getByRole('heading', { name: 'Tasks' })).toBeVisible();
        expect(screen.getByRole('link', { name: 'Queue view 8' })).toBeVisible();
        expect(screen.queryByRole('link', { name: 'Queue view 9' })).not.toBeInTheDocument();
        expect(screen.getByText(/Showing the first 8 of 10 matches/)).toBeVisible();

        await user.type(screen.getByRole('searchbox', { name: 'Search saved views' }), '10');
        expect(screen.getByRole('link', { name: 'Queue view 10' })).toBeVisible();
        expect(screen.queryByRole('link', { name: 'Queue view 8' })).not.toBeInTheDocument();
        expect(screen.getByRole('button', { name: 'Close saved view browser' }))
            .toHaveAttribute('aria-expanded', 'true');
        expect(screen.getByLabelText('10 saved views')).toHaveTextContent('10');
    });

    it('keeps successful saved-view groups browsable when another group fails', async () => {
        savedViewServiceMock.getAll.mockImplementation(({ view_type }: { view_type: string }) => {
            if (view_type === 'tasks') return Promise.resolve(crowdedSystemViews());
            if (view_type === 'triage') return Promise.reject(new Error('offline'));
            return Promise.resolve([]);
        });
        const { user } = renderWithProviders(<AppSidebar />, { initialEntries: ['/tasks'] });

        await user.click(screen.getByText('Views'));
        expect(await screen.findByRole('status')).toHaveTextContent(
            'Some saved views may be unavailable.',
        );
        const browse = screen.getByRole('button', { name: 'Browse 7 saved views' });
        expect(browse).toBeEnabled();
        await user.click(browse);
        expect(screen.getByRole('searchbox', { name: 'Search saved views' })).toHaveFocus();
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

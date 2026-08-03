import { describe, expect, it, vi } from 'vitest';
import { screen, within } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { AppTopNav } from './AppTopNav';

const planningReadinessMock = vi.hoisted(() => ({
    usePlanningNavigationSummary: vi.fn(),
}));

const triageServiceMock = vi.hoisted(() => ({
    getAll: vi.fn(),
}));

vi.mock('../../features/planningMasters/usePlanningNavigationSummary', () => planningReadinessMock);
vi.mock('../../services/triageService', () => ({ triageService: triageServiceMock }));
vi.mock('../../navigation/routeModules', () => ({ warmRouteModule: vi.fn() }));
vi.mock('../UserSessionBadge', () => ({ UserSessionBadge: () => null }));
vi.mock('./AppSidebar', () => ({
    SidebarContent: ({
        attentionAction,
        onNavigate,
    }: {
        attentionAction?: { label: string };
        onNavigate?: () => void;
    }) => (
        <div>
            <div data-sidebar-context-heading tabIndex={-1}>Contextual destinations</div>
            {attentionAction && (
                <button
                    type="button"
                    data-sidebar-attention-action
                    onClick={onNavigate}
                >
                    {attentionAction.label}
                </button>
            )}
        </div>
    ),
}));

describe('AppTopNav', () => {
    it('uses three workspace links and marks the active workspace for deep routes', () => {
        planningReadinessMock.usePlanningNavigationSummary.mockReturnValue({
            iterations: [],
            ready: { total: 0, done: 0 },
        });
        triageServiceMock.getAll.mockResolvedValue([]);

        renderWithProviders(<AppTopNav />, { initialEntries: ['/roadmap'] });

        expect(screen.getByRole('link', { name: 'Go to WorkChord overview' }))
            .toHaveAttribute('href', '/');

        const switcher = screen.getByRole('navigation', { name: 'Work area homes' });
        expect(within(switcher).getAllByRole('link')).toHaveLength(3);
        expect(within(switcher).getByRole('link', { name: 'Open Timeline & Planning home' }))
            .toHaveAttribute('aria-current', 'location');
    });

    it('opens a labeled navigation drawer', async () => {
        planningReadinessMock.usePlanningNavigationSummary.mockReturnValue({
            iterations: [],
            ready: { total: 0, done: 0 },
        });
        triageServiceMock.getAll.mockResolvedValue([]);

        const { user } = renderWithProviders(<AppTopNav />, { initialEntries: ['/tasks'] });
        await user.click(screen.getByRole('button', { name: 'Open navigation menu' }));

        const drawer = screen.getByRole('dialog', { name: 'Primary navigation' });
        expect(within(drawer).getByText('Navigation')).toBeInTheDocument();
        expect(within(drawer).getByRole('link', { name: 'Open Delivery Hub home' }))
            .toHaveAttribute('aria-current', 'location');
        expect(within(drawer).getByText('Choose an area here; its link always opens that area’s home.'))
            .toBeInTheDocument();
        expect(within(drawer).getByText('Contextual destinations')).toBeInTheDocument();

        await user.keyboard('{Escape}');
        expect(screen.queryByRole('dialog', { name: 'Primary navigation' })).not.toBeInTheDocument();
    });

    it('keeps the planning workspace stable and describes attention without another tab stop', () => {
        planningReadinessMock.usePlanningNavigationSummary.mockReturnValue({
            iterations: [{ id: 1 }],
            ready: { total: 6, done: 4 },
        });
        triageServiceMock.getAll.mockResolvedValue([]);

        renderWithProviders(<AppTopNav />, { initialEntries: ['/roadmap'] });

        const switcher = screen.getByRole('navigation', { name: 'Work area homes' });
        const planningHome = within(switcher).getByRole('link', {
            name: 'Open Timeline & Planning home',
        });
        expect(planningHome).toHaveAttribute('href', '/plan');
        expect(planningHome).toHaveAccessibleDescription(
            'Timeline & Planning needs attention: 2 Plan Work checkpoint(s) remain.',
        );
        expect(planningHome).toHaveTextContent('2');
        expect(within(switcher).getAllByRole('link')).toHaveLength(3);
    });

    it('labels unavailable planning attention on the stable workspace home', () => {
        planningReadinessMock.usePlanningNavigationSummary.mockReturnValue({
            iterations: [{ id: 1 }],
            ready: { total: 6, done: 0 },
            isReadinessError: true,
        });
        triageServiceMock.getAll.mockResolvedValue([]);

        renderWithProviders(<AppTopNav />, { initialEntries: ['/roadmap'] });

        const planningLink = screen.getByRole('link', {
            name: 'Open Timeline & Planning home',
        });
        expect(planningLink).toHaveAttribute('href', '/plan');
        expect(planningLink).toHaveAccessibleDescription(
            'Plan Work readiness could not be loaded. Open Plan Work to retry.',
        );
    });

    it('does not announce placeholder planning attention while readiness is loading', () => {
        planningReadinessMock.usePlanningNavigationSummary.mockReturnValue({
            iterations: [{ id: 1 }],
            ready: { total: 6, done: 1 },
            isReadinessLoading: true,
        });
        triageServiceMock.getAll.mockResolvedValue([]);

        renderWithProviders(<AppTopNav />, { initialEntries: ['/roadmap'] });

        const planningLink = screen.getByRole('link', {
            name: 'Open Timeline & Planning home',
        });
        expect(planningLink).toHaveAccessibleDescription(
            'Open Timeline & Planning home — Readiness, schedules, roadmaps, periods, and calendars.',
        );
        expect(planningLink).not.toHaveAccessibleDescription(
            expect.stringContaining('checkpoint'),
        );
        expect(planningLink).not.toHaveTextContent('5');
    });

    it('keeps the drawer open and focuses contextual attention after switching workspaces', async () => {
        planningReadinessMock.usePlanningNavigationSummary.mockReturnValue({
            iterations: [{ id: 1 }],
            ready: { total: 6, done: 4 },
        });
        triageServiceMock.getAll.mockResolvedValue([]);

        const { user } = renderWithProviders(<AppTopNav />, { initialEntries: ['/tasks'] });
        await user.click(screen.getByRole('button', { name: 'Open navigation menu' }));

        const drawer = screen.getByRole('dialog', { name: 'Primary navigation' });
        await user.click(within(drawer).getByRole('link', {
            name: 'Open Timeline & Planning home',
        }));

        expect(drawer).toBeInTheDocument();
        expect(within(drawer).getByRole('link', {
            name: 'Open Timeline & Planning home',
        })).toHaveAttribute('aria-current', 'location');

        const attentionAction = await within(drawer).findByRole('button', {
            name: 'Continue Plan Work (2 remaining)',
        });
        expect(attentionAction).toHaveFocus();

        await user.click(attentionAction);
        expect(screen.queryByRole('dialog', { name: 'Primary navigation' }))
            .not.toBeInTheDocument();
    });

    it('focuses the contextual heading when the switched workspace has no attention action', async () => {
        planningReadinessMock.usePlanningNavigationSummary.mockReturnValue({
            iterations: [{ id: 1 }],
            ready: { total: 6, done: 6 },
        });
        triageServiceMock.getAll.mockResolvedValue([]);

        const { user } = renderWithProviders(<AppTopNav />, { initialEntries: ['/tasks'] });
        await user.click(screen.getByRole('button', { name: 'Open navigation menu' }));

        const drawer = screen.getByRole('dialog', { name: 'Primary navigation' });
        await user.click(within(drawer).getByRole('link', {
            name: 'Open Resource & Settings home',
        }));

        expect(drawer).toBeInTheDocument();
        expect(within(drawer).getByText('Contextual destinations')).toHaveFocus();
    });
});

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
vi.mock('../UserSessionBadge', () => ({ UserSessionBadge: () => null }));
vi.mock('./AppSidebar', () => ({
    SidebarContent: () => <div>Contextual destinations</div>,
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

    it('keeps the planning workspace stable and exposes attention as a separate recovery link', async () => {
        planningReadinessMock.usePlanningNavigationSummary.mockReturnValue({
            iterations: [{ id: 1 }],
            ready: { total: 6, done: 4 },
        });
        triageServiceMock.getAll.mockResolvedValue([]);

        renderWithProviders(<AppTopNav />, { initialEntries: ['/roadmap'] });

        const switcher = screen.getByRole('navigation', { name: 'Work area homes' });
        expect(within(switcher).getByRole('link', { name: 'Open Timeline & Planning home' }))
            .toHaveAttribute('href', '/plan');

        const recoveryLink = await screen.findByRole('link', {
            name: 'Timeline & Planning needs attention: 2 Plan Work checkpoint(s) remain.',
        });
        expect(recoveryLink).toHaveAttribute('href', '/plan/master');
        expect(recoveryLink).toHaveTextContent('2');
    });

    it('labels unavailable planning attention and links to its recovery surface', async () => {
        planningReadinessMock.usePlanningNavigationSummary.mockReturnValue({
            iterations: [{ id: 1 }],
            ready: { total: 6, done: 0 },
            isReadinessError: true,
        });
        triageServiceMock.getAll.mockResolvedValue([]);

        renderWithProviders(<AppTopNav />, { initialEntries: ['/roadmap'] });

        const planningLink = await screen.findByRole('link', {
            name: 'Plan Work readiness could not be loaded. Open Plan Work to retry.',
        });
        expect(planningLink).toHaveAttribute('href', '/plan/master');
    });
});

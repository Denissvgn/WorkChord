import { describe, expect, it, vi } from 'vitest';
import { screen, within } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { AppTopNav } from './AppTopNav';

const planningReadinessMock = vi.hoisted(() => ({
    usePlanningReadiness: vi.fn(),
}));

const triageServiceMock = vi.hoisted(() => ({
    getAll: vi.fn(),
}));

vi.mock('../../features/planningMasters/usePlanningReadiness', () => planningReadinessMock);
vi.mock('../../services/triageService', () => ({ triageService: triageServiceMock }));
vi.mock('../UserSessionBadge', () => ({ UserSessionBadge: () => null }));
vi.mock('./AppSidebar', () => ({
    SidebarContent: () => <div>Contextual destinations</div>,
}));

describe('AppTopNav', () => {
    it('uses three workspace links and marks the active workspace for deep routes', () => {
        planningReadinessMock.usePlanningReadiness.mockReturnValue({
            iterations: [],
            ready: { total: 0, done: 0 },
        });
        triageServiceMock.getAll.mockResolvedValue([]);

        renderWithProviders(<AppTopNav />, { initialEntries: ['/roadmap'] });

        const switcher = screen.getByRole('navigation', { name: 'Workspace selector' });
        expect(within(switcher).getAllByRole('link')).toHaveLength(3);
        expect(within(switcher).getByRole('link', { name: 'Timeline & Planning' }))
            .toHaveAttribute('aria-current', 'location');
    });

    it('opens a labeled navigation drawer', async () => {
        planningReadinessMock.usePlanningReadiness.mockReturnValue({
            iterations: [],
            ready: { total: 0, done: 0 },
        });
        triageServiceMock.getAll.mockResolvedValue([]);

        const { user } = renderWithProviders(<AppTopNav />, { initialEntries: ['/tasks'] });
        await user.click(screen.getByRole('button', { name: 'Open navigation menu' }));

        const drawer = screen.getByRole('dialog', { name: 'Primary navigation' });
        expect(within(drawer).getByText('Navigation')).toBeInTheDocument();
        expect(within(drawer).getByRole('link', { name: 'Delivery Hub' }))
            .toHaveAttribute('aria-current', 'location');
        expect(within(drawer).getByText('Contextual destinations')).toBeInTheDocument();

        await user.keyboard('{Escape}');
        expect(screen.queryByRole('dialog', { name: 'Primary navigation' })).not.toBeInTheDocument();
    });
});

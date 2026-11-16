import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, within } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { AppSidebar } from './AppSidebar';

const planningSummaryMock = vi.hoisted(() => ({
    usePlanningNavigationSummary: vi.fn(),
}));

const triageServiceMock = vi.hoisted(() => ({
    getAll: vi.fn(),
}));

vi.mock('../../features/planningMasters/usePlanningNavigationSummary', () => planningSummaryMock);
vi.mock('../../services/triageService', () => ({ triageService: triageServiceMock }));

const planSummary = (overrides: Record<string, unknown> = {}) => ({
    iterations: [{ id: 1 }],
    ready: { done: 3, total: 6, pct: 50 },
    isIterationsLoading: false,
    isIterationsError: false,
    isReadinessLoading: false,
    isReadinessError: false,
    isPlanProgressKnown: true,
    ...overrides,
});

const DESTINATION_NAMES = [
    'Overview', 'My Work', 'Triage',
    'Projects', 'Plan', 'Gantt',
    'Tasks', 'Analytics',
    'Team', 'Settings',
];

const destinationLinks = () => within(screen.getByRole('navigation', { name: 'Primary navigation' }))
    .getAllByRole('link');

describe('AppSidebar', () => {
    beforeEach(() => {
        planningSummaryMock.usePlanningNavigationSummary.mockReset();
        planningSummaryMock.usePlanningNavigationSummary.mockReturnValue(planSummary({
            ready: { done: 6, total: 6, pct: 100 },
        }));
        triageServiceMock.getAll.mockReset();
        triageServiceMock.getAll.mockResolvedValue([]);
    });

    it.each([
        '/', '/my-work', '/triage', '/projects', '/projects/7', '/roadmap', '/plan', '/plan/master',
        '/iterations', '/gantt', '/tasks', '/agent-pipeline', '/analytics', '/team',
        '/agent-team/setup', '/settings', '/calendar',
    ])('lists the same ten destinations on %s', pathname => {
        renderWithProviders(<AppSidebar />, { initialEntries: [pathname] });

        expect(destinationLinks().map(link => link.textContent?.replace(/\d+\/\d+|\d+$/, '').trim()))
            .toEqual(DESTINATION_NAMES);
    });

    it('puts the three first destinations outside any group and names the other three groups', () => {
        renderWithProviders(<AppSidebar />, { initialEntries: ['/tasks'] });

        const groups = screen.getAllByRole('group');
        expect(groups.map(group => group.getAttribute('aria-labelledby')
            && document.getElementById(group.getAttribute('aria-labelledby')!)?.textContent))
            .toEqual(['Plan', 'Deliver', 'Setup']);
        expect(groups.map(group => within(group).getAllByRole('link').map(link => link.textContent)))
            .toEqual([['Projects', 'Plan', 'Gantt'], ['Tasks', 'Analytics'], ['Team', 'Settings']]);
        const start = within(screen.getByRole('navigation', { name: 'Primary navigation' }))
            .getAllByRole('link').slice(0, 3);
        expect(start.map(link => link.textContent)).toEqual(['Overview', 'My Work', 'Triage']);
        for (const link of start) expect(link.closest('[role="group"]')).toBeNull();
    });

    it.each([
        ['/roadmap', 'Projects'],
        ['/projects/7', 'Projects'],
        ['/plan/master', 'Plan'],
        ['/iterations', 'Plan'],
        ['/agent-pipeline', 'Tasks'],
        ['/agent-team/setup', 'Team'],
        ['/calendar', 'Settings'],
    ])('marks only %s as the current page under %s', (pathname, current) => {
        renderWithProviders(<AppSidebar />, { initialEntries: [pathname] });

        const currentLinks = destinationLinks().filter(link => link.getAttribute('aria-current') === 'page');
        expect(currentLinks.map(link => link.textContent)).toEqual([current]);
    });

    it('has no work-area switcher, saved-views disclosure or iteration card', () => {
        renderWithProviders(<AppSidebar />, { initialEntries: ['/tasks'] });

        expect(screen.getAllByRole('complementary')).toHaveLength(1);
        expect(screen.queryByText('Views')).not.toBeInTheDocument();
        expect(screen.queryByText('Delivery Hub')).not.toBeInTheDocument();
        expect(screen.queryByText('Timeline & Planning')).not.toBeInTheDocument();
        expect(screen.queryByRole('button')).not.toBeInTheDocument();
        expect(document.querySelector('details')).toBeNull();
    });

    describe('counters', () => {
        const planLink = () => screen.getByRole('link', { name: 'Plan' });

        it('shows plan progress only as the counter on the Plan item, and only while the plan is below 6 of 6', () => {
            planningSummaryMock.usePlanningNavigationSummary.mockReturnValue(planSummary({
                ready: { done: 4, total: 6, pct: 67 },
            }));
            const { unmount } = renderWithProviders(<AppSidebar />, { initialEntries: ['/plan'] });

            expect(planLink()).toHaveTextContent('4/6');
            expect(planLink()).toHaveAccessibleDescription('4 of 6 plan steps complete');
            expect(screen.getAllByText('4/6')).toHaveLength(1);
            expect(destinationLinks().filter(link => link !== planLink() && /\d/.test(link.textContent ?? '')))
                .toEqual([]);
            unmount();

            planningSummaryMock.usePlanningNavigationSummary.mockReturnValue(planSummary({
                ready: { done: 6, total: 6, pct: 100 },
            }));
            renderWithProviders(<AppSidebar />, { initialEntries: ['/plan'] });

            expect(planLink()).toHaveTextContent(/^Plan$/);
            expect(screen.queryByText(/\d\/6/)).not.toBeInTheDocument();
        });

        it('shows no plan counter while progress is loading or unavailable', () => {
            for (const state of [{ isReadinessLoading: true }, { isReadinessError: true }, { isIterationsLoading: true }, { isIterationsError: true }]) {
                planningSummaryMock.usePlanningNavigationSummary.mockReturnValue(planSummary({
                    ready: { done: 1, total: 6, pct: 17 },
                    ...state,
                }));
                const { unmount } = renderWithProviders(<AppSidebar />, { initialEntries: ['/plan'] });
                expect(planLink()).toHaveTextContent(/^Plan$/);
                unmount();
            }
        });

        it('counts the requests waiting on Triage and nothing on Tasks', async () => {
            triageServiceMock.getAll.mockResolvedValue([{ id: 1 }, { id: 2 }, { id: 3 }]);
            renderWithProviders(<AppSidebar />, { initialEntries: ['/tasks'] });

            const triage = screen.getByRole('link', { name: 'Triage' });
            await within(triage).findByText('3');
            expect(triage).toHaveAccessibleDescription('3 requests waiting');
            expect(screen.getByRole('link', { name: 'Tasks' })).toHaveTextContent(/^Tasks$/);
        });

        it('shows no Triage counter when nothing waits or the count cannot be loaded', async () => {
            triageServiceMock.getAll.mockRejectedValue(new Error('offline'));
            renderWithProviders(<AppSidebar />, { initialEntries: ['/tasks'] });

            await vi.waitFor(() => expect(triageServiceMock.getAll).toHaveBeenCalled());
            expect(screen.getByRole('link', { name: 'Triage' })).toHaveTextContent(/^Triage$/);
        });
    });
});

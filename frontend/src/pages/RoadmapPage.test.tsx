import { beforeEach, describe, expect, it, vi } from 'vitest';
import { fireEvent, screen, within } from '@testing-library/react';
import { renderWithProviders } from '../test/renderWithProviders';
import RoadmapPage from './RoadmapPage';

const projectServiceMock = vi.hoisted(() => ({
    getAll: vi.fn(),
    getInitiatives: vi.fn(),
    getRoadmapMilestones: vi.fn(),
}));

vi.mock('../services/projectService', () => ({
    projectService: projectServiceMock,
}));

const project = {
    id: 1,
    name: 'Atlas',
    description: 'Coordinate the launch plan.',
    status: 'active',
    health: 'on_track',
    owner_id: null,
    owner: null,
    owner_profile_id: null,
    owner_profile: null,
    initiative_id: null,
    initiative: null,
    start_date: '2026-08-01',
    target_date: '2026-09-01',
    completed_at: null,
    sort_order: 1,
    created_at: '2026-08-01T00:00:00Z',
    updated_at: '2026-08-01T00:00:00Z',
};

const milestone = {
    id: 1,
    project_id: 1,
    name: 'Launch',
    description: null,
    target_date: '2026-08-20',
    completed_at: null,
    sort_order: 1,
    status: 'planned',
    created_at: '2026-08-01T00:00:00Z',
    updated_at: '2026-08-01T00:00:00Z',
};

describe('RoadmapPage', () => {
    beforeEach(() => {
        projectServiceMock.getAll.mockReset();
        projectServiceMock.getInitiatives.mockReset();
        projectServiceMock.getRoadmapMilestones.mockReset();

        projectServiceMock.getAll.mockResolvedValue([project]);
        projectServiceMock.getInitiatives.mockResolvedValue([]);
        projectServiceMock.getRoadmapMilestones.mockResolvedValue({
            items: [milestone],
            next_cursor: null,
        });
    });

    it('keeps filters in a labeled drawer and exposes active-filter recovery', async () => {
        const { user } = renderWithProviders(<RoadmapPage />, {
            initialEntries: ['/roadmap'],
        });

        expect(await screen.findByRole('heading', { name: 'Timeline' })).toBeVisible();
        expect(screen.queryByRole('dialog', { name: 'Filters' })).not.toBeInTheDocument();
        expect(screen.queryByLabelText('Status')).not.toBeInTheDocument();

        const filterTrigger = screen.getByRole('button', { name: 'Filters' });
        await user.click(filterTrigger);

        let drawer = screen.getByRole('dialog', { name: 'Filters' });
        await user.keyboard('{Escape}');

        expect(screen.queryByRole('dialog', { name: 'Filters' })).not.toBeInTheDocument();
        expect(filterTrigger).toHaveFocus();

        await user.click(filterTrigger);
        drawer = screen.getByRole('dialog', { name: 'Filters' });
        await user.selectOptions(within(drawer).getByLabelText('Status'), 'completed');

        expect(screen.getByRole('button', { name: 'Filters, 1 active filter' })).toBeInTheDocument();
        expect(within(drawer).getByRole('button', { name: 'Clear filters' })).toBeEnabled();

        await user.click(within(drawer).getByRole('button', { name: 'Close' }));

        const emptyHeading = await screen.findByRole('heading', {
            name: 'No roadmap rows match the filters',
        });
        expect(emptyHeading).toBeVisible();
        await user.click(screen.getByRole('button', {
            name: 'Remove filter: Status: Completed',
        }));

        expect(screen.getByRole('button', { name: 'Filters' })).toBeInTheDocument();
        expect(screen.getByRole('link', { name: 'Atlas' })).toBeVisible();
        expect(screen.getByText(content => content.startsWith('Scheduled from')))
            .toHaveClass('sr-only');

        const milestoneButton = screen.getByRole('button', { name: /^Launch,/ });
        expect(milestoneButton).toHaveAttribute('aria-expanded', 'false');

        await user.click(milestoneButton);

        expect(milestoneButton).toHaveAttribute('aria-expanded', 'true');
        expect(document.getElementById(milestoneButton.getAttribute('aria-controls')!))
            .toBeVisible();

        await user.keyboard('{Escape}');

        expect(milestoneButton).toHaveAttribute('aria-expanded', 'false');
        expect(projectServiceMock.getRoadmapMilestones).toHaveBeenCalledTimes(1);
    });

    it('summarizes a long active lens and reopens hidden filters on demand', async () => {
        const { user } = renderWithProviders(<RoadmapPage />, {
            initialEntries: ['/roadmap'],
        });

        await screen.findByRole('heading', { name: 'Timeline' });
        await user.click(screen.getByRole('button', { name: 'Filters' }));
        const drawer = screen.getByRole('dialog', { name: 'Filters' });
        await user.selectOptions(within(drawer).getByLabelText('Status'), 'active');
        await user.selectOptions(within(drawer).getByLabelText('Health'), 'on_track');
        await user.selectOptions(within(drawer).getByLabelText('Owner'), 'unassigned');
        await user.selectOptions(within(drawer).getByLabelText('Initiative'), 'unassigned');
        await user.click(within(drawer).getByRole('button', { name: 'Close' }));

        expect(screen.getByRole('button', {
            name: 'Remove filter: Status: Active',
        })).toBeVisible();
        expect(screen.getByRole('button', {
            name: 'Remove filter: Health: On Track',
        })).toBeVisible();
        expect(screen.getByRole('button', {
            name: 'Remove filter: Owner: Unassigned',
        })).toBeVisible();

        await user.click(screen.getByRole('button', {
            name: 'Open 1 more filter',
        }));

        expect(screen.getByRole('dialog', { name: 'Filters' })).toBeVisible();
        expect(within(screen.getByRole('dialog', { name: 'Filters' })).getByLabelText('Initiative'))
            .toHaveValue('unassigned');
    });

    it('does not clamp milestone markers outside a custom date window onto its boundaries', async () => {
        const { user } = renderWithProviders(<RoadmapPage />, {
            initialEntries: ['/roadmap'],
        });

        expect(await screen.findByRole('button', { name: /^Launch,/ })).toBeVisible();
        await user.click(screen.getByRole('button', { name: 'Filters' }));
        const drawer = screen.getByRole('dialog', { name: 'Filters' });
        fireEvent.change(within(drawer).getByLabelText('From'), {
            target: { value: '2026-08-25' },
        });
        fireEvent.change(within(drawer).getByLabelText('To'), {
            target: { value: '2026-08-30' },
        });
        await user.click(within(drawer).getByRole('button', { name: 'Close' }));

        expect(screen.getByRole('link', { name: 'Atlas' })).toBeVisible();
        expect(screen.queryByRole('button', { name: /^Launch,/ })).not.toBeInTheDocument();
    });

    it('keeps project-date bars visible when milestone markers are unavailable', async () => {
        projectServiceMock.getRoadmapMilestones.mockRejectedValue(new Error('milestone feed offline'));

        renderWithProviders(<RoadmapPage />, {
            initialEntries: ['/roadmap'],
        });

        expect(await screen.findByRole('link', { name: 'Atlas' })).toBeVisible();
        expect(await screen.findByText(content => (
            content.startsWith('Milestone markers are unavailable.')
        ))).toBeVisible();
        expect(screen.getByRole('button', { name: 'Retry' })).toBeVisible();
        expect(projectServiceMock.getRoadmapMilestones).toHaveBeenCalledTimes(1);
    });

    it('retains loaded markers and retries only the failed cursor page', async () => {
        const secondMilestone = {
            ...milestone,
            id: 2,
            name: 'Release',
            target_date: '2026-08-28',
        };
        projectServiceMock.getRoadmapMilestones
            .mockResolvedValueOnce({
                items: [milestone],
                next_cursor: milestone.id,
            })
            .mockRejectedValueOnce(new Error('second page offline'))
            .mockResolvedValueOnce({
                items: [secondMilestone],
                next_cursor: null,
            });

        const { user } = renderWithProviders(<RoadmapPage />, {
            initialEntries: ['/roadmap'],
        });

        expect(await screen.findByRole('button', { name: /^Launch,/ })).toBeVisible();
        expect(await screen.findByText(content => (
            content.startsWith('1 milestone markers and all project date ranges remain visible.')
        ))).toBeVisible();

        await user.click(screen.getByRole('button', { name: 'Retry' }));

        expect(await screen.findByRole('button', { name: /^Release,/ })).toBeVisible();
        expect(projectServiceMock.getRoadmapMilestones).toHaveBeenCalledTimes(3);
    });

    it('labels a date-window miss as incomplete while later milestone pages are unavailable', async () => {
        projectServiceMock.getRoadmapMilestones
            .mockResolvedValueOnce({
                items: [milestone],
                next_cursor: milestone.id,
            })
            .mockRejectedValueOnce(new Error('second page offline'));

        const { user } = renderWithProviders(<RoadmapPage />, {
            initialEntries: ['/roadmap'],
        });

        expect(await screen.findByText(content => (
            content.startsWith('1 milestone markers and all project date ranges remain visible.')
        ))).toBeVisible();
        await user.click(screen.getByRole('button', { name: 'Filters' }));
        const drawer = screen.getByRole('dialog', { name: 'Filters' });
        fireEvent.change(within(drawer).getByLabelText('From'), {
            target: { value: '2026-10-01' },
        });
        fireEvent.change(within(drawer).getByLabelText('To'), {
            target: { value: '2026-10-15' },
        });
        await user.click(within(drawer).getByRole('button', { name: 'Close' }));

        expect(await screen.findByRole('heading', {
            name: 'No loaded roadmap rows match this date window yet',
        })).toBeVisible();
        expect(screen.getByRole('button', { name: 'Use derived range' })).toBeVisible();
    });

    it('places every initiative on one keyboard-scrollable date axis', async () => {
        projectServiceMock.getAll.mockResolvedValue([
            { ...project, initiative_id: 10 },
            { ...project, id: 2, name: 'Beacon', initiative_id: 20 },
        ]);
        projectServiceMock.getInitiatives.mockResolvedValue([
            {
                id: 10,
                name: 'Launch program',
                description: null,
                owner_id: null,
                owner: null,
                owner_profile_id: null,
                owner_profile: null,
                health: 'on_track',
                target_date: '2026-09-01',
                created_at: '2026-08-01T00:00:00Z',
                updated_at: '2026-08-01T00:00:00Z',
            },
            {
                id: 20,
                name: 'Growth program',
                description: null,
                owner_id: null,
                owner: null,
                owner_profile_id: null,
                owner_profile: null,
                health: 'at_risk',
                target_date: '2026-10-01',
                created_at: '2026-08-01T00:00:00Z',
                updated_at: '2026-08-01T00:00:00Z',
            },
        ]);
        projectServiceMock.getRoadmapMilestones.mockResolvedValue({
            items: [],
            next_cursor: null,
        });

        renderWithProviders(<RoadmapPage />, {
            initialEntries: ['/roadmap'],
        });

        const timelines = await screen.findAllByRole('region', {
            name: 'Portfolio timeline, horizontal scroll',
        });
        expect(timelines).toHaveLength(1);
        expect(timelines[0]).toHaveAttribute('tabindex', '0');
        expect(within(timelines[0]).getByRole('heading', { name: 'Launch program' })).toBeVisible();
        expect(within(timelines[0]).getByRole('heading', { name: 'Growth program' })).toBeVisible();
        expect(within(timelines[0]).getByRole('link', { name: 'Atlas' })).toBeVisible();
        expect(within(timelines[0]).getByRole('link', { name: 'Beacon' })).toBeVisible();
    });
});

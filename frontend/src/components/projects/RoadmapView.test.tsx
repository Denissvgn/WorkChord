import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor, within } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { RoadmapView } from './RoadmapView';
import type { Initiative, Project } from '../../types/project';

const projectServiceMock = vi.hoisted(() => ({
    getRoadmapMilestones: vi.fn(),
}));

vi.mock('../../services/projectService', () => ({
    projectService: projectServiceMock,
}));

const project = {
    id: 1,
    name: 'Atlas',
    description: null,
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
} as unknown as Project;

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

const initiative = (id: number, name: string): Initiative => ({
    id,
    name,
    description: null,
    owner_id: null,
    owner: null,
    owner_profile_id: null,
    owner_profile: null,
    health: 'on_track',
    target_date: '2026-09-01',
    created_at: '2026-08-01T00:00:00Z',
    updated_at: '2026-08-01T00:00:00Z',
} as unknown as Initiative);

const renderView = (props: Partial<Parameters<typeof RoadmapView>[0]> = {}) => renderWithProviders(
    <RoadmapView
        projects={[project]}
        initiatives={[]}
        includeEmptyGroups
        window={{ from: '', to: '' }}
        onResetWindow={vi.fn()}
        onEditInitiative={vi.fn()}
        onDeleteInitiative={vi.fn()}
        {...props}
    />,
    { initialEntries: ['/projects?view=roadmap'] },
);

describe('RoadmapView', () => {
    beforeEach(() => {
        projectServiceMock.getRoadmapMilestones.mockReset();
        projectServiceMock.getRoadmapMilestones.mockResolvedValue({ items: [milestone], next_cursor: null });
    });

    it('does not clamp milestone markers outside the window onto its boundaries', async () => {
        renderView({ window: { from: '2026-08-25', to: '2026-08-30' } });
        expect(await screen.findByRole('link', { name: 'Atlas' })).toBeVisible();
        await waitFor(() => expect(screen.queryByText(/^Loading milestone markers/)).not.toBeInTheDocument());
        expect(projectServiceMock.getRoadmapMilestones).toHaveBeenCalledTimes(1);
        expect(screen.queryByRole('button', { name: /^Launch,/ })).not.toBeInTheDocument();
    });

    it('keeps project-date bars visible when milestone markers are unavailable', async () => {
        projectServiceMock.getRoadmapMilestones.mockRejectedValue(new Error('milestone feed offline'));
        renderView();
        expect(await screen.findByRole('link', { name: 'Atlas' })).toBeVisible();
        expect(await screen.findByText(content => content.startsWith('Milestone markers are unavailable.'))).toBeVisible();
        expect(screen.getByRole('button', { name: 'Retry' })).toBeVisible();
        expect(projectServiceMock.getRoadmapMilestones).toHaveBeenCalledTimes(1);
    });

    it('retains loaded markers and retries only the failed cursor page', async () => {
        const secondMilestone = { ...milestone, id: 2, name: 'Release', target_date: '2026-08-28' };
        projectServiceMock.getRoadmapMilestones
            .mockResolvedValueOnce({ items: [milestone], next_cursor: milestone.id })
            .mockRejectedValueOnce(new Error('second page offline'))
            .mockResolvedValueOnce({ items: [secondMilestone], next_cursor: null });

        const { user } = renderView();
        expect(await screen.findByRole('button', { name: /^Launch,/ })).toBeVisible();
        await user.click(screen.getByRole('button', { name: 'Load more' }));
        expect(await screen.findByText(content => (
            content.startsWith('1 milestone marker and all project date ranges remain visible.')
        ))).toBeVisible();

        await user.click(screen.getByRole('button', { name: 'Retry' }));
        expect(await screen.findByRole('button', { name: /^Release,/ })).toBeVisible();
        expect(projectServiceMock.getRoadmapMilestones).toHaveBeenCalledTimes(3);
    });

    it('labels a window miss as incomplete while later milestone pages are missing, and offers to fit', async () => {
        projectServiceMock.getRoadmapMilestones
            .mockResolvedValueOnce({ items: [milestone], next_cursor: milestone.id })
            .mockRejectedValueOnce(new Error('second page offline'));
        const onResetWindow = vi.fn();
        const { user } = renderView({ window: { from: '2026-10-01', to: '2026-10-15' }, onResetWindow });

        expect(await screen.findByRole('heading', { name: 'No loaded roadmap rows match this date window yet' })).toBeVisible();
        await user.click(screen.getByRole('button', { name: 'Fit all' }));
        expect(onResetWindow).toHaveBeenCalledTimes(1);
    });

    it('places every initiative on one keyboard-scrollable date axis', async () => {
        projectServiceMock.getRoadmapMilestones.mockResolvedValue({ items: [], next_cursor: null });
        renderView({
            projects: [
                { ...project, initiative_id: 10 },
                { ...project, id: 2, name: 'Beacon', initiative_id: 20 },
            ],
            initiatives: [initiative(10, 'Launch program'), initiative(20, 'Growth program'), initiative(30, 'Quiet program')],
        });

        const timelines = await screen.findAllByRole('region', { name: 'Portfolio timeline, horizontal scroll' });
        expect(timelines).toHaveLength(1);
        expect(timelines[0]).toHaveAttribute('tabindex', '0');
        expect(within(timelines[0]).getByRole('heading', { name: 'Launch program' })).toBeVisible();
        expect(within(timelines[0]).getByRole('heading', { name: 'Growth program' })).toBeVisible();
        // An initiative without projects still has its header, so it can be seen and edited.
        const quiet = within(timelines[0]).getByRole('heading', { name: 'Quiet program' }).closest('section')!;
        expect(within(quiet).getByText('No projects in this initiative yet.')).toBeVisible();
        expect(within(timelines[0]).getByRole('link', { name: 'Atlas' })).toBeVisible();
        expect(within(timelines[0]).getByRole('link', { name: 'Beacon' })).toBeVisible();
    });

    it('keeps the axis for projects without dates and puts the way to date them on their track', async () => {
        projectServiceMock.getRoadmapMilestones.mockResolvedValue({ items: [], next_cursor: null });
        renderView({ projects: [{ ...project, start_date: null, target_date: null }] });
        const timeline = await screen.findByRole('region', { name: 'Portfolio timeline, horizontal scroll' });
        expect(within(timeline).getByRole('heading', { name: 'No initiative' })).toBeVisible();
        expect(within(timeline).getByText('No dates yet')).toBeVisible();
        expect(within(timeline).getByRole('button', { name: 'Set dates' })).toHaveAttribute('aria-haspopup', 'dialog');
        expect(within(timeline).getByRole('button', { name: 'Add milestone' })).toBeVisible();
        expect(within(timeline).queryByRole('link', { name: /Set project dates|Add milestone/ })).not.toBeInTheDocument();
    });
});

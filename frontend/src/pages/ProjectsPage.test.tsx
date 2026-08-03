import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, within } from '@testing-library/react';
import i18n from '../i18n/i18n';
import { renderWithProviders } from '../test/renderWithProviders';
import ProjectsPage from './ProjectsPage';

const projectServiceMock = vi.hoisted(() => ({
    getAll: vi.fn(),
    getInitiatives: vi.fn(),
    getPortfolioSummaries: vi.fn(),
    deleteInitiative: vi.fn(),
}));

const savedViewServiceMock = vi.hoisted(() => ({
    getById: vi.fn(),
}));

vi.mock('../services/projectService', () => ({
    projectService: projectServiceMock,
}));

vi.mock('../services/savedViewService', () => ({
    savedViewService: savedViewServiceMock,
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

describe('ProjectsPage', () => {
    beforeEach(() => {
        projectServiceMock.getAll.mockReset();
        projectServiceMock.getInitiatives.mockReset();
        projectServiceMock.getPortfolioSummaries.mockReset();
        projectServiceMock.deleteInitiative.mockReset();
        savedViewServiceMock.getById.mockReset();

        projectServiceMock.getAll.mockResolvedValue([project]);
        projectServiceMock.getInitiatives.mockResolvedValue([]);
        projectServiceMock.getPortfolioSummaries.mockResolvedValue([{
            project_id: project.id,
            total_tasks: 0,
            completed_tasks: 0,
            total_effort_days: 0,
            remaining_effort_days: 0,
            blocked_tasks: 0,
            overdue_tasks: 0,
            target_date_risk: 'on_track',
        }]);
    });

    it('offers filter recovery instead of project creation when a view has no matches', async () => {
        const { user } = renderWithProviders(<ProjectsPage />, {
            initialEntries: ['/projects'],
        });

        expect(await screen.findByRole('link', { name: 'Atlas' })).toBeVisible();

        await user.type(
            screen.getByRole('textbox', { name: 'Search projects' }),
            'missing',
        );

        const filteredEmptyHeading = screen.getByRole('heading', {
            name: 'No projects match these filters',
        });
        expect(filteredEmptyHeading).toBeVisible();
        expect(within(filteredEmptyHeading.closest('.inline-empty')!).getAllByRole('button'))
            .toHaveLength(1);

        await user.click(within(filteredEmptyHeading.closest('.inline-empty')!).getByRole('button', {
            name: 'Clear filters',
        }));

        expect(screen.getByRole('link', { name: 'Atlas' })).toBeVisible();
        expect(screen.queryByRole('heading', {
            name: 'No projects match these filters',
        })).not.toBeInTheDocument();
    });

    it('keeps creation as the recovery when no projects exist at all', async () => {
        projectServiceMock.getAll.mockResolvedValue([]);

        renderWithProviders(<ProjectsPage />, {
            initialEntries: ['/projects'],
        });

        expect(await screen.findByRole('heading', { name: 'No projects found' }))
            .toBeVisible();
        expect(screen.queryByRole('button', { name: 'Clear filters' }))
            .not.toBeInTheDocument();
        expect(screen.getAllByRole('button', { name: 'New Project' })).toHaveLength(1);
    });

    it('keeps the project table primary and initiative management collapsed', async () => {
        const { user } = renderWithProviders(<ProjectsPage />, {
            initialEntries: ['/projects'],
        });

        const projectLink = await screen.findByRole('link', { name: 'Atlas' });
        const initiativesLabel = screen.getByText('Initiatives');
        const initiativesDisclosure = initiativesLabel.closest('details');

        expect(screen.getAllByRole('button', { name: 'New Project' })).toHaveLength(1);
        expect(screen.getByRole('heading', { name: 'Project portfolio' })).toBeVisible();
        expect(initiativesDisclosure).not.toHaveAttribute('open');
        expect(projectLink.compareDocumentPosition(initiativesDisclosure!))
            .toBe(Node.DOCUMENT_POSITION_FOLLOWING);
        expect(screen.getByRole('button', { name: 'New Initiative' })).not.toBeVisible();

        await user.click(initiativesLabel.closest('summary')!);

        expect(initiativesDisclosure).toHaveAttribute('open');
        expect(screen.getByRole('button', { name: 'New Initiative' })).toBeVisible();
    });

    it('names project signals and formats effort with the active locale', async () => {
        projectServiceMock.getPortfolioSummaries.mockResolvedValue([{
            project_id: project.id,
            total_tasks: 4,
            completed_tasks: 1,
            total_effort_days: 4,
            remaining_effort_days: 2.5,
            blocked_tasks: 2,
            overdue_tasks: 1,
            target_date_risk: 'at_risk',
        }]);

        renderWithProviders(<ProjectsPage />, {
            initialEntries: ['/projects'],
        });

        expect(await screen.findByText('2 blocked tasks')).toHaveClass('sr-only');
        expect(screen.getByText('1 overdue task')).toHaveClass('sr-only');
        expect(screen.getByText(new Intl.NumberFormat(i18n.language, {
            style: 'unit',
            unit: 'day',
            unitDisplay: 'narrow',
            maximumFractionDigits: 1,
        }).format(2.5))).toBeVisible();
        expect(projectServiceMock.getPortfolioSummaries).toHaveBeenCalledTimes(1);
        expect(screen.queryByText('Loading project summary...')).not.toBeInTheDocument();
    });

    it('keeps the project table usable when portfolio signals are unavailable', async () => {
        projectServiceMock.getPortfolioSummaries.mockRejectedValue(new Error('summary service offline'));

        renderWithProviders(<ProjectsPage />, {
            initialEntries: ['/projects'],
        });

        expect(await screen.findByRole('link', { name: 'Atlas' })).toBeVisible();
        expect(await screen.findByText(
            'Portfolio signals are unavailable. Project details and filters are still available.',
        )).toBeVisible();
        expect(screen.getByRole('columnheader', { name: 'Tasks' })).toBeVisible();
        expect(projectServiceMock.getPortfolioSummaries).toHaveBeenCalledTimes(1);
    });
});

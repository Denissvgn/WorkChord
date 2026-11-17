import { beforeEach, describe, expect, it, vi } from 'vitest';
import { render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QueryClientProvider } from '@tanstack/react-query';
import { createMemoryRouter, RouterProvider, useLocation } from 'react-router-dom';
import { addDays, format } from 'date-fns';
import i18n from '../i18n/i18n';
import { ToastProvider } from '../components/feedback/ToastProvider';
import { LegacyRedirect } from '../navigation/LegacyRedirect';
import { expectPageChrome } from '../test/pageChrome';
import { createTestQueryClient, renderWithProviders } from '../test/renderWithProviders';
import ProjectsPage from './ProjectsPage';

const projectServiceMock = vi.hoisted(() => ({
    getAll: vi.fn(),
    getInitiatives: vi.fn(),
    getPortfolioSummaries: vi.fn(),
    deleteInitiative: vi.fn(),
    getRoadmapMilestones: vi.fn(),
    update: vi.fn(),
    createMilestone: vi.fn(),
    deleteMilestone: vi.fn(),
}));

const savedViewServiceMock = vi.hoisted(() => ({
    getById: vi.fn(),
}));

const planningInputServiceMock = vi.hoisted(() => ({
    readInitial: vi.fn(),
}));

vi.mock('../services/projectService', () => ({
    projectService: projectServiceMock,
}));

vi.mock('../services/savedViewService', () => ({
    savedViewService: savedViewServiceMock,
}));

vi.mock('../services/planningInputService', () => ({
    planningInputService: planningInputServiceMock,
}));

vi.mock('../services/teamService', () => ({
    teamService: { getProfiles: vi.fn().mockResolvedValue([]) },
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

const ownerProfile = {
    id: 7,
    display_name: 'Rina Ito',
    position: 'Product lead',
};

const launchInitiative = {
    id: 10,
    name: 'Launch program',
    description: null,
    owner_id: null,
    owner: null,
    owner_profile_id: 7,
    owner_profile: ownerProfile,
    health: 'at_risk',
    target_date: '2026-09-30',
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

const LocationProbe = () => {
    const location = useLocation();
    return <output data-testid="location">{location.pathname + location.search}</output>;
};

const renderPage = (path: string) => renderWithProviders(<><ProjectsPage /><LocationProbe /></>, { initialEntries: [path] });
const currentLocation = () => screen.getByTestId('location').textContent ?? '';

describe('ProjectsPage', () => {
    beforeEach(() => {
        Object.values(projectServiceMock).forEach(mock => mock.mockReset());
        savedViewServiceMock.getById.mockReset();
        planningInputServiceMock.readInitial.mockReset();

        projectServiceMock.getAll.mockResolvedValue([project]);
        projectServiceMock.getInitiatives.mockResolvedValue([]);
        projectServiceMock.getRoadmapMilestones.mockResolvedValue({ items: [milestone], next_cursor: null });
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
        const { user } = renderPage('/projects');

        expect(await screen.findByRole('link', { name: 'Atlas' })).toBeVisible();

        await user.type(screen.getByRole('searchbox', { name: 'Search projects' }), 'missing');

        const filteredEmptyHeading = screen.getByRole('heading', { name: 'Nothing matches the filters' });
        expect(filteredEmptyHeading).toBeVisible();
        expect(within(filteredEmptyHeading.closest('.inline-empty')!).getAllByRole('button')).toHaveLength(1);

        await user.click(within(filteredEmptyHeading.closest('.inline-empty')!).getByRole('button', { name: 'Clear filters' }));

        expect(screen.getByRole('link', { name: 'Atlas' })).toBeVisible();
        expect(screen.queryByRole('heading', { name: 'Nothing matches the filters' })).not.toBeInTheDocument();
    });

    it('keeps creation as the recovery when no projects exist at all', async () => {
        projectServiceMock.getAll.mockResolvedValue([]);

        renderPage('/projects');

        expect(await screen.findByRole('heading', { name: 'No projects yet' })).toBeVisible();
        expect(screen.queryByRole('button', { name: 'Clear filters' })).not.toBeInTheDocument();
        expect(screen.getAllByRole('button', { name: 'New project' })).toHaveLength(1);
    });

    it('leads with New project and offers New initiative as the one supporting action', async () => {
        renderPage('/projects');
        await screen.findByRole('link', { name: 'Atlas' });

        const header = screen.getByTestId('page-header');
        expect(within(header).getByRole('button', { name: 'New project' })).toHaveClass('btn-primary');
        expect(within(header).getByRole('button', { name: 'New initiative' })).toHaveClass('btn-secondary');
        expect(screen.getAllByTestId('page-toolbar')).toHaveLength(1);
        expect(screen.queryByText('Initiatives', { selector: 'strong' })).not.toBeInTheDocument();
        expect(document.querySelector('details')).toBeNull();
    });

    it.each(['/projects', '/projects?view=roadmap'])('builds %s from the shared page parts', async path => {
        projectServiceMock.getAll.mockResolvedValue([
            { ...project, initiative_id: 10, initiative: launchInitiative },
            { ...project, id: 2, name: 'Beacon', start_date: null, target_date: null },
        ]);
        projectServiceMock.getInitiatives.mockResolvedValue([launchInitiative]);
        const { container } = renderPage(path);
        await screen.findByRole('link', { name: 'Beacon' });
        await waitFor(() => expect(screen.queryByText(/^Loading/)).not.toBeInTheDocument());
        expectPageChrome(container);
    });

    it('never says "No risk flags" while a project health is unassessed', async () => {
        projectServiceMock.getAll.mockResolvedValue([project, { ...project, id: 2, name: 'Beacon', health: 'unknown' }]);
        renderPage('/projects');
        expect(await screen.findByText('1 project not assessed')).toBeInTheDocument();
        expect(screen.queryByText('No risk flags')).not.toBeInTheDocument();
    });

    it('filters the table to the projects a portfolio count names', async () => {
        projectServiceMock.getAll.mockResolvedValue([project, { ...project, id: 2, name: 'Beacon', health: 'at_risk' }, { ...project, id: 3, name: 'Comet', health: 'off_track' }]);
        const { user } = renderPage('/projects');
        const count = await screen.findByRole('button', { name: /2 at risk/i });
        await user.click(count);
        expect(count).toHaveAttribute('aria-pressed', 'true');
        expect(screen.queryByRole('link', { name: 'Atlas' })).not.toBeInTheDocument();
        expect(screen.getByRole('link', { name: 'Beacon' })).toBeInTheDocument();
        expect(screen.getByRole('link', { name: 'Comet' })).toBeInTheDocument();
        await user.click(count);
        expect(await screen.findByRole('link', { name: 'Atlas' })).toBeInTheDocument();
    });

    it('shows the at-risk count as a removable Health chip in the shared filter bar', async () => {
        projectServiceMock.getAll.mockResolvedValue([project, { ...project, id: 2, name: 'Beacon', health: 'at_risk' }, { ...project, id: 3, name: 'Comet', health: 'off_track' }]);
        const { user } = renderPage('/projects');
        await user.click(await screen.findByRole('button', { name: /2 at risk/i }));

        expect(screen.getByRole('combobox', { name: 'Health' })).toHaveValue('at_risk_or_off_track');
        const chips = within(screen.getByRole('list', { name: 'Active filters' }));
        expect(chips.getByText('Health: At risk or off track')).toBeVisible();
        expect(currentLocation()).toContain('attention=at_risk');

        // The chip removes just that condition.
        await user.click(chips.getByRole('button', { name: 'Remove filter Health: At risk or off track' }));
        expect(await screen.findByRole('link', { name: 'Atlas' })).toBeInTheDocument();
        expect(screen.getByRole('button', { name: /2 at risk/i })).toHaveAttribute('aria-pressed', 'false');
        expect(screen.queryByRole('list', { name: 'Active filters' })).not.toBeInTheDocument();
        expect(currentLocation()).not.toContain('attention=');

        // Choosing one health replaces it, so the shown chip is always the applied filter.
        await user.selectOptions(screen.getByRole('combobox', { name: 'Health' }), 'at_risk_or_off_track');
        await user.selectOptions(screen.getByRole('combobox', { name: 'Health' }), 'off_track');
        expect(currentLocation()).not.toContain('attention=');
        expect(within(screen.getByRole('list', { name: 'Active filters' })).getByText('Health: Off track')).toBeVisible();
        expect(screen.getByRole('link', { name: 'Comet' })).toBeInTheDocument();
        expect(screen.queryByRole('link', { name: 'Beacon' })).not.toBeInTheDocument();
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

        renderPage('/projects');

        expect(await screen.findByText('2 tasks blocked or waiting on dependencies')).toHaveClass('sr-only');
        expect(screen.getByText('1 overdue task')).toHaveClass('sr-only');
        expect(screen.getByText(new Intl.NumberFormat(i18n.language, {
            style: 'unit',
            unit: 'day',
            unitDisplay: 'narrow',
            maximumFractionDigits: 1,
        }).format(2.5))).toBeVisible();
        expect(projectServiceMock.getPortfolioSummaries).toHaveBeenCalledTimes(1);
        expect(screen.queryByText('Loading project summary…')).not.toBeInTheDocument();
    });

    it('keeps the project table usable when portfolio signals are unavailable', async () => {
        projectServiceMock.getPortfolioSummaries.mockRejectedValue(new Error('summary service offline'));

        renderPage('/projects');

        expect(await screen.findByRole('link', { name: 'Atlas' })).toBeVisible();
        expect(await screen.findByText(
            'Portfolio signals are unavailable. Project details and filters are still available.',
        )).toBeVisible();
        expect(screen.getByRole('columnheader', { name: 'Tasks' })).toBeVisible();
        expect(projectServiceMock.getPortfolioSummaries).toHaveBeenCalledTimes(1);
    });

    it('fits by merging health into signals, sorts by column, and keeps actions in a pinned row menu', async () => {
        projectServiceMock.getAll.mockResolvedValue([project, { ...project, id: 2, name: 'Beacon', health: 'at_risk', target_date: '2026-08-15' }]);
        const { user } = renderPage('/projects');
        const table = await screen.findByRole('region', { name: 'Projects table' });
        expect(table).toHaveAttribute('tabindex', '0');
        expect(within(table).queryByRole('columnheader', { name: /^Health$/ })).toBeNull();
        expect(within(table).queryByRole('columnheader', { name: /^Initiative$/ })).toBeNull();
        const rows = () => screen.getAllByRole('link').filter(link => ['Atlas', 'Beacon'].includes(link.textContent ?? '')).map(link => link.textContent);
        expect(rows()).toEqual(['Atlas', 'Beacon']);
        await user.click(screen.getByRole('button', { name: /^Target/ }));
        expect(rows()).toEqual(['Beacon', 'Atlas']);
        expect(within(table).getByRole('columnheader', { name: /Target/ })).toHaveAttribute('aria-sort', 'ascending');
        expect(screen.getByRole('button', { name: 'Actions for Atlas' })).toBeInTheDocument();
    });

    it('groups projects under initiative headers with owner, health, target date and Edit in both views', async () => {
        projectServiceMock.getAll.mockResolvedValue([
            { ...project, initiative_id: 10, initiative: launchInitiative },
            { ...project, id: 2, name: 'Beacon' },
        ]);
        projectServiceMock.getInitiatives.mockResolvedValue([launchInitiative]);
        const { user } = renderPage('/projects');

        const table = await screen.findByRole('region', { name: 'Projects table' });
        const groups = within(table).getAllByRole('rowheader');
        expect(groups.map(group => within(group).getByText(/program|No initiative/).textContent))
            .toEqual(['Launch program', 'No initiative']);
        const launchHeader = groups[0];
        expect(within(launchHeader).getByText('Owner: Rina Ito')).toBeVisible();
        expect(within(launchHeader).getByText('Health: At risk')).toBeVisible();
        expect(within(launchHeader).getByText(`Target: ${format(new Date(2026, 8, 30), 'PP')}`)).toBeVisible();
        // Atlas sits under its initiative, Beacon under "No initiative".
        const atlasRow = within(table).getByRole('link', { name: 'Atlas' }).closest('tbody')!;
        expect(within(atlasRow).getByText('Launch program')).toBeVisible();
        const beaconRow = within(table).getByRole('link', { name: 'Beacon' }).closest('tbody')!;
        expect(within(beaconRow).getByText('No initiative')).toBeVisible();
        expect(within(groups[1]).queryByRole('button', { name: /Edit initiative/ })).not.toBeInTheDocument();

        await user.click(within(launchHeader).getByRole('button', { name: 'Edit initiative Launch program' }));
        const drawer = await screen.findByRole('dialog', { name: 'Edit initiative' });
        expect(within(drawer).getByRole('textbox', { name: /Initiative name/ })).toHaveValue('Launch program');
        await user.click(within(drawer).getByRole('button', { name: 'Close' }));

        await user.click(screen.getByRole('button', { name: 'Roadmap' }));
        const timeline = await screen.findByRole('region', { name: 'Portfolio timeline, horizontal scroll' });
        const launchSection = within(timeline).getByRole('heading', { name: 'Launch program' }).closest('section')!;
        expect(within(launchSection).getByText('Owner: Rina Ito')).toBeVisible();
        expect(within(launchSection).getByText('Health: At risk')).toBeVisible();
        expect(within(launchSection).getByText(`Target: ${format(new Date(2026, 8, 30), 'PP')}`)).toBeVisible();
        expect(within(launchSection).getByRole('link', { name: 'Atlas' })).toBeVisible();
        const unassignedSection = within(timeline).getByRole('heading', { name: 'No initiative' }).closest('section')!;
        expect(within(unassignedSection).getByRole('link', { name: 'Beacon' })).toBeVisible();

        await user.click(within(launchSection).getByRole('button', { name: 'Edit initiative Launch program' }));
        expect(await screen.findByRole('dialog', { name: 'Edit initiative' })).toBeVisible();
    });

    it('shows initiatives with Edit in both views while there are no projects yet', async () => {
        projectServiceMock.getAll.mockResolvedValue([]);
        projectServiceMock.getPortfolioSummaries.mockResolvedValue([]);
        projectServiceMock.getRoadmapMilestones.mockResolvedValue({ items: [], next_cursor: null });
        projectServiceMock.getInitiatives.mockResolvedValue([launchInitiative]);
        const { user } = renderPage('/projects');

        const table = await screen.findByRole('region', { name: 'Projects table' });
        const [launchHeader] = within(table).getAllByRole('rowheader');
        expect(within(launchHeader).getByText('Launch program')).toBeVisible();
        expect(within(launchHeader).getByText('Owner: Rina Ito')).toBeVisible();
        expect(within(launchHeader).getByText('Health: At risk')).toBeVisible();
        expect(within(table).getByText('No projects in this initiative yet.')).toBeVisible();
        expect(screen.queryByRole('heading', { name: 'No projects yet' })).not.toBeInTheDocument();
        // Without the empty state, New project stays in the header.
        expect(within(screen.getByTestId('page-header')).getByRole('button', { name: 'New project' })).toHaveClass('btn-primary');

        await user.click(within(launchHeader).getByRole('button', { name: 'Edit initiative Launch program' }));
        const drawer = await screen.findByRole('dialog', { name: 'Edit initiative' });
        await user.click(within(drawer).getByRole('button', { name: 'Close' }));

        await user.click(screen.getByRole('button', { name: 'Roadmap' }));
        const timeline = await screen.findByRole('region', { name: 'Portfolio timeline, horizontal scroll' });
        const launchSection = within(timeline).getByRole('heading', { name: 'Launch program' }).closest('section')!;
        expect(within(launchSection).getByText('Owner: Rina Ito')).toBeVisible();
        expect(within(launchSection).getByText('No projects in this initiative yet.')).toBeVisible();
        await user.click(within(launchSection).getByRole('button', { name: 'Edit initiative Launch program' }));
        expect(await screen.findByRole('dialog', { name: 'Edit initiative' })).toBeVisible();
    });

    it('keeps the search text and the active filters when switching between List and Roadmap', async () => {
        projectServiceMock.getAll.mockResolvedValue([
            project,
            { ...project, id: 2, name: 'Atlas mobile', status: 'planned' },
            { ...project, id: 3, name: 'Beacon' },
        ]);
        const { user } = renderPage('/projects');
        await screen.findByRole('link', { name: 'Beacon' });

        await user.type(screen.getByRole('searchbox', { name: 'Search projects' }), 'atlas');
        await user.selectOptions(screen.getByRole('combobox', { name: 'Status' }), 'active');
        await user.selectOptions(screen.getByRole('combobox', { name: 'Health' }), 'on_track');

        const expectFiltered = () => {
            expect(screen.getByRole('searchbox', { name: 'Search projects' })).toHaveValue('atlas');
            expect(screen.getByRole('combobox', { name: 'Status' })).toHaveValue('active');
            expect(screen.getByRole('combobox', { name: 'Health' })).toHaveValue('on_track');
            const chips = within(screen.getByRole('list', { name: 'Active filters' }));
            expect(chips.getByText('Status: Active')).toBeVisible();
            expect(chips.getByText('Health: On track')).toBeVisible();
            expect(screen.getByRole('link', { name: 'Atlas' })).toBeVisible();
            expect(screen.queryByRole('link', { name: 'Atlas mobile' })).not.toBeInTheDocument();
            expect(screen.queryByRole('link', { name: 'Beacon' })).not.toBeInTheDocument();
        };
        expectFiltered();

        await user.click(screen.getByRole('button', { name: 'Roadmap' }));
        expect(await screen.findByRole('region', { name: 'Portfolio timeline, horizontal scroll' })).toBeVisible();
        expect(screen.getByRole('button', { name: 'Roadmap' })).toHaveAttribute('aria-pressed', 'true');
        expectFiltered();
        expect(currentLocation()).toContain('view=roadmap');

        await user.click(screen.getByRole('button', { name: 'List' }));
        expect(await screen.findByRole('region', { name: 'Projects table' })).toBeVisible();
        expect(screen.getByRole('button', { name: 'List' })).toHaveAttribute('aria-pressed', 'true');
        expectFiltered();
    });

    it('dates a project without dates from the Roadmap view in two clicks without leaving the page', async () => {
        const undated = { ...project, start_date: null, target_date: null };
        projectServiceMock.getAll.mockResolvedValue([undated]);
        projectServiceMock.getRoadmapMilestones.mockResolvedValue({ items: [], next_cursor: null });
        planningInputServiceMock.readInitial.mockResolvedValue({
            kind: 'project', resource_id: 1, complete: true, resource: undated, expected_revisions: { 1: 4 },
        });
        const start = format(new Date(), 'yyyy-MM-dd');
        const target = format(addDays(new Date(), 28), 'yyyy-MM-dd');
        projectServiceMock.update.mockImplementation(async () => {
            projectServiceMock.getAll.mockResolvedValue([{ ...undated, start_date: start, target_date: target }]);
            return { ...undated, start_date: start, target_date: target };
        });
        const { user } = renderPage('/projects?view=roadmap');
        const timeline = await screen.findByRole('region', { name: 'Portfolio timeline, horizontal scroll' });
        expect(within(timeline).getByText('No dates yet')).toBeVisible();

        // Click one opens the popover with the dates proposed.
        await user.click(within(timeline).getByRole('button', { name: 'Set dates' }));
        const popover = screen.getByRole('dialog', { name: 'Set dates for Atlas' });
        expect(await within(popover).findByLabelText('Start date')).toHaveValue(start);
        expect(within(popover).getByLabelText('Target date')).toHaveValue(target);

        // Click two saves them.
        await user.click(within(popover).getByRole('button', { name: 'Save dates' }));

        await waitFor(() => expect(projectServiceMock.update).toHaveBeenCalledWith(1, { start_date: start, target_date: target }, { 1: 4 }));
        await waitFor(() => expect(screen.queryByRole('dialog', { name: 'Set dates for Atlas' })).not.toBeInTheDocument());
        expect(await within(timeline).findByText(content => content.startsWith('Scheduled from'))).toHaveClass('sr-only');
        expect(within(timeline).queryByRole('button', { name: 'Set dates' })).not.toBeInTheDocument();
        expect(currentLocation()).toBe('/projects?view=roadmap');
    });

    it('keeps Set dates and Add milestone on a project without dates whose milestones place it on the timeline', async () => {
        const undated = { ...project, start_date: null, target_date: null };
        const later = { ...milestone, id: 2, name: 'Review', target_date: '2026-09-10' };
        projectServiceMock.getAll.mockResolvedValue([undated]);
        projectServiceMock.getRoadmapMilestones.mockResolvedValue({ items: [milestone, later], next_cursor: null });
        planningInputServiceMock.readInitial.mockResolvedValue({
            kind: 'project', resource_id: 1, complete: true, resource: undated, expected_revisions: { 1: 4 },
        });
        projectServiceMock.update.mockResolvedValue({ ...undated, start_date: '2026-08-20', target_date: '2026-09-10' });
        const { user } = renderPage('/projects?view=roadmap');
        const timeline = await screen.findByRole('region', { name: 'Portfolio timeline, horizontal scroll' });

        // The milestones draw the row, and the project can still be dated.
        expect(await within(timeline).findByRole('button', { name: /^Launch,/ })).toBeInTheDocument();
        expect(within(timeline).getByText('Milestone-derived range')).toBeVisible();
        expect(within(timeline).queryByText('No dates yet')).not.toBeInTheDocument();
        expect(within(timeline).getByRole('button', { name: 'Add milestone' })).toBeVisible();

        // Two clicks: the popover proposes the span the milestones draw, and saving keeps it.
        await user.click(within(timeline).getByRole('button', { name: 'Set dates' }));
        const popover = screen.getByRole('dialog', { name: 'Set dates for Atlas' });
        expect(await within(popover).findByLabelText('Start date')).toHaveValue('2026-08-20');
        expect(within(popover).getByLabelText('Target date')).toHaveValue('2026-09-10');
        await user.click(within(popover).getByRole('button', { name: 'Save dates' }));
        await waitFor(() => expect(projectServiceMock.update).toHaveBeenCalledWith(
            1, { start_date: '2026-08-20', target_date: '2026-09-10' }, { 1: 4 },
        ));
        expect(currentLocation()).toBe('/projects?view=roadmap');

        await user.click(within(timeline).getByRole('button', { name: 'Add milestone' }));
        expect(screen.getByRole('dialog', { name: 'Add milestone' })).toBeVisible();
    });

    it('adds a milestone to a project without dates in a short modal on the same page', async () => {
        projectServiceMock.getAll.mockResolvedValue([{ ...project, start_date: null, target_date: null }]);
        projectServiceMock.getRoadmapMilestones.mockResolvedValue({ items: [], next_cursor: null });
        projectServiceMock.createMilestone.mockResolvedValue({ ...milestone, name: 'Beta' });
        const { user } = renderPage('/projects?view=roadmap');
        const timeline = await screen.findByRole('region', { name: 'Portfolio timeline, horizontal scroll' });

        await user.click(within(timeline).getByRole('button', { name: 'Add milestone' }));
        const modal = screen.getByRole('dialog', { name: 'Add milestone' });
        expect(within(modal).getAllByRole('textbox')).toHaveLength(1);
        await user.type(within(modal).getByRole('textbox', { name: /Milestone name/ }), 'Beta');
        await user.type(within(modal).getByLabelText(/Target date/), '2026-08-20');
        await user.click(within(modal).getByRole('button', { name: 'Add milestone' }));

        await waitFor(() => expect(projectServiceMock.createMilestone).toHaveBeenCalledWith(1, {
            name: 'Beta', target_date: '2026-08-20', status: 'planned',
        }));
        await waitFor(() => expect(screen.queryByRole('dialog', { name: 'Add milestone' })).not.toBeInTheDocument());
        expect(currentLocation()).toBe('/projects?view=roadmap');
    });

    it('shows milestone markers on the timeline and sets the window from a preset', async () => {
        const { user } = renderPage('/projects?view=roadmap');
        const marker = await screen.findByRole('button', { name: /^Launch,/ });
        expect(marker).toHaveAttribute('aria-expanded', 'false');
        await user.click(marker);
        expect(marker).toHaveAttribute('aria-expanded', 'true');

        const presets = screen.getByRole('group', { name: 'Timeline window' });
        expect(within(presets).getByRole('button', { name: 'Fit all' })).toHaveAttribute('aria-pressed', 'true');
        await user.click(within(presets).getByRole('button', { name: 'This year' }));
        expect(within(presets).getByRole('button', { name: 'This year' })).toHaveAttribute('aria-pressed', 'true');
        const year = new Date().getFullYear();
        expect(currentLocation()).toContain(`from=${year}-01-01`);
        expect(currentLocation()).toContain(`to=${year}-12-31`);
    });
});

describe('the old Roadmap address', () => {
    beforeEach(() => {
        Object.values(projectServiceMock).forEach(mock => mock.mockReset());
        projectServiceMock.getAll.mockResolvedValue([
            { ...project, initiative_id: 10, initiative: launchInitiative },
            { ...project, id: 2, name: 'Beacon', status: 'planned' },
        ]);
        projectServiceMock.getInitiatives.mockResolvedValue([launchInitiative]);
        projectServiceMock.getPortfolioSummaries.mockResolvedValue([]);
        projectServiceMock.getRoadmapMilestones.mockResolvedValue({ items: [], next_cursor: null });
    });

    it('opens the Roadmap view with the same filters when /roadmap carries filter parameters', async () => {
        const router = createMemoryRouter([
            { path: '/roadmap', element: <LegacyRedirect><div>Old roadmap</div></LegacyRedirect> },
            { path: '/projects', element: <ProjectsPage /> },
        ], { initialEntries: ['/roadmap?status=active&initiative=10&q=atl'] });
        render(
            <QueryClientProvider client={createTestQueryClient()}>
                <ToastProvider><RouterProvider router={router} /></ToastProvider>
            </QueryClientProvider>,
        );

        const timeline = await screen.findByRole('region', { name: 'Portfolio timeline, horizontal scroll' });
        expect(screen.queryByText('Old roadmap')).not.toBeInTheDocument();
        expect(router.state.location.pathname).toBe('/projects');
        expect(new URLSearchParams(router.state.location.search).get('view')).toBe('roadmap');
        expect(screen.getByRole('button', { name: 'Roadmap' })).toHaveAttribute('aria-pressed', 'true');
        expect(screen.getByRole('searchbox', { name: 'Search projects' })).toHaveValue('atl');
        expect(screen.getByRole('combobox', { name: 'Status' })).toHaveValue('active');
        expect(screen.getByRole('combobox', { name: 'Initiative' })).toHaveValue('10');
        const chips = within(screen.getByRole('list', { name: 'Active filters' }));
        expect(chips.getByText('Status: Active')).toBeVisible();
        expect(chips.getByText('Initiative: Launch program')).toBeVisible();
        expect(within(timeline).getByRole('link', { name: 'Atlas' })).toBeVisible();
        expect(within(timeline).queryByRole('link', { name: 'Beacon' })).not.toBeInTheDocument();

        const user = userEvent.setup();
        await user.click(screen.getByRole('button', { name: 'Remove filter Status: Active' }));
        expect(new URLSearchParams(router.state.location.search).get('status')).toBeNull();
        expect(new URLSearchParams(router.state.location.search).get('view')).toBe('roadmap');
    });
});

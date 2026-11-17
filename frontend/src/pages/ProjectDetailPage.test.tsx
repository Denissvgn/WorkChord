import { beforeEach, describe, expect, it, vi } from 'vitest';
import { fireEvent, screen, waitFor, within } from '@testing-library/react';
import { Route, Routes, useLocation, useNavigate } from 'react-router-dom';
import { renderWithProviders } from '../test/renderWithProviders';
import ProjectDetailPage from './ProjectDetailPage';

import { Button } from '../components/common/Button';
const services = vi.hoisted(() => ({
    project: { getById: vi.fn(), getSummary: vi.fn(), getTasks: vi.fn(), getMilestones: vi.fn(), getUpdates: vi.fn(), getIterations: vi.fn(), update: vi.fn(), createMilestone: vi.fn() },
    release: { getForProject: vi.fn() },
    planning: { readInitial: vi.fn() },
    team: { getProfiles: vi.fn() },
}));
vi.mock('../services/projectService', () => ({ projectService: services.project }));
vi.mock('../services/releaseService', () => ({ releaseService: services.release }));
vi.mock('../services/planningInputService', () => ({ planningInputService: services.planning }));
vi.mock('../services/teamService', () => ({ teamService: services.team }));
// Child workflows have their own tests; this suite exercises the project frame and real inline editors.
vi.mock('../components/projects/ProjectIterationsSection', () => ({ ProjectIterationsSection: () => <h2>Project iterations</h2> }));
vi.mock('../components/projects/TimeEntriesReport', () => ({ TimeEntriesReport: () => <h2>Recorded time</h2> }));
vi.mock('../components/requestSources/RequestSourceLinksPanel', () => ({ RequestSourceLinksPanel: () => <h2>Project requests</h2> }));
vi.mock('../components/projects/ProjectForm', () => ({ ProjectForm: () => <p>Full project editor</p> }));

const project = {
    id: 1, name: 'Atlas', description: 'Deliver the launch.', status: 'active', health: 'on_track',
    owner_id: null, owner: null, owner_profile_id: null, owner_profile: null,
    start_date: null, target_date: null, sort_order: 0, created_at: '2026-08-01', updated_at: '2026-08-01',
};
const revisions = { project: 7 };
const Location = () => {
    const location = useLocation();
    const navigate = useNavigate();
    return <><output data-testid="location">{location.search}</output><Button onClick={() => navigate(-1)} variant="secondary">Back</Button><Button onClick={() => navigate('?action=add-milestone')} variant="secondary">Milestone deep link</Button></>;
};
const renderPage = (search = '') => renderWithProviders(<><Location /><Routes><Route path="/projects/:projectId" element={<ProjectDetailPage />} /></Routes></>, { initialEntries: [`/projects/1${search}`] });

beforeEach(() => {
    vi.resetAllMocks();
    services.project.getById.mockResolvedValue(project);
    services.project.getSummary.mockResolvedValue({ total_tasks: 0, milestone_groups: [], status_counts: {}, update_freshness: 'fresh', days_since_latest_update: 0 });
    for (const key of ['getTasks', 'getMilestones', 'getUpdates', 'getIterations'] as const) services.project[key].mockResolvedValue([]);
    services.release.getForProject.mockResolvedValue([]);
    services.team.getProfiles.mockResolvedValue([{ id: 9, display_name: 'Avery', kind: 'human' }]);
    services.planning.readInitial.mockResolvedValue({ resource: project, resource_id: 1, expected_revisions: revisions });
    services.project.update.mockImplementation(async (_id, data) => ({ ...project, ...data }));
});

describe('Project detail tabs', () => {
    it('shows Summary by default and gives every other tab its own URL with back navigation', async () => {
        const { user } = renderPage('?keep=scope');
        expect(await screen.findByRole('tab', { name: 'Summary', selected: true })).toBeVisible();
        expect(screen.getByRole('heading', { name: 'Latest update' })).toBeVisible();
        expect(screen.queryByRole('heading', { name: 'Linked tasks' })).not.toBeInTheDocument();
        for (const label of ['Tasks', 'Iterations', 'Releases', 'Requests', 'Updates']) {
            const tab = screen.getByRole('tab', { name: label });
            expect(tab).toHaveAttribute('href', `/projects/1?keep=scope&tab=${label.toLowerCase()}`);
            await user.click(tab);
            expect(screen.getByRole('tab', { name: label, selected: true })).toBeVisible();
            expect(screen.getByTestId('location')).toHaveTextContent(`tab=${label.toLowerCase()}`);
            expect(screen.queryByRole('heading', { name: 'Latest update' })).not.toBeInTheDocument();
        }
        expect(screen.getByRole('heading', { name: 'Update history' })).toBeVisible();
        expect(screen.getByRole('heading', { name: 'Recorded time' })).toBeVisible();
        await user.click(screen.getByRole('button', { name: 'Back' }));
        expect(screen.getByRole('tab', { name: 'Requests', selected: true })).toBeVisible();
    });

    it.each(['tasks', 'iterations', 'releases', 'requests', 'updates'])('opens the %s tab from a copied URL', async tab => {
        renderPage(`?tab=${tab}`);
        expect(await screen.findByRole('tab', { name: new RegExp(`^${tab}$`, 'i'), selected: true })).toBeVisible();
        expect(screen.getAllByRole('tabpanel')).toHaveLength(1);
    });

    it('supports arrow, Home and End keys and falls back to Summary for an unknown tab', async () => {
        const { user } = renderPage('?tab=unknown');
        const summary = await screen.findByRole('tab', { name: 'Summary', selected: true });
        summary.focus();
        await user.keyboard('{ArrowRight}');
        expect(screen.getByRole('tab', { name: 'Tasks', selected: true })).toHaveFocus();
        await user.keyboard('{End}');
        expect(screen.getByRole('tab', { name: 'Updates', selected: true })).toHaveFocus();
        await user.keyboard('{Home}');
        expect(screen.getByRole('tab', { name: 'Summary', selected: true })).toHaveFocus();
    });

    it('has exactly one primary header action and saves dates and owner inline without the edit form', async () => {
        const { user } = renderPage();
        const header = await screen.findByTestId('page-header');
        expect(header.querySelectorAll('.btn-primary')).toHaveLength(1);
        expect(within(header).getByRole('button', { name: 'Post update' })).toHaveClass('btn-primary');
        await user.click(within(header).getByRole('button', { name: /^Edit Dates:/ }));
        fireEvent.change(await screen.findByLabelText('Start date'), { target: { value: '2026-11-01' } });
        fireEvent.change(screen.getByLabelText('Target date'), { target: { value: '2026-12-01' } });
        await user.click(within(header).getByRole('button', { name: 'Save' }));
        await waitFor(() => expect(services.project.update).toHaveBeenCalledWith(1, { start_date: '2026-11-01', target_date: '2026-12-01' }, revisions));
        await user.click(within(header).getByRole('button', { name: /^Edit Owner:/ }));
        await user.selectOptions(await screen.findByRole('combobox', { name: 'Owner' }), '9');
        await user.click(within(header).getByRole('button', { name: 'Save' }));
        await waitFor(() => expect(services.project.update).toHaveBeenCalledWith(1, { owner_id: null, owner_profile_id: 9 }, revisions));
        expect(screen.queryByText('Full project editor')).not.toBeInTheDocument();
        expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
        expect(header.querySelectorAll('.btn-primary')).toHaveLength(1);
    });

    it('keeps status and health editable and retains a failed inline save for retry', async () => {
        const { user } = renderPage();
        await user.click(await screen.findByRole('button', { name: /^Edit Status:/ }));
        await user.selectOptions(await screen.findByRole('combobox', { name: 'Status' }), 'paused');
        await user.click(screen.getByRole('button', { name: 'Save' }));
        await waitFor(() => expect(services.project.update).toHaveBeenCalledWith(1, { status: 'paused' }, revisions));
        await user.click(screen.getByRole('button', { name: /^Edit Health:/ }));
        await user.selectOptions(await screen.findByRole('combobox', { name: 'Health' }), 'at_risk');
        services.project.update.mockRejectedValueOnce(new Error('Save unavailable'));
        await user.click(screen.getByRole('button', { name: 'Save' }));
        expect(await screen.findByRole('alert')).toBeVisible();
        expect(screen.getByRole('combobox', { name: 'Health' })).toHaveValue('at_risk');
        await user.click(screen.getByRole('button', { name: 'Save' }));
        await waitFor(() => expect(screen.queryByRole('combobox', { name: 'Health' })).not.toBeInTheDocument());
    });

    it('keeps edit and repeated add-milestone deep links working and uses drawers', async () => {
        const { user } = renderPage('?action=edit');
        const editor = await screen.findByRole('dialog', { name: 'Edit project' });
        expect(editor.tagName).toBe('ASIDE');
        expect(within(editor).getByText('Full project editor')).toBeVisible();
        await user.click(within(editor).getByRole('button', { name: 'Close' }));
        for (let count = 0; count < 2; count++) {
            await user.click(screen.getByRole('button', { name: 'Milestone deep link' }));
            const milestone = await screen.findByRole('dialog', { name: 'Create milestone' });
            expect(milestone.tagName).toBe('ASIDE');
            expect(screen.getByRole('tab', { name: 'Summary', selected: true })).toBeInTheDocument();
            await user.click(within(milestone).getByRole('button', { name: 'Close' }));
        }
    });
});

it('frames a missing project with a purpose and one way back', async () => {
    services.project.getById.mockResolvedValue(null);
    renderPage();
    const header = await screen.findByTestId('page-header');
    expect(within(header).getByRole('heading', { name: 'Project not found' })).toBeVisible();
    expect(within(header).getByText('Return to projects to find another project.')).toBeVisible();
    expect(within(header).getAllByRole('button')).toHaveLength(1);
});

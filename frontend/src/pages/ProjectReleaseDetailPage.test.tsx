import { beforeEach, expect, it, vi } from 'vitest';
import { screen, within } from '@testing-library/react';
import { Route, Routes } from 'react-router-dom';
import { renderWithProviders } from '../test/renderWithProviders';
import ProjectReleaseDetailPage from './ProjectReleaseDetailPage';

const services = vi.hoisted(() => ({ project: { getById: vi.fn() }, release: { getById: vi.fn(), update: vi.fn() } }));
vi.mock('../services/projectService', () => ({ projectService: services.project }));
vi.mock('../services/releaseService', () => ({ releaseService: services.release }));
vi.mock('../components/releases/ReleaseForm', () => ({ ReleaseForm: () => <p>Release editor fields</p> }));
vi.mock('../components/tasks/WorkMetricsLine', () => ({ WorkMetricsLine: () => null }));
const renderPage = (path = '/projects/1/releases/2') => renderWithProviders(<Routes><Route path="/projects/:projectId/releases/:releaseId" element={<ProjectReleaseDetailPage />} /><Route path="/projects/:projectId" element={<p>Project destination</p>} /></Routes>, { initialEntries: [path] });
beforeEach(() => {
    vi.resetAllMocks();
    services.project.getById.mockResolvedValue({ id: 1, name: 'Atlas' });
    services.release.getById.mockResolvedValue({ id: 2, project_id: 1, name: 'Launch', description: 'Release notes', status: 'planned', target_date: null, version: null, environment: null, shipped_at: null, updated_at: null, tasks: [] });
});
it('frames the release with a fixed purpose and description in the body', async () => {
    renderPage();
    const header = await screen.findByTestId('page-header');
    expect(within(header).getByRole('heading', { name: 'Launch' })).toBeVisible();
    expect(within(header).getByText('Review the release and its linked tasks.')).toBeVisible();
    expect(within(header).queryByText('Release notes')).not.toBeInTheDocument();
    expect(screen.getByText('Release notes')).toBeVisible();
    expect(header.querySelectorAll('.btn-primary')).toHaveLength(1);
});
it('frames a missing release with one way back', async () => {
    services.release.getById.mockResolvedValue(null);
    const { user } = renderPage();
    const header = await screen.findByTestId('page-header');
    expect(within(header).getByRole('heading', { name: 'Release not found' })).toBeVisible();
    expect(within(header).getByText('Return to find a release.')).toBeVisible();
    expect(within(header).getAllByRole('button')).toHaveLength(1);
    await user.click(within(header).getByRole('button', { name: 'Back to project' }));
    expect(screen.getByText('Project destination')).toBeVisible();
});
it('opens the release editor in a slide-over drawer from either edit action', async () => {
    const { user } = renderPage();
    const header = await screen.findByTestId('page-header');
    for (const button of [within(header).getByRole('button', { name: 'Edit' }), screen.getByRole('button', { name: 'Edit linked tasks' })]) {
        await user.click(button);
        const dialog = screen.getByRole('dialog', { name: 'Edit release' });
        expect(dialog.tagName).toBe('ASIDE');
        expect(dialog).toHaveClass('wc-slide-over');
        expect(within(dialog).getByText('Release editor fields')).toBeVisible();
        await user.click(within(dialog).getByRole('button', { name: 'Close' }));
    }
});

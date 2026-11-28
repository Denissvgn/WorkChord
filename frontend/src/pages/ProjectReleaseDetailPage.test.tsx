import { afterEach, beforeEach, expect, it, vi } from 'vitest';
import { screen, waitFor, within } from '@testing-library/react';
import { Route, Routes } from 'react-router-dom';
import { renderWithProviders } from '../test/renderWithProviders';
import ProjectReleaseDetailPage from './ProjectReleaseDetailPage';
import { changeAppLanguage } from '../i18n/i18n';

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
afterEach(async () => { await changeAppLanguage('en'); });

const task = (id: number, status: string, displayed_state?: string) => ({ id, title: `Task ${id}`, status, displayed_state });
const setTasks = (tasks: ReturnType<typeof task>[]) => {
    services.release.getById.mockResolvedValue({ id: 2, project_id: 1, name: 'Launch', status: 'planned', tasks });
};

it.each([
    ['closed', [task(1, 'closed'), task(2, 'closed')]],
    ['resolved', [task(1, 'resolved')]],
    ['canceled', [task(1, 'active', 'canceled')]],
    ['superseded', [task(1, 'planned', 'superseded')]],
    ['empty', []],
])('uses a neutral shipping confirmation for %s tasks', async (_label, tasks) => {
    setTasks(tasks);
    const { user } = renderPage();
    await user.click(await screen.findByRole('button', { name: 'Mark shipped' }));
    const dialog = screen.getByRole('dialog', { name: 'Ship Launch?' });
    expect(within(dialog).getByText('Shipping records the release as shipped now and adds a release entry to each linked task’s history.')).toBeVisible();
    expect(within(dialog).queryByText(/needs? resolution/)).not.toBeInTheDocument();
    expect(within(dialog).getByRole('button', { name: 'Mark shipped' })).toHaveClass('btn-primary');
});

it('shows only unresolved tasks and can confirm shipping', async () => {
    const tasks = [task(1, 'closed', 'active'), task(2, 'postponed'), task(3, 'active', 'canceled'), task(4, 'closed')];
    setTasks(tasks);
    services.release.update.mockResolvedValue({ id: 2, project_id: 1, name: 'Launch', status: 'shipped', tasks });
    const { user } = renderPage();
    await user.click(await screen.findByRole('button', { name: 'Mark shipped' }));
    const dialog = screen.getByRole('dialog', { name: 'Ship Launch?' });
    expect(within(dialog).getByText('2 linked tasks still need resolution.')).toBeVisible();
    expect(within(dialog).getByRole('button', { name: 'Mark shipped' })).toHaveClass('warning');
    await user.click(within(dialog).getByText('View unresolved tasks'));
    expect(within(dialog).getByText('Task 1 (Task #1)')).toBeVisible();
    expect(within(dialog).getByText('Task 2 (Task #2)')).toBeVisible();
    expect(within(dialog).queryByText(/Task 3/)).not.toBeInTheDocument();
    await user.click(within(dialog).getByRole('button', { name: 'Mark shipped' }));
    await waitFor(() => expect(services.release.update).toHaveBeenCalledWith(2, { status: 'shipped', shipped_at: expect.any(String) }));
});

it.each([
    ['en', 1, '1 linked task still needs resolution.'],
    ['en', 2, '2 linked tasks still need resolution.'],
    ['ru', 1, '1 связанная задача ещё требует решения.'],
    ['ru', 2, '2 связанные задачи ещё требуют решения.'],
    ['ru', 5, '5 связанных задач ещё требуют решения.'],
])('renders the %s warning for %i tasks', async (language, count, message) => {
    await changeAppLanguage(language);
    setTasks(Array.from({ length: count }, (_, index) => task(index + 1, 'active')));
    const { user } = renderPage();
    await user.click(await screen.findByRole('button', { name: language === 'ru' ? 'Отметить выпущенным' : 'Mark shipped' }));
    expect(within(screen.getByRole('dialog')).getByText(message)).toBeVisible();
});

it('renders the neutral confirmation in Russian', async () => {
    await changeAppLanguage('ru');
    const { user } = renderPage();
    await user.click(await screen.findByRole('button', { name: 'Отметить выпущенным' }));
    expect(within(screen.getByRole('dialog')).getByText('Релиз будет отмечен выпущенным сейчас, а в историю каждой связанной задачи добавится запись о релизе.')).toBeVisible();
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

it('frames a release 404 returned by the API', async () => {
    services.release.getById.mockRejectedValue({ response: { status: 404, data: { code: 'not_found', message: 'Release with id 2 not found', details: [] } } });
    renderPage();
    const header = await screen.findByTestId('page-header');
    expect(within(header).getByRole('heading', { name: 'Release not found' })).toBeVisible();
    expect(within(header).getAllByRole('button')).toHaveLength(1);
    expect(within(header).getByRole('button', { name: 'Back to project' })).toBeVisible();
});

it('frames a project 404 on the release page', async () => {
    services.project.getById.mockRejectedValue({ response: { status: 404, data: { code: 'not_found', message: 'Project with id 1 not found', details: [] } } });
    renderPage();
    const header = await screen.findByTestId('page-header');
    expect(within(header).getByRole('heading', { name: 'Release not found' })).toBeVisible();
    expect(within(header).getAllByRole('button')).toHaveLength(1);
    expect(within(header).getByRole('button', { name: 'Back to Projects' })).toBeVisible();
});

it.each(['project', 'release'] as const)('offers retry for a %s load failure', async resource => {
    services[resource].getById.mockRejectedValueOnce({ response: { status: 500, data: { code: 'error', message: 'Server unavailable', details: [] } } });
    const { user } = renderPage();
    expect(await screen.findByText('Server unavailable')).toBeVisible();
    await user.click(screen.getByRole('button', { name: 'Retry' }));
    expect(await screen.findByRole('heading', { name: 'Launch' })).toBeVisible();
});

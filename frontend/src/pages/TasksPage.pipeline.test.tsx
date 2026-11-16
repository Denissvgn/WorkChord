import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor, within } from '@testing-library/react';
import { Route, Routes, useLocation } from 'react-router-dom';
import { renderWithProviders } from '../test/renderWithProviders';
import { expectPageChrome } from '../test/pageChrome';
import { ScopeBar } from '../components/layout/ScopeBar';
import { LegacyRedirect } from '../navigation/LegacyRedirect';
import { useScopeStore } from '../features/scope/scopeStore';
import type { Task } from '../types/task';
import type { AgentPipeline } from '../types/agent';
import TasksPage from './TasksPage';
import i18n from '../i18n/i18n';

const api = vi.hoisted(() => ({ pipeline: vi.fn(), iterations: vi.fn(), task: vi.fn(), snapshot: vi.fn() }));
const access = vi.hoisted(() => ({ hasAdminKey: true }));
vi.mock('../hooks/useAdminAccess', () => ({ useAdminAccess: () => access, useKeylessReader: () => ({ workViews: true }) }));
vi.mock('../hooks/useAgentAccess', () => ({ useAgentAccess: () => ({ hasAgentKey: false }) }));
vi.mock('../services/agentService', () => ({ agentService: { getPipeline: api.pipeline, getTaskTimeline: vi.fn().mockResolvedValue({ items: [] }) } }));
vi.mock('../services/iterationService', () => ({ iterationService: { getAll: api.iterations } }));
vi.mock('../services/taskService', () => ({ taskService: { getById: api.task, lookup: vi.fn().mockResolvedValue({ items: [], has_more: false }) } }));
vi.mock('../services/savedViewService', () => ({ savedViewService: { getAll: vi.fn().mockResolvedValue([]) } }));
vi.mock('../services/labelService', () => ({ labelService: { getGroups: vi.fn().mockResolvedValue([]) } }));
vi.mock('../services/sessionService', () => ({ sessionService: { getWhoAmI: vi.fn().mockResolvedValue({ id: 3 }) } }));
vi.mock('../services/projectService', () => ({ projectService: { getAll: vi.fn().mockResolvedValue([
    { id: 3, name: 'Orchard', sort_order: 0 }, { id: 4, name: 'Harbor', sort_order: 1 },
]) } }));
vi.mock('../services/teamService', () => ({ teamService: { getByIteration: vi.fn().mockResolvedValue([]) } }));
vi.mock('../components/tasks/taskEditorSnapshot', () => ({ readTaskEditorSnapshot: api.snapshot, keepNewestTaskSnapshot: (_old: unknown, next: unknown) => next }));
vi.mock('../components/tasks/TaskReadView', () => ({ TASK_PART_PARAM: 'part', TaskReadView: ({ task }: { task: Task }) => <p>Shared task view: {task.title}</p> }));
vi.mock('../components/agent/TaskRoutingPanel', () => ({ TaskRoutingPanel: () => <p>Task routing</p> }));

const stages: (keyof AgentPipeline)[] = ['needs_definition', 'ready_to_assign', 'assigned_waiting', 'start_ready', 'executing', 'verification_required', 'recovery_required'];
const task = (id: number, overrides: Partial<Task> = {}): Task => ({
    id, title: `Work item ${id}`, description: 'Delivery work', iteration_id: 1, project_id: 3,
    priority: 2, effort_days: null, effort_hours: null, status: 'planned', is_overdue: false,
    is_delayed: false, is_composite: false, is_optional: false, is_deferred: false,
    tags: [], sort_order: id, external_links: [], request_count: 0, version: 1,
    children: [], dependencies: [],
    agent_readiness: { is_ready: false, blockers: ['Add acceptance criteria.'], warnings: [], criteria: [] },
    ...overrides,
});
const pipeline = (tasks: Task[] = []): AgentPipeline => ({
    needs_definition: tasks, ready_to_assign: [], assigned_waiting: [], start_ready: [],
    executing: [], verification_required: [], recovery_required: [],
});
const LocationProbe = () => { const location = useLocation(); return <output data-testid="pipeline-location">{location.pathname}{location.search}{location.hash}</output>; };
const renderTasks = (url = '/tasks?layout=pipeline&project=all&iteration=1') => renderWithProviders(<>
    <ScopeBar />
    <Routes>
        <Route path="/tasks" element={<TasksPage />} />
        <Route path="/agent-pipeline" element={<LegacyRedirect><p>Old pipeline page</p></LegacyRedirect>} />
    </Routes>
    <LocationProbe />
</>, { initialEntries: [url] });
const strip = () => screen.findByRole('navigation', { name: i18n.t('agentPipeline.stagesLabel') });

const backlogTasks = [
    task(41, { title: 'Orchard release', description: 'Searchable delivery evidence', iteration_id: null, assignee: { id: 7, name: 'Builder' } }),
    task(42, { title: 'Harbor release', description: 'Searchable delivery evidence', project_id: 4, iteration_id: null, claimed_by: { id: 8, name: 'runner', display_name: 'Runner' } }),
    task(43, { title: 'Orchard cleanup', iteration_id: null, assignee: { id: 7, name: 'Builder' } }),
    task(44, { title: 'Iteration work' }),
];

describe('Tasks pipeline view', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        access.hasAdminKey = true;
        useScopeStore.setState({ project: null, iteration: null });
        api.iterations.mockResolvedValue([
            { id: 1, project_id: 3, name: 'Orchard iteration', start_date: '2026-11-01', end_date: '2026-11-30' },
            { id: 2, project_id: 4, name: 'Harbor iteration', start_date: '2026-11-01', end_date: '2026-11-30' },
        ]);
        api.pipeline.mockResolvedValue(pipeline([task(1)]));
        api.task.mockImplementation(async (id: number) => task(id));
        api.snapshot.mockImplementation(async (id: number) => task(id));
        Element.prototype.scrollIntoView = vi.fn();
    });

    it('offers three Tasks views and shows all seven response stage counts with human decision marks', async () => {
        const response = Object.fromEntries(stages.map((stage, index) => [stage, Array.from({ length: index + 1 }, (_, n) => task(index * 10 + n + 1))])) as unknown as AgentPipeline;
        api.pipeline.mockResolvedValue(response);
        const { container, user } = renderTasks();
        const nav = await strip();
        expectPageChrome(container.querySelector<HTMLElement>('.tasks-workbench')!);
        expect(within(screen.getByRole('group', { name: 'Task layout' })).getAllByRole('button')).toHaveLength(3);
        expect(screen.getAllByTestId('page-toolbar')).toHaveLength(1);
        expect(within(nav).getAllByRole('button')).toHaveLength(7);
        expect(within(nav).getAllByText(i18n.t('agentPipeline.needsDecision'))).toHaveLength(3);
        for (const stage of stages) {
            expect(screen.getByTestId(`column-${stage}`)).toHaveTextContent(String(response[stage].length));
        }
        await user.click(screen.getByTestId('column-executing'));
        expect(screen.getAllByTestId(/^task-card-/)).toHaveLength(5);
        expect(screen.getAllByText('Why it is here: Add acceptance criteria.')).toHaveLength(5);
        expect(screen.getAllByText('Estimate unknown')).toHaveLength(5);
    });

    it('filters pipeline work by project and iteration scope, Agent chip and text in the shared toolbar', async () => {
        api.pipeline.mockResolvedValue(pipeline(backlogTasks));
        const { user } = renderTasks('/tasks?layout=pipeline&project=all&iteration=backlog');
        await strip();
        expect(screen.getAllByTestId(/^task-card-/)).toHaveLength(3);
        const toolbar = screen.getByTestId('page-toolbar');
        expect(within(toolbar).queryByRole('combobox', { name: 'Project' })).not.toBeInTheDocument();
        await user.selectOptions(within(toolbar).getByRole('combobox', { name: 'Agent' }), 'Builder');
        expect(screen.getAllByTestId(/^task-card-/)).toHaveLength(2);
        expect(screen.getByRole('list', { name: 'Active filters' })).toHaveTextContent('Agent: Builder');
        await user.type(within(toolbar).getByRole('searchbox'), 'searchable');
        expect(screen.getAllByTestId(/^task-card-/)).toHaveLength(1);
        expect(screen.getByTestId('task-card-41')).toBeVisible();
        await user.click(screen.getByRole('button', { name: 'Remove filter Agent: Builder' }));
        expect(screen.getAllByTestId(/^task-card-/)).toHaveLength(2);
        await user.click(screen.getByRole('combobox', { name: 'Project' }));
        await user.click(screen.getByRole('option', { name: 'Orchard' }));
        await waitFor(() => expect(screen.queryByTestId('task-card-42')).not.toBeInTheDocument());
        expect(screen.getByTestId('pipeline-location')).toHaveTextContent('project=3');
        expect(screen.getByTestId('pipeline-location')).toHaveTextContent('iteration=1');
        expect(within(toolbar).getByRole('searchbox')).toHaveValue('');
        expect(screen.getByTestId('task-card-44')).toBeVisible();
        await user.click(screen.getByRole('combobox', { name: 'Iteration' }));
        await user.click(screen.getByRole('option', { name: /^Backlog/ }));
        expect(screen.getByTestId('pipeline-location')).toHaveTextContent('iteration=backlog');
        expect(screen.getByTestId('task-card-41')).toBeVisible();
        expect(screen.getByTestId('task-card-43')).toBeVisible();
        expect(screen.queryByTestId('task-card-42')).not.toBeInTheDocument();
        await user.selectOptions(within(toolbar).getByRole('combobox', { name: 'Agent' }), 'Builder');
        await user.click(screen.getByRole('button', { name: 'Clear' }));
        expect(screen.getByTestId('pipeline-location')).not.toHaveTextContent('agent=');
        expect(screen.queryByRole('list', { name: 'Active filters' })).not.toBeInTheDocument();
        await user.clear(within(toolbar).getByRole('searchbox'));
        await user.click(screen.getByRole('combobox', { name: 'Iteration' }));
        await user.click(screen.getByRole('option', { name: /Orchard iteration/ }));
        expect(await screen.findByTestId('task-card-44')).toBeVisible();
        expect(screen.queryByTestId('task-card-41')).not.toBeInTheDocument();
    });

    it('redirects the legacy pipeline path preserving project, iteration, agent, text and stage filters', async () => {
        api.pipeline.mockResolvedValue({ ...pipeline(), executing: backlogTasks });
        const { user } = renderTasks('/agent-pipeline?project=4&iteration=backlog&agent=Runner&q=searchable&stage=executing#work');
        await strip();
        const url = screen.getByTestId('pipeline-location');
        for (const part of ['/tasks?', 'layout=pipeline', 'project=4', 'iteration=backlog', 'agent=Runner', 'q=searchable', 'stage=executing', '#work']) expect(url).toHaveTextContent(part);
        expect(screen.queryByText('Old pipeline page')).not.toBeInTheDocument();
        expect(screen.getByRole('button', { name: 'Pipeline' })).toHaveAttribute('aria-pressed', 'true');
        expect(screen.getByRole('combobox', { name: 'Agent' })).toHaveValue('Runner');
        expect(screen.getByRole('searchbox')).toHaveValue('searchable');
        expect(screen.getAllByTestId(/^task-card-/)).toHaveLength(1);
        await user.click(screen.getByTestId('task-card-42'));
        expect(await screen.findByText('Shared task view: Work item 42')).toBeInTheDocument();
        expect(screen.getAllByRole('dialog')).toHaveLength(1);
        expect(screen.getByText('Task routing')).toBeInTheDocument();
        expect(url).toHaveTextContent('task=42');
        expect(url).toHaveTextContent('layout=pipeline');
        await user.keyboard('{Escape}');
        await waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument());
        for (const part of ['layout=pipeline', 'project=4', 'iteration=backlog', 'agent=Runner', 'q=searchable', 'stage=executing']) expect(url).toHaveTextContent(part);
        expect(url).not.toHaveTextContent('task=42');
    });

    it('keeps Pipeline reachable when switching to List or Board in Backlog', async () => {
        api.pipeline.mockResolvedValue(pipeline(backlogTasks));
        const { user } = renderTasks('/tasks?layout=pipeline&project=all&iteration=backlog');
        await strip();
        for (const layout of ['List', 'Board']) {
            await user.click(screen.getByRole('button', { name: layout }));
            expect(screen.getAllByTestId('page-toolbar')).toHaveLength(1);
            expect(within(screen.getByRole('group', { name: 'Task layout' })).getAllByRole('button')).toHaveLength(3);
            await user.click(screen.getByRole('button', { name: 'Pipeline' }));
            await strip();
            expect(screen.getByTestId('pipeline-location')).toHaveTextContent('iteration=backlog');
            expect(screen.getAllByTestId(/^task-card-/)).toHaveLength(3);
        }
    });

    it('applies shared label filters to pipeline rows and stage counts', async () => {
        api.pipeline.mockResolvedValue(pipeline([task(1, { tags: ['delivery'] }), task(2)]));
        const { user } = renderTasks('/tasks?layout=pipeline&project=all&iteration=1&label=delivery');
        await strip();
        expect(screen.getByTestId('task-card-1')).toBeVisible();
        expect(screen.queryByTestId('task-card-2')).not.toBeInTheDocument();
        expect(screen.getByTestId('column-needs_definition')).toHaveTextContent('1');
        await user.click(screen.getByRole('button', { name: 'Clear' }));
        expect(screen.getAllByTestId(/^task-card-/)).toHaveLength(2);
        expect(screen.getByTestId('column-needs_definition')).toHaveTextContent('2');
    });

    it('keeps the stage strip when the response is empty and removes cached rows after authorization fails', async () => {
        const { queryClient } = renderTasks();
        await strip();
        expect(screen.getByTestId('task-card-1')).toBeVisible();
        api.pipeline.mockRejectedValue({ response: { status: 403, data: { detail: 'private upstream error' } } });
        await queryClient.invalidateQueries({ queryKey: ['agent-pipeline'] });
        expect(await screen.findByText(i18n.t('agentPipeline.pipelineUnavailable'))).toBeVisible();
        expect(screen.queryByTestId('task-card-1')).not.toBeInTheDocument();
        expect(document.body).not.toHaveTextContent('private upstream error');
        api.pipeline.mockResolvedValue(pipeline());
        await userRetry();
        expect(within(await strip()).getAllByRole('button')).toHaveLength(7);
        expect(screen.getByText(i18n.t('agentPipeline.emptyTitle'))).toBeVisible();
    });

    it('shows pipeline work to a keyless reader and leaves the key note beneath the toolbar', async () => {
        access.hasAdminKey = false;
        renderTasks();
        await strip();
        expect(screen.getByTestId('task-card-1')).toBeVisible();
        expect(screen.getByText(i18n.t('agentPipeline.runLogsNeedKey'))).toBeVisible();
    });
});

async function userRetry() {
    const { default: userEvent } = await import('@testing-library/user-event');
    await userEvent.click(screen.getByRole('button', { name: /retry/i }));
}

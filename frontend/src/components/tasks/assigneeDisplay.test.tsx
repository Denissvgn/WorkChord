import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor, within } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import type { Task } from '../../types/task';
import type { GanttTask } from '../../types/gantt';
import type { AgentPipeline } from '../../types/agent';
import { TaskRow } from './TaskRow';
import { agentRowValues, useAgentRowFacts } from './useAgentRowFacts';
import { TaskReadView } from './TaskReadView';
import { KanbanCard } from './KanbanBoard/KanbanCard';
import { GanttChart } from '../gantt/GanttChart';
import { PipelineView } from './PipelineView';
import type { usePipeline } from './usePipeline';
import { defaultFilters } from '../../utils/taskFilterDefaults';

const services = vi.hoisted(() => ({ team: vi.fn(), detail: vi.fn(), task: vi.fn() }));
vi.mock('../../services/teamService', () => ({ teamService: { getByIteration: services.team } }));
vi.mock('../../services/taskService', () => ({ taskService: { getDetail: services.detail, getById: services.task } }));
vi.mock('./TaskWorkPanel', () => ({ TaskWorkPanel: () => null }));
vi.mock('./DeliveryDependencies', () => ({ DeliveryDependencies: () => null }));
vi.mock('./TaskDiscussion', () => ({ TaskDiscussion: () => null }));
vi.mock('./TimeEntriesPanel', () => ({ TimeEntriesPanel: () => null }));
vi.mock('./TaskTimelinePanel', () => ({ TaskTimelinePanel: () => null }));
vi.mock('../gantt/TaskEditDrawer', () => ({ TaskEditDrawer: () => null }));
vi.mock('@tanstack/react-virtual', () => ({ useVirtualizer: (options: { count: number; horizontal?: boolean }) => ({
    getTotalSize: () => options.count * 50,
    getVirtualItems: () => options.horizontal ? [] : Array.from({ length: options.count }, (_, index) => ({ index, start: index * 50, size: 50 })),
}) }));

const base = {
    id: 101, title: 'Import holidays', version: 3, iteration_id: 2, project_id: 1, status: 'planned',
    assignee: { id: 7, name: 'Builder' }, owner_profile_id: 9, owner: { id: 9, name: 'Builder' },
    start_date: '2026-11-17', end_date: '2026-11-21', priority: 3, effort_days: 2,
    dependencies: [], children: [], tags: [], external_links: [], request_count: 0,
    is_composite: false, is_optional: false, is_deferred: false, is_overdue: false, is_delayed: false,
    agent_working: false, claimed_by: null, agent_readiness: { is_ready: true, blockers: [], warnings: [], criteria: [] },
} as unknown as Task;
const options = [{ id: 7, name: 'Builder', kind: 'agent' as const, profileId: 9, agentConnected: false }];
const listOptions = [...options];
const ListRow = ({ task }: { task: Task }) => {
    const facts = useAgentRowFacts([task]);
    return <TaskRow id={task.id} title={task.title} status={task.status} assignee={task.assignee} assigneeOptions={listOptions}
        {...agentRowValues(task, listOptions, facts)} onOpen={vi.fn()} menuItems={[]} />;
};
const readView = (task: Task) => <TaskReadView task={task} draftKey={null} onTaskUpdated={vi.fn()} onEditAll={vi.fn()} onDirty={vi.fn()} onPending={vi.fn()} onReload={vi.fn()} />;

beforeEach(() => {
    services.team.mockResolvedValue([{ id: 7, name: 'Builder', profile_id: 9, profile: { profile_kind: 'agent', agent_connected: false } }]);
    services.detail.mockResolvedValue({ reviewer_name: 'Morgan' });
});

describe('assignee consistency across task views', () => {
    it.each([
        ['No agent connected', 'planned', false, null],
        ['Not sent to the agent yet', 'planned', false, null],
        ['Queued', 'planned', true, null],
        ['Working', 'active', true, { id: 4, name: 'runtime', display_name: 'Runtime connection' }],
        ['Waiting for review', 'resolved', false, null],
    ] as const)('shows the same assignee and %s in list, board, Gantt, pipeline and read view', async (label, status, agent_working, claimed_by) => {
        const connected = label !== 'No agent connected';
        services.team.mockResolvedValue([{ id: 7, name: 'Builder', profile_id: 9, profile: { profile_kind: 'agent', agent_connected: connected } }]);
        listOptions.splice(0, 1, { ...options[0], agentConnected: connected });
        const task: Task = { ...base, status, agent_working, claimed_by };
        services.task.mockResolvedValue(task);
        const pipeline: AgentPipeline = { needs_definition: [], ready_to_assign: [], assigned_waiting: [], start_ready: [], executing: [], verification_required: [], recovery_required: [] };
        pipeline.executing = [task];
        const gantt = { ...task, agent_readiness: undefined } as unknown as GanttTask;
        delete (gantt as unknown as Partial<Task>).agent_readiness;
        delete (gantt as unknown as Partial<Task>).agent_working;
        delete (gantt as unknown as Partial<Task>).claimed_by;
        renderWithProviders(<>
            <section aria-label="List"><ListRow task={task} /></section>
            <section aria-label="Board"><KanbanCard task={task} /></section>
            <section aria-label="Gantt"><GanttChart iterationId={2} startDate="2026-11-16" endDate="2026-11-30" tasks={[gantt]} weekends={[]} holidays={[]} memberVacations={{}} /></section>
            <section aria-label="Pipeline"><PipelineView query={{ pipeline, usableData: pipeline, canRead: true, isPending: false, isError: false } as ReturnType<typeof usePipeline>} project={undefined} iteration={undefined} search="" agent="" filters={defaultFilters} labelGroups={[]} onOpenTask={vi.fn()} /></section>
            <section aria-label="Read view">{readView(task)}</section>
        </>, { initialEntries: ['/tasks?stage=executing'] });
        for (const name of ['List', 'Board', 'Gantt', 'Pipeline', 'Read view']) {
            const region = screen.getByRole('region', { name });
            await waitFor(() => expect(region.querySelector('[data-assignee-cell]')).toHaveTextContent('Builder'));
            await waitFor(() => expect(region.querySelector('[data-agent-dispatch]')).toHaveTextContent(label));
            expect(within(region).queryByText('Runtime connection')).not.toBeInTheDocument();
            if (status === 'resolved') await waitFor(() => expect(region.querySelector('[data-reviewer-cell]')).toHaveTextContent('Reviewer: Morgan'));
        }
    });

    it('hides Owner when it equals the assignee profile and shows Owner when it differs', async () => {
        const { rerender } = renderWithProviders(readView(base));
        expect(await screen.findByText('No agent connected')).toBeInTheDocument();
        expect(screen.queryByText('Owner')).not.toBeInTheDocument();
        rerender(readView({ ...base, owner_profile_id: 11, owner: { id: 11, name: 'Priya' } }));
        expect(await screen.findByText('Priya')).toBeInTheDocument();
        expect(screen.getByText('Owner')).toBeInTheDocument();
    });

    it('hides Owner when the assignee profile cannot be read', async () => {
        services.team.mockRejectedValue(new Error('Capacity unavailable'));
        const { queryClient } = renderWithProviders(readView({ ...base, owner_profile_id: 11, owner: { id: 11, name: 'Priya' } }));
        await waitFor(() => expect(queryClient.getQueryState(['team', 2])?.status).toBe('error'));
        expect(screen.queryByText('Owner')).not.toBeInTheDocument();
        expect(screen.queryByText('Priya')).not.toBeInTheDocument();
    });

    it('hides Owner while the assignee profile is still loading', async () => {
        services.team.mockReturnValue(new Promise(() => undefined));
        const { queryClient } = renderWithProviders(readView({ ...base, owner_profile_id: 11, owner: { id: 11, name: 'Priya' } }));
        await waitFor(() => expect(queryClient.getQueryState(['team', 2])?.fetchStatus).toBe('fetching'));
        expect(screen.getByText('Builder', { selector: '[data-assignee-cell] *' })).toBeInTheDocument();
        expect(screen.queryByText('Owner')).not.toBeInTheDocument();
    });

    it('hides Owner when the loaded team has no row for the assignee', async () => {
        services.team.mockResolvedValue([{ id: 8, name: 'Priya', profile_id: 11, profile: { profile_kind: 'human', agent_connected: false } }]);
        const { queryClient } = renderWithProviders(readView(base));
        await waitFor(() => expect(queryClient.getQueryState(['team', 2])?.status).toBe('success'));
        expect(screen.queryByText('Owner')).not.toBeInTheDocument();
    });

    it('shows Owner on a task with no assignee', async () => {
        renderWithProviders(readView({ ...base, assignee: null, owner_profile_id: 11, owner: { id: 11, name: 'Priya' } }));
        expect(await screen.findByText('Owner')).toHaveTextContent('Owner Priya');
    });

    it('offers Send to the agent instead of Start work for a connected agent not sent the task yet', async () => {
        services.team.mockResolvedValue([{ id: 7, name: 'Builder', profile_id: 9, profile: { profile_kind: 'agent', agent_connected: true } }]);
        renderWithProviders(readView(base), { initialEntries: ['/tasks?project=1&iteration=2&task=101'] });
        expect(await screen.findByText('Not sent to the agent yet')).toBeInTheDocument();
        const send = screen.getByRole('link', { name: 'Send to the agent' });
        expect(send).toHaveAttribute('href', expect.stringContaining('layout=pipeline'));
        expect(send).toHaveAttribute('href', expect.stringContaining('task=101'));
        expect(screen.queryByRole('button', { name: 'Start work' })).not.toBeInTheDocument();
        expect(document.querySelectorAll('[data-agent-dispatch]')).toHaveLength(1);
    });

    it('keeps Start work for an agent with no agent connected', async () => {
        renderWithProviders(readView(base));
        expect(await screen.findByText('No agent connected')).toBeInTheDocument();
        expect(screen.getByRole('button', { name: 'Start work' })).toBeInTheDocument();
        expect(screen.queryByRole('link', { name: 'Send to the agent' })).not.toBeInTheDocument();
    });

    it('shows no status line on a closed task', async () => {
        const { queryClient } = renderWithProviders(readView({ ...base, status: 'closed' }));
        await waitFor(() => expect(queryClient.getQueryState(['team', 2])?.status).toBe('success'));
        expect(screen.getByText('Builder', { selector: '[data-assignee-cell] *' })).toBeInTheDocument();
        expect(document.querySelector('[data-agent-dispatch]')).toBeNull();
    });

    it('says Agent status unknown when the team read cannot say whether the agent is connected', async () => {
        services.team.mockResolvedValue([{ id: 7, name: 'Builder', profile_id: 9, profile: { profile_kind: 'agent' } }]);
        renderWithProviders(readView(base));
        expect(await screen.findByText('Agent status unknown')).toBeInTheDocument();
        expect(document.querySelectorAll('[data-agent-dispatch]')).toHaveLength(1);
    });

    it('requests task detail on the Gantt only for rows whose assignee is an agent', async () => {
        services.team.mockResolvedValue([
            { id: 7, name: 'Builder', profile_id: 9, profile: { profile_kind: 'agent' } },
            { id: 8, name: 'Priya', profile_id: 11, profile: { profile_kind: 'human' } },
        ]);
        services.task.mockClear();
        services.task.mockImplementation(async (id: number) => ({ ...base, id }));
        const gantt = (fields: Partial<Task>) => {
            const row = { ...base, ...fields } as Partial<Task>;
            delete row.agent_readiness;
            delete row.agent_working;
            delete row.claimed_by;
            return row as unknown as GanttTask;
        };
        const tasks = [
            gantt({ id: 101 }),
            gantt({ id: 102, title: 'Person task', assignee: { id: 8, name: 'Priya' } as Task['assignee'] }),
            gantt({ id: 103, title: 'Unassigned task', assignee: null }),
            gantt({ id: 104, title: 'Unscheduled person task', assignee: { id: 8, name: 'Priya' } as Task['assignee'], start_date: null, end_date: null }),
        ];
        const { queryClient } = renderWithProviders(<GanttChart iterationId={2} startDate="2026-11-16" endDate="2026-11-30" tasks={tasks} weekends={[]} holidays={[]} memberVacations={{}} />);
        await waitFor(() => expect(queryClient.getQueryState(['team', 2])?.status).toBe('success'));
        await waitFor(() => expect(services.task).toHaveBeenCalledWith(101));
        expect(screen.getAllByText('Priya').length).toBeGreaterThan(0);
        expect(services.task.mock.calls.map(([id]) => id)).toEqual([101]);
    });

    it('keeps the full assignee name accessible and in the tooltip on a short Gantt bar', async () => {
        const name = 'Builder responsible for importing regional holidays and coordinating calendar updates';
        const task = { ...base, assignee: { id: 7, name }, end_date: base.start_date };
        services.task.mockResolvedValue(task);
        const { container } = renderWithProviders(<GanttChart iterationId={2} startDate="2026-11-16" endDate="2026-11-30" tasks={[task as unknown as GanttTask]} weekends={[]} holidays={[]} memberVacations={{}} />);
        const bar = container.querySelector('[data-gantt-task-id="101"]');
        expect(bar).toHaveAccessibleName(expect.stringContaining(name));
        expect(bar).toHaveAttribute('title', expect.stringContaining(name));
        await waitFor(() => expect(bar?.querySelector('[data-agent-dispatch]')).toHaveTextContent('No agent connected'));
        expect(within(bar as HTMLElement).getByTitle(name)).toHaveTextContent(name);
    });
});

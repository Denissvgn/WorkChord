import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor, within } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import type { Task } from '../../types/task';
import { TaskReadView } from './TaskReadView';

// The Work & review panel is the real one: only the services under it are replaced.
const services = vi.hoisted(() => ({ team: vi.fn(), actions: vi.fn(), detail: vi.fn(), task: vi.fn() }));
vi.mock('../../services/teamService', () => ({ teamService: { getByIteration: services.team } }));
vi.mock('../../services/taskService', () => ({ taskService: { actions: services.actions, getDetail: services.detail, getById: services.task } }));
vi.mock('../../services/iterationService', () => ({ iterationService: { getAll: vi.fn().mockResolvedValue([]) } }));
vi.mock('./DeliveryDependencies', () => ({ DeliveryDependencies: () => null }));
vi.mock('./TimeEntriesPanel', () => ({ TimeEntriesPanel: () => null }));

const task = {
    id: 101, title: 'Import holidays', version: 3, iteration_id: 2, project_id: null, status: 'planned',
    assignee: { id: 7, name: 'Builder' }, owner: null, start_date: null, end_date: null, priority: 3, effort_days: 2,
    dependencies: [], children: [], tags: [], external_links: [], request_count: 0,
    is_composite: false, is_optional: false, is_deferred: false, is_overdue: false, is_delayed: false,
    agent_working: false, claimed_by: null, agent_readiness: { is_ready: true, blockers: [], warnings: [], criteria: [] },
} as unknown as Task;

const teamWith = (agentConnected: boolean) => [{ id: 7, name: 'Builder', profile_id: 9, profile: { profile_kind: 'agent', agent_connected: agentConnected } }];

const renderWork = () => renderWithProviders(
    <TaskReadView task={task} draftKey={null} onTaskUpdated={vi.fn()} onEditAll={vi.fn()} onDirty={vi.fn()} onPending={vi.fn()} onReload={vi.fn()} />,
    { initialEntries: ['/tasks?task=101&part=work'] },
);

const workActions = async () => {
    const work = await screen.findByRole('region', { name: 'Work & review' });
    const select = await within(work).findByRole('combobox', { name: 'Action' });
    return within(select).getAllByRole('option').map(option => option.textContent);
};

beforeEach(() => {
    services.actions.mockResolvedValue({
        task_id: 101, version: 3, claim_generation: 0, running_run_ids: [], live_assignment_ids: [],
        actions: [{ action: 'start_manual', allowed: true, blockers: [] }, { action: 'cancel', allowed: true, blockers: [] }],
    });
});

describe('dispatch in the task view', () => {
    it('offers Send to the agent and no manual Start work anywhere in the task view for a connected agent not sent the task yet', async () => {
        services.team.mockResolvedValue(teamWith(true));
        renderWork();
        expect(await screen.findByText('Not sent to the agent yet')).toBeInTheDocument();
        expect(screen.getByRole('link', { name: 'Send to the agent' })).toHaveAttribute('href', expect.stringContaining('layout=pipeline'));
        expect(screen.queryByRole('button', { name: 'Start work' })).not.toBeInTheDocument();
        // Work & review still offers the other manual actions, but not Start work.
        await waitFor(async () => expect(await workActions()).toEqual(['Choose an action', 'Cancel work']));
    });

    it('keeps manual Start work in Work & review for an agent with no agent connected', async () => {
        services.team.mockResolvedValue(teamWith(false));
        renderWork();
        expect(await screen.findByText('No agent connected')).toBeInTheDocument();
        expect(screen.queryByRole('link', { name: 'Send to the agent' })).not.toBeInTheDocument();
        await waitFor(async () => expect(await workActions()).toEqual(['Choose an action', 'Start work', 'Cancel work']));
    });
});

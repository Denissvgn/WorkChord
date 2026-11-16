import { beforeEach, describe, expect, it, vi } from 'vitest';
import { fireEvent, screen, waitFor, within } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { ProjectTaskTree } from './ProjectTaskTree';
import type { Task } from '../../types/task';
import { taskDetailResponse } from '../../test/fixtures/taskDetail';

const services = vi.hoisted(() => ({
    runBulkOperation: vi.fn(),
    team: vi.fn(),
    getDetail: vi.fn(),
}));

vi.mock('../../services/taskService', () => ({ taskService: { runBulkOperation: services.runBulkOperation, update: vi.fn(), changeStatus: vi.fn(), getByIteration: vi.fn().mockResolvedValue([]), getDetail: services.getDetail } }));
vi.mock('../../services/teamService', () => ({ teamService: { getByIteration: services.team } }));
vi.mock('../../services/projectService', () => ({ projectService: { getAll: vi.fn().mockResolvedValue([]), getMilestones: vi.fn().mockResolvedValue([]) } }));
vi.mock('../../services/iterationService', () => ({ iterationService: { getById: vi.fn().mockResolvedValue({ id: 1, name: 'Iteration', project_id: null }) } }));

const task = (id: number, overrides: Partial<Task> = {}): Task => ({
    id, iteration_id: 1, project_id: 1, parent_id: null, title: `Task ${id}`, priority: 2, effort_days: 3, effort_hours: 24,
    assignee: { id: 5, name: 'Ada' }, status: 'planned', is_overdue: false, is_delayed: false, is_composite: false, is_optional: false,
    is_deferred: false, tags: [], sort_order: id, external_links: [], request_count: 0, version: 1, children: [], dependencies: [],
    agent_readiness: { is_ready: true, blockers: [], warnings: [], criteria: [] }, ...overrides,
});

beforeEach(() => {
    services.getDetail.mockReset();
    services.getDetail.mockImplementation(async (id: number) => taskDetailResponse(task(id, { status: 'resolved' }), null));
});

const sections = (...tasks: Task[]) => [{ key: 'all', tasks }];
const rowOf = (title: string) => screen.getByRole('button', { name: title }).closest<HTMLElement>('[data-task-row]')!;

describe('ProjectTaskTree', () => {
    it('shows each task as the shared row: status, priority, title, state, assignee and effort', () => {
        services.team.mockResolvedValue([]);
        renderWithProviders(<ProjectTaskTree sections={sections(task(1, { children: [task(2, { parent_id: 1, status: 'resolved' })], is_composite: true }))} />);
        const parent = rowOf('Task 1');
        const child = rowOf('Task 2');
        expect(parent.className).toContain('min-h-11');
        expect(parent).toHaveTextContent('P2');
        expect(parent).toHaveTextContent('Ada');
        expect(child).toHaveTextContent('In review');
        expect(child.style.paddingLeft).toBe('32px');
    });

    it('shows the assignee who does the task, never the owner', () => {
        services.team.mockResolvedValue([]);
        renderWithProviders(<ProjectTaskTree sections={sections(
            task(1, { assignee: { id: 5, name: 'Ada' }, owner: { id: 9, name: 'Olga Owner' } }),
            task(2, { assignee: null, owner: { id: 9, name: 'Olga Owner' } }),
        )} />);
        expect(rowOf('Task 1')).toHaveTextContent('Ada');
        expect(rowOf('Task 2')).toHaveTextContent('Unassigned');
        expect(screen.queryByText(/Olga Owner/)).toBeNull();
    });

    it('shows the agent status line under an agent assignee and the Reviewer beside it', async () => {
        const agent = { id: 6, name: 'Build agent' };
        services.team.mockResolvedValue([
            { id: 5, name: 'Ada', profile_id: 50, profile: { id: 50, profile_kind: 'human' } },
            { id: 6, name: 'Build agent', profile_id: 60, profile: { id: 60, profile_kind: 'agent' } },
        ]);
        renderWithProviders(<ProjectTaskTree sections={sections(
            task(1, { assignee: agent, agent_working: true }),
            task(2, { assignee: agent, agent_working: true, claimed_by: { id: 3, name: 'builder', display_name: 'Builder' }, status: 'active' }),
            task(3, { assignee: agent, agent_working: false, status: 'resolved' }),
            task(4, { agent_working: false }),
        )} />);
        const lineOf = (title: string) => rowOf(title).querySelector('[data-agent-dispatch]')?.textContent;
        await waitFor(() => expect(lineOf('Task 1')).toBe('Agent status: Queued'));
        expect(lineOf('Task 2')).toBe('Agent status: Working');
        expect(lineOf('Task 3')).toBe('Agent status: Waiting for review');
        expect(lineOf('Task 4')).toBeUndefined();
        await waitFor(() => expect(rowOf('Task 3')).toHaveTextContent('Reviewer: anyone'));
        expect(rowOf('Task 1')).not.toHaveTextContent('Reviewer');
        // Rows not yet submitted keep an empty reviewer cell, so the columns line up.
        expect(rowOf('Task 1').querySelector('[data-reviewer-cell]')).toBeEmptyDOMElement();
        // The Reviewer is read for the submitted task only.
        expect(services.getDetail.mock.calls.map(([id]) => id)).toEqual([3]);
    });

    it('says the agent status is unknown when this reader cannot read the agent roster', async () => {
        services.team.mockResolvedValue([{ id: 6, name: 'Build agent', profile_id: 60, profile: { id: 60, profile_kind: 'agent' } }]);
        renderWithProviders(<ProjectTaskTree sections={sections(
            task(1, { assignee: { id: 6, name: 'Build agent' }, agent_working: false }),
            task(2, { assignee: { id: 6, name: 'Build agent' }, agent_working: true }),
        )} />);
        // Without the roster no row claims that no agent is connected, and the line stays.
        await waitFor(() => expect(rowOf('Task 1').querySelector('[data-agent-dispatch]')?.textContent).toBe('Agent status unknown'));
        expect(rowOf('Task 2').querySelector('[data-agent-dispatch]')?.textContent).toBe('Agent status: Queued');
        expect(screen.queryByText(/No agent connected/)).toBeNull();
    });

    it('leaves the reviewer cell out when no task is submitted, so the title keeps the room', async () => {
        services.team.mockResolvedValue([]);
        renderWithProviders(<ProjectTaskTree sections={sections(task(1), task(2))} />);
        await screen.findByRole('button', { name: 'Task 1' });
        expect(rowOf('Task 1').querySelector('[data-reviewer-cell]')).toBeNull();
        expect(services.getDetail).not.toHaveBeenCalled();
    });

    it('offers the assignee picker with the people and agents of the iteration', async () => {
        services.team.mockResolvedValue([{ id: 5, name: 'Ada', profile: { profile_kind: 'human' } }, { id: 6, name: 'Build agent', profile: { profile_kind: 'agent' } }]);
        renderWithProviders(<ProjectTaskTree sections={sections(task(1))} />);
        const picker = await within(rowOf('Task 1')).findByRole('combobox', { name: 'Assignee: Task 1' });
        await waitFor(() => expect(within(picker).getByRole('option', { name: 'Build agent' })).toBeInTheDocument());
        expect(picker).toHaveValue('5');
    });

    it('selects across the sections and assigns them from one bulk bar', async () => {
        services.team.mockResolvedValue([{ id: 5, name: 'Ada', profile: { profile_kind: 'human' } }]);
        services.runBulkOperation.mockImplementation(async (request: { dry_run: boolean; task_ids: number[] }) => ({
            dry_run: request.dry_run, requested_count: request.task_ids.length, succeeded_count: request.task_ids.length, failed_count: 0,
            task_versions: {}, input_revisions: {},
            results: request.task_ids.map(id => ({ task_id: id, outcome: request.dry_run ? 'would_update' : 'updated', changes: {}, warnings: [] })),
        }));
        const { user } = renderWithProviders(<ProjectTaskTree sections={[
            { key: 'active', heading: 'Active', tasks: [task(1, { status: 'active' }), task(2, { status: 'active' })] },
            { key: 'planned', heading: 'Planned', tasks: [task(3)] },
        ]} />);

        fireEvent.mouseOver(rowOf('Task 1'));
        await user.click(await screen.findByRole('checkbox', { name: 'Select: Task 1' }));
        await user.keyboard('{Shift>}');
        await user.click(screen.getByRole('checkbox', { name: 'Select: Task 3' }));
        await user.keyboard('{/Shift}');
        expect(screen.getAllByTestId('task-bulk-operations')).toHaveLength(1);
        expect(screen.getByText('Selected tasks: 3')).toBeInTheDocument();
        expect(screen.getByRole('button', { name: 'Merge (3)' })).toBeInTheDocument();
        await user.click(screen.getByRole('button', { name: 'Assign' }));
        await user.selectOptions(await screen.findByRole('combobox', { name: 'Choose assignee' }), 'Ada');
        await user.click(screen.getByRole('button', { name: 'Apply' }));

        await waitFor(() => expect(services.runBulkOperation).toHaveBeenCalledTimes(2));
        expect(services.runBulkOperation.mock.calls.at(-1)![0]).toMatchObject({ action: 'set_assignee', payload: { assignee_id: 5 }, dry_run: false, task_ids: [1, 2, 3] });
    });

    it('does not offer a checkbox on a parent or a backlog task, and not across iterations', async () => {
        services.team.mockResolvedValue([]);
        const { user } = renderWithProviders(<ProjectTaskTree sections={sections(
            task(1, { children: [task(2, { parent_id: 1 })], is_composite: true }),
            task(3, { iteration_id: null }),
            task(4, { iteration_id: 2 }),
        )} />);
        fireEvent.mouseOver(rowOf('Task 1'));
        expect(screen.queryByRole('checkbox', { name: 'Select: Task 1' })).toBeNull();
        fireEvent.mouseOver(rowOf('Task 3'));
        expect(screen.queryByRole('checkbox', { name: 'Select: Task 3' })).toBeNull();
        fireEvent.mouseOver(rowOf('Task 2'));
        await user.click(screen.getByRole('checkbox', { name: 'Select: Task 2' }));
        const other = within(rowOf('Task 4')).getByRole('checkbox', { name: 'Select: Task 4' });
        expect(other).toBeDisabled();
    });
});

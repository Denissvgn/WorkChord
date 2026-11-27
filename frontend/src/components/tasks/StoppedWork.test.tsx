import { useState } from 'react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor, within } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { MutationSuccessFeedback } from '../../features/MutationSuccessFeedback';
import { IdentityContext } from '../../features/identity/identityContext';
import type { WorkspaceIdentity } from '../../features/identity/identityService';
import i18n, { ensureLanguageResources } from '../../i18n/i18n';
import type { Task } from '../../types/task';
import { defaultFilters } from '../../utils/taskFilterDefaults';
import { filterTaskBySearch, filterTaskWithChildren } from '../../utils/taskFilters';
import { TaskFiltersBar, type TaskFilters } from './TaskFiltersBar';
import { TaskRow } from './TaskRow';
import { TaskSupersedeForm } from './TaskSupersedeForm';
import { TaskWorkPanel } from './TaskWorkPanel';

const service = vi.hoisted(() => ({
    actions: vi.fn(), progress: vi.fn(), command: vi.fn(), review: vi.fn(), getDetail: vi.fn(), ownerAccept: vi.fn(), reviews: vi.fn(),
    lookup: vi.fn(), supersede: vi.fn(), postpone: vi.fn(), reactivate: vi.fn(), recordOwnerDecision: vi.fn(),
}));
vi.mock('../../services/taskService', () => ({ taskService: service }));
vi.mock('../../services/iterationService', () => ({ iterationService: { getAll: vi.fn().mockResolvedValue([]) } }));
vi.mock('../../services/teamService', () => ({ teamService: { getByIteration: vi.fn().mockResolvedValue([]) } }));
vi.mock('../../services/projectService', () => ({ projectService: { getAll: vi.fn().mockResolvedValue([]), getRoadmapMilestones: vi.fn().mockResolvedValue({ items: [], next_cursor: null }) } }));
vi.mock('../../services/labelService', () => ({ labelService: { getGroups: vi.fn().mockResolvedValue([]) } }));

const base = {
    id: 42, iteration_id: null, project_id: 2, title: 'Ship the importer', priority: 5, effort_days: null, effort_hours: null,
    status: 'active', execution_mode: 'manual', is_overdue: false, is_delayed: false, is_composite: false,
    is_optional: false, is_deferred: false, tags: [], sort_order: 0, external_links: [], request_count: 0,
    agent_readiness: { is_ready: false, blockers: [], warnings: [], criteria: [] }, version: 3, children: [], dependencies: [],
    brief_revision: 1, artifact_revision: 1, assignee: { id: 7, name: 'Sam' },
} as Task;

const identity = (overrides: Partial<WorkspaceIdentity> = {}): WorkspaceIdentity => ({ mode: 'managed', authenticated: true, configured: true,
    principal: { id: 9, kind: 'human', display_name: 'Olga' }, profile: null, workspace_role: 'member', projects: { '2': 'manager' }, csrf_token: 'x', access: 'full', ...overrides });

const setLanguage = async (language: 'en' | 'ru') => { await ensureLanguageResources(language); await i18n.changeLanguage(language); };

beforeEach(async () => {
    vi.clearAllMocks();
    await setLanguage('en');
    service.reviews.mockResolvedValue([]);
    service.actions.mockResolvedValue({ task_id: 42, version: 3, claim_generation: 0, running_run_ids: [], live_assignment_ids: [], actions: [] });
    service.getDetail.mockResolvedValue({ task: { ...base, status: 'planned', displayed_state: 'superseded', successor_task_id: 77, version: 4 }, reviewer_name: null });
    service.lookup.mockResolvedValue({ items: [
        { id: 77, title: 'Importer shipped earlier', version: 6, status: 'closed', displayed_state: 'closed' },
        { id: 78, title: 'Canceled closed work', version: 2, status: 'closed', displayed_state: 'canceled' },
        { id: 42, title: 'Ship the importer', version: 3, status: 'closed', displayed_state: 'closed' },
    ], has_more: false, next_after_id: null, limit: 20 });
    service.supersede.mockResolvedValue({ id: 1, disposition: 'supersession', original_task_id: 42, replacement_task_id: 77 });
});

const row = (props: Partial<Parameters<typeof TaskRow>[0]> = {}) => renderWithProviders(
    <TaskRow id={5} title="Fix login" status="active" onOpen={vi.fn()} menuItems={[]} onStatusChange={vi.fn()} {...props} />);

describe('task row states', () => {
    it.each([
        ['postponed', 'Postponed'], ['canceled', 'Canceled'], ['superseded', 'Superseded'],
    ] as const)('writes %s out as a label and keeps it out of the status menu', (state, label) => {
        row({ state });
        // A visible word, not colour alone, and the status control is not a menu any more.
        expect(screen.getByText(label, { selector: '[data-task-state]' })).toBeVisible();
        expect(screen.getByText(`Status: ${label}`)).toBeInTheDocument();
        expect(screen.queryByRole('button', { name: new RegExp(`Status: ${label}`) })).not.toBeInTheDocument();
    });

    it('shows ordinary status without a state label', () => {
        row({ status: 'planned' });
        expect(document.querySelector('[data-task-state]')).toBeNull();
        expect(screen.getByRole('button', { name: /Status: Planned/ })).toBeInTheDocument();
    });

    it('links a superseded task to its successor from the keyboard', async () => {
        const onOpen = vi.fn();
        const { user } = row({ state: 'superseded', successor: { id: 77, onOpen } });
        await user.tab();
        const link = screen.getByRole('button', { name: 'Superseded by #77' });
        link.focus();
        await user.keyboard('{Enter}');
        expect(onOpen).toHaveBeenCalledTimes(1);
    });

    it('names the states in Russian', async () => {
        await setLanguage('ru');
        row({ state: 'canceled' });
        expect(screen.getByText('Отменено', { selector: '[data-task-state]' })).toBeVisible();
    });
});

describe('state filters', () => {
    const Harness = ({ onChange }: { onChange: (filters: TaskFilters) => void }) => {
        const [filters, setFilters] = useState(defaultFilters);
        return <TaskFiltersBar iterationId={1} filters={filters} onFiltersChange={next => { setFilters(next); onChange(next); }} />;
    };

    it('offers postponed, canceled and superseded beside the lifecycle statuses', async () => {
        const onChange = vi.fn();
        const { user } = renderWithProviders(<Harness onChange={onChange} />);
        const status = await screen.findByRole('combobox', { name: 'Status' });
        expect(within(status).getAllByRole('option').map(option => option.textContent)).toEqual(
            ['Status', 'Planned', 'Active', 'Resolved', 'Closed', 'Postponed', 'Canceled', 'Superseded']);
        await user.selectOptions(status, 'Superseded');
        expect(onChange).toHaveBeenLastCalledWith(expect.objectContaining({ status: 'superseded' }));
    });

    const make = (id: number, overrides: Partial<Task>): Task => ({ ...base, id, iteration_id: 1, title: `Task ${id}`, ...overrides } as Task);

    it('matches each state by what the task is shown as, not the status it kept', () => {
        const pool = [
            make(1, { status: 'active' }),
            make(2, { status: 'postponed', displayed_state: 'postponed' }),
            make(3, { status: 'active', displayed_state: 'canceled' }),
            make(4, { status: 'planned', displayed_state: 'superseded' }),
        ];
        const ids = (status: string) => pool.filter(task => filterTaskWithChildren(task, { ...defaultFilters, status })).map(task => task.id);
        expect(ids('active')).toEqual([1]);
        expect(ids('postponed')).toEqual([2]);
        expect(ids('canceled')).toEqual([3]);
        expect(ids('superseded')).toEqual([4]);
        expect(filterTaskBySearch(pool[2], 'Task 3')).not.toBeNull();
    });
});

describe('Supersede on the task page', () => {
    const renderPanel = (task: Task = base, who: WorkspaceIdentity = identity(), onUpdated = vi.fn()) => ({ onUpdated, ...renderWithProviders(
        <IdentityContext.Provider value={{ identity: who, refresh: vi.fn(), signOut: vi.fn() }}>
            <MutationSuccessFeedback />
            <TaskWorkPanel task={task} disabled={false} draftKey={null} onDirty={vi.fn()} onPending={vi.fn()} onUpdated={onUpdated} onReload={vi.fn()} />
        </IdentityContext.Provider>) });

    it('is offered to a project manager and not to an editor, an observer or an agent', async () => {
        const manager = renderPanel();
        expect(await screen.findByRole('heading', { name: 'Supersede' })).toBeInTheDocument();
        manager.unmount();
        for (const who of [identity({ projects: { '2': 'editor' }, workspace_role: 'member' }), identity({ access: 'observe' }),
            identity({ principal: { id: 3, kind: 'agent', display_name: 'Bot' } })]) {
            const view = renderPanel(base, who);
            await screen.findByText('No actions are currently available.');
            expect(screen.queryByRole('heading', { name: 'Supersede' })).not.toBeInTheDocument();
            view.unmount();
        }
    });

    it('follows the server when the actions list exposes supersede', async () => {
        service.actions.mockResolvedValue({ task_id: 42, version: 3, claim_generation: 0, running_run_ids: [], live_assignment_ids: [],
            actions: [{ action: 'supersede', allowed: false, blockers: [{ code: 'permission_denied', message: 'Not yours.' }] }] });
        renderPanel();
        await screen.findByText('No actions are currently available.');
        expect(screen.queryByRole('heading', { name: 'Supersede' })).not.toBeInTheDocument();
    });

    it('is not offered for accepted work or for a task that is already superseded', async () => {
        const accepted = renderPanel({ ...base, status: 'closed', accepted_at: '2026-11-01T00:00:00Z' } as Task);
        await screen.findByText('No actions are currently available.');
        expect(screen.queryByRole('heading', { name: 'Supersede' })).not.toBeInTheDocument();
        accepted.unmount();
        renderPanel({ ...base, displayed_state: 'superseded', successor_task_id: 77 } as Task);
        await screen.findByText('No actions are currently available.');
        expect(screen.queryByRole('heading', { name: 'Supersede' })).not.toBeInTheDocument();
    });

    it('records the supersession with both expected versions and a reason, entirely from the keyboard', async () => {
        const onUpdated = vi.fn();
        const { user } = renderPanel(base, identity(), onUpdated);
        const open = await screen.findByRole('button', { name: 'Supersede this task' });
        open.focus();
        await user.keyboard('{Enter}');
        // Focus moves into the form.
        const search = screen.getByRole('textbox', { name: 'Search closed tasks in this project' });
        expect(search).toHaveFocus();
        const confirm = screen.getByRole('button', { name: 'Supersede' });
        expect(confirm).toBeDisabled();
        expect(screen.getByText(/Choose the successor\./)).toBeInTheDocument();
        // Only closed work that is not canceled, and not this task, can be the successor.
        const select = await screen.findByRole('combobox', { name: 'Successor' });
        await waitFor(() => expect(within(select).getAllByRole('option')).toHaveLength(2));
        expect(within(select).queryByRole('option', { name: /Canceled closed work/ })).not.toBeInTheDocument();
        expect(within(select).queryByRole('option', { name: /Ship the importer/ })).not.toBeInTheDocument();
        await user.selectOptions(select, '77');
        await user.type(screen.getByRole('textbox', { name: /Why does the successor deliver this work\?/ }), 'The earlier release already shipped it');
        expect(confirm).toBeEnabled();
        await user.click(confirm);
        await waitFor(() => expect(service.supersede).toHaveBeenCalledWith(42, {
            successor_task_id: 77, expected_original_version: 3, expected_successor_version: 6, reason: 'The earlier release already shipped it',
        }));
        await waitFor(() => expect(onUpdated).toHaveBeenCalledWith(expect.objectContaining({ displayed_state: 'superseded', successor_task_id: 77 })));
        // The form closes and focus returns to the control that opened it.
        await waitFor(() => expect(screen.queryByRole('textbox', { name: 'Search closed tasks in this project' })).not.toBeInTheDocument());
        expect(await screen.findByText('Superseded “Ship the importer”.')).toBeInTheDocument();
    });

    it('shows the server refusal and keeps the form so the person can correct it', async () => {
        service.supersede.mockRejectedValue({ isAxiosError: true, response: { status: 409, data: { detail: { code: 'replacement_original_accepted', message: 'Accepted work cannot be superseded.' } } } });
        const { user } = renderPanel();
        await user.click(await screen.findByRole('button', { name: 'Supersede this task' }));
        await user.selectOptions(await screen.findByRole('combobox', { name: 'Successor' }), '77');
        await user.type(screen.getByRole('textbox', { name: /Why does the successor/ }), 'Because');
        await user.click(screen.getByRole('button', { name: 'Supersede' }));
        expect((await screen.findAllByRole('alert')).length).toBeGreaterThan(0);
        expect(screen.getByRole('textbox', { name: /Why does the successor/ })).toHaveValue('Because');
        expect(screen.getByRole('button', { name: 'Supersede' })).toBeEnabled();
    });

    it('discards the form and returns focus to its opener', async () => {
        const { user } = renderPanel();
        await user.click(await screen.findByRole('button', { name: 'Supersede this task' }));
        await user.click(screen.getByRole('button', { name: 'Discard' }));
        await waitFor(() => expect(screen.getByRole('button', { name: 'Supersede this task' })).toHaveFocus());
    });

    it('reads in Russian', async () => {
        await setLanguage('ru');
        const { user } = renderPanel();
        await user.click(await screen.findByRole('button', { name: 'Заменить эту задачу' }));
        expect(screen.getByRole('combobox', { name: 'Заменяющая задача' })).toBeInTheDocument();
        expect(screen.getByRole('textbox', { name: /Почему заменяющая задача выполняет эту работу\?/ })).toBeInTheDocument();
        expect(screen.getByRole('button', { name: 'Заменить' })).toBeDisabled();
    });

    it('stays closed, with the reason, while something outside the form blocks it', () => {
        const onUpdated = vi.fn();
        renderWithProviders(<TaskSupersedeForm task={{ ...base, project_id: 2 } as Task} disabled disabledReasons={['Finish editing first.']} onPending={vi.fn()} onUpdated={onUpdated} />);
        expect(screen.getByRole('button', { name: 'Supersede this task' })).toBeDisabled();
    });
});

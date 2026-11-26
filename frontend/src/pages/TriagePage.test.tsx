import { resolve } from 'node:path';
import { readdirSync, readFileSync } from 'node:fs';
import { screen, waitFor, within } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { expectPageChrome } from '../test/pageChrome';
import { renderWithProviders } from '../test/renderWithProviders';
import TriagePage from './TriagePage';
import { sourceLinkHref } from '../utils/safeUrl';
import { TaskForm } from '../components/tasks/TaskForm';
import { TriageActionModal } from '../components/triage/TriageActionModal';
import { ConvertTriageDrawer } from '../components/triage/ConvertTriageDrawer';
import type { TriageItem } from '../types/triage';
import type { Iteration } from '../types/iteration';
import type { Project } from '../types/project';

const api = vi.hoisted(() => ({ get: vi.fn(), post: vi.fn() }));
vi.mock('../services/api', () => ({ default: api }));
const project = { id: 1, name: 'Calendar' } as Project;
const iteration = { id: 2, name: 'November', nominal_day_hours: 8, project_id: 1, project, start_date: '2026-11-01' } as unknown as Iteration;
const item: TriageItem = {
    id: 7, title: 'Import holidays', description: 'Calendar request', source: 'email', status: 'new',
    labels: ['calendar'], metadata_json: {}, iteration_hint_id: 2, project_hint_id: 1,
    request_count: 0, created_at: '2026-11-01T10:00:00Z', updated_at: '2026-11-01T10:00:00Z',
};
const secondItem = { ...item, id: 8, title: 'Improve search', labels: ['search'], source: 'web' };
beforeEach(() => {
    api.get.mockReset(); api.post.mockReset();
    api.get.mockImplementation(async (path: string) => {
        if (path === '/iterations/page') return { data: { items: [iteration], has_more: false, upper_id: 2 } };
        if (path === '/iterations/2') return { data: iteration };
        if (path === '/projects/page') return { data: { items: [project], has_more: false, upper_id: 1 } };
        if (path === '/tasks/owner-options' || path === '/tasks/lookup') return { data: { items: [], has_more: false } };
        if (path.includes('/duplicate-suggestions')) return { data: { triage_item_id: 7, triage_items: [], tasks: [] } };
        if (path.startsWith('/triage?')) return { data: [item, secondItem] };
        return { data: [] };
    });
    api.post.mockResolvedValue({ data: item });
});

describe('Triage shared page parts', () => {
    it('passes expectPageChrome with loaded requests and keeps every part within 500 lines', async () => {
        const { container } = renderWithProviders(<TriagePage />);
        await screen.findByRole('heading', { name: item.title });
        expectPageChrome(container);
        expect(screen.getAllByTestId('page-toolbar')).toHaveLength(1);
        expect(screen.getByRole('button', { name: 'Waiting' })).toHaveAttribute('aria-pressed', 'true');
        expect(screen.getByRole('button', { name: 'Convert' })).toBeInTheDocument();
        expect(screen.getByRole('button', { name: 'Accept' })).toBeInTheDocument();
        expect(screen.queryByRole('button', { name: 'Decline' })).not.toBeInTheDocument();
        const root = resolve(process.cwd(), 'src/components/triage');
        const files = readdirSync(root).map(name => resolve(root, name));
        files.push(resolve(process.cwd(), 'src/pages/TriagePage.tsx'));
        for (const path of files) expect(readFileSync(path, 'utf8').trimEnd().split('\n').length, path).toBeLessThanOrEqual(500);
    });
    it('shows removable status, source and label chips and preserves the list query contract', async () => {
        const { user } = renderWithProviders(<TriagePage />);
        await screen.findByRole('heading', { name: item.title });
        await user.selectOptions(screen.getByRole('combobox', { name: 'Status' }), 'accepted');
        await user.selectOptions(screen.getByRole('combobox', { name: 'Source' }), 'email');
        await user.selectOptions(screen.getByRole('combobox', { name: 'Labels' }), 'calendar');
        expect(screen.queryByRole('row', { name: /Improve search/ })).not.toBeInTheDocument();
        await user.click(screen.getByRole('button', { name: 'Remove filter Labels: calendar' }));
        expect(screen.getByRole('row', { name: /Improve search/ })).toBeInTheDocument();
        await user.click(screen.getByRole('button', { name: 'All' }));
        await waitFor(() => expect(api.get).toHaveBeenCalledWith('/triage?active=false&status=accepted&source=email&limit=100'));
        await user.click(screen.getByRole('button', { name: 'Clear' }));
        expect(screen.getByRole('button', { name: 'Waiting' })).toHaveAttribute('aria-pressed', 'true');
        expect(screen.queryByRole('list', { name: 'Active filters' })).not.toBeInTheDocument();
    });
    it('opens the same request drawer from New request and the first list row More fields', async () => {
        const { user, container } = renderWithProviders(<TriagePage />);
        await screen.findByRole('heading', { name: item.title });
        const capture = container.querySelector('form')!;
        expect(capture.parentElement?.contains(screen.getByRole('table'))).toBe(true);
        await user.type(within(capture).getByRole('textbox'), 'Customer note');
        await user.click(within(capture).getByRole('button', { name: 'More fields' }));
        let drawer = screen.getByRole('dialog', { name: 'New request' });
        expect(drawer.tagName).toBe('ASIDE');
        expect(within(drawer).getByRole('textbox', { name: 'Title' })).toHaveValue('Customer note');
        await user.click(within(drawer).getByRole('button', { name: 'Cancel' }));
        await user.click(within(container).getByRole('button', { name: 'New request' }));
        drawer = screen.getByRole('dialog', { name: 'New request' });
        expect(within(drawer).getByRole('textbox', { name: 'Title' })).toHaveValue('');
        await user.type(within(drawer).getByRole('textbox', { name: 'Title' }), 'New customer request');
        await user.click(within(drawer).getByRole('button', { name: 'Create request' }));
        await waitFor(() => expect(api.post).toHaveBeenCalledWith('/triage', expect.objectContaining({ title: 'New customer request', labels: [] })));
    });
    it('shows the named source link refusal beside the Source URL field', async () => {
        api.post.mockRejectedValueOnce({ response: { status: 400, data: { detail: {
            code: 'intake_source_link_not_allowed', field: 'source_url',
            message: 'Source link is not allowed: Private, local, or reserved IP targets are not allowed.',
            next_step: 'Use a public http(s) link, or clear the source link.',
        } } } });
        const { user, container } = renderWithProviders(<TriagePage />);
        await screen.findByRole('heading', { name: item.title });
        await user.click(within(container).getByRole('button', { name: 'New request' }));
        const drawer = screen.getByRole('dialog', { name: 'New request' });
        await user.type(within(drawer).getByRole('textbox', { name: 'Title' }), 'Board request');
        await user.type(within(drawer).getByLabelText('Source URL'), 'http://192.168.1.20/board/7');
        await user.click(within(drawer).getByRole('button', { name: 'Create request' }));
        const field = await within(drawer).findByText(/Source link is not allowed.*Use a public http\(s\) link/);
        expect(field).toHaveAttribute('role', 'alert');
        expect(within(drawer).getByLabelText('Source URL')).toHaveAttribute('aria-invalid', 'true');
        expect(within(drawer).getAllByRole('alert')).toHaveLength(1);
    });
    it('lets a relative source link be submitted and only links safe paths', async () => {
        const { user, container } = renderWithProviders(<TriagePage />);
        await screen.findByRole('heading', { name: item.title });
        await user.click(within(container).getByRole('button', { name: 'New request' }));
        const drawer = screen.getByRole('dialog', { name: 'New request' });
        await user.type(within(drawer).getByRole('textbox', { name: 'Title' }), 'Local page');
        await user.type(within(drawer).getByLabelText('Source URL'), '/tasks?project=6');
        await user.click(within(drawer).getByRole('button', { name: 'Create request' }));
        await waitFor(() => expect(api.post).toHaveBeenCalledWith('/triage', expect.objectContaining({ source_url: '/tasks?project=6' })));
        expect(sourceLinkHref('/tasks?project=6')).toBe('/tasks?project=6');
        for (const bad of ['/\t/evil.com', '//evil.com', '/a\\b', '/a b']) expect(sourceLinkHref(bad)).toBeUndefined();
    });
    it('says what became of the source link after a conversion', async () => {
        const note = 'The source link pointed at this instance and was carried over as the relative path /tasks?project=6.';
        api.post.mockResolvedValueOnce({ data: {
            triage_item: { ...item, status: 'converted', converted_task_id: 9 },
            task: { id: 9, title: item.title },
            source_link: { action: 'rewritten', original: 'http://127.0.0.1:8480/tasks?project=6', task_source_url: '/tasks?project=6', message: note },
        } });
        const { user } = renderWithProviders(<TriagePage />);
        await screen.findByRole('heading', { name: item.title });
        await user.click(screen.getByRole('button', { name: 'Convert' }));
        const drawer = await screen.findByRole('dialog');
        await user.type(within(drawer).getByLabelText('Effort (hours)'), '4');
        await user.click(within(drawer).getByRole('button', { name: 'Convert' }));
        expect(await screen.findByText(note)).toBeInTheDocument();
    });
    it.each([
        ['Accept', 'Accept request', '/accept'], ['Decline', 'Decline request', '/decline'],
        ['Snooze', 'Snooze request', '/snooze'], ['Ask for clarification', 'Ask for clarification', '/snooze'],
    ])('preserves the %s disposition request', async (action, dialogTitle, endpoint) => {
        const { user, container } = renderWithProviders(<TriagePage />);
        await screen.findByRole('heading', { name: item.title });
        if (action !== 'Accept') await user.click(screen.getByRole('button', { name: 'More actions' }));
        await user.click(screen.getByRole(action === 'Accept' ? 'button' : 'menuitem', { name: action }));
        const dialog = screen.getByRole('dialog', { name: dialogTitle });
        expect(dialog.tagName).not.toBe('ASIDE');
        await user.type(within(dialog).getByRole('textbox'), 'Reviewed');
        await user.click(within(dialog).getByRole('button', { name: action }));
        const payload = endpoint === '/snooze' ? { reason: 'Reviewed', snoozed_until: expect.any(String) } : { reason: 'Reviewed' };
        await waitFor(() => expect(api.post).toHaveBeenCalledWith(`/triage/7${endpoint}`, payload));
        await waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument());
        expectPageChrome(container);
    });
    it('keeps chrome visible when supporting data fails and offers retry', async () => {
        api.get.mockRejectedValue(new Error('offline'));
        const { container } = renderWithProviders(<TriagePage />);
        await screen.findAllByRole('alert');
        expectPageChrome(container);
        expect(screen.getAllByRole('button', { name: /Retry/ }).length).toBeGreaterThan(0);
    });
});

describe('request conversion shares task creation sections', () => {
    it('shows the same essentials, More section and task field names as task creation', async () => {
        const task = renderWithProviders(<TaskForm iterationId={2} onSuccess={vi.fn()} onCancel={vi.fn()} />);
        await screen.findByRole('textbox', { name: 'Task title' });
        const essentialNames = ['Task title', 'Assignee', 'Effort (hours)', 'Goal'];
        for (const name of essentialNames) expect(screen.getByLabelText(name)).toBeInTheDocument();
        expect(screen.getByText('Acceptance criteria', { exact: true })).toBeInTheDocument();
        await task.user.click(screen.getByRole('button', { name: 'More' }));
        const detailNames = ['Context', 'Scope', 'Out of scope', 'Verification approach', 'Expected artifacts', 'Priority'];
        for (const name of detailNames) expect(screen.getByLabelText(name)).toBeInTheDocument();
        for (const name of ['Project', 'Waits for', 'Labels']) expect(screen.getByText(name, { exact: true })).toBeInTheDocument();
        task.unmount();
        const convert = renderWithProviders(<ConvertTriageDrawer item={item} projects={[project]} iterations={[iteration]} selectedIterationId={2}
            isSubmitting={false} onSubmit={vi.fn()} onClose={vi.fn()} />);
        const drawer = screen.getByRole('dialog', { name: 'Convert to task' });
        for (const name of essentialNames) expect(within(drawer).getByLabelText(name)).toBeInTheDocument();
        expect(within(drawer).getByText('Acceptance criteria', { exact: true })).toBeInTheDocument();
        expect(within(drawer).queryByLabelText('Context')).not.toBeInTheDocument();
        await convert.user.click(within(drawer).getByRole('button', { name: 'More' }));
        for (const name of detailNames) expect(within(drawer).getByLabelText(name)).toBeInTheDocument();
        for (const name of ['Project', 'Waits for', 'Labels']) expect(within(drawer).getByText(name, { exact: true })).toBeInTheDocument();
    });
    it('preserves conversion payloads, effort hours, structured brief and backlog destination', async () => {
        const onSubmit = vi.fn();
        const { user } = renderWithProviders(<ConvertTriageDrawer item={item} projects={[project]} iterations={[iteration]} selectedIterationId={2}
            isSubmitting={false} onSubmit={onSubmit} onClose={vi.fn()} />);
        await user.type(screen.getByLabelText('Effort (hours)'), '16');
        expect(screen.getByText(/2.*8/)).toBeInTheDocument();
        await user.click(screen.getByRole('button', { name: 'Convert' }));
        expect(onSubmit).toHaveBeenLastCalledWith(expect.objectContaining({ destination: 'iteration', iteration_id: 2, project_id: 1, title: item.title,
            effort_days: null, effort_hours: 16, tags: item.labels, depends_on: [], brief: expect.objectContaining({ goal: item.title, context: item.description }) }));
        await user.click(screen.getByRole('button', { name: 'More' }));
        await user.selectOptions(screen.getByLabelText('Destination'), 'project_backlog');
        await user.click(screen.getByRole('button', { name: 'Convert' }));
        expect(onSubmit).toHaveBeenLastCalledWith(expect.objectContaining({ destination: 'project_backlog', iteration_id: null, project_id: 1, assignee_id: null }));
    });
});


describe('request action details', () => {
    it.each(['triage', 'task'] as const)('preserves a suggested duplicate of a %s', async targetType => {
        const onSubmit = vi.fn();
        const { user } = renderWithProviders(<TriageActionModal action="duplicate" item={item} allTriageItems={[item, secondItem]}
            iterations={[iteration]} selectedIterationId={2} defaultSnooze="2026-12-01T10:00"
            defaultDuplicate={{ targetType, targetId: targetType === 'triage' ? 8 : 99, title: 'Existing request', iterationId: 2 }}
            isSubmitting={false} onSubmit={onSubmit} onClose={vi.fn()} />);
        if (targetType === 'task') expect(screen.getByRole('checkbox', { name: 'Link this request to the duplicate task' })).toBeChecked();
        await user.type(screen.getByRole('textbox', { name: 'Reason' }), 'Same request');
        await user.click(screen.getByRole('button', { name: 'Mark duplicate' }));
        expect(onSubmit).toHaveBeenCalledWith(targetType === 'triage'
            ? { duplicate_of_id: 8, duplicate_task_id: null, reason: 'Same request' }
            : { duplicate_of_id: null, duplicate_task_id: 99, link_request_to_duplicate_task: true, reason: 'Same request' });
    });

    it('keeps draft application and individual suggestions in the conversion drawer', async () => {
        api.post.mockResolvedValue({ data: { triage_item_id: 7, suggested_title: 'Drafted task', suggested_description: 'Drafted context',
            acceptance_criteria: ['Verified result'], suggested_checklist: ['Inspect output'], risks: ['Check calendar'], is_fallback: true } });
        const onSubmit = vi.fn();
        const { user } = renderWithProviders(<ConvertTriageDrawer item={item} projects={[project]} iterations={[iteration]} selectedIterationId={2}
            isSubmitting={false} onSubmit={onSubmit} onClose={vi.fn()} />);
        await user.click(screen.getByRole('button', { name: 'Draft task details' }));
        await screen.findByText('AI draft preview');
        expect(api.post).toHaveBeenCalledWith('/triage/7/draft-task', { template_id: null, current_title: item.title, current_description: item.description });
        await user.click(screen.getByRole('button', { name: 'Apply suggested title' }));
        expect(screen.getByLabelText('Task title')).toHaveValue('Drafted task');
        await user.click(screen.getAllByRole('button', { name: 'Append to description' })[0]);
        expect(screen.getByLabelText('Criterion 1')).toHaveValue('Verified result');
        await user.click(screen.getByRole('button', { name: 'Apply suggested description' }));
        await user.click(screen.getByRole('button', { name: 'More' }));
        expect(screen.getByLabelText('Context')).toHaveValue('Drafted context');
        await user.click(screen.getByRole('button', { name: 'Apply draft' }));
        await user.click(screen.getByRole('button', { name: 'Convert' }));
        expect(onSubmit).toHaveBeenCalledWith(expect.objectContaining({ title: 'Drafted task', brief: expect.objectContaining({
            goal: 'Drafted task', context: expect.stringContaining('Drafted context'), acceptance_criteria: [expect.objectContaining({ text: 'Verified result' })],
        }) }));
    });
});

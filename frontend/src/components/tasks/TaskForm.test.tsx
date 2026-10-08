import { beforeEach, describe, expect, it, vi } from 'vitest';
import { act, screen, waitFor } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { TaskForm } from './TaskForm';
import { emptyTaskBrief } from './taskEditorContract';
import type { WorkTemplate } from '../../types/template';

const api = vi.hoisted(() => ({ get: vi.fn(), post: vi.fn() }));
vi.mock('../../services/api', () => ({ default: api }));

describe('task template application', () => {
    beforeEach(() => {
        api.get.mockReset();
        api.post.mockReset();
        api.post.mockResolvedValue({ data: { id: 42 } });
    });

    const configure = (template: WorkTemplate) => {
        api.get.mockImplementation(async (path: string) => {
            if (path.startsWith('/templates')) return { data: [template] };
            if (path === '/projects') return { data: [{ id: 1, name: 'Project' }] };
            if (path === '/projects/page') return { data: { items: [{ id: 1, name: 'Project' }], has_more: false, upper_id: 1, next_after_id: null } };
            if (path === '/tasks/owner-options') return { data: { items: [], has_more: false } };
            if (path === '/tasks/lookup') return { data: { items: [], has_more: false } };
            return { data: [] };
        });
    };

    const template = (payload: WorkTemplate['default_payload'] = {}): WorkTemplate => ({
        id: 7, name: 'Delivery template', template_type: 'task', default_title: 'New deliverable',
        default_description: 'Legacy context', default_checklist: [], default_payload: payload,
        default_labels: [], is_active: true, sort_order: 0, created_at: '', updated_at: '',
    });

    it('saves the canonical brief instead of overwriting it with legacy defaults', async () => {
        const brief = { ...emptyTaskBrief(), goal: 'Canonical goal', context: 'Canonical context',
            scope: 'Bounded delivery', exclusions: 'Excluded work', verification: 'Inspect output', artifact_expectations: 'A report',
            acceptance_criteria: [{ id: 'template-criterion', revision: 4, text: 'Canonical result', verification: 'Independent check' }] };
        const source = template({ brief });
        configure(source);
        const { user } = renderWithProviders(<TaskForm iterationId={null} parentProjectId={1} onSuccess={vi.fn()} onCancel={vi.fn()} />);
        await user.selectOptions(await screen.findByRole('combobox', { name: 'Template' }), '7');
        expect(screen.getByRole('textbox', { name: 'Goal' })).toHaveValue('Canonical goal');
        expect(screen.getByRole('textbox', { name: 'Criterion 1' })).toHaveValue('Canonical result');
        await user.click(screen.getByRole('button', { name: 'Create Task' }));
        await waitFor(() => expect(api.post).toHaveBeenCalled());
        const [path, saved] = api.post.mock.calls[0];
        expect(path).toBe('/projects/1/backlog');
        expect(saved.brief).toEqual({ ...brief, acceptance_criteria: [
            { ...brief.acceptance_criteria[0], id: expect.any(String), revision: 1 },
        ] });
        expect(saved.brief.acceptance_criteria[0].id).not.toBe('template-criterion');
        expect(source.default_payload.brief).toEqual(brief);
    });

    it('adapts a legacy template into the same canonical save contract', async () => {
        const source = { ...template(), default_checklist: ['Legacy criterion'] };
        configure(source);
        const { user } = renderWithProviders(<TaskForm iterationId={null} parentProjectId={1} onSuccess={vi.fn()} onCancel={vi.fn()} />);
        await user.selectOptions(await screen.findByRole('combobox', { name: 'Template' }), '7');
        await user.click(screen.getByRole('button', { name: 'Create Task' }));
        await waitFor(() => expect(api.post).toHaveBeenCalled());
        expect(api.post.mock.calls[0][1].brief).toMatchObject({ goal: 'New deliverable', context: 'Legacy context',
            acceptance_criteria: [{ id: expect.any(String), revision: 1, text: 'Legacy criterion', verification: '' }] });
    });

    it('does not blindly create again after an uncertain result without a current comparison', async () => {
        configure(template());
        api.post.mockRejectedValueOnce(new TypeError('No verified response'));
        const { user } = renderWithProviders(<TaskForm iterationId={null} parentProjectId={1} onSuccess={vi.fn()} onCancel={vi.fn()} />);
        await user.type(await screen.findByRole('textbox', { name: /Task Title/i }), 'Possibly created work');
        await user.click(screen.getByRole('button', { name: 'Create Task' }));
        await screen.findByText('Failed to create task');
        expect(screen.getByRole('button', { name: 'Create Task' })).toBeDisabled();
        await user.click(screen.getByRole('button', { name: 'Reload current server work' }));
        await user.click(await screen.findByRole('button', { name: 'I compared current work; resume this draft' }));
        expect(screen.getByRole('button', { name: 'Create Task' })).toBeEnabled();
        expect(api.post).toHaveBeenCalledTimes(1);
    });

    it('does not notify an obsolete route when a delayed create completes after unmount', async () => {
        configure(template());
        let finish!: (value: unknown) => void;
        api.post.mockImplementationOnce(() => new Promise(resolve => { finish = resolve; }));
        const completed = vi.fn();
        const view = renderWithProviders(<TaskForm iterationId={null} parentProjectId={1} onSuccess={completed} onCancel={vi.fn()} />);
        await view.user.type(await screen.findByRole('textbox', { name: /Task Title/i }), 'Deferred creation');
        await view.user.click(screen.getByRole('button', { name: 'Create Task' }));
        await waitFor(() => expect(finish).toBeTypeOf('function'));
        view.unmount();
        await act(async () => finish({ data: { id: 44 } }));
        expect(completed).not.toHaveBeenCalled();
    });
});

import { act, fireEvent, screen, waitFor } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { createTestQueryClient, renderWithProviders } from '../../test/renderWithProviders';
import { TaskTextEditorModal } from './TaskTextEditorModal';
import { ImportTasksModal } from './ImportTasksModal';

const service = vi.hoisted(() => ({ getTasksTextContext: vi.fn(), bulkUpdateTasks: vi.fn(), importFromText: vi.fn() }));
const iterations = vi.hoisted(() => ({ getById: vi.fn() }));
vi.mock('../../services/taskService', () => ({ taskService: service }));
vi.mock('../../services/iterationService', () => ({ iterationService: iterations }));

describe('Revision-bound text commands', () => {
    afterEach(() => vi.unstubAllGlobals());
    beforeEach(() => {
        vi.clearAllMocks();
        service.getTasksTextContext.mockResolvedValue({ text: '- Original', iteration_id: 9, iteration_revision: 3 });
        iterations.getById.mockResolvedValue({ id: 9, revision: 3 });
        service.bulkUpdateTasks.mockResolvedValue({ task_count: 1, triage_count: 0 });
        service.importFromText.mockResolvedValue({ task_count: 1, triage_count: 0 });
    });

    it('preserves a stale draft and requires comparison before using a new revision', async () => {
        service.bulkUpdateTasks.mockRejectedValueOnce({ response: { status: 409, data: { detail: {
            code: 'iteration_version_conflict', message: 'The iteration changed.' } } } });
        renderWithProviders(<TaskTextEditorModal iterationId={9} onClose={vi.fn()} />);
        const editor = await screen.findByDisplayValue('- Original');
        fireEvent.change(editor, { target: { value: '- My changes' } });
        fireEvent.click(screen.getByRole('button', { name: 'Apply' }));
        await screen.findByText('The iteration changed.');
        expect(editor).toHaveValue('- My changes');
        expect(screen.getByRole('button', { name: 'Apply' })).toBeDisabled();
        expect(service.bulkUpdateTasks).toHaveBeenCalledTimes(1);
        service.getTasksTextContext.mockResolvedValueOnce({ text: '- Another editor', iteration_id: 9, iteration_revision: 4 });
        fireEvent.click(screen.getByRole('button', { name: 'Compare current text' }));
        expect(await screen.findByLabelText('Current server text')).toHaveValue('- Another editor');
        expect(editor).toHaveValue('- My changes');
        expect(service.bulkUpdateTasks).toHaveBeenCalledTimes(1);
        fireEvent.click(screen.getByRole('button', { name: 'I compared the changes; keep my input' }));
        fireEvent.click(screen.getByRole('button', { name: 'Apply' }));
        await waitFor(() => expect(service.bulkUpdateTasks).toHaveBeenLastCalledWith(9, '- My changes', { destination: 'auto', expectedRevision: 4 }));
    });

    it('keeps the original text base when a query refresh returns a newer revision', async () => {
        const queryClient = createTestQueryClient();
        renderWithProviders(<TaskTextEditorModal iterationId={9} onClose={vi.fn()} />, { queryClient });
        const editor = await screen.findByDisplayValue('- Original');
        fireEvent.change(editor, { target: { value: '- My draft' } });
        service.getTasksTextContext.mockResolvedValueOnce({ text: '- New server text', iteration_id: 9, iteration_revision: 8 });
        await queryClient.invalidateQueries({ queryKey: ['tasks', 'text-context', 9] });
        expect(editor).toHaveValue('- My draft');
        fireEvent.click(screen.getByRole('button', { name: 'Apply' }));
        await waitFor(() => expect(service.bulkUpdateTasks).toHaveBeenCalledWith(9, '- My draft', { destination: 'auto', expectedRevision: 3 }));
    });

    it('sends the observed planning revision for a text import', async () => {
        renderWithProviders(<ImportTasksModal iterationId={9} onClose={vi.fn()} />);
        await waitFor(() => expect(screen.getByPlaceholderText('Or paste text here...')).not.toHaveAttribute('readonly'));
        const editor = screen.getByPlaceholderText('Or paste text here...');
        fireEvent.change(editor, { target: { value: '- Captured request' } });
        await waitFor(() => expect(screen.getByRole('button', { name: 'Import tasks' })).toBeEnabled());
        fireEvent.click(screen.getByRole('button', { name: 'Import tasks' }));
        await waitFor(() => expect(service.importFromText).toHaveBeenCalledWith(9, '- Captured request', { destination: 'tasks', expectedRevision: 3 }));
    });

    it('ignores an older file read and prevents submission while the current read is pending', async () => {
        const readers: Reader[] = [];
        class Reader {
            onload: ((event: ProgressEvent<FileReader>) => void) | null = null;
            onabort: (() => void) | null = null;
            onerror: (() => void) | null = null;
            constructor() { readers.push(this); }
            readAsText() {}
            abort() { this.onabort?.(); }
            finish(text: string) { this.onload?.({ target: { result: text } } as unknown as ProgressEvent<FileReader>); }
        }
        vi.stubGlobal('FileReader', Reader);
        renderWithProviders(<ImportTasksModal iterationId={9} onClose={vi.fn()} />);
        await waitFor(() => expect(screen.getByPlaceholderText('Or paste text here...')).not.toHaveAttribute('readonly'));
        const input = screen.getByRole('dialog').querySelector<HTMLInputElement>('input[type="file"]');
        if (!input) throw new Error('Missing file chooser');
        fireEvent.change(input, { target: { files: [new File(['first'], 'first.txt')] } });
        fireEvent.change(input, { target: { files: [new File(['second'], 'second.txt')] } });
        expect(screen.getByRole('button', { name: 'Import tasks' })).toBeDisabled();
        act(() => readers[0].finish('- Old file'));
        expect(screen.getByPlaceholderText('Or paste text here...')).not.toHaveValue('- Old file');
        act(() => readers[1].finish('- Current file'));
        expect(screen.getByPlaceholderText('Or paste text here...')).toHaveValue('- Current file');
        expect(screen.getByRole('button', { name: 'Import tasks' })).toBeEnabled();
    });
});

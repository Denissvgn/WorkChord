import { describe, expect, it, vi } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import { useMutation } from '@tanstack/react-query';
import { renderWithProviders } from '../test/renderWithProviders';
import i18n from '../i18n/i18n';
import { MutationSuccessFeedback } from './MutationSuccessFeedback';
import { feedbackMessage } from './mutationFeedback';
import type { MutationFeedbackMeta } from './mutationFeedback';

const Writer = ({ meta, fail = false }: { meta: MutationFeedbackMeta; fail?: boolean }) => {
    const write = useMutation({
        mutationFn: async (title: string) => { if (fail) throw new Error('Rejected'); return { id: 7, title }; },
        meta,
    });
    return <button type="button" onClick={() => write.mutate('Fix login')}>Write</button>;
};

describe('mutation success feedback', () => {
    it('names the object written, from the mutation result', async () => {
        const { user } = renderWithProviders(<><MutationSuccessFeedback />
            <Writer meta={{ success: data => feedbackMessage(i18n.t, 'created', 'task', (data as { title: string }).title) }} /></>);
        await user.click(screen.getByRole('button', { name: 'Write' }));
        expect(await screen.findByText('Created task “Fix login”.')).toBeInTheDocument();
    });

    it('offers Undo and announces when it was applied', async () => {
        const run = vi.fn().mockResolvedValue(undefined);
        const { user } = renderWithProviders(<><MutationSuccessFeedback />
            <Writer meta={{ success: 'Saved.', undo: () => ({ run, done: 'Back as it was.' }) }} /></>);
        await user.click(screen.getByRole('button', { name: 'Write' }));
        await user.click(await screen.findByRole('button', { name: 'Undo' }));
        await waitFor(() => expect(run).toHaveBeenCalledOnce());
        expect(await screen.findByText('Back as it was.')).toBeInTheDocument();
    });

    it('says when Undo failed and shows nothing for a failed write', async () => {
        const run = vi.fn().mockRejectedValue(new Error('Server refused'));
        const { user, unmount } = renderWithProviders(<><MutationSuccessFeedback />
            <Writer meta={{ success: 'Saved.', undo: () => ({ run }) }} /></>);
        await user.click(screen.getByRole('button', { name: 'Write' }));
        await user.click(await screen.findByRole('button', { name: 'Undo' }));
        expect(await screen.findByRole('alert')).toHaveTextContent(/Server refused|Could not undo/);
        unmount();
        const second = renderWithProviders(<><MutationSuccessFeedback /><Writer fail meta={{ success: 'Saved.' }} /></>);
        await second.user.click(screen.getByRole('button', { name: 'Write' }));
        await new Promise(resolve => setTimeout(resolve, 20));
        expect(screen.queryByText('Saved.')).toBeNull();
    });
});

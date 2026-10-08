import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { IdentityContext } from '../../features/identity/identityContext';
import { TaskDiscussion } from './TaskDiscussion';

const service = vi.hoisted(() => ({ list: vi.fn(), mentions: vi.fn(), save: vi.fn(), history: vi.fn(), subscription: vi.fn(), subscribe: vi.fn() }));
vi.mock('../../services/discussionService', () => ({ discussionService: service }));
const comment = (version = 1, body = 'Original question') => ({ id: 7, task_id: 42, principal_id: 1, author_name: 'Sam', body, mentions: [], version, deleted: false, created_at: '2026-09-30T10:00:00Z', updated_at: '2026-09-30T10:00:00Z' });
const renderDiscussion = () => renderWithProviders(<IdentityContext.Provider value={{ identity: {
    mode: 'managed', authenticated: true, configured: true, principal: { id: 1, kind: 'human', display_name: 'Sam' },
    profile: { id: 8, display_name: 'Sam' }, workspace_role: 'member', projects: { '2': 'editor' }, csrf_token: null,
}, refresh: vi.fn(), signOut: async () => undefined }}><TaskDiscussion taskId={42} draftKey="discussion-test" disabled={false} onDirty={vi.fn()} onPending={vi.fn()} /></IdentityContext.Provider>);

describe('task discussion', () => {
    beforeEach(() => {
        sessionStorage.clear();
        vi.resetAllMocks();
        service.list.mockResolvedValue({ items: [comment()], has_more: false });
        service.subscription.mockResolvedValue({ version: 0, enabled: false, events: ['discussion', 'mention'] });
        service.mentions.mockResolvedValue({ items: [], has_more: false });
        service.history.mockResolvedValue({ items: [], has_more: false });
    });

    it('preserves an edit on conflict and explicitly adopts the reviewed current version', async () => {
        service.save.mockRejectedValueOnce(new Error('Conflict'));
        const { user } = renderDiscussion();
        await user.click(await screen.findByRole('button', { name: 'Edit' }));
        const input = screen.getByRole('textbox', { name: 'Edit comment' });
        await user.clear(input);
        await user.type(input, 'My retained draft');
        await user.click(screen.getByRole('button', { name: 'Save comment' }));
        await screen.findByRole('alert');
        expect(input).toHaveValue('My retained draft');
        service.list.mockResolvedValue({ items: [comment(2, 'Another editor changed the note')], has_more: false });
        await user.click(screen.getByRole('button', { name: 'Reload comments' }));
        await user.click(await screen.findByRole('button', { name: 'Keep draft with current version' }));
        service.save.mockResolvedValue(comment(3, 'My retained draft'));
        await user.click(screen.getByRole('button', { name: 'Save comment' }));
        await waitFor(() => expect(service.save).toHaveBeenLastCalledWith(42, 'My retained draft', [], expect.objectContaining({ id: 7, version: 2 }), false));
    });

    it('restores the original edit identity and renders HTML as plain text', async () => {
        sessionStorage.setItem('discussion-test:discussion', JSON.stringify({ body: 'Recovered edit', mentions: [2], editing: { id: 7, version: 1 }, savedAt: Date.now() }));
        service.list.mockResolvedValue({ items: [comment(1, '<script>alert(1)</script>')], has_more: false });
        service.save.mockResolvedValue(comment(2));
        const { user, container } = renderDiscussion();
        expect(await screen.findByText('<script>alert(1)</script>')).toBeInTheDocument();
        expect(container.querySelector('script')).toBeNull();
        expect(screen.getByRole('textbox', { name: 'Edit comment' })).toHaveValue('Recovered edit');
        await user.click(screen.getByRole('button', { name: 'Save comment' }));
        await waitFor(() => expect(service.save).toHaveBeenCalledWith(42, 'Recovered edit', [2], { id: 7, version: 1 }, false));
    });

    it('requires a current read and explicit comparison before resuming an uncertain recovered write', async () => {
        service.save.mockRejectedValueOnce(new TypeError('No verified response'));
        const view = renderDiscussion();
        await view.user.type(await screen.findByRole('textbox', { name: 'New comment' }), 'Possibly committed comment');
        await view.user.click(screen.getByRole('button', { name: 'Post comment' }));
        await screen.findByRole('alert');
        view.unmount();
        service.list.mockResolvedValue({ items: [comment(1, 'Possibly committed comment')], has_more: false });
        const reopened = renderDiscussion();
        expect(await screen.findByRole('textbox', { name: 'New comment' })).toHaveValue('Possibly committed comment');
        expect(screen.getByRole('button', { name: 'Post comment' })).toBeDisabled();
        await reopened.user.click(screen.getByRole('button', { name: 'Reload current comments' }));
        await reopened.user.click(await screen.findByRole('button', { name: 'I compared the current comments' }));
        expect(screen.getByRole('button', { name: 'Post comment' })).toBeEnabled();
        expect(service.save).toHaveBeenCalledTimes(1);
    });
});

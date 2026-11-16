import { describe, expect, it, vi } from 'vitest';
import { screen, waitFor, within } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import type { PlanShare } from '../../services/planShareService';
import { PlanShareSection } from './PlanShareSection';

const service = vi.hoisted(() => ({ getCurrent: vi.fn(), create: vi.fn(), revoke: vi.fn(), getByPublicId: vi.fn() }));
vi.mock('../../services/planShareService', () => ({ planShareService: service }));

const share = {
    id: 7,
    public_id: 'abc123',
    iteration_id: 4,
    iteration_name: 'Iteration 4',
    created_by_display: 'Sam',
    created_at: '2026-11-01T10:00:00Z',
    revoked_at: null,
    snapshot_data: {} as PlanShare['snapshot_data'],
} satisfies PlanShare;

const revokeDialogName = /Revoke this plan link\?/;

// Waits until the failed attempt has settled, reading the dialog from the document each time.
const waitForConfirmationReady = () => waitFor(() => {
    const dialog = screen.getByRole('dialog', { name: revokeDialogName });
    expect(within(dialog).getByRole('button', { name: 'Revoke link' })).toBeEnabled();
});

const openRevokeConfirmation = async (user: ReturnType<typeof renderWithProviders>['user']) => {
    await user.click(await screen.findByRole('button', { name: 'Revoke link' }));
    return screen.findByRole('dialog', { name: revokeDialogName });
};

describe('sharing the plan from the Review checkpoint', () => {
    it('keeps the confirmation open when revoking fails, and Retry after cancelling does not bring it back', async () => {
        service.getCurrent.mockResolvedValue(share);
        service.revoke.mockRejectedValueOnce(new Error('network down'));
        const { user } = renderWithProviders(<PlanShareSection iterationId={4} />);

        const dialog = await openRevokeConfirmation(user);
        await user.click(within(dialog).getByRole('button', { name: 'Revoke link' }));
        await waitFor(() => expect(service.revoke).toHaveBeenCalledWith(7));

        // The failed revocation leaves the confirmation in place, ready to try again or cancel.
        await waitForConfirmationReady();
        expect(screen.getByRole('dialog', { name: revokeDialogName })).toBe(dialog);
        expect(document.activeElement).not.toBe(document.body);
        expect(dialog.contains(document.activeElement)).toBe(true);

        // Cancelling closes it for good and hands focus to the error panel's Retry.
        await user.click(within(dialog).getByRole('button', { name: 'Cancel' }));
        await waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument());
        const retry = await screen.findByRole('button', { name: 'Retry' });
        await waitFor(() => expect(retry).toHaveFocus());

        // Recovery: Retry reads the link again and shows it; the old confirmation stays closed.
        await user.click(retry);
        const heading = await screen.findByRole('heading', { name: 'Plan snapshot shared' });
        expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
        await waitFor(() => expect(heading).toHaveFocus());
        expect(service.getCurrent).toHaveBeenCalledTimes(2);
    });

    it('revokes the link when confirming again after a failed attempt', async () => {
        service.getCurrent.mockResolvedValue(share);
        service.revoke.mockRejectedValueOnce(new Error('network down')).mockResolvedValueOnce(undefined);
        const { user } = renderWithProviders(<PlanShareSection iterationId={4} />);

        const dialog = await openRevokeConfirmation(user);
        await user.click(within(dialog).getByRole('button', { name: 'Revoke link' }));
        await waitForConfirmationReady();
        await user.click(within(dialog).getByRole('button', { name: 'Revoke link' }));

        await waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument());
        expect(service.revoke).toHaveBeenCalledTimes(2);
        const heading = await screen.findByRole('heading', { name: 'Plan ready to share' });
        await waitFor(() => expect(heading).toHaveFocus());
        expect(screen.queryByRole('button', { name: 'Retry' })).not.toBeInTheDocument();
    });
});

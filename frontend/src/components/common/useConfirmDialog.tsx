import { useState } from 'react';
import type { ReactNode } from 'react';
import { ConfirmDialog } from './ConfirmDialog';
import type { ConfirmDialogTone } from './ConfirmDialog';

export interface ConfirmationRequest {
    title: ReactNode;
    description: ReactNode;
    confirmLabel: string;
    cancelLabel: string;
    closeLabel: string;
    onConfirm: () => Promise<unknown> | unknown;
    tone?: ConfirmDialogTone;
}

/** Render-once controller for destructive confirmations local to a feature. */
export const useConfirmDialog = () => {
    const [request, setRequest] = useState<ConfirmationRequest | null>(null);
    const [pending, setPending] = useState(false);

    const confirm = async () => {
        if (!request || pending) return;
        setPending(true);
        try {
            await request.onConfirm();
            setRequest(null);
        } catch {
            // Feature mutations own their translated inline/toast error state.
            // Keep the confirmation open so the user can retry or cancel.
        } finally {
            setPending(false);
        }
    };

    const cancel = () => {
        if (!pending) setRequest(null);
    };

    return {
        requestConfirmation: setRequest,
        confirmationOpen: request !== null,
        confirmationDialog: (
            <ConfirmDialog
                open={request !== null}
                title={request?.title ?? ''}
                description={request?.description ?? ''}
                confirmLabel={request?.confirmLabel ?? ''}
                cancelLabel={request?.cancelLabel ?? ''}
                closeLabel={request?.closeLabel ?? ''}
                tone={request?.tone}
                pending={pending}
                onConfirm={() => void confirm()}
                onCancel={cancel}
            />
        ),
    };
};

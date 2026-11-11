import { useEffect } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { useToast } from '../components/feedback/toast';
import { getApiErrorMessage } from '../utils/apiError';
import type { MutationFeedbackMeta } from './mutationFeedback';

const UNDO_TOAST_MS = 10000;

/** Shows the success toast declared by each mutation's `meta`. Mount once inside the work query client. */
export const MutationSuccessFeedback = () => {
    const client = useQueryClient();
    const toast = useToast();
    const { t } = useTranslation();
    useEffect(() => client.getMutationCache().subscribe(event => {
        if (event.type !== 'updated' || event.action.type !== 'success') return;
        const meta = event.mutation.options.meta as MutationFeedbackMeta | undefined;
        if (!meta?.success) return;
        const { data, variables } = event.mutation.state;
        const message = typeof meta.success === 'function' ? meta.success(data, variables) : meta.success;
        if (!message) return;
        const undo = meta.undo?.(data, variables);
        toast.success(message, undo ? {
            actionLabel: t('feedback.undo'),
            durationMs: UNDO_TOAST_MS,
            onAction: async () => {
                try {
                    await undo.run();
                    await client.invalidateQueries();
                    toast.success(undo.done ?? t('feedback.undone'));
                } catch (error) {
                    toast.error(getApiErrorMessage(error, t('feedback.undoFailed')));
                }
            },
        } : undefined);
    }), [client, toast, t]);
    return null;
};

import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { SlideOverDrawer } from '../ui';
import { useConfirmDialog } from '../common/useConfirmDialog';
import type { Iteration } from '../../types/iteration';
import { IterationForm } from './IterationForm';

interface IterationEditorDrawerProps {
    /** The iteration to edit; a new iteration is created when omitted. */
    iteration?: Iteration;
    /** Project the new iteration starts on. */
    defaultProjectId?: number;
    onClose: () => void;
    onSaved: (iteration?: Iteration, iterations?: Iteration[]) => void;
}

/** The iteration form in the slide-over drawer, the one place an iteration is created or edited. */
export const IterationEditorDrawer = ({ iteration, defaultProjectId, onClose, onSaved }: IterationEditorDrawerProps) => {
    const { t } = useTranslation();
    const [formState, setFormState] = useState({ dirty: false, pending: false });
    const { requestConfirmation, confirmationDialog } = useConfirmDialog();

    // Closing by the close button, Escape or the backdrop asks first when there are unsaved changes.
    const requestClose = () => {
        if (!formState.dirty) { onClose(); return; }
        requestConfirmation({
            title: t('iterationForm.discardTitle'),
            description: t('iterationForm.discardBody'),
            confirmLabel: t('iterationForm.discard'),
            cancelLabel: t('iterationForm.keepEditing'),
            closeLabel: t('actions.close'),
            tone: 'danger',
            onConfirm: onClose,
        });
    };

    return (
        <>
            <SlideOverDrawer
                open
                title={iteration ? t('iterations.editIteration') : t('iterations.createIteration')}
                closeLabel={t('actions.close')}
                closeDisabled={formState.pending}
                onClose={requestClose}
            >
                <div className="p-5">
                    <IterationForm
                        initialData={iteration}
                        defaultProjectId={!iteration ? defaultProjectId : undefined}
                        onStateChange={setFormState}
                        onSuccess={onSaved}
                        onCancel={onClose}
                    />
                </div>
            </SlideOverDrawer>
            {confirmationDialog}
        </>
    );
};

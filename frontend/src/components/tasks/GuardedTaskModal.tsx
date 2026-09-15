import type { ComponentProps, ReactNode } from 'react';
import { Modal } from '../common/Modal';
import { TaskForm } from './TaskForm';
import { DraftDismissalDialog } from './DraftDismissalDialog';
import { useDraftDismissal } from './useDraftDismissal';

type FormProps = Omit<ComponentProps<typeof TaskForm>, 'onSuccess' | 'onCancel' | 'onDirtyChange' | 'onPendingChange' | 'onDiscardReady' | 'confirmUnsavedOnCancel'>;

export const GuardedTaskModal = ({ title, closeLabel, onClose, ...form }: FormProps & {
    title: ReactNode; closeLabel: string; onClose: () => void;
}) => {
    const guard = useDraftDismissal(onClose);
    return <>
        <Modal open title={title} closeLabel={closeLabel} onClose={guard.requestClose} closeDisabled={guard.pending}>
            <TaskForm {...form} onSuccess={guard.complete} onCancel={guard.requestClose}
                onDirtyChange={guard.setDirty} onPendingChange={guard.setPending} onDiscardReady={guard.onDiscardReady} confirmUnsavedOnCancel={false} />
        </Modal>
        <DraftDismissalDialog guard={guard} />
    </>;
};

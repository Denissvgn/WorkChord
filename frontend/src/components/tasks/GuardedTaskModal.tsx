import { useId, useState, type ComponentProps, type ReactNode } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import type { Task } from '../../types/task';
import { Modal } from '../common/Modal';
import { TaskForm } from './TaskForm';
import { DraftDismissalDialog } from './DraftDismissalDialog';
import { useDraftDismissal } from './useDraftDismissal';
import { QueryErrorState, QueryLoadingState } from '../feedback/QueryState';
import { readTaskEditorSnapshot, keepNewestTaskSnapshot } from './taskEditorSnapshot';

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

const OpenedTaskModal = ({ initialData, onClose }: { initialData: Task; onClose: () => void }) => {
    const { t } = useTranslation();
    // One coherent read initializes this opening; background data never rebases an active draft.
    const [snapshot] = useState(initialData);
    return <GuardedTaskModal title={snapshot.title} closeLabel={t('actions.close')}
        iterationId={snapshot.iteration_id} initialData={snapshot} onClose={onClose} />;
};

export const CurrentTaskModal = ({ taskId, onClose }: { taskId: number; onClose: () => void }) => {
    const { t } = useTranslation();
    const openingId = useId();
    // feedback-policy: query loading,error,retry,empty - each opening waits for its authoritative read.
    const snapshot = useQuery({ queryKey: ['taskEditor', taskId, openingId], gcTime: 0, staleTime: 0,
        refetchOnWindowFocus: false,
        queryFn: ({ signal }) => readTaskEditorSnapshot(taskId, signal), structuralSharing: keepNewestTaskSnapshot });
    if (snapshot.data && !snapshot.isError) return <OpenedTaskModal initialData={snapshot.data} onClose={onClose} />;
    return <Modal open title={t('taskEditor.taskCode', { id: taskId })} closeLabel={t('actions.close')} onClose={onClose}>
        {snapshot.isLoading && <QueryLoadingState />}
        {snapshot.isError && <QueryErrorState error={snapshot.error} fallback={t('teamwork.taskUnavailable')}
            onRetry={() => void snapshot.refetch()} />}
    </Modal>;
};

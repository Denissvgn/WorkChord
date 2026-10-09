import { useId } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { exportService } from '../../services/exportService';
import type { ObservedRevisions } from '../../services/planningInputService';
import { useActiveMount } from '../tasks/useDraftDismissal';
import { Modal } from '../common/Modal';
import { Button } from '../common/Button';
import { QueryErrorState, QueryLoadingState } from '../feedback/QueryState';
import { getApiErrorMessage } from '../../utils/apiError';

export const IterationImportDialog = ({ file, iterationId, onClose }: { file: File; iterationId?: number; onClose: () => void }) => {
    const { t } = useTranslation();
    const opening = useId();
    const active = useActiveMount();
    const queryClient = useQueryClient();
    // feedback-policy: query loading,error,retry,empty
    const preview = useQuery({ queryKey: ['iterationImportPreview', opening, iterationId],
        queryFn: ({ signal }) => exportService.previewImport(file, iterationId, signal),
        staleTime: Infinity, gcTime: 0, refetchOnWindowFocus: false, retry: false });
    // feedback-policy: mutation pending,inline
    const write = useMutation({ mutationFn: (revisions: ObservedRevisions) => iterationId
        ? exportService.importIntoIteration(iterationId, file, revisions) : exportService.importIteration(file, revisions),
        onSuccess: () => { if (!active()) return;
            for (const root of ['iterations', 'tasks', 'team', 'gantt']) void queryClient.invalidateQueries({ queryKey: [root] });
            onClose();
        }, onError: () => undefined });
    return <Modal open title={t('planningInput.preview')} description={file.name} closeLabel={t('actions.close')}
        closeDisabled={write.isPending} onClose={onClose} footer={<div className="flex flex-wrap justify-end gap-2">
            <Button type="button" variant="ghost" disabled={write.isPending} onClick={onClose}>{t('actions.cancel')}</Button>
            <Button type="button" variant="secondary" disabled={write.isPending || preview.isFetching}
                onClick={() => void preview.refetch()}>{t('planningInput.reviewAgain')}</Button>
            <Button type="button" disabled={!preview.data?.complete || preview.isError || preview.isFetching} isLoading={write.isPending}
                onClick={() => { if (preview.data) write.mutate(preview.data.expected_revisions); }}>{t('actions.import')}</Button>
        </div>}>
        {preview.isFetching && <QueryLoadingState />}
        {preview.isError && <QueryErrorState error={preview.error} onRetry={() => void preview.refetch()} />}
        {write.isError && <p role="alert" className="text-sm text-feedback-danger-foreground">{getApiErrorMessage(write.error, t('iterations.importFailed'))}</p>}
        {preview.data && <p className="text-sm text-content-secondary">{t('planningInput.previewReady')}</p>}
    </Modal>;
};

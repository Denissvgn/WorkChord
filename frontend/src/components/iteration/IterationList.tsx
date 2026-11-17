import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { Trash2, Download, FolderOpen } from 'lucide-react';
import { useState } from 'react';
import { Link } from 'react-router-dom';
import { iterationService } from '../../services/iterationService';
import { planningInputService, type ObservedRevisions } from '../../services/planningInputService';
import { exportService } from '../../services/exportService';
import { Button } from '../common/Button';
import { ConfirmDialog } from '../common/ConfirmDialog';
import { useIterationStore } from '../../store/iterationStore';
import type { Iteration } from '../../types/iteration';
import { useToast } from '../feedback/toast';
import { getApiErrorMessage } from '../../utils/apiError';
import { formatDate } from '../../utils/formatDate';
import { IterationCapacityLine } from './IterationCapacityLine';
import { useWorkScope } from '../../features/scope/useWorkScope';

interface IterationListProps {
    /** Makes the iteration the one in scope and shows it in Plan. */
    onOpen: (iteration: Iteration) => void;
    onEdit: (iteration: Iteration) => void;
    /** Lists only this project's iterations; every iteration when omitted. */
    projectId?: number;
}

export const IterationList = ({ onOpen, onEdit, projectId }: IterationListProps) => {
    const queryClient = useQueryClient();
    const { selectedIterationId, setSelectedIterationId } = useIterationStore();
    const { iteration: scopeIteration } = useWorkScope();
    const { t, i18n } = useTranslation();
    const toast = useToast();
    const [deleteContext, setDeleteContext] = useState<{ id: number; revisions: ObservedRevisions; name: string; taskCount: number | null } | null>(null);
    const [deleteConfirmation, setDeleteConfirmation] = useState('');
    const [deletingId, setDeletingId] = useState<number | null>(null);
    const { data: allIterations, isLoading, isError, error, refetch } = useQuery({
        queryKey: ['iterations'],
        queryFn: iterationService.getAll,
    });
    const iterations = projectId === undefined ? allIterations : allIterations?.filter(item => item.project_id === projectId);

    const deleteMutation = useMutation({
        mutationFn: ({ id, revisions }: { id: number; revisions: ObservedRevisions }) => iterationService.delete(id, revisions),
        onSuccess: (_data, { id: deletedId }) => {
            // Invalidate task cache for the deleted iteration
            queryClient.invalidateQueries({ queryKey: ['tasks', deletedId] });
            queryClient.invalidateQueries({ queryKey: ['team', deletedId] });
            queryClient.invalidateQueries({ queryKey: ['gantt', deletedId] });
            // Reset selected iteration if it was the deleted one
            if (selectedIterationId === deletedId) {
                setSelectedIterationId(0);
            }
            toast.success(t('feedback.iterationDeleteSuccess'));
            setDeletingId(null);
        },
        onError: (error: unknown) => {
            toast.error(getApiErrorMessage(error, t('feedback.iterationDeleteFailed')));
        },
        onSettled: () => {
            // Always invalidate after delete attempt (success or failure)
            queryClient.invalidateQueries({ queryKey: ['iterations'] });
        },
    });

    const handleExport = async (id: number, name: string) => {
        try {
            const blob = await exportService.exportIteration(id);
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${name.replace(/\s+/g, '_')}_export.json`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            toast.success(t('feedback.iterationExportSuccess'));
        } catch (error: unknown) {
            toast.error(getApiErrorMessage(error, t('feedback.iterationExportFailed')));
        }
    };

    const openDelete = async (id: number) => {
        try {
            const observed = await planningInputService.readInitial<Iteration>('iteration', id);
            // The task count makes the loss explicit; the dialog still works when it cannot be read.
            const taskCount = await iterationService.getPlanningReadiness(id)
                .then(summary => summary.task_count)
                .catch(() => null);
            const name = iterations?.find(item => item.id === id)?.name ?? '';
            setDeleteConfirmation('');
            setDeleteContext({ id, revisions: observed.expected_revisions, name, taskCount }); setDeletingId(id);
        } catch (cause) { toast.error(getApiErrorMessage(cause, t('feedback.iterationDeleteFailed'))); }
    };

    if (isLoading) return <p role="status" className="text-sm text-content-secondary">{t('iterations.loading')}</p>;
    if (isError) {
        // The sentence says what failed; the server's detail, when it differs, follows it.
        const detail = getApiErrorMessage(error, '');
        return (
            <div role="alert" className="rounded-md border border-feedback-danger-border bg-feedback-danger-muted p-4 text-feedback-danger-foreground">
                <p className="font-medium">{t('iterations.loadFailed')}</p>
                {detail && detail !== t('iterations.loadFailed') && <p className="mt-1 text-sm">{detail}</p>}
                <Button className="mt-3" variant="secondary" onClick={() => void refetch()}>{t('queryFeedback.retry')}</Button>
            </div>
        );
    }

    return (
        <div>
            {iterations?.length === 0 && (
                <p className="m-5 rounded-lg border border-dashed border-border bg-surface-muted px-4 py-10 text-center text-content-tertiary">
                    {t('iterations.noIterations')}
                </p>
            )}
            <ul className="divide-y divide-border-subtle" aria-label={t('iterations.allIterations')}>
                {iterations?.map((iteration) => (
                    <li
                        key={iteration.id}
                        className="space-y-3 px-5 py-4"
                        aria-current={iteration.id === scopeIteration ? 'true' : undefined}
                    >
                        <div className="flex items-start justify-between gap-3">
                            <div className="min-w-0">
                                <h3 className="truncate font-semibold">{iteration.name}</h3>
                                <p className="flex flex-wrap items-center gap-x-2 text-sm text-content-secondary">
                                    <span>{formatDate(iteration.start_date, i18n.language)} – {formatDate(iteration.end_date, i18n.language)}</span>
                                    <span aria-hidden="true">·</span>
                                    <span>{t('units.days', { count: iteration.working_days })}</span>
                                </p>
                                <p className="text-sm text-content-secondary">
                                    {iteration.project ? (
                                        <Link
                                            to={`/projects/${iteration.project.id}`}
                                            className="inline-flex min-w-0 items-center gap-1 font-medium text-action hover:underline"
                                            aria-label={t('iterations.openProject', { project: iteration.project.name })}
                                        >
                                            <FolderOpen aria-hidden="true" className="h-3.5 w-3.5 shrink-0" />
                                            <span className="truncate">{iteration.project.name}</span>
                                        </Link>
                                    ) : (
                                        <span>{t('iterations.unscoped')}</span>
                                    )}
                                </p>
                            </div>
                            {iteration.id === scopeIteration && (
                                <span className="pill sm shrink-0">{t('iterations.inScope')}</span>
                            )}
                        </div>

                        <IterationCapacityLine iterationId={iteration.id} />

                        <div className="flex flex-wrap items-center gap-1">
                            <Button
                                variant="secondary"
                                size="sm"
                                onClick={() => onOpen(iteration)}
                                aria-label={t('iterations.openNamed', { name: iteration.name })}
                            >
                                {t('iterations.open')}
                            </Button>
                            <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => onEdit(iteration)}
                                aria-label={t('iterations.editNamed', { name: iteration.name })}
                            >
                                {t('actions.edit')}
                            </Button>
                            <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => void handleExport(iteration.id, iteration.name)}
                                aria-label={t('iterations.exportNamed', { name: iteration.name })}
                            >
                                <Download aria-hidden="true" className="h-4 w-4" />
                                {t('iterations.export')}
                            </Button>
                            <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => void openDelete(iteration.id)}
                                aria-label={t('iterations.deleteNamed', { name: iteration.name })}
                                className="ml-auto text-feedback-danger-foreground hover:bg-feedback-danger-muted"
                            >
                                <Trash2 aria-hidden="true" className="h-4 w-4" />
                                {t('actions.delete')}
                            </Button>
                        </div>
                    </li>
                ))}
            </ul>

            <ConfirmDialog
                open={deletingId !== null}
                title={t('iterations.deleteNamedTitle', { name: deleteContext?.name ?? '' })}
                description={<>
                    <p>{deleteContext?.taskCount == null
                        ? t('iterations.deleteBody')
                        : t('iterations.deleteBodyWithCount', { count: deleteContext.taskCount })}</p>
                    {(deleteContext?.taskCount ?? 1) > 0 && deleteContext?.name && (
                        <label className="mt-3 block text-sm">
                            <span className="field-lbl">{t('iterations.deleteTypeName', { name: deleteContext.name })}</span>
                            <input
                                className="input mt-1 w-full"
                                value={deleteConfirmation}
                                onChange={event => setDeleteConfirmation(event.target.value)}
                                autoComplete="off"
                            />
                        </label>
                    )}
                    {deleteMutation.isError && <p role="alert">{getApiErrorMessage(deleteMutation.error, t('feedback.iterationDeleteFailed'))}<Button type="button" variant="secondary" disabled={deleteMutation.isPending} onClick={() => { if (deletingId) void openDelete(deletingId); }}>{t('planningInput.reviewAgain')}</Button></p>}</>}
                confirmLabel={deleteContext?.taskCount
                    ? t('iterations.deleteConfirmWithCount', { count: deleteContext.taskCount })
                    : t('iterations.deleteConfirm')}
                cancelLabel={t('actions.cancel')}
                closeLabel={t('actions.close')}
                pending={deleteMutation.isPending}
                confirmDisabled={(deleteContext?.taskCount ?? 1) > 0 && Boolean(deleteContext?.name)
                    && deleteConfirmation.trim() !== deleteContext?.name.trim()}
                onCancel={() => setDeletingId(null)}
                onConfirm={() => { if (deleteContext) deleteMutation.mutate(deleteContext); }}
            />
        </div>
    );
};

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { Calendar, Trash2, ArrowRight, Download, Upload, FolderOpen } from 'lucide-react';
import { useState, useRef } from 'react';
import { Link } from 'react-router-dom';
import { iterationService } from '../../services/iterationService';
import { exportService } from '../../services/exportService';
import { Button } from '../common/Button';
import { ConfirmDialog } from '../common/ConfirmDialog';
import { useIterationStore } from '../../store/iterationStore';
import type { Iteration } from '../../types/iteration';
import { useToast } from '../feedback/toast';
import { getApiErrorMessage } from '../../utils/apiError';
import { formatDate } from '../../utils/formatDate';

interface IterationListProps {
    onEdit?: (iteration: Iteration) => void;
}

export const IterationList = ({ onEdit }: IterationListProps) => {
    const queryClient = useQueryClient();
    const { selectedIterationId, setSelectedIterationId } = useIterationStore();
    const { t } = useTranslation();
    const toast = useToast();
    const [deletingId, setDeletingId] = useState<number | null>(null);
    const [importingId, setImportingId] = useState<number | null>(null);
    const importFileInputRef = useRef<HTMLInputElement>(null);
    const { data: iterations, isLoading, isError, error, refetch } = useQuery({
        queryKey: ['iterations'],
        queryFn: iterationService.getAll,
    });

    const deleteMutation = useMutation({
        mutationFn: iterationService.delete,
        onSuccess: (_data, deletedId) => {
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

    const handleImportClick = (iterationId: number) => {
        setImportingId(iterationId);
        importFileInputRef.current?.click();
    };

    const handleImportFile = async (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0] && importingId) {
            try {
                await exportService.importIntoIteration(importingId, e.target.files[0]);
                queryClient.invalidateQueries({ queryKey: ['iterations'] });
                queryClient.invalidateQueries({ queryKey: ['tasks', importingId] });
                queryClient.invalidateQueries({ queryKey: ['team', importingId] });
                queryClient.invalidateQueries({ queryKey: ['gantt', importingId] });
                toast.success(t('feedback.iterationImportSuccess'));
            } catch (error: unknown) {
                toast.error(getApiErrorMessage(error, t('feedback.iterationImportFailed')));
            }
            // Reset input and state
            e.target.value = '';
            setImportingId(null);
        }
    };

    if (isLoading) return <div>{t('common.loading')}</div>;
    if (isError) return (
        <div role="alert" className="rounded-md border border-feedback-danger-border bg-feedback-danger-muted p-4 text-feedback-danger-foreground">
            <p>{getApiErrorMessage(error, t('feedback.iterationDeleteFailed'))}</p>
            <Button className="mt-3" variant="secondary" onClick={() => void refetch()}>{t('queryFeedback.retry')}</Button>
        </div>
    );

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Hidden file input for import */}
            <input
                type="file"
                ref={importFileInputRef}
                className="hidden"
                accept=".json"
                onChange={handleImportFile}
            />
            {iterations?.map((iteration) => (
                <div key={iteration.id} className="card hover:shadow-md transition-shadow">
                    <div className="flex items-start justify-between mb-4">
                        <div className="flex items-center gap-3">
                            <div className="p-2 bg-feedback-purple-muted rounded-lg text-feedback-purple-foreground">
                                <Calendar className="w-6 h-6" />
                            </div>
                            <div>
                                <h3 className="font-semibold text-lg">{iteration.name}</h3>
                                <div className="flex items-center text-sm text-content-secondary gap-1">
                                    <span>{formatDate(iteration.start_date)}</span>
                                    <ArrowRight className="w-3 h-3" />
                                    <span>{formatDate(iteration.end_date)}</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="space-y-2 mb-6">
                        <div className="flex items-center justify-between gap-3 text-sm">
                            <span className="text-content-secondary">{t('iterations.projectScope')}</span>
                            {iteration.project ? (
                                <Link
                                    to={`/projects/${iteration.project.id}`}
                                    className="inline-flex min-w-0 items-center gap-1 font-medium text-action hover:text-action hover:underline"
                                    aria-label={t('iterations.openProject', { project: iteration.project.name })}
                                >
                                    <FolderOpen className="h-3.5 w-3.5 shrink-0 text-action" />
                                    <span className="truncate">{iteration.project.name}</span>
                                </Link>
                            ) : (
                                <span className="inline-flex min-w-0 items-center gap-1 font-medium text-content-primary">
                                    <FolderOpen className="h-3.5 w-3.5 shrink-0 text-content-tertiary" />
                                    <span className="truncate">{t('iterations.unscoped')}</span>
                                </span>
                            )}
                        </div>
                        {!iteration.project && (
                            <p className="text-xs text-content-secondary">{t('iterations.unscopedHelp')}</p>
                        )}
                        <div className="flex justify-between text-sm">
                            <span className="text-content-secondary">{t('iterations.workingDays')}</span>
                            <span className="font-medium">{t('units.days', { count: iteration.working_days })}</span>
                        </div>
                    </div>

                    <div className="flex justify-end gap-2 pt-4 border-t border-border-subtle">
                        <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleImportClick(iteration.id)}
                            title={t('iterations.importJson')}
                            aria-label={t('iterations.importJson')}
                        >
                            <Download className="w-4 h-4" />
                        </Button>
                        <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleExport(iteration.id, iteration.name)}
                            title={t('iterations.exportJson')}
                            aria-label={t('iterations.exportJson')}
                        >
                            <Upload className="w-4 h-4" />
                        </Button>
                        {onEdit && (
                            <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => onEdit(iteration)}
                                className="text-action hover:text-action hover:bg-action-muted"
                            >
                                {t('actions.edit')}
                            </Button>
                        )}
                        <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => setDeletingId(iteration.id)}
                            aria-label={t('actions.delete')}
                                className="text-feedback-danger-foreground hover:bg-feedback-danger-muted"
                        >
                            <Trash2 className="w-4 h-4" />
                        </Button>
                    </div>
                </div>
            ))}

            {iterations?.length === 0 && (
                <div className="col-span-full text-center py-12 text-content-tertiary bg-surface-muted rounded-lg border border-dashed border-border">
                    {t('iterations.noIterations')}
                </div>
            )}

            <ConfirmDialog
                open={deletingId !== null}
                title={t('iterations.deleteTitle')}
                description={t('iterations.deleteBody')}
                confirmLabel={t('actions.delete')}
                cancelLabel={t('actions.cancel')}
                closeLabel={t('actions.close')}
                pending={deleteMutation.isPending}
                onCancel={() => setDeletingId(null)}
                onConfirm={() => { if (deletingId !== null) deleteMutation.mutate(deletingId); }}
            />
        </div>
    );
};

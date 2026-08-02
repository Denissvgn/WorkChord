import { useMemo, useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { CalendarDays, Link2, Pencil, Plus, Unlink } from 'lucide-react';
import { Button } from '../common/Button';
import { ConfirmDialog } from '../common/ConfirmDialog';
import { Modal } from '../common/Modal';
import { IterationForm } from '../iteration/IterationForm';
import { InlineEmptyState, SectionCard } from '../ui';
import { iterationService } from '../../services/iterationService';
import type { Iteration } from '../../types/iteration';
import { formatDate } from '../../utils/formatDate';
import { QueryErrorState } from '../feedback/QueryState';

interface ProjectIterationsSectionProps {
    projectId: number;
    projectName: string;
    iterations: Iteration[];
    isLoading: boolean;
}

type IterationEditorState =
    | { mode: 'create'; iteration: null }
    | { mode: 'edit'; iteration: Iteration };

export const ProjectIterationsSection = ({
    projectId,
    projectName,
    iterations,
    isLoading,
}: ProjectIterationsSectionProps) => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const [editor, setEditor] = useState<IterationEditorState | null>(null);
    const [attachOpen, setAttachOpen] = useState(false);
    const [attachIterationId, setAttachIterationId] = useState('');
    const [removeTarget, setRemoveTarget] = useState<Iteration | null>(null);
    const [actionError, setActionError] = useState<string | null>(null);

    const { data: allIterations = [], error: allIterationsError, refetch: refetchAllIterations } = useQuery({
        queryKey: ['iterations'],
        queryFn: iterationService.getAll,
    });

    const unscopedIterations = useMemo(
        () => allIterations.filter(iteration => iteration.project_id === null || iteration.project_id === undefined),
        [allIterations],
    );

    const invalidateProjectIterationScope = (iterationId?: number) => {
        queryClient.invalidateQueries({ queryKey: ['projectIterations', projectId] });
        queryClient.invalidateQueries({ queryKey: ['projectIterations'] });
        queryClient.invalidateQueries({ queryKey: ['iterations'] });
        queryClient.invalidateQueries({ queryKey: ['projects'] });
        queryClient.invalidateQueries({ queryKey: ['projectSummary', projectId] });
        queryClient.invalidateQueries({ queryKey: ['projectTasks', projectId] });
        queryClient.invalidateQueries({ queryKey: ['tasks'] });
        queryClient.invalidateQueries({ queryKey: ['gantt'] });
        if (iterationId) {
            queryClient.invalidateQueries({ queryKey: ['iteration', iterationId] });
        }
    };

    const attachMutation = useMutation({
        mutationFn: (iterationId: number) => iterationService.update(iterationId, { project_id: projectId }),
        onSuccess: iteration => {
            setAttachOpen(false);
            setAttachIterationId('');
            setActionError(null);
            invalidateProjectIterationScope(iteration.id);
        },
        onError: () => {
            setActionError(t('projectIterations.attachError'));
        },
    });

    const removeMutation = useMutation({
        mutationFn: (iterationId: number) => iterationService.update(iterationId, { project_id: null }),
        onSuccess: iteration => {
            setRemoveTarget(null);
            setActionError(null);
            invalidateProjectIterationScope(iteration.id);
        },
        onError: () => {
            setActionError(t('projectIterations.removeError'));
        },
    });

    const handleFormSuccess = (iteration?: Iteration) => {
        setEditor(null);
        setActionError(null);
        invalidateProjectIterationScope(iteration?.id);
    };

    const selectedAttachId = attachIterationId ? Number(attachIterationId) : null;
    const isMutating = attachMutation.isPending || removeMutation.isPending;

    return (
        <>
            <SectionCard
                icon={<CalendarDays className="h-4 w-4 text-action" />}
                title={t('projectIterations.title')}
                description={t('projectIterations.description')}
                count={<span className="rounded-full bg-surface-subtle px-1.5 text-wc-micro font-bold tabular-nums text-content-secondary">{iterations.length}</span>}
                actions={(
                    <div className="flex flex-wrap gap-2">
                        <Button size="sm" variant="outline" onClick={() => setAttachOpen(true)}>
                            <Link2 className="mr-1.5 h-3.5 w-3.5" />
                            {t('projectIterations.attach')}
                        </Button>
                        <Button size="sm" onClick={() => setEditor({ mode: 'create', iteration: null })}>
                            <Plus className="mr-1.5 h-3.5 w-3.5" />
                            {t('projectIterations.create')}
                        </Button>
                    </div>
                )}
                testId="project-scoped-iterations-section"
            >
                {actionError && (
                    <div className="mb-3 rounded-md border border-feedback-danger-border bg-feedback-danger-muted px-3 py-2 text-sm text-feedback-danger-foreground">
                        {actionError}
                    </div>
                )}

                {isLoading ? (
                    <div className="rounded-md bg-surface-muted p-4 text-sm text-content-secondary">{t('projectIterations.loading')}</div>
                ) : iterations.length === 0 ? (
                    <InlineEmptyState
                        title={t('projectIterations.emptyTitle')}
                        description={t('projectIterations.emptyDescription')}
                    />
                ) : (
                    <div className="divide-y divide-border-subtle rounded-md border border-border">
                        {iterations.map(iteration => (
                            <div
                                key={iteration.id}
                                data-testid={`project-iteration-row-${iteration.id}`}
                                className="flex flex-wrap items-center justify-between gap-3 px-4 py-3"
                            >
                                <div className="min-w-0">
                                    <p className="font-medium text-content-primary">{iteration.name}</p>
                                    <p className="mt-1 text-xs text-content-secondary">
                                        {t('projectIterations.dateRange', {
                                            start: formatDate(iteration.start_date),
                                            end: formatDate(iteration.end_date),
                                        })}
                                    </p>
                                </div>
                                <div className="flex flex-wrap items-center gap-2">
                                    <span className="rounded-full border border-border bg-surface-muted px-2 py-0.5 text-xs font-medium text-content-primary">
                                        {t('projectIterations.workingDays', { count: iteration.working_days })}
                                    </span>
                                    <Button
                                        size="sm"
                                        variant="ghost"
                                        onClick={() => setEditor({ mode: 'edit', iteration })}
                                    >
                                        <Pencil className="mr-1.5 h-3.5 w-3.5" />
                                        {t('actions.edit')}
                                    </Button>
                                    <Button
                                        size="sm"
                                        variant="ghost"
                                        onClick={() => setRemoveTarget(iteration)}
                                        disabled={isMutating}
                                    >
                                        <Unlink className="mr-1.5 h-3.5 w-3.5" />
                                        {t('projectIterations.remove')}
                                    </Button>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </SectionCard>

            <Modal
                open={editor !== null}
                title={editor?.mode === 'create' ? t('projectIterations.createTitle') : t('projectIterations.editTitle')}
                closeLabel={t('actions.close')}
                onClose={() => setEditor(null)}
            >
                {editor && (
                    <IterationForm
                        initialData={editor.iteration ?? undefined}
                        lockedProject={{ id: projectId, name: projectName }}
                        onSuccess={handleFormSuccess}
                        onCancel={() => setEditor(null)}
                    />
                )}
            </Modal>

            <Modal open={attachOpen} title={t('projectIterations.attachTitle')} closeLabel={t('actions.close')} onClose={() => setAttachOpen(false)}>
                {attachOpen && (
        <div className="space-y-4">
            {allIterationsError && <QueryErrorState error={allIterationsError} onRetry={() => void refetchAllIterations()} fallback={t('queryFeedback.optionLoadFailed')} />}
                        <div>
                            <label className="mb-1 block text-sm font-medium text-content-primary" htmlFor="attach-unscoped-iteration">
                                {t('projectIterations.unscopedIteration')}
                            </label>
                            <select
                                id="attach-unscoped-iteration"
                                value={attachIterationId}
                                onChange={event => setAttachIterationId(event.target.value)}
                                className="w-full rounded-md border border-border-strong bg-surface-card px-3 py-2 shadow-sm focus:outline-none focus:ring-1 focus:ring-focus"
                            >
                                <option value="">{t('projectIterations.selectUnscoped')}</option>
                                {unscopedIterations.map(iteration => (
                                    <option key={iteration.id} value={iteration.id}>
                                        {iteration.name}
                                    </option>
                                ))}
                            </select>
                            {unscopedIterations.length === 0 && (
                                <p className="mt-2 text-sm text-content-secondary">{t('projectIterations.noUnscoped')}</p>
                            )}
                        </div>
                        <div className="flex justify-end gap-2 border-t pt-4">
                            <Button type="button" variant="ghost" onClick={() => setAttachOpen(false)}>
                                {t('actions.cancel')}
                            </Button>
                            <Button
                                type="button"
                                isLoading={attachMutation.isPending}
                                disabled={!selectedAttachId}
                                onClick={() => selectedAttachId && attachMutation.mutate(selectedAttachId)}
                            >
                                {t('projectIterations.attachConfirm')}
                            </Button>
                        </div>
                    </div>
                )}
            </Modal>

            <ConfirmDialog
                open={removeTarget !== null}
                title={t('projectIterations.removeTitle')}
                description={<>{removeTarget && t('projectIterations.removeBody', { iteration: removeTarget.name, project: projectName })}<span className="mt-2 block">{t('projectIterations.taskLinksUnchanged')}</span></>}
                confirmLabel={t('projectIterations.remove')}
                cancelLabel={t('actions.cancel')}
                closeLabel={t('actions.close')}
                pending={removeMutation.isPending}
                onCancel={() => setRemoveTarget(null)}
                onConfirm={() => { if (removeTarget) removeMutation.mutate(removeTarget.id); }}
                tone="warning"
            />
        </>
    );
};

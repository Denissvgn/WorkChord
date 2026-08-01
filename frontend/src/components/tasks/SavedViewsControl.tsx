import i18n from '../../i18n/i18n';
import { useEffect, useMemo, useRef, useState } from 'react';
import type { FormEvent } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { AlertTriangle, Copy, Save, Trash2 } from 'lucide-react';
import { Button } from '../common/Button';
import { Input } from '../common/Input';
import { Modal } from '../common/Modal';
import { useConfirmDialog } from '../common/useConfirmDialog';
import { savedViewService } from '../../services/savedViewService';
import { sessionService } from '../../services/sessionService';
import { getApiErrorMessage } from '../../utils/apiError';
import type { SavedView, SavedViewScope } from '../../types/savedView';
import type { TaskFilters } from './TaskFiltersBar';
import type { SortKey } from './TaskList';
import { savedViewDisplay } from '../../i18n/seedDisplay';
import { QueryErrorState } from '../feedback/QueryState';

const t = i18n.t.bind(i18n);

type EditableScope = Exclude<SavedViewScope, 'system'>;
type FormMode = 'create' | 'duplicate';

interface SavedViewsControlProps {
    filters: TaskFilters;
    sortKey: SortKey;
    selectedViewId: number | null;
    requestedViewId?: number | null;
    onSelectedViewIdChange: (viewId: number | null) => void;
    onApplyView: (view: SavedView) => void;
}

const sortScopeLabel = (scope: SavedViewScope) => {
    if (scope === 'personal') return t('surfaces.savedViews.personal');
    if (scope === 'shared') return t('surfaces.savedViews.shared');
    return t('surfaces.savedViews.system');
};

export const SavedViewsControl = ({
    filters,
    sortKey,
    selectedViewId,
    requestedViewId,
    onSelectedViewIdChange,
    onApplyView,
}: SavedViewsControlProps) => {
    const queryClient = useQueryClient();
    const [formMode, setFormMode] = useState<FormMode | null>(null);
    const [formName, setFormName] = useState('');
    const [formDescription, setFormDescription] = useState('');
    const [formScope, setFormScope] = useState<EditableScope>('personal');
    const [formError, setFormError] = useState<string | null>(null);
    const [statusMessage, setStatusMessage] = useState<string | null>(null);
    const appliedRequestedViewIdRef = useRef<number | null>(null);
    const formNameRef = useRef<HTMLInputElement>(null);
    const { requestConfirmation, confirmationDialog } = useConfirmDialog();

    const { data: session, error: sessionError, refetch: refetchSession } = useQuery({
        queryKey: ['session', 'whoami'],
        queryFn: sessionService.getWhoAmI,
    });

    const { data: savedViews = [], isLoading, error: viewsError, refetch: refetchViews } = useQuery({
        queryKey: ['saved-views', 'tasks'],
        queryFn: () => savedViewService.getAll({ view_type: 'tasks' }),
    });

    const selectedView = useMemo(
        () => savedViews.find(view => view.id === selectedViewId) ?? null,
        [savedViews, selectedViewId],
    );

    const canMutateSelected = Boolean(
        selectedView &&
        selectedView.is_valid &&
        selectedView.scope !== 'system' &&
        selectedView.created_by_session_id === session?.id,
    );

    const currentViewPayload = {
        filters_json: filters as unknown as Record<string, unknown>,
        sort_json: { sortKey },
        columns_json: {},
    };

    useEffect(() => {
        if (!requestedViewId || appliedRequestedViewIdRef.current === requestedViewId) {
            return;
        }

        const view = savedViews.find(candidate => candidate.id === requestedViewId);
        if (!view || !view.is_valid) {
            return;
        }

        appliedRequestedViewIdRef.current = requestedViewId;
        onSelectedViewIdChange(view.id);
        onApplyView(view);
    }, [requestedViewId, savedViews, onApplyView, onSelectedViewIdChange]);

    const createMutation = useMutation({
        mutationFn: savedViewService.create,
    });

    const updateMutation = useMutation({
        mutationFn: ({ id, data }: { id: number; data: Parameters<typeof savedViewService.update>[1] }) =>
            savedViewService.update(id, data),
    });

    const deleteMutation = useMutation({
        mutationFn: savedViewService.delete,
    });

    const duplicateMutation = useMutation({
        mutationFn: ({ id, data }: { id: number; data: Parameters<typeof savedViewService.duplicate>[1] }) =>
            savedViewService.duplicate(id, data),
    });

    const invalidateSavedViews = async () => {
        await queryClient.invalidateQueries({ queryKey: ['saved-views', 'tasks'] });
    };

    const resetForm = () => {
        setFormMode(null);
        setFormName('');
        setFormDescription('');
        setFormScope('personal');
        setFormError(null);
    };

    const openCreateForm = () => {
        setFormMode('create');
        setFormName('');
        setFormDescription('');
        setFormScope('personal');
        setFormError(null);
    };

    const openDuplicateForm = () => {
        if (!selectedView) return;
        setFormMode('duplicate');
        setFormName(`Copy of ${selectedView.name}`.slice(0, 255));
        setFormDescription(selectedView.description ?? '');
        setFormScope('personal');
        setFormError(null);
    };

    const handleViewSelect = (viewId: string) => {
        if (!viewId) {
            onSelectedViewIdChange(null);
            return;
        }

        const view = savedViews.find(candidate => candidate.id === Number(viewId));
        if (!view || !view.is_valid) return;

        onSelectedViewIdChange(view.id);
        onApplyView(view);
        setStatusMessage(t('surfaces.savedViews.appliedSavedView'));
    };

    const handleSubmitForm = async (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        const name = formName.trim();
        if (!name) {
            setFormError(t('surfaces.savedViews.nameIsRequired'));
            return;
        }

        try {
            const savedView = formMode === 'create'
                ? await createMutation.mutateAsync({
                    name,
                    description: formDescription.trim() || null,
                    view_type: 'tasks',
                    scope: formScope,
                    ...currentViewPayload,
                })
                : selectedView
                    ? await duplicateMutation.mutateAsync({
                        id: selectedView.id,
                        data: {
                            name,
                            description: formDescription.trim() || null,
                            scope: formScope,
                        },
                    })
                    : null;

            if (savedView) {
                await invalidateSavedViews();
                onSelectedViewIdChange(savedView.id);
                setStatusMessage(formMode === 'create' ? t('surfaces.savedViews.savedViewCreated') : t('surfaces.savedViews.savedViewDuplicated'));
            }
            resetForm();
        } catch (error) {
            setFormError(getApiErrorMessage(error, t('surfaces.savedViews.failedToSaveView')));
        }
    };

    const handleUpdateSelected = async () => {
        if (!selectedView || !canMutateSelected) return;
        try {
            const updated = await updateMutation.mutateAsync({
                id: selectedView.id,
                data: currentViewPayload,
            });
            await invalidateSavedViews();
            onSelectedViewIdChange(updated.id);
            setStatusMessage(t('surfaces.savedViews.savedViewUpdated'));
        } catch (error) {
            setStatusMessage(getApiErrorMessage(error, t('surfaces.savedViews.failedToUpdateView')));
        }
    };

    const handleDeleteSelected = () => {
        if (!selectedView || !canMutateSelected) return;
        requestConfirmation({
            title: t('surfaces.savedViews.delete'),
            description: t('surfaces.savedViews.deleteSelectedSavedView'),
            confirmLabel: t('surfaces.savedViews.delete'),
            cancelLabel: t('surfaces.savedViews.cancel'),
            closeLabel: t('actions.close'),
            onConfirm: async () => {
                try {
                    await deleteMutation.mutateAsync(selectedView.id);
                    await invalidateSavedViews();
                    onSelectedViewIdChange(null);
                    setStatusMessage(t('surfaces.savedViews.savedViewDeleted'));
                } catch (error) {
                    setStatusMessage(getApiErrorMessage(error, t('surfaces.savedViews.failedToDeleteView')));
                    throw error;
                }
            },
        });
    };

    return (
        <div className="space-y-3">
            {(sessionError || viewsError) && <QueryErrorState className="mb-3" error={sessionError ?? viewsError} onRetry={() => { void refetchSession(); void refetchViews(); }} />}
            <div className="flex flex-wrap items-center gap-2">
                <select
                    value={selectedViewId ?? ''}
                    onChange={event => handleViewSelect(event.target.value)}
                    disabled={isLoading}
                    className="min-w-[220px] rounded-md border border-border-strong bg-surface-card px-3 py-2 text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-focus"
                >
                    <option value="">{t('surfaces.savedViews.savedViews')}</option>
                    {savedViews.map(view => (
                        <option key={view.id} value={view.id} disabled={!view.is_valid}>
                            {savedViewDisplay(view).name} · {sortScopeLabel(view.scope)}{view.is_valid ? '' : ` · ${t('surfaces.savedViews.invalid')}`}
                        </option>
                    ))}
                </select>

                <Button variant="secondary" size="sm" onClick={openCreateForm}>
                    <Save className="mr-1 h-4 w-4" />
                    {t('surfaces.savedViews.save')}
                </Button>
                <Button
                    variant="outline"
                    size="sm"
                    onClick={handleUpdateSelected}
                    disabled={!canMutateSelected || updateMutation.isPending}
                    isLoading={updateMutation.isPending}
                >
                    {t('surfaces.savedViews.update')}
                </Button>
                <Button
                    variant="outline"
                    size="sm"
                    onClick={openDuplicateForm}
                    disabled={!selectedView || !selectedView.is_valid}
                >
                    <Copy className="mr-1 h-4 w-4" />
                    {t('surfaces.savedViews.duplicate')}
                </Button>
                <Button
                    variant="ghost"
                    size="sm"
                    onClick={handleDeleteSelected}
                    disabled={!canMutateSelected || deleteMutation.isPending}
                    isLoading={deleteMutation.isPending}
                >
                    <Trash2 className="mr-1 h-4 w-4" />
                    {t('surfaces.savedViews.delete')}
                </Button>

                {selectedView && !selectedView.is_valid && (
                    <span className="inline-flex items-center gap-1 text-sm text-feedback-warning-foreground">
                        <AlertTriangle className="h-4 w-4" />
                        {selectedView.invalid_reason ?? t('surfaces.savedViews.invalidReason')}
                    </span>
                )}
                {statusMessage && (
                    <span className="text-sm text-content-secondary">{statusMessage}</span>
                )}
            </div>

            <Modal
                open={formMode !== null}
                title={t(formMode === 'create' ? 'surfaces.savedViews.saveCurrentView' : 'surfaces.savedViews.duplicateView')}
                closeLabel={t('actions.close')}
                onClose={resetForm}
                initialFocusRef={formNameRef}
                className="max-w-md"
            >
                {formMode && (
                    <form
                        onSubmit={handleSubmitForm}
                        className="space-y-4"
                    >
                        <div className="space-y-3">
                            <Input
                                ref={formNameRef}
                                label={t('surfaces.savedViews.name')}
                                value={formName}
                                onChange={event => setFormName(event.target.value)}
                                maxLength={255}
                            />
                            <div>
                                <label className="mb-1 block text-sm font-medium text-content-primary">{t('surfaces.savedViews.description')}</label>
                                <textarea
                                    value={formDescription}
                                    onChange={event => setFormDescription(event.target.value)}
                                    className="min-h-20 w-full rounded-md border border-border-strong px-3 py-2 shadow-sm focus:outline-none focus:ring-1 focus:ring-focus"
                                />
                            </div>
                            <div>
                                <label className="mb-1 block text-sm font-medium text-content-primary">{t('surfaces.savedViews.scope')}</label>
                                <select
                                    value={formScope}
                                    onChange={event => setFormScope(event.target.value as EditableScope)}
                                    className="w-full rounded-md border border-border-strong bg-surface-card px-3 py-2 shadow-sm focus:outline-none focus:ring-1 focus:ring-focus"
                                >
                                    <option value="personal">{t('surfaces.savedViews.personal')}</option>
                                    <option value="shared">{t('surfaces.savedViews.shared')}</option>
                                </select>
                            </div>
                            {formError && (
                                <p className="rounded-md bg-feedback-danger-muted px-3 py-2 text-sm text-feedback-danger-foreground">{formError}</p>
                            )}
                        </div>

                        <div className="mt-5 flex justify-end gap-2">
                            <Button type="button" variant="ghost" onClick={resetForm}>
                                {t('surfaces.savedViews.cancel')}
                            </Button>
                            <Button
                                type="submit"
                                isLoading={createMutation.isPending || duplicateMutation.isPending}
                            >
                                {t(formMode === 'create' ? 'surfaces.savedViews.save' : 'surfaces.savedViews.duplicate')}
                            </Button>
                        </div>
                    </form>
                )}
            </Modal>
            {confirmationDialog}
        </div>
    );
};

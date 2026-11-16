import { savedViewModified } from '../../utils/savedViewState';
import i18n from '../../i18n/i18n';
import { useMemo, useRef, useState } from 'react';
import type { FormEvent } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
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
import { Textarea } from '../common/Textarea';
import { Select } from '../common/Select';

const t = i18n.t.bind(i18n);

type EditableScope = Exclude<SavedViewScope, 'system'>;
type FormMode = 'create' | 'duplicate';

interface SavedViewManagerOptions {
    filters: TaskFilters;
    sortKey: SortKey;
    /** Conditions applied for the person, such as a hand-over from Plan; they do not count as a change. */
    systemFilters?: Partial<TaskFilters>;
    selectedViewId: number | null;
    onSelectedViewIdChange: (viewId: number | null) => void;
    onApplyView: (view: SavedView) => void;
}

/**
 * The saved views of the Tasks page and what can be done with the one shown: choose, save as,
 * save changes, duplicate, delete and reset. Render `dialogs` once on the page.
 */
export const useSavedViewManager = ({
    filters,
    sortKey,
    systemFilters,
    selectedViewId,
    onSelectedViewIdChange,
    onApplyView,
}: SavedViewManagerOptions) => {
    const queryClient = useQueryClient();
    const [formMode, setFormMode] = useState<FormMode | null>(null);
    const [formName, setFormName] = useState('');
    const [formDescription, setFormDescription] = useState('');
    const [formScope, setFormScope] = useState<EditableScope>('personal');
    const [formError, setFormError] = useState<string | null>(null);
    const [statusMessage, setStatusMessage] = useState<string | null>(null);
    const formNameRef = useRef<HTMLInputElement>(null);
    const { requestConfirmation, confirmationDialog } = useConfirmDialog();

    // feedback-policy: query loading,error,retry,empty - the view menu shows the failure and its retry; actions stay unavailable until it loads.
    const { data: session, error: sessionError, refetch: refetchSession } = useQuery({
        queryKey: ['session', 'whoami'],
        queryFn: sessionService.getWhoAmI,
    });

    // feedback-policy: query loading,error,retry,empty - the view menu says while views load, shows a failure with retry, and always offers All tasks.
    const { data: savedViews = [], isLoading, error: viewsError, refetch: refetchViews } = useQuery({
        queryKey: ['saved-views', 'tasks'],
        queryFn: () => savedViewService.getAll({ view_type: 'tasks' }),
    });

    const selectedView = useMemo(
        () => savedViews.find(view => view.id === selectedViewId) ?? null,
        [savedViews, selectedViewId],
    );

    const modified = savedViewModified(selectedView, filters, sortKey, systemFilters);

    const canMutateSelected = Boolean(
        selectedView &&
        selectedView.is_valid &&
        selectedView.scope !== 'system' &&
        (selectedView.owner_principal_id != null
            ? selectedView.owner_principal_id === session?.principal_id
            : selectedView.created_by_session_id === session?.id),
    );

    const currentViewPayload = {
        filters_json: filters as unknown as Record<string, unknown>,
        sort_json: { sortKey },
        columns_json: {},
    };

    // feedback-policy: mutation pending,inline - the save dialog shows progress and keeps its fields with the error.
    const createMutation = useMutation({
        mutationFn: savedViewService.create,
    });

    // feedback-policy: mutation pending,inline - Save changes shows progress; a failure is announced next to the view name.
    const updateMutation = useMutation({
        mutationFn: ({ id, data }: { id: number; data: Parameters<typeof savedViewService.update>[1] }) =>
            savedViewService.update(id, data),
    });

    // feedback-policy: mutation pending,inline - the confirmation stays open while deleting and shows a failure.
    const deleteMutation = useMutation({
        mutationFn: savedViewService.delete,
    });

    // feedback-policy: mutation pending,inline - the duplicate dialog shows progress and keeps its fields with the error.
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

    const openSaveAs = () => {
        setFormMode('create');
        setFormName('');
        setFormDescription('');
        setFormScope('personal');
        setFormError(null);
    };

    const openDuplicate = () => {
        if (!selectedView) return;
        setFormMode('duplicate');
        setFormName(`Copy of ${selectedView.name}`.slice(0, 255));
        setFormDescription(selectedView.description ?? '');
        setFormScope('personal');
        setFormError(null);
    };

    const chooseView = (viewId: number | null) => {
        if (viewId === null) {
            onSelectedViewIdChange(null);
            setStatusMessage(null);
            return;
        }
        const view = savedViews.find(candidate => candidate.id === viewId);
        if (!view || !view.is_valid) return;
        onSelectedViewIdChange(view.id);
        onApplyView(view);
        setStatusMessage(null);
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

    const saveChanges = async () => {
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

    const requestDelete = () => {
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

    const resetView = () => {
        if (selectedView) onApplyView(selectedView);
    };

    const dialogs = (
        <>
            <Modal
                open={formMode !== null}
                title={t(formMode === 'create' ? 'surfaces.savedViews.saveCurrentView' : 'surfaces.savedViews.duplicateView')}
                closeLabel={t('actions.close')}
                onClose={resetForm}
                initialFocusRef={formNameRef}
                className="max-w-md"
            >
                {formMode && (
                    <form onSubmit={handleSubmitForm} className="space-y-4">
                        <div className="space-y-3">
                            <Input
                                ref={formNameRef}
                                label={t('surfaces.savedViews.name')}
                                value={formName}
                                onChange={event => setFormName(event.target.value)}
                                maxLength={255}
                            />
                            <Textarea label={t('surfaces.savedViews.description')} value={formDescription} onChange={event => setFormDescription(event.target.value)} className="min-h-20" />
                            <Select label={t('surfaces.savedViews.scope')} value={formScope} onChange={event => setFormScope(event.target.value as EditableScope)}><option value="personal">{t('surfaces.savedViews.personal')}</option><option value="shared">{t('surfaces.savedViews.shared')}</option></Select>
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
        </>
    );

    return {
        savedViews,
        isLoading,
        loadError: sessionError ?? viewsError,
        retryLoad: () => { void refetchSession(); void refetchViews(); },
        selectedView,
        modified,
        canMutateSelected,
        isSaving: updateMutation.isPending,
        isDeleting: deleteMutation.isPending,
        statusMessage,
        chooseView,
        openSaveAs,
        saveChanges,
        openDuplicate,
        requestDelete,
        resetView,
        dialogs,
    };
};

export type SavedViewManager = ReturnType<typeof useSavedViewManager>;

import { useState, useRef } from 'react';
import { useTranslation } from 'react-i18next';
import { useSearchParams } from 'react-router-dom';
import { useWorkScope } from '../features/scope/useWorkScope';
import { IterationList } from '../components/iteration/IterationList';
import { IterationForm } from '../components/iteration/IterationForm';
import { IterationImportDialog } from '../components/iteration/IterationImportDialog';
import type { Iteration } from '../types/iteration';
import { PageHeader, PageLayout, SlideOverDrawer } from '../components/ui';
import { useConfirmDialog } from '../components/common/useConfirmDialog';
import { PlanReturnBar } from '../components/planning/PlanReturnBar';
import { Plus, Upload } from 'lucide-react';

const IterationsPage = () => {
    const [searchParams, setSearchParams] = useSearchParams();
    const { project } = useWorkScope();
    // The create parameter is the open state of the new-iteration form, so the scope bar's
    // New iteration opens it and Manage iterations closes it, even while this page is mounted.
    const isCreating = searchParams.get('create') === '1';
    const setIsCreating = (open: boolean) => {
        setSearchParams(current => {
            const next = new URLSearchParams(current);
            if (open) next.set('create', '1'); else next.delete('create');
            return next;
        }, { replace: !open });
    };
    const fileInputRef = useRef<HTMLInputElement>(null);
    const { t } = useTranslation();
    const [editingIteration, setEditingIteration] = useState<Iteration | null>(null);
    const [formState, setFormState] = useState({ dirty: false, pending: false });
    const { requestConfirmation, confirmationDialog } = useConfirmDialog();
    const drawerOpen = isCreating || editingIteration !== null;

    const closeDrawer = () => {
        setEditingIteration(null);
        setFormState({ dirty: false, pending: false });
        if (isCreating) setIsCreating(false);
    };
    // Closing the drawer by its close button, Escape or the backdrop asks first when there are unsaved changes.
    const requestCloseDrawer = () => {
        if (!formState.dirty) { closeDrawer(); return; }
        requestConfirmation({
            title: t('iterationForm.discardTitle'),
            description: t('iterationForm.discardBody'),
            confirmLabel: t('iterationForm.discard'),
            cancelLabel: t('iterationForm.keepEditing'),
            closeLabel: t('actions.close'),
            tone: 'danger',
            onConfirm: closeDrawer,
        });
    };

    const [importFile, setImportFile] = useState<File | null>(null);
    const handleImport = (event: React.ChangeEvent<HTMLInputElement>) => {
        setImportFile(event.target.files?.[0] ?? null); event.currentTarget.value = '';
    };

    return (
        <PageLayout>
            {importFile && <IterationImportDialog file={importFile} onClose={() => setImportFile(null)} />}
            <PageHeader
                title={t('iterations.title')}
                subtitle={t('iterations.description')}
                actions={(
                    <>
                    <input type="file" ref={fileInputRef} className="hidden" accept=".json" onChange={handleImport}/>
                    <button className="btn" onClick={() => fileInputRef.current?.click()}>
                        <Upload aria-hidden="true" className="h-4 w-4" /> {t('actions.import')}
                    </button>
                    <button className="btn primary" onClick={() => setIsCreating(true)}>
                        <Plus aria-hidden="true" className="h-4 w-4" /> {t('iterations.newIteration')}
                    </button>
                    </>
                )}
            />
            <PlanReturnBar />

            <IterationList
                projectId={typeof project === 'number' ? project : undefined}
                onEdit={(iter) => setEditingIteration(iter)}
            />

            <SlideOverDrawer
                open={drawerOpen}
                title={editingIteration ? t('iterations.editIteration') : t('iterations.createIteration')}
                closeLabel={t('actions.close')}
                closeDisabled={formState.pending}
                onClose={requestCloseDrawer}
            >
                <div className="p-5">
                    <IterationForm
                        initialData={editingIteration || undefined}
                        defaultProjectId={!editingIteration && typeof project === 'number' ? project : undefined}
                        onStateChange={setFormState}
                        onSuccess={closeDrawer}
                        onCancel={closeDrawer}
                    />
                </div>
            </SlideOverDrawer>
            {confirmationDialog}
        </PageLayout>
    );
};

export default IterationsPage;

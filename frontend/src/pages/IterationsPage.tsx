import { useState, useRef } from 'react';
import { useTranslation } from 'react-i18next';
import { IterationList } from '../components/iteration/IterationList';
import { IterationForm } from '../components/iteration/IterationForm';
import { IterationImportDialog } from '../components/iteration/IterationImportDialog';
import type { Iteration } from '../types/iteration';
import { PageHeader, PageLayout } from '../components/ui';
import { PlanReturnBar } from '../components/planning/PlanReturnBar';

const IterationsPage = () => {
    const [isCreating, setIsCreating] = useState(false);
    const fileInputRef = useRef<HTMLInputElement>(null);
    const { t } = useTranslation();
    const [editingIteration, setEditingIteration] = useState<Iteration | null>(null);

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
                    <button className="btn" onClick={() => fileInputRef.current?.click()} disabled={isCreating || !!editingIteration}>
                        ↓ {t('actions.import')}
                    </button>
                    <button className="btn primary" onClick={() => setIsCreating(true)} disabled={isCreating || !!editingIteration}>
                        + {t('iterations.newIteration')}
                    </button>
                    </>
                )}
            />
            <PlanReturnBar />

            {isCreating || editingIteration ? (
                <div className="card card-pad" style={{maxWidth:640}}>
                    <h2 style={{margin:'0 0 20px', fontSize:16, fontWeight:600}}>
                        {editingIteration ? t('iterations.editIteration') : t('iterations.createIteration')}
                    </h2>
                    <IterationForm
                        initialData={editingIteration || undefined}
                        onSuccess={() => { setIsCreating(false); setEditingIteration(null); }}
                        onCancel={() => { setIsCreating(false); setEditingIteration(null); }}
                    />
                </div>
            ) : (
                <IterationList onEdit={(iter) => setEditingIteration(iter)} />
            )}
        </PageLayout>
    );
};

export default IterationsPage;

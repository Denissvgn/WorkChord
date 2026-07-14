import { useState, useRef } from 'react';
import { useTranslation } from 'react-i18next';
import { IterationList } from '../components/iteration/IterationList';
import { IterationForm } from '../components/iteration/IterationForm';
import { exportService } from '../services/exportService';
import { useQueryClient } from '@tanstack/react-query';
import type { Iteration } from '../types/iteration';
import { PageHeader, PageLayout } from '../components/ui';
import { useToast } from '../components/feedback/toast';
import { getApiErrorMessage } from '../utils/apiError';

const IterationsPage = () => {
    const [isCreating, setIsCreating] = useState(false);
    const fileInputRef = useRef<HTMLInputElement>(null);
    const queryClient = useQueryClient();
    const { t } = useTranslation();
    const toast = useToast();
    const [editingIteration, setEditingIteration] = useState<Iteration | null>(null);

    const handleImport = async (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            try {
                await exportService.importIteration(e.target.files[0]);
                queryClient.invalidateQueries({ queryKey: ['iterations'] });
                toast.success(t('iterations.importSuccess'));
            } catch (error: unknown) {
                toast.error(getApiErrorMessage(error, t('iterations.importFailed')));
            }
            e.target.value = '';
        }
    };

    return (
        <PageLayout>
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

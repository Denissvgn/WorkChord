import { useRef, useState } from 'react';
import type { ChangeEvent } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { Upload } from 'lucide-react';
import { projectService } from '../../services/projectService';
import type { Iteration } from '../../types/iteration';
import { Button } from '../common/Button';
import { SlideOverDrawer } from '../ui';
import { IterationImportDialog } from './IterationImportDialog';
import { IterationList } from './IterationList';

interface AllIterationsDrawerProps {
    /** Lists only this project's iterations; every project's when omitted. */
    projectId?: number;
    onOpen: (iteration: Iteration) => void;
    onEdit: (iteration: Iteration) => void;
    onClose: () => void;
}

/** Every iteration of the project in scope, with Open, Edit, Export and Delete per row and Import in the header. */
export const AllIterationsDrawer = ({ projectId, onOpen, onEdit, onClose }: AllIterationsDrawerProps) => {
    const { t } = useTranslation();
    const fileInputRef = useRef<HTMLInputElement>(null);
    const [importFile, setImportFile] = useState<File | null>(null);
    // feedback-policy: query loading,error,retry,empty - the subtitle falls back to a generic sentence without the project name.
    const projects = useQuery({ queryKey: ['projects'], queryFn: projectService.getAll, enabled: projectId !== undefined });
    const projectName = projects.data?.find(project => project.id === projectId)?.name;

    const handleImport = (event: ChangeEvent<HTMLInputElement>) => {
        setImportFile(event.target.files?.[0] ?? null);
        event.currentTarget.value = '';
    };

    return (
        <>
            <SlideOverDrawer
                open
                title={t('iterations.allIterations')}
                subtitle={projectId === undefined
                    ? t('iterations.allIterationsOfAllProjects')
                    : projectName ? t('iterations.allIterationsOfProject', { project: projectName }) : undefined}
                closeLabel={t('actions.close')}
                onClose={onClose}
                actions={(
                    <>
                        <input type="file" ref={fileInputRef} className="hidden" accept=".json" onChange={handleImport} aria-label={t('iterations.importJson')} />
                        <Button variant="secondary" size="sm" onClick={() => fileInputRef.current?.click()}>
                            <Upload aria-hidden="true" className="h-4 w-4" />
                            {t('actions.import')}
                        </Button>
                    </>
                )}
            >
                <IterationList projectId={projectId} onOpen={onOpen} onEdit={onEdit} />
            </SlideOverDrawer>
            {importFile && <IterationImportDialog file={importFile} onClose={() => setImportFile(null)} />}
        </>
    );
};

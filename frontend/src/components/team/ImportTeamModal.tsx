import { useState, useRef } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { Upload, FileText, AlertCircle, CheckCircle } from 'lucide-react';
import { Button } from '../common/Button';
import { Modal } from '../common/Modal';
import { teamService } from '../../services/teamService';
import { getApiErrorMessage } from '../../utils/apiError';

interface ImportTeamModalProps {
    iterationId: number;
    onClose: () => void;
}

export const ImportTeamModal = ({ iterationId, onClose }: ImportTeamModalProps) => {
    const [text, setText] = useState('');
    const [error, setError] = useState<string | null>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);
    const queryClient = useQueryClient();
    const { t } = useTranslation();

    const importMutation = useMutation({
        mutationFn: (text: string) => teamService.importFromText(iterationId, text),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['team', iterationId] });
            queryClient.invalidateQueries({ queryKey: ['teamMemberProfiles'] });
            onClose();
        },
        onError: (err: unknown) => {
            setError(getApiErrorMessage(err, t('teamImport.importError')));
        }
    });

    const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (event) => {
                const content = event.target?.result as string;
                setText(content);
                setError(null);
            };
            reader.readAsText(file);
        }
    };

    const handleImport = () => {
        if (!text.trim()) {
            setError(t('teamImport.emptyError'));
            return;
        }
        setError(null);
        importMutation.mutate(text);
    };

    return (
        <Modal
            open
            title={t('teamImport.title')}
            closeLabel={t('actions.close')}
            onClose={onClose}
            footer={(
                <div className="flex justify-end gap-3">
                    <Button variant="secondary" onClick={onClose} disabled={importMutation.isPending}>{t('actions.cancel')}</Button>
                    <Button onClick={handleImport} disabled={importMutation.isPending || !text.trim()} isLoading={importMutation.isPending}>{t('teamImport.submit')}</Button>
                </div>
            )}
        >
                <div className="space-y-4">
                    {/* Format example */}
                    <div className="bg-surface-muted rounded-lg p-4 text-sm">
                        <h3 className="font-semibold mb-2 flex items-center gap-2">
                            <FileText className="w-4 h-4" />
                            {t('teamImport.formatTitle')}
                        </h3>
                        <pre className="text-content-secondary whitespace-pre-wrap font-mono text-xs bg-surface-card p-3 rounded border">
                            {t('teamImport.formatExample')}
                        </pre>
                        <p className="text-content-secondary mt-2 text-xs">
                            {t('teamImport.formatHelp')}<code className="bg-surface-hover px-1 rounded">{t('teamImport.formatSyntax')}</code>
                        </p>
                        <ul className="text-content-secondary mt-2 text-xs list-disc list-inside space-y-1">
                            <li>{t('teamImport.nameRule')}</li>
                            <li>{t('teamImport.roleRule')}</li>
                            <li>{t('teamImport.availabilityRule')}</li>
                            <li>{t('teamImport.proficiencyRule')}</li>
                            <li>{t('teamImport.loadRule')}</li>
                        </ul>
                    </div>

                    {/* File upload */}
                    <div>
                        <input
                            ref={fileInputRef}
                            type="file"
                            accept=".txt"
                            onChange={handleFileUpload}
                            className="hidden"
                        />
                        <Button
                            variant="secondary"
                            onClick={() => fileInputRef.current?.click()}
                            className="w-full"
                        >
                            <Upload className="w-4 h-4 mr-2" />
                            {t('actions.uploadTxt')}
                        </Button>
                    </div>

                    {/* Text area */}
                    <textarea
                        value={text}
                        onChange={(e) => {
                            setText(e.target.value);
                            setError(null);
                        }}
                        placeholder={t('teamImport.placeholder')}
                        className="w-full h-48 p-3 border rounded-lg font-mono text-sm resize-none focus:outline-none focus:ring-2 focus:ring-focus"
                    />

                    {/* Error message */}
                    {error && (
                        <div className="flex items-center gap-2 text-feedback-danger-foreground bg-feedback-danger-muted p-3 rounded-lg">
                            <AlertCircle className="w-4 h-4 flex-shrink-0" />
                            <span className="text-sm">{error}</span>
                        </div>
                    )}

                    {/* Success indication */}
                    {importMutation.isSuccess && (
                        <div className="flex items-center gap-2 text-feedback-success-foreground bg-feedback-success-muted p-3 rounded-lg">
                            <CheckCircle className="w-4 h-4 flex-shrink-0" />
                            <span className="text-sm">{t('teamImport.success', { count: importMutation.data?.imported_count })}</span>
                        </div>
                    )}
                </div>

        </Modal>
    );
};

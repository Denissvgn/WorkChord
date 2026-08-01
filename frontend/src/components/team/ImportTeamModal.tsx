import { useEffect, useId, useRef, useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { Upload, FileText, AlertCircle } from 'lucide-react';
import { Button } from '../common/Button';
import { Modal } from '../common/Modal';
import { teamService } from '../../services/teamService';
import { getApiErrorMessage } from '../../utils/apiError';

const MAX_IMPORT_ROWS = 500;

interface ImportTeamModalProps {
    iterationId: number;
    onClose: () => void;
    onSuccess?: () => void;
    onStateChange?: (state: { dirty: boolean; pending: boolean }) => void;
}

export const ImportTeamModal = ({
    iterationId,
    onClose,
    onSuccess: onImportSuccess,
    onStateChange,
}: ImportTeamModalProps) => {
    const [text, setText] = useState('');
    const [error, setError] = useState<string | null>(null);
    const [isReadingFile, setIsReadingFile] = useState(false);
    const fileInputRef = useRef<HTMLInputElement>(null);
    const fileReaderRef = useRef<FileReader | null>(null);
    const readRequestRef = useRef(0);
    const queryClient = useQueryClient();
    const { t } = useTranslation();
    const fileInputId = useId();
    const textInputId = useId();
    const textHintId = useId();

    const importMutation = useMutation({
        mutationFn: (text: string) => teamService.importFromText(iterationId, text),
        onSuccess: async () => {
            await Promise.all([
                queryClient.invalidateQueries({ queryKey: ['team', iterationId] }),
                queryClient.invalidateQueries({ queryKey: ['teamMemberProfiles'] }),
                queryClient.invalidateQueries({ queryKey: ['workload'] }),
                queryClient.invalidateQueries({ queryKey: ['gantt'] }),
            ]);
            (onImportSuccess ?? onClose)();
        },
        onError: (err: unknown) => {
            setError(getApiErrorMessage(err, t('teamImport.importError')));
        }
    });

    const isPending = importMutation.isPending;
    const isDirty = text.length > 0;

    useEffect(() => {
        onStateChange?.({ dirty: isDirty, pending: isPending });
    }, [isDirty, isPending, onStateChange]);

    useEffect(() => () => {
        readRequestRef.current += 1;
        const reader = fileReaderRef.current;
        fileReaderRef.current = null;
        if (reader?.readyState === 1) reader.abort();
    }, []);

    const cancelPendingFileRead = () => {
        readRequestRef.current += 1;
        const reader = fileReaderRef.current;
        fileReaderRef.current = null;
        if (reader?.readyState === 1) reader.abort();
        setIsReadingFile(false);
    };

    const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        e.currentTarget.value = '';
        if (!file || isPending) return;

        cancelPendingFileRead();
        const requestId = readRequestRef.current;
        const reader = new FileReader();
        fileReaderRef.current = reader;
        setError(null);
        setIsReadingFile(true);

        const finishCurrentRead = () => {
            if (
                requestId !== readRequestRef.current
                || fileReaderRef.current !== reader
            ) return false;
            fileReaderRef.current = null;
            setIsReadingFile(false);
            return true;
        };

        reader.onload = () => {
            if (!finishCurrentRead()) return;
            if (typeof reader.result !== 'string') {
                setError(t(
                    'teamImport.fileReadError',
                    'The selected file could not be read. Choose another file or paste its contents.',
                ));
                return;
            }
            setText(reader.result);
            setError(null);
        };
        reader.onerror = () => {
            if (!finishCurrentRead()) return;
            setError(t(
                'teamImport.fileReadError',
                'The selected file could not be read. Choose another file or paste its contents.',
            ));
        };
        reader.onabort = () => {
            if (!finishCurrentRead()) return;
            setError(t(
                'teamImport.fileReadError',
                'The selected file could not be read. Choose another file or paste its contents.',
            ));
        };

        try {
            reader.readAsText(file);
        } catch {
            if (!finishCurrentRead()) return;
            setError(t(
                'teamImport.fileReadError',
                'The selected file could not be read. Choose another file or paste its contents.',
            ));
        }
    };

    const handleImport = () => {
        if (isPending || isReadingFile) return;

        const rows = text
            .split(/\r?\n/)
            .map(row => row.trim())
            .filter(Boolean);

        if (rows.length === 0) {
            setError(t('teamImport.emptyError'));
            return;
        }

        if (rows.length > MAX_IMPORT_ROWS) {
            setError(t(
                'teamImport.tooManyRows',
                'Import up to 500 non-empty rows at a time.',
            ));
            return;
        }

        if (!rows.some(row => row.startsWith('-- '))) {
            setError(t(
                'teamImport.noRecognizedRows',
                'No team rows were found. Each team row must start with --.',
            ));
            return;
        }

        setError(null);
        importMutation.mutate(text);
    };

    const handleTextChange = (value: string) => {
        if (isPending) return;
        cancelPendingFileRead();
        setText(value);
        setError(null);
    };

    const handleClose = () => {
        if (isPending) return;
        cancelPendingFileRead();
        onClose();
    };

    return (
        <Modal
            open
            title={t('teamImport.title')}
            closeLabel={t('actions.close')}
            onClose={handleClose}
            closeDisabled={isPending}
            footer={(
                <div className="flex flex-col-reverse gap-3 sm:flex-row sm:justify-end">
                    <Button type="button" variant="secondary" onClick={handleClose} disabled={isPending}>
                        {t('actions.cancel')}
                    </Button>
                    <Button
                        type="button"
                        onClick={handleImport}
                        disabled={isPending || isReadingFile}
                        isLoading={isPending}
                    >
                        {t('teamImport.submit')}
                    </Button>
                </div>
            )}
        >
            <div className="space-y-4">
                <div className="rounded-lg bg-surface-muted p-4 text-sm">
                    <h3 className="mb-2 flex items-center gap-2 font-semibold">
                        <FileText aria-hidden="true" className="h-4 w-4" />
                        {t('teamImport.formatTitle')}
                    </h3>
                    <pre className="break-words whitespace-pre-wrap rounded border bg-surface-card p-3 font-mono text-xs text-content-secondary">
                        {t('teamImport.formatExample')}
                    </pre>
                    <p id={textHintId} className="mt-2 text-xs text-content-secondary">
                        {t('teamImport.formatHelp')}
                        <code className="rounded bg-surface-hover px-1">{t('teamImport.formatSyntax')}</code>
                    </p>
                    <ul className="mt-2 list-inside list-disc space-y-1 text-xs text-content-secondary">
                        <li>{t('teamImport.nameRule')}</li>
                        <li>{t('teamImport.roleRule')}</li>
                        <li>{t('teamImport.availabilityRule')}</li>
                        <li>{t('teamImport.proficiencyRule')}</li>
                        <li>{t('teamImport.loadRule')}</li>
                    </ul>
                </div>

                <div>
                    <label className="sr-only" htmlFor={fileInputId}>
                        {t('teamImport.fileInputLabel', 'Team import file')}
                    </label>
                    <input
                        ref={fileInputRef}
                        id={fileInputId}
                        type="file"
                        accept=".txt,text/plain"
                        onChange={handleFileUpload}
                        disabled={isPending}
                        className="hidden"
                    />
                    <Button
                        type="button"
                        variant="secondary"
                        onClick={() => fileInputRef.current?.click()}
                        disabled={isPending}
                        aria-controls={fileInputId}
                        className="w-full"
                    >
                        <Upload aria-hidden="true" className="mr-2 h-4 w-4" />
                        {t('actions.uploadTxt')}
                    </Button>
                    {isReadingFile && (
                        <p className="mt-2 text-sm text-content-secondary" role="status">
                            {t('teamImport.readingFile', 'Reading file…')}
                        </p>
                    )}
                </div>

                <div>
                    <label className="mb-1 block text-sm font-medium text-content-primary" htmlFor={textInputId}>
                        {t('teamImport.textInputLabel', 'Team members to import')}
                    </label>
                    <textarea
                        id={textInputId}
                        aria-describedby={textHintId}
                        value={text}
                        onChange={event => handleTextChange(event.target.value)}
                        disabled={isPending}
                        placeholder={t('teamImport.placeholder')}
                        className="h-48 w-full resize-y rounded-lg border border-border-strong bg-surface-card p-3 font-mono text-sm text-content-primary focus:outline-none focus:ring-2 focus:ring-focus disabled:cursor-not-allowed disabled:bg-surface-muted"
                    />
                </div>

                {error && (
                    <div
                        className="flex items-start gap-2 rounded-lg bg-feedback-danger-muted p-3 text-feedback-danger-foreground"
                        role="alert"
                    >
                        <AlertCircle aria-hidden="true" className="mt-0.5 h-4 w-4 flex-shrink-0" />
                        <span className="min-w-0 break-words text-sm">{error}</span>
                    </div>
                )}
            </div>
        </Modal>
    );
};

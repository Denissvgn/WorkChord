import { useState, useRef } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { Upload, FileText, AlertCircle, CheckCircle, Maximize2, Minimize2, Inbox } from 'lucide-react';
import { Button } from '../common/Button';
import { Modal } from '../common/Modal';
import { taskService } from '../../services/taskService';
import { getApiErrorMessage } from '../../utils/apiError';
import type { TaskImportDestination } from '../../types/task';
import clsx from 'clsx';

interface ImportTasksModalProps {
    iterationId: number;
    onClose: () => void;
}

export const ImportTasksModal = ({ iterationId, onClose }: ImportTasksModalProps) => {
    const [text, setText] = useState('');
    const [error, setError] = useState<string | null>(null);
    const [isFullScreen, setIsFullScreen] = useState(false);
    const [destination, setDestination] = useState<TaskImportDestination>('tasks');
    const fileInputRef = useRef<HTMLInputElement>(null);
    const editorRef = useRef<HTMLTextAreaElement>(null);
    const queryClient = useQueryClient();
    const { t } = useTranslation();

    const importMutation = useMutation({
        mutationFn: (payload: { text: string; destination: TaskImportDestination }) => (
            taskService.importFromText(iterationId, payload.text, { destination: payload.destination })
        ),
        onSuccess: (data) => {
            if (data.task_count > 0) {
                queryClient.invalidateQueries({ queryKey: ['tasks', iterationId] });
                queryClient.invalidateQueries({ queryKey: ['tasks', 'text', iterationId] });
                queryClient.invalidateQueries({ queryKey: ['workload'] });
                queryClient.invalidateQueries({ queryKey: ['gantt'] });
                queryClient.invalidateQueries({ queryKey: ['projects'] });
                queryClient.invalidateQueries({ queryKey: ['projectSummary'] });
                queryClient.invalidateQueries({ queryKey: ['projectTasks'] });
            }
            if (data.triage_count > 0) {
                queryClient.invalidateQueries({ queryKey: ['triage'] });
            }
            onClose();
        },
        onError: (err: unknown) => {
            setError(getApiErrorMessage(err, t('taskImport.importError')));
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
            setError(t('taskImport.emptyError'));
            return;
        }
        setError(null);
        importMutation.mutate({ text, destination });
    };

    return (
        <Modal
            open
            title={<span className="flex items-center justify-between gap-4"><span>{t('taskImport.title')}</span><button
                            type="button"
                            onClick={() => setIsFullScreen(!isFullScreen)}
                            className="p-1 hover:bg-surface-subtle rounded text-content-secondary"
                            title={isFullScreen ? t('actions.exitFullScreen') : t('actions.enterFullScreen')}
                            aria-label={isFullScreen ? t('actions.exitFullScreen') : t('actions.enterFullScreen')}
                        >
                            {isFullScreen ? <Minimize2 className="w-5 h-5" /> : <Maximize2 className="w-5 h-5" />}
                        </button></span>}
            closeLabel={t('actions.close')}
            onClose={onClose}
            closeDisabled={importMutation.isPending}
            fullScreen={isFullScreen}
            initialFocusRef={isFullScreen ? editorRef : undefined}
            footer={<div className="flex justify-end gap-3"><Button variant="secondary" onClick={onClose} disabled={importMutation.isPending}>{t('actions.cancel')}</Button><Button onClick={handleImport} disabled={importMutation.isPending || !text.trim()} isLoading={importMutation.isPending}>{destination === 'triage' ? t('taskImport.importTriage') : t('taskImport.importTasks')}</Button></div>}
        >
                <div className="flex min-h-0 flex-1 flex-col space-y-4">
                    {/* Format example */}
                    {!isFullScreen && (
                        <div className="bg-surface-muted rounded-lg p-4 text-sm shrink-0">
                            <h3 className="font-semibold mb-2 flex items-center gap-2">
                                <FileText className="w-4 h-4" />
                                {t('taskImport.formatTitle')}
                            </h3>
                            <pre className="text-content-secondary whitespace-pre-wrap font-mono text-xs bg-surface-card p-3 rounded border">
                                {t('taskImport.formatExample')}
                            </pre>
                            <p className="text-content-secondary mt-2 text-xs">
                                {t('taskImport.formatHelp')}<code className="bg-surface-hover px-1 rounded">{t('surfaces.taskImport.ltPriority110GtLtAssigneeGtLtDaysGtLtTitleGt')}</code>.
                                {' '}{t('taskImport.formatHelpSuffix')}
                            </p>
                        </div>
                    )}

                    {isFullScreen && (
                        <div className="bg-feedback-indigo-muted border border-feedback-indigo-border rounded p-2 text-xs text-feedback-indigo-foreground flex justify-between items-center shrink-0">
                            <span>
                                <strong>{t('taskImport.fullscreenFormat')}</strong>
                                <code className="bg-surface-card/50 px-1 rounded">{t('surfaces.taskImport.text3Name25Title')}</code>
                            </span>
                            <span className="text-xs text-feedback-indigo-foreground">{t('taskImport.fullscreenColumns')}</span>
                        </div>
                    )}

                    {/* File upload */}
                    {!isFullScreen && (
                        <div className="shrink-0 space-y-3">
                            <div className="grid grid-cols-2 gap-2">
                                <button
                                    type="button"
                                    onClick={() => setDestination('tasks')}
                                    className={clsx(
                                        "flex items-center justify-center gap-2 rounded border px-3 py-2 text-sm font-medium",
                                        destination === 'tasks'
                                            ? "border-action bg-action-muted text-action"
                                            : "border-border bg-surface-card text-content-secondary hover:bg-surface-muted"
                                    )}
                                >
                                    <FileText className="w-4 h-4" />
                                    {t('taskImport.destinationTasks')}
                                </button>
                                <button
                                    type="button"
                                    onClick={() => setDestination('triage')}
                                    className={clsx(
                                        "flex items-center justify-center gap-2 rounded border px-3 py-2 text-sm font-medium",
                                        destination === 'triage'
                                            ? "border-action bg-action-muted text-action"
                                            : "border-border bg-surface-card text-content-secondary hover:bg-surface-muted"
                                    )}
                                >
                                    <Inbox className="w-4 h-4" />
                                    {t('taskImport.destinationTriage')}
                                </button>
                            </div>
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
                    )}

                    {/* Text area */}
                    <textarea
                        ref={editorRef}
                        value={text}
                        onChange={(e) => {
                            setText(e.target.value);
                            setError(null);
                        }}
                        placeholder={isFullScreen ? t('taskImport.placeholderFull') : t('taskImport.placeholderInline')}
                        className={clsx(
                            "w-full p-3 border rounded-lg font-mono text-sm resize-none focus:outline-none focus:ring-2 focus:ring-focus",
                            isFullScreen ? "flex-1" : "h-48"
                        )}
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
                            <span className="text-sm">
                                {t('taskImport.success', { tasks: importMutation.data?.task_count, triage: importMutation.data?.triage_count })}
                            </span>
                        </div>
                    )}
                </div>
        </Modal>
    );
};

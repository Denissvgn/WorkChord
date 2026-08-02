import { useRef, useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { Save, FileText, AlertCircle, CheckCircle, Loader2, Maximize2, Minimize2 } from 'lucide-react';
import { Button } from '../common/Button';
import { Modal } from '../common/Modal';
import { taskService } from '../../services/taskService';
import { getApiErrorMessage } from '../../utils/apiError';
import clsx from 'clsx';

interface TaskTextEditorModalProps {
    iterationId: number;
    onClose: () => void;
}

export const TaskTextEditorModal = ({ iterationId, onClose }: TaskTextEditorModalProps) => {
    const { data: initialText = '', isLoading, isError, error, refetch } = useQuery({
        queryKey: ['tasks', 'text', iterationId],
        queryFn: () => taskService.getTasksAsText(iterationId),
        refetchOnWindowFocus: false,
    });

    return (
        <TaskTextEditorBody
            key={`${iterationId}-${initialText}`}
            iterationId={iterationId}
            initialText={initialText}
            isLoading={isLoading}
            queryError={isError ? error : null}
            onRetry={() => void refetch()}
            onClose={onClose}
        />
    );
};

interface TaskTextEditorBodyProps extends TaskTextEditorModalProps {
    initialText: string;
    isLoading: boolean;
    queryError: unknown;
    onRetry: () => void;
}

const TaskTextEditorBody = ({ iterationId, initialText, isLoading, queryError, onRetry, onClose }: TaskTextEditorBodyProps) => {
    const [text, setText] = useState(initialText);
    const [error, setError] = useState<string | null>(null);
    const [isFullScreen, setIsFullScreen] = useState(false);
    const editorRef = useRef<HTMLTextAreaElement>(null);
    const queryClient = useQueryClient();
    const { t } = useTranslation();

    const updateMutation = useMutation({
        mutationFn: (text: string) => taskService.bulkUpdateTasks(iterationId, text, { destination: 'auto' }),
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
        },
        onError: (err: unknown) => {
            setError(getApiErrorMessage(err, t('taskTextEditor.saveError')));
        }
    });

    const handleSave = () => {
        if (!text.trim()) {
            return;
        }
        setError(null);
        updateMutation.mutate(text);
    };

    return (
        <Modal
            open
            title={<span className="flex items-center gap-2">
                        <div className="p-2 bg-status-active-muted rounded-lg text-action">
                            <FileText className="w-5 h-5" />
                        </div>
                        <span>{t('taskTextEditor.title')}</span>
                        <button
                            type="button"
                            onClick={() => setIsFullScreen(!isFullScreen)}
                            className="p-1 hover:bg-surface-subtle rounded text-content-secondary"
                            title={isFullScreen ? t('actions.exitFullScreen') : t('actions.enterFullScreen')}
                            aria-label={isFullScreen ? t('actions.exitFullScreen') : t('actions.enterFullScreen')}
                        >
                            {isFullScreen ? <Minimize2 className="w-5 h-5" /> : <Maximize2 className="w-5 h-5" />}
                        </button>
                    </span>}
            description={t('taskTextEditor.subtitle')}
            closeLabel={t('actions.close')}
            onClose={onClose}
            closeDisabled={updateMutation.isPending}
            fullScreen={isFullScreen}
            initialFocusRef={editorRef}
            className={isFullScreen ? undefined : 'h-[90vh] max-w-5xl'}
            footer={<div className="flex items-center justify-between"><span className="text-xs text-content-tertiary">{t('taskTextEditor.instantApply')}</span><div className="flex gap-3"><Button variant="secondary" onClick={onClose} disabled={updateMutation.isPending}>{t('actions.close')}</Button><Button onClick={handleSave} disabled={updateMutation.isPending || isLoading || Boolean(queryError)} isLoading={updateMutation.isPending} className="min-w-[120px]"><Save className="mr-2 h-4 w-4" />{t('actions.apply')}</Button></div></div>}
        >
                <div className="flex-1 flex overflow-hidden">
                    {/* Main Editor */}
                    <div className="flex-1 p-0 flex flex-col border-r relative">
                        {isLoading && (
                            <div className="absolute inset-0 flex items-center justify-center bg-surface-card/80 z-10">
                                <Loader2 className="w-8 h-8 animate-spin text-action" />
                            </div>
                        )}
                        <textarea
                            ref={editorRef}
                            value={text}
                            onChange={(e) => {
                                setText(e.target.value);
                                setError(null);
                                updateMutation.reset();
                            }}
                            className={clsx(
                                "flex-1 p-4 font-mono text-sm resize-none focus:outline-none leading-relaxed w-full h-full",
                                isFullScreen && "max-w-6xl mx-auto" // Center content in extremely wide screens for readability
                            )}
                            placeholder={t('taskTextEditor.loadingPlaceholder')}
                            spellCheck={false}
                        />
                    </div>

                    {/* Sidebar / Legend */}
                    <div className={clsx(
                        "bg-surface-muted flex flex-col overflow-y-auto border-l transition-all duration-300",
                        isFullScreen ? "w-64" : "w-80"
                    )}>
                        <div className="p-4 border-b bg-surface-card">
                            <h3 className="font-semibold text-sm mb-2">{t('taskTextEditor.formatHelpTitle')}</h3>
                            <div className="text-xs text-content-secondary space-y-2">
                                <p>{t('taskTextEditor.eachLine')}</p>
                                <code className="block bg-surface-subtle p-2 rounded border">
                                    {t('taskTextEditor.formatLine')}
                                </code>
                                <ul className="list-disc pl-4 space-y-1">
                                    <li>{t('taskTextEditor.idRule')}</li>
                                    <li>{t('taskTextEditor.newTaskRule')}</li>
                                    <li>{t('taskTextEditor.priorityRule')}</li>
                                    <li>{t('taskTextEditor.daysRule')}</li>
                                    <li>{t('taskTextEditor.triageRule')}</li>
                                </ul>
                            </div>
                        </div>

                        <div className="p-4">
                            {queryError !== null && (
                                <div role="alert" className="mb-3 rounded-lg border border-feedback-danger-border bg-feedback-danger-muted p-3 text-xs text-feedback-danger-foreground">
                                    <p>{getApiErrorMessage(queryError, t('queryFeedback.fallback'))}</p>
                                    <Button className="mt-2" size="sm" variant="secondary" onClick={onRetry}>{t('queryFeedback.retry')}</Button>
                                </div>
                            )}
                            {error && (
                                <div className="text-feedback-danger-foreground bg-feedback-danger-muted p-3 rounded-lg text-xs mb-3 border border-feedback-danger-border">
                                    <strong className="flex items-center gap-1 mb-1">
                                        <AlertCircle className="w-3 h-3" /> {t('common.error')}:
                                    </strong>
                                    {error}
                                </div>
                            )}

                            {updateMutation.isSuccess && (
                                <div className="text-feedback-success-foreground bg-feedback-success-muted p-3 rounded-lg text-xs mb-3 border border-feedback-success-border">
                                    <strong className="flex items-center gap-1 mb-1">
                                        <CheckCircle className="w-3 h-3" /> {t('common.success')}:
                                    </strong>
                                    {t('taskTextEditor.successCounts', { tasks: updateMutation.data?.task_count, triage: updateMutation.data?.triage_count })}
                                </div>
                            )}
                        </div>
                    </div>
                </div>

        </Modal>
    );
};

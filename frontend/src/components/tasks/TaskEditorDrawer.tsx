import { useMemo } from 'react';
import type { ReactNode, RefObject } from 'react';
import { Loader2 } from 'lucide-react';
import { useQuery } from '@tanstack/react-query';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { taskService } from '../../services/taskService';
import type { Task, TaskUpdate } from '../../types/task';
import { Button } from '../common/Button';
import { DraftDismissalDialog } from './DraftDismissalDialog';
import { useDraftDismissal } from './useDraftDismissal';
import { SlideOverDrawer } from '../ui/SlideOverDrawer';
import { TaskContextSummary } from './TaskContextSummary';
import { TaskForm } from './TaskForm';

type DrawerCopy = ReactNode | ((task: Task | null) => ReactNode);

const resolveDrawerCopy = (copy: DrawerCopy | undefined, task: Task | null) => (
    typeof copy === 'function' ? copy(task) : copy
);

export const TaskEditorDrawer = ({
    taskId,
    iterationId,
    open,
    onClose,
    mode = 'direct',
    prepareTask,
    onSaveSandbox,
    title,
    subtitle,
    icon,
    beforeForm,
    className,
    restoreFocusRef,
}: {
    taskId: number | null;
    iterationId?: number;
    open: boolean;
    onClose: () => void;
    mode?: 'direct' | 'sandbox';
    prepareTask?: (task: Task) => Task;
    onSaveSandbox?: (update: TaskUpdate) => void;
    title?: DrawerCopy;
    subtitle?: DrawerCopy;
    icon?: ReactNode;
    beforeForm?: ReactNode;
    className?: string;
    restoreFocusRef?: RefObject<HTMLElement | null>;
}) => {
    if (!open || taskId === null) return null;

    return (
        <TaskEditorDrawerContent
            key={`${taskId}:${mode}`}
            taskId={taskId}
            iterationId={iterationId}
            onClose={onClose}
            mode={mode}
            prepareTask={prepareTask}
            onSaveSandbox={onSaveSandbox}
            title={title}
            subtitle={subtitle}
            icon={icon}
            beforeForm={beforeForm}
            className={className}
            restoreFocusRef={restoreFocusRef}
        />
    );
};

const TaskEditorDrawerContent = ({
    taskId,
    iterationId,
    onClose,
    mode,
    prepareTask,
    onSaveSandbox,
    title,
    subtitle,
    icon,
    beforeForm,
    className,
    restoreFocusRef,
}: {
    taskId: number;
    iterationId?: number;
    onClose: () => void;
    mode: 'direct' | 'sandbox';
    prepareTask?: (task: Task) => Task;
    onSaveSandbox?: (update: TaskUpdate) => void;
    title?: DrawerCopy;
    subtitle?: DrawerCopy;
    icon?: ReactNode;
    beforeForm?: ReactNode;
    className?: string;
    restoreFocusRef?: RefObject<HTMLElement | null>;
}) => {
    const { t } = useTranslation();
    const guard = useDraftDismissal(onClose);
    const navigate = useNavigate();
    const [params] = useSearchParams();
    // The drawer renders a spinner, inline retry, and withholds the editor until a task exists.
    const {
        data: fullTask,
        isLoading,
        isError,
        refetch,
        // feedback-policy: query loading,error,retry,empty
    } = useQuery({
        queryKey: ['taskEditor', taskId],
        gcTime: 0,
        staleTime: 0,
        queryFn: async () => {
            const detail = await taskService.getDetail(taskId);
            return { ...detail.task, dependencies: detail.dependencies.items.map(item => item.id), detail_context: detail };
        },
    });
    const editorTask = useMemo(
        () => fullTask && !isError ? prepareTask?.(fullTask) ?? fullTask : null,
        [fullTask, prepareTask, isError],
    );
    const resolvedIterationId = iterationId ?? editorTask?.iteration_id ?? null;

    return (
        <SlideOverDrawer
            open
            title={resolveDrawerCopy(title, editorTask) ?? t('taskEditor.editTask')}
            subtitle={resolveDrawerCopy(subtitle, editorTask)
                ?? t('taskEditor.taskCode', { id: taskId })}
            icon={icon}
            closeLabel={t('taskEditor.close')}
            onClose={guard.requestClose}
            closeDisabled={guard.pending}
            className={className ?? 'max-w-2xl'}
            restoreFocusRef={restoreFocusRef}
        >
            <div className="flex min-h-full flex-col p-4 sm:p-6">
                {isLoading && (
                    <div className="flex flex-1 items-center justify-center gap-2 text-content-secondary">
                        <Loader2 aria-hidden="true" className="h-5 w-5 animate-spin" />
                        {t('common.loading')}
                    </div>
                )}
                {isError && (
                    <div
                        role="alert"
                        className="space-y-3 rounded-md border border-feedback-danger-border bg-feedback-danger-muted p-4 text-feedback-danger-foreground"
                    >
                        <p>{t('taskEditor.loadFailed')}</p>
                        <Button
                            type="button"
                            size="sm"
                            variant="secondary"
                            onClick={() => { void refetch(); }}
                        >
                            {t('taskEditor.retry')}
                        </Button>
                    </div>
                )}
                {beforeForm}
                {editorTask?.detail_context && <TaskContextSummary key={`context:${editorTask.version}`} detail={editorTask.detail_context} onReload={() => void refetch()} onNavigate={id => guard.request(() => {
                    const next = new URLSearchParams(params); next.set('task', String(id));
                    onClose(); navigate(`/tasks?${next}`);
                })} />}
                {editorTask && (
                    <TaskForm
                        iterationId={resolvedIterationId}
                        initialData={editorTask}
                        mode={mode}
                        onSaveSandbox={onSaveSandbox}
                        onDirtyChange={guard.setDirty}
                        onPendingChange={guard.setPending}
                        onDiscardReady={guard.onDiscardReady}
                        confirmUnsavedOnCancel={false}
                        onSuccess={guard.complete}
                        onCancel={guard.requestClose}
                    />
                )}
            </div>
            <DraftDismissalDialog guard={guard} />
        </SlideOverDrawer>
    );
};

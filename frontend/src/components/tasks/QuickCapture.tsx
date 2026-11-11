import { useId, useRef, useState, type FormEvent } from 'react';
import { useMutation } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { CornerDownLeft, Plus } from 'lucide-react';
import { Button } from '../common/Button';
import { taskService } from '../../services/taskService';
import { triageService } from '../../services/triageService';
import { iterationService } from '../../services/iterationService';
import { getApiErrorMessage } from '../../utils/apiError';
import { feedbackMessage, type MutationFeedbackMeta } from '../../features/mutationFeedback';
import type { Task } from '../../types/task';
import type { TriageItem } from '../../types/triage';

export type QuickCaptureTarget = { kind: 'task'; iterationId: number } | { kind: 'triage' };

/**
 * One line that captures work from a title and Enter. Priority is left to the
 * server default, and "More fields" carries the title into the full form.
 */
export const QuickCapture = ({ target, onExpand }: { target: QuickCaptureTarget; onExpand: (title: string) => void }) => {
    const { t } = useTranslation();
    const id = useId();
    const inputRef = useRef<HTMLInputElement>(null);
    const [title, setTitle] = useState('');
    // feedback-policy: mutation pending,inline - the row is read-only while saving and keeps the title on failure.
    const capture = useMutation({
        meta: {
            success: data => target.kind === 'task'
                ? feedbackMessage(t, 'created', 'task', (data as Task).title)
                : feedbackMessage(t, 'created', 'triageItem', (data as TriageItem).title),
            undo: data => target.kind === 'task'
                ? { run: () => taskService.delete((data as Task).id, (data as Task).version, (data as Task).iteration_revision ?? undefined) }
                : undefined,
        } satisfies MutationFeedbackMeta,
        mutationFn: async (value: string): Promise<Task | TriageItem> => {
            if (target.kind === 'triage') return triageService.create({ title: value });
            // Read the plan right before writing so the capture is checked against its current revision.
            const iteration = await iterationService.getById(target.iterationId);
            return taskService.create(target.iterationId, { title: value, effort_days: null, depends_on: [], expected_revision: iteration.revision });
        },
        // The shared mutation listener (installWorkFreshness) refetches every active work view.
        onSuccess: () => {
            setTitle('');
            inputRef.current?.focus();
        },
    });
    const submit = (event: FormEvent) => {
        event.preventDefault();
        const value = title.trim();
        if (!value || capture.isPending) return;
        capture.mutate(value);
    };
    const label = t(target.kind === 'task' ? 'quickCapture.taskLabel' : 'quickCapture.triageLabel');
    return <form onSubmit={submit} className="space-y-1" aria-label={label}>
        <div className="flex items-center gap-2 rounded-md border border-border bg-surface-card px-2 py-1 focus-within:ring-2 focus-within:ring-focus">
            <Plus className="h-4 w-4 shrink-0 text-content-tertiary" aria-hidden="true" />
            <label htmlFor={`${id}-title`} className="sr-only">{label}</label>
            <input ref={inputRef} id={`${id}-title`} value={title} maxLength={500} readOnly={capture.isPending}
                onChange={event => { setTitle(event.target.value); if (capture.isError) capture.reset(); }}
                placeholder={t(target.kind === 'task' ? 'quickCapture.taskPlaceholder' : 'quickCapture.triagePlaceholder')}
                aria-describedby={`${id}-hint`}
                className="min-h-9 min-w-0 flex-1 bg-transparent text-sm text-content-primary outline-none placeholder:text-content-tertiary" />
            <span id={`${id}-hint`} className="hidden items-center gap-1 text-xs text-content-tertiary sm:inline-flex">
                <CornerDownLeft className="h-3 w-3" aria-hidden="true" />{t('quickCapture.enterHint')}
            </span>
            <Button type="button" variant="ghost" size="sm" disabled={capture.isPending}
                onClick={() => { const value = title; setTitle(''); capture.reset(); onExpand(value.trim()); }}>
                {t('quickCapture.moreFields')}
            </Button>
        </div>
        {capture.isPending && <p role="status" className="text-xs text-content-secondary">{t('quickCapture.saving')}</p>}
        {capture.isError && <p role="alert" className="text-sm text-feedback-danger-foreground">
            {getApiErrorMessage(capture.error, t('quickCapture.failed'))}
        </p>}
    </form>;
};

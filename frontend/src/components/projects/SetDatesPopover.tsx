import { useCallback, useEffect, useId, useLayoutEffect, useRef, useState } from 'react';
import type { ReactNode } from 'react';
import { createPortal } from 'react-dom';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { addDays, format } from 'date-fns';
import { CalendarDays } from 'lucide-react';
import { Button } from '../common/Button';
import { PlanningInputBoundary } from '../planning/PlanningInputBoundary';
import type { ObservedPlanningInput } from '../../services/planningInputService';
import { projectService } from '../../services/projectService';
import type { Project } from '../../types/project';
import { feedbackMessage, type MutationFeedbackMeta } from '../../features/mutationFeedback';
import { getApiErrorMessage, getApiErrorStatus } from '../../utils/apiError';

const PANEL_WIDTH = 288;
const GAP = 6;
const EDGE = 16;
/** A new project is proposed to run for four weeks from today. */
const DEFAULT_SPAN_DAYS = 28;

const toInputDate = (date: Date) => format(date, 'yyyy-MM-dd');

const DatesForm = ({ observed, controls, onDone }: {
    observed: ObservedPlanningInput<Project>;
    controls: ReactNode;
    onDone: () => void;
}) => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const project = observed.resource;
    const firstFieldRef = useRef<HTMLInputElement>(null);
    const [startDate, setStartDate] = useState(() => project.start_date?.slice(0, 10) || toInputDate(new Date()));
    const [targetDate, setTargetDate] = useState(() => project.target_date?.slice(0, 10)
        || toInputDate(addDays(new Date(), DEFAULT_SPAN_DAYS)));
    const outOfOrder = Boolean(startDate && targetDate && targetDate < startDate);

    useEffect(() => { firstFieldRef.current?.focus(); }, []);

    // feedback-policy: mutation pending,inline - the form is disabled while saving; a failure stays in the popover with revision recovery.
    const save = useMutation({
        mutationFn: () => projectService.update(project.id, {
            start_date: startDate || null,
            target_date: targetDate || null,
        }, observed.expected_revisions),
        meta: { success: data => feedbackMessage(t, 'saved', 'project', (data as Project).name) } satisfies MutationFeedbackMeta,
        onSuccess: updated => {
            queryClient.setQueryData(['project', project.id], updated);
            for (const queryKey of [['projects'], ['projectSummary'], ['gantt']]) {
                void queryClient.invalidateQueries({ queryKey });
            }
            onDone();
        },
    });
    const conflict = [409, 412].includes(getApiErrorStatus(save.error) ?? 0);

    return (
        <form
            className="space-y-3"
            onSubmit={event => {
                event.preventDefault();
                if (!save.isPending && !outOfOrder) save.mutate();
            }}
        >
            <fieldset disabled={save.isPending} className="m-0 grid min-w-0 grid-cols-2 gap-2 border-0 p-0">
                <label className="field">
                    <span className="field-lbl">{t('surfaces.projectForm.startDate')}</span>
                    <input ref={firstFieldRef} type="date" className="input" value={startDate}
                        onChange={event => setStartDate(event.target.value)} />
                </label>
                <label className="field">
                    <span className="field-lbl">{t('surfaces.projectForm.targetDate')}</span>
                    <input type="date" className="input" value={targetDate} aria-invalid={outOfOrder}
                        onChange={event => setTargetDate(event.target.value)} />
                </label>
            </fieldset>
            {outOfOrder && <p role="alert" className="text-sm text-feedback-danger-foreground">{t('surfaces.projectsPage.datesOutOfOrder')}</p>}
            {save.error && (
                <p role="alert" className="text-sm text-feedback-danger-foreground">
                    {getApiErrorMessage(save.error, t('surfaces.projectsPage.datesSaveFailed'))}
                </p>
            )}
            {conflict && controls}
            <div className="flex justify-end gap-2">
                <Button type="button" variant="ghost" size="sm" onClick={onDone}>{t('actions.cancel')}</Button>
                <Button type="submit" size="sm" isLoading={save.isPending} disabled={outOfOrder}>{t('surfaces.projectsPage.saveDates')}</Button>
            </div>
        </form>
    );
};

/**
 * "Set dates" for a project that has none, edited in place: a small popover
 * under the button with the start and target date, proposed as today and four
 * weeks on, so saving them is the second click.
 */
export const SetDatesPopover = ({ project }: { project: Project }) => {
    const { t } = useTranslation();
    const [open, setOpen] = useState(false);
    const [position, setPosition] = useState<{ top: number; left: number } | null>(null);
    const triggerRef = useRef<HTMLButtonElement>(null);
    const panelRef = useRef<HTMLDivElement>(null);
    const panelId = useId();
    const titleId = useId();

    const close = useCallback((restoreFocus = true) => {
        setOpen(false);
        setPosition(null);
        if (restoreFocus) triggerRef.current?.focus();
    }, []);

    const place = useCallback(() => {
        const trigger = triggerRef.current;
        if (!trigger) return;
        const rect = trigger.getBoundingClientRect();
        const height = panelRef.current?.offsetHeight ?? 0;
        const left = Math.max(EDGE, Math.min(rect.left, window.innerWidth - PANEL_WIDTH - EDGE));
        const below = rect.bottom + GAP;
        const top = below + height > window.innerHeight - EDGE && rect.top - GAP - height > EDGE
            ? rect.top - GAP - height
            : below;
        setPosition(current => (current && current.top === top && current.left === left ? current : { top, left }));
    }, []);

    useLayoutEffect(() => {
        if (open) place();
    });

    useEffect(() => {
        if (!open) return;
        const onPointerDown = (event: MouseEvent) => {
            const target = event.target as Node;
            if (panelRef.current?.contains(target) || triggerRef.current?.contains(target)) return;
            close(false);
        };
        const onKeyDown = (event: KeyboardEvent) => {
            if (event.key === 'Escape') {
                event.preventDefault();
                close();
            }
        };
        window.addEventListener('mousedown', onPointerDown);
        window.addEventListener('keydown', onKeyDown);
        window.addEventListener('resize', place);
        window.addEventListener('scroll', place, true);
        return () => {
            window.removeEventListener('mousedown', onPointerDown);
            window.removeEventListener('keydown', onKeyDown);
            window.removeEventListener('resize', place);
            window.removeEventListener('scroll', place, true);
        };
    }, [open, close, place]);

    return (
        <>
            <Button
                ref={triggerRef}
                variant="secondary"
                size="sm"
                aria-haspopup="dialog"
                aria-expanded={open}
                aria-controls={open ? panelId : undefined}
                onClick={() => (open ? close() : setOpen(true))}
            >
                <CalendarDays aria-hidden="true" className="h-3.5 w-3.5" />
                {t('surfaces.projectsPage.setDates')}
            </Button>
            {open && typeof document !== 'undefined' && createPortal(
                <div className="wc contents">
                    <div
                        ref={panelRef}
                        id={panelId}
                        role="dialog"
                        aria-modal="false"
                        aria-labelledby={titleId}
                        className="projects-dates-popover"
                        style={{ top: position?.top ?? 0, left: position?.left ?? 0, visibility: position ? 'visible' : 'hidden' }}
                    >
                        <p id={titleId} className="projects-dates-popover-title">
                            {t('surfaces.projectsPage.setDatesFor', { name: project.name })}
                        </p>
                        <PlanningInputBoundary<Project> kind="project" resourceId={project.id} onCancel={() => close()}>
                            {(observed, controls) => <DatesForm observed={observed} controls={controls} onDone={() => close()} />}
                        </PlanningInputBoundary>
                    </div>
                </div>,
                document.body,
            )}
        </>
    );
};

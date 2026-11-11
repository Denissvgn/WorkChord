import { useEffect, useId, useRef, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { Button } from '../common/Button';
import { QueryErrorState } from '../feedback/QueryState';
import { teamService } from '../../services/teamService';
import type { GanttTask } from '../../types/gantt';

export interface GanttBarInputChanges {
    assignee: { id: number; name: string } | null;
    effort_days: number | null;
    min_start_date: string | null;
    max_end_date: string | null;
    dependencies: number[];
}

interface GanttBarInputsProps {
    task: GanttTask;
    iterationId: number;
    /** Other tasks this one may wait for. */
    taskOptions: Array<{ id: number; title: string }>;
    anchor: { top: number; left: number };
    onApply: (changes: GanttBarInputChanges) => void;
    onMoreFields: () => void;
    onClose: () => void;
}

/**
 * The five inputs that move a task's dates. Dates themselves are scheduler
 * output, so this edits inputs only; the sandbox then recalculates.
 */
export const GanttBarInputs = ({ task, iterationId, taskOptions, anchor, onApply, onMoreFields, onClose }: GanttBarInputsProps) => {
    const { t } = useTranslation();
    const id = useId();
    const firstFieldRef = useRef<HTMLSelectElement>(null);
    // feedback-policy: query loading,error,retry,empty
    const team = useQuery({ queryKey: ['team', iterationId], queryFn: () => teamService.getByIteration(iterationId) });
    const [assigneeId, setAssigneeId] = useState(task.assignee ? String(task.assignee.id) : '');
    const [effort, setEffort] = useState(task.effort_days === null ? '' : String(task.effort_days));
    const [earliestStart, setEarliestStart] = useState(task.min_start_date ?? '');
    const [dueBy, setDueBy] = useState(task.max_end_date ?? '');
    const [waitsFor, setWaitsFor] = useState<number[]>(task.dependencies ?? []);

    useEffect(() => { firstFieldRef.current?.focus(); }, []);
    // Escape closes the popover and returns focus to the bar.
    useEffect(() => {
        const closeOnEscape = (event: KeyboardEvent) => {
            if (event.key === 'Escape') onClose();
        };
        window.addEventListener('keydown', closeOnEscape);
        return () => window.removeEventListener('keydown', closeOnEscape);
    }, [onClose]);
    const apply = () => {
        const member = (team.data ?? []).find(item => String(item.id) === assigneeId);
        const parsedEffort = effort.trim() === '' ? null : Number(effort);
        onApply({
            assignee: member ? { id: member.id, name: member.name } : null,
            effort_days: parsedEffort !== null && Number.isFinite(parsedEffort) && parsedEffort > 0 ? parsedEffort : null,
            min_start_date: earliestStart || null,
            max_end_date: dueBy || null,
            dependencies: waitsFor,
        });
    };

    return (
        <div
            role="dialog"
            aria-modal="false"
            aria-labelledby={`${id}-title`}
            className="fixed z-50 w-80 max-w-[calc(100vw-2rem)] space-y-3 rounded-lg border border-border bg-surface-card p-4 shadow-lg"
            style={{ top: anchor.top, left: anchor.left }}
        >
            <div>
                <h3 id={`${id}-title`} className="font-semibold text-content-primary">{task.title}</h3>
                <p className="text-xs text-content-secondary">{t('gantt.datesAreCalculated')}</p>
            </div>
            {team.isError && <QueryErrorState error={team.error} fallback={t('queryFeedback.optionLoadFailed')} onRetry={() => void team.refetch()} />}
            <label className="block">
                <span className="field-lbl">{t('gantt.inputAssignee')}</span>
                <select ref={firstFieldRef} className="input w-full" value={assigneeId} onChange={event => setAssigneeId(event.target.value)}>
                    <option value="">{t('common.unassigned')}</option>
                    {(team.data ?? []).map(member => <option key={member.id} value={member.id}>{member.name}</option>)}
                </select>
            </label>
            <label className="block">
                <span className="field-lbl">{t('gantt.inputEffort')}</span>
                <input className="input w-full" type="number" min="0" step="0.5" value={effort} onChange={event => setEffort(event.target.value)} />
            </label>
            <div className="grid grid-cols-2 gap-2">
                <label className="block">
                    <span className="field-lbl">{t('gantt.inputEarliestStart')}</span>
                    <input className="input w-full" type="date" value={earliestStart} onChange={event => setEarliestStart(event.target.value)} />
                </label>
                <label className="block">
                    <span className="field-lbl">{t('gantt.inputDueBy')}</span>
                    <input className="input w-full" type="date" value={dueBy} onChange={event => setDueBy(event.target.value)} />
                </label>
            </div>
            <label className="block">
                <span className="field-lbl">{t('gantt.inputWaitsFor')}</span>
                <select multiple className="input h-24 w-full" value={waitsFor.map(String)}
                    onChange={event => setWaitsFor(Array.from(event.target.selectedOptions, option => Number(option.value)))}>
                    {taskOptions.filter(option => option.id !== task.id).map(option => (
                        <option key={option.id} value={option.id}>#{option.id} · {option.title}</option>
                    ))}
                </select>
            </label>
            <div className="flex flex-wrap justify-end gap-2">
                <Button type="button" variant="ghost" size="sm" onClick={onMoreFields}>{t('gantt.moreFields')}</Button>
                <Button type="button" variant="secondary" size="sm" onClick={onClose}>{t('actions.cancel')}</Button>
                <Button type="button" size="sm" onClick={apply}>{t('gantt.tryTheseInputs')}</Button>
            </div>
        </div>
    );
};

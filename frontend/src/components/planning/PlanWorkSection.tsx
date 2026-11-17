import { ButtonLink } from '../common/ButtonLink';
import { useState } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { Button } from '../common/Button';
import { Modal } from '../common/Modal';
import { QueryErrorState } from '../feedback/QueryState';
import { ImportTasksModal } from '../tasks/ImportTasksModal';
import { GuardedTaskDrawer } from '../tasks/GuardedTaskDrawer';
import { taskService } from '../../services/taskService';
import { iterationService } from '../../services/iterationService';
import { useScopeLink } from '../../features/scope/useScopeLink';
import { withPlanReturn } from '../../features/planningMasters/planningReturn';
import type { Iteration } from '../../types/iteration';
import type { Task, TaskReference } from '../../types/task';
import { formatDecimal } from '../../utils/workNumbers';
import { getApiErrorMessage } from '../../utils/apiError';

export const PlanWorkSection = ({ iteration, tasks, count }: { iteration: Iteration; tasks: Task[]; count: number }) => {
    const { t, i18n } = useTranslation();
    const scopeLink = useScopeLink();
    const client = useQueryClient();
    const [picker, setPicker] = useState(false);
    const [importing, setImporting] = useState(false);
    const [creating, setCreating] = useState(false);
    const refresh = async () => {
        await Promise.all(['tasks', 'backlog', 'planning-navigation-summary', 'workload', 'gantt', 'projectSummary'].map(key => client.invalidateQueries({ queryKey: [key] })));
    };
    const hours = tasks.reduce((sum, task) => sum + (task.effort_hours ?? (task.effort_days ?? 0) * (task.nominal_day_hours ?? 8)), 0);
    return <div className="space-y-4">
        <p>{t('planWork.total', { count, hours: formatDecimal(hours, i18n.language) })}</p>
        {tasks.some(task => !task.effort_days) && <p className="text-sm text-content-secondary">{t('planWork.unknownEffort')}</p>}
        <div className="flex flex-wrap gap-2">
            {/* A new task is created here in this iteration, so planning never has to leave Plan to add work. */}
            <Button variant={count === 0 ? 'primary' : 'secondary'} onClick={() => setCreating(true)}>{t('tasks.newTask')}</Button>
            <Button variant="secondary" disabled={!iteration.project_id} onClick={() => setPicker(true)}>{t('planWork.addBacklog')}</Button>
            <Button variant="secondary" onClick={() => setImporting(true)}>{t('planWork.import')}</Button>
            <ButtonLink  to={scopeLink(withPlanReturn('/tasks', 'work'))} variant="secondary">{t('planWork.openTasks')}</ButtonLink>
        </div>
        {!iteration.project_id && <p className="text-sm text-content-secondary">{t('planWork.projectRequired')}</p>}
        {picker && iteration.project_id && <BacklogPicker iteration={iteration} onClose={() => setPicker(false)} onChanged={refresh} />}
        {creating && <GuardedTaskDrawer title={t('tasks.createNewTask')} closeLabel={t('actions.close')} iterationId={iteration.id}
            onClose={() => { setCreating(false); void refresh(); }} />}
        {importing && <ImportTasksModal iterationId={iteration.id} onClose={() => { setImporting(false); void refresh(); }} />}
    </div>;
};

const BacklogPicker = ({ iteration, onClose, onChanged }: { iteration: Iteration; onClose: () => void; onChanged: () => Promise<void> }) => {
    const { t } = useTranslation();
    const [selected, setSelected] = useState<number[]>([]);
    const [pending, setPending] = useState(false);
    const [error, setError] = useState<string | null>(null);
    // feedback-policy: query loading,error,retry,empty - the picker renders each query state below.
    const backlog = useQuery({ queryKey: ['backlog', 'plan-picker', iteration.project_id], queryFn: async () => {
        const items: TaskReference[] = [];
        let after_id = 0;
        for (;;) {
            const page = await taskService.lookup({ project_id: iteration.project_id!, backlog_only: true, roots_only: true, task_status: 'planned', after_id, limit: 100 });
            items.push(...page.items);
            if (!page.has_more) return items;
            after_id = page.next_after_id!;
        }
    } });
    const add = async () => {
        setPending(true); setError(null);
        let added = 0;
        try {
            let revision = (await iterationService.getById(iteration.id)).revision;
            if (revision === undefined) throw new Error(t('planWork.refreshRequired'));
            for (const id of selected) {
                const task = backlog.data?.find(task => task.id === id);
                if (!task) throw new Error(t('planWork.refreshRequired'));
                const moved = await taskService.move(id, { iteration_id: iteration.id, expected_version: task.version, expected_revisions: { [iteration.id]: revision } });
                added++;
                setSelected(ids => ids.filter(value => value !== id));
                revision = moved.iteration_revision;
                if (revision === undefined) throw new Error(t('planWork.refreshRequired'));
            }
            onClose();
        } catch (err) {
            setError(t('planWork.addFailed', { count: added }) + ' ' + getApiErrorMessage(err, t('planWork.refreshRequired')));
        } finally { await onChanged(); setPending(false); }
    };
    return <Modal open title={t('planWork.addBacklog')} closeLabel={t('actions.close')} onClose={onClose} closeDisabled={pending}
        footer={<Button disabled={pending || !selected.length || backlog.isError} onClick={() => void add()}>{t('planWork.addSelected', { count: selected.length })}</Button>}>
        {backlog.isLoading && <p role="status">{t('common.loading')}</p>}
        {backlog.isError && <QueryErrorState error={backlog.error} onRetry={() => void backlog.refetch()} />}
        {error && <p role="alert" className="text-feedback-danger-foreground">{error}</p>}
        {backlog.isSuccess && !backlog.data.length && <p>{t('planWork.emptyBacklog')}</p>}
        <ul className="divide-y divide-border">{backlog.data?.map(task => <li key={task.id} className="py-3">
            <label className="flex items-center gap-3"><input type="checkbox" disabled={pending} checked={selected.includes(task.id)}
                onChange={event => setSelected(ids => event.target.checked ? [...ids, task.id] : ids.filter(id => id !== task.id))} />{task.title}</label>
        </li>)}</ul>
    </Modal>;
};

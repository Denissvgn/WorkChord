import { useMemo, useState } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { Bot, UserRound } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { Button } from '../common/Button';
import { QueryErrorState } from '../feedback/QueryState';
import { taskService } from '../../services/taskService';
import { teamService } from '../../services/teamService';
import { labelService } from '../../services/labelService';
import { iterationService } from '../../services/iterationService';
import { planningIssueTasksHref, taskMatchesPlanningIssue } from '../../features/planningMasters/planningTaskIssues';
import { useScopeLink } from '../../features/scope/useScopeLink';
import type { Task, TaskBulkOperationRequest, TaskBulkOperationResponse } from '../../types/task';
import type { TeamMember } from '../../types/team';
import { formatDecimal } from '../../utils/workNumbers';
import { getApiErrorMessage } from '../../utils/apiError';

interface Props { iterationId: number; tasks: Task[]; members: TeamMember[]; unassignedCount: number; effortCount: number }
interface RowLoad { member: TeamMember; current: number; capacity: number; added: number; unknown: boolean }
interface Batch { request: TaskBulkOperationRequest; response: TaskBulkOperationResponse }
const effortHours = (task: Task) => task.effort_hours ?? (task.effort_days ?? 0) * (task.nominal_day_hours ?? 8);

export const PlanBlockersSection = ({ iterationId, tasks, members, unassignedCount, effortCount }: Props) => {
    const { t, i18n } = useTranslation();
    const scopeLink = useScopeLink();
    const client = useQueryClient();
    const unassigned = useMemo(() => tasks.filter(task => taskMatchesPlanningIssue(task, 'unassigned')), [tasks]);
    const missingEffort = tasks.filter(task => taskMatchesPlanningIssue(task, 'missing-effort'));
    const [choices, setChoices] = useState<Record<string, number>>({});
    const [preview, setPreview] = useState<{ signature: string; batches: Batch[]; loads: RowLoad[] } | null>(null);
    const [pending, setPending] = useState(false);
    const [message, setMessage] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);
    const refresh = async () => {
        await Promise.all(['tasks', 'planning-navigation-summary', 'plan-assignment', 'workload', 'gantt', 'projectSummary'].map(key => client.invalidateQueries({ queryKey: [key] })));
    };
    // feedback-policy: query loading,error,retry,empty - assignment controls wait for complete recommendations and workloads; errors offer retry.
    const options = useQuery({ queryKey: ['plan-assignment', iterationId, unassigned.map(task => [task.id, task.version]), members.map(member => member.id)],
        enabled: unassigned.length > 0,
        queryFn: async () => {
            const [labels, recommendations, workloads] = await Promise.all([
                labelService.getLabels({ group_key: 'capability', include_inactive: true }),
                Promise.all(unassigned.map(async task => ({ id: task.id, rows: await taskService.getAssigneeRecommendations(task.id) }))),
                Promise.all(members.map(member => teamService.getWorkload(member.id))),
            ]);
            return { labels, recommendations, workloads };
        },
    });
    const groups = useMemo(() => {
        const byLabel = new Map<string, { key: string; label: string; tasks: Task[]; recommended?: number }>();
        for (const task of unassigned) {
            const labels = (options.data?.labels ?? []).filter(label => task.tags.includes(label.slug)).sort((a, b) => a.slug.localeCompare(b.slug));
            const key = JSON.stringify(labels.map(label => label.slug));
            const group = byLabel.get(key) ?? { key, label: labels.map(label => label.name).join(' + ') || t('planWork.noCapability'), tasks: [] };
            group.tasks.push(task); byLabel.set(key, group);
        }
        for (const group of byLabel.values()) {
            const scores = new Map<number, number>();
            for (const task of group.tasks) {
                for (const row of options.data?.recommendations.find(item => item.id === task.id)?.rows ?? []) {
                    if (members.some(member => member.id === row.team_member_id)) scores.set(row.team_member_id, (scores.get(row.team_member_id) ?? 0) + row.score);
                }
            }
            group.recommended = [...scores.entries()].sort((a, b) => b[1] - a[1])[0]?.[0];
        }
        return [...byLabel.values()];
    }, [unassigned, options.data, members, t]);
    const selectedRow = (group: typeof groups[number]) => choices[group.key] ?? group.recommended;
    const assignments = groups.map(group => ({ row: selectedRow(group), tasks: group.tasks }));
    const signature = JSON.stringify([assignments.map(group => [group.row, group.tasks.map(task => [task.id, task.version])]), options.dataUpdatedAt]);
    const currentPreview = preview?.signature === signature ? preview : null;
    const rowLoads = members.flatMap(member => {
        const assigned = assignments.filter(group => group.row === member.id).flatMap(group => group.tasks);
        if (!assigned.length) return [];
        const workload = options.data?.workloads.find(row => row.team_member_id === member.id);
        const day = workload?.nominal_day_hours ?? 8;
        const current = workload?.allocated_hours ?? (workload?.allocated_days ?? 0) * day;
        const capacity = workload?.capacity_hours ?? (workload?.capacity_days ?? 0) * day;
        return [{ member, current, capacity, added: assigned.reduce((sum, task) => sum + effortHours(task), 0), unknown: assigned.some(task => !(task.effort_days && task.effort_days > 0)) }];
    });
    const previewAssignments = async () => {
        setPending(true); setError(null); setMessage(null); setPreview(null);
        try {
            const revision = (await iterationService.getById(iterationId)).revision;
            if (revision === undefined) throw new Error(t('planWork.refreshRequired'));
            const workloads = await Promise.all(rowLoads.map(load => teamService.getWorkload(load.member.id)));
            const loads = rowLoads.map(load => {
                const workload = workloads.find(row => row.team_member_id === load.member.id)!;
                const day = workload.nominal_day_hours ?? 8;
                return { ...load, current: workload.allocated_hours ?? workload.allocated_days * day,
                    capacity: workload.capacity_hours ?? workload.capacity_days * day };
            });
            const batches: Batch[] = [];
            for (const load of rowLoads) {
                const selected = assignments.filter(group => group.row === load.member.id).flatMap(group => group.tasks);
                const request: TaskBulkOperationRequest = { task_ids: selected.map(task => task.id), action: 'set_assignee', payload: { assignee_id: load.member.id }, dry_run: true,
                    expected_versions: Object.fromEntries(selected.map(task => [task.id, task.version])), expected_revisions: { [iterationId]: revision } };
                const response = await taskService.runBulkOperation(request);
                if (response.failed_count || response.results.length !== selected.length || response.results.some(result => result.outcome !== 'would_update')
                    || response.input_revisions?.[iterationId] !== revision || selected.some(task => response.task_versions?.[task.id] !== task.version)) {
                    throw new Error(response.results.find(result => result.error)?.error || t('planWork.refreshRequired'));
                }
                batches.push({ request, response });
            }
            setPreview({ signature, batches, loads });
        } catch (err) { setError(getApiErrorMessage(err, t('planWork.refreshRequired'))); }
        finally { setPending(false); }
    };
    const apply = async () => {
        if (!currentPreview) return;
        setPending(true); setError(null); setMessage(null);
        let applied = 0;
        try {
            let revisions = currentPreview.batches[0].response.input_revisions;
            for (const batch of currentPreview.batches) {
                const response = await taskService.runBulkOperation({ ...batch.request, dry_run: false,
                    expected_versions: batch.response.task_versions, expected_revisions: revisions });
                applied += response.results.filter(result => result.outcome === 'updated').length;
                if (response.failed_count || response.results.some(result => result.outcome !== 'updated')) throw new Error(t('planWork.refreshRequired'));
                const revision = response.results[0]?.task?.iteration_revision;
                if (revision === undefined) throw new Error(t('planWork.refreshRequired'));
                revisions = { [iterationId]: revision };
            }
            setMessage(t('planWork.assigned', { count: applied }));
        } catch (err) { setError(t('planWork.assignFailed', { count: applied }) + ' ' + getApiErrorMessage(err, t('planWork.refreshRequired'))); }
        finally { setPreview(null); await refresh(); setPending(false); }
    };
    const tasksLink = (issue: 'unassigned' | 'missing-effort') => scopeLink(planningIssueTasksHref({ issue, iterationId, returnStepId: 'blockers' }));
    const hours = (value: number) => t('capacity.hourValue', { hours: formatDecimal(value, i18n.language) });
    return <div className="space-y-6">
        <section aria-labelledby="plan-needs-assignee" className="space-y-3">
            <div className="flex flex-wrap items-center justify-between gap-3"><h3 id="plan-needs-assignee" className="font-semibold">{t('planWork.needsAssignee', { count: unassignedCount })}</h3>
                <Link className="text-action underline" to={tasksLink('unassigned')}>{t('planWork.editSelection')}</Link></div>
            {options.isLoading && <p role="status">{t('common.loading')}</p>}
            {options.isError && <QueryErrorState error={options.error} onRetry={() => void options.refetch()} />}
            {!unassigned.length && <p className="text-content-secondary">{t('planWork.noAssigneeGaps')}</p>}
            {options.isSuccess && groups.map(group => {
                const row = members.find(member => member.id === selectedRow(group));
                const recommended = members.find(member => member.id === group.recommended);
                const workload = options.data.workloads.find(load => load.team_member_id === row?.id);
                return <div key={group.key} className="border-b border-border py-3 space-y-2">
                    <div className="flex flex-wrap items-center justify-between gap-3"><div className="min-w-0"><h4 className="font-medium">{group.label} · {t('planWork.taskCount', { count: group.tasks.length })}</h4>
                        <p className="text-sm text-content-secondary">{recommended ? t('planWork.recommended', { name: recommended.name }) : t('planWork.chooseRow')}</p></div>
                        <label className="flex items-center gap-2">{row?.profile?.profile_kind === 'agent' ? <Bot size={16} aria-label={t('capacity.agent')} /> : <UserRound size={16} aria-label={t('capacity.person')} />}
                            <span className="sr-only">{t('planWork.assigneeFor', { label: group.label })}</span>
                            <select className="input" disabled={pending} value={selectedRow(group) ?? ''} onChange={event => { setChoices(values => ({ ...values, [group.key]: Number(event.target.value) })); setPreview(null); }}>
                                <option value="" disabled>{t('planWork.chooseRow')}</option>{members.map(member => <option value={member.id} key={member.id}>{member.name}</option>)}
                            </select></label></div>
                    {workload && <p className="text-sm text-content-secondary">{t('planWork.currentLoad', { hours: hours(workload.allocated_hours ?? workload.allocated_days * (workload.nominal_day_hours ?? 8)), capacity: hours(workload.capacity_hours ?? workload.capacity_days * (workload.nominal_day_hours ?? 8)) })}</p>}
                    <details><summary className="cursor-pointer text-sm text-action">{t('planWork.showTasks')}</summary><ul className="mt-2 space-y-1">{group.tasks.map(task => <li key={task.id}>{task.title}</li>)}</ul></details>
                </div>;
            })}
            {currentPreview && <div className="space-y-3" role="region" aria-label={t('planWork.preview')}>
                <h4 className="font-semibold">{t('planWork.preview')}</h4>
                <div className="overflow-x-auto"><table className="w-full text-left text-sm"><thead><tr>{['row', 'current', 'added', 'result', 'capacity'].map(key => <th key={key} className="px-2 py-2">{t(`planWork.${key}`)}</th>)}</tr></thead>
                    <tbody>{currentPreview.loads.map(load => <tr key={load.member.id} className={load.current + load.added > load.capacity ? 'bg-feedback-warning-muted text-feedback-warning-foreground' : ''}>
                        <th scope="row" className="px-2 py-3">{load.member.name}</th><td className="px-2 py-3">{hours(load.current)}</td><td className="px-2 py-3">{hours(load.added)}</td><td className="px-2 py-3">{hours(load.current + load.added)}
                            {load.current + load.added > load.capacity && <strong className="block">{t('planWork.overCapacity')}</strong>}{load.unknown && <span className="block">{t('planWork.unknownEffort')}</span>}</td><td className="px-2 py-3">{hours(load.capacity)}</td>
                    </tr>)}</tbody></table></div>
                {currentPreview.batches.flatMap(batch => batch.response.results.flatMap(result => result.warnings.map((warning, index) => <p key={`${result.task_id}-${index}`} className="text-sm">{warning}</p>)))}
            </div>}
            {unassigned.length > 0 && <div className="flex flex-wrap gap-2"><Button variant="secondary" disabled={pending || !options.isSuccess || options.isFetching || assignments.some(group => !members.some(member => member.id === group.row))} onClick={() => void previewAssignments()}>{t('planWork.preview')}</Button>
                {currentPreview && <Button disabled={pending || options.isFetching} onClick={() => void apply()}>{t('planWork.assign', { count: unassigned.length })}</Button>}</div>}
            {message && <p role="status">{message}</p>}{error && <p role="alert" className="text-feedback-danger-foreground">{error}</p>}
        </section>
        <section aria-labelledby="plan-needs-effort" className="space-y-3">
            <div className="flex flex-wrap items-center justify-between gap-3"><h3 id="plan-needs-effort" className="font-semibold">{t('planWork.needsEffort', { count: effortCount })}</h3>
                <Link className="text-action underline" to={tasksLink('missing-effort')}>{t('planWork.editSelection')}</Link></div>
            {!missingEffort.length && <p className="text-content-secondary">{t('planWork.noEffortGaps')}</p>}
            <ul className="divide-y divide-border">{missingEffort.map(task => <EffortRow key={`${task.id}-${task.version}`} task={task} disabled={pending} onSaved={async () => { setPreview(null); await refresh(); }} />)}</ul>
        </section>
    </div>;
};

const EffortRow = ({ task, disabled, onSaved }: { task: Task; disabled: boolean; onSaved: () => Promise<void> }) => {
    const { t, i18n } = useTranslation();
    const [value, setValue] = useState('');
    const [pending, setPending] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const hours = Number(value);
    const save = async () => {
        setPending(true); setError(null);
        try {
            const iteration = await iterationService.getById(task.iteration_id!);
            if (iteration.revision === undefined) throw new Error(t('planWork.refreshRequired'));
            await taskService.update(task.id, { effort_hours: hours, expected_version: task.version, expected_revision: iteration.revision });
            await onSaved();
        } catch (err) { setError(getApiErrorMessage(err, t('planWork.refreshRequired'))); }
        finally { setPending(false); }
    };
    return <li className="py-3"><form className="flex flex-wrap items-center gap-3" onSubmit={event => { event.preventDefault(); void save(); }}>
        <label className="min-w-0 flex-1" htmlFor={`plan-effort-${task.id}`}>{task.title}<span className="block text-sm text-content-secondary">{t('planWork.effortHours')}</span></label>
        <div><input id={`plan-effort-${task.id}`} className="input w-28" type="number" min="0.01" step="any" required disabled={disabled || pending} value={value} onChange={event => setValue(event.target.value)} aria-describedby={`plan-days-${task.id}`} />
            <p id={`plan-days-${task.id}`} className="text-xs text-content-secondary">{t('planWork.days', { days: formatDecimal(hours / (task.nominal_day_hours ?? 8), i18n.language), hours: task.nominal_day_hours ?? 8 })}</p></div>
        <Button type="submit" variant="secondary" disabled={disabled || pending || !Number.isFinite(hours) || hours <= 0}>{t('actions.save')}</Button>
    </form>{error && <p role="alert" className="text-feedback-danger-foreground">{error}</p>}</li>;
};

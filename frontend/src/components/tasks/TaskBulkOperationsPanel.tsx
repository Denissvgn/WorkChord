import { useEffect, useMemo, useRef, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { Trash2 } from 'lucide-react';
import { Button } from '../common/Button';
import { OverflowMenu } from '../ui/OverflowMenu';
import { taskService } from '../../services/taskService';
import { teamService } from '../../services/teamService';
import { projectService } from '../../services/projectService';
import { iterationService } from '../../services/iterationService';
import { getApiErrorMessage } from '../../utils/apiError';
import { QueryErrorState } from '../feedback/QueryState';
import type { Task, TaskBulkAction, TaskBulkOperationResponse, TaskStatus } from '../../types/task';
import { resultsNeedingRouting, routingChangeItems, routingNeedsResolution, type RoutingChangeItem } from '../../utils/routingCheck';
import { RoutingResultsList } from './RoutingCheckNotice';
import type { MutationFeedbackMeta } from '../../features/mutationFeedback';

import { Select } from '../../components/common/Select';
type BulkKind = 'assign' | 'status' | 'priority' | 'iteration' | 'project' | 'clearProject' | 'milestone' | 'clearMilestone' | 'addLabels' | 'removeLabels' | 'flags' | 'delete';

/** What the bar needs of a selected task. */
export type BulkSelectedTask = Pick<Task, 'id' | 'title' | 'version'>;

interface TaskBulkOperationsPanelProps {
    iterationId: number;
    /** The selected tasks, all leaves of one iteration. */
    selectedTasks: BulkSelectedTask[];
    /** How many tasks match the list's filters; offered as "Select all n matching". */
    matchingCount: number;
    onSelectAll: () => void;
    onClearSelection: () => void;
    /** Opens the merge dialog; offered for two or more tasks. */
    onMerge?: () => void;
    /** Open the Assign step on arrival, for hand-offs that come to assign work. */
    openAssign?: boolean;
}

const STATUS_OPTIONS: TaskStatus[] = ['planned', 'active', 'resolved', 'closed'];
const AUTO = '__auto__';
const NONE = '__none__';
const selectClassName = 'h-8 rounded-md border border-border-strong bg-surface-card px-2 text-sm text-content-primary focus:outline-hidden focus-visible:ring-2 focus-visible:ring-focus';

type RoutingChoice = 'apply_suggestion' | 'keep';

/**
 * A dry run that found tasks whose reviewer would no longer fit; nothing was written. It keeps the
 * versions it was read at, and what it was read for, so a changed selection or choice drops it.
 */
interface RoutingDecision {
    signature: string;
    items: RoutingChangeItem[];
    canKeep: boolean;
    versions: TaskBulkOperationResponse['task_versions'];
    revisions: TaskBulkOperationResponse['input_revisions'];
}

const isRoutingDecision = (value: unknown): value is RoutingDecision => Boolean(value) && typeof value === 'object' && 'signature' in (value as object);

class BulkRejected extends Error {
    readonly failures: { taskId: number; message: string }[];
    constructor(failures: { taskId: number; message: string }[]) { super('bulk-rejected'); this.failures = failures; }
}

/**
 * The bar shown while tasks are selected. Each change is one choice and one Apply: the server
 * checks it first (a dry run), then applies it, so a rejected change leaves every task untouched.
 */
export const TaskBulkOperationsPanel = ({
    iterationId, selectedTasks, matchingCount, onSelectAll, onClearSelection, onMerge, openAssign = false,
}: TaskBulkOperationsPanelProps) => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const [kind, setKind] = useState<BulkKind | null>(openAssign ? 'assign' : null);
    const [value, setValue] = useState('');
    const [reason, setReason] = useState('');
    const [milestoneId, setMilestoneId] = useState('');
    const [isOptional, setIsOptional] = useState('');
    const [isDeferred, setIsDeferred] = useState('');
    const [failures, setFailures] = useState<{ taskId: number; message: string }[]>([]);
    const [decision, setDecision] = useState<RoutingDecision | null>(null);
    const selectedCount = selectedTasks.length;
    const signature = JSON.stringify([kind, value, selectedTasks.map(task => [task.id, task.version])]);
    const currentDecision = decision && decision.signature === signature ? decision : null;
    const titles = useMemo(() => new Map(selectedTasks.map(task => [task.id, task.title])), [selectedTasks]);

    const teamQuery = useQuery({ queryKey: ['team', iterationId], queryFn: () => teamService.getByIteration(iterationId), enabled: kind === 'assign' });
    const iterationsQuery = useQuery({ queryKey: ['iterations'], queryFn: () => iterationService.getAll(), enabled: kind === 'iteration' });
    const iterationQuery = useQuery({ queryKey: ['iteration', iterationId], queryFn: () => iterationService.getById(iterationId) });
    const projectsQuery = useQuery({ queryKey: ['projects'], queryFn: () => projectService.getAll(), enabled: kind === 'project' || kind === 'milestone' });
    const scopedProjectId = iterationQuery.data?.project_id ?? null;
    const projectId = scopedProjectId ?? (value && (kind === 'project' || kind === 'milestone') ? Number(value) : null);
    const milestonesQuery = useQuery({ queryKey: ['projectMilestones', projectId], queryFn: () => projectService.getMilestones(projectId!), enabled: projectId !== null });

    // Opening a change puts focus on its first choice, so it is one keystroke from Apply.
    const editorRef = useRef<HTMLDivElement>(null);
    useEffect(() => { editorRef.current?.querySelector<HTMLElement>('select, input')?.focus(); }, [kind]);

    const choose = (next: BulkKind | null) => {
        setKind(next); setValue(''); setReason(''); setMilestoneId(''); setIsOptional(''); setIsDeferred(''); setFailures([]); setDecision(null);
    };

    const request = (): { action: TaskBulkAction; payload: Record<string, unknown> } | null => {
        switch (kind) {
            case 'assign':
                if (value === NONE) return { action: 'clear_assignee', payload: {} };
                if (value === AUTO) return { action: 'auto_assign', payload: { min_confidence: 0.5 } };
                return value ? { action: 'set_assignee', payload: { assignee_id: Number(value) } } : null;
            case 'status':
                return value ? { action: 'change_status', payload: { status: value, reason: reason.trim() || undefined } } : null;
            case 'priority': {
                const priority = Number(value);
                return Number.isInteger(priority) && priority >= 1 && priority <= 10 ? { action: 'set_priority', payload: { priority } } : null;
            }
            case 'project':
                return scopedProjectId !== null || value
                    ? { action: 'set_project', payload: { project_id: scopedProjectId ?? Number(value), ...(milestoneId ? { milestone_id: Number(milestoneId) } : {}) } }
                    : null;
            case 'clearProject':
                // An iteration that belongs to a project keeps it, so the server would refuse this.
                return iterationQuery.isSuccess && scopedProjectId === null ? { action: 'clear_project', payload: {} } : null;
            case 'milestone':
                return milestoneId ? { action: 'set_milestone', payload: { milestone_id: Number(milestoneId) } } : null;
            case 'clearMilestone':
                return { action: 'clear_milestone', payload: {} };
            case 'addLabels':
            case 'removeLabels': {
                const labels = value.split(/[\n,]/).map(label => label.trim()).filter(Boolean);
                return labels.length ? { action: kind === 'addLabels' ? 'add_labels' : 'remove_labels', payload: { labels } } : null;
            }
            case 'flags':
                return isOptional || isDeferred
                    ? { action: 'set_flags', payload: { ...(isOptional ? { is_optional: isOptional === 'true' } : {}), ...(isDeferred ? { is_deferred: isDeferred === 'true' } : {}) } }
                    : null;
            case 'delete':
                return { action: 'delete', payload: {} };
            default:
                return null;
        }
    };

    const mutation = useMutation<unknown, Error, RoutingChoice | undefined>({
        mutationFn: async (choice) => {
            const taskIds = selectedTasks.map(task => task.id);
            if (kind === 'iteration') {
                const targetId = Number(value);
                let moved = 0;
                try {
                    for (const task of selectedTasks) {
                        const [source, target] = await Promise.all([iterationService.getById(iterationId), iterationService.getById(targetId)]);
                        await taskService.move(task.id, {
                            iteration_id: targetId, parent_id: null, expected_version: task.version,
                            expected_revisions: Object.fromEntries([[iterationId, source.revision], [targetId, target.revision]].filter(([, revision]) => revision !== undefined)),
                        });
                        moved += 1;
                    }
                } catch (error) {
                    throw new Error(t('surfaces.taskBulk.movePartial', { done: moved, count: taskIds.length, message: getApiErrorMessage(error, t('surfaces.taskBulk.failedToRun')) }));
                }
                return null;
            }
            const base = request();
            if (!base) return null;
            // Choosing the suggested routing rides with the change; keeping the reviewers sends the plain change.
            const operation = choice === 'apply_suggestion' ? { ...base, payload: { ...base.payload, routing_resolution: choice } } : base;
            // A confirmation is read at the versions the list was shown at.
            const expected = choice && currentDecision ? { expected_versions: currentDecision.versions, expected_revisions: currentDecision.revisions } : {};
            const check = await taskService.runBulkOperation({ task_ids: taskIds, ...operation, ...expected, dry_run: true });
            const failed = check.results.filter(result => result.outcome === 'failed');
            const needsRouting = resultsNeedingRouting(check.results);
            // A refused reviewer conflict is a decision to take, not a rejection, until the person has taken it.
            const onlyRouting = choice === undefined && failed.every(result => routingNeedsResolution(result.routing_check));
            if (failed.length > 0 && !onlyRouting) {
                throw new BulkRejected(failed.map(result => ({ taskId: result.task_id, message: result.error ?? t('surfaces.taskBulk.failedToRun') })));
            }
            if (choice === undefined && needsRouting.length > 0) {
                // List exactly what using the suggested routing would change: it can rewrite more tasks than the ones that conflict.
                const suggested = await taskService.runBulkOperation({
                    task_ids: taskIds, ...base, payload: { ...base.payload, routing_resolution: 'apply_suggestion' },
                    expected_versions: check.task_versions, expected_revisions: check.input_revisions, dry_run: true,
                });
                return {
                    signature, items: routingChangeItems(needsRouting, suggested.results), canKeep: needsRouting.every(result => result.routing_check?.conflict_mode === 'warn'),
                    versions: check.task_versions, revisions: check.input_revisions,
                } satisfies RoutingDecision;
            }
            if (choice === 'apply_suggestion' && currentDecision) {
                const shown = currentDecision.items.map(item => item.taskId).sort().join();
                const rewritten = routingChangeItems([], check.results).map(item => item.taskId).sort().join();
                // The server would now rewrite something other than what was shown: show the new list instead of saving.
                if (shown !== rewritten) {
                    const modes = check.results.flatMap(result => result.routing_check ? [result.routing_check.conflict_mode] : []);
                    return { ...currentDecision, items: routingChangeItems(needsRouting, check.results), canKeep: modes.length > 0 ? modes.every(mode => mode === 'warn') : currentDecision.canKeep } satisfies RoutingDecision;
                }
            }
            return taskService.runBulkOperation({
                task_ids: taskIds, ...operation, ...expected, dry_run: false,
                ...(choice && currentDecision ? {} : { expected_versions: check.task_versions, expected_revisions: check.input_revisions }),
            });
        },
        // Stopping at the reviewer list changes nothing, so it announces nothing.
        meta: { success: (data) => isRoutingDecision(data) ? '' : t('feedback.bulkApplied', { count: selectedCount }) } satisfies MutationFeedbackMeta,
        onSuccess: async (data) => {
            if (isRoutingDecision(data)) {
                setDecision(data);
                return;
            }
            await Promise.all(['tasks', 'workload', 'gantt', 'projects', 'projectSummary', 'saved-view-dashboard-cards']
                .map(key => queryClient.invalidateQueries({ queryKey: [key] })));
            choose(null);
            onClearSelection();
        },
        onError: error => { setDecision(null); setFailures(error instanceof BulkRejected ? error.failures : []); },
    });

    const optionsError = [teamQuery, iterationsQuery, iterationQuery, projectsQuery, milestonesQuery].find(query => query.isError);
    const ready = kind === 'iteration' ? Boolean(value) : request() !== null;
    const actionLabel = (key: BulkKind) => t(`surfaces.taskBulk.kinds.${key}`);

    const input = (() => {
        switch (kind) {
            case 'assign':
                return (
                    <Select data-page-chrome-control="select" aria-label={t('surfaces.taskBulk.chooseAssignee')} value={value} onChange={event => setValue(event.target.value)} className={selectClassName}>
                        <option value="">{t('surfaces.taskBulk.chooseAssignee')}</option>
                        <option value={NONE}>{t('common.unassigned')}</option>
                        <option value={AUTO}>{t('surfaces.taskBulk.actions.autoAssign')}</option>
                        {(teamQuery.data ?? []).map(member => <option key={member.id} value={member.id}>{member.name}</option>)}
                    </Select>
                );
            case 'status':
                return (
                    <>
                        <Select data-page-chrome-control="select" aria-label={t('surfaces.taskBulk.statusLabel')} value={value} onChange={event => setValue(event.target.value)} className={selectClassName}>
                            <option value="">{t('surfaces.taskBulk.chooseStatus')}</option>
                            {STATUS_OPTIONS.map(status => <option key={status} value={status}>{t(`statuses.${status}`, { defaultValue: status })}</option>)}
                        </Select>
                        <input aria-label={t('surfaces.taskBulk.reasonLabel')} value={reason} onChange={event => setReason(event.target.value)} placeholder={t('surfaces.taskBulk.reasonOptional')} className={selectClassName} />
                    </>
                );
            case 'priority':
                return <input aria-label={t('surfaces.taskBulk.priorityLabel')} type="number" min="1" max="10" value={value} onChange={event => setValue(event.target.value)} className={`${selectClassName} w-20`} />;
            case 'iteration':
                return (
                    <Select data-page-chrome-control="select" aria-label={t('surfaces.taskBulk.chooseIteration')} value={value} onChange={event => setValue(event.target.value)} className={selectClassName}>
                        <option value="">{t('surfaces.taskBulk.chooseIteration')}</option>
                        {(iterationsQuery.data ?? []).filter(iteration => iteration.id !== iterationId).map(iteration => <option key={iteration.id} value={iteration.id}>{iteration.name}</option>)}
                    </Select>
                );
            case 'project':
            case 'milestone':
                return (
                    <>
                        {scopedProjectId === null && (
                            <Select data-page-chrome-control="select" aria-label={t('surfaces.taskBulk.projectLabel')} value={value} onChange={event => { setValue(event.target.value); setMilestoneId(''); }} className={selectClassName}>
                                <option value="">{t('surfaces.taskBulk.chooseProject')}</option>
                                {(projectsQuery.data ?? []).map(project => <option key={project.id} value={project.id}>{project.name}</option>)}
                            </Select>
                        )}
                        {scopedProjectId !== null && <span className="text-sm text-content-primary">{iterationQuery.data?.project?.name}</span>}
                        <Select data-page-chrome-control="select" aria-label={t('surfaces.taskBulk.milestoneLabel')} value={milestoneId} onChange={event => setMilestoneId(event.target.value)} disabled={projectId === null} className={selectClassName}>
                            <option value="">{kind === 'project' ? t('surfaces.taskBulk.leaveMilestoneUnchangedUnlessIncompatible') : t('surfaces.taskBulk.chooseMilestone')}</option>
                            {(milestonesQuery.data ?? []).map(milestone => <option key={milestone.id} value={milestone.id}>{milestone.name}</option>)}
                        </Select>
                    </>
                );
            case 'addLabels':
            case 'removeLabels':
                return <input aria-label={t('surfaces.taskBulk.labelsLabel')} value={value} onChange={event => setValue(event.target.value)} placeholder={t('surfaces.taskBulk.labelsCommaSeparated')} className={`${selectClassName} w-64`} />;
            case 'flags':
                return (
                    <>
                        <Select data-page-chrome-control="select" aria-label={t('surfaces.taskBulk.optionalLabel')} value={isOptional} onChange={event => setIsOptional(event.target.value)} className={selectClassName}>
                            <option value="">{t('surfaces.taskBulk.optionalUnchanged')}</option>
                            <option value="true">{t('surfaces.taskBulk.setOptional')}</option>
                            <option value="false">{t('surfaces.taskBulk.clearOptional')}</option>
                        </Select>
                        <Select data-page-chrome-control="select" aria-label={t('surfaces.taskBulk.deferredLabel')} value={isDeferred} onChange={event => setIsDeferred(event.target.value)} className={selectClassName}>
                            <option value="">{t('surfaces.taskBulk.deferredUnchanged')}</option>
                            <option value="true">{t('surfaces.taskBulk.setDeferred')}</option>
                            <option value="false">{t('surfaces.taskBulk.clearDeferred')}</option>
                        </Select>
                    </>
                );
            case 'clearProject':
            case 'clearMilestone':
                return <span className="text-sm text-content-primary">{t(kind === 'clearProject' ? 'surfaces.taskBulk.clearProjectHelp' : 'surfaces.taskBulk.clearMilestoneHelp', { count: selectedCount })}</span>;
            case 'delete':
                return (
                    <span className="flex items-center gap-1 text-xs text-feedback-danger-foreground">
                        <Trash2 aria-hidden="true" className="h-3 w-3" />
                        {t('surfaces.taskBulk.deleteRemovesSelectedTasksAndTheirSubtasks')}
                    </span>
                );
            default:
                return null;
        }
    })();

    return (
        <div data-testid="task-bulk-operations" role="region" aria-label={t('taskList.bulkEdit')}
            className="sticky top-0 z-20 space-y-2 rounded-lg border border-action bg-action-muted px-3 py-2">
            <div className="flex flex-wrap items-center gap-2">
                <div className="mr-2 text-sm font-semibold text-content-primary" aria-live="polite">{t('taskList.selectedTasks', { count: selectedCount })}</div>
                {(['assign', 'status', 'priority', 'iteration'] as const).map(key => (
                    <Button key={key} size="sm" variant="secondary" aria-pressed={kind === key} onClick={() => choose(kind === key ? null : key)}>{actionLabel(key)}</Button>
                ))}
                {onMerge && selectedCount >= 2 && <Button size="sm" variant="secondary" onClick={onMerge}>{t('taskList.mergeSelected', { count: selectedCount })}</Button>}
                <OverflowMenu
                    label={t('surfaces.taskBulk.moreChanges')}
                    alwaysMenu
                    items={(['project', 'clearProject', 'milestone', 'clearMilestone', 'addLabels', 'removeLabels', 'flags', 'delete'] as const)
                        // A project-scoped iteration keeps its project, so clearing it is not offered.
                        .filter(key => key !== 'clearProject' || scopedProjectId === null)
                        .map(key => ({
                        label: actionLabel(key), onSelect: () => choose(key), tone: key === 'delete' ? 'danger' as const : undefined,
                    }))}
                />
                <span className="flex-1" />
                {selectedCount < matchingCount && (
                    <Button size="sm" variant="ghost" onClick={onSelectAll}>{t('taskList.selectAllMatching', { count: matchingCount })}</Button>
                )}
                <Button size="sm" variant="ghost" onClick={() => { choose(null); onClearSelection(); }}>{t('surfaces.taskBulk.clearSelection')}</Button>
            </div>

            {kind && (
                <div ref={editorRef} className="flex flex-wrap items-center gap-2">
                    {input}
                    <Button size="sm" variant={kind === 'delete' ? 'danger' : 'primary'} disabled={!ready || mutation.isPending} isLoading={mutation.isPending} onClick={() => { setDecision(null); mutation.mutate(undefined); }}>
                        {t('surfaces.taskBulk.apply')}
                    </Button>
                    <Button size="sm" variant="ghost" disabled={mutation.isPending} onClick={() => choose(null)}>{t('actions.cancel')}</Button>
                </div>
            )}

            {/* Mounted before it has text, so the stop is announced. */}
            <p role="status" className="sr-only">{currentDecision ? `${t('taskReassign.bulkTitle', { count: currentDecision.items.length })}. ${t('taskReassign.bulkHelp')}` : ''}</p>
            {currentDecision && (
                <div role="region" aria-label={t('taskReassign.bulkTitle', { count: currentDecision.items.length })}
                    className="space-y-2 rounded-md border border-feedback-warning-border bg-feedback-warning-muted px-3 py-2 text-feedback-warning-foreground">
                    <p className="text-sm font-semibold">{t('taskReassign.bulkTitle', { count: currentDecision.items.length })}</p>
                    <RoutingResultsList items={currentDecision.items} titleOf={taskId => titles.get(taskId) ?? t('surfaces.taskBulk.taskNumber', { id: taskId })} />
                    <p className="text-sm">{t('taskReassign.bulkHelp')}</p>
                    {currentDecision.items.some(item => !item.after) && <p className="text-sm font-medium">{t('taskReassign.bulkNoSuggestion')}</p>}
                    <div className="flex flex-wrap items-center gap-2">
                        <Button size="sm" disabled={mutation.isPending || currentDecision.items.some(item => !item.after)} isLoading={mutation.isPending} onClick={() => mutation.mutate('apply_suggestion')}>{t('taskReassign.bulkApplySuggestions')}</Button>
                        {currentDecision.canKeep && (
                            <Button size="sm" variant="secondary" disabled={mutation.isPending} onClick={() => mutation.mutate('keep')}>{t('taskReassign.bulkKeepReviewers')}</Button>
                        )}
                        <Button size="sm" variant="ghost" disabled={mutation.isPending} onClick={() => setDecision(null)}>{t('taskReassign.bulkBack')}</Button>
                    </div>
                </div>
            )}
            {optionsError && <QueryErrorState error={optionsError.error} fallback={t('queryFeedback.optionLoadFailed')} onRetry={() => void optionsError.refetch()} />}
            {mutation.isError && !(mutation.error instanceof BulkRejected) && (
                <div role="alert" className="rounded-md border border-feedback-danger-border bg-feedback-danger-muted px-3 py-2 text-sm text-feedback-danger-foreground">
                    {getApiErrorMessage(mutation.error, t('surfaces.taskBulk.failedToRun'))}
                </div>
            )}
            {failures.length > 0 && (
                <div role="alert" className="rounded-md border border-feedback-danger-border bg-feedback-danger-muted px-3 py-2 text-sm text-feedback-danger-foreground">
                    <p>{t('surfaces.taskBulk.rejected', { count: failures.length })}</p>
                    <ul className="mt-1 list-disc pl-5 text-xs">
                        {failures.slice(0, 5).map(failure => <li key={failure.taskId}>{titles.get(failure.taskId) ?? t('surfaces.taskBulk.taskNumber', { id: failure.taskId })}: {failure.message}</li>)}
                    </ul>
                </div>
            )}
        </div>
    );
};

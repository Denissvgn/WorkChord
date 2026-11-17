import { useMutation, useQuery } from '@tanstack/react-query';
import {
    Send,
    Sparkles
} from 'lucide-react';
import type { FormEvent } from 'react';
import { useMemo, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { templateDisplay } from '../../i18n/seedDisplay';
import { teamService } from '../../services/teamService';
import { templateService } from '../../services/templateService';
import { triageService } from '../../services/triageService';
import type { Iteration } from '../../types/iteration';
import type { Project } from '../../types/project';
import type { TeamMember } from '../../types/team';
import type {
    TriageConvertToTaskRequest,
    TriageItem,
    TriageTaskDraftResponse
} from '../../types/triage';
import { getApiErrorMessage } from '../../utils/apiError';
import { Button } from '../common/Button';
import { CollapsibleSection } from '../common/CollapsibleSection';
import { Input, RequiredIndicator } from '../common/Input';
import { Select } from '../common/Select';
import { QueryErrorState } from '../feedback/QueryState';
import { LabelSelector } from '../labels/LabelSelector';
import { TaskBriefEditor } from '../tasks/TaskBriefEditor';
import { TaskDependencySelector } from '../tasks/TaskDependencySelector';
import { emptyTaskBrief, newCriterion } from '../tasks/taskEditorContract';
import { AssigneeRecommendationsPanel } from '../team/AssigneeRecommendationsPanel';

import { TaskCreateSections } from '../tasks/TaskCreateSections';
import { SlideOverDrawer } from '../ui/SlideOverDrawer';
import { TriageConvertSource } from './TriageConvertSource';
import { TriageDraftPreview } from './TriageDraftPreview';
import { formatDraftDescription, makeLookup, optionalText, parseOptionalNumber } from './triageUtils';
interface ConvertTriageDrawerProps {
    item: TriageItem;
    projects: Project[];
    iterations: Iteration[];
    selectedIterationId: number;
    isSubmitting: boolean;
    error?: string | null;
    onSubmit: (payload: TriageConvertToTaskRequest) => void;
    onClose: () => void;
}

export const ConvertTriageDrawer = ({
    item,
    projects,
    iterations,
    selectedIterationId,
    isSubmitting,
    error,
    onSubmit,
    onClose,
}: ConvertTriageDrawerProps) => {
    const { t } = useTranslation();
    const defaultIterationId = useMemo(() => {
        const hintExists = item.iteration_hint_id
            ? iterations.some(iteration => iteration.id === item.iteration_hint_id)
            : false;
        const selectedExists = iterations.some(iteration => iteration.id === selectedIterationId);
        return (hintExists ? item.iteration_hint_id : null) || (selectedExists ? selectedIterationId : iterations[0]?.id) || 0;
    }, [item.iteration_hint_id, iterations, selectedIterationId]);

    const [iterationId, setIterationId] = useState(String(defaultIterationId || ''));
    const [destination, setDestination] = useState<'iteration' | 'project_backlog'>(defaultIterationId ? 'iteration' : 'project_backlog');
    const [projectId, setProjectId] = useState(item.project_hint_id ? String(item.project_hint_id) : '');
    const [assigneeId, setAssigneeId] = useState('');
    const [priority, setPriority] = useState(String(item.priority_hint || 5));
    const [tags, setTags] = useState<string[]>(item.labels);
    const [effortHours, setEffortHours] = useState('');
    const [dependsOn, setDependsOn] = useState<number[]>([]);
    const [title, setTitle] = useState(item.title);
    const [brief, setBrief] = useState(item.brief ?? { ...emptyTaskBrief(), goal: item.title, context: item.description || '' });
    const description = brief.context;
    const setDescription = (value: string | ((previous: string) => string)) => setBrief(previous => ({ ...previous, context: typeof value === 'function' ? value(previous.context) : value }));
    const [selectedTaskTemplateId, setSelectedTaskTemplateId] = useState('');
    const [draftPreview, setDraftPreview] = useState<TriageTaskDraftResponse | null>(null);

    const projectsById = useMemo(() => makeLookup(projects), [projects]);
    const iterationsById = useMemo(() => makeLookup(iterations), [iterations]);

    const parsedIterationId = Number(iterationId);
    const selectedIteration = destination === "iteration" ? iterations.find(iteration => iteration.id === parsedIterationId) : undefined;
    const dayHours = selectedIteration?.nominal_day_hours ?? 8;
    const hasSelectedIteration = Boolean(selectedIteration);
    // feedback-policy: query loading,error,retry,empty - optional members default to Unassigned; errors offer retry.
    const { data: teamMembers = [], error: teamError, refetch: refetchTeam } = useQuery<TeamMember[]>({
        queryKey: ['team', parsedIterationId],
        queryFn: () => teamService.getByIteration(parsedIterationId),
        enabled: hasSelectedIteration,
    });
    // feedback-policy: query loading,error,retry,empty - manual entry remains available without templates; errors offer retry.
    const { data: taskTemplates = [], error: templatesError, refetch: refetchTemplates } = useQuery({
        queryKey: ['templates', 'task'],
        queryFn: () => templateService.getAll({ template_type: 'task' }),
    });

    // feedback-policy: mutation pending,inline - the draft button is busy and failures stay beside the preview.
    const draftMutation = useMutation({
        mutationFn: () => triageService.draftTask(item.id, {
            template_id: parseOptionalNumber(selectedTaskTemplateId),
            current_title: optionalText(title),
            current_description: optionalText(description),
        }),
        onSuccess: draft => setDraftPreview(draft),
    });
    const draftErrorMessage = draftMutation.error
        ? getApiErrorMessage(draftMutation.error, t('surfaces.triagePage.draftFailed'))
        : null;
    const scopedProjectId = selectedIteration?.project_id ?? null;
    const scopedProject = selectedIteration?.project ?? null;
    const effectiveProjectId = scopedProjectId ?? parseOptionalNumber(projectId);

    const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        if (destination === "iteration" ? !hasSelectedIteration : !effectiveProjectId) return;
        onSubmit({
            iteration_id: destination === "iteration" ? parsedIterationId : null,
            destination,
            brief,
            title: title.trim(),

            project_id: effectiveProjectId,
            assignee_id: hasSelectedIteration ? parseOptionalNumber(assigneeId) : null,
            priority: Number(priority),
            tags,
            effort_days: null,
            effort_hours: effortHours === "" ? null : Number(effortHours),
            depends_on: dependsOn,
        });
    };

    const applyDraft = () => {
        if (!draftPreview) return;
        setTitle(draftPreview.suggested_title);
        setBrief(draftPreview.brief ?? { ...emptyTaskBrief(), goal: draftPreview.suggested_title, context: formatDraftDescription(draftPreview), acceptance_criteria: draftPreview.acceptance_criteria.map(text => newCriterion(text)) });
    };

    return <SlideOverDrawer open title={t('surfaces.triagePage.convertToTask')} onClose={onClose} className="max-w-2xl">
        <form onSubmit={handleSubmit} className="space-y-6 p-6">
            {(teamError || templatesError) && <QueryErrorState error={teamError ?? templatesError} fallback={t('queryFeedback.optionLoadFailed')}
                onRetry={() => { void refetchTeam(); void refetchTemplates(); }} />}
            {error && <p role="alert" className="text-sm text-feedback-danger-foreground">{error}</p>}
            <CollapsibleSection title={t('surfaces.triagePage.rawIntake')}>
                <TriageConvertSource item={item} projectsById={projectsById} iterationsById={iterationsById} />
            </CollapsibleSection>
            <TaskCreateSections
                title={<Input label={t('surfaces.taskForm.taskTitle')} value={title} onChange={event => setTitle(event.target.value)} required maxLength={255} />}
                assignee={<Select label={t('surfaces.taskForm.assignee')} value={assigneeId} onChange={event => setAssigneeId(event.target.value)} disabled={!hasSelectedIteration}><option value="">{t('surfaces.triagePage.unassigned')}</option>{teamMembers.map(member => (
                    <option key={member.id} value={member.id}>
                        {member.name}
                    </option>
                ))}</Select>

                }
                effort={<div>
                    <Input
                        label={t('surfaces.taskForm.effortHours')}
                        type="number"
                        min="0.5"
                        step="0.5"
                        value={effortHours}
                        onChange={event => setEffortHours(event.target.value)}
                    />
                    <p className="mt-1 text-xs text-content-secondary">{t('surfaces.taskForm.effortDaysHint', { days: effortHours === '' ? 'n' : (Number(effortHours) / dayHours).toLocaleString(undefined, { maximumFractionDigits: 1 }), hours: dayHours })}</p>
                </div>

                }
                brief={<TaskBriefEditor part="essential" value={brief} onChange={setBrief} disabled={isSubmitting} actions={
                    <Button type="button" size="sm" variant="ghost" onClick={() => draftMutation.mutate()} isLoading={draftMutation.isPending}>
                        <Sparkles className="mr-1 h-4 w-4" aria-hidden="true" />{t('surfaces.triagePage.draftTaskDetails')}
                    </Button>
                } />}
                assistance={<TriageDraftPreview draftPreview={draftPreview} applyDraft={applyDraft} setBrief={setBrief}
                    description={description} setDescription={setDescription} title={title} setTitle={setTitle} draftErrorMessage={draftErrorMessage} />}
                more={<>
                    <div>
                        <Select label={t('domain.destination')} value={destination} onChange={event => { setDestination(event.target.value as 'iteration' | 'project_backlog'); setAssigneeId(''); setDependsOn([]); }}>
                            <option value="iteration">{t('domain.scheduledDestination')}</option>
                            <option value="project_backlog">{t('domain.backlog')}</option>
                        </Select>
                    </div>
                    {/* Quick Assignment Row */}
                    <div className="grid grid-cols-2 gap-4 p-4 rounded-lg border border-border bg-surface-muted/50">
                        <Select label={<>{t('surfaces.triagePage.iteration')}{destination === "iteration" && <RequiredIndicator />}</>} disabled={destination === "project_backlog"} value={iterationId} onChange={event => {
                            const nextIterationId = event.target.value;
                            const nextIteration = iterations.find(iteration => String(iteration.id) === nextIterationId);
                            setIterationId(nextIterationId);
                            if (nextIteration?.project_id != null) {
                                setProjectId(String(nextIteration.project_id));
                            } else {
                                setProjectId(item.project_hint_id ? String(item.project_hint_id) : '');
                            }
                            setAssigneeId('');
                            setDependsOn([]);
                        }} required={destination === "iteration"}><option value="">{t('surfaces.triagePage.select')}</option>{iterations.map(iteration => (
                            <option key={iteration.id} value={iteration.id}>{iteration.name}</option>
                        ))}</Select>

                        <div>
                            <label className="mb-1 block text-sm font-medium text-content-primary">{t('surfaces.taskForm.project')}</label>
                            {scopedProjectId !== null ? (
                                <div className="w-full rounded-md border border-border-strong bg-surface-subtle px-3 py-2 text-content-primary shadow-sm text-sm">
                                    {scopedProject?.name ?? `Project #${scopedProjectId}`}
                                </div>
                            ) : (
                                <Select
                                    aria-label={t('surfaces.taskForm.project')}
                                    value={projectId}
                                    onChange={event => setProjectId(event.target.value)}
                                    className="w-full rounded-md border border-border-strong bg-surface-card px-3 py-2 shadow-sm focus:outline-none focus:ring-1 focus:ring-focus text-sm"
                                >
                                    <option value="">{t('surfaces.triagePage.noProject')}</option>
                                    {projects.map(project => (
                                        <option key={project.id} value={project.id}>{project.name}</option>
                                    ))}
                                </Select>
                            )}
                        </div>

                        <Input
                            label={t('surfaces.taskForm.priority')}
                            type="number"
                            min="1"
                            max="10"
                            value={priority}
                            onChange={event => setPriority(event.target.value)}
                        />
                    </div>

                    <LabelSelector
                        label={t('surfaces.taskForm.tags')}
                        value={tags}
                        onChange={setTags}
                        placeholder={t('surfaces.taskForm.newTag')}
                    />

                    <Select label={t('surfaces.taskForm.template')} value={selectedTaskTemplateId} onChange={event => setSelectedTaskTemplateId(event.target.value)}><option value="">{t('surfaces.triagePage.noTemplate')}</option>{taskTemplates.map(template => (
                        <option key={template.id} value={template.id}>
                            {templateDisplay(template).name}
                        </option>
                    ))}</Select>

                    {hasSelectedIteration && (
                        <div>
                            <label className="mb-1 block text-sm font-medium text-content-primary">{t('surfaces.taskForm.dependencies')}</label>
                            <div className="max-h-32 overflow-y-auto rounded-md border border-border p-2 bg-surface-card">
                                <TaskDependencySelector
                                    iterationId={parsedIterationId}
                                    selectedIds={dependsOn}
                                    onChange={setDependsOn}
                                />
                            </div>
                        </div>
                    )}

                    <AssigneeRecommendationsPanel targetType="triage" triageItemId={item.id}
                        iterationId={hasSelectedIteration ? parsedIterationId : null} selectedAssigneeId={parseOptionalNumber(assigneeId)}
                        onSelectAssignee={id => setAssigneeId(String(id))} />
                    <TaskBriefEditor part="details" value={brief} onChange={setBrief} disabled={isSubmitting} />
                </>}
            />
            <div className="flex justify-end gap-3 border-t border-border pt-4">
                <Button type="button" variant="ghost" onClick={onClose}>{t('surfaces.triagePage.cancel')}</Button>
                <Button type="submit" isLoading={isSubmitting} disabled={(destination === 'iteration' ? !hasSelectedIteration : !effectiveProjectId) || !title.trim()}>
                    <Send className="mr-2 h-4 w-4" aria-hidden="true" />{t('surfaces.triagePage.convert')}
                </Button>
            </div>
        </form>
    </SlideOverDrawer>;
};

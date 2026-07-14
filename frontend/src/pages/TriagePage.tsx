import i18n from '../i18n/i18n';
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import type { FormEvent, MouseEvent, ReactNode } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { Link, useSearchParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import {
    AlertCircle,
    CheckCircle2,
    Clock3,
    CopyCheck,
    ExternalLink,
    Inbox,
    ListFilter,
    Loader2,
    MessageSquare,
    Plus,
    Search,
    Send,
    Sparkles,
    X,
    XCircle,
} from 'lucide-react';
import clsx from 'clsx';
import { Button } from '../components/common/Button';
import { Modal } from '../components/common/Modal';
import { Input } from '../components/common/Input';
import { CollapsibleSection } from '../components/common/CollapsibleSection';
import { LabelSelector } from '../components/labels/LabelSelector';
import { RequestSourceLinksPanel } from '../components/requestSources/RequestSourceLinksPanel';
import { TaskDependencySelector } from '../components/tasks/TaskDependencySelector';
import { AssigneeRecommendationsPanel } from '../components/team/AssigneeRecommendationsPanel';
import { QueryErrorState } from '../components/feedback/QueryState';
import { iterationService } from '../services/iterationService';
import { projectService } from '../services/projectService';
import { taskService } from '../services/taskService';
import { templateService } from '../services/templateService';
import { teamService } from '../services/teamService';
import { triageService } from '../services/triageService';
import { savedViewService } from '../services/savedViewService';
import { useIterationStore } from '../store/iterationStore';
import { formatDateTime } from '../utils/formatDate';
import {
    appendChecklistToDescription,
    getPayloadString,
    mergeLabels,
} from '../utils/templateDefaults';
import { getApiErrorMessage } from '../utils/apiError';
import { safeExternalHref } from '../utils/safeUrl';
import type { Iteration } from '../types/iteration';
import type { Project } from '../types/project';
import type { SavedView } from '../types/savedView';
import type { Task } from '../types/task';
import type { WorkTemplate } from '../types/template';
import type { TeamMember } from '../types/team';
import { templateDisplay } from '../i18n/seedDisplay';
import { MetricGrid, PageHeader, PageLayout } from '../components/ui';
import type {
    TriageActionRequest,
    TriageConvertToTaskRequest,
    TriageConvertToTaskResponse,
    TriageDuplicateRequest,
    TriageDuplicateSuggestion,
    TriageDuplicateSuggestionsResponse,
    TriageItem,
    TriageItemCreate,
    TriageItemStatus,
    TriageListParams,
    TriageSnoozeRequest,
    TriageTaskDraftResponse,
} from '../types/triage';

const t = i18n.t.bind(i18n);

const statusOptions: TriageItemStatus[] = ['new', 'accepted', 'snoozed', 'declined', 'duplicate', 'converted'];

const statusLabelKeys: Record<TriageItemStatus, string> = {
    new: 'surfaces.triagePage.statuses.new',
    accepted: 'surfaces.triagePage.statuses.accepted',
    declined: 'surfaces.triagePage.statuses.declined',
    duplicate: 'surfaces.triagePage.statuses.duplicate',
    snoozed: 'surfaces.triagePage.statuses.snoozed',
    converted: 'surfaces.triagePage.statuses.converted',
};

const statusClassName = (status: TriageItemStatus) => {
    switch (status) {
        case 'accepted':
            return 'bg-feedback-success-muted text-feedback-success-foreground border-feedback-success-border';
        case 'declined':
            return 'bg-feedback-danger-muted text-feedback-danger-foreground border-feedback-danger-border';
        case 'duplicate':
            return 'bg-feedback-warning-muted text-feedback-warning-foreground border-feedback-warning-border';
        case 'snoozed':
            return 'bg-action-muted text-action border-action';
        case 'converted':
            return 'bg-feedback-purple-muted text-feedback-purple-foreground border-feedback-purple-border';
        default:
            return 'bg-surface-muted text-content-primary border-border';
    }
};

const triageFiltersFromSavedView = (view: SavedView) => {
    const raw = view.filters_json;
    const statuses = Array.isArray(raw.statuses)
        ? raw.statuses.filter((status): status is TriageItemStatus => (
            typeof status === 'string' && statusOptions.includes(status as TriageItemStatus)
        ))
        : [];

    return {
        active: typeof raw.active === 'boolean' ? raw.active : true,
        status: statuses[0] ?? '',
        q: typeof raw.q === 'string' ? raw.q : '',
        source: typeof raw.source === 'string' ? raw.source : '',
    };
};

const toLocalDateTimeInputValue = (date: Date) => {
    const timezoneOffsetMs = date.getTimezoneOffset() * 60000;
    return new Date(date.getTime() - timezoneOffsetMs).toISOString().slice(0, 16);
};

const optionalText = (value: string) => {
    const trimmed = value.trim();
    return trimmed ? trimmed : null;
};

const parseOptionalNumber = (value: string) => value ? Number(value) : null;

const formatSuggestionScore = (score: number) => score.toFixed(score >= 10 ? 1 : 2);

const formatDraftDescription = (draft: TriageTaskDraftResponse) => {
    const sections = [draft.suggested_description.trim()].filter(Boolean);

    if (draft.acceptance_criteria.length > 0) {
        sections.push(`Acceptance Criteria:\n${draft.acceptance_criteria.map(item => `- ${item}`).join('\n')}`);
    }
    if (draft.suggested_checklist.length > 0) {
        sections.push(`Checklist:\n${draft.suggested_checklist.map(item => `- ${item}`).join('\n')}`);
    }
    if (draft.risks.length > 0) {
        sections.push(`Risks:\n${draft.risks.map(item => `- ${item}`).join('\n')}`);
    }

    return sections.join('\n\n');
};

const isDueSnoozed = (item: TriageItem) => {
    if (item.status !== 'snoozed' || !item.snoozed_until) return false;
    return new Date(item.snoozed_until).getTime() <= Date.now();
};

const getErrorMessage = (error: unknown, fallback: string) => {
    const response = (error as { response?: { data?: { detail?: unknown } } })?.response;
    const detail = response?.data?.detail;

    if (typeof detail === 'string') return detail;
    if (Array.isArray(detail)) {
        const messages = detail
            .map(item => {
                if (typeof item === 'string') return item;
                if (item && typeof item === 'object' && 'msg' in item) {
                    return String((item as { msg: unknown }).msg);
                }
                return '';
            })
            .filter(Boolean);
        if (messages.length > 0) return messages.join(', ');
    }
    if (error instanceof Error && error.message) return error.message;
    return fallback;
};

interface TaskListOption {
    id: number;
    title: string;
    depth: number;
}

const flattenTasks = (tasks: Task[] = [], depth = 0): TaskListOption[] => {
    return tasks.flatMap(task => [
        { id: task.id, title: task.title, depth },
        ...flattenTasks(task.children ?? [], depth + 1),
    ]);
};

const makeLookup = <T extends { id: number; name: string }>(items: T[]) => {
    return items.reduce<Record<number, string>>((lookup, item) => {
        lookup[item.id] = item.name;
        return lookup;
    }, {});
};

const StatusPill = ({ status }: { status: TriageItemStatus }) => (
    <span className={clsx('inline-flex items-center rounded-full border px-2 py-0.5 text-xs font-medium', statusClassName(status))}>
        {t(statusLabelKeys[status])}
    </span>
);



interface ModalFrameProps {
    title: string;
    children: ReactNode;
    onClose: () => void;
    size?: 'md' | 'lg' | 'xl';
}

const ModalFrame = ({ title, children, onClose, size = 'md' }: ModalFrameProps) => (
    <Modal
        open
        title={title}
        closeLabel={t('surfaces.triagePage.close')}
        onClose={onClose}
        className={clsx(
            size === 'md' && 'max-w-lg',
            size === 'lg' && 'max-w-2xl',
            size === 'xl' && 'max-w-4xl',
        )}
    >
        {children}
    </Modal>
);

interface CreateTriageModalProps {
    projects: Project[];
    iterations: Iteration[];
    isSubmitting: boolean;
    error?: string | null;
    onSubmit: (payload: TriageItemCreate) => void;
    onClose: () => void;
}

const CreateTriageModal = ({ projects, iterations, isSubmitting, error, onSubmit, onClose }: CreateTriageModalProps) => {
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [source, setSource] = useState('');
    const [sourceUrl, setSourceUrl] = useState('');
    const [externalKey, setExternalKey] = useState('');
    const [priorityHint, setPriorityHint] = useState('');
    const [assigneeHint, setAssigneeHint] = useState('');
    const [projectHintId, setProjectHintId] = useState('');
    const [iterationHintId, setIterationHintId] = useState('');
    const [labels, setLabels] = useState<string[]>([]);
    const [selectedTemplateId, setSelectedTemplateId] = useState('');

    const { data: triageTemplates = [], error: templatesError, refetch: refetchTemplates } = useQuery({
        queryKey: ['templates', 'triage'],
        queryFn: () => templateService.getAll({ template_type: 'triage' }),
    });

    const applyTriageTemplate = (template: WorkTemplate) => {
        const display = templateDisplay(template);
        setTitle(display.default_title ?? title);
        setDescription(appendChecklistToDescription(
            display.default_description ?? description,
            display.default_checklist,
        ));
        setSource(getPayloadString(template.default_payload, 'source', source || null) ?? source);
        setPriorityHint(template.default_priority != null ? String(template.default_priority) : priorityHint);
        setLabels(mergeLabels(labels, template.default_labels));
    };

    const handleTemplateSelect = (templateId: string) => {
        setSelectedTemplateId(templateId);
        const template = triageTemplates.find(candidate => String(candidate.id) === templateId);
        if (template) {
            applyTriageTemplate(template);
        }
    };

    const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        onSubmit({
            title: title.trim(),
            description: optionalText(description),
            source: optionalText(source),
            source_url: optionalText(sourceUrl),
            external_key: optionalText(externalKey),
            priority_hint: parseOptionalNumber(priorityHint),
            assignee_hint: optionalText(assigneeHint),
            project_hint_id: parseOptionalNumber(projectHintId),
            iteration_hint_id: parseOptionalNumber(iterationHintId),
            labels,
        });
    };

    return (
        <ModalFrame title={t('surfaces.triagePage.newIntake')} onClose={onClose} size="lg">
            <form onSubmit={handleSubmit} className="space-y-4">
                {templatesError && (
                    <QueryErrorState
                        error={templatesError}
                        fallback={t('queryFeedback.optionLoadFailed')}
                        onRetry={() => void refetchTemplates()}
                    />
                )}
                {error && (
                    <div className="flex items-start gap-2 rounded-md bg-feedback-danger-muted p-3 text-sm text-feedback-danger-foreground">
                        <AlertCircle className="mt-0.5 h-4 w-4 flex-shrink-0" />
                        <span>{error}</span>
                    </div>
                )}

                {triageTemplates.length > 0 && (
                    <div>
                        <label className="mb-1 block text-sm font-medium text-content-primary">{t('surfaces.triagePage.template')}</label>
                        <select
                            value={selectedTemplateId}
                            onChange={event => handleTemplateSelect(event.target.value)}
                            className="w-full rounded-md border border-border-strong bg-surface-card px-3 py-2 shadow-sm focus:outline-none focus:ring-1 focus:ring-focus"
                        >
                            <option value="">{t('surfaces.triagePage.noTemplate')}</option>
                            {triageTemplates.map(template => (
                                <option key={template.id} value={template.id}>
                                    {templateDisplay(template).name}
                                </option>
                            ))}
                        </select>
                    </div>
                )}

                <Input
                    label={t('surfaces.triagePage.title')}
                    value={title}
                    onChange={event => setTitle(event.target.value)}
                    required
                    maxLength={255}
                />

                <div>
                    <label className="mb-1 block text-sm font-medium text-content-primary">{t('surfaces.triagePage.description')}</label>
                    <textarea
                        value={description}
                        onChange={event => setDescription(event.target.value)}
                        className="min-h-[110px] w-full rounded-md border border-border-strong px-3 py-2 shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus"
                    />
                </div>

                <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
                    <Input label={t('surfaces.triagePage.source')} value={source} onChange={event => setSource(event.target.value)} maxLength={100} />
                    <Input label={t('surfaces.triagePage.externalKey')} value={externalKey} onChange={event => setExternalKey(event.target.value)} maxLength={255} />
                    <Input label={t('surfaces.triagePage.priorityHint')} type="number" min="1" max="10" value={priorityHint} onChange={event => setPriorityHint(event.target.value)} />
                </div>

                <Input label={t('surfaces.triagePage.sourceURL')} type="url" value={sourceUrl} onChange={event => setSourceUrl(event.target.value)} maxLength={500} />

                <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
                    <Input label={t('surfaces.triagePage.assigneeHint')} value={assigneeHint} onChange={event => setAssigneeHint(event.target.value)} maxLength={255} />
                    <div>
                        <label className="mb-1 block text-sm font-medium text-content-primary">{t('surfaces.triagePage.projectHint')}</label>
                        <select
                            value={projectHintId}
                            onChange={event => setProjectHintId(event.target.value)}
                            className="w-full rounded-md border border-border-strong bg-surface-card px-3 py-2 shadow-sm focus:outline-none focus:ring-1 focus:ring-focus"
                        >
                            <option value="">{t('surfaces.triagePage.noProject')}</option>
                            {projects.map(project => (
                                <option key={project.id} value={project.id}>{project.name}</option>
                            ))}
                        </select>
                    </div>
                    <div>
                        <label className="mb-1 block text-sm font-medium text-content-primary">{t('surfaces.triagePage.iterationHint')}</label>
                        <select
                            value={iterationHintId}
                            onChange={event => setIterationHintId(event.target.value)}
                            className="w-full rounded-md border border-border-strong bg-surface-card px-3 py-2 shadow-sm focus:outline-none focus:ring-1 focus:ring-focus"
                        >
                            <option value="">{t('surfaces.triagePage.noIteration')}</option>
                            {iterations.map(iteration => (
                                <option key={iteration.id} value={iteration.id}>{iteration.name}</option>
                            ))}
                        </select>
                    </div>
                </div>

                <LabelSelector
                    label={t('surfaces.triagePage.labels')}
                    value={labels}
                    onChange={setLabels}
                    placeholder={t('surfaces.triagePage.addCustomLabel')}
                />

                <div className="flex justify-end gap-2 pt-2">
                    <Button type="button" variant="ghost" onClick={onClose}>{t('surfaces.triagePage.cancel')}</Button>
                    <Button type="submit" isLoading={isSubmitting} disabled={!title.trim()}>
                        <Plus className="mr-2 h-4 w-4" />
                        {t('surfaces.triagePage.create')}
                    </Button>
                </div>
            </form>
        </ModalFrame>
    );
};

type TriageLifecycleAction = 'accept' | 'decline' | 'snooze' | 'duplicate';

interface DuplicateActionDefaults {
    targetType: 'triage' | 'task';
    targetId: number;
    title: string;
    iterationId?: number | null;
}

interface TriageActionModalProps {
    action: TriageLifecycleAction;
    item: TriageItem;
    allTriageItems: TriageItem[];
    iterations: Iteration[];
    selectedIterationId: number;
    defaultSnooze: string;
    defaultDuplicate?: DuplicateActionDefaults;
    isSubmitting: boolean;
    error?: string | null;
    onSubmit: (payload: TriageActionRequest | TriageSnoozeRequest | TriageDuplicateRequest) => void;
    onClose: () => void;
}

const TriageActionModal = ({
    action,
    item,
    allTriageItems,
    iterations,
    selectedIterationId,
    defaultSnooze,
    defaultDuplicate,
    isSubmitting,
    error,
    onSubmit,
    onClose,
}: TriageActionModalProps) => {
    const fallbackIterationId = defaultDuplicate?.iterationId || item.iteration_hint_id || selectedIterationId || iterations[0]?.id || 0;
    const [reason, setReason] = useState('');
    const [snoozedUntil, setSnoozedUntil] = useState(defaultSnooze);
    const [duplicateTargetType, setDuplicateTargetType] = useState<'triage' | 'task'>(defaultDuplicate?.targetType ?? 'triage');
    const [duplicateItemId, setDuplicateItemId] = useState(
        defaultDuplicate?.targetType === 'triage' ? String(defaultDuplicate.targetId) : ''
    );
    const [duplicateIterationId, setDuplicateIterationId] = useState(String(fallbackIterationId || ''));
    const [duplicateTaskId, setDuplicateTaskId] = useState(
        defaultDuplicate?.targetType === 'task' ? String(defaultDuplicate.targetId) : ''
    );
    const [linkRequestToDuplicateTask, setLinkRequestToDuplicateTask] = useState(
        defaultDuplicate?.targetType === 'task'
    );

    const parsedDuplicateIterationId = Number(duplicateIterationId);
    const { data: duplicateTasks = [], error: duplicateTasksError, refetch: refetchDuplicateTasks } = useQuery({
        queryKey: ['tasks', parsedDuplicateIterationId],
        queryFn: () => taskService.getByIteration(parsedDuplicateIterationId),
        enabled: action === 'duplicate' && duplicateTargetType === 'task' && parsedDuplicateIterationId > 0,
    });

    const flatDuplicateTasks = useMemo(() => flattenTasks(duplicateTasks), [duplicateTasks]);
    const otherTriageItems = useMemo(
        () => allTriageItems.filter(candidate => candidate.id !== item.id),
        [allTriageItems, item.id]
    );
    const triageDuplicateOptions = useMemo(() => {
        const options = otherTriageItems.map(candidate => ({
            id: candidate.id,
            title: candidate.title,
        }));
        if (
            defaultDuplicate?.targetType === 'triage'
            && !options.some(option => option.id === defaultDuplicate.targetId)
        ) {
            options.unshift({ id: defaultDuplicate.targetId, title: defaultDuplicate.title });
        }
        return options;
    }, [defaultDuplicate, otherTriageItems]);
    const taskDuplicateOptions = useMemo(() => {
        const options = flatDuplicateTasks.map(task => ({
            id: task.id,
            title: task.title,
            depth: task.depth,
        }));
        if (
            defaultDuplicate?.targetType === 'task'
            && !options.some(option => option.id === defaultDuplicate.targetId)
        ) {
            options.unshift({ id: defaultDuplicate.targetId, title: defaultDuplicate.title, depth: 0 });
        }
        return options;
    }, [defaultDuplicate, flatDuplicateTasks]);

    const modalTitle = t({
        accept: 'surfaces.triagePage.acceptIntake',
        decline: 'surfaces.triagePage.declineIntake',
        snooze: 'surfaces.triagePage.snoozeIntake',
        duplicate: 'surfaces.triagePage.markDuplicate',
    }[action]);

    const submitLabel = t({
        accept: 'surfaces.triagePage.accept',
        decline: 'surfaces.triagePage.decline',
        snooze: 'surfaces.triagePage.snooze',
        duplicate: 'surfaces.triagePage.markDuplicate',
    }[action]);

    const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        const trimmedReason = optionalText(reason);

        if (action === 'snooze') {
            onSubmit({
                snoozed_until: new Date(snoozedUntil).toISOString(),
                reason: trimmedReason,
            });
            return;
        }

        if (action === 'duplicate') {
            if (duplicateTargetType === 'triage') {
                onSubmit({
                    duplicate_of_id: Number(duplicateItemId),
                    duplicate_task_id: null,
                    reason: trimmedReason,
                });
                return;
            }
            onSubmit({
                duplicate_of_id: null,
                duplicate_task_id: Number(duplicateTaskId),
                link_request_to_duplicate_task: linkRequestToDuplicateTask,
                reason: trimmedReason,
            });
            return;
        }

        onSubmit({ reason: trimmedReason });
    };

    const duplicateSubmitDisabled = action === 'duplicate'
        && ((duplicateTargetType === 'triage' && !duplicateItemId) || (duplicateTargetType === 'task' && !duplicateTaskId));

    return (
        <ModalFrame title={modalTitle} onClose={onClose} size="lg">
            <form onSubmit={handleSubmit} className="space-y-4">
                {duplicateTasksError && (
                    <QueryErrorState
                        error={duplicateTasksError}
                        fallback={t('queryFeedback.optionLoadFailed')}
                        onRetry={() => void refetchDuplicateTasks()}
                    />
                )}
                {error && (
                    <div className="flex items-start gap-2 rounded-md bg-feedback-danger-muted p-3 text-sm text-feedback-danger-foreground">
                        <AlertCircle className="mt-0.5 h-4 w-4 flex-shrink-0" />
                        <span>{error}</span>
                    </div>
                )}

                <div className="rounded-md border border-border bg-surface-muted p-3">
                    <div className="flex items-center justify-between gap-3">
                        <p className="truncate font-medium text-content-primary">{item.title}</p>
                        <StatusPill status={item.status} />
                    </div>
                    {item.source && <p className="mt-1 text-xs text-content-secondary">{item.source}{item.external_key ? ` / ${item.external_key}` : ''}</p>}
                </div>

                {action === 'snooze' && (
                    <Input
                        label={t('surfaces.triagePage.snoozedUntil')}
                        type="datetime-local"
                        value={snoozedUntil}
                        onChange={event => setSnoozedUntil(event.target.value)}
                        required
                    />
                )}

                {action === 'duplicate' && (
                    <div className="space-y-3">
                        <div className="flex rounded-md border border-border bg-surface-muted p-1">
                            <button
                                type="button"
                                onClick={() => {
                                    setDuplicateTargetType('triage');
                                    setLinkRequestToDuplicateTask(false);
                                }}
                                className={clsx(
                                    'flex-1 rounded px-3 py-2 text-sm font-medium',
                                    duplicateTargetType === 'triage' ? 'bg-surface-card text-content-primary shadow-sm' : 'text-content-secondary hover:text-content-primary'
                                )}
                            >
                                {t('surfaces.triagePage.triageItem')}
                            </button>
                            <button
                                type="button"
                                onClick={() => {
                                    setDuplicateTargetType('task');
                                    setLinkRequestToDuplicateTask(true);
                                }}
                                className={clsx(
                                    'flex-1 rounded px-3 py-2 text-sm font-medium',
                                    duplicateTargetType === 'task' ? 'bg-surface-card text-content-primary shadow-sm' : 'text-content-secondary hover:text-content-primary'
                                )}
                            >
                                {t('surfaces.triagePage.task')}
                            </button>
                        </div>

                        {duplicateTargetType === 'triage' ? (
                            <div>
                                <label className="mb-1 block text-sm font-medium text-content-primary">{t('surfaces.triagePage.duplicateOf')}</label>
                                <select
                                    value={duplicateItemId}
                                    onChange={event => setDuplicateItemId(event.target.value)}
                                    className="w-full rounded-md border border-border-strong bg-surface-card px-3 py-2 shadow-sm focus:outline-none focus:ring-1 focus:ring-focus"
                                    required
                                >
                                    <option value="">{t('surfaces.triagePage.selectIntakeItem')}</option>
                                    {triageDuplicateOptions.map(candidate => (
                                        <option key={candidate.id} value={candidate.id}>
                                            #{candidate.id} {candidate.title}
                                        </option>
                                    ))}
                                </select>
                            </div>
                        ) : (
                            <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
                                <div>
                                    <label className="mb-1 block text-sm font-medium text-content-primary">{t('surfaces.triagePage.taskIteration')}</label>
                                    <select
                                        value={duplicateIterationId}
                                        onChange={event => {
                                            setDuplicateIterationId(event.target.value);
                                            setDuplicateTaskId('');
                                        }}
                                        className="w-full rounded-md border border-border-strong bg-surface-card px-3 py-2 shadow-sm focus:outline-none focus:ring-1 focus:ring-focus"
                                        required
                                    >
                                        <option value="">{t('surfaces.triagePage.selectIteration')}</option>
                                        {iterations.map(iteration => (
                                            <option key={iteration.id} value={iteration.id}>{iteration.name}</option>
                                        ))}
                                    </select>
                                </div>
                                <div>
                                    <label className="mb-1 block text-sm font-medium text-content-primary">{t('surfaces.triagePage.task')}</label>
                                    <select
                                        value={duplicateTaskId}
                                        onChange={event => setDuplicateTaskId(event.target.value)}
                                        className="w-full rounded-md border border-border-strong bg-surface-card px-3 py-2 shadow-sm focus:outline-none focus:ring-1 focus:ring-focus"
                                        required
                                        disabled={!parsedDuplicateIterationId}
                                    >
                                        <option value="">{t('surfaces.triagePage.selectTask')}</option>
                                        {taskDuplicateOptions.map(task => (
                                            <option key={task.id} value={task.id}>
                                                {'-'.repeat(task.depth)} {task.title}
                                            </option>
                                        ))}
                                    </select>
                                </div>
                                <label className="flex items-start gap-2 rounded-md border border-action bg-action-muted p-3 text-sm text-action md:col-span-2">
                                    <input
                                        type="checkbox"
                                        checked={linkRequestToDuplicateTask}
                                        onChange={event => setLinkRequestToDuplicateTask(event.target.checked)}
                                        className="mt-0.5 rounded border-action text-action focus:ring-focus"
                                    />
                                    <span>{t('surfaces.triagePage.linkThisIntakeAsARequestOnTheDuplicateTask')}</span>
                                </label>
                            </div>
                        )}
                    </div>
                )}

                <div>
                    <label className="mb-1 block text-sm font-medium text-content-primary">{t('surfaces.triagePage.reason')}</label>
                    <textarea
                        value={reason}
                        onChange={event => setReason(event.target.value)}
                        className="min-h-[90px] w-full rounded-md border border-border-strong px-3 py-2 shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus"
                    />
                </div>

                <div className="flex justify-end gap-2 pt-2">
                    <Button type="button" variant="ghost" onClick={onClose}>{t('surfaces.triagePage.cancel')}</Button>
                    <Button type="submit" isLoading={isSubmitting} disabled={duplicateSubmitDisabled}>
                        {submitLabel}
                    </Button>
                </div>
            </form>
        </ModalFrame>
    );
};

interface ConvertTriageModalProps {
    item: TriageItem;
    projects: Project[];
    iterations: Iteration[];
    selectedIterationId: number;
    isSubmitting: boolean;
    error?: string | null;
    onSubmit: (payload: TriageConvertToTaskRequest) => void;
    onClose: () => void;
}

const ConvertTriageSplitView = ({
    item,
    projects,
    iterations,
    selectedIterationId,
    isSubmitting,
    error,
    onSubmit,
    onClose,
}: ConvertTriageModalProps) => {
    const { t } = useTranslation();
    const defaultIterationId = useMemo(() => {
        const hintExists = item.iteration_hint_id
            ? iterations.some(iteration => iteration.id === item.iteration_hint_id)
            : false;
        const selectedExists = iterations.some(iteration => iteration.id === selectedIterationId);
        return (hintExists ? item.iteration_hint_id : null) || (selectedExists ? selectedIterationId : iterations[0]?.id) || 0;
    }, [item.iteration_hint_id, iterations, selectedIterationId]);

    const [iterationId, setIterationId] = useState(String(defaultIterationId || ''));
    const [projectId, setProjectId] = useState(item.project_hint_id ? String(item.project_hint_id) : '');
    const [assigneeId, setAssigneeId] = useState('');
    const [priority, setPriority] = useState(String(item.priority_hint || 5));
    const [tags, setTags] = useState<string[]>(item.labels);
    const [effortDays, setEffortDays] = useState('1');
    const [effortHours, setEffortHours] = useState('8');
    const [dependsOn, setDependsOn] = useState<number[]>([]);
    const [title, setTitle] = useState(item.title);
    const [description, setDescription] = useState(item.description || '');
    const [selectedTaskTemplateId, setSelectedTaskTemplateId] = useState('');
    const [draftPreview, setDraftPreview] = useState<TriageTaskDraftResponse | null>(null);

    const projectsById = useMemo(() => makeLookup(projects), [projects]);
    const iterationsById = useMemo(() => makeLookup(iterations), [iterations]);

    const parsedIterationId = Number(iterationId);
    const selectedIteration = iterations.find(iteration => iteration.id === parsedIterationId);
    const hasSelectedIteration = Boolean(selectedIteration);
    const { data: teamMembers = [], error: teamError, refetch: refetchTeam } = useQuery<TeamMember[]>({
        queryKey: ['team', parsedIterationId],
        queryFn: () => teamService.getByIteration(parsedIterationId),
        enabled: hasSelectedIteration,
    });
    const { data: taskTemplates = [], error: templatesError, refetch: refetchTemplates } = useQuery({
        queryKey: ['templates', 'task'],
        queryFn: () => templateService.getAll({ template_type: 'task' }),
    });

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

    const handleDaysChange = (value: string) => {
        setEffortDays(value);
        const parsedDays = Number(value);
        if (!Number.isNaN(parsedDays)) {
            setEffortHours(String(parsedDays * 8));
        }
    };

    const handleHoursChange = (value: string) => {
        setEffortHours(value);
        const parsedHours = Number(value);
        if (!Number.isNaN(parsedHours)) {
            setEffortDays(String(parsedHours / 8));
        }
    };

    const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        if (!hasSelectedIteration) return;
        onSubmit({
            iteration_id: parsedIterationId,
            title: title.trim(),
            description: optionalText(description),
            project_id: effectiveProjectId,
            assignee_id: parseOptionalNumber(assigneeId),
            priority: Number(priority),
            tags,
            effort_days: Number(effortDays),
            effort_hours: Number(effortHours),
            depends_on: dependsOn,
        });
    };

    const applyDraft = () => {
        if (!draftPreview) return;
        setTitle(draftPreview.suggested_title);
        setDescription(formatDraftDescription(draftPreview));
    };

    return (
        <div className="flex flex-col h-full overflow-hidden border border-border rounded-lg bg-surface-card">
            {/* Header banner */}
            <div className="flex items-center justify-between border-b border-border bg-surface-card px-6 py-4 shrink-0">
                <div>
                    <h2 className="text-xl font-bold text-content-primary">{t('surfaces.triagePage.convertToTask')}</h2>
                    <p className="text-xs text-content-secondary">Triage Item #{item.id}</p>
                </div>
                <button
                    type="button"
                    onClick={onClose}
                    className="rounded-md p-1.5 text-content-tertiary hover:bg-surface-subtle hover:text-content-primary transition-colors"
                    aria-label={t('surfaces.triagePage.close')}
                >
                    <X className="h-5 w-5" />
                </button>
            </div>

            {(teamError || templatesError) && (
                <QueryErrorState
                    className="m-4"
                    error={teamError ?? templatesError}
                    fallback={t('queryFeedback.optionLoadFailed')}
                    onRetry={() => {
                        void refetchTeam();
                        void refetchTemplates();
                    }}
                />
            )}

            {/* Split view columns */}
            <div className="flex-1 grid grid-cols-1 lg:grid-cols-2 min-h-0 divide-y lg:divide-y-0 lg:divide-x divide-border">
                {/* Left: Source Details */}
                <div className="flex flex-col h-full bg-surface-muted/50 overflow-y-auto p-6 space-y-6">
                    <div>
                        <h3 className="text-xs font-semibold uppercase tracking-wide text-content-secondary">{t('surfaces.triagePage.rawIntake')}</h3>
                        <div className="mt-2 rounded-lg border border-border bg-surface-card p-4 shadow-sm">
                            <h4 className="font-semibold text-content-primary text-base mb-2">{item.title}</h4>
                            <p className="whitespace-pre-wrap text-sm text-content-primary leading-relaxed">
                                {item.description || t('surfaces.triagePage.noDescriptionProvided')}
                            </p>
                        </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4 text-sm">
                        <InfoBlock label={t('surfaces.triagePage.source')} value={item.source || '-'} />
                        <InfoBlock label={t('surfaces.triagePage.externalKey')} value={item.external_key || '-'} />
                        <InfoBlock label={t('surfaces.triagePage.priorityHint')} value={item.priority_hint ? String(item.priority_hint) : '-'} />
                        <InfoBlock label={t('surfaces.triagePage.requests')} value={String(item.request_count ?? 0)} />
                        <InfoBlock label={t('surfaces.triagePage.assigneeHint')} value={item.assignee_hint || '-'} />
                        <InfoBlock label={t('surfaces.triagePage.projectHint')} value={item.project_hint_id ? projectsById[item.project_hint_id] || `#${item.project_hint_id}` : '-'} />
                        <InfoBlock label={t('surfaces.triagePage.iterationHint')} value={item.iteration_hint_id ? iterationsById[item.iteration_hint_id] || `#${item.iteration_hint_id}` : '-'} />
                        <InfoBlock label={t('surfaces.triagePage.created')} value={formatDateTime(item.created_at)} />
                    </div>

                    {item.source_url && (
                        <div>
                            <a
                                href={safeExternalHref(item.source_url)}
                                target="_blank"
                                rel="noreferrer"
                                className="inline-flex items-center gap-1.5 text-sm font-medium text-action hover:text-action transition-colors"
                            >
                                <ExternalLink className="h-4 w-4" />
                                {t('surfaces.triagePage.openSourceLink')}
                            </a>
                        </div>
                    )}

                    <div>
                        <h3 className="text-xs font-semibold uppercase tracking-wide text-content-secondary mb-2">{t('surfaces.triagePage.originalLabels')}</h3>
                        <div className="flex flex-wrap gap-2">
                            {item.labels.length > 0 ? item.labels.map(label => (
                                <span key={label} className="rounded-full bg-surface-hover/80 px-2.5 py-1 text-xs font-medium text-content-primary">{label}</span>
                            )) : (
                                <span className="text-sm text-content-secondary">{t('surfaces.triagePage.noLabels')}</span>
                            )}
                        </div>
                    </div>
                </div>

                {/* Right: Task Form */}
                <form onSubmit={handleSubmit} className="flex flex-col h-full overflow-hidden bg-surface-card">
                    <div className="flex-1 overflow-y-auto p-6 space-y-6">
                        {error && (
                            <div className="flex items-start gap-2 rounded-md bg-feedback-danger-muted p-3 text-sm text-feedback-danger-foreground">
                                <AlertCircle className="mt-0.5 h-4 w-4 flex-shrink-0" />
                                <span>{error}</span>
                            </div>
                        )}

                        {/* AI Suggestions / Draft Task Details Header */}
                        <div className="flex flex-wrap items-center justify-between gap-2 border-b border-border-subtle pb-3">
                            <div>
                                <h3 className="text-lg font-bold text-content-primary">{t('surfaces.triagePage.taskDetails')}</h3>
                                <p className="text-xs text-content-secondary">{t('surfaces.triagePage.configureAndRefineTheFieldsForTheNewTask')}</p>
                            </div>
                            <Button
                                type="button"
                                size="sm"
                                variant="outline"
                                onClick={() => draftMutation.mutate()}
                                isLoading={draftMutation.isPending}
                                className="shadow-sm border-action text-action hover:bg-action-muted/50"
                            >
                                <Sparkles className="mr-1.5 h-4 w-4 text-action" />
                                {t('surfaces.triagePage.draftTaskDetails')}
                            </Button>
                        </div>

                        {/* Global AI Draft Preview if available */}
                        {draftPreview && (
                            <div className="space-y-3 rounded-lg border border-action bg-action-muted/40 p-4 text-sm text-content-primary shadow-sm">
                                <div className="flex flex-wrap items-center justify-between gap-3 border-b border-action/50 pb-2">
                                    <div className="flex items-center gap-2">
                                        <span className="text-xs font-semibold uppercase tracking-wide text-action">{t('surfaces.triagePage.aiDraftPreview')}</span>
                                        <span className="rounded-full border border-action bg-surface-card px-2 py-0.5 text-xs text-action">
                                            {draftPreview.is_fallback ? t('surfaces.triagePage.fallbackDraft') : 'AI'}
                                        </span>
                                        {draftPreview.provider && (
                                            <span className="rounded-full border border-action bg-surface-card px-2 py-0.5 text-xs text-action">
                                                {draftPreview.provider}
                                            </span>
                                        )}
                                    </div>
                                    <Button type="button" size="sm" onClick={applyDraft}>
                                        {t('surfaces.triagePage.applyDraft')}
                                    </Button>
                                </div>

                                {draftPreview.warnings && draftPreview.warnings.length > 0 && (
                                    <div className="rounded border border-feedback-warning-border bg-feedback-warning-muted p-2 text-xs text-feedback-warning-foreground">
                                        <div className="font-semibold flex items-center gap-1 mb-1">
                                            <AlertCircle className="h-3.5 w-3.5 text-feedback-warning" />
                                            <span>{t('surfaces.triagePage.warnings')}</span>
                                        </div>
                                        <ul className="list-disc pl-4 space-y-0.5">
                                            {draftPreview.warnings.map((w, idx) => (
                                                <li key={idx}>{w}</li>
                                            ))}
                                        </ul>
                                    </div>
                                )}

                                <div>
                                    <p className="font-semibold text-content-primary">{draftPreview.suggested_title}</p>
                                    <p className="mt-1 whitespace-pre-wrap text-xs text-action leading-relaxed">{draftPreview.suggested_description}</p>
                                </div>

                                {/* Granular interactive suggestion options */}
                                <div className="grid grid-cols-1 gap-3 border-t border-action/50 pt-3">
                                    {draftPreview.acceptance_criteria.length > 0 && (
                                        <div>
                                            <div className="flex items-center justify-between text-xs font-semibold text-action mb-1">
                                                <span>{t('surfaces.triagePage.acceptanceCriteria')}</span>
                                                <button
                                                    type="button"
                                                    onClick={() => setDescription(prev => prev + (prev ? '\n\n' : '') + `${t('surfaces.triagePage.acceptanceCriteria')}:\n${draftPreview.acceptance_criteria.map(item => `- ${item}`).join('\n')}`)}
                                                    className="text-action hover:text-action font-semibold underline shrink-0 ml-2"
                                                >
                                                    {t('surfaces.triagePage.appendToDescription')}
                                                </button>
                                            </div>
                                            <ul className="list-disc pl-4 text-xs text-action-muted-foreground space-y-0.5">
                                                {draftPreview.acceptance_criteria.map((item, index) => (
                                                    <li key={index}>{item}</li>
                                                ))}
                                            </ul>
                                        </div>
                                    )}
                                    {draftPreview.suggested_checklist.length > 0 && (
                                        <div>
                                            <div className="flex items-center justify-between text-xs font-semibold text-action mb-1">
                                                <span>{t('surfaces.triagePage.suggestedChecklist')}</span>
                                                <button
                                                    type="button"
                                                    onClick={() => setDescription(prev => prev + (prev ? '\n\n' : '') + `${t('surfaces.triagePage.checklist')}:\n${draftPreview.suggested_checklist.map(item => `- ${item}`).join('\n')}`)}
                                                    className="text-action hover:text-action font-semibold underline shrink-0 ml-2"
                                                >
                                                    {t('surfaces.triagePage.appendToDescription')}
                                                </button>
                                            </div>
                                            <ul className="list-disc pl-4 text-xs text-action-muted-foreground space-y-0.5">
                                                {draftPreview.suggested_checklist.map((item, index) => (
                                                    <li key={index}>{item}</li>
                                                ))}
                                            </ul>
                                        </div>
                                    )}
                                    {draftPreview.risks.length > 0 && (
                                        <div>
                                            <div className="flex items-center justify-between text-xs font-semibold text-action mb-1">
                                                <span>{t('surfaces.triagePage.risks')}</span>
                                                <button
                                                    type="button"
                                                    onClick={() => setDescription(prev => prev + (prev ? '\n\n' : '') + `${t('surfaces.triagePage.risks')}:\n${draftPreview.risks.map(item => `- ${item}`).join('\n')}`)}
                                                    className="text-action hover:text-action font-semibold underline shrink-0 ml-2"
                                                >
                                                    {t('surfaces.triagePage.appendToDescription')}
                                                </button>
                                            </div>
                                            <ul className="list-disc pl-4 text-xs text-action-muted-foreground space-y-0.5">
                                                {draftPreview.risks.map((item, index) => (
                                                    <li key={index}>{item}</li>
                                                ))}
                                            </ul>
                                        </div>
                                    )}
                                </div>
                            </div>
                        )}

                        {draftErrorMessage && (
                            <div className="flex items-start gap-2 rounded-md border border-feedback-danger-border bg-feedback-danger-muted p-3 text-sm text-feedback-danger-foreground">
                                <AlertCircle className="mt-0.5 h-4 w-4 flex-shrink-0" />
                                <span>{draftErrorMessage}</span>
                            </div>
                        )}

                        {/* Title Input with Inline Suggestion */}
                        <div>
                            <Input
                                label={t('surfaces.triagePage.taskTitle')}
                                value={title}
                                onChange={event => setTitle(event.target.value)}
                                required
                                maxLength={255}
                            />
                            {draftPreview && draftPreview.suggested_title !== title && (
                                <div className="mt-1 flex items-center justify-between rounded-md bg-action-muted/30 border border-action/50 px-2 py-1 text-xs text-action">
                                    <span className="truncate">{t('surfaces.triagePage.suggested')}<strong>{draftPreview.suggested_title}</strong></span>
                                    <button
                                        type="button"
                                        onClick={() => setTitle(draftPreview.suggested_title)}
                                        className="text-action hover:text-action font-semibold underline shrink-0 ml-2"
                                    >
                                        {t('surfaces.triagePage.applySuggestedTitle')}
                                    </button>
                                </div>
                            )}
                        </div>

                        {/* Description Textarea with Inline Suggestion */}
                        <div>
                            <label className="mb-1 block text-sm font-medium text-content-primary">{t('surfaces.triagePage.description')}</label>
                            <textarea
                                value={description}
                                onChange={event => setDescription(event.target.value)}
                                className="min-h-[140px] w-full rounded-md border border-border-strong px-3 py-2 shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus text-sm"
                            />
                            {draftPreview && draftPreview.suggested_description !== description && (
                                <div className="mt-1 flex flex-col gap-1 rounded-md bg-action-muted/30 border border-action/50 px-2 py-1 text-xs text-action">
                                    <div className="flex items-center justify-between">
                                        <span>{t('surfaces.triagePage.suggestedDescriptionPreview')}</span>
                                        <button
                                            type="button"
                                            onClick={() => setDescription(draftPreview.suggested_description)}
                                            className="text-action hover:text-action font-semibold underline shrink-0 ml-2"
                                        >
                                            {t('surfaces.triagePage.applySuggestedDescription')}
                                        </button>
                                    </div>
                                    <pre className="max-h-24 overflow-y-auto whitespace-pre-wrap rounded bg-surface-card p-1.5 border border-action font-mono text-[10px] text-action leading-snug">
                                        {draftPreview.suggested_description}
                                    </pre>
                                </div>
                            )}
                        </div>

                        {/* Quick Assignment Row */}
                        <div className="grid grid-cols-2 gap-4 p-4 rounded-lg border border-border bg-surface-muted/50">
                            <div>
                                <label className="mb-1 block text-sm font-medium text-content-primary">{t('surfaces.triagePage.iteration')}</label>
                                <select
                                    value={iterationId}
                                    onChange={event => {
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
                                    }}
                                    className="w-full rounded-md border border-border-strong bg-surface-card px-3 py-2 shadow-sm focus:outline-none focus:ring-1 focus:ring-focus text-sm"
                                    required
                                >
                                    <option value="">{t('surfaces.triagePage.select')}</option>
                                    {iterations.map(iteration => (
                                        <option key={iteration.id} value={iteration.id}>{iteration.name}</option>
                                    ))}
                                </select>
                            </div>

                            <div>
                                <label className="mb-1 block text-sm font-medium text-content-primary">{t('surfaces.triagePage.project')}</label>
                                {scopedProjectId !== null ? (
                                    <div className="w-full rounded-md border border-border-strong bg-surface-subtle px-3 py-2 text-content-primary shadow-sm text-sm">
                                        {scopedProject?.name ?? `Project #${scopedProjectId}`}
                                    </div>
                                ) : (
                                    <select
                                        value={projectId}
                                        onChange={event => setProjectId(event.target.value)}
                                        className="w-full rounded-md border border-border-strong bg-surface-card px-3 py-2 shadow-sm focus:outline-none focus:ring-1 focus:ring-focus text-sm"
                                    >
                                        <option value="">{t('surfaces.triagePage.noProject')}</option>
                                        {projects.map(project => (
                                            <option key={project.id} value={project.id}>{project.name}</option>
                                        ))}
                                    </select>
                                )}
                            </div>

                            <div>
                                <label className="mb-1 block text-sm font-medium text-content-primary">{t('surfaces.triagePage.assignee')}</label>
                                <select
                                    value={assigneeId}
                                    onChange={event => setAssigneeId(event.target.value)}
                                    className="w-full rounded-md border border-border-strong bg-surface-card px-3 py-2 shadow-sm focus:outline-none focus:ring-1 focus:ring-focus text-sm"
                                    disabled={!parsedIterationId}
                                >
                                    <option value="">{t('surfaces.triagePage.unassigned')}</option>
                                    {teamMembers.map(member => (
                                        <option key={member.id} value={member.id}>
                                            {member.name}
                                        </option>
                                    ))}
                                </select>
                            </div>

                            <Input
                                label={t('surfaces.triagePage.priority')}
                                type="number"
                                min="1"
                                max="10"
                                value={priority}
                                onChange={event => setPriority(event.target.value)}
                            />
                        </div>

                        {/* Assignee Recommendations */}
                        <AssigneeRecommendationsPanel
                            targetType="triage"
                            triageItemId={item.id}
                            iterationId={hasSelectedIteration ? parsedIterationId : 0}
                            selectedAssigneeId={parseOptionalNumber(assigneeId)}
                            onSelectAssignee={teamMemberId => setAssigneeId(String(teamMemberId))}
                        />

                        {/* Collapsible: More Options */}
                        <CollapsibleSection title={t('triageConvert.moreOptions')}>
                            <div className="space-y-4 pt-1">
                                <LabelSelector
                                    label={t('surfaces.triagePage.tags')}
                                    value={tags}
                                    onChange={setTags}
                                    placeholder={t('surfaces.triagePage.addCustomTag')}
                                />

                                <div>
                                    <label className="mb-1 block text-sm font-medium text-content-primary">{t('surfaces.triagePage.taskTemplate')}</label>
                                    <select
                                        value={selectedTaskTemplateId}
                                        onChange={event => setSelectedTaskTemplateId(event.target.value)}
                                        className="w-full rounded-md border border-border-strong bg-surface-card px-3 py-2 shadow-sm focus:outline-none focus:ring-1 focus:ring-focus text-sm"
                                    >
                                        <option value="">{t('surfaces.triagePage.noTemplate')}</option>
                                        {taskTemplates.map(template => (
                                            <option key={template.id} value={template.id}>
                                                {templateDisplay(template).name}
                                            </option>
                                        ))}
                                    </select>
                                </div>

                                <div className="grid grid-cols-2 gap-4">
                                    <Input
                                        label={t('surfaces.triagePage.effortDays')}
                                        type="number"
                                        min="0.1"
                                        step="0.1"
                                        value={effortDays}
                                        onChange={event => handleDaysChange(event.target.value)}
                                    />
                                    <Input
                                        label={t('surfaces.triagePage.effortHours')}
                                        type="number"
                                        min="0.5"
                                        step="0.5"
                                        value={effortHours}
                                        onChange={event => handleHoursChange(event.target.value)}
                                    />
                                </div>

                                {hasSelectedIteration && (
                                    <div>
                                        <label className="mb-1 block text-sm font-medium text-content-primary">{t('surfaces.triagePage.dependencies')}</label>
                                        <div className="max-h-32 overflow-y-auto rounded-md border border-border p-2 bg-surface-card">
                                            <TaskDependencySelector
                                                iterationId={parsedIterationId}
                                                selectedIds={dependsOn}
                                                onChange={setDependsOn}
                                            />
                                        </div>
                                    </div>
                                )}
                            </div>
                        </CollapsibleSection>
                    </div>

                    {/* Footer Actions */}
                    <div className="flex items-center justify-end gap-3 border-t border-border bg-surface-muted/80 px-6 py-4 shrink-0">
                        <Button type="button" variant="ghost" onClick={onClose}>{t('surfaces.triagePage.cancel')}</Button>
                        <Button type="submit" isLoading={isSubmitting} disabled={!hasSelectedIteration || !title.trim()}>
                            <Send className="mr-2 h-4 w-4" />
                            {t('surfaces.triagePage.convert')}
                        </Button>
                    </div>
                </form>
            </div>
        </div>
    );
};

interface TriageDetailPanelProps {
    item: TriageItem | null;
    projectsById: Record<number, string>;
    iterationsById: Record<number, string>;
    canConvert: boolean;
    onAction: (action: TriageLifecycleAction, item: TriageItem) => void;
    onMarkSuggestion: (item: TriageItem, suggestion: TriageDuplicateSuggestion) => void;
    onConvert: (item: TriageItem) => void;
    onRequestLinksChanged: () => void;
}

const TriageDetailPanel = ({
    item,
    projectsById,
    iterationsById,
    canConvert,
    onAction,
    onMarkSuggestion,
    onConvert,
    onRequestLinksChanged,
}: TriageDetailPanelProps) => {
    const suggestionItemId = item?.id ?? 0;
    const {
        data: duplicateSuggestions,
        isLoading: isLoadingDuplicateSuggestions,
        isError: isDuplicateSuggestionsError,
        error: duplicateSuggestionsError,
        refetch: refetchDuplicateSuggestions,
    } = useQuery({
        queryKey: ['triage', 'duplicate-suggestions', suggestionItemId],
        queryFn: () => triageService.getDuplicateSuggestions(suggestionItemId),
        enabled: suggestionItemId > 0,
    });

    if (!item) {
        return (
            <aside className="flex h-full flex-col items-center justify-center rounded-lg border border-border bg-surface-card p-8 text-center text-content-secondary">
                <Inbox className="mb-3 h-8 w-8 text-content-tertiary" />
                <p className="font-medium text-content-primary">{t('surfaces.triagePage.noIntakeSelected')}</p>
                <p className="mt-1 text-sm">{t('surfaces.triagePage.selectAnItemFromTheInbox')}</p>
            </aside>
        );
    }

    const convertDisabled = item.status === 'converted' || !canConvert;

    return (
        <aside className="flex h-full flex-col rounded-lg border border-border bg-surface-card">
            <div className="border-b border-border p-5">
                <div className="mb-3 flex items-start justify-between gap-3">
                    <h2 className="text-lg font-semibold leading-6 text-content-primary">{item.title}</h2>
                    <StatusPill status={item.status} />
                </div>
                <div className="flex flex-wrap gap-2">
                    <Button size="sm" variant="secondary" onClick={() => onAction('accept', item)}>
                        <CheckCircle2 className="mr-1 h-4 w-4" />
                        {t('surfaces.triagePage.accept')}
                    </Button>
                    <Button size="sm" variant="outline" onClick={() => onAction('snooze', item)}>
                        <Clock3 className="mr-1 h-4 w-4" />
                        {t('surfaces.triagePage.snooze')}
                    </Button>
                    <Button size="sm" variant="outline" onClick={() => onAction('duplicate', item)}>
                        <CopyCheck className="mr-1 h-4 w-4" />
                        {t('surfaces.triagePage.duplicate')}
                    </Button>
                    <Button size="sm" variant="danger" onClick={() => onAction('decline', item)}>
                        <XCircle className="mr-1 h-4 w-4" />
                        {t('surfaces.triagePage.decline')}
                    </Button>
                    <Button
                        size="sm"
                        onClick={() => onConvert(item)}
                        disabled={convertDisabled}
                        title={!canConvert ? t('surfaces.triagePage.convertDisabledTooltip') : undefined}
                    >
                        <Send className="mr-1 h-4 w-4" />
                        {t('surfaces.triagePage.convert')}
                    </Button>
                </div>
            </div>

            <div className="flex-1 space-y-5 overflow-y-auto p-5">
                <section>
                    <h3 className="mb-2 text-xs font-semibold uppercase tracking-wide text-content-secondary">{t('surfaces.triagePage.rawIntake')}</h3>
                    <p className="whitespace-pre-wrap rounded-md border border-border bg-surface-muted p-3 text-sm text-content-primary">
                        {item.description || t('surfaces.triagePage.noDescriptionProvided')}
                    </p>
                </section>

                <section className="grid grid-cols-1 gap-3 text-sm sm:grid-cols-2">
                    <InfoBlock label={t('surfaces.triagePage.source')} value={item.source || '-'} />
                    <InfoBlock label={t('surfaces.triagePage.externalKey')} value={item.external_key || '-'} />
                    <InfoBlock label={t('surfaces.triagePage.priorityHint')} value={item.priority_hint ? String(item.priority_hint) : '-'} />
                    <InfoBlock label={t('surfaces.triagePage.requests')} value={String(item.request_count ?? 0)} />
                    <InfoBlock label={t('surfaces.triagePage.assigneeHint')} value={item.assignee_hint || '-'} />
                    <InfoBlock label={t('surfaces.triagePage.projectHint')} value={item.project_hint_id ? projectsById[item.project_hint_id] || `#${item.project_hint_id}` : '-'} />
                    <InfoBlock label={t('surfaces.triagePage.iterationHint')} value={item.iteration_hint_id ? iterationsById[item.iteration_hint_id] || `#${item.iteration_hint_id}` : '-'} />
                    <InfoBlock label={t('surfaces.triagePage.created')} value={formatDateTime(item.created_at)} />
                    <InfoBlock label={t('surfaces.triagePage.updated')} value={formatDateTime(item.updated_at)} />
                </section>

                {item.source_url && (
                    <a
                        href={safeExternalHref(item.source_url)}
                        target="_blank"
                        rel="noreferrer"
                        className="inline-flex items-center gap-1 text-sm font-medium text-action hover:text-action"
                    >
                        <ExternalLink className="h-4 w-4" />
                        {t('surfaces.triagePage.openSource')}
                    </a>
                )}

                <RequestSourceLinksPanel
                    targetType="triage_item"
                    targetId={item.id}
                    initialCount={item.request_count ?? 0}
                    title={t('surfaces.triagePage.requestSources')}
                    compact
                    onChanged={onRequestLinksChanged}
                />

                <section>
                    <h3 className="mb-2 text-xs font-semibold uppercase tracking-wide text-content-secondary">{t('surfaces.triagePage.labels')}</h3>
                    <div className="flex flex-wrap gap-2">
                        {item.labels.length > 0 ? item.labels.map(label => (
                            <span key={label} className="rounded-full bg-surface-subtle px-2 py-0.5 text-xs text-content-primary">{label}</span>
                        )) : (
                            <span className="text-sm text-content-secondary">{t('surfaces.triagePage.noLabels')}</span>
                        )}
                    </div>
                </section>

                <section className="grid grid-cols-1 gap-3 text-sm sm:grid-cols-2">
                    <InfoBlock label={t('surfaces.triagePage.snoozedUntil')} value={formatDateTime(item.snoozed_until)} />
                    <InfoBlock label={t('surfaces.triagePage.duplicateOf')} value={item.duplicate_of_id ? `Triage #${item.duplicate_of_id}` : item.duplicate_task_id ? `Task #${item.duplicate_task_id}` : '-'} />
                    <InfoBlock label={t('surfaces.triagePage.convertedTask')} value={item.converted_task_id ? `Task #${item.converted_task_id}` : '-'} />
                </section>

                <DuplicateSuggestionsPanel
                    suggestions={duplicateSuggestions}
                    isLoading={isLoadingDuplicateSuggestions}
                    isError={isDuplicateSuggestionsError}
                    error={duplicateSuggestionsError}
                    onRetry={() => void refetchDuplicateSuggestions()}
                    projectsById={projectsById}
                    iterationsById={iterationsById}
                    onMarkSuggestion={suggestion => onMarkSuggestion(item, suggestion)}
                />
            </div>
        </aside>
    );
};

const InfoBlock = ({ label, value }: { label: string; value: string }) => (
    <div className="rounded-md border border-border bg-surface-card p-3">
        <p className="text-xs font-medium uppercase tracking-wide text-content-secondary">{label}</p>
        <p className="mt-1 break-words text-content-primary">{value}</p>
    </div>
);

interface DuplicateSuggestionsPanelProps {
    suggestions?: TriageDuplicateSuggestionsResponse;
    isLoading: boolean;
    isError: boolean;
    error?: unknown;
    onRetry: () => void;
    projectsById: Record<number, string>;
    iterationsById: Record<number, string>;
    onMarkSuggestion: (suggestion: TriageDuplicateSuggestion) => void;
}

const DuplicateSuggestionsPanel = ({
    suggestions,
    isLoading,
    isError,
    error,
    onRetry,
    projectsById,
    iterationsById,
    onMarkSuggestion,
}: DuplicateSuggestionsPanelProps) => {
    const triageSuggestions = suggestions?.triage_items ?? [];
    const taskSuggestions = suggestions?.tasks ?? [];
    const hasSuggestions = triageSuggestions.length > 0 || taskSuggestions.length > 0;

    return (
        <section className="space-y-3">
            <div className="flex items-center justify-between gap-2">
                <h3 className="text-xs font-semibold uppercase tracking-wide text-content-secondary">{t('surfaces.triagePage.likelyDuplicates')}</h3>
                {isLoading && <Loader2 className="h-4 w-4 animate-spin text-content-tertiary" />}
            </div>

            {isError && (
                <QueryErrorState
                    error={error}
                    fallback={t('surfaces.triagePage.couldNotLoadDuplicateSuggestions')}
                    onRetry={onRetry}
                />
            )}

            {!isLoading && !isError && !hasSuggestions && (
                <div className="rounded-md border border-border bg-surface-muted p-3 text-sm text-content-secondary">
                    {t('surfaces.triagePage.noLikelyDuplicatesFound')}
                </div>
            )}

            <DuplicateSuggestionGroup
                title={t('surfaces.triagePage.triageItems')}
                suggestions={triageSuggestions}
                projectsById={projectsById}
                iterationsById={iterationsById}
                onMarkSuggestion={onMarkSuggestion}
            />
            <DuplicateSuggestionGroup
                title={t('surfaces.triagePage.tasks')}
                suggestions={taskSuggestions}
                projectsById={projectsById}
                iterationsById={iterationsById}
                onMarkSuggestion={onMarkSuggestion}
            />
        </section>
    );
};

interface DuplicateSuggestionGroupProps {
    title: string;
    suggestions: TriageDuplicateSuggestion[];
    projectsById: Record<number, string>;
    iterationsById: Record<number, string>;
    onMarkSuggestion: (suggestion: TriageDuplicateSuggestion) => void;
}

const DuplicateSuggestionGroup = ({
    title,
    suggestions,
    projectsById,
    iterationsById,
    onMarkSuggestion,
}: DuplicateSuggestionGroupProps) => {
    if (suggestions.length === 0) {
        return null;
    }

    return (
        <div className="space-y-2">
            <p className="text-xs font-medium text-content-secondary">{title}</p>
            {suggestions.map(suggestion => {
                const iteration = suggestion.iteration_id ? iterationsById[suggestion.iteration_id] || `Iteration #${suggestion.iteration_id}` : null;
                const project = suggestion.project_id ? projectsById[suggestion.project_id] || `Project #${suggestion.project_id}` : null;
                return (
                    <div key={`${suggestion.target_type}-${suggestion.target_id}`} className="rounded-md border border-border bg-surface-card p-3">
                        <div className="flex items-start justify-between gap-3">
                            <div className="min-w-0">
                                <p className="truncate text-sm font-medium text-content-primary">
                                    #{suggestion.target_id} {suggestion.title}
                                </p>
                                <p className="mt-1 text-xs text-content-secondary">
                                    Score {formatSuggestionScore(suggestion.score)}
                                    {suggestion.status ? ` / ${suggestion.status}` : ''}
                                    {iteration ? ` / ${iteration}` : ''}
                                    {project ? ` / ${project}` : ''}
                                </p>
                            </div>
                            <Button size="sm" variant="outline" onClick={() => onMarkSuggestion(suggestion)}>
                                <CopyCheck className="mr-1 h-4 w-4" />
                                {t('surfaces.triagePage.mark')}
                            </Button>
                        </div>
                        {suggestion.signals.length > 0 && (
                            <div className="mt-2 flex flex-wrap gap-1">
                                {suggestion.signals.map(signal => (
                                    <span key={signal} className="rounded-full bg-action-muted px-2 py-0.5 text-xs text-action">
                                        {signal}
                                    </span>
                                ))}
                            </div>
                        )}
                    </div>
                );
            })}
        </div>
    );
};

interface TriageRowProps {
    item: TriageItem;
    isSelected: boolean;
    projectsById: Record<number, string>;
    iterationsById: Record<number, string>;
    canConvert: boolean;
    onSelect: (id: number) => void;
    onAction: (action: TriageLifecycleAction, item: TriageItem) => void;
    onConvert: (item: TriageItem) => void;
}

const TriageRow = ({
    item,
    isSelected,
    projectsById,
    iterationsById,
    canConvert,
    onSelect,
    onAction,
    onConvert,
}: TriageRowProps) => {
    const handleActionClick = (event: MouseEvent, action: TriageLifecycleAction) => {
        event.stopPropagation();
        onAction(action, item);
    };

    const handleConvertClick = (event: MouseEvent) => {
        event.stopPropagation();
        onConvert(item);
    };
    const convertDisabled = item.status === 'converted' || !canConvert;

    return (
        <tr
            className={clsx(
                'cursor-pointer border-b border-border-subtle hover:bg-surface-muted',
                isSelected && 'bg-action-muted/70 hover:bg-action-muted'
            )}
            onClick={() => onSelect(item.id)}
        >
            <td className="px-4 py-3">
                <div className="flex min-w-0 flex-col gap-1">
                    <div className="flex items-center gap-2">
                        <span className="truncate font-medium text-content-primary">{item.title}</span>
                        {isDueSnoozed(item) && (
                            <span className="rounded-full bg-status-active-muted px-2 py-0.5 text-xs font-medium text-action">{t('surfaces.triagePage.due')}</span>
                        )}
                        {(item.request_count ?? 0) > 0 && (
                            <span className="inline-flex items-center gap-1 rounded-full bg-action-muted px-2 py-0.5 text-xs font-medium text-action">
                                <MessageSquare className="h-3 w-3" />
                                {item.request_count}
                            </span>
                        )}
                    </div>
                    <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-content-secondary">
                        <span>{item.source || 'triage'}{item.external_key ? ` / ${item.external_key}` : ''}</span>
                        {item.snoozed_until && <span>{t('surfaces.triagePage.snoozedAt', { date: formatDateTime(item.snoozed_until) })}</span>}
                    </div>
                </div>
            </td>
            <td className="px-4 py-3">
                <StatusPill status={item.status} />
            </td>
            <td className="px-4 py-3 text-sm text-content-primary">{item.priority_hint || '-'}</td>
            <td className="px-4 py-3">
                <div className="flex max-w-[160px] flex-wrap gap-1">
                    {item.labels.slice(0, 3).map(label => (
                        <span key={label} className="rounded-full bg-surface-subtle px-2 py-0.5 text-xs text-content-primary">{label}</span>
                    ))}
                    {item.labels.length > 3 && <span className="text-xs text-content-tertiary">+{item.labels.length - 3}</span>}
                    {item.labels.length === 0 && <span className="text-xs text-content-tertiary">-</span>}
                </div>
            </td>
            <td className="px-4 py-3 text-sm text-content-secondary">
                <div className="max-w-[160px] truncate">
                    {item.project_hint_id ? projectsById[item.project_hint_id] || `#${item.project_hint_id}` : '-'}
                </div>
                <div className="max-w-[160px] truncate text-xs text-content-tertiary">
                    {item.iteration_hint_id ? iterationsById[item.iteration_hint_id] || `#${item.iteration_hint_id}` : ''}
                </div>
            </td>
            <td className="px-4 py-3 text-right">
                <div className="flex justify-end gap-1">
                    <Button size="sm" variant="ghost" onClick={event => handleActionClick(event, 'accept')} title={t('surfaces.triagePage.accept')} aria-label={t('surfaces.triagePage.accept')}>
                        <CheckCircle2 className="h-4 w-4" />
                    </Button>
                    <Button size="sm" variant="ghost" onClick={event => handleActionClick(event, 'snooze')} title={t('surfaces.triagePage.snooze')} aria-label={t('surfaces.triagePage.snooze')}>
                        <Clock3 className="h-4 w-4" />
                    </Button>
                    <Button size="sm" variant="ghost" onClick={event => handleActionClick(event, 'duplicate')} title={t('surfaces.triagePage.duplicate')} aria-label={t('surfaces.triagePage.duplicate')}>
                        <CopyCheck className="h-4 w-4" />
                    </Button>
                    <Button size="sm" variant="ghost" onClick={event => handleActionClick(event, 'decline')} title={t('surfaces.triagePage.decline')} aria-label={t('surfaces.triagePage.decline')}>
                        <XCircle className="h-4 w-4" />
                    </Button>
                    <Button
                        size="sm"
                        variant="ghost"
                        onClick={handleConvertClick}
                        title={canConvert ? t('surfaces.triagePage.convert') : t('surfaces.triagePage.convertDisabledTooltip')}
                        disabled={convertDisabled}
                        aria-label={t('surfaces.triagePage.convertToTask')}
                    >
                        <Send className="h-4 w-4" />
                    </Button>
                </div>
            </td>
        </tr>
    );
};

type ActionMutationInput =
    | { type: 'accept'; itemId: number; payload: TriageActionRequest }
    | { type: 'decline'; itemId: number; payload: TriageActionRequest }
    | { type: 'snooze'; itemId: number; payload: TriageSnoozeRequest }
    | { type: 'duplicate'; itemId: number; payload: TriageDuplicateRequest };

interface ConvertMutationInput {
    itemId: number;
    payload: TriageConvertToTaskRequest;
}

const TriagePage = () => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const [searchParams, setSearchParams] = useSearchParams();
    const { selectedIterationId } = useIterationStore();
    const [search, setSearch] = useState('');
    const [sourceFilter, setSourceFilter] = useState('');
    const [statusFilter, setStatusFilter] = useState<TriageItemStatus | ''>('');
    const [activeOnly, setActiveOnly] = useState(true);
    const [selectedId, setSelectedId] = useState<number | null>(null);
    const [isCreating, setIsCreating] = useState(false);
    const [actionState, setActionState] = useState<{
        action: TriageLifecycleAction;
        item: TriageItem;
        defaultSnooze: string;
        defaultDuplicate?: DuplicateActionDefaults;
    } | null>(null);
    const [convertItem, setConvertItem] = useState<TriageItem | null>(null);
    const [conversionResult, setConversionResult] = useState<{ taskId: number; taskTitle: string } | null>(null);
    const requestedSavedViewId = Number(searchParams.get('view')) || null;
    const appliedSavedViewIdRef = useRef<number | null>(null);

    const { data: requestedSavedView, error: savedViewError, refetch: refetchSavedView } = useQuery({
        queryKey: ['saved-view', requestedSavedViewId],
        queryFn: () => savedViewService.getById(requestedSavedViewId as number),
        enabled: Boolean(requestedSavedViewId),
    });

    const clearRequestedViewParam = useCallback(() => {
        if (!searchParams.has('view')) return;
        const nextParams = new URLSearchParams(searchParams);
        nextParams.delete('view');
        appliedSavedViewIdRef.current = null;
        setSearchParams(nextParams, { replace: true });
    }, [searchParams, setSearchParams]);

    useEffect(() => {
        if (
            !requestedSavedViewId ||
            !requestedSavedView ||
            appliedSavedViewIdRef.current === requestedSavedViewId ||
            requestedSavedView.view_type !== 'triage' ||
            !requestedSavedView.is_valid
        ) {
            return;
        }

        appliedSavedViewIdRef.current = requestedSavedViewId;
        const filters = triageFiltersFromSavedView(requestedSavedView);
        const timeoutId = window.setTimeout(() => {
            setActiveOnly(filters.active);
            setStatusFilter(filters.status);
            setSearch(filters.q);
            setSourceFilter(filters.source);
        }, 0);

        return () => window.clearTimeout(timeoutId);
    }, [requestedSavedView, requestedSavedViewId]);

    const activeSavedView = requestedSavedViewId !== null && requestedSavedView?.view_type === 'triage'
        ? requestedSavedView
        : null;

    const triageFilters = useMemo<TriageListParams>(() => {
        const filters: TriageListParams = { active: activeOnly, limit: 100 };
        if (statusFilter) filters.statuses = [statusFilter];
        if (search.trim()) filters.q = search.trim();
        if (sourceFilter) filters.source = sourceFilter;
        return filters;
    }, [activeOnly, search, sourceFilter, statusFilter]);

    const { data: triageItems = [], isLoading, error: listError, refetch: refetchTriageItems } = useQuery({
        queryKey: ['triage', triageFilters],
        queryFn: () => triageService.getAll(triageFilters),
    });

    const { data: allTriageItems = [], error: allTriageError, refetch: refetchAllTriage } = useQuery({
        queryKey: ['triage', 'all'],
        queryFn: () => triageService.getAll({ active: false, limit: 500 }),
    });

    const { data: iterations = [], error: iterationsError, refetch: refetchIterations } = useQuery({
        queryKey: ['iterations'],
        queryFn: iterationService.getAll,
    });
    const hasPlannableIterations = iterations.length > 0;

    const { data: projects = [], error: projectsError, refetch: refetchProjects } = useQuery({
        queryKey: ['projects'],
        queryFn: projectService.getAll,
    });

    const projectsById = useMemo(() => makeLookup(projects), [projects]);
    const iterationsById = useMemo(() => makeLookup(iterations), [iterations]);
    const selectedItem = useMemo(() => triageItems.find(item => item.id === selectedId) ?? triageItems[0] ?? null, [selectedId, triageItems]);
    const effectiveSelectedId = selectedItem?.id ?? null;
    const sources = useMemo(() => Array.from(new Set(allTriageItems.map(item => item.source).filter((source): source is string => Boolean(source)))).sort(), [allTriageItems]);

    const counts = useMemo(() => {
        return {
            listed: triageItems.length,
            total: allTriageItems.length,
            new: allTriageItems.filter(item => item.status === 'new').length,
            snoozedDue: allTriageItems.filter(isDueSnoozed).length,
        };
    }, [allTriageItems, triageItems.length]);

    const invalidateTriageQueries = () => {
        queryClient.invalidateQueries({ queryKey: ['triage'] });
    };

    const invalidateTaskProjectQueries = (iterationId: number, projectId?: number | null) => {
        invalidateTriageQueries();
        queryClient.invalidateQueries({ queryKey: ['tasks', iterationId] });
        queryClient.invalidateQueries({ queryKey: ['tasks'] });
        queryClient.invalidateQueries({ queryKey: ['workload'] });
        queryClient.invalidateQueries({ queryKey: ['gantt', iterationId] });
        queryClient.invalidateQueries({ queryKey: ['gantt'] });
        queryClient.invalidateQueries({ queryKey: ['projects'] });
        if (projectId) {
            queryClient.invalidateQueries({ queryKey: ['projectSummary', projectId] });
            queryClient.invalidateQueries({ queryKey: ['projectTasks', projectId] });
        } else {
            queryClient.invalidateQueries({ queryKey: ['projectSummary'] });
            queryClient.invalidateQueries({ queryKey: ['projectTasks'] });
        }
    };

    const createMutation = useMutation({
        mutationFn: (payload: TriageItemCreate) => triageService.create(payload),
        onSuccess: item => {
            setIsCreating(false);
            setSelectedId(item.id);
            invalidateTriageQueries();
        },
    });

    const actionMutation = useMutation<TriageItem, unknown, ActionMutationInput>({
        mutationFn: input => {
            switch (input.type) {
                case 'accept':
                    return triageService.accept(input.itemId, input.payload);
                case 'decline':
                    return triageService.decline(input.itemId, input.payload);
                case 'snooze':
                    return triageService.snooze(input.itemId, input.payload);
                case 'duplicate':
                    return triageService.markDuplicate(input.itemId, input.payload);
            }
        },
        onSuccess: (item, variables) => {
            setActionState(null);
            setSelectedId(item.id);
            invalidateTriageQueries();
            if (variables.type === 'duplicate' && variables.payload.duplicate_task_id) {
                queryClient.invalidateQueries({ queryKey: ['tasks'] });
                queryClient.invalidateQueries({ queryKey: ['projectSummary'] });
                queryClient.invalidateQueries({ queryKey: ['projectTasks'] });
                queryClient.invalidateQueries({ queryKey: ['request-source-links'] });
            }
        },
    });

    const convertMutation = useMutation<TriageConvertToTaskResponse, unknown, ConvertMutationInput>({
        mutationFn: input => triageService.convertToTask(input.itemId, input.payload),
        onSuccess: (response, variables) => {
            setConvertItem(null);
            setConversionResult({ taskId: response.task.id, taskTitle: response.task.title });
            setSelectedId(response.triage_item.id);
            invalidateTaskProjectQueries(variables.payload.iteration_id, variables.payload.project_id);
        },
    });

    const openAction = (
        action: TriageLifecycleAction,
        item: TriageItem,
        defaultDuplicate?: DuplicateActionDefaults,
    ) => {
        actionMutation.reset();
        setActionState({
            action,
            item,
            defaultSnooze: toLocalDateTimeInputValue(new Date(Date.now() + 24 * 60 * 60 * 1000)),
            defaultDuplicate,
        });
    };

    const openSuggestedDuplicate = (item: TriageItem, suggestion: TriageDuplicateSuggestion) => {
        openAction('duplicate', item, {
            targetType: suggestion.target_type === 'task' ? 'task' : 'triage',
            targetId: suggestion.target_id,
            title: suggestion.title,
            iterationId: suggestion.iteration_id,
        });
    };

    const openConvert = (item: TriageItem) => {
        if (!hasPlannableIterations) return;
        convertMutation.reset();
        setConvertItem(item);
    };

    const handleActionSubmit = (payload: TriageActionRequest | TriageSnoozeRequest | TriageDuplicateRequest) => {
        if (!actionState) return;
        if (actionState.action === 'accept' || actionState.action === 'decline') {
            actionMutation.mutate({
                type: actionState.action,
                itemId: actionState.item.id,
                payload: payload as TriageActionRequest,
            });
            return;
        }
        if (actionState.action === 'snooze') {
            actionMutation.mutate({
                type: 'snooze',
                itemId: actionState.item.id,
                payload: payload as TriageSnoozeRequest,
            });
            return;
        }
        actionMutation.mutate({
            type: 'duplicate',
            itemId: actionState.item.id,
            payload: payload as TriageDuplicateRequest,
        });
    };

    const listErrorMessage = listError ? getErrorMessage(listError, t('surfaces.triagePage.loadFailed')) : null;
    const createErrorMessage = createMutation.error ? getErrorMessage(createMutation.error, t('surfaces.triagePage.createFailed')) : null;
    const actionErrorMessage = actionMutation.error ? getErrorMessage(actionMutation.error, t('surfaces.triagePage.updateFailed')) : null;
    const convertErrorMessage = convertMutation.error ? getErrorMessage(convertMutation.error, t('surfaces.triagePage.convertFailed')) : null;
    const supportingQueryError = savedViewError ?? allTriageError ?? iterationsError ?? projectsError;

    if (supportingQueryError) {
        return (
            <QueryErrorState
                error={supportingQueryError}
                fallback={t('queryFeedback.optionLoadFailed')}
                onRetry={() => {
                    void refetchSavedView();
                    void refetchAllTriage();
                    void refetchIterations();
                    void refetchProjects();
                }}
            />
        );
    }

    if (convertItem && hasPlannableIterations) {
        return (
            <PageLayout variant="workbench">
                <ConvertTriageSplitView
                    key={`${convertItem.id}-${convertItem.iteration_hint_id || 0}-${iterations.length}-${selectedIterationId}`}
                    item={convertItem}
                    projects={projects}
                    iterations={iterations}
                    selectedIterationId={selectedIterationId}
                    isSubmitting={convertMutation.isPending}
                    error={convertErrorMessage}
                    onSubmit={payload => convertMutation.mutate({ itemId: convertItem.id, payload })}
                    onClose={() => setConvertItem(null)}
                />
            </PageLayout>
        );
    }

    return (
        <PageLayout variant="workbench">
            <PageHeader
                title={t('surfaces.triagePage.triageIntake')}
                subtitle={t('surfaces.triagePage.reviewRawIntakeAndConvertAcceptedWorkIntoPlannedTasks')}
                actions={(
                    <button className="btn primary" onClick={() => { createMutation.reset(); setIsCreating(true); }}>
                    + {t('surfaces.triagePage.newIntake')}
                    </button>
                )}
            />
            <MetricGrid className="shrink-0">
                <div className="kpi"><div className="kpi-lbl">{t('surfaces.triagePage.listed')}</div><div className="kpi-val tnum">{counts.listed}</div></div>
                <div className="kpi"><div className="kpi-lbl">{t('surfaces.triagePage.totalIntake')}</div><div className="kpi-val tnum">{counts.total}</div></div>
                <div className="kpi"><div className="kpi-lbl">{t('surfaces.triagePage.new')}</div><div className="kpi-val tnum">{counts.new}</div></div>
                <div className="kpi"><div className="kpi-lbl">{t('surfaces.triagePage.dueSnoozed')}</div><div className="kpi-val tnum">{counts.snoozedDue}</div></div>
            </MetricGrid>

            {/* Conversion success banner */}
            {conversionResult && (
                <div className="flex items-center justify-between rounded-lg border border-feedback-success-border bg-feedback-success-muted p-3 text-sm text-feedback-success-foreground">
                    <div className="flex items-center gap-2">
                        <CheckCircle2 className="h-4 w-4" />
                        <span>{t('quickActions.taskCreated')}</span>
                    </div>
                    <div className="flex items-center gap-2">
                        <Link
                            to={`/tasks?highlight=${conversionResult.taskId}`}
                            className="inline-flex items-center gap-1 font-medium text-feedback-success-foreground hover:underline"
                        >
                            {t('quickActions.viewTask')} #{conversionResult.taskId}
                            <ExternalLink className="h-3 w-3" />
                        </Link>
                        <button
                            type="button"
                            onClick={() => setConversionResult(null)}
                            className="ml-2 rounded p-1 hover:bg-feedback-success-muted-hover"
                            aria-label={t('surfaces.triagePage.dismissConversionSuccess')}
                        >
                            <X className="h-4 w-4" aria-hidden="true" />
                        </button>
                    </div>
                </div>
            )}

            <div className="wc-toolbar">
                <div className="wc-form-grid" style={{flex:1}}>
                    <div className="relative">
                        <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-content-tertiary" />
                        <Input
                            value={search}
                            onChange={event => {
                                clearRequestedViewParam();
                                setSearch(event.target.value);
                            }}
                            placeholder={t('surfaces.triagePage.searchTitleDescriptionSourceKey')}
                            className="pl-9"
                        />
                    </div>
                    <select
                        value={statusFilter}
                        onChange={event => {
                            clearRequestedViewParam();
                            setStatusFilter(event.target.value as TriageItemStatus | '');
                        }}
                        className="input"
                    >
                        <option value="">{t('surfaces.triagePage.allStatuses')}</option>
                        {statusOptions.map(status => (
                            <option key={status} value={status}>{t(statusLabelKeys[status])}</option>
                        ))}
                    </select>
                    <select
                        value={sourceFilter}
                        onChange={event => {
                            clearRequestedViewParam();
                            setSourceFilter(event.target.value);
                        }}
                        className="input"
                    >
                        <option value="">{t('surfaces.triagePage.allSources')}</option>
                        {sources.map(source => (
                            <option key={source} value={source}>{source}</option>
                        ))}
                    </select>
                    <div className="seg">
                        <button
                            type="button"
                            onClick={() => {
                                clearRequestedViewParam();
                                setActiveOnly(true);
                            }}
                            aria-pressed={activeOnly}
                        >
                            {t('surfaces.triagePage.active')}
                        </button>
                        <button
                            type="button"
                            onClick={() => {
                                clearRequestedViewParam();
                                setActiveOnly(false);
                            }}
                            aria-pressed={!activeOnly}
                        >
                            {t('surfaces.triagePage.all')}
                        </button>
                    </div>
                    <Button
                        variant="outline"
                        onClick={() => {
                            clearRequestedViewParam();
                            setSearch('');
                            setSourceFilter('');
                            setStatusFilter('');
                            setActiveOnly(true);
                        }}
                    >
                        <ListFilter className="mr-2 h-4 w-4" />
                        {t('surfaces.triagePage.reset')}
                    </Button>
                </div>
                {activeSavedView && (
                    <div className="mt-3 inline-flex items-center rounded-full bg-action-muted px-3 py-1 text-xs font-medium text-action">
                        Saved view: {activeSavedView.name}
                    </div>
                )}
            </div>

            {!hasPlannableIterations && (
                <div className="flex flex-wrap items-center justify-between gap-3 rounded-lg border border-feedback-warning-border bg-feedback-warning-muted px-4 py-3 text-sm text-feedback-warning-foreground">
                    <div className="flex min-w-0 items-start gap-2">
                        <AlertCircle className="mt-0.5 h-4 w-4 flex-shrink-0" />
                        <div>
                            <p className="font-medium">{t('surfaces.triagePage.conversionRequiresAnIteration')}</p>
                            <p className="mt-0.5 text-feedback-warning-foreground">{t('surfaces.triagePage.intakeCanStayInTriageUntilPlanningCreatesARealTargetIteration')}</p>
                        </div>
                    </div>
                    <Link
                        to="/iterations"
                        className="inline-flex items-center rounded-md border border-feedback-warning-border bg-surface-card px-3 py-1.5 font-medium text-feedback-warning-foreground hover:bg-feedback-warning-muted-hover"
                    >
                        {t('surfaces.triagePage.createIteration')}
                    </Link>
                </div>
            )}

            <div className="grid min-h-0 flex-1 grid-cols-1 gap-4 xl:grid-cols-[minmax(0,1fr)_420px]">
                <div className="min-h-0 overflow-hidden rounded-lg border border-border bg-surface-card">
                    {listErrorMessage ? (
                        <QueryErrorState
                            className="m-4"
                            message={listErrorMessage}
                            onRetry={() => void refetchTriageItems()}
                        />
                    ) : isLoading ? (
                        <div className="flex h-full items-center justify-center p-8 text-content-secondary">{t('surfaces.triagePage.loadingIntake')}</div>
                    ) : triageItems.length === 0 ? (
                        <div className="flex h-full items-center justify-center p-8 text-center">
                            <div>
                                <Inbox className="mx-auto mb-3 h-10 w-10 text-content-tertiary" />
                                <p className="font-medium text-content-primary">{t('surfaces.triagePage.noIntakeItemsMatchTheCurrentFilters')}</p>
                                <p className="mt-1 text-sm text-content-secondary">{t('surfaces.triagePage.convertedDeclinedDuplicateAndFutureSnoozedItemsAreHiddenByTheActiveInboxUnlessFiltered')}</p>
                            </div>
                        </div>
                    ) : (
                        <div className="h-full overflow-auto">
                            <table className="min-w-[980px] w-full">
                                <thead className="sticky top-0 z-10 border-b border-border bg-surface-muted text-left text-xs font-semibold uppercase tracking-wide text-content-secondary">
                                    <tr>
                                        <th className="px-4 py-3">{t('surfaces.triagePage.item')}</th>
                                        <th className="px-4 py-3">{t('surfaces.triagePage.status')}</th>
                                        <th className="px-4 py-3">{t('surfaces.triagePage.priority')}</th>
                                        <th className="px-4 py-3">{t('surfaces.triagePage.labels')}</th>
                                        <th className="px-4 py-3">{t('surfaces.triagePage.hints')}</th>
                                        <th className="px-4 py-3 text-right">{t('surfaces.triagePage.actions')}</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {triageItems.map(item => (
                                        <TriageRow
                                            key={item.id}
                                            item={item}
                                            isSelected={item.id === effectiveSelectedId}
                                            projectsById={projectsById}
                                            iterationsById={iterationsById}
                                            canConvert={hasPlannableIterations}
                                            onSelect={setSelectedId}
                                            onAction={openAction}
                                            onConvert={openConvert}
                                        />
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>

                <div className="min-h-[420px] xl:min-h-0">
                    <TriageDetailPanel
                        item={selectedItem}
                        projectsById={projectsById}
                        iterationsById={iterationsById}
                        canConvert={hasPlannableIterations}
                        onAction={openAction}
                        onMarkSuggestion={openSuggestedDuplicate}
                        onConvert={openConvert}
                        onRequestLinksChanged={invalidateTriageQueries}
                    />
                </div>
            </div>

            {isCreating && (
                <CreateTriageModal
                    projects={projects}
                    iterations={iterations}
                    isSubmitting={createMutation.isPending}
                    error={createErrorMessage}
                    onSubmit={payload => createMutation.mutate(payload)}
                    onClose={() => setIsCreating(false)}
                />
            )}

            {actionState && (
                <TriageActionModal
                    key={`${actionState.action}-${actionState.item.id}-${actionState.defaultSnooze}-${actionState.defaultDuplicate?.targetType || 'none'}-${actionState.defaultDuplicate?.targetId || 0}`}
                    action={actionState.action}
                    item={actionState.item}
                    allTriageItems={allTriageItems}
                    iterations={iterations}
                    selectedIterationId={selectedIterationId}
                    defaultSnooze={actionState.defaultSnooze}
                    defaultDuplicate={actionState.defaultDuplicate}
                    isSubmitting={actionMutation.isPending}
                    error={actionErrorMessage}
                    onSubmit={handleActionSubmit}
                    onClose={() => setActionState(null)}
                />
            )}
        </PageLayout>
    );
};

export default TriagePage;

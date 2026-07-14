import { useMemo, useState } from 'react';
import type { FormEvent } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import clsx from 'clsx';
import { Save } from 'lucide-react';
import { Button } from '../common/Button';
import { CollapsibleSection } from '../common/CollapsibleSection';
import { projectService } from '../../services/projectService';
import { releaseService } from '../../services/releaseService';
import { getApiErrorMessage } from '../../utils/apiError';
import type { Task } from '../../types/task';
import type {
    Release,
    ReleaseCreateRequest,
    ReleaseStatus,
    ReleaseUpdateRequest,
} from '../../types/release';
import { QueryErrorState } from '../feedback/QueryState';
import { pillToneClassName, STATUS_TONE } from '../ui/tone';

interface ReleaseFormProps {
    projectId: number;
    initialData?: Release;
    onSuccess: (release: Release) => void;
    onCancel: () => void;
}

type FlattenedTask = {
    task: Task;
    level: number;
};

type ReleaseFormState = {
    name: string;
    description: string;
    status: ReleaseStatus;
    target_date: string;
    shipped_at: string;
    version: string;
    environment: string;
    task_ids: number[];
};

const releaseStatusOptions: { value: ReleaseStatus; labelKey: string }[] = [
    { value: 'planned', labelKey: 'surfaces.releaseForm.statuses.planned' },
    { value: 'building', labelKey: 'surfaces.releaseForm.statuses.building' },
    { value: 'shipped', labelKey: 'surfaces.releaseForm.statuses.shipped' },
    { value: 'canceled', labelKey: 'surfaces.releaseForm.statuses.canceled' },
];

const dateValue = (value?: string | null) => value?.slice(0, 10) || '';
const dateTimeValue = (value?: string | null) => value ? value.slice(0, 16) : '';

const flattenTasks = (tasks: Task[], level = 0): FlattenedTask[] => (
    tasks.flatMap(task => [
        { task, level },
        ...flattenTasks(task.children ?? [], level + 1),
    ])
);

const textInputClassName = 'mt-1 w-full rounded-md border border-border-strong px-3 py-2 text-sm shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus';

const nullableTrimmedText = (value: string) => {
    const trimmed = value.trim();
    return trimmed.length > 0 ? trimmed : null;
};

export const ReleaseForm = ({
    projectId,
    initialData,
    onSuccess,
    onCancel,
}: ReleaseFormProps) => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const [error, setError] = useState<string | null>(null);
    const [formData, setFormData] = useState<ReleaseFormState>({
        name: initialData?.name ?? '',
        description: initialData?.description ?? '',
        status: initialData?.status ?? 'planned',
        target_date: dateValue(initialData?.target_date),
        shipped_at: dateTimeValue(initialData?.shipped_at),
        version: initialData?.version ?? '',
        environment: initialData?.environment ?? '',
        task_ids: initialData?.task_ids ?? [],
    });

    const tasksQuery = useQuery({
        queryKey: ['projectTasks', projectId],
        queryFn: () => projectService.getTasks(projectId),
        enabled: projectId > 0,
    });
    const tasks = useMemo(() => tasksQuery.data ?? [], [tasksQuery.data]);
    const areTasksLoading = tasksQuery.isLoading;

    const flattenedTasks = useMemo(() => flattenTasks(tasks), [tasks]);
    const selectedTaskIds = useMemo(() => new Set(formData.task_ids), [formData.task_ids]);

    const invalidateReleaseQueries = (release: Release) => {
        queryClient.invalidateQueries({ queryKey: ['projectReleases', projectId] });
        queryClient.invalidateQueries({ queryKey: ['release', release.id] });
        queryClient.invalidateQueries({ queryKey: ['project', projectId] });
        queryClient.invalidateQueries({ queryKey: ['projectSummary', projectId] });
        queryClient.invalidateQueries({ queryKey: ['projectTasks', projectId] });
    };

    const createMutation = useMutation({
        mutationFn: (payload: ReleaseCreateRequest) => releaseService.createForProject(projectId, payload),
        onSuccess: (release) => {
            invalidateReleaseQueries(release);
            onSuccess(release);
        },
        onError: (err: unknown) => {
            setError(getApiErrorMessage(err, t('surfaces.releaseForm.createFailed')));
        },
    });

    const updateMutation = useMutation({
        mutationFn: (payload: ReleaseUpdateRequest) => releaseService.update(initialData!.id, payload),
        onSuccess: (release) => {
            invalidateReleaseQueries(release);
            onSuccess(release);
        },
        onError: (err: unknown) => {
            setError(getApiErrorMessage(err, t('surfaces.releaseForm.updateFailed')));
        },
    });

    const isPending = createMutation.isPending || updateMutation.isPending;
    const nameIsBlank = formData.name.trim().length === 0;

    const setField = <K extends keyof ReleaseFormState>(
        field: K,
        value: ReleaseFormState[K],
    ) => {
        setFormData(previous => ({ ...previous, [field]: value }));
        if (error) setError(null);
    };

    const toggleTask = (taskId: number) => {
        setFormData(previous => {
            const nextTaskIds = new Set(previous.task_ids);
            if (nextTaskIds.has(taskId)) {
                nextTaskIds.delete(taskId);
            } else {
                nextTaskIds.add(taskId);
            }
            return { ...previous, task_ids: Array.from(nextTaskIds) };
        });
        if (error) setError(null);
    };

    const normalizePayload = (): ReleaseCreateRequest => ({
        name: formData.name.trim(),
        description: nullableTrimmedText(formData.description),
        status: formData.status,
        target_date: formData.target_date || null,
        shipped_at: formData.shipped_at || null,
        version: nullableTrimmedText(formData.version),
        environment: nullableTrimmedText(formData.environment),
        task_ids: formData.task_ids,
    });

    const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        if (nameIsBlank || isPending) return;
        setError(null);
        const payload = normalizePayload();
        if (initialData) {
            updateMutation.mutate(payload);
        } else {
            createMutation.mutate(payload);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-5">
            {tasksQuery.isError && (
                <QueryErrorState
                    error={tasksQuery.error}
                    fallback={t('queryFeedback.optionLoadFailed')}
                    onRetry={() => void tasksQuery.refetch()}
                />
            )}
            {error && (
                <div className="rounded-md bg-feedback-danger-muted p-3 text-sm text-feedback-danger-foreground">
                    {error}
                </div>
            )}

            {/* Essential: Name and Status */}
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
                <label className="block text-sm font-medium text-content-primary" htmlFor="release-name">
                    {t('surfaces.releaseForm.name')}
                    <input
                        id="release-name"
                        value={formData.name}
                        onChange={event => setField('name', event.target.value)}
                        className={textInputClassName}
                        maxLength={255}
                    />
                </label>

                <label className="block text-sm font-medium text-content-primary" htmlFor="release-status">
                    {t('surfaces.releaseForm.status')}
                    <select
                        id="release-status"
                        value={formData.status}
                        onChange={event => setField('status', event.target.value as ReleaseStatus)}
                        className={textInputClassName}
                    >
                        {releaseStatusOptions.map(option => (
                            <option key={option.value} value={option.value}>
                                {t(option.labelKey)}
                            </option>
                        ))}
                    </select>
                </label>
            </div>

            {/* Description */}
            <label className="block text-sm font-medium text-content-primary" htmlFor="release-description">
                {t('surfaces.releaseForm.description')}
                <textarea
                    id="release-description"
                    value={formData.description}
                    onChange={event => setField('description', event.target.value)}
                    className={clsx(textInputClassName, 'min-h-20')}
                    rows={3}
                />
            </label>

            {/* Collapsible: Dates */}
            <CollapsibleSection title={t('releaseForm.dates')}>
                <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
                    <label className="block text-sm font-medium text-content-primary" htmlFor="release-target-date">
                        {t('surfaces.releaseForm.targetDate')}
                        <input
                            id="release-target-date"
                            type="date"
                            value={formData.target_date}
                            onChange={event => setField('target_date', event.target.value)}
                            className={textInputClassName}
                        />
                    </label>

                    <label className="block text-sm font-medium text-content-primary" htmlFor="release-shipped-at">
                        {t('surfaces.releaseForm.shippedAt')}
                        <input
                            id="release-shipped-at"
                            type="datetime-local"
                            value={formData.shipped_at}
                            onChange={event => setField('shipped_at', event.target.value)}
                            className={textInputClassName}
                        />
                    </label>
                </div>
            </CollapsibleSection>

            {/* Collapsible: Details */}
            <CollapsibleSection title={t('releaseForm.details')}>
                <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
                    <label className="block text-sm font-medium text-content-primary" htmlFor="release-version">
                        {t('surfaces.releaseForm.version')}
                        <input
                            id="release-version"
                            value={formData.version}
                            onChange={event => setField('version', event.target.value)}
                            className={textInputClassName}
                            maxLength={100}
                        />
                    </label>

                    <label className="block text-sm font-medium text-content-primary" htmlFor="release-environment">
                        {t('surfaces.releaseForm.environment')}
                        <input
                            id="release-environment"
                            value={formData.environment}
                            onChange={event => setField('environment', event.target.value)}
                            className={textInputClassName}
                            maxLength={100}
                        />
                    </label>
                </div>
            </CollapsibleSection>

            {/* Collapsible: Linked Tasks */}
            <CollapsibleSection title={t('releaseForm.linkedTasks')} defaultOpen={formData.task_ids.length > 0}>
                <div className="flex flex-wrap items-center justify-between gap-2">
                    <h3 className="text-sm font-semibold text-content-primary">{t('surfaces.releaseForm.linkedTasks')}</h3>
                    <span className="text-xs text-content-secondary">
                        {t('surfaces.releaseForm.selectedCount', { count: formData.task_ids.length })}
                    </span>
                </div>

                {areTasksLoading ? (
                    <div className="mt-2 rounded-md bg-surface-muted p-4 text-sm text-content-secondary">
                        {t('surfaces.releaseForm.loadingProjectTasks')}
                    </div>
                ) : flattenedTasks.length === 0 ? (
                    <div className="mt-2 rounded-md bg-surface-muted p-4 text-sm text-content-secondary">
                        {t('surfaces.releaseForm.noProjectTasksAvailable')}
                    </div>
                ) : (
                    <div className="mt-2 max-h-72 divide-y divide-border-subtle overflow-y-auto rounded-md border border-border">
                        {flattenedTasks.map(({ task, level }) => (
                            <label
                                key={task.id}
                                className="flex cursor-pointer items-center gap-3 px-3 py-2 text-sm hover:bg-surface-muted"
                                style={{ paddingLeft: 12 + level * 18 }}
                            >
                                <input
                                    type="checkbox"
                                    checked={selectedTaskIds.has(task.id)}
                                    onChange={() => toggleTask(task.id)}
                                    className="h-4 w-4 rounded border-border-strong text-action focus:ring-focus"
                                />
                                <span className="min-w-0 flex-1 truncate text-content-primary">{task.title}</span>
                                <span className={clsx('rounded-full px-2 py-0.5 text-xs', pillToneClassName[STATUS_TONE[task.status]])}>
                                    {t(`statuses.${task.status}`)}
                                </span>
                            </label>
                        ))}
                    </div>
                )}
            </CollapsibleSection>

            <div className="flex justify-end gap-3">
                <Button type="button" variant="secondary" onClick={onCancel}>
                    {t('surfaces.releaseForm.cancel')}
                </Button>
                <Button type="submit" isLoading={isPending} disabled={nameIsBlank || tasksQuery.isError}>
                    {!isPending && <Save className="mr-2 h-4 w-4" />}
                    {initialData ? t('surfaces.releaseForm.saveRelease') : t('surfaces.releaseForm.createRelease')}
                </Button>
            </div>
        </form>
    );
};

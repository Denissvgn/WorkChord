import { useMemo, useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { CalendarRange, ListChecks, Repeat, Save } from 'lucide-react';
import { Button } from '../common/Button';
import { Input } from '../common/Input';
import { CollapsibleSection } from '../common/CollapsibleSection';
import { iterationService } from '../../services/iterationService';
import { projectService } from '../../services/projectService';
import { useIterationStore } from '../../store/iterationStore';
import type { Iteration, IterationCreate, IterationSeriesCreate } from '../../types/iteration';
import { getApiErrorMessage } from '../../utils/apiError';
import { formatDate } from '../../utils/formatDate';

interface IterationFormProps {
    initialData?: Iteration;
    lockedProject?: {
        id: number;
        name: string;
    };
    hideProjectScope?: boolean;
    onSuccess: (iteration?: Iteration, iterations?: Iteration[]) => void;
    onCancel: () => void;
}

type EditorMode = 'single' | 'series';
type StopMode = 'count' | 'until_date';

type SingleDraft = {
    name: string;
    project_id: string;
    start_date: string;
    end_date: string;
    manager_email: string;
};

type SeriesDraft = {
    base_name: string;
    project_id: string;
    start_date: string;
    duration_days: number;
    stop_mode: StopMode;
    count: number;
    until_date: string;
    manager_email: string;
};

const MAX_SERIES_ITERATIONS = 100;

const toIsoDate = (date: Date) => {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
};

const todayIso = () => toIsoDate(new Date());

const addDays = (value: string, days: number) => {
    const [year, month, day] = value.split('-').map(Number);
    if (!year || !month || !day) return '';
    const date = new Date(year, month - 1, day);
    date.setDate(date.getDate() + days);
    return toIsoDate(date);
};

const isOrderedRange = (start: string, end: string) => (
    Boolean(start && end && start <= end)
);

const sequenceName = (baseName: string, index: number) => {
    const cleaned = baseName.trim();
    const match = cleaned.match(/^(.*?)(\d+)$/);
    if (match) {
        const [, prefix, number] = match;
        return `${prefix}${String(Number(number) + index).padStart(number.length, '0')}`;
    }
    return `${cleaned} ${index + 1}`;
};

const initialSingleDraft = (
    initialData: Iteration | undefined,
    lockedProject: IterationFormProps['lockedProject'],
): SingleDraft => ({
    name: initialData?.name ?? '',
    project_id: String(lockedProject?.id ?? initialData?.project_id ?? ''),
    start_date: initialData?.start_date ?? '',
    end_date: initialData?.end_date ?? '',
    manager_email: initialData?.manager_email ?? '',
});

const initialSeriesDraft = (lockedProject: IterationFormProps['lockedProject']): SeriesDraft => {
    const start = todayIso();
    return {
        base_name: '',
        project_id: String(lockedProject?.id ?? ''),
        start_date: start,
        duration_days: 14,
        stop_mode: 'count',
        count: 3,
        until_date: addDays(start, 41),
        manager_email: '',
    };
};

const IterationFormEditor = ({
    initialData,
    lockedProject,
    hideProjectScope = false,
    onSuccess,
    onCancel,
}: IterationFormProps) => {
    const { t, i18n } = useTranslation();
    const queryClient = useQueryClient();
    const { setSelectedIterationId } = useIterationStore();
    const [mode, setMode] = useState<EditorMode>('single');
    const [singleDraft, setSingleDraft] = useState<SingleDraft>(() => initialSingleDraft(initialData, lockedProject));
    const [seriesDraft, setSeriesDraft] = useState<SeriesDraft>(() => initialSeriesDraft(lockedProject));

    const projectsQuery = useQuery({
        queryKey: ['projects'],
        queryFn: projectService.getAll,
        enabled: !lockedProject && !hideProjectScope,
    });
    const projects = projectsQuery.data ?? [];

    const upsertIterations = (iterations: Iteration[]) => {
        queryClient.setQueryData<Iteration[]>(['iterations'], current => {
            const merged = new Map<number, Iteration>();
            for (const item of current ?? []) merged.set(item.id, item);
            for (const item of iterations) merged.set(item.id, item);
            return [...merged.values()].sort((a, b) => (
                b.start_date.localeCompare(a.start_date) || b.id - a.id
            ));
        });
    };

    const invalidateIterationQueries = (iterations: Iteration[]) => {
        queryClient.invalidateQueries({ queryKey: ['iterations'] });
        queryClient.invalidateQueries({ queryKey: ['projectIterations'] });
        queryClient.invalidateQueries({ queryKey: ['projects'] });
        for (const iteration of iterations) {
            queryClient.invalidateQueries({ queryKey: ['iterationSummary', iteration.id] });
            queryClient.invalidateQueries({ queryKey: ['team', iteration.id] });
            queryClient.invalidateQueries({ queryKey: ['tasks', iteration.id] });
            queryClient.invalidateQueries({ queryKey: ['gantt', iteration.id] });
            if (iteration.project_id) {
                queryClient.invalidateQueries({ queryKey: ['projectSummary', iteration.project_id] });
                queryClient.invalidateQueries({ queryKey: ['projectTasks', iteration.project_id] });
            }
        }
    };

    const handleSuccessfulIterations = (iterations: Iteration[]) => {
        if (iterations.length === 0) return;
        upsertIterations(iterations);
        invalidateIterationQueries(iterations);
        setSelectedIterationId(iterations[0].id);
        onSuccess(iterations[0], iterations);
    };

    const createMutation = useMutation({
        mutationFn: iterationService.create,
        onSuccess: iteration => handleSuccessfulIterations([iteration]),
    });

    const updateMutation = useMutation({
        mutationFn: (data: Partial<IterationCreate>) => iterationService.update(initialData!.id, data),
        onSuccess: iteration => handleSuccessfulIterations([iteration]),
    });

    const seriesMutation = useMutation({
        mutationFn: iterationService.createSeries,
        onSuccess: response => handleSuccessfulIterations(response.iterations),
    });

    const seriesPreview = useMemo(() => {
        const preview: Array<{ name: string; start_date: string; end_date: string }> = [];
        if (!seriesDraft.base_name.trim() || !seriesDraft.start_date || !seriesDraft.duration_days) return preview;
        if (seriesDraft.duration_days < 1 || seriesDraft.duration_days > 366) return preview;

        let start = seriesDraft.start_date;
        const addPreview = () => {
            const end = addDays(start, seriesDraft.duration_days - 1);
            preview.push({
                name: sequenceName(seriesDraft.base_name, preview.length),
                start_date: start,
                end_date: end,
            });
            start = addDays(end, 1);
        };

        if (seriesDraft.stop_mode === 'count') {
            for (let index = 0; index < Math.min(seriesDraft.count, MAX_SERIES_ITERATIONS + 1); index += 1) {
                addPreview();
            }
            return preview;
        }

        if (!seriesDraft.until_date || seriesDraft.until_date < seriesDraft.start_date) return preview;
        while (start <= seriesDraft.until_date && preview.length <= MAX_SERIES_ITERATIONS) {
            addPreview();
        }
        return preview;
    }, [seriesDraft]);

    const selectedProjectId = (projectId: string) => {
        if (hideProjectScope) return null;
        if (lockedProject) return lockedProject.id;
        return projectId ? Number(projectId) : null;
    };

    const isSaving = createMutation.isPending || updateMutation.isPending || seriesMutation.isPending;
    const mutationError = createMutation.error || updateMutation.error || seriesMutation.error;
    const singleValid = Boolean(
        singleDraft.name.trim()
        && singleDraft.start_date
        && singleDraft.end_date
        && isOrderedRange(singleDraft.start_date, singleDraft.end_date)
        && !isSaving,
    );
    const seriesValid = Boolean(
        seriesDraft.base_name.trim()
        && seriesDraft.start_date
        && seriesDraft.duration_days >= 1
        && seriesDraft.duration_days <= 366
        && seriesPreview.length > 0
        && seriesPreview.length <= MAX_SERIES_ITERATIONS
        && !isSaving,
    );

    const submitSingle = () => {
        const managerEmail = singleDraft.manager_email.trim();
        const payload: Partial<IterationCreate> = {
            name: singleDraft.name.trim(),
            project_id: selectedProjectId(singleDraft.project_id),
            start_date: singleDraft.start_date,
            end_date: singleDraft.end_date,
            manager_email: managerEmail || undefined,
        };

        if (initialData) {
            updateMutation.mutate(payload);
            return;
        }

        createMutation.mutate(payload as IterationCreate);
    };

    const submitSeries = () => {
        const managerEmail = seriesDraft.manager_email.trim();
        const payload: IterationSeriesCreate = {
            base_name: seriesDraft.base_name.trim(),
            project_id: selectedProjectId(seriesDraft.project_id),
            start_date: seriesDraft.start_date,
            duration_days: Number(seriesDraft.duration_days),
            stop: seriesDraft.stop_mode === 'count'
                ? { mode: 'count', count: Number(seriesDraft.count) }
                : { mode: 'until_date', until_date: seriesDraft.until_date },
            manager_email: managerEmail || undefined,
        };
        seriesMutation.mutate(payload);
    };

    const handleSubmit = (event: React.FormEvent) => {
        event.preventDefault();
        if (mode === 'series') {
            if (seriesValid) submitSeries();
            return;
        }
        if (singleValid) submitSingle();
    };

    const projectScope = (
        <div>
            <label className="block text-sm font-medium text-content-secondary mb-1">{t('iterations.projectScope')}</label>
            {lockedProject ? (
                <div className="rounded-md border border-border-strong bg-surface-muted px-3 py-2 text-sm text-content-secondary shadow-sm">
                    <div className="font-medium">{lockedProject.name}</div>
                    <p className="mt-1 text-xs text-content-tertiary">{t('projectIterations.lockedScopeHelp')}</p>
                </div>
            ) : (
                <select
                    aria-label={t('iterations.projectScope')}
                    value={mode === 'series' ? seriesDraft.project_id : singleDraft.project_id}
                    onChange={event => {
                        const value = event.target.value;
                        if (mode === 'series') {
                            setSeriesDraft(current => ({ ...current, project_id: value }));
                            return;
                        }
                        setSingleDraft(current => ({ ...current, project_id: value }));
                    }}
                    className="w-full rounded-md border border-border-strong px-3 py-2 shadow-sm focus:outline-none focus:ring-1 focus:ring-focus"
                >
                    <option value="">{t('iterations.noProjectScope')}</option>
                    {projects?.map(project => (
                        <option key={project.id} value={project.id}>
                            {project.name}
                        </option>
                    ))}
                </select>
            )}
        </div>
    );

    return (
        <form onSubmit={handleSubmit} className="iteration-period-editor space-y-6">
            {!initialData && (
                <div className="grid grid-cols-2 gap-2 rounded-lg border border-border bg-surface-muted p-1">
                    <button
                        type="button"
                        className={`inline-flex items-center justify-center gap-2 rounded-md px-3 py-2 text-sm font-medium ${mode === 'single' ? 'bg-surface-card text-content-primary shadow-sm' : 'text-content-secondary hover:text-content-primary'}`}
                        onClick={() => setMode('single')}
                    >
                        <CalendarRange className="h-4 w-4" />
                        {t('iterationForm.singleMode', 'Single period')}
                    </button>
                    <button
                        type="button"
                        className={`inline-flex items-center justify-center gap-2 rounded-md px-3 py-2 text-sm font-medium ${mode === 'series' ? 'bg-surface-card text-content-primary shadow-sm' : 'text-content-secondary hover:text-content-primary'}`}
                        onClick={() => setMode('series')}
                    >
                        <Repeat className="h-4 w-4" />
                        {t('iterationForm.seriesMode', 'Repeating series')}
                    </button>
                </div>
            )}

            {mode === 'single' ? (
                <>
                    <Input
                        label={t('iterations.iterationName')}
                        value={singleDraft.name}
                        onChange={event => setSingleDraft(current => ({ ...current, name: event.target.value }))}
                        required
                        placeholder={t('iterations.iterationNamePlaceholder')}
                    />

                    {!hideProjectScope && projectScope}

                    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                        <Input
                            type="date"
                            label={t('iterations.startDate')}
                            value={singleDraft.start_date}
                            onChange={event => setSingleDraft(current => ({ ...current, start_date: event.target.value }))}
                            required
                        />
                        <Input
                            type="date"
                            label={t('iterations.endDate')}
                            value={singleDraft.end_date}
                            onChange={event => setSingleDraft(current => ({ ...current, end_date: event.target.value }))}
                            required
                            error={
                                singleDraft.start_date && singleDraft.end_date && !isOrderedRange(singleDraft.start_date, singleDraft.end_date)
                                    ? t('iterationForm.endBeforeStart', 'End date must be on or after start date')
                                    : undefined
                            }
                        />
                    </div>
                </>
            ) : (
                <>
                    <Input
                        label={t('iterationForm.baseName', 'Base name')}
                        value={seriesDraft.base_name}
                        onChange={event => setSeriesDraft(current => ({ ...current, base_name: event.target.value }))}
                        required
                        placeholder={t('iterations.iterationNamePlaceholder')}
                    />

                    {!hideProjectScope && projectScope}

                    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                        <Input
                            type="date"
                            label={t('iterations.startDate')}
                            value={seriesDraft.start_date}
                            onChange={event => setSeriesDraft(current => ({ ...current, start_date: event.target.value }))}
                            required
                        />
                        <Input
                            type="number"
                            min={1}
                            max={366}
                            label={t('iterationForm.durationDays', 'Duration (calendar days)')}
                            value={seriesDraft.duration_days}
                            onChange={event => setSeriesDraft(current => ({ ...current, duration_days: Number(event.target.value) }))}
                            required
                        />
                    </div>

                    <div className="space-y-3 rounded-lg border border-border p-3">
                        <div className="text-sm font-medium text-content-secondary">{t('iterationForm.seriesStops', 'Series stops')}</div>
                        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
                            <label className="flex items-start gap-2 rounded-md border border-border p-3 text-sm">
                                <input
                                    type="radio"
                                    checked={seriesDraft.stop_mode === 'count'}
                                    onChange={() => setSeriesDraft(current => ({ ...current, stop_mode: 'count' }))}
                                />
                                <span>
                                    <span className="block font-medium text-content-primary">{t('iterationForm.byCount', 'After a count')}</span>
                                    <Input
                                        type="number"
                                        min={1}
                                        max={MAX_SERIES_ITERATIONS}
                                        value={seriesDraft.count}
                                        onChange={event => setSeriesDraft(current => ({ ...current, count: Number(event.target.value) }))}
                                        disabled={seriesDraft.stop_mode !== 'count'}
                                        className="mt-2"
                                        aria-label={t('iterationForm.count', 'Count')}
                                    />
                                </span>
                            </label>
                            <label className="flex items-start gap-2 rounded-md border border-border p-3 text-sm">
                                <input
                                    type="radio"
                                    checked={seriesDraft.stop_mode === 'until_date'}
                                    onChange={() => setSeriesDraft(current => ({ ...current, stop_mode: 'until_date' }))}
                                />
                                <span>
                                    <span className="block font-medium text-content-primary">{t('iterationForm.byUntilDate', 'Until a date')}</span>
                                    <Input
                                        type="date"
                                        value={seriesDraft.until_date}
                                        onChange={event => setSeriesDraft(current => ({ ...current, until_date: event.target.value }))}
                                        disabled={seriesDraft.stop_mode !== 'until_date'}
                                        className="mt-2"
                                        aria-label={t('iterationForm.untilDate', 'Until date')}
                                    />
                                </span>
                            </label>
                        </div>
                    </div>

                    <div className="rounded-lg border border-border bg-surface-muted p-3">
                        <div className="mb-2 flex items-center gap-2 text-sm font-medium text-content-secondary">
                            <ListChecks className="h-4 w-4" />
                            {t('iterationForm.preview', 'Preview')}
                        </div>
                        {seriesPreview.length === 0 ? (
                            <p className="text-sm text-content-tertiary">{t('iterationForm.previewEmpty', 'Enter the required series fields to preview generated iterations.')}</p>
                        ) : seriesPreview.length > MAX_SERIES_ITERATIONS ? (
                            <p className="text-sm text-feedback-danger-foreground">{t('iterationForm.previewTooLarge', 'Series cannot create more than 100 iterations.')}</p>
                        ) : (
                            <div className="space-y-1 text-sm">
                                {seriesPreview.slice(0, 6).map(item => (
                                    <div key={item.name} className="flex flex-wrap justify-between gap-2 rounded bg-surface-card px-2 py-1">
                                        <span className="font-medium text-content-primary">{item.name}</span>
                                        <span className="text-content-tertiary">{formatDate(item.start_date, i18n.language)} - {formatDate(item.end_date, i18n.language)}</span>
                                    </div>
                                ))}
                                {seriesPreview.length > 6 && (
                                    <p className="pt-1 text-xs text-content-tertiary">
                                        {t('iterationForm.previewMore', '+{{count}} more', { count: seriesPreview.length - 6 })}
                                    </p>
                                )}
                            </div>
                        )}
                    </div>
                </>
            )}

            <CollapsibleSection title={t('iterationForm.notifications')} defaultOpen={Boolean(
                mode === 'series' ? seriesDraft.manager_email : singleDraft.manager_email
            )}>
                <Input
                    type="email"
                    label={t('iterations.managerEmail')}
                    value={mode === 'series' ? seriesDraft.manager_email : singleDraft.manager_email}
                    onChange={event => {
                        const value = event.target.value;
                        if (mode === 'series') {
                            setSeriesDraft(current => ({ ...current, manager_email: value }));
                            return;
                        }
                        setSingleDraft(current => ({ ...current, manager_email: value }));
                    }}
                    placeholder={t('iterationForm.managerEmailPlaceholder')}
                />
            </CollapsibleSection>

            {mutationError && (
                <div className="rounded-md border border-feedback-danger-border bg-feedback-danger-muted px-3 py-2 text-sm text-feedback-danger-foreground">
                    {getApiErrorMessage(mutationError, t('iterationForm.saveFailed', 'Failed to save iteration'))}
                </div>
            )}

            <div className="flex justify-end gap-2 border-t pt-4">
                <Button type="button" variant="ghost" onClick={onCancel}>
                    {t('actions.cancel')}
                </Button>
                <Button
                    type="submit"
                    isLoading={isSaving}
                    disabled={mode === 'series' ? !seriesValid : !singleValid}
                >
                    <Save className="mr-2 h-4 w-4" />
                    {initialData
                        ? t('iterations.updateIteration')
                        : mode === 'series'
                            ? t('iterationForm.createSeries', 'Create series')
                            : t('iterations.saveIteration')}
                </Button>
            </div>
        </form>
    );
};

export const IterationForm = (props: IterationFormProps) => {
    const formKey = [
        props.initialData?.id ?? 'new',
        props.lockedProject?.id ?? 'unscoped',
        props.hideProjectScope ? 'hidden-scope' : 'visible-scope',
    ].join(':');

    return <IterationFormEditor key={formKey} {...props} />;
};

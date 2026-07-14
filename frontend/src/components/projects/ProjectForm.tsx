import { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { Save } from 'lucide-react';
import { Button } from '../common/Button';
import { Input } from '../common/Input';
import { CollapsibleSection } from '../common/CollapsibleSection';
import { projectService } from '../../services/projectService';
import { teamService } from '../../services/teamService';
import { templateService } from '../../services/templateService';
import { getApiErrorMessage } from '../../utils/apiError';
import { formatTeamMemberProfileLabel } from '../../utils/teamMemberLabels';
import {
    appendChecklistToDescription,
    getPayloadNumber,
} from '../../utils/templateDefaults';
import type { Project, ProjectCreate, ProjectHealth, ProjectStatus } from '../../types/project';
import type { WorkTemplate } from '../../types/template';
import { templateDisplay } from '../../i18n/seedDisplay';
import { QueryErrorState, QueryLoadingState } from '../feedback/QueryState';

interface ProjectFormProps {
    initialData?: Project;
    onSuccess: (project: Project) => void;
    onCancel: () => void;
}

const statusOptions: { value: ProjectStatus; labelKey: string }[] = [
    { value: 'proposed', labelKey: 'surfaces.projectForm.statuses.proposed' },
    { value: 'planned', labelKey: 'surfaces.projectForm.statuses.planned' },
    { value: 'active', labelKey: 'surfaces.projectForm.statuses.active' },
    { value: 'paused', labelKey: 'surfaces.projectForm.statuses.paused' },
    { value: 'completed', labelKey: 'surfaces.projectForm.statuses.completed' },
    { value: 'canceled', labelKey: 'surfaces.projectForm.statuses.canceled' },
];

const healthOptions: { value: ProjectHealth; labelKey: string }[] = [
    { value: 'unknown', labelKey: 'surfaces.projectForm.healths.unknown' },
    { value: 'on_track', labelKey: 'surfaces.projectForm.healths.onTrack' },
    { value: 'at_risk', labelKey: 'surfaces.projectForm.healths.atRisk' },
    { value: 'off_track', labelKey: 'surfaces.projectForm.healths.offTrack' },
];

const projectStatusValues = statusOptions.map(option => option.value);
const projectHealthValues = healthOptions.map(option => option.value);
const dateValue = (value?: string | null) => value?.slice(0, 10) || '';
const dateTimeValue = (value?: string | null) => value ? value.slice(0, 16) : '';
const isProjectStatus = (value: unknown): value is ProjectStatus => (
    typeof value === 'string' && projectStatusValues.includes(value as ProjectStatus)
);
const isProjectHealth = (value: unknown): value is ProjectHealth => (
    typeof value === 'string' && projectHealthValues.includes(value as ProjectHealth)
);

export const ProjectForm = ({ initialData, onSuccess, onCancel }: ProjectFormProps) => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const [error, setError] = useState<string | null>(null);
    const [selectedTemplateId, setSelectedTemplateId] = useState('');
    const canApplyTemplates = !initialData;
    const [formData, setFormData] = useState<ProjectCreate & { completed_at?: string | null }>({
        name: initialData?.name || '',
        description: initialData?.description || '',
        status: initialData?.status || 'planned',
        health: initialData?.health || 'unknown',
        owner_id: null,
        owner_profile_id: initialData?.owner_profile_id ?? null,
        initiative_id: initialData?.initiative_id ?? null,
        start_date: dateValue(initialData?.start_date) || null,
        target_date: dateValue(initialData?.target_date) || null,
        completed_at: dateTimeValue(initialData?.completed_at) || null,
        sort_order: initialData?.sort_order ?? 0,
    });

    const projectTemplatesQuery = useQuery({
        queryKey: ['templates', 'project'],
        queryFn: () => templateService.getAll({ template_type: 'project' }),
        enabled: canApplyTemplates,
    });

    const initiativesQuery = useQuery({
        queryKey: ['initiatives'],
        queryFn: projectService.getInitiatives,
    });

    const ownerOptionsQuery = useQuery({
        queryKey: ['teamMemberProfiles'],
        queryFn: teamService.getProfiles,
    });
    const projectTemplates = projectTemplatesQuery.data ?? [];
    const initiatives = initiativesQuery.data ?? [];
    const ownerOptions = ownerOptionsQuery.data ?? [];
    const optionQueries = [projectTemplatesQuery, initiativesQuery, ownerOptionsQuery];
    const optionError = optionQueries.find(query => query.isError)?.error;
    const optionsLoading = optionQueries.some(query => query.isLoading);

    const selectedOwnerMissing = Boolean(
        formData.owner_profile_id &&
        !ownerOptions.some(owner => owner.id === formData.owner_profile_id),
    );

    const invalidateProjectQueries = (projectId?: number) => {
        queryClient.invalidateQueries({ queryKey: ['projects'] });
        queryClient.invalidateQueries({ queryKey: ['initiatives'] });
        queryClient.invalidateQueries({ queryKey: ['projectSummary'] });
        queryClient.invalidateQueries({ queryKey: ['projectTasks'] });
        if (projectId) {
            queryClient.invalidateQueries({ queryKey: ['project', projectId] });
            queryClient.invalidateQueries({ queryKey: ['projectSummary', projectId] });
            queryClient.invalidateQueries({ queryKey: ['projectTasks', projectId] });
        }
    };

    const createMutation = useMutation({
        mutationFn: (data: ProjectCreate) => projectService.create(data),
        onSuccess: (project) => {
            invalidateProjectQueries(project.id);
            onSuccess(project);
        },
        onError: (err: unknown) => {
            setError(getApiErrorMessage(err, t('surfaces.projectForm.createFailed')));
        },
    });

    const updateMutation = useMutation({
        mutationFn: (data: typeof formData) => projectService.update(initialData!.id, data),
        onSuccess: (project) => {
            invalidateProjectQueries(project.id);
            onSuccess(project);
        },
        onError: (err: unknown) => {
            setError(getApiErrorMessage(err, t('surfaces.projectForm.updateFailed')));
        },
    });

    const normalizePayload = () => ({
        name: formData.name,
        description: formData.description?.trim() || null,
        status: formData.status,
        health: formData.health,
        owner_profile_id: formData.owner_profile_id ?? null,
        initiative_id: formData.initiative_id ?? null,
        start_date: formData.start_date || null,
        target_date: formData.target_date || null,
        completed_at: formData.completed_at || null,
        sort_order: Number.isFinite(formData.sort_order) ? formData.sort_order : 0,
    });

    const handleSubmit = (event: React.FormEvent) => {
        event.preventDefault();
        setError(null);
        const payload = normalizePayload();
        if (initialData) {
            updateMutation.mutate(payload);
        } else {
            const createPayload: ProjectCreate = {
                name: payload.name,
                description: payload.description,
                status: payload.status,
                health: payload.health,
                owner_profile_id: payload.owner_profile_id,
                initiative_id: payload.initiative_id,
                start_date: payload.start_date,
                target_date: payload.target_date,
                sort_order: payload.sort_order,
            };
            createMutation.mutate(createPayload);
        }
    };

    const applyProjectTemplate = (template: WorkTemplate) => {
        const display = templateDisplay(template);
        setFormData(prev => ({
            ...prev,
            name: display.default_title ?? prev.name,
            description: appendChecklistToDescription(
                display.default_description ?? prev.description,
                display.default_checklist,
            ),
            status: isProjectStatus(template.default_payload.status)
                ? template.default_payload.status
                : prev.status,
            health: isProjectHealth(template.default_payload.health)
                ? template.default_payload.health
                : prev.health,
            sort_order: getPayloadNumber(template.default_payload, 'sort_order', prev.sort_order),
        }));
    };

    const handleTemplateSelect = (templateId: string) => {
        setSelectedTemplateId(templateId);
        const template = projectTemplates.find(candidate => String(candidate.id) === templateId);
        if (template) {
            applyProjectTemplate(template);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-6">
            {optionsLoading && <QueryLoadingState />}
            {optionError && (
                <QueryErrorState
                    error={optionError}
                    fallback={t('queryFeedback.optionLoadFailed')}
                    onRetry={() => optionQueries.forEach(query => void query.refetch())}
                />
            )}
            {error && (
                <div className="bg-feedback-danger-muted text-feedback-danger-foreground p-3 rounded-md text-sm">
                    {error}
                </div>
            )}

            {canApplyTemplates && projectTemplates.length > 0 && (
                <div>
                    <label className="block text-sm font-medium text-content-primary mb-1">{t('surfaces.projectForm.template')}</label>
                    <select
                        value={selectedTemplateId}
                        onChange={event => handleTemplateSelect(event.target.value)}
                        className="w-full px-3 py-2 border border-border-strong rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-focus bg-surface-card"
                    >
                        <option value="">{t('surfaces.projectForm.noTemplate')}</option>
                        {projectTemplates.map(template => (
                            <option key={template.id} value={template.id}>
                                {templateDisplay(template).name}
                            </option>
                        ))}
                    </select>
                </div>
            )}

            <Input
                label={t('surfaces.projectForm.projectName')}
                value={formData.name}
                onChange={event => setFormData({ ...formData, name: event.target.value })}
                required
            />

            <div>
                <label className="block text-sm font-medium text-content-primary mb-1">{t('surfaces.projectForm.description')}</label>
                <textarea
                    value={formData.description || ''}
                    onChange={event => setFormData({ ...formData, description: event.target.value })}
                    className="w-full px-3 py-2 border border-border-strong rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-focus min-h-[96px]"
                />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <label className="block text-sm font-medium text-content-primary mb-1">{t('surfaces.projectForm.status')}</label>
                    <select
                        value={formData.status}
                        onChange={event => setFormData({ ...formData, status: event.target.value as ProjectStatus })}
                        className="w-full px-3 py-2 border border-border-strong rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-focus bg-surface-card"
                    >
                        {statusOptions.map(option => (
                            <option key={option.value} value={option.value}>{t(option.labelKey)}</option>
                        ))}
                    </select>
                </div>

                <div>
                    <label className="block text-sm font-medium text-content-primary mb-1">{t('surfaces.projectForm.health')}</label>
                    <select
                        value={formData.health}
                        onChange={event => setFormData({ ...formData, health: event.target.value as ProjectHealth })}
                        className="w-full px-3 py-2 border border-border-strong rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-focus bg-surface-card"
                    >
                        {healthOptions.map(option => (
                            <option key={option.value} value={option.value}>{t(option.labelKey)}</option>
                        ))}
                    </select>
                </div>
            </div>

            {/* Collapsible: Dates */}
            <CollapsibleSection title={t('projectForm.dates')}>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <Input
                        type="date"
                        label={t('surfaces.projectForm.startDate')}
                        value={formData.start_date || ''}
                        onChange={event => setFormData({ ...formData, start_date: event.target.value || null })}
                    />
                    <Input
                        type="date"
                        label={t('surfaces.projectForm.targetDate')}
                        value={formData.target_date || ''}
                        onChange={event => setFormData({ ...formData, target_date: event.target.value || null })}
                    />
                </div>
            </CollapsibleSection>

            {/* Collapsible: Advanced Options */}
            <CollapsibleSection title={t('taskForm.advancedOptions')}>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label className="block text-sm font-medium text-content-primary mb-1">{t('surfaces.projectForm.owner')}</label>
                        <select
                            value={formData.owner_profile_id ?? ''}
                            onChange={event => setFormData({
                                ...formData,
                                owner_id: null,
                                owner_profile_id: event.target.value ? parseInt(event.target.value) : null,
                            })}
                            className="w-full px-3 py-2 border border-border-strong rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-focus bg-surface-card"
                        >
                            <option value="">{t('surfaces.projectForm.unassigned')}</option>
                            {selectedOwnerMissing && formData.owner_profile_id && initialData?.owner_profile && (
                                <option value={formData.owner_profile_id}>
                                    {formatTeamMemberProfileLabel(initialData.owner_profile)}
                                </option>
                            )}
                            {ownerOptions.map(owner => (
                                <option key={owner.id} value={owner.id}>
                                    {formatTeamMemberProfileLabel(owner)}
                                </option>
                            ))}
                        </select>
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-content-primary mb-1">{t('surfaces.projectForm.initiative')}</label>
                        <select
                            value={formData.initiative_id ?? ''}
                            onChange={event => setFormData({
                                ...formData,
                                initiative_id: event.target.value ? parseInt(event.target.value) : null,
                            })}
                            className="w-full px-3 py-2 border border-border-strong rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-focus bg-surface-card"
                        >
                            <option value="">{t('surfaces.projectForm.noInitiative')}</option>
                            {initiatives.map(initiative => (
                                <option key={initiative.id} value={initiative.id}>
                                    {initiative.name}
                                </option>
                            ))}
                        </select>
                    </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <Input
                        type="number"
                        label={t('surfaces.projectForm.sortOrder')}
                        value={formData.sort_order}
                        onChange={event => setFormData({ ...formData, sort_order: parseInt(event.target.value) || 0 })}
                    />
                </div>

                {initialData && (
                    <Input
                        type="datetime-local"
                        label={t('surfaces.projectForm.completedAt')}
                        value={formData.completed_at || ''}
                        onChange={event => setFormData({ ...formData, completed_at: event.target.value || null })}
                    />
                )}
            </CollapsibleSection>

            <div className="flex justify-end gap-2 pt-4 border-t">
                <Button type="button" variant="ghost" onClick={onCancel}>
                    {t('surfaces.projectForm.cancel')}
                </Button>
                <Button
                    type="submit"
                    isLoading={createMutation.isPending || updateMutation.isPending}
                    disabled={optionsLoading || Boolean(optionError)}
                >
                    <Save className="w-4 h-4 mr-2" />
                    {initialData ? t('surfaces.projectForm.updateProject') : t('surfaces.projectForm.createProject')}
                </Button>
            </div>
        </form>
    );
};

import { useId, useMemo, useRef, useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import {
    Archive,
    ChevronDown,
    ChevronUp,
    Edit3,
    FileText,
    Plus,
    Save,
    Tags,
    X,
} from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { Button } from '../common/Button';
import { Input, RequiredIndicator } from '../common/Input';
import { QueryEmptyState, QueryErrorState, QueryLoadingState } from '../feedback/QueryState';
import { LabelSelector } from '../labels/LabelSelector';
import { templateService } from '../../services/templateService';
import { labelService } from '../../services/labelService';
import { getApiErrorMessage } from '../../utils/apiError';
import type { Label, LabelCreate, LabelGroup, LabelGroupCreate, LabelGroupUpdate, LabelUpdate } from '../../types/label';
import type { TemplateType, WorkTemplate, WorkTemplateCreate, WorkTemplateUpdate } from '../../types/template';
import { labelDisplay, labelGroupDisplay, templateDisplay } from '../../i18n/seedDisplay';
import { useToast } from '../feedback/toast';
import { OverflowMenu } from '../ui';
import { SlideOverDrawer } from '../ui/SlideOverDrawer';
import type { MutationFeedbackMeta } from '../../features/mutationFeedback';

const arrayMove = <T,>(items: T[], from: number, to: number) => {
    const next = [...items];
    const [moved] = next.splice(from, 1);
    next.splice(to, 0, moved);
    return next;
};

type ManagementSection = 'templates' | 'labels';
interface TemplateFormState {
    name: string;
    description: string;
    template_type: TemplateType;
    default_title: string;
    default_description: string;
    default_priority: string;
    default_effort_days: string;
    default_labels: string[];
    default_checklist: string;
    default_payload: string;
    is_active: boolean;
    sort_order: number;
}

interface LabelGroupFormState {
    key: string;
    name: string;
    description: string;
    color: string;
    is_active: boolean;
    sort_order: number;
}

interface LabelFormState {
    slug: string;
    name: string;
    group_id: string;
    description: string;
    color: string;
    is_active: boolean;
    sort_order: number;
}

const templateTypes: { value: TemplateType; labelKey: string }[] = [
    { value: 'task', labelKey: 'surfaces.templateLabels.taskType' },
    { value: 'project', labelKey: 'surfaces.templateLabels.projectType' },
    { value: 'triage', labelKey: 'surfaces.templateLabels.triageType' },
];

const optionalText = (value: string) => {
    const trimmed = value.trim();
    return trimmed ? trimmed : null;
};

const nextSortOrder = (items: { sort_order: number }[]) => (
    items.length > 0 ? Math.max(...items.map(item => item.sort_order)) + 10 : 10
);

const splitLines = (value: string) => (
    value.split('\n').map(item => item.trim()).filter(Boolean)
);

const formatJson = (value: Record<string, unknown>) => (
    JSON.stringify(value && typeof value === 'object' ? value : {}, null, 2)
);

const emptyTemplateForm = (templateType: TemplateType, sortOrder: number): TemplateFormState => ({
    name: '',
    description: '',
    template_type: templateType,
    default_title: '',
    default_description: '',
    default_priority: '',
    default_effort_days: '',
    default_labels: [],
    default_checklist: '',
    default_payload: '{}',
    is_active: true,
    sort_order: sortOrder,
});

const templateToForm = (template: WorkTemplate): TemplateFormState => ({
    name: template.name,
    description: template.description ?? '',
    template_type: template.template_type,
    default_title: template.default_title ?? '',
    default_description: template.default_description ?? '',
    default_priority: template.default_priority != null ? String(template.default_priority) : '',
    default_effort_days: template.default_effort_days != null ? String(template.default_effort_days) : '',
    default_labels: template.default_labels ?? [],
    default_checklist: (template.default_checklist ?? []).join('\n'),
    default_payload: formatJson(template.default_payload),
    is_active: template.is_active,
    sort_order: template.sort_order,
});

const parseTemplatePayload = (
    form: TemplateFormState,
    messages: { invalidJson: string; mustBeObject: string },
): WorkTemplateCreate => {
    let parsedPayload: unknown;
    try {
        parsedPayload = form.default_payload.trim() ? JSON.parse(form.default_payload) : {};
    } catch {
        throw new Error(messages.invalidJson);
    }

    if (!parsedPayload || typeof parsedPayload !== 'object' || Array.isArray(parsedPayload)) {
        throw new Error(messages.mustBeObject);
    }

    return {
        name: form.name.trim(),
        description: optionalText(form.description),
        template_type: form.template_type,
        default_title: optionalText(form.default_title),
        default_description: optionalText(form.default_description),
        default_priority: form.default_priority === '' ? null : Number(form.default_priority),
        default_effort_days: form.default_effort_days === '' ? null : Number(form.default_effort_days),
        default_labels: form.default_labels,
        default_checklist: splitLines(form.default_checklist),
        default_payload: parsedPayload as Record<string, unknown>,
        is_active: form.is_active,
        sort_order: form.sort_order,
    };
};

const emptyGroupForm = (sortOrder: number): LabelGroupFormState => ({
    key: '',
    name: '',
    description: '',
    color: '#64748b',
    is_active: true,
    sort_order: sortOrder,
});

const groupToForm = (group: LabelGroup): LabelGroupFormState => ({
    key: group.key,
    name: group.name,
    description: group.description ?? '',
    color: group.color,
    is_active: group.is_active,
    sort_order: group.sort_order,
});

const emptyLabelForm = (group: LabelGroup): LabelFormState => ({
    slug: '',
    name: '',
    group_id: String(group.id),
    description: '',
    color: group.color,
    is_active: true,
    sort_order: nextSortOrder(group.labels),
});

const labelToForm = (label: Label): LabelFormState => ({
    slug: label.slug,
    name: label.name,
    group_id: String(label.group_id),
    description: label.description ?? '',
    color: label.color,
    is_active: label.is_active,
    sort_order: label.sort_order,
});

const formToGroupPayload = (form: LabelGroupFormState): LabelGroupCreate => ({
    key: form.key.trim(),
    name: form.name.trim(),
    description: optionalText(form.description),
    color: form.color,
    is_active: form.is_active,
    sort_order: form.sort_order,
});

const formToLabelPayload = (form: LabelFormState): LabelCreate => ({
    slug: form.slug.trim(),
    name: form.name.trim(),
    group_id: Number(form.group_id),
    description: optionalText(form.description),
    color: form.color,
    is_active: form.is_active,
    sort_order: form.sort_order,
});

const waitForAllUpdates = async (updates: Promise<unknown>[]) => {
    const results = await Promise.allSettled(updates);
    const failedUpdate = results.find(
        (result): result is PromiseRejectedResult => result.status === 'rejected',
    );
    if (failedUpdate) throw failedUpdate.reason;
};

interface TemplateRowProps {
    isBusy: boolean;
    template: WorkTemplate;
    isFirst: boolean;
    isLast: boolean;
    onEdit: (template: WorkTemplate) => void;
    onToggleActive: (template: WorkTemplate) => void;
    onMove: (template: WorkTemplate, direction: -1 | 1) => void;
}

/** One template: an "Active" switch with its label, Edit, and a menu that moves it up or down. */
const TemplateRow = ({ isBusy, template, isFirst, isLast, onEdit, onToggleActive, onMove }: TemplateRowProps) => {
    const { t } = useTranslation();
    const display = templateDisplay(template);
    const headingId = `work-template-${template.id}-heading`;
    const switchId = `work-template-${template.id}-active`;

    return (
        <article
            className={`rounded-lg border bg-surface-card p-4 shadow-sm ${template.is_active ? 'border-border' : 'border-border opacity-70'}`}
            aria-labelledby={headingId}
        >
            <div className="flex items-start gap-3">
                <div className="min-w-0 flex-1">
                    <div className="flex flex-wrap items-center gap-2">
                        <h4 id={headingId} className="font-medium text-content-primary">{display.name}</h4>
                        {template.seed_key && (
                            <span className="rounded-full bg-action-muted px-2 py-0.5 text-xs font-medium text-action">{t('surfaces.templateLabels.seeded')}</span>
                        )}
                    </div>
                    {display.description && (
                        <p className="mt-1 line-clamp-2 text-sm text-content-secondary">{display.description}</p>
                    )}
                    <div className="mt-2 flex flex-wrap gap-2 text-xs text-content-secondary">
                        {template.default_priority != null && <span>P{template.default_priority}</span>}
                        {template.default_effort_days != null && <span>{template.default_effort_days}d</span>}
                        {template.default_labels.map(label => (
                            <span key={label} className="rounded-full bg-surface-muted px-2 py-0.5 text-content-secondary">{label}</span>
                        ))}
                    </div>
                </div>
                <div className="flex shrink-0 items-center gap-2">
                    <label htmlFor={switchId} className="flex cursor-pointer items-center gap-2 text-sm text-content-secondary">
                        <input
                            id={switchId}
                            type="checkbox"
                            role="switch"
                            checked={template.is_active}
                            disabled={isBusy}
                            onChange={() => onToggleActive(template)}
                            aria-describedby={headingId}
                            className="h-4 w-4"
                        />
                        {t('surfaces.templateLabels.active')}
                    </label>
                    <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        onClick={() => onEdit(template)}
                        disabled={isBusy}
                        aria-label={`${t('surfaces.templateLabels.editTemplate')}: ${display.name}`}
                    >
                        <Edit3 className="mr-1 h-4 w-4" aria-hidden="true" />
                        {t('actions.edit')}
                    </Button>
                    <OverflowMenu
                        label={t('surfaces.templateLabels.rowActions', { name: display.name })}
                        items={[
                            { label: t('surfaces.templateLabels.moveUp'), icon: <ChevronUp className="h-4 w-4" aria-hidden="true" />, onSelect: () => onMove(template, -1), disabled: isBusy || isFirst },
                            { label: t('surfaces.templateLabels.moveDown'), icon: <ChevronDown className="h-4 w-4" aria-hidden="true" />, onSelect: () => onMove(template, 1), disabled: isBusy || isLast },
                        ]}
                    />
                </div>
            </div>
        </article>
    );
};

export const TemplateLabelSettings = () => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const toast = useToast();
    const [activeSection, setActiveSection] = useState<ManagementSection>('templates');
    const [activeTemplateType, setActiveTemplateType] = useState<TemplateType>('task');
    const [templateForm, setTemplateForm] = useState<{ id: number | null; state: TemplateFormState } | null>(null);
    const [templateFormError, setTemplateFormError] = useState<string | null>(null);
    const [includeArchivedLabels, setIncludeArchivedLabels] = useState(false);
    const [groupForm, setGroupForm] = useState<{ id: number | null; state: LabelGroupFormState } | null>(null);
    const [labelForm, setLabelForm] = useState<{ id: number | null; state: LabelFormState } | null>(null);
    const sectionTabRefs = useRef<Partial<Record<ManagementSection, HTMLButtonElement | null>>>({});
    const editorControlPrefix = useId();
    const templateTypeId = `${editorControlPrefix}-template-type`;
    const templateDescriptionId = `${editorControlPrefix}-template-description`;
    const templateDefaultDescriptionId = `${editorControlPrefix}-template-default-description`;
    const templateChecklistId = `${editorControlPrefix}-template-checklist`;
    const templatePayloadId = `${editorControlPrefix}-template-payload`;
    const groupDescriptionId = `${editorControlPrefix}-group-description`;
    const labelGroupId = `${editorControlPrefix}-label-group`;
    const labelDescriptionId = `${editorControlPrefix}-label-description`;

    const invalidateTemplates = () => (
        queryClient.invalidateQueries({ queryKey: ['templates'] })
    );

    const invalidateLabels = () => Promise.all([
        queryClient.invalidateQueries({ queryKey: ['label-groups'] }),
        queryClient.invalidateQueries({ queryKey: ['labels'] }),
    ]);

    const {
        data: templates = [],
        error: templatesError,
        isError: isTemplatesError,
        isLoading: templatesLoading,
        refetch: refetchTemplates,
    } = useQuery({
        queryKey: ['templates', { includeInactive: true }],
        queryFn: () => templateService.getAll({ include_inactive: true }),
    });

    const {
        data: labelGroups = [],
        error: labelsError,
        isError: isLabelsError,
        isLoading: labelsLoading,
        refetch: refetchLabels,
    } = useQuery({
        queryKey: ['label-groups', { includeInactive: includeArchivedLabels }],
        queryFn: () => labelService.getGroups({ include_inactive: includeArchivedLabels }),
    });

    const visibleTemplates = useMemo(() => (
        templates.filter(template => template.template_type === activeTemplateType)
    ), [templates, activeTemplateType]);

    const saveTemplateMutation = useMutation({
        mutationFn: async ({ id, data }: { id: number | null; data: WorkTemplateCreate | WorkTemplateUpdate }) => (
            id ? templateService.update(id, data as WorkTemplateUpdate) : templateService.create(data as WorkTemplateCreate)
        ),
        onSuccess: () => {
            invalidateTemplates();
            setTemplateForm(null);
            setTemplateFormError(null);
            toast.success(t('surfaces.templateLabels.templateSaved'));
        },
        onError: (error: unknown) => {
            const message = getApiErrorMessage(error, t('queryFeedback.fallback'));
            setTemplateFormError(message);
            toast.error(message);
        },
    });

    const updateTemplateMutation = useMutation({
        mutationFn: ({ id, data }: { id: number; data: WorkTemplateUpdate }) => templateService.update(id, data),
        onSuccess: () => {
            invalidateTemplates();
            toast.success(t('surfaces.templateLabels.templateUpdated'));
        },
        onError: (error: unknown) => toast.error(getApiErrorMessage(error, t('queryFeedback.fallback'))),
    });

    const reorderTemplatesMutation = useMutation({
        mutationFn: async (nextTemplates: WorkTemplate[]) => {
            await waitForAllUpdates(nextTemplates.map((template, index) => (
                templateService.update(template.id, { sort_order: (index + 1) * 10 })
            )));
        },
        onSuccess: () => {
            toast.success(t('surfaces.templateLabels.templateOrderSaved'));
        },
        onError: () => toast.error(t('surfaces.templateLabels.templateOrderSaveFailed')),
        onSettled: invalidateTemplates,
    });

    const saveGroupMutation = useMutation({
        mutationFn: async ({ id, data }: { id: number | null; data: LabelGroupCreate | LabelGroupUpdate }) => (
            id ? labelService.updateGroup(id, data as LabelGroupUpdate) : labelService.createGroup(data as LabelGroupCreate)
        ),
        onSuccess: () => {
            invalidateLabels();
            setGroupForm(null);
            toast.success(t('surfaces.templateLabels.labelGroupSaved'));
        },
        onError: (error: unknown) => toast.error(getApiErrorMessage(error, t('queryFeedback.fallback'))),
    });

    const saveLabelMutation = useMutation({
        mutationFn: async ({ id, data }: { id: number | null; data: LabelCreate | LabelUpdate }) => (
            id ? labelService.updateLabel(id, data as LabelUpdate) : labelService.createLabel(data as LabelCreate)
        ),
        onSuccess: () => {
            invalidateLabels();
            setLabelForm(null);
            toast.success(t('surfaces.templateLabels.labelSaved'));
        },
        onError: (error: unknown) => toast.error(getApiErrorMessage(error, t('queryFeedback.fallback'))),
    });

    // feedback-policy: mutation pending,toast - the taxonomy locks while the row action is recoverable by retry.
    const toggleGroupMutation = useMutation({
        // Archiving is reversible, so it says so and offers the way back through the shared feedback.
        meta: {
            success: (_data, variables) => {
                const { isActive, name } = variables as { isActive: boolean; name: string };
                return t(isActive ? 'surfaces.templateLabels.groupRestored' : 'surfaces.templateLabels.groupArchived', { name });
            },
            undo: (_data, variables) => {
                const { id, isActive, name } = variables as { id: number; isActive: boolean; name: string };
                return isActive ? null : { run: () => labelService.updateGroup(id, { is_active: true }), done: t('surfaces.templateLabels.groupRestored', { name }) };
            },
        } satisfies MutationFeedbackMeta,
        mutationFn: ({ id, isActive }: { id: number; isActive: boolean; name: string }) => (
            labelService.updateGroup(id, { is_active: isActive })
        ),
        onSuccess: () => { invalidateLabels(); },
        onError: (error: unknown) => toast.error(getApiErrorMessage(error, t('queryFeedback.fallback'))),
    });

    // feedback-policy: mutation pending,toast - the taxonomy locks while the row action is recoverable by retry.
    const toggleLabelMutation = useMutation({
        meta: {
            success: (_data, variables) => {
                const { isActive, name } = variables as { isActive: boolean; name: string };
                return t(isActive ? 'surfaces.templateLabels.labelRestored' : 'surfaces.templateLabels.labelArchived', { name });
            },
            undo: (_data, variables) => {
                const { id, isActive, name } = variables as { id: number; isActive: boolean; name: string };
                return isActive ? null : { run: () => labelService.updateLabel(id, { is_active: true }), done: t('surfaces.templateLabels.labelRestored', { name }) };
            },
        } satisfies MutationFeedbackMeta,
        mutationFn: ({ id, isActive }: { id: number; isActive: boolean; name: string }) => (
            labelService.updateLabel(id, { is_active: isActive })
        ),
        onSuccess: () => { invalidateLabels(); },
        onError: (error: unknown) => toast.error(getApiErrorMessage(error, t('queryFeedback.fallback'))),
    });

    const reorderGroupsMutation = useMutation({
        mutationFn: async (groups: LabelGroup[]) => {
            await waitForAllUpdates(groups.map((group, index) => (
                labelService.updateGroup(group.id, { sort_order: (index + 1) * 10 })
            )));
        },
        onSuccess: () => {
            toast.success(t('surfaces.templateLabels.groupOrderSaved'));
        },
        onError: () => toast.error(t('surfaces.templateLabels.groupOrderSaveFailed')),
        onSettled: invalidateLabels,
    });

    const reorderLabelsMutation = useMutation({
        mutationFn: async (labels: Label[]) => {
            await waitForAllUpdates(labels.map((label, index) => (
                labelService.updateLabel(label.id, { sort_order: (index + 1) * 10 })
            )));
        },
        onSuccess: () => {
            toast.success(t('surfaces.templateLabels.labelOrderSaved'));
        },
        onError: () => toast.error(t('surfaces.templateLabels.labelOrderSaveFailed')),
        onSettled: invalidateLabels,
    });

    const isTemplateListBusy = saveTemplateMutation.isPending
        || updateTemplateMutation.isPending
        || reorderTemplatesMutation.isPending;
    const isLabelsBusy = saveGroupMutation.isPending
        || toggleGroupMutation.isPending
        || reorderGroupsMutation.isPending
        || saveLabelMutation.isPending
        || toggleLabelMutation.isPending
        || reorderLabelsMutation.isPending;
    const isGroupListBusy = isLabelsBusy;
    const isLabelListBusy = isLabelsBusy;
    const isAnyMutationPending = isTemplateListBusy || isLabelsBusy;

    const startCreateTemplate = () => {
        setTemplateForm({ id: null, state: emptyTemplateForm(activeTemplateType, nextSortOrder(visibleTemplates)) });
        setTemplateFormError(null);
    };

    const startEditTemplate = (template: WorkTemplate) => {
        setTemplateForm({ id: template.id, state: templateToForm(template) });
        setTemplateFormError(null);
    };

    const saveTemplate = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        if (!templateForm) return;

        try {
            const payload = parseTemplatePayload(templateForm.state, {
                invalidJson: t('surfaces.templateLabels.payloadInvalidJson'),
                mustBeObject: t('surfaces.templateLabels.payloadMustBeObject'),
            });
            saveTemplateMutation.mutate({ id: templateForm.id, data: payload });
        } catch (error) {
            setTemplateFormError(error instanceof Error ? error.message : t('surfaces.templateLabels.formInvalid'));
        }
    };

    // One reorder pattern everywhere: Move up and Move down in the row menu.
    const moveTemplate = (template: WorkTemplate, direction: -1 | 1) => {
        if (isTemplateListBusy) return;
        const oldIndex = visibleTemplates.findIndex(candidate => candidate.id === template.id);
        const newIndex = oldIndex + direction;
        if (oldIndex === -1 || newIndex < 0 || newIndex >= visibleTemplates.length) return;
        reorderTemplatesMutation.mutate(arrayMove(visibleTemplates, oldIndex, newIndex));
    };

    const updateTemplateForm = <K extends keyof TemplateFormState>(field: K, value: TemplateFormState[K]) => {
        setTemplateForm(prev => prev ? ({ ...prev, state: { ...prev.state, [field]: value } }) : prev);
    };

    const updateGroupForm = <K extends keyof LabelGroupFormState>(field: K, value: LabelGroupFormState[K]) => {
        setGroupForm(prev => prev ? ({ ...prev, state: { ...prev.state, [field]: value } }) : prev);
    };

    const updateLabelForm = <K extends keyof LabelFormState>(field: K, value: LabelFormState[K]) => {
        setLabelForm(prev => prev ? ({ ...prev, state: { ...prev.state, [field]: value } }) : prev);
    };

    const moveGroup = (group: LabelGroup, direction: -1 | 1) => {
        if (isGroupListBusy) return;
        const oldIndex = labelGroups.findIndex(candidate => candidate.id === group.id);
        const newIndex = oldIndex + direction;
        if (oldIndex === -1 || newIndex < 0 || newIndex >= labelGroups.length) return;
        reorderGroupsMutation.mutate(arrayMove(labelGroups, oldIndex, newIndex));
    };

    const moveLabel = (group: LabelGroup, label: Label, direction: -1 | 1) => {
        if (isLabelListBusy) return;
        const oldIndex = group.labels.findIndex(candidate => candidate.id === label.id);
        const newIndex = oldIndex + direction;
        if (oldIndex === -1 || newIndex < 0 || newIndex >= group.labels.length) return;
        reorderLabelsMutation.mutate(arrayMove(group.labels, oldIndex, newIndex));
    };

    const handleSectionKeyDown = (
        event: React.KeyboardEvent<HTMLButtonElement>,
        currentSection: ManagementSection,
    ) => {
        if (isAnyMutationPending) return;
        let nextSection: ManagementSection | null = null;
        if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
            nextSection = currentSection === 'templates' ? 'labels' : 'templates';
        }
        if (event.key === 'Home') nextSection = 'templates';
        if (event.key === 'End') nextSection = 'labels';
        if (!nextSection) return;
        event.preventDefault();
        setActiveSection(nextSection);
        sectionTabRefs.current[nextSection]?.focus();
    };

    return (
        <div className="max-w-6xl space-y-6">
            <div
                className="inline-flex rounded-lg border border-border bg-surface-card p-1"
                role="tablist"
                aria-label={t('surfaces.templateLabels.managementSections')}
            >
                <button
                    type="button"
                    role="tab"
                    id="template-labels-tab-templates"
                    aria-selected={activeSection === 'templates'}
                    aria-controls="template-labels-panel-templates"
                    tabIndex={activeSection === 'templates' ? 0 : -1}
                    ref={node => { sectionTabRefs.current.templates = node; }}
                    onKeyDown={event => handleSectionKeyDown(event, 'templates')}
                    onClick={() => setActiveSection('templates')}
                    disabled={isAnyMutationPending}
                    className={`flex items-center gap-2 rounded-md px-3 py-2 text-sm font-medium disabled:cursor-not-allowed disabled:opacity-60 ${
                        activeSection === 'templates' ? 'bg-action-muted text-action' : 'text-content-secondary hover:bg-surface-muted'
                    }`}
                >
                    <FileText aria-hidden="true" className="h-4 w-4" />
                    {t('surfaces.templateLabels.templates')}
                </button>
                <button
                    type="button"
                    role="tab"
                    id="template-labels-tab-labels"
                    aria-selected={activeSection === 'labels'}
                    aria-controls="template-labels-panel-labels"
                    tabIndex={activeSection === 'labels' ? 0 : -1}
                    ref={node => { sectionTabRefs.current.labels = node; }}
                    onKeyDown={event => handleSectionKeyDown(event, 'labels')}
                    onClick={() => setActiveSection('labels')}
                    disabled={isAnyMutationPending}
                    className={`flex items-center gap-2 rounded-md px-3 py-2 text-sm font-medium disabled:cursor-not-allowed disabled:opacity-60 ${
                        activeSection === 'labels' ? 'bg-action-muted text-action' : 'text-content-secondary hover:bg-surface-muted'
                    }`}
                >
                    <Tags aria-hidden="true" className="h-4 w-4" />
                    {t('surfaces.templateLabels.labels')}
                </button>
            </div>

            {activeSection === 'templates' && (
                <section
                    id="template-labels-panel-templates"
                    role="tabpanel"
                    aria-labelledby="template-labels-tab-templates"
                    className="space-y-6"
                >
                    <section className="card space-y-4" aria-labelledby="template-list-heading">
                        <div className="flex flex-wrap items-center justify-between gap-3">
                            <div>
                                <h3 id="template-list-heading" className="text-lg font-semibold text-content-primary">{t('surfaces.templateLabels.templates')}</h3>
                                <p className="text-sm text-content-secondary">{t('surfaces.templateLabels.manageDefaultsUsedByCreateForms')}</p>
                            </div>
                            <Button type="button" onClick={startCreateTemplate} disabled={templatesLoading || isTemplatesError || isTemplateListBusy}>
                                <Plus className="mr-2 h-4 w-4" />
                                {t('surfaces.templateLabels.newTemplate')}
                            </Button>
                        </div>

                        <div className="flex flex-wrap gap-2">
                            {templateTypes.map(option => (
                                <button
                                    key={option.value}
                                    type="button"
                                    onClick={() => setActiveTemplateType(option.value)}
                                    disabled={templatesLoading || isTemplatesError || isTemplateListBusy}
                                    className={`rounded-md border px-3 py-1.5 text-sm font-medium ${
                                        activeTemplateType === option.value
                                            ? 'border-action bg-action-muted text-action'
                                            : 'border-border bg-surface-card text-content-secondary hover:bg-surface-muted'
                                    }`}
                                >
                                    {t(option.labelKey)}
                                </button>
                            ))}
                        </div>

                        {templatesLoading ? (
                            <QueryLoadingState message={t('surfaces.templateLabels.loadingTemplates')} />
                        ) : isTemplatesError ? (
                            <QueryErrorState
                                error={templatesError}
                                fallback={t('queryFeedback.fallback')}
                                onRetry={() => { void refetchTemplates(); }}
                                title={t('surfaces.templateLabels.templates')}
                            />
                        ) : visibleTemplates.length === 0 ? (
                            <QueryEmptyState title={t('queryFeedback.emptyTitle')} />
                        ) : (
                            <div className="space-y-3">
                                {visibleTemplates.map((template, index) => (
                                    <TemplateRow
                                        isBusy={isTemplateListBusy}
                                        key={template.id}
                                        template={template}
                                        isFirst={index === 0}
                                        isLast={index === visibleTemplates.length - 1}
                                        onEdit={startEditTemplate}
                                        onMove={moveTemplate}
                                        onToggleActive={(item) => updateTemplateMutation.mutate({
                                            id: item.id,
                                            data: { is_active: !item.is_active },
                                        })}
                                    />
                                ))}
                            </div>
                        )}
                    </section>

                    {/* The editor opens in the shared drawer, beside the list at every width. */}
                    <SlideOverDrawer
                        open={templateForm !== null}
                        title={templateForm?.id ? t('surfaces.templateLabels.editTemplate') : t('surfaces.templateLabels.templateDetails')}
                        ariaLabel={templateForm?.id ? t('surfaces.templateLabels.editTemplate') : t('surfaces.templateLabels.templateDetails')}
                        onClose={() => { if (!isTemplateListBusy) setTemplateForm(null); }}
                        closeDisabled={isTemplateListBusy}
                        closeLabel={t('surfaces.templateLabels.closeTemplateForm')}
                        className="max-w-xl"
                    >
                        {templateForm && <div className="p-6">
                            <form onSubmit={saveTemplate}>
                                <fieldset disabled={isTemplateListBusy} className="min-w-0 space-y-4">
                                {templateFormError && (
                                    <div className="rounded-md bg-feedback-danger-muted p-3 text-sm text-feedback-danger-foreground" role="alert">{templateFormError}</div>
                                )}
                                <Input
                                    label={t('surfaces.templateLabels.name')}
                                    value={templateForm.state.name}
                                    onChange={event => updateTemplateForm('name', event.target.value)}
                                    required
                                />
                                <div>
                                    <label htmlFor={templateTypeId} className="block text-sm font-medium text-content-primary mb-1">{t('surfaces.templateLabels.type')}</label>
                                    <select
                                        id={templateTypeId}
                                        value={templateForm.state.template_type}
                                        onChange={event => updateTemplateForm('template_type', event.target.value as TemplateType)}
                                        className="w-full rounded-md border border-border-strong bg-surface-card px-3 py-2 shadow-sm focus:outline-none focus:ring-1 focus:ring-focus"
                                    >
                                        {templateTypes.map(option => (
                                            <option key={option.value} value={option.value}>{t(option.labelKey)}</option>
                                        ))}
                                    </select>
                                </div>
                                <div>
                                    <label htmlFor={templateDescriptionId} className="block text-sm font-medium text-content-primary mb-1">{t('surfaces.templateLabels.description')}</label>
                                    <textarea
                                        id={templateDescriptionId}
                                        value={templateForm.state.description}
                                        onChange={event => updateTemplateForm('description', event.target.value)}
                                        className="min-h-[72px] w-full rounded-md border border-border-strong px-3 py-2 shadow-sm focus:outline-none focus:ring-1 focus:ring-focus"
                                    />
                                </div>
                                <Input
                                    label={t('surfaces.templateLabels.defaultTitle')}
                                    value={templateForm.state.default_title}
                                    onChange={event => updateTemplateForm('default_title', event.target.value)}
                                />
                                <div>
                                    <label htmlFor={templateDefaultDescriptionId} className="block text-sm font-medium text-content-primary mb-1">{t('surfaces.templateLabels.defaultDescription')}</label>
                                    <textarea
                                        id={templateDefaultDescriptionId}
                                        value={templateForm.state.default_description}
                                        onChange={event => updateTemplateForm('default_description', event.target.value)}
                                        className="min-h-[96px] w-full rounded-md border border-border-strong px-3 py-2 shadow-sm focus:outline-none focus:ring-1 focus:ring-focus"
                                    />
                                </div>
                                <div className="grid grid-cols-2 gap-3">
                                    <Input
                                        type="number"
                                        label={t('surfaces.templateLabels.priority')}
                                        min="1"
                                        max="10"
                                        value={templateForm.state.default_priority}
                                        onChange={event => updateTemplateForm('default_priority', event.target.value)}
                                    />
                                    <Input
                                        type="number"
                                        label={t('surfaces.templateLabels.effortDays')}
                                        min="0.1"
                                        step="0.1"
                                        value={templateForm.state.default_effort_days}
                                        onChange={event => updateTemplateForm('default_effort_days', event.target.value)}
                                    />
                                </div>
                                <LabelSelector
                                    value={templateForm.state.default_labels}
                                    onChange={labels => updateTemplateForm('default_labels', labels)}
                                    label={t('surfaces.templateLabels.defaultLabels')}
                                    placeholder={t('surfaces.templateLabels.addCustomDefault')}
                                />
                                <div>
                                    <label htmlFor={templateChecklistId} className="block text-sm font-medium text-content-primary mb-1">{t('surfaces.templateLabels.checklist')}</label>
                                    <textarea
                                        id={templateChecklistId}
                                        value={templateForm.state.default_checklist}
                                        onChange={event => updateTemplateForm('default_checklist', event.target.value)}
                                        placeholder={t('surfaces.templateLabels.oneItemPerLine')}
                                        className="min-h-[96px] w-full rounded-md border border-border-strong px-3 py-2 shadow-sm focus:outline-none focus:ring-1 focus:ring-focus"
                                    />
                                </div>
                                <div>
                                    <label htmlFor={templatePayloadId} className="block text-sm font-medium text-content-primary mb-1">{t('surfaces.templateLabels.defaultPayloadJSON')}</label>
                                    <textarea
                                        id={templatePayloadId}
                                        value={templateForm.state.default_payload}
                                        onChange={event => updateTemplateForm('default_payload', event.target.value)}
                                        className="min-h-[112px] w-full rounded-md border border-border-strong px-3 py-2 font-mono text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-focus"
                                    />
                                </div>
                                <div className="grid grid-cols-2 gap-3">
                                    <Input
                                        type="number"
                                        label={t('surfaces.templateLabels.sortOrder')}
                                        value={templateForm.state.sort_order}
                                        onChange={event => updateTemplateForm('sort_order', parseInt(event.target.value) || 0)}
                                    />
                                    <label className="flex items-end gap-2 pb-2 text-sm font-medium text-content-primary">
                                        <input
                                            type="checkbox"
                                            checked={templateForm.state.is_active}
                                            onChange={event => updateTemplateForm('is_active', event.target.checked)}
                                            className="h-4 w-4 rounded border-border-strong text-action focus:ring-focus"
                                        />
                                        {t('surfaces.templateLabels.active')}
                                    </label>
                                </div>
                                <Button type="submit" isLoading={saveTemplateMutation.isPending}>
                                    <Save className="mr-2 h-4 w-4" />
                                    {t('surfaces.templateLabels.saveTemplate')}
                                </Button>
                                </fieldset>
                            </form>
                        </div>}
                    </SlideOverDrawer>
                </section>
            )}

            {activeSection === 'labels' && (
                <section
                    id="template-labels-panel-labels"
                    role="tabpanel"
                    aria-labelledby="template-labels-tab-labels"
                    className="grid grid-cols-1 gap-6 xl:grid-cols-[minmax(0,1fr)_420px]"
                >
                    <section className="card space-y-4" aria-labelledby="label-taxonomy-heading">
                        <div className="flex flex-wrap items-center justify-between gap-3">
                            <div>
                                <h3 id="label-taxonomy-heading" className="text-lg font-semibold text-content-primary">{t('surfaces.templateLabels.labelTaxonomy')}</h3>
                                <p className="text-sm text-content-secondary">{t('surfaces.templateLabels.manageGovernedLabelsAndArchivedRows')}</p>
                            </div>
                            <div className="flex items-center gap-3">
                                <label className="flex items-center gap-2 text-sm text-content-secondary">
                                    <input
                                        type="checkbox"
                                        checked={includeArchivedLabels}
                                        onChange={event => setIncludeArchivedLabels(event.target.checked)}
                                        disabled={labelsLoading || isLabelsError || isLabelsBusy}
                                        className="h-4 w-4 rounded border-border-strong text-action focus:ring-focus"
                                    />
                                    {t('surfaces.templateLabels.includeArchived')}
                                </label>
                                <Button type="button" onClick={() => setGroupForm({ id: null, state: emptyGroupForm(nextSortOrder(labelGroups)) })} disabled={labelsLoading || isLabelsError || isLabelsBusy}>
                                    <Plus className="mr-2 h-4 w-4" />
                                    {t('surfaces.templateLabels.newGroup')}
                                </Button>
                            </div>
                        </div>

                        {labelsLoading ? (
                            <QueryLoadingState message={t('surfaces.templateLabels.loadingLabels')} />
                        ) : isLabelsError ? (
                            <QueryErrorState
                                error={labelsError}
                                fallback={t('queryFeedback.fallback')}
                                onRetry={() => { void refetchLabels(); }}
                                title={t('surfaces.templateLabels.labels')}
                            />
                        ) : labelGroups.length === 0 ? (
                            <QueryEmptyState title={t('surfaces.templateLabels.noLabelGroupsYet')} />
                        ) : (
                            <div className="space-y-4">
                                {labelGroups.map((group, groupIndex) => (
                                    <section
                                        key={group.id}
                                        className={`min-w-0 rounded-lg border bg-surface-card p-4 shadow-sm ${group.is_active ? 'border-border' : 'border-border opacity-70'}`}
                                        aria-labelledby={`label-group-${group.id}-heading`}
                                    >
                                        <div className="flex flex-wrap items-start justify-between gap-3">
                                            <div className="min-w-0">
                                                <div className="flex flex-wrap items-center gap-2">
                                                    <span aria-hidden="true" className="h-3 w-3 shrink-0 rounded-full" style={{ backgroundColor: group.color }} />
                                                    <h4 id={`label-group-${group.id}-heading`} className="min-w-0 font-medium text-content-primary">{labelGroupDisplay(group).name}</h4>
                                                    <span className="max-w-full break-all font-mono text-xs text-content-secondary">{group.key}</span>
                                                    {!group.is_active && (
                                                        <span className="rounded-full bg-surface-subtle px-2 py-0.5 text-xs font-medium text-content-secondary">{t('surfaces.templateLabels.archived')}</span>
                                                    )}
                                                    {group.seed_key && (
                                                        <span className="rounded-full bg-action-muted px-2 py-0.5 text-xs font-medium text-action">{t('surfaces.templateLabels.seeded')}</span>
                                                    )}
                                                </div>
                                                {labelGroupDisplay(group).description && (
                                                    <p className="mt-1 text-sm text-content-secondary">{labelGroupDisplay(group).description}</p>
                                                )}
                                            </div>
                                            <OverflowMenu
                                                label={t('surfaces.templateLabels.rowActions', { name: labelGroupDisplay(group).name })}
                                                items={[
                                                    { label: t('surfaces.templateLabels.editGroup'), icon: <Edit3 className="h-4 w-4" aria-hidden="true" />, onSelect: () => setGroupForm({ id: group.id, state: groupToForm(group) }), disabled: isGroupListBusy },
                                                    { label: t('surfaces.templateLabels.moveUp'), icon: <ChevronUp className="h-4 w-4" aria-hidden="true" />, onSelect: () => moveGroup(group, -1), disabled: groupIndex === 0 || isGroupListBusy },
                                                    { label: t('surfaces.templateLabels.moveDown'), icon: <ChevronDown className="h-4 w-4" aria-hidden="true" />, onSelect: () => moveGroup(group, 1), disabled: groupIndex === labelGroups.length - 1 || isGroupListBusy },
                                                    { label: group.is_active ? t('surfaces.templateLabels.archiveGroup') : t('surfaces.templateLabels.restoreGroup'), icon: <Archive className="h-4 w-4" aria-hidden="true" />,
                                                        onSelect: () => toggleGroupMutation.mutate({ id: group.id, isActive: !group.is_active, name: labelGroupDisplay(group).name }), disabled: isGroupListBusy },
                                                ]}
                                            />
                                        </div>

                                        <div className="mt-4 space-y-2">
                                            {group.labels.length === 0 ? (
                                                <p className="rounded-md bg-surface-muted px-3 py-2 text-sm text-content-secondary">{t('surfaces.templateLabels.noLabelsInThisGroup')}</p>
                                            ) : (
                                                group.labels.map((label, labelIndex) => (
                                                    <article
                                                        key={label.id}
                                                        className={`flex flex-wrap items-center justify-between gap-2 rounded-md border border-border-subtle px-3 py-2 ${
                                                            label.is_active ? 'bg-surface-card' : 'bg-surface-muted opacity-70'
                                                        }`}
                                                        aria-labelledby={`label-${label.id}-name`}
                                                    >
                                                        <div className="flex min-w-0 flex-1 flex-wrap items-center gap-2">
                                                            <span aria-hidden="true" className="h-3 w-3 shrink-0 rounded-full" style={{ backgroundColor: label.color }} />
                                                            <span id={`label-${label.id}-name`} className="min-w-0 break-words font-medium text-content-primary">{labelDisplay(label).name}</span>
                                                            <span className="max-w-full break-all font-mono text-xs text-content-secondary">{label.slug}</span>
                                                            {!label.is_active && (
                                                                <span className="rounded-full bg-surface-subtle px-2 py-0.5 text-xs font-medium text-content-secondary">{t('surfaces.templateLabels.archived')}</span>
                                                            )}
                                                        </div>
                                                        <OverflowMenu
                                                            label={t('surfaces.templateLabels.rowActions', { name: labelDisplay(label).name })}
                                                            items={[
                                                                { label: t('surfaces.templateLabels.editLabel'), icon: <Edit3 className="h-4 w-4" aria-hidden="true" />, onSelect: () => setLabelForm({ id: label.id, state: labelToForm(label) }), disabled: isLabelListBusy },
                                                                { label: t('surfaces.templateLabels.moveUp'), icon: <ChevronUp className="h-4 w-4" aria-hidden="true" />, onSelect: () => moveLabel(group, label, -1), disabled: labelIndex === 0 || isLabelListBusy },
                                                                { label: t('surfaces.templateLabels.moveDown'), icon: <ChevronDown className="h-4 w-4" aria-hidden="true" />, onSelect: () => moveLabel(group, label, 1), disabled: labelIndex === group.labels.length - 1 || isLabelListBusy },
                                                                { label: label.is_active ? t('surfaces.templateLabels.archiveLabel') : t('surfaces.templateLabels.restoreLabel'), icon: <Archive className="h-4 w-4" aria-hidden="true" />,
                                                                    onSelect: () => toggleLabelMutation.mutate({ id: label.id, isActive: !label.is_active, name: labelDisplay(label).name }), disabled: isLabelListBusy },
                                                            ]}
                                                        />
                                                    </article>
                                                ))
                                            )}
                                            <Button type="button" variant="outline" size="sm" onClick={() => setLabelForm({ id: null, state: emptyLabelForm(group) })} disabled={isLabelListBusy}>
                                                <Plus className="mr-2 h-4 w-4" />
                                                {t('surfaces.templateLabels.addLabel')}
                                            </Button>
                                        </div>
                                    </section>
                                ))}
                            </div>
                        )}
                    </section>

                    <section
                        className="card h-fit space-y-6"
                        aria-labelledby="group-editor-heading label-editor-heading"
                    >
                        <div className="space-y-4">
                            <div className="flex items-center justify-between">
                                <h3 id="group-editor-heading" className="text-lg font-semibold text-content-primary">
                                    {groupForm?.id ? t('surfaces.templateLabels.editGroup') : t('surfaces.templateLabels.groupDetails')}
                                </h3>
                                {groupForm && (
                                    <button
                                        type="button"
                                        onClick={() => setGroupForm(null)}
                                        disabled={isLabelsBusy}
                                        className="rounded-md p-1 text-content-tertiary hover:bg-surface-subtle hover:text-content-primary disabled:cursor-not-allowed disabled:opacity-60"
                                        aria-label={t('surfaces.templateLabels.closeGroupForm')} title={t('surfaces.templateLabels.closeGroupForm')}
                                    >
                                        <X aria-hidden="true" className="h-4 w-4" />
                                    </button>
                                )}
                            </div>
                            {!groupForm ? (
                                <p className="text-sm text-content-secondary">{t('surfaces.templateLabels.selectAGroupOrCreateANewOne')}</p>
                            ) : (
                                <form
                                    onSubmit={event => {
                                        event.preventDefault();
                                        if (isLabelsBusy) return;
                                        saveGroupMutation.mutate({
                                            id: groupForm.id,
                                            data: formToGroupPayload(groupForm.state),
                                        });
                                    }}
                                >
                                    <fieldset disabled={isLabelsBusy} className="min-w-0 space-y-4">
                                    <Input label={t('surfaces.templateLabels.key')} value={groupForm.state.key} onChange={event => updateGroupForm('key', event.target.value)} required />
                                    <Input label={t('surfaces.templateLabels.name')} value={groupForm.state.name} onChange={event => updateGroupForm('name', event.target.value)} required />
                                    <div>
                                        <label htmlFor={groupDescriptionId} className="block text-sm font-medium text-content-primary mb-1">{t('surfaces.templateLabels.description')}</label>
                                        <textarea
                                            id={groupDescriptionId}
                                            value={groupForm.state.description}
                                            onChange={event => updateGroupForm('description', event.target.value)}
                                            className="min-h-[72px] w-full rounded-md border border-border-strong px-3 py-2 shadow-sm focus:outline-none focus:ring-1 focus:ring-focus"
                                        />
                                    </div>
                                    <div className="grid grid-cols-[48px_minmax(0,1fr)] gap-3">
                                        <input
                                            type="color"
                                            value={groupForm.state.color}
                                            onChange={event => updateGroupForm('color', event.target.value)}
                                            className="h-10 w-12 rounded-md border border-border-strong bg-surface-card p-1"
                                            aria-label={t('surfaces.templateLabels.groupColor')}
                                        />
                                        <Input label={t('surfaces.templateLabels.color')} value={groupForm.state.color} onChange={event => updateGroupForm('color', event.target.value)} />
                                    </div>
                                    <div className="grid grid-cols-2 gap-3">
                                        <Input
                                            type="number"
                                            label={t('surfaces.templateLabels.sortOrder')}
                                            value={groupForm.state.sort_order}
                                            onChange={event => updateGroupForm('sort_order', parseInt(event.target.value) || 0)}
                                        />
                                        <label className="flex items-end gap-2 pb-2 text-sm font-medium text-content-primary">
                                            <input
                                                type="checkbox"
                                                checked={groupForm.state.is_active}
                                                onChange={event => updateGroupForm('is_active', event.target.checked)}
                                                className="h-4 w-4 rounded border-border-strong text-action focus:ring-focus"
                                            />
                                            {t('surfaces.templateLabels.active')}
                                        </label>
                                    </div>
                                    <Button type="submit" isLoading={saveGroupMutation.isPending}>
                                        <Save aria-hidden="true" className="mr-2 h-4 w-4" />
                                        {t('surfaces.templateLabels.saveGroup')}
                                    </Button>
                                    </fieldset>
                                </form>
                            )}
                        </div>

                        <div className="border-t border-border pt-6">
                            <div className="mb-4 flex items-center justify-between">
                                <h3 id="label-editor-heading" className="text-lg font-semibold text-content-primary">
                                    {labelForm?.id ? t('surfaces.templateLabels.editLabel') : t('surfaces.templateLabels.labelDetails')}
                                </h3>
                                {labelForm && (
                                    <button
                                        type="button"
                                        onClick={() => setLabelForm(null)}
                                        disabled={isLabelsBusy}
                                        className="rounded-md p-1 text-content-tertiary hover:bg-surface-subtle hover:text-content-primary disabled:cursor-not-allowed disabled:opacity-60"
                                        aria-label={t('surfaces.templateLabels.closeLabelForm')} title={t('surfaces.templateLabels.closeLabelForm')}
                                    >
                                        <X aria-hidden="true" className="h-4 w-4" />
                                    </button>
                                )}
                            </div>
                            {!labelForm ? (
                                <p className="text-sm text-content-secondary">{t('surfaces.templateLabels.selectALabelOrAddOneFromAGroup')}</p>
                            ) : (
                                <form
                                    onSubmit={event => {
                                        event.preventDefault();
                                        if (isLabelsBusy) return;
                                        saveLabelMutation.mutate({
                                            id: labelForm.id,
                                            data: formToLabelPayload(labelForm.state),
                                        });
                                    }}
                                >
                                    <fieldset disabled={isLabelsBusy} className="min-w-0 space-y-4">
                                    <div>
                                        <label htmlFor={labelGroupId} className="block text-sm font-medium text-content-primary mb-1">
                                            {t('surfaces.templateLabels.group')}
                                            <RequiredIndicator />
                                        </label>
                                        <select
                                            id={labelGroupId}
                                            aria-label={t('surfaces.templateLabels.group')}
                                            value={labelForm.state.group_id}
                                            onChange={event => updateLabelForm('group_id', event.target.value)}
                                            className="w-full rounded-md border border-border-strong bg-surface-card px-3 py-2 shadow-sm focus:outline-none focus:ring-1 focus:ring-focus"
                                            required
                                        >
                                            {labelGroups.map(group => (
                                                <option key={group.id} value={group.id}>{labelGroupDisplay(group).name}</option>
                                            ))}
                                        </select>
                                    </div>
                                    <Input label={t('surfaces.templateLabels.slug')} value={labelForm.state.slug} onChange={event => updateLabelForm('slug', event.target.value)} required />
                                    <Input label={t('surfaces.templateLabels.name')} value={labelForm.state.name} onChange={event => updateLabelForm('name', event.target.value)} required />
                                    <div>
                                        <label htmlFor={labelDescriptionId} className="block text-sm font-medium text-content-primary mb-1">{t('surfaces.templateLabels.description')}</label>
                                        <textarea
                                            id={labelDescriptionId}
                                            value={labelForm.state.description}
                                            onChange={event => updateLabelForm('description', event.target.value)}
                                            className="min-h-[72px] w-full rounded-md border border-border-strong px-3 py-2 shadow-sm focus:outline-none focus:ring-1 focus:ring-focus"
                                        />
                                    </div>
                                    <div className="grid grid-cols-[48px_minmax(0,1fr)] gap-3">
                                        <input
                                            type="color"
                                            value={labelForm.state.color}
                                            onChange={event => updateLabelForm('color', event.target.value)}
                                            className="h-10 w-12 rounded-md border border-border-strong bg-surface-card p-1"
                                            aria-label={t('surfaces.templateLabels.labelColor')}
                                        />
                                        <Input label={t('surfaces.templateLabels.color')} value={labelForm.state.color} onChange={event => updateLabelForm('color', event.target.value)} />
                                    </div>
                                    <div className="grid grid-cols-2 gap-3">
                                        <Input
                                            type="number"
                                            label={t('surfaces.templateLabels.sortOrder')}
                                            value={labelForm.state.sort_order}
                                            onChange={event => updateLabelForm('sort_order', parseInt(event.target.value) || 0)}
                                        />
                                        <label className="flex items-end gap-2 pb-2 text-sm font-medium text-content-primary">
                                            <input
                                                type="checkbox"
                                                checked={labelForm.state.is_active}
                                                onChange={event => updateLabelForm('is_active', event.target.checked)}
                                                className="h-4 w-4 rounded border-border-strong text-action focus:ring-focus"
                                            />
                                            {t('surfaces.templateLabels.active')}
                                        </label>
                                    </div>
                                    <Button type="submit" isLoading={saveLabelMutation.isPending}>
                                        <Save aria-hidden="true" className="mr-2 h-4 w-4" />
                                        {t('surfaces.templateLabels.saveLabel')}
                                    </Button>
                                    </fieldset>
                                </form>
                            )}
                        </div>
                    </section>
                </section>
            )}
        </div>
    );
};

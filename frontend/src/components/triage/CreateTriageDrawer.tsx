import { useQuery } from '@tanstack/react-query';
import {
    AlertCircle,
    Plus
} from 'lucide-react';
import type { FormEvent } from 'react';
import { useState } from 'react';
import { templateDisplay } from '../../i18n/seedDisplay';
import { templateService } from '../../services/templateService';
import type { Iteration } from '../../types/iteration';
import type { Project } from '../../types/project';
import type { WorkTemplate } from '../../types/template';
import type {
    TriageItemCreate
} from '../../types/triage';
import {
    appendChecklistToDescription,
    getPayloadString,
    mergeLabels,
} from '../../utils/templateDefaults';
import { Button } from '../common/Button';
import { Input } from '../common/Input';
import { Select } from '../common/Select';
import { Textarea } from '../common/Textarea';
import { QueryErrorState } from '../feedback/QueryState';
import { LabelSelector } from '../labels/LabelSelector';

import { SlideOverDrawer } from '../ui/SlideOverDrawer';
import { optionalText, parseOptionalNumber, t } from './triageUtils';
interface CreateTriageDrawerProps {
    projects: Project[];
    iterations: Iteration[];
    isSubmitting: boolean;
    error?: string | null;
    /** Named refusal of the source link, shown beside that field. */
    sourceUrlError?: string | null;
    onSubmit: (payload: TriageItemCreate) => void;
    onClose: () => void;
    /** A title carried over from quick capture. */
    initialTitle?: string;
}

export const CreateTriageDrawer = ({ projects, iterations, isSubmitting, error, sourceUrlError, onSubmit, onClose, initialTitle = '' }: CreateTriageDrawerProps) => {
    const [title, setTitle] = useState(initialTitle);
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

    // feedback-policy: query loading,error,retry,empty - manual entry remains available without templates; errors offer retry.
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
        <SlideOverDrawer open className="max-w-2xl" title={t('surfaces.triagePage.newIntake')} onClose={onClose}>
            <form onSubmit={handleSubmit} className="space-y-4 p-6">
                {templatesError && (
                    <QueryErrorState
                        error={templatesError}
                        fallback={t('queryFeedback.optionLoadFailed')}
                        onRetry={() => void refetchTemplates()}
                    />
                )}
                {error && (
                    <div className="flex items-start gap-2 rounded-md bg-feedback-danger-muted p-3 text-sm text-feedback-danger-foreground">
                        <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" />
                        <span>{error}</span>
                    </div>
                )}

                {triageTemplates.length > 0 && (
                    <Select label={t('surfaces.triagePage.template')} value={selectedTemplateId} onChange={event => handleTemplateSelect(event.target.value)}><option value="">{t('surfaces.triagePage.noTemplate')}</option>{triageTemplates.map(template => (
                        <option key={template.id} value={template.id}>
                            {templateDisplay(template).name}
                        </option>
                    ))}</Select>
                )}

                <Input
                    label={t('surfaces.triagePage.title')}
                    value={title}
                    onChange={event => setTitle(event.target.value)}
                    required
                    maxLength={255}
                />

                <Textarea label={t('surfaces.triagePage.description')} value={description} onChange={event => setDescription(event.target.value)} className="min-h-[110px]" />

                <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
                    <Input label={t('surfaces.triagePage.source')} value={source} onChange={event => setSource(event.target.value)} maxLength={100} />
                    <Input label={t('surfaces.triagePage.externalKey')} value={externalKey} onChange={event => setExternalKey(event.target.value)} maxLength={255} />
                    <Input label={t('surfaces.triagePage.priorityHint')} type="number" min="1" max="10" value={priorityHint} onChange={event => setPriorityHint(event.target.value)} />
                </div>

                <Input label={t('surfaces.triagePage.sourceURL')} type="url" error={sourceUrlError ?? undefined} value={sourceUrl} onChange={event => setSourceUrl(event.target.value)} maxLength={500} />

                <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
                    <Input label={t('surfaces.triagePage.assigneeHint')} value={assigneeHint} onChange={event => setAssigneeHint(event.target.value)} maxLength={255} />
                    <Select label={t('surfaces.triagePage.projectHint')} value={projectHintId} onChange={event => setProjectHintId(event.target.value)}><option value="">{t('surfaces.triagePage.noProject')}</option>{projects.map(project => (
                        <option key={project.id} value={project.id}>{project.name}</option>
                    ))}</Select>
                    <Select label={t('surfaces.triagePage.iterationHint')} value={iterationHintId} onChange={event => setIterationHintId(event.target.value)}><option value="">{t('surfaces.triagePage.noIteration')}</option>{iterations.map(iteration => (
                        <option key={iteration.id} value={iteration.id}>{iteration.name}</option>
                    ))}</Select>
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
        </SlideOverDrawer>
    );
};


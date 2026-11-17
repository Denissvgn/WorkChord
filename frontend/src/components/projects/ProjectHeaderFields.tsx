import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { Pencil } from 'lucide-react';
import { useState, type ReactNode } from 'react';
import { useTranslation } from 'react-i18next';
import type { ObservedPlanningInput } from '../../services/planningInputService';
import { projectService } from '../../services/projectService';
import { teamService } from '../../services/teamService';
import type { Project, ProjectUpdate } from '../../types/project';
import { getApiErrorMessage, getApiErrorStatus } from '../../utils/apiError';
import { formatDate } from '../../utils/formatDate';
import { formatPortfolioOwnerLabel, formatTeamMemberProfileLabel } from '../../utils/teamMemberLabels';
import { Button } from '../common/Button';
import { QueryErrorState } from '../feedback/QueryState';
import { PlanningInputBoundary } from '../planning/PlanningInputBoundary';
import { healthLabelKeys, projectStatusLabelKeys } from './projectDetailShared';

import { Select } from '../../components/common/Select';
type Field = 'status' | 'health' | 'dates' | 'owner';
const inputClass = 'rounded-md border border-border-strong bg-surface-card px-2 py-1.5 text-sm text-content-primary';

const HeaderFieldEditor = ({ field, observed, controls, onClose }: {
    field: Field; observed: ObservedPlanningInput<Project>; controls: ReactNode; onClose: () => void;
}) => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const project = observed.resource;
    const [draft, setDraft] = useState<ProjectUpdate>(() => field === 'dates'
        ? { start_date: project.start_date?.slice(0, 10) ?? null, target_date: project.target_date?.slice(0, 10) ?? null }
        : field === 'owner' ? { owner_profile_id: project.owner_profile_id, owner_id: null }
            : { [field]: project[field] });
    // feedback-policy: query loading,error,retry,empty - owner loading disables save; errors offer retry and an empty list allows unassigned.
    const owners = useQuery({ queryKey: ['teamMemberProfiles'], queryFn: teamService.getProfiles, enabled: field === 'owner' });
    // feedback-policy: mutation pending,inline - disable the editor during save; retain failed drafts and expose revision conflict recovery.
    const save = useMutation({
        mutationFn: () => projectService.update(project.id, draft, observed.expected_revisions),
        onSuccess: updated => {
            queryClient.setQueryData(['project', project.id], updated);
            for(const queryKey of [['projects'], ['projectSummary', project.id], ['gantt'], ['projectTasks', project.id]]) {
                void queryClient.invalidateQueries({ queryKey });
            }
            onClose();
        },
    });
    const conflict = [409, 412].includes(getApiErrorStatus(save.error) ?? 0);
    return <form onSubmit={event => { event.preventDefault(); if(!save.isPending) save.mutate(); }} className="space-y-2">
        <fieldset disabled={save.isPending} className="m-0 flex min-w-0 flex-wrap items-end gap-2 border-0 p-0">
            {field === 'dates' ? <>{(['start_date', 'target_date'] as const).map(key => <label key={key} className="flex flex-col gap-1 text-sm">
                {t(key === 'start_date' ? 'surfaces.projectForm.startDate' : 'surfaces.projectForm.targetDate')}
                <input type="date" className={inputClass} value={draft[key] ?? ''} onChange={event => setDraft({ ...draft, [key]: event.target.value || null })} />
            </label>)}</> : field === 'owner' ? <label className="flex flex-col gap-1 text-sm">
                {t('surfaces.projectForm.owner')}
                <Select className={inputClass} value={draft.owner_profile_id ?? ''} onChange={event => setDraft({ owner_id: null, owner_profile_id: event.target.value ? Number(event.target.value) : null })} disabled={owners.isLoading || owners.isError}>
                    <option value="">{t('surfaces.projectForm.unassigned')}</option>
                    {project.owner_profile && !owners.data?.some(owner => owner.id === project.owner_profile_id) && <option value={project.owner_profile.id}>{formatTeamMemberProfileLabel(project.owner_profile)}</option>}
                    {owners.data?.map(owner => <option key={owner.id} value={owner.id}>{formatTeamMemberProfileLabel(owner)}</option>)}
                </Select>
            </label> : <label className="flex flex-col gap-1 text-sm">
                {t(`surfaces.projectForm.${field}`)}
                <Select className={inputClass} value={draft[field]} onChange={event => setDraft({ [field]: event.target.value })}>
                    {Object.entries(field === 'status' ? projectStatusLabelKeys : healthLabelKeys).map(([value, label]) => <option key={value} value={value}>{t(label)}</option>)}
                </Select>
            </label>}
            <Button type="submit" size="sm" variant="secondary" isLoading={save.isPending} disabled={field === 'owner' && (owners.isLoading || owners.isError)}>{t('actions.save')}</Button>
            <Button type="button" size="sm" variant="ghost" onClick={onClose}>{t('actions.cancel')}</Button>
        </fieldset>
        {field === 'owner' && owners.isLoading && <p role="status">{t('common.loading')}</p>}
        {owners.error && <QueryErrorState error={owners.error} onRetry={() => void owners.refetch()} />}
        {save.error && <p role="alert" className="text-sm text-feedback-danger-foreground">{getApiErrorMessage(save.error, t('surfaces.projectForm.updateFailed'))}</p>}
        {conflict && controls}
    </form>;
};

export const ProjectHeaderFields = ({ project }: { project: Project }) => {
    const { t } = useTranslation();
    const [editing, setEditing] = useState<Field | null>(null);
    const values: Record<Field, string> = {
        status: t(projectStatusLabelKeys[project.status]),
        health: t(healthLabelKeys[project.health]),
        dates: `${formatDate(project.start_date)} – ${formatDate(project.target_date)}`,
        owner: formatPortfolioOwnerLabel(project.owner_profile, project.owner, project.owner_id, t('surfaces.projectForm.unassigned')),
    };
    return <dl className="flex w-full flex-wrap gap-x-6 gap-y-3">
        {(Object.keys(values) as Field[]).map(field => <div key={field} className="min-w-0">
            <dt className="mb-1 text-xs font-medium text-content-secondary">{t(`projectTabs.${field}Label`)}</dt>
            <dd>{editing === field ? <PlanningInputBoundary<Project> kind="project" resourceId={project.id} onCancel={() => setEditing(null)}>
                {(observed, controls) => <HeaderFieldEditor field={field} observed={observed} controls={controls} onClose={() => setEditing(null)} />}
            </PlanningInputBoundary> : <Button type="button" className="inline-flex items-center gap-2 rounded px-1 py-1 text-sm text-content-primary hover:bg-surface-muted focus-visible:outline focus-visible:outline-2 focus-visible:outline-action"
                aria-label={t('projectTabs.editField', { field: t(`projectTabs.${field}Label`), value: values[field] })}
                onClick={() => setEditing(field)} variant="secondary">{values[field]}<Pencil className="h-3 w-3 text-content-tertiary" aria-hidden="true" /></Button>}</dd>
        </div>)}
    </dl>;
};

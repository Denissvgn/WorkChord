import { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { Save } from 'lucide-react';
import { Button } from '../common/Button';
import { Input } from '../common/Input';
import { CollapsibleSection } from '../common/CollapsibleSection';
import { projectService } from '../../services/projectService';
import { teamService } from '../../services/teamService';
import { getApiErrorMessage } from '../../utils/apiError';
import { formatTeamMemberProfileLabel } from '../../utils/teamMemberLabels';
import { QueryErrorState, QueryLoadingState } from '../feedback/QueryState';
import type { Initiative, InitiativeCreate, ProjectHealth } from '../../types/project';

interface InitiativeFormProps {
    initialData?: Initiative;
    onSuccess: (initiative: Initiative) => void;
    onCancel: () => void;
}

type InitiativeFormState = InitiativeCreate;

const healthOptions: { value: ProjectHealth; labelKey: string }[] = [
    { value: 'unknown', labelKey: 'surfaces.initiativeForm.healths.unknown' },
    { value: 'on_track', labelKey: 'surfaces.initiativeForm.healths.onTrack' },
    { value: 'at_risk', labelKey: 'surfaces.initiativeForm.healths.atRisk' },
    { value: 'off_track', labelKey: 'surfaces.initiativeForm.healths.offTrack' },
];

const dateValue = (value?: string | null) => value?.slice(0, 10) || '';

export const InitiativeForm = ({ initialData, onSuccess, onCancel }: InitiativeFormProps) => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const [error, setError] = useState<string | null>(null);
    const [formData, setFormData] = useState<InitiativeFormState>({
        name: initialData?.name || '',
        description: initialData?.description || '',
        owner_id: null,
        owner_profile_id: initialData?.owner_profile_id ?? null,
        health: initialData?.health || 'unknown',
        target_date: dateValue(initialData?.target_date) || null,
    });

    const ownerOptionsQuery = useQuery({
        queryKey: ['teamMemberProfiles'],
        queryFn: teamService.getProfiles,
    });
    const ownerOptions = ownerOptionsQuery.data ?? [];

    const selectedOwnerMissing = Boolean(
        formData.owner_profile_id &&
        !ownerOptions.some(owner => owner.id === formData.owner_profile_id),
    );

    const invalidateInitiativeQueries = () => {
        queryClient.invalidateQueries({ queryKey: ['initiatives'] });
        queryClient.invalidateQueries({ queryKey: ['projects'] });
    };

    const createMutation = useMutation({
        mutationFn: (data: InitiativeCreate) => projectService.createInitiative(data),
        onSuccess: initiative => {
            invalidateInitiativeQueries();
            onSuccess(initiative);
        },
        onError: (err: unknown) => {
            setError(getApiErrorMessage(err, t('surfaces.initiativeForm.createFailed')));
        },
    });

    const updateMutation = useMutation({
        mutationFn: (data: InitiativeFormState) => projectService.updateInitiative(initialData!.id, data),
        onSuccess: initiative => {
            invalidateInitiativeQueries();
            onSuccess(initiative);
        },
        onError: (err: unknown) => {
            setError(getApiErrorMessage(err, t('surfaces.initiativeForm.updateFailed')));
        },
    });

    const normalizePayload = () => ({
        name: formData.name.trim(),
        description: formData.description?.trim() || null,
        owner_profile_id: formData.owner_profile_id ?? null,
        health: formData.health,
        target_date: formData.target_date || null,
    });

    const handleSubmit = (event: React.FormEvent) => {
        event.preventDefault();
        setError(null);

        const payload = normalizePayload();
        if (initialData) {
            updateMutation.mutate(payload);
        }
        else {
            createMutation.mutate(payload);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-5">
            {ownerOptionsQuery.isLoading && <QueryLoadingState />}
            {ownerOptionsQuery.isError && (
                <QueryErrorState
                    error={ownerOptionsQuery.error}
                    fallback={t('queryFeedback.optionLoadFailed')}
                    onRetry={() => void ownerOptionsQuery.refetch()}
                />
            )}
            {error && (
                <div className="rounded-md bg-feedback-danger-muted p-3 text-sm text-feedback-danger-foreground">
                    {error}
                </div>
            )}

            <Input
                label={t('surfaces.initiativeForm.initiativeName')}
                value={formData.name}
                onChange={event => setFormData({ ...formData, name: event.target.value })}
                required
            />

            <div>
                <label className="mb-1 block text-sm font-medium text-content-primary">{t('surfaces.initiativeForm.description')}</label>
                <textarea
                    value={formData.description || ''}
                    onChange={event => setFormData({ ...formData, description: event.target.value })}
                    className="min-h-[96px] w-full rounded-md border border-border-strong px-3 py-2 shadow-sm focus:outline-none focus:ring-1 focus:ring-focus"
                />
            </div>

            <div>
                <label className="mb-1 block text-sm font-medium text-content-primary">{t('surfaces.initiativeForm.health')}</label>
                <select
                    value={formData.health}
                    onChange={event => setFormData({ ...formData, health: event.target.value as ProjectHealth })}
                    className="w-full rounded-md border border-border-strong bg-surface-card px-3 py-2 shadow-sm focus:outline-none focus:ring-1 focus:ring-focus"
                >
                    {healthOptions.map(option => (
                        <option key={option.value} value={option.value}>{t(option.labelKey)}</option>
                    ))}
                </select>
            </div>

            {/* Collapsible: Details */}
            <CollapsibleSection title={t('taskForm.advancedOptions')}>
                <div className="grid gap-4 md:grid-cols-2">
                    <div>
                        <label className="mb-1 block text-sm font-medium text-content-primary">{t('surfaces.initiativeForm.owner')}</label>
                        <select
                            value={formData.owner_profile_id ?? ''}
                            onChange={event => setFormData({
                                ...formData,
                                owner_id: null,
                                owner_profile_id: event.target.value ? parseInt(event.target.value) : null,
                            })}
                            className="w-full rounded-md border border-border-strong bg-surface-card px-3 py-2 shadow-sm focus:outline-none focus:ring-1 focus:ring-focus"
                            disabled={ownerOptionsQuery.isLoading || ownerOptionsQuery.isError}
                        >
                            <option value="">{t('surfaces.initiativeForm.unassigned')}</option>
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

                    <Input
                        type="date"
                        label={t('surfaces.initiativeForm.targetDate')}
                        value={formData.target_date || ''}
                        onChange={event => setFormData({ ...formData, target_date: event.target.value || null })}
                    />
                </div>
            </CollapsibleSection>

            <div className="flex justify-end gap-2 border-t pt-4">
                <Button type="button" variant="ghost" onClick={onCancel}>
                    {t('surfaces.initiativeForm.cancel')}
                </Button>
                <Button
                    type="submit"
                    isLoading={createMutation.isPending || updateMutation.isPending}
                    disabled={!formData.name.trim() || ownerOptionsQuery.isLoading || ownerOptionsQuery.isError}
                >
                    <Save className="mr-2 h-4 w-4" />
                    {initialData ? t('surfaces.initiativeForm.updateInitiative') : t('surfaces.initiativeForm.createInitiative')}
                </Button>
            </div>
        </form>
    );
};

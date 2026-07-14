import { useState } from 'react';
import { useMutation, useQueryClient, useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { Save } from 'lucide-react';
import { Button } from '../common/Button';
import { Input } from '../common/Input';
import { CollapsibleSection } from '../common/CollapsibleSection';
import { teamService } from '../../services/teamService';
import { getApiErrorMessage } from '../../utils/apiError';
import type { TeamMember, TeamMemberCreate, TeamMemberProfile } from '../../types/team';
import { QueryErrorState, QueryLoadingState } from '../feedback/QueryState';

interface TeamFormProps {
    iterationId: number;
    initialData?: TeamMember;
    initialProfile?: TeamMemberProfile;
    onSuccess: () => void;
    onCancel: () => void;
}

export const TeamForm = ({ iterationId, initialData, initialProfile, onSuccess, onCancel }: TeamFormProps) => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const [error, setError] = useState<string | null>(null);
    const [formData, setFormData] = useState<TeamMemberCreate>(
        initialData ? {
            name: initialData.profile?.display_name ?? initialData.name,
            position: initialData.position,
            email: initialData.profile?.email || initialData.email || '',
            profile_id: initialData.profile_id ?? null,
            availability_percent: initialData.availability_percent,
            professionalism_coefficient: initialData.professionalism_coefficient,
            operational_utilization: initialData.operational_utilization,
        } : initialProfile ? {
            name: initialProfile.display_name,
            position: initialProfile.headline || t('teamCapacity.defaultRole'),
            email: initialProfile.email || '',
            profile_id: initialProfile.id,
            availability_percent: 100,
            professionalism_coefficient: 1.0,
            operational_utilization: 20,
        } : {
            name: '',
            position: t('teamCapacity.defaultRole'),
            email: '',
            profile_id: null,
            availability_percent: 100,
            professionalism_coefficient: 1.0,
            operational_utilization: 20,
        }
    );

    const profilesQuery = useQuery({
        queryKey: ['teamMemberProfiles'],
        queryFn: teamService.getProfiles,
    });
    const profiles = profilesQuery.data ?? [];
    const isLoadingProfiles = profilesQuery.isLoading;
    const initialDataProfile = initialData?.profile ?? null;
    const selectedProfile = profiles.find(profile => profile.id === formData.profile_id)
        ?? (initialProfile?.id === formData.profile_id ? initialProfile : null)
        ?? (initialDataProfile?.id === formData.profile_id ? initialDataProfile : null);
    const hasLinkedProfile = formData.profile_id !== null && formData.profile_id !== undefined;

    const createMutation = useMutation({
        mutationFn: (data: TeamMemberCreate) => teamService.create(iterationId, data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['team', iterationId] });
            queryClient.invalidateQueries({ queryKey: ['teamMemberProfiles'] });
            queryClient.invalidateQueries({ queryKey: ['workload'] });
            queryClient.invalidateQueries({ queryKey: ['gantt'] });
            onSuccess();
        },
        onError: (err: unknown) => {
            setError(getApiErrorMessage(err, t('teamCapacity.failedCreateMember')));
        }
    });

    const updateMutation = useMutation({
        mutationFn: (data: TeamMemberCreate) => teamService.update(initialData!.id, data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['team', iterationId] });
            queryClient.invalidateQueries({ queryKey: ['workload'] });
            queryClient.invalidateQueries({ queryKey: ['gantt'] });
            onSuccess();
        },
        onError: (err: unknown) => {
            setError(getApiErrorMessage(err, t('teamCapacity.failedUpdateMember')));
        }
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);
        const payload = selectedProfile
            ? {
                ...formData,
                name: selectedProfile.display_name,
                email: selectedProfile.email || '',
                profile_id: selectedProfile.id,
            }
            : formData;
        if (initialData) {
            updateMutation.mutate(payload);
        } else {
            createMutation.mutate(payload);
        }
    };

    const handleProfileChange = (profileId: number | null) => {
        const profile = profiles.find(candidate => candidate.id === profileId) ?? null;
        setFormData(prev => ({
            ...prev,
            profile_id: profileId,
            name: profile ? profile.display_name : prev.name,
            email: profile ? profile.email || '' : prev.email,
            position: profile && (!prev.position || prev.position === t('teamCapacity.defaultRole'))
                ? profile.headline || t('teamCapacity.defaultRole')
                : prev.position,
        }));
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-6">
            {profilesQuery.isLoading && <QueryLoadingState />}
            {profilesQuery.isError && (
                <QueryErrorState
                    error={profilesQuery.error}
                    fallback={t('queryFeedback.optionLoadFailed')}
                    onRetry={() => void profilesQuery.refetch()}
                />
            )}
            {error && (
                <div className="bg-feedback-danger-muted text-feedback-danger-foreground p-3 rounded-md text-sm">
                    {error}
                </div>
            )}

            <div className="rounded-md border border-action bg-action-muted p-3 text-sm text-action">
                {t('teamCapacity.intro')}
            </div>

            <div>
                <label className="block text-sm font-medium text-content-primary mb-1">{t('teamCapacity.globalProfile')}</label>
                <select
                    aria-label={t('teamCapacity.globalProfile')}
                    value={formData.profile_id ?? ''}
                    onChange={event => handleProfileChange(event.target.value ? Number(event.target.value) : null)}
                    className="w-full rounded-md border border-border-strong bg-surface-card px-3 py-2 shadow-sm focus:outline-none focus:ring-1 focus:ring-focus"
                >
                    <option value="">{t('teamCapacity.selectProfile')}</option>
                    {profiles.map(profile => (
                        <option key={profile.id} value={profile.id}>
                            {profile.display_name}
                            {profile.headline ? ` - ${profile.headline}` : ''}
                        </option>
                    ))}
                </select>
                <p className="mt-1 text-xs text-content-secondary">
                    {t('teamCapacity.profileHelp')}
                </p>
                {!isLoadingProfiles && profiles.length === 0 && !initialData && (
                    <p className="mt-2 rounded-md border border-feedback-warning-border bg-feedback-warning-muted px-3 py-2 text-xs text-feedback-warning-foreground">
                        {t('teamCapacity.noProfilesCreateFromDetails')}
                    </p>
                )}
            </div>

            <div className="grid grid-cols-2 gap-4">
                <Input
                    label={t('teamCapacity.person')}
                    value={formData.name}
                    onChange={e => setFormData({ ...formData, name: e.target.value })}
                    disabled={hasLinkedProfile}
                    required
                />
                <Input
                    label={t('teamCapacity.iterationRole')}
                    value={formData.position}
                    onChange={e => setFormData({ ...formData, position: e.target.value })}
                    required
                />
            </div>

            <Input
                type="email"
                label={t('teamCapacity.profileEmail')}
                value={formData.email || ''}
                onChange={e => setFormData({ ...formData, email: e.target.value })}
                placeholder={t('teamCapacity.emailPlaceholder')}
                disabled={hasLinkedProfile}
            />

            {/* Collapsible: Workload Settings */}
            <CollapsibleSection title={t('teamForm.iterationCapacity')} defaultOpen={initialData?.availability_percent !== 100 || initialData?.professionalism_coefficient !== 1 || initialData?.operational_utilization !== 20}>
                <div className="grid grid-cols-3 gap-4">
                    <Input
                        type="number"
                        label={t('teamCapacity.availability')}
                        min="0"
                        max="100"
                        value={formData.availability_percent}
                        onChange={e => setFormData({ ...formData, availability_percent: parseFloat(e.target.value) })}
                        required
                    />
                    <Input
                        type="number"
                        label={t('teamCapacity.professionalismCoefficient')}
                        step="0.1"
                        min="0.1"
                        value={formData.professionalism_coefficient}
                        onChange={e => setFormData({ ...formData, professionalism_coefficient: parseFloat(e.target.value) })}
                        required
                    />
                    <Input
                        type="number"
                        label={t('teamCapacity.utilization')}
                        min="0"
                        max="100"
                        value={formData.operational_utilization}
                        onChange={e => setFormData({ ...formData, operational_utilization: parseFloat(e.target.value) })}
                        required
                    />
                </div>
            </CollapsibleSection>

            <div className="flex justify-end gap-2 pt-4 border-t">
                <Button type="button" variant="ghost" onClick={onCancel}>
                    {t('actions.cancel')}
                </Button>
                <Button
                    type="submit"
                    isLoading={createMutation.isPending || updateMutation.isPending}
                    disabled={profilesQuery.isLoading || profilesQuery.isError}
                >
                    <Save className="w-4 h-4 mr-2" />
                    {initialData ? t('teamCapacity.updateAssignment') : t('teamCapacity.addToIteration')}
                </Button>
            </div>
        </form>
    );
};

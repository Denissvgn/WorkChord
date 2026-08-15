import { useEffect, useId, useState } from 'react';
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
    onStateChange?: (state: { dirty: boolean; pending: boolean }) => void;
}

const initialFormData = (
    defaultRole: string,
    initialData?: TeamMember,
    initialProfile?: TeamMemberProfile,
): TeamMemberCreate => {
    if (initialData) {
        return {
            name: initialData.profile?.display_name ?? initialData.name,
            position: initialData.position,
            email: initialData.profile?.email || initialData.email || '',
            profile_id: initialData.profile_id ?? null,
            availability_percent: initialData.availability_percent,
            professionalism_coefficient: initialData.professionalism_coefficient,
            operational_utilization: initialData.operational_utilization,
        };
    }

    if (initialProfile) {
        return {
            name: initialProfile.display_name,
            position: initialProfile.headline || defaultRole,
            email: initialProfile.email || '',
            profile_id: initialProfile.id,
            availability_percent: 100,
            professionalism_coefficient: 1.0,
            operational_utilization: 20,
        };
    }

    return {
        name: '',
        position: defaultRole,
        email: '',
        profile_id: null,
        availability_percent: 100,
        professionalism_coefficient: 1.0,
        operational_utilization: 20,
    };
};

const formsMatch = (left: TeamMemberCreate, right: TeamMemberCreate) => (
    left.name === right.name
    && left.position === right.position
    && (left.email ?? '') === (right.email ?? '')
    && (left.profile_id ?? null) === (right.profile_id ?? null)
    && Object.is(left.availability_percent, right.availability_percent)
    && Object.is(left.professionalism_coefficient, right.professionalism_coefficient)
    && Object.is(left.operational_utilization, right.operational_utilization)
);

export const TeamForm = ({
    iterationId,
    initialData,
    initialProfile,
    onSuccess,
    onCancel,
    onStateChange,
}: TeamFormProps) => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const profileSelectId = useId();
    const profileHelpId = useId();
    const [error, setError] = useState<string | null>(null);
    const [baselineFormData] = useState<TeamMemberCreate>(() => (
        initialFormData(t('teamCapacity.defaultRole'), initialData, initialProfile)
    ));
    const [formData, setFormData] = useState<TeamMemberCreate>(
        baselineFormData,
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

    const isPending = createMutation.isPending || updateMutation.isPending;
    const isDirty = !formsMatch(formData, baselineFormData);

    useEffect(() => {
        onStateChange?.({ dirty: isDirty, pending: isPending });
    }, [isDirty, isPending, onStateChange]);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (isPending) return;
        setError(null);
        const payload = selectedProfile
            ? {
                ...formData,
                name: selectedProfile.display_name,
                email: selectedProfile.email || '',
                profile_id: selectedProfile.id,
            }
            : { ...formData };
        if (initialData) {
            updateMutation.mutate(payload);
        } else {
            createMutation.mutate(payload);
        }
    };

    const handleProfileChange = (profileId: number | null) => {
        if (isPending) return;
        const profile = profiles.find(candidate => candidate.id === profileId) ?? null;
        setError(null);
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

    const updateForm = (patch: Partial<TeamMemberCreate>) => {
        if (isPending) return;
        setError(null);
        setFormData(current => ({ ...current, ...patch }));
    };

    const handleCancel = () => {
        if (isPending) return;
        onCancel();
    };

    return (
        <div className="space-y-6">
            {profilesQuery.isLoading && <QueryLoadingState />}
            {profilesQuery.isError && (
                <QueryErrorState
                    error={profilesQuery.error}
                    fallback={t(
                        'teamCapacity.profileLoadFailedManual',
                        'Existing profiles could not be loaded. Retry, or enter person details manually below.',
                    )}
                    onRetry={isPending ? undefined : () => void profilesQuery.refetch()}
                />
            )}

            <form onSubmit={handleSubmit} aria-busy={isPending} className="space-y-6">
                <fieldset disabled={isPending} className="min-w-0 space-y-6 border-0 p-0">
                    {error && (
                        <div
                            className="rounded-md bg-feedback-danger-muted p-3 text-sm text-feedback-danger-foreground"
                            role="alert"
                        >
                            {error}
                        </div>
                    )}

                    <div className="rounded-md border border-action bg-action-muted p-3 text-sm text-action">
                        {t('teamCapacity.intro')}
                    </div>

                    <div>
                        <label
                            className="mb-1 block text-sm font-medium text-content-primary"
                            htmlFor={profileSelectId}
                        >
                            {t('teamCapacity.globalProfile')}
                        </label>
                        <select
                            id={profileSelectId}
                            aria-describedby={profileHelpId}
                            value={formData.profile_id ?? ''}
                            onChange={event => handleProfileChange(event.target.value ? Number(event.target.value) : null)}
                            disabled={isPending || isLoadingProfiles || profilesQuery.isError}
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
                        <p id={profileHelpId} className="mt-1 text-xs text-content-secondary">
                            {t('teamCapacity.profileHelp')}
                        </p>
                        {profilesQuery.isSuccess && profiles.length === 0 && !initialData && (
                            <p className="mt-2 rounded-md border border-feedback-warning-border bg-feedback-warning-muted px-3 py-2 text-xs text-feedback-warning-foreground">
                                {t('teamCapacity.noProfilesCreateFromDetails')}
                            </p>
                        )}
                    </div>

                    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                        <Input
                            label={t('teamCapacity.person')}
                            value={formData.name}
                            onChange={event => updateForm({ name: event.target.value })}
                            disabled={hasLinkedProfile || isPending}
                            maxLength={255}
                            required
                        />
                        <Input
                            label={t('teamCapacity.iterationRole')}
                            value={formData.position}
                            onChange={event => updateForm({ position: event.target.value })}
                            maxLength={255}
                            required
                        />
                    </div>

                    <Input
                        type="email"
                        label={t('teamCapacity.profileEmail')}
                        value={formData.email || ''}
                        onChange={event => updateForm({ email: event.target.value })}
                        placeholder={t('teamCapacity.emailPlaceholder')}
                        disabled={hasLinkedProfile || isPending}
                        maxLength={255}
                    />

                    <CollapsibleSection title={t('teamForm.iterationCapacity')} defaultOpen={initialData?.availability_percent !== 100 || initialData?.professionalism_coefficient !== 1 || initialData?.operational_utilization !== 20}>
                        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
                            <Input
                                type="number"
                                label={t('teamCapacity.availability')}
                                min="0"
                                max="100"
                                value={formData.availability_percent}
                                onChange={event => updateForm({ availability_percent: parseFloat(event.target.value) })}
                                required
                            />
                            <Input
                                type="number"
                                label={t('teamCapacity.professionalismCoefficient')}
                                step="0.1"
                                min="0.5"
                                max="5"
                                value={formData.professionalism_coefficient}
                                onChange={event => updateForm({ professionalism_coefficient: parseFloat(event.target.value) })}
                                required
                            />
                            <Input
                                type="number"
                                label={t('teamCapacity.utilization')}
                                min="0"
                                max="100"
                                value={formData.operational_utilization}
                                onChange={event => updateForm({ operational_utilization: parseFloat(event.target.value) })}
                                required
                            />
                        </div>
                    </CollapsibleSection>

                    <div className="flex justify-end gap-2 border-t pt-4">
                        <Button type="button" variant="ghost" onClick={handleCancel} disabled={isPending}>
                            {t('actions.cancel')}
                        </Button>
                        <Button
                            type="submit"
                            isLoading={isPending}
                            disabled={isPending}
                        >
                            <Save aria-hidden="true" className="mr-2 h-4 w-4" />
                            {initialData ? t('teamCapacity.updateAssignment') : t('teamCapacity.addToIteration')}
                        </Button>
                    </div>
                </fieldset>
            </form>
        </div>
    );
};

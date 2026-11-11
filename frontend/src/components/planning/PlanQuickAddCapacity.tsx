import { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { Button } from '../common/Button';
import { QueryErrorState } from '../feedback/QueryState';
import { teamService } from '../../services/teamService';
import { planningInputService } from '../../services/planningInputService';
import type { Iteration } from '../../types/iteration';
import type { TeamMember, TeamMemberProfile } from '../../types/team';
import { getApiErrorMessage } from '../../utils/apiError';

/** Adds one capacity row from an existing profile without leaving the plan (the default case). */
export const PlanQuickAddCapacity = ({ iteration, members }: { iteration: Iteration; members: TeamMember[] }) => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const [profileId, setProfileId] = useState('');
    // feedback-policy: query loading,error,retry,empty
    const profiles = useQuery({ queryKey: ['team-member-profiles'], queryFn: teamService.getProfiles, staleTime: 60_000 });
    const onIteration = new Set(members.map(member => member.profile_id).filter((id): id is number => typeof id === 'number'));
    const available = (profiles.data ?? []).filter(profile => !onIteration.has(profile.id));
    // feedback-policy: mutation pending,inline
    const add = useMutation({
        mutationFn: async (profile: TeamMemberProfile) => {
            // The same revision read the Team form makes before creating a capacity row.
            const observed = await planningInputService.readInitial<TeamMember>('member', iteration.id, true, { profile_id: profile.id });
            const isAgent = profile.profile_kind === 'agent';
            return teamService.create(iteration.id, {
                name: profile.display_name,
                position: profile.headline || (isAgent ? t('plan.quickCapacity.agentRole') : t('plan.quickCapacity.personRole')),
                email: profile.email || undefined,
                profile_id: profile.id,
                availability_percent: 100,
                professionalism_coefficient: 1,
                // An agent has no meetings or admin overhead; a person keeps the usual 20%.
                operational_utilization: isAgent ? 0 : 20,
            }, observed?.expected_revisions ?? {});
        },
        onSuccess: () => {
            setProfileId('');
            void queryClient.invalidateQueries({ queryKey: ['team'] });
        },
    });
    if (profiles.isError) {
        return <QueryErrorState error={profiles.error} fallback={t('plan.quickCapacity.profilesFailed')} onRetry={() => void profiles.refetch()} />;
    }
    if (profiles.isLoading) return <p role="status" className="text-sm text-content-secondary">{t('common.loading')}</p>;
    if (available.length === 0) return <p className="text-sm text-content-secondary">{t('plan.quickCapacity.noProfiles')}</p>;
    const selected = available.find(profile => String(profile.id) === profileId);
    return (
        <form className="flex flex-wrap items-end gap-2" onSubmit={event => { event.preventDefault(); if (selected) add.mutate(selected); }}>
            <label className="min-w-48 flex-1">
                <span className="field-lbl">{t('plan.quickCapacity.profile')}</span>
                <select className="input w-full" value={profileId} onChange={event => setProfileId(event.target.value)}>
                    <option value="">{t('plan.quickCapacity.chooseProfile')}</option>
                    {available.map(profile => (
                        <option key={profile.id} value={profile.id}>
                            {profile.display_name}{profile.profile_kind === 'agent' ? ` · ${t('plan.quickCapacity.agent')}` : ''}
                        </option>
                    ))}
                </select>
            </label>
            <Button type="submit" disabled={!selected} isLoading={add.isPending}>{t('plan.quickCapacity.add')}</Button>
            {add.isError && <p role="alert" className="w-full text-sm text-feedback-danger-foreground">{getApiErrorMessage(add.error, t('plan.quickCapacity.addFailed'))}</p>}
            <p className="w-full text-xs text-content-secondary">{t('plan.quickCapacity.help')}</p>
        </form>
    );
};

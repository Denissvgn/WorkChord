import { useQueries, useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { teamService } from '../../services/teamService';
import type { TeamMember, TeamMemberProfile } from '../../types/team';
import { QueryErrorState } from '../feedback/QueryState';

import { Button } from '../../components/common/Button';
import { Select } from '../../components/common/Select';
export const AssigneePicker = ({ id, members, value, profile, disabled, allowAdd, onChange }: {
    id: string; members: TeamMember[]; value: number | null; profile: TeamMemberProfile | null;
    disabled: boolean; allowAdd: boolean;
    onChange: (memberId: number | null, profile: TeamMemberProfile | null) => void;
}) => {
    const { t } = useTranslation();
    // feedback-policy: query loading,error,retry,empty - the existing iteration choices remain usable while the profile list loads.
    const profiles = useQuery({ queryKey: ['team-member-profiles'], queryFn: teamService.getProfiles, enabled: allowAdd && !disabled });
    // feedback-policy: query loading,error,retry,empty - a failed load is explicitly unknown and can be retried.
    const workloads = useQueries({ queries: members.map(member => ({ queryKey: ['workload', member.id], queryFn: () => teamService.getWorkload(member.id), enabled: !disabled })) });
    const label = (member: TeamMember) => {
        const workload = workloads[members.indexOf(member)];
        return `${member.name} · ${workload?.data ? t('assigneePicker.load', { percent: Math.round(workload.data.workload_percent) }) : t(workload?.isPending ? 'common.loading' : 'assigneePicker.loadUnknown')}`;
    };
    const outside = profiles.data?.filter(candidate => !members.some(member => member.profile_id === candidate.id)) ?? [];
    return <div className="field">
        <label htmlFor={id} className="field-lbl">{t('taskList.assignee')}</label>
        <Select id={id} className="input w-full" disabled={disabled} value={profile ? `profile:${profile.id}` : value ?? ''} onChange={event => {
            const selected = event.target.value;
            if (selected.startsWith('profile:')) onChange(null, outside.find(candidate => candidate.id === Number(selected.slice(8))) ?? null);
            else onChange(selected ? Number(selected) : null, null);
        }}>
            <option value="">{t('common.unassigned')}</option>
            {(['human', 'agent'] as const).map(kind => <optgroup key={kind} label={t(kind === 'agent' ? 'assigneePicker.agents' : 'assigneePicker.people')}>
                {members.filter(member => (member.profile?.profile_kind === 'agent') === (kind === 'agent')).map(member => <option key={member.id} value={member.id}>{label(member)}</option>)}
            </optgroup>)}
            {outside.length > 0 && <optgroup label={t('assigneePicker.outside')}>
                {outside.map(candidate => <option key={candidate.id} value={`profile:${candidate.id}`}>{candidate.display_name} · {t('assigneePicker.addAndAssign')}</option>)}
            </optgroup>}
        </Select>
        {profiles.isLoading && <p role="status" className="mt-1 text-xs text-content-secondary">{t('common.loading')}</p>}
        {profiles.isError && <QueryErrorState error={profiles.error} fallback={t('queryFeedback.optionLoadFailed')} onRetry={() => void profiles.refetch()} />}
        {workloads.some(query => query.isError) && <Button type="button"  onClick={() => workloads.filter(query => query.isError).forEach(query => void query.refetch())} variant="ghost" size="sm">{t('common.retry')}</Button>}
        {profile && <p className="mt-2 text-xs text-content-secondary">{t('assigneePicker.confirmHint', { name: profile.display_name, overhead: profile.profile_kind === 'agent' ? 0 : 20 })}</p>}
    </div>;
};

import { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { Bot, User } from 'lucide-react';
import { Button } from '../common/Button';
import { Modal } from '../common/Modal';
import { QueryErrorState } from '../feedback/QueryState';
import { teamService } from '../../services/teamService';
import type { Iteration } from '../../types/iteration';
import type { TeamMember } from '../../types/team';
import { getApiErrorMessage } from '../../utils/apiError';
import { addCapacityRows, refreshCapacity } from './capacityMutations';

export const PlanQuickAddCapacity = ({ iteration, members, primary = true }: { iteration: Iteration; members: TeamMember[]; primary?: boolean }) => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const [open, setOpen] = useState(false);
    const [selected, setSelected] = useState<number[]>([]);
    // feedback-policy: query loading,error,retry,empty
    const profiles = useQuery({ queryKey: ['teamMemberProfiles'], queryFn: teamService.getProfiles, enabled: open, staleTime: 60_000 });
    const onIteration = new Set(members.map(member => member.profile_id));
    const available = (profiles.data ?? []).filter(profile => !onIteration.has(profile.id));
    // feedback-policy: mutation pending,inline
    const add = useMutation({
        mutationFn: () => addCapacityRows(iteration.id, available.filter(profile => selected.includes(profile.id)).map(profile => ({
            name: profile.display_name,
            position: profile.headline || t(profile.profile_kind === 'agent' ? 'plan.quickCapacity.agentRole' : 'plan.quickCapacity.personRole'),
            email: profile.email || undefined,
            profile_id: profile.id,
            availability_percent: 100,
            professionalism_coefficient: 1,
            operational_utilization: profile.profile_kind === 'agent' ? 0 : 20,
        }))),
        onSuccess: () => { setOpen(false); setSelected([]); },
        onSettled: () => refreshCapacity(queryClient),
    });
    const close = () => { if (!add.isPending) setOpen(false); };
    return <>
        <Button variant={primary ? 'primary' : 'secondary'} onClick={() => { setOpen(true); setSelected([]); add.reset(); }}>{t('plan.quickCapacity.add')}</Button>
        {open && <Modal open title={t('plan.quickCapacity.add')} onClose={close} closeLabel={t('actions.close')} closeDisabled={add.isPending}
            footer={<div className="flex justify-end gap-2">
                <Button variant="secondary" onClick={close} disabled={add.isPending}>{t('actions.cancel')}</Button>
                <Button onClick={() => add.mutate()} isLoading={add.isPending} disabled={add.isPending || profiles.isError || !available.some(profile => selected.includes(profile.id))}>{t('capacity.addSelected')}</Button>
            </div>}>
            <p className="mb-4 text-sm text-content-secondary">{t('plan.quickCapacity.help')}</p>
            {profiles.isLoading && <p role="status">{t('common.loading')}</p>}
            {profiles.isError && <QueryErrorState error={profiles.error} onRetry={() => void profiles.refetch()} />}
            {profiles.isSuccess && available.length === 0 && <p>{t('plan.quickCapacity.noProfiles')}</p>}
            <fieldset disabled={add.isPending} className="m-0 min-w-0 space-y-1 border-0 p-0">
                <legend className="sr-only">{t('capacity.chooseMembers')}</legend>
                {available.map(profile => {
                    const agent = profile.profile_kind === 'agent';
                    const Icon = agent ? Bot : User;
                    return <label key={profile.id} className="flex cursor-pointer items-center gap-3 rounded-md px-2 py-3 hover:bg-surface-muted">
                        <input type="checkbox" checked={selected.includes(profile.id)} onChange={event => setSelected(current => event.target.checked ? [...current, profile.id] : current.filter(id => id !== profile.id))} />
                        <Icon aria-hidden="true" className="h-4 w-4 shrink-0 text-content-secondary" />
                        <span className="min-w-0 break-words">{profile.display_name}</span>
                        <span className="ml-auto text-xs text-content-secondary">{t(agent ? 'capacity.agent' : 'capacity.person')}</span>
                    </label>;
                })}
            </fieldset>
            {add.isError && <p role="alert" className="mt-3 text-sm text-feedback-danger-foreground">{getApiErrorMessage(add.error, t('capacity.addFailed'))}</p>}
        </Modal>}
    </>;
};

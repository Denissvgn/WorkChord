import { useId, useState } from 'react';
import type { FormEvent } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { Button } from '../../components/common/Button';
import { teamService } from '../../services/teamService';
import { getApiErrorMessage } from '../../utils/apiError';
import { identityService } from './identityService';
import type { WorkProfile } from './identityService';

/**
 * Lets a trusted-local session say which person it works as. The choice is
 * stored on the server session and is never a verified identity.
 */
export const LocalProfilePicker = ({ current, onChosen }: { current: WorkProfile | null; onChosen: () => void }) => {
    const { t } = useTranslation();
    const ids = useId();
    const [profileId, setProfileId] = useState(current ? String(current.id) : '');
    const [name, setName] = useState('');
    // feedback-policy: query loading,error,retry,empty
    const profiles = useQuery({ queryKey: ['teamMemberProfiles'], queryFn: teamService.getProfiles });
    // feedback-policy: mutation pending,inline
    const choose = useMutation({ mutationFn: (id: number | null) => identityService.chooseLocalProfile(id), onSuccess: onChosen });
    // feedback-policy: mutation pending,inline
    const addMe = useMutation({
        mutationFn: async (displayName: string) => {
            const created = await teamService.createProfile({ display_name: displayName, profile_kind: 'human', automation_enabled: true, assignment_modes: [] });
            return identityService.chooseLocalProfile(created.id);
        },
        onSuccess: onChosen,
    });
    const people = (profiles.data ?? []).filter(profile => profile.profile_kind === 'human');
    const pending = choose.isPending || addMe.isPending;
    const failure = choose.error ?? addMe.error;
    const submitChoice = (event: FormEvent) => { event.preventDefault(); if (profileId) choose.mutate(Number(profileId)); };
    const submitName = (event: FormEvent) => { event.preventDefault(); if (name.trim()) addMe.mutate(name.trim()); };

    return <div className="space-y-3 text-sm">
        <p className="text-content-secondary">{t('identity.localProfileHelp')}</p>
        {profiles.isLoading && <p role="status">{t('common.loading')}</p>}
        {profiles.isError && <p role="alert" className="text-feedback-danger-foreground">{t('identity.profilesFailed')}{' '}
            <button type="button" className="underline" onClick={() => { void profiles.refetch(); }}>{t('taskEditor.retry')}</button></p>}
        {profiles.isSuccess && people.length === 0 && <p>{t('identity.noPeople')}</p>}
        {people.length > 0 && <form className="space-y-2" onSubmit={submitChoice}>
            <label className="block font-medium" htmlFor={`${ids}-person`}>{t('identity.personProfile')}</label>
            <select id={`${ids}-person`} className="min-h-11 w-full rounded-md border border-border bg-surface-card px-2" value={profileId}
                onChange={event => setProfileId(event.target.value)}>
                <option value="">{t('identity.choosePerson')}</option>
                {people.map(profile => <option key={profile.id} value={profile.id}>{profile.display_name}</option>)}
            </select>
            <Button type="submit" size="sm" disabled={!profileId || pending || Number(profileId) === current?.id}>{t('identity.useProfile')}</Button>
        </form>}
        <form className="space-y-2" onSubmit={submitName}>
            <label className="block font-medium" htmlFor={`${ids}-name`}>{t('identity.yourName')}</label>
            <input id={`${ids}-name`} className="min-h-11 w-full rounded-md border border-border bg-surface-card px-2" value={name} maxLength={255}
                autoComplete="name" aria-describedby={`${ids}-name-help`} onChange={event => setName(event.target.value)} />
            <p id={`${ids}-name-help`} className="text-xs text-content-secondary">{t('identity.addMeHelp')}</p>
            <Button type="submit" size="sm" variant="secondary" disabled={!name.trim() || pending}>{t('identity.addMe')}</Button>
        </form>
        {current && <Button size="sm" variant="ghost" disabled={pending} onClick={() => choose.mutate(null)}>
            {t('identity.stopWorkingAs', { name: current.display_name })}</Button>}
        {failure && <p role="alert" className="text-feedback-danger-foreground">{getApiErrorMessage(failure, t('identity.localProfileFailed'))}</p>}
    </div>;
};

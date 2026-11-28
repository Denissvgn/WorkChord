import { useCallback, useEffect, useState, type RefObject } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { Plus, Trash2 } from 'lucide-react';
import { teamService } from '../../services/teamService';
import { agentService } from '../../services/agentService';
import { useAdminAccess } from '../../hooks/useAdminAccess';
import { getApiErrorMessage } from '../../utils/apiError';
import { formatDateTime } from '../../utils/formatDate';
import { Button } from '../common/Button';
import { Input } from '../common/Input';
import { useConfirmDialog } from '../common/useConfirmDialog';
import { QueryErrorState } from '../feedback/QueryState';
import { SlideOverDrawer } from '../ui';
import { PersonCapacity } from '../tasks/PersonCapacity';
import { usePlanningObservation } from '../../features/usePlanningObservation';
import { planningInputService, type ObservedPlanningInput } from '../../services/planningInputService';
import type {
    TeamMemberAssignmentMode,
    TeamMemberProfile,
    TeamMemberProfileCreate,
    TeamMemberProfileKind,
    TeamMemberProfileSkill,
    TeamMemberProfileSkillCreate,
    TeamMemberProfileUpdate,
} from '../../types/team';
import { feedbackMessage } from '../../features/mutationFeedback';
import type { MutationFeedbackMeta } from '../../features/mutationFeedback';
import { actorName, modelName, statusKnown, type AgentStatus, type DirectoryActor, type DirectoryRow } from './directoryModel';
import { isConnected } from '../../features/agentTeamSetup/connectAgent';
import { useWaitingAgents } from '../../features/agentTeamSetup/useWaitingAgents';
import { ConnectionSteps } from './ConnectionSteps';
import type { AgentActorRosterItem } from '../../types/agent';

import { Select } from '../../components/common/Select';
const PROFILE_KINDS: TeamMemberProfileKind[] = ['human', 'agent', 'hybrid'];

const ASSIGNMENT_MODES: TeamMemberAssignmentMode[] = [
    'ownership',
    'execution',
    'verification',
    'design_handoff',
];

const emptyProfileForm: TeamMemberProfileCreate = {
    seed_key: '',
    display_name: '',
    email: '',
    headline: '',
    summary: '',
    notes: '',
    automation_enabled: true,
    profile_kind: 'human',
    assignment_modes: [],
};

const emptySkillForm: TeamMemberProfileSkillCreate = {
    skill_key: '',
    skill_name: '',
    category: '',
    level: 3,
    interest: 3,
    is_weakness: false,
    keywords_json: [],
    notes: '',
};

const skillKeyFromName = (value: string) => value
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9+#.:-]+/g, '-')
    .replace(/^-+|-+$/g, '');

const optionalText = (value?: string | null) => {
    const text = value?.trim();
    return text || null;
};

const formFromProfile = (profile: TeamMemberProfile): TeamMemberProfileCreate => ({
    seed_key: profile.seed_key || '',
    display_name: profile.display_name,
    email: profile.email || '',
    headline: profile.headline || '',
    summary: profile.summary || '',
    notes: profile.notes || '',
    automation_enabled: profile.automation_enabled,
    profile_kind: profile.profile_kind,
    assignment_modes: [...profile.assignment_modes],
});

interface TeamProfileManagerProps {
    /** The person or agent to edit; absent when a person is being added. */
    row: DirectoryRow | null;
    onClose: () => void;
    /** Called with the profile's id once a person has been added or an agent's profile has been created. */
    onCreated: (profileId: number) => void;
    /** Where focus goes on close when the control that opened the drawer is gone. */
    fallbackFocusRef?: RefObject<HTMLElement | null>;
}

type ObservedProfile = ObservedPlanningInput<TeamMemberProfile>;
type ProfileContext = ReturnType<typeof usePlanningObservation<TeamMemberProfile>>;

/** The profile as it was observed: the editable values and the revisions they were read at stay together. */
interface FormBase {
    fields: TeamMemberProfileCreate;
    revisions: Record<number, number>;
}

const sameFields = (a: TeamMemberProfileCreate, b: TeamMemberProfileCreate) => JSON.stringify(a) === JSON.stringify(b);

const MODE_FOR_ROLE: Record<string, TeamMemberAssignmentMode> = { pm: 'ownership', worker: 'execution', verifier: 'verification' };

const useInvalidateTeam = () => {
    const queryClient = useQueryClient();
    return () => Promise.all([
        queryClient.invalidateQueries({ queryKey: ['teamMemberProfiles'] }),
        queryClient.invalidateQueries({ queryKey: ['team'] }),
        queryClient.invalidateQueries({ queryKey: ['assigneeRecommendations'] }),
        queryClient.invalidateQueries({ queryKey: ['agent-actor-roster'] }),
    ]);
};

/** The read-only model and connection of an agent, with the one sentence on when it receives work. */
const AgentSection = ({ row }: { row: DirectoryRow }) => {
    const { t } = useTranslation();
    // Actor details (last seen, eligible models) come from the same roster read, so they are shown only when its status is known.
    const readable = statusKnown(row.status) && row.actors.length > 0;
    return (
        <section aria-labelledby="team-drawer-agent" className="space-y-2">
            <h3 id="team-drawer-agent" className="text-sm font-semibold text-content-primary">{t('teamProfiles.modelBinding')}</h3>
            <p className="text-sm text-content-secondary">{t('teamProfiles.agentDispatchNote')}</p>
            {!readable && (
                <StatusList status={row.status ?? { model: undefined, connection: 'unknown' }} />
            )}
            {readable && row.actors.length === 1 && <ActorBinding entry={row.actors[0]} />}
            {readable && row.actors.length > 1 && row.actors.map(entry => {
                const role = entry.role ? t(`teamPage.roles.${entry.role}`) : null;
                const label = role ? `${role} · ${actorName(entry.actor)}` : actorName(entry.actor);
                return (
                    <div key={entry.actor.id} role="group" aria-label={label} className="space-y-1 border-t border-border pt-2">
                        <p className="text-sm font-medium text-content-primary">{label}</p>
                        <ActorBinding entry={entry} />
                    </div>
                );
            })}
            {row.rosterState === 'unavailable' && <p className="text-sm text-content-secondary">{t('teamPage.adminKeyNote')}</p>}
            <WaitingConnection row={row} />
        </section>
    );
};

/**
 * The connection steps of an agent that still waits for its runtime's acknowledgement. They come from the
 * team status, not from the Connect page, so they stay reachable after Connect was left.
 */
const WaitingConnection = ({ row }: { row: DirectoryRow }) => {
    const { t } = useTranslation();
    const { hasAdminAccess } = useAdminAccess();
    const { status, manifest, waiting } = useWaitingAgents(hasAdminAccess);
    const entry = waiting.find(item => row.actors.some(actor => actor.actor.name === item.member.actor_name));
    if (!entry || !manifest) return null;
    return (
        <section aria-labelledby="team-drawer-connection" className="space-y-3 border-t border-border pt-4">
            <h3 id="team-drawer-connection" className="text-sm font-semibold text-content-primary">{t('agentTeamSetup.connect.drawerTitle')}</h3>
            <ConnectionSteps manifest={manifest} member={entry.member} memberStatus={entry.memberStatus} connected={isConnected(entry.memberStatus)}
                checking={status.isFetching} onCheck={() => void status.refetch()} />
        </section>
    );
};

/** A connection and a model as the status says; Unknown when the roster could not be read. */
const StatusList = ({ status, lastSeenAt }: { status: AgentStatus; lastSeenAt?: string | null }) => {
    const { t, i18n } = useTranslation();
    return (
        <dl className="grid grid-cols-[auto_1fr] gap-x-4 gap-y-1 text-sm">
            <dt className="text-content-secondary">{t('teamPage.columns.connection')}</dt>
            <dd>{t(`teamPage.connection.${status.connection}`)}</dd>
            {lastSeenAt && statusKnown(status) && (
                <>
                    <dt className="text-content-secondary">{t('teamProfiles.lastSeen')}</dt>
                    <dd>{formatDateTime(lastSeenAt, i18n.language)}</dd>
                </>
            )}
            <dt className="text-content-secondary">{t('teamPage.columns.model')}</dt>
            <dd>{status.model === undefined ? t('teamPage.unknown') : status.model ? modelName(status.model, effort => t(`modelAdministration.effort_${effort}`)) : t('teamPage.noModel')}</dd>
        </dl>
    );
};

/** One actor's connection, when it was last seen, its default model and every model it may use. */
const ActorBinding = ({ entry }: { entry: DirectoryActor }) => {
    const { t } = useTranslation();
    const bindings = statusKnown(entry.status) ? entry.actor.eligible_model_bindings : [];
    return (
        <>
            <StatusList status={entry.status} lastSeenAt={entry.actor.last_seen_at} />
            {bindings.length > 0 && (
                <ul className="space-y-1 text-sm" aria-label={t('teamProfiles.modelBinding')}>
                    {bindings.map(binding => (
                        <li key={binding.id} className="flex flex-wrap items-center gap-2">
                            <span className="font-medium text-content-primary">{binding.model_catalog ? modelName(binding, effort => t(`modelAdministration.effort_${effort}`)) :binding.model_catalog_key}</span>
                            {binding.model_catalog && <span className="text-content-secondary">{binding.model_catalog.provider}</span>}
                            {binding.is_default && <span className="text-content-secondary">· {t('teamProfiles.defaultModel')}</span>}
                        </li>
                    ))}
                </ul>
            )}
        </>
    );
};

/**
 * The drawer for one person or agent: profile, capabilities, default availability and, for an agent, its model.
 * A row without a profile (an agent that has not been given one) is handled apart, so this drawer never
 * offers to create an unrelated person for it.
 */
export const TeamProfileManager = ({ row, ...drawer }: TeamProfileManagerProps) => {
    if (row === null) return <ProfileDrawer row={null} initial={null} {...drawer} />;
    if (row.profile === null) return <AgentWithoutProfileDrawer row={row} {...drawer} />;
    return <ObservedProfileDrawer row={row} profileId={row.profile.id} {...drawer} />;
};

/** Reads the profile first, so the form and the revisions it will be saved at come from the same observation. */
const ObservedProfileDrawer = ({ row, profileId, onClose, onCreated, fallbackFocusRef }: TeamProfileManagerProps & { row: DirectoryRow; profileId: number }) => {
    const { t } = useTranslation();
    const [initial, setInitial] = useState<ObservedProfile | null>(null);
    const [failure, setFailure] = useState<unknown>(null);

    const load = useCallback(() => {
        setFailure(null);
        planningInputService.readInitial<TeamMemberProfile>('profile', profileId).then(
            observed => setInitial(observed),
            cause => setFailure(cause),
        );
    }, [profileId]);

    useEffect(() => { queueMicrotask(load); }, [load]);

    if (initial) {
        return <ProfileDrawer row={row} initial={initial} onClose={onClose} onCreated={onCreated} fallbackFocusRef={fallbackFocusRef} />;
    }
    return (
        <SlideOverDrawer open onClose={onClose} title={row.name} subtitle={t(`teamPage.kinds.${row.kind}`)} fallbackFocusRef={fallbackFocusRef}>
            <div className="space-y-6 p-5">
                {failure === null
                    ? <p role="status" className="text-sm text-content-secondary">{t('common.loading')}</p>
                    : <QueryErrorState error={failure} onRetry={load} />}
                {row.kind === 'agent' && <AgentSection row={row} />}
            </div>
        </SlideOverDrawer>
    );
};

/** An agent that has no profile yet: say so, and offer to create its profile and link it to the agent. */
const AgentWithoutProfileDrawer = ({ row, onClose, onCreated, fallbackFocusRef }: TeamProfileManagerProps & { row: DirectoryRow }) => {
    const { t } = useTranslation();
    const { hasAdminAccess } = useAdminAccess();
    const invalidate = useInvalidateTeam();
    const [error, setError] = useState<string | null>(null);
    // If linking fails after the profile exists, a retry links it instead of creating a second one.
    const [createdProfileId, setCreatedProfileId] = useState<number | null>(null);
    const actor: AgentActorRosterItem | null = row.actors[0]?.actor ?? null;

    const linkMutation = useMutation({
        mutationFn: async () => {
            if (!actor) throw new Error('Agent not found');
            let profileId = createdProfileId;
            if (profileId === null) {
                const mode = MODE_FOR_ROLE[actor.role];
                const profile = await teamService.createProfile({
                    ...emptyProfileForm,
                    seed_key: null,
                    display_name: (actor.display_name || actor.name).trim(),
                    email: null,
                    headline: null,
                    summary: null,
                    notes: null,
                    profile_kind: 'agent',
                    assignment_modes: mode ? [mode] : [],
                });
                profileId = profile.id;
                setCreatedProfileId(profileId);
            }
            try {
                await agentService.linkActorProfile(actor.id, profileId);
            } catch (cause) {
                throw new LinkProfileError(cause);
            }
            return profileId;
        },
        onSuccess: async profileId => {
            await invalidate();
            onCreated(profileId);
        },
        onError: err => setError(err instanceof LinkProfileError
            ? `${t('teamProfiles.failedLinkProfile')} ${getApiErrorMessage(err.cause, '')}`.trim()
            : getApiErrorMessage(err, t('teamProfiles.failedSaveProfile'))),
    });

    return (
        <SlideOverDrawer open onClose={onClose} title={row.name} subtitle={t(`teamPage.kinds.${row.kind}`)} fallbackFocusRef={fallbackFocusRef}
            footer={<div className="flex justify-end"><Button type="button" variant="ghost" onClick={onClose}>{t('actions.close')}</Button></div>}>
            <div className="space-y-6 p-5">
                {error && <div className="rounded-md bg-feedback-danger-muted p-3 text-sm text-feedback-danger-foreground" role="alert">{error}</div>}
                <AgentSection row={row} />
                <section aria-labelledby="team-drawer-no-profile" className="space-y-2">
                    <h3 id="team-drawer-no-profile" className="text-sm font-semibold text-content-primary">{t('teamProfiles.profile')}</h3>
                    <p className="text-sm text-content-secondary">{t('teamProfiles.noProfileYet')}</p>
                    {!hasAdminAccess && <p className="text-sm text-content-secondary">{t('teamProfiles.linkProfileNeedsAdminKey')}</p>}
                    <Button type="button" variant="secondary" disabled={!hasAdminAccess || !actor} isLoading={linkMutation.isPending}
                        onClick={() => { setError(null); linkMutation.mutate(); }}>
                        <Plus className="h-4 w-4" aria-hidden="true" />
                        {t('teamProfiles.createLinkProfile')}
                    </Button>
                </section>
            </div>
        </SlideOverDrawer>
    );
};

class LinkProfileError extends Error {
    constructor(cause: unknown) { super('Linking the profile failed', { cause }); }
}

interface ProfileDrawerProps {
    row: DirectoryRow | null;
    /** The observation the form is filled from; absent when a person is being added. */
    initial: ObservedProfile | null;
    onClose: () => void;
    onCreated: (profileId: number) => void;
    fallbackFocusRef?: RefObject<HTMLElement | null>;
}

const ProfileDrawer = ({ row, initial, onClose, onCreated, fallbackFocusRef }: ProfileDrawerProps) => {
    const { t } = useTranslation();
    const profileId = initial?.resource.id ?? null;
    const [profileForm, setProfileForm] = useState<TeamMemberProfileCreate>(
        () => (initial ? formFromProfile(initial.resource) : emptyProfileForm),
    );
    const [base, setBase] = useState<FormBase | null>(
        () => (initial ? { fields: formFromProfile(initial.resource), revisions: initial.expected_revisions } : null),
    );
    const [skillForm, setSkillForm] = useState<TeamMemberProfileSkillCreate>(emptySkillForm);
    const [editingSkillId, setEditingSkillId] = useState<number | null>(null);
    const [skillFormOpen, setSkillFormOpen] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const { requestConfirmation, confirmationDialog } = useConfirmDialog();
    const context: ProfileContext = usePlanningObservation<TeamMemberProfile>();
    const current = context.observation ?? initial;

    const skills: TeamMemberProfileSkill[] = current?.resource.skills ?? [];
    const agent = row?.kind === 'agent';
    const saving = context.loading;

    /**
     * Reads the profile again. After a save the form shows what was stored. After a capability change
     * the saved revisions move on only if nobody else changed the profile fields in the meantime, so a
     * later save of an out-of-date form is still refused. Keeping a draft is the explicit way to move on.
     */
    const refresh = async (id: number, mode: 'saved' | 'capability' | 'keepDraft') => {
        const fresh = await context.read('profile', id, true);
        if (!fresh) return;
        const fields = formFromProfile(fresh.resource);
        if (mode === 'saved') {
            setProfileForm(fields);
            setBase({ fields, revisions: fresh.expected_revisions });
        } else if (mode === 'keepDraft') {
            setBase({ fields, revisions: fresh.expected_revisions });
        } else {
            setBase(previous => (previous && sameFields(previous.fields, fields) ? { fields, revisions: fresh.expected_revisions } : previous));
        }
    };

    const invalidate = useInvalidateTeam();

    const createProfileMutation = useMutation({
        mutationFn: (data: TeamMemberProfileCreate) => teamService.createProfile(data),
        meta: { success: data => feedbackMessage(t, 'created', 'profile', (data as { display_name?: string }).display_name) } satisfies MutationFeedbackMeta,
        onSuccess: async profile => {
            await invalidate();
            onCreated(profile.id);
        },
        onError: err => setError(getApiErrorMessage(err, t('teamProfiles.failedSaveProfile'))),
    });

    const updateProfileMutation = useMutation({
        mutationFn: ({ id, data }: { id: number; data: TeamMemberProfileUpdate }) => teamService.updateProfile(id, data, base!.revisions),
        meta: { success: data => feedbackMessage(t, 'saved', 'profile', (data as { display_name?: string }).display_name) } satisfies MutationFeedbackMeta,
        onSuccess: async (_data, variables) => {
            await invalidate();
            void refresh(variables.id, 'saved');
        },
        onError: err => setError(getApiErrorMessage(err, t('teamProfiles.failedSaveProfile'))),
    });

    const deleteProfileMutation = useMutation({
        mutationFn: ({ id, revisions }: { id: number; revisions: Record<number, number> }) => teamService.deleteProfile(id, revisions),
        meta: { success: () => feedbackMessage(t, 'deleted', 'profile', row?.name) } satisfies MutationFeedbackMeta,
        onSuccess: async () => {
            await invalidate();
            onClose();
        },
        onError: err => setError(getApiErrorMessage(err, t('teamProfiles.failedDeleteProfile'))),
    });

    const closeSkillForm = () => {
        setSkillForm(emptySkillForm);
        setEditingSkillId(null);
        setSkillFormOpen(false);
    };

    const createSkillMutation = useMutation({
        mutationFn: ({ id, data }: { id: number; data: TeamMemberProfileSkillCreate }) => teamService.createProfileSkill(id, data, current!.expected_revisions),
        onSuccess: async (_data, variables) => {
            await invalidate();
            void refresh(variables.id, 'capability');
            closeSkillForm();
        },
        onError: err => setError(getApiErrorMessage(err, t('teamProfiles.failedSaveSkill'))),
    });

    const updateSkillMutation = useMutation({
        mutationFn: ({ id, skillId, data }: { id: number; skillId: number; data: TeamMemberProfileSkillCreate }) => teamService.updateProfileSkill(id, skillId, data, current!.expected_revisions),
        onSuccess: async (_data, variables) => {
            await invalidate();
            void refresh(variables.id, 'capability');
            closeSkillForm();
        },
        onError: err => setError(getApiErrorMessage(err, t('teamProfiles.failedSaveSkill'))),
    });

    const deleteSkillMutation = useMutation({
        mutationFn: ({ id, skillId, revisions }: { id: number; skillId: number; revisions: Record<number, number> }) => teamService.deleteProfileSkill(id, skillId, revisions),
        onSuccess: async (_data, variables) => {
            await invalidate();
            void refresh(variables.id, 'capability');
        },
        onError: err => setError(getApiErrorMessage(err, t('teamProfiles.failedDeleteSkill'))),
    });

    const submitProfile = (event: React.FormEvent) => {
        event.preventDefault();
        setError(null);
        const data: TeamMemberProfileCreate = {
            ...profileForm,
            seed_key: optionalText(profileForm.seed_key),
            display_name: profileForm.display_name.trim(),
            email: optionalText(profileForm.email),
            headline: optionalText(profileForm.headline),
            summary: optionalText(profileForm.summary),
            notes: optionalText(profileForm.notes),
        };
        if (profileId !== null) {
            if (!base || context.loading) return;
            const updateData: TeamMemberProfileUpdate = {
                display_name: data.display_name,
                email: data.email,
                headline: data.headline,
                summary: data.summary,
                notes: data.notes,
                automation_enabled: data.automation_enabled,
                profile_kind: data.profile_kind,
                assignment_modes: data.assignment_modes,
            };
            updateProfileMutation.mutate({ id: profileId, data: updateData });
        } else {
            createProfileMutation.mutate(data);
        }
    };

    const toggleAssignmentMode = (mode: TeamMemberAssignmentMode, checked: boolean) => {
        setProfileForm(current => ({
            ...current,
            assignment_modes: checked
                ? current.assignment_modes.includes(mode) ? current.assignment_modes : [...current.assignment_modes, mode]
                : current.assignment_modes.filter(item => item !== mode),
        }));
    };

    const submitSkill = (event: React.FormEvent) => {
        event.preventDefault();
        if (profileId === null || !current || context.loading) return;
        setError(null);
        const skillName = skillForm.skill_name.trim();
        const data = {
            ...skillForm,
            skill_name: skillName,
            skill_key: skillForm.skill_key.trim() || skillKeyFromName(skillName),
            category: optionalText(skillForm.category),
            keywords_json: skillForm.keywords_json,
            notes: optionalText(skillForm.notes),
        };
        if (editingSkillId) updateSkillMutation.mutate({ id: profileId, skillId: editingSkillId, data });
        else createSkillMutation.mutate({ id: profileId, data });
    };

    const editSkill = (skill: TeamMemberProfileSkill) => {
        setEditingSkillId(skill.id);
        setSkillFormOpen(true);
        setSkillForm({
            skill_key: skill.skill_key,
            skill_name: skill.skill_name,
            category: skill.category || '',
            level: skill.level,
            interest: skill.interest,
            is_weakness: skill.is_weakness,
            keywords_json: skill.keywords_json || [],
            notes: skill.notes || '',
        });
    };

    const confirmProfileDelete = async () => {
        if (profileId === null) return;
        try {
            const observed = await planningInputService.readInitial<TeamMemberProfile>('profile', profileId);
            requestConfirmation({ title: t('actions.delete'), description: t('teamProfiles.deleteProfileConfirm', { name: observed.resource.display_name }),
                confirmLabel: t('actions.delete'), cancelLabel: t('actions.cancel'), closeLabel: t('actions.close'),
                onConfirm: () => deleteProfileMutation.mutateAsync({ id: profileId, revisions: observed.expected_revisions }) });
        } catch (cause) { setError(getApiErrorMessage(cause, t('teamProfiles.failedDeleteProfile'))); }
    };

    const confirmSkillDelete = async (skill: TeamMemberProfileSkill) => {
        if (profileId === null) return;
        try {
            const observed = await planningInputService.readInitial<TeamMemberProfile>('profile', profileId);
            const current = observed.resource.skills.find(item => item.id === skill.id);
            if (!current) return;
            requestConfirmation({ title: t('actions.delete'), description: current.skill_name,
                confirmLabel: t('actions.delete'), cancelLabel: t('actions.cancel'), closeLabel: t('actions.close'),
                onConfirm: () => deleteSkillMutation.mutateAsync({ id: profileId, skillId: skill.id, revisions: observed.expected_revisions }) });
        } catch (cause) { setError(getApiErrorMessage(cause, t('teamProfiles.failedDeleteSkill'))); }
    };

    const summaryLine = (skill: TeamMemberProfileSkill) => {
        const summary = t('teamProfiles.skillSummary', { category: skill.category || t('teamProfiles.uncategorized'), level: skill.level, interest: skill.interest });
        return skill.is_weakness ? t('teamProfiles.skillSummaryWeakness', { summary }) : summary;
    };

    const formId = 'team-profile-form';
    const title = row ? row.name : t('teamProfiles.addPerson');

    return (
        <SlideOverDrawer
            open
            onClose={onClose}
            fallbackFocusRef={fallbackFocusRef}
            title={title}
            subtitle={row ? t(`teamPage.kinds.${row.kind}`) : t('teamProfiles.addPersonHint')}
            footer={(
                <div className="flex justify-between gap-2">
                    {profileId !== null ? (
                        <Button type="button" variant="ghost" className="text-feedback-danger-foreground" onClick={() => void confirmProfileDelete()}>
                            <Trash2 className="h-4 w-4" aria-hidden="true" />
                            {t('actions.delete')}
                        </Button>
                    ) : <span />}
                    <div className="flex gap-2">
                        <Button type="button" variant="ghost" onClick={onClose}>{t('actions.cancel')}</Button>
                        <Button type="submit" form={formId} disabled={saving}
                            isLoading={createProfileMutation.isPending || updateProfileMutation.isPending}>
                            {profileId !== null ? t('teamProfiles.save') : t('teamProfiles.create')}
                        </Button>
                    </div>
                </div>
            )}
        >
            <div className="space-y-6 p-5">
                {context.loading && <p role="status" className="text-sm text-content-secondary">{t('common.loading')}</p>}
                {Boolean(context.error) && (
                    <QueryErrorState error={context.error} onRetry={() => { if (profileId !== null) void context.read('profile', profileId, true); }} />
                )}
                {error && (
                    <div className="rounded-md bg-feedback-danger-muted p-3 text-sm text-feedback-danger-foreground" role="alert">
                        {error}
                        {profileId !== null && (
                            <Button type="button" size="sm" variant="secondary" onClick={() => { void refresh(profileId, 'keepDraft'); }}>
                                {t('taskEditor.keepDraftWithCurrentVersion')}
                            </Button>
                        )}
                    </div>
                )}

                {agent && row && <AgentSection row={row} />}

                <form id={formId} onSubmit={submitProfile} className="space-y-3" aria-label={t('teamProfiles.profile')}>
                    <h3 className="text-sm font-semibold text-content-primary">{t('teamProfiles.profile')}</h3>
                    <Input
                        id="profile-seed-key"
                        aria-describedby="profile-seed-key-help"
                        label={t('teamProfiles.seedKey')}
                        value={profileForm.seed_key || ''}
                        onChange={event => setProfileForm({ ...profileForm, seed_key: event.target.value })}
                        placeholder={t('teamProfiles.seedKeyPlaceholder')}
                        readOnly={profileId !== null}
                    />
                    <p id="profile-seed-key-help" className="-mt-2 text-xs text-content-tertiary">
                        {profileId !== null ? t('teamProfiles.seedKeyImmutableHelp') : t('teamProfiles.seedKeyHelp')}
                    </p>
                    <Input label={t('teamProfiles.displayName')} value={profileForm.display_name} onChange={event => setProfileForm({ ...profileForm, display_name: event.target.value })} required />
                    <Input label={t('teamProfiles.email')} type="email" value={profileForm.email || ''} onChange={event => setProfileForm({ ...profileForm, email: event.target.value })} />
                    <Input label={t('teamProfiles.headline')} value={profileForm.headline || ''} onChange={event => setProfileForm({ ...profileForm, headline: event.target.value })} placeholder={t('teamProfiles.headlinePlaceholder')} />
                    <textarea
                        aria-label={t('teamProfiles.summaryPlaceholder')}
                        value={profileForm.summary || ''}
                        onChange={event => setProfileForm({ ...profileForm, summary: event.target.value })}
                        placeholder={t('teamProfiles.summaryPlaceholder')}
                        className="min-h-[80px] w-full rounded-md border border-border-strong px-3 py-2 text-sm shadow-xs focus:border-action focus:outline-hidden focus:ring-1 focus:ring-focus"
                    />
                    <div className="field">
                        <label htmlFor="profile-kind" className="field-lbl">{t('teamProfiles.profileKind')}</label>
                        <Select
                            id="profile-kind"
                            className="input"
                            value={profileForm.profile_kind}
                            onChange={event => setProfileForm({ ...profileForm, profile_kind: event.target.value as TeamMemberProfileKind })}
                        >
                            {PROFILE_KINDS.map(kind => <option key={kind} value={kind}>{t(`teamProfiles.profileKinds.${kind}`)}</option>)}
                        </Select>
                    </div>
                    <fieldset className="rounded-md border border-border-subtle p-3">
                        <legend className="px-1 text-sm font-medium text-content-primary">{t('teamProfiles.assignmentModes')}</legend>
                        <div className="mt-1 grid gap-2 sm:grid-cols-2">
                            {ASSIGNMENT_MODES.map(mode => (
                                <label key={mode} className="flex items-center gap-2 text-sm text-content-primary">
                                    <input
                                        type="checkbox"
                                        checked={profileForm.assignment_modes.includes(mode)}
                                        onChange={event => toggleAssignmentMode(mode, event.target.checked)}
                                        className="h-4 w-4 rounded border-border-strong text-action focus:ring-focus"
                                    />
                                    {t(`teamProfiles.assignmentModeOptions.${mode}`)}
                                </label>
                            ))}
                        </div>
                    </fieldset>
                    <div>
                        <label className="flex items-center gap-2 text-sm text-content-primary">
                            <input
                                type="checkbox"
                                aria-describedby="profile-automation-help"
                                checked={profileForm.automation_enabled}
                                onChange={event => setProfileForm({ ...profileForm, automation_enabled: event.target.checked })}
                                className="h-4 w-4 rounded border-border-strong text-action focus:ring-focus"
                            />
                            {t('teamProfiles.useForRecommendations')}
                        </label>
                        <p id="profile-automation-help" className="mt-1 text-xs text-content-tertiary">{t('teamProfiles.automationEligibilityHelp')}</p>
                    </div>
                </form>

                {profileId !== null && (
                    <section aria-labelledby="team-drawer-capabilities" className="space-y-3">
                        <div className="flex items-center justify-between gap-2">
                            <h3 id="team-drawer-capabilities" className="text-sm font-semibold text-content-primary">{t('teamProfiles.capabilities')}</h3>
                            {!skillFormOpen && (
                                <Button type="button" size="sm" variant="secondary" onClick={() => setSkillFormOpen(true)}>
                                    <Plus className="h-4 w-4" aria-hidden="true" />
                                    {t('teamProfiles.addSkill')}
                                </Button>
                            )}
                        </div>
                        {skillFormOpen && (
                            <form onSubmit={submitSkill} className="space-y-2 rounded-md border border-border-subtle bg-surface-muted p-3" aria-label={t('teamProfiles.capabilities')}>
                                <Input label={t('teamProfiles.skill')} value={skillForm.skill_name} onChange={event => setSkillForm({ ...skillForm, skill_name: event.target.value })} placeholder={t('teamProfiles.skillPlaceholder')} required />
                                <div className="grid grid-cols-2 gap-2">
                                    <Input label={t('teamProfiles.category')} value={skillForm.category || ''} onChange={event => setSkillForm({ ...skillForm, category: event.target.value })} placeholder={t('teamProfiles.categoryPlaceholder')} />
                                    <Input label={t('teamProfiles.key')} value={skillForm.skill_key} onChange={event => setSkillForm({ ...skillForm, skill_key: event.target.value })} placeholder={t('teamProfiles.keyPlaceholder')} />
                                </div>
                                <div className="grid grid-cols-2 gap-2">
                                    <Input type="number" min="1" max="5" label={t('teamProfiles.level')} value={skillForm.level} onChange={event => setSkillForm({ ...skillForm, level: Number(event.target.value) })} />
                                    <Input type="number" min="1" max="5" label={t('teamProfiles.interest')} value={skillForm.interest} onChange={event => setSkillForm({ ...skillForm, interest: Number(event.target.value) })} />
                                </div>
                                <Input
                                    label={t('teamProfiles.keywords')}
                                    value={(skillForm.keywords_json || []).join(', ')}
                                    onChange={event => setSkillForm({ ...skillForm, keywords_json: event.target.value.split(',').map(item => item.trim()).filter(Boolean) })}
                                    placeholder={t('teamProfiles.keywordsPlaceholder')}
                                />
                                <label className="flex items-center gap-2 text-sm text-content-primary">
                                    <input
                                        type="checkbox"
                                        checked={skillForm.is_weakness}
                                        onChange={event => setSkillForm({ ...skillForm, is_weakness: event.target.checked })}
                                        className="h-4 w-4 rounded border-border-strong text-feedback-warning focus:ring-focus"
                                    />
                                    {t('teamProfiles.markAsWeakness')}
                                </label>
                                <div className="flex gap-2">
                                    <Button type="button" size="sm" variant="ghost" onClick={closeSkillForm}>{t('actions.cancel')}</Button>
                                    <Button type="submit" size="sm" disabled={context.loading}
                                        isLoading={createSkillMutation.isPending || updateSkillMutation.isPending}>
                                        {editingSkillId ? t('teamProfiles.saveSkill') : t('teamProfiles.addSkill')}
                                    </Button>
                                </div>
                            </form>
                        )}
                        <ul className="space-y-2">
                            {skills.map(skill => (
                                <li key={skill.id} className="flex items-center justify-between rounded-md border border-border-subtle px-3 py-2">
                                    <div>
                                        <div className="text-sm font-medium text-content-primary">{skill.skill_name}</div>
                                        <div className="text-xs text-content-secondary">{summaryLine(skill)}</div>
                                    </div>
                                    <div className="flex gap-1">
                                        <Button type="button" size="sm" variant="ghost" onClick={() => editSkill(skill)}>{t('actions.edit')}</Button>
                                        <Button type="button" size="sm" variant="ghost" className="text-feedback-danger-foreground"
                                            aria-label={`${t('actions.delete')} ${skill.skill_name}`} onClick={() => void confirmSkillDelete(skill)}>
                                            <Trash2 className="h-4 w-4" aria-hidden="true" />
                                        </Button>
                                    </div>
                                </li>
                            ))}
                            {skills.length === 0 && <li className="text-sm text-content-tertiary">{t('teamProfiles.noSkills')}</li>}
                        </ul>
                    </section>
                )}

                {profileId !== null && (
                    <PersonCapacity profileId={profileId} manage label={t('teamProfiles.defaultAvailability')} />
                )}
                {confirmationDialog}
            </div>
        </SlideOverDrawer>
    );
};

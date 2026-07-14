import { useMemo, useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { Plus, Trash2 } from 'lucide-react';
import { teamService } from '../../services/teamService';
import { getApiErrorMessage } from '../../utils/apiError';
import { Button } from '../common/Button';
import { Input } from '../common/Input';
import { useConfirmDialog } from '../common/useConfirmDialog';
import { QueryErrorState } from '../feedback/QueryState';
import type {
    TeamMemberProfile,
    TeamMemberProfileCreate,
    TeamMemberProfileSkill,
    TeamMemberProfileSkillCreate,
} from '../../types/team';

const emptyProfileForm: TeamMemberProfileCreate = {
    display_name: '',
    email: '',
    headline: '',
    summary: '',
    notes: '',
    automation_enabled: true,
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

interface TeamProfileManagerProps {
    currentIterationId?: number | null;
    currentIterationName?: string | null;
    assignedProfileIds?: number[];
    onAssignProfile?: (profile: TeamMemberProfile) => void;
}

export const TeamProfileManager = ({
    currentIterationId = null,
    currentIterationName = null,
    assignedProfileIds = [],
    onAssignProfile,
}: TeamProfileManagerProps) => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const [selectedProfileId, setSelectedProfileId] = useState<number | null>(null);
    const [profileForm, setProfileForm] = useState<TeamMemberProfileCreate>(emptyProfileForm);
    const [editingProfileId, setEditingProfileId] = useState<number | null>(null);
    const [skillForm, setSkillForm] = useState<TeamMemberProfileSkillCreate>(emptySkillForm);
    const [editingSkillId, setEditingSkillId] = useState<number | null>(null);
    const [error, setError] = useState<string | null>(null);
    const { requestConfirmation, confirmationDialog } = useConfirmDialog();

    const { data: profiles = [], error: profilesError, refetch: refetchProfiles } = useQuery({
        queryKey: ['teamMemberProfiles'],
        queryFn: teamService.getProfiles,
    });

    const selectedProfile = useMemo(
        () => profiles.find(profile => profile.id === selectedProfileId) ?? profiles[0] ?? null,
        [profiles, selectedProfileId],
    );
    const assignedProfileIdSet = useMemo(
        () => new Set(assignedProfileIds),
        [assignedProfileIds],
    );

    const invalidate = () => {
        queryClient.invalidateQueries({ queryKey: ['teamMemberProfiles'] });
        queryClient.invalidateQueries({ queryKey: ['team'] });
        queryClient.invalidateQueries({ queryKey: ['assigneeRecommendations'] });
    };

    const createProfileMutation = useMutation({
        mutationFn: (data: TeamMemberProfileCreate) => teamService.createProfile(data),
        onSuccess: profile => {
            invalidate();
            setSelectedProfileId(profile.id);
            setProfileForm(emptyProfileForm);
            setEditingProfileId(null);
        },
        onError: err => setError(getApiErrorMessage(err, t('teamProfiles.failedSaveProfile'))),
    });

    const updateProfileMutation = useMutation({
        mutationFn: ({ id, data }: { id: number; data: TeamMemberProfileCreate }) => teamService.updateProfile(id, data),
        onSuccess: profile => {
            invalidate();
            setSelectedProfileId(profile.id);
            setProfileForm(emptyProfileForm);
            setEditingProfileId(null);
        },
        onError: err => setError(getApiErrorMessage(err, t('teamProfiles.failedSaveProfile'))),
    });

    const deleteProfileMutation = useMutation({
        mutationFn: teamService.deleteProfile,
        onSuccess: () => {
            invalidate();
            setSelectedProfileId(null);
        },
        onError: err => setError(getApiErrorMessage(err, t('teamProfiles.failedDeleteProfile'))),
    });

    const createSkillMutation = useMutation({
        mutationFn: ({ profileId, data }: { profileId: number; data: TeamMemberProfileSkillCreate }) => teamService.createProfileSkill(profileId, data),
        onSuccess: () => {
            invalidate();
            setSkillForm(emptySkillForm);
            setEditingSkillId(null);
        },
        onError: err => setError(getApiErrorMessage(err, t('teamProfiles.failedSaveSkill'))),
    });

    const updateSkillMutation = useMutation({
        mutationFn: ({ profileId, skillId, data }: { profileId: number; skillId: number; data: TeamMemberProfileSkillCreate }) => teamService.updateProfileSkill(profileId, skillId, data),
        onSuccess: () => {
            invalidate();
            setSkillForm(emptySkillForm);
            setEditingSkillId(null);
        },
        onError: err => setError(getApiErrorMessage(err, t('teamProfiles.failedSaveSkill'))),
    });

    const deleteSkillMutation = useMutation({
        mutationFn: ({ profileId, skillId }: { profileId: number; skillId: number }) => teamService.deleteProfileSkill(profileId, skillId),
        onSuccess: invalidate,
        onError: err => setError(getApiErrorMessage(err, t('teamProfiles.failedDeleteSkill'))),
    });

    const submitProfile = (event: React.FormEvent) => {
        event.preventDefault();
        setError(null);
        const data = {
            ...profileForm,
            display_name: profileForm.display_name.trim(),
            email: optionalText(profileForm.email),
            headline: optionalText(profileForm.headline),
            summary: optionalText(profileForm.summary),
            notes: optionalText(profileForm.notes),
        };
        if (editingProfileId) {
            updateProfileMutation.mutate({ id: editingProfileId, data });
        } else {
            createProfileMutation.mutate(data);
        }
    };

    const editProfile = (profile: TeamMemberProfile) => {
        setEditingProfileId(profile.id);
        setSelectedProfileId(profile.id);
        setProfileForm({
            display_name: profile.display_name,
            email: profile.email || '',
            headline: profile.headline || '',
            summary: profile.summary || '',
            notes: profile.notes || '',
            automation_enabled: profile.automation_enabled,
        });
    };

    const submitSkill = (event: React.FormEvent) => {
        event.preventDefault();
        if (!selectedProfile) return;
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
        if (editingSkillId) {
            updateSkillMutation.mutate({ profileId: selectedProfile.id, skillId: editingSkillId, data });
        } else {
            createSkillMutation.mutate({ profileId: selectedProfile.id, data });
        }
    };

    const editSkill = (skill: TeamMemberProfileSkill) => {
        setEditingSkillId(skill.id);
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

    return (
        <div className="grid grid-cols-1 gap-4 lg:grid-cols-[minmax(0,1fr)_360px]">
            {profilesError && <QueryErrorState className="lg:col-span-2" error={profilesError} onRetry={() => void refetchProfiles()} />}
            <div className="card p-4">
                <div className="mb-4 flex items-center justify-between">
                    <div>
                        <h2 className="text-lg font-semibold text-content-primary">{t('teamProfiles.title')}</h2>
                        <p className="text-sm text-content-secondary">
                            {t('teamProfiles.description')}
                        </p>
                    </div>
                </div>

                {error && <div className="mb-3 rounded-md bg-feedback-danger-muted p-3 text-sm text-feedback-danger-foreground">{error}</div>}

                <div className="space-y-3">
                    {profiles.map(profile => {
                        const isAssignedToCurrentIteration = assignedProfileIdSet.has(profile.id);
                        return (
                            <div
                                key={profile.id}
                                data-testid="profile-card"
                                className={`rounded-md border p-3 transition-colors ${selectedProfile?.id === profile.id ? 'border-action bg-action-muted' : 'border-border bg-surface-card'}`}
                            >
                                <button
                                    type="button"
                                    onClick={() => setSelectedProfileId(profile.id)}
                                    className="w-full text-left"
                                >
                                    <div className="flex items-start justify-between gap-3">
                                        <div>
                                            <div className="font-medium text-content-primary">{profile.display_name}</div>
                                            <div className="text-sm text-content-secondary">{profile.headline || profile.email || t('teamProfiles.noHeadline')}</div>
                                        </div>
                                        <span className={`rounded-full px-2 py-0.5 text-xs ${profile.automation_enabled ? 'bg-feedback-success-muted text-feedback-success-foreground' : 'bg-surface-subtle text-content-secondary'}`}>
                                            {profile.automation_enabled ? t('teamProfiles.automationOn') : t('teamProfiles.automationOff')}
                                        </span>
                                    </div>
                                    <div className="mt-2 flex flex-wrap gap-1">
                                        {profile.skills.slice(0, 6).map(skill => (
                                            <span
                                                key={skill.id}
                                                className={`rounded-full px-2 py-0.5 text-xs ${skill.is_weakness ? 'bg-feedback-warning-muted text-feedback-warning-foreground' : 'bg-surface-subtle text-content-primary'}`}
                                            >
                                                {skill.skill_name} {skill.is_weakness ? t('teamProfiles.weak') : t('teamProfiles.levelCompact', { level: skill.level })}
                                            </span>
                                        ))}
                                        {profile.skills.length === 0 && (
                                            <span className="text-xs text-content-tertiary">{t('teamProfiles.noSkills')}</span>
                                        )}
                                    </div>
                                </button>
                                {currentIterationId && onAssignProfile && (
                                    <div className="mt-3 flex justify-end">
                                        <Button
                                            type="button"
                                            size="sm"
                                            variant={isAssignedToCurrentIteration ? 'outline' : 'secondary'}
                                            disabled={isAssignedToCurrentIteration}
                                            onClick={() => onAssignProfile(profile)}
                                        >
                                            {isAssignedToCurrentIteration
                                                ? t('teamProfiles.alreadyAssigned')
                                                : t('teamProfiles.addToIteration', { iteration: currentIterationName || t('teamProfiles.iterationFallback') })}
                                        </Button>
                                    </div>
                                )}
                            </div>
                        );
                    })}
                    {profiles.length === 0 && (
                        <div className="rounded-md border border-dashed border-border py-8 text-center text-sm text-content-tertiary">
                            {t('teamProfiles.empty')}
                        </div>
                    )}
                </div>
            </div>

            <div className="space-y-4">
                <form onSubmit={submitProfile} className="card space-y-3 p-4">
                    <h3 className="font-medium text-content-primary">{editingProfileId ? t('teamProfiles.editProfile') : t('teamProfiles.createProfile')}</h3>
                    <Input label={t('teamProfiles.displayName')} value={profileForm.display_name} onChange={event => setProfileForm({ ...profileForm, display_name: event.target.value })} required />
                    <Input label={t('teamProfiles.email')} type="email" value={profileForm.email || ''} onChange={event => setProfileForm({ ...profileForm, email: event.target.value })} />
                    <Input label={t('teamProfiles.headline')} value={profileForm.headline || ''} onChange={event => setProfileForm({ ...profileForm, headline: event.target.value })} placeholder={t('teamProfiles.headlinePlaceholder')} />
                    <textarea
                        value={profileForm.summary || ''}
                        onChange={event => setProfileForm({ ...profileForm, summary: event.target.value })}
                        placeholder={t('teamProfiles.summaryPlaceholder')}
                        className="min-h-[80px] w-full rounded-md border border-border-strong px-3 py-2 text-sm shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus"
                    />
                    <label className="flex items-center gap-2 text-sm text-content-primary">
                        <input
                            type="checkbox"
                            checked={profileForm.automation_enabled}
                            onChange={event => setProfileForm({ ...profileForm, automation_enabled: event.target.checked })}
                            className="h-4 w-4 rounded border-border-strong text-action focus:ring-focus"
                        />
                        {t('teamProfiles.useForRecommendations')}
                    </label>
                    <div className="flex justify-between gap-2">
                        {editingProfileId && (
                            <Button type="button" variant="ghost" onClick={() => {
                                setEditingProfileId(null);
                                setProfileForm(emptyProfileForm);
                            }}>
                                {t('actions.cancel')}
                            </Button>
                        )}
                        <Button type="submit" isLoading={createProfileMutation.isPending || updateProfileMutation.isPending}>
                            <Plus className="mr-2 h-4 w-4" />
                            {editingProfileId ? t('teamProfiles.save') : t('teamProfiles.create')}
                        </Button>
                    </div>
                </form>

                {selectedProfile && (
                    <div className="card space-y-3 p-4">
                        <div className="flex items-center justify-between gap-2">
                            <h3 className="font-medium text-content-primary">{selectedProfile.display_name}</h3>
                            <div className="flex gap-1">
                                <Button type="button" size="sm" variant="ghost" onClick={() => editProfile(selectedProfile)}>{t('actions.edit')}</Button>
                                <Button
                                    type="button"
                                    size="sm"
                                    variant="ghost"
                                    className="text-feedback-danger-foreground"
                                    aria-label={t('actions.delete')}
                                    onClick={() => requestConfirmation({
                                        title: t('actions.delete'),
                                        description: t('teamProfiles.deleteProfileConfirm', { name: selectedProfile.display_name }),
                                        confirmLabel: t('actions.delete'),
                                        cancelLabel: t('actions.cancel'),
                                        closeLabel: t('actions.close'),
                                        onConfirm: () => deleteProfileMutation.mutateAsync(selectedProfile.id),
                                    })}
                                >
                                    <Trash2 className="h-4 w-4" />
                                </Button>
                            </div>
                        </div>

                        <form onSubmit={submitSkill} className="space-y-2 rounded-md border border-border-subtle bg-surface-muted p-3">
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
                                onChange={event => setSkillForm({
                                    ...skillForm,
                                    keywords_json: event.target.value.split(',').map(item => item.trim()).filter(Boolean),
                                })}
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
                                {editingSkillId && (
                                    <Button
                                        type="button"
                                        size="sm"
                                        variant="ghost"
                                        onClick={() => {
                                            setEditingSkillId(null);
                                            setSkillForm(emptySkillForm);
                                        }}
                                    >
                                        {t('actions.cancel')}
                                    </Button>
                                )}
                                <Button
                                    type="submit"
                                    size="sm"
                                    isLoading={createSkillMutation.isPending || updateSkillMutation.isPending}
                                >
                                    {editingSkillId ? t('teamProfiles.saveSkill') : t('teamProfiles.addSkill')}
                                </Button>
                            </div>
                        </form>

                        <div className="space-y-2">
                            {selectedProfile.skills.map(skill => (
                                <div key={skill.id} className="flex items-center justify-between rounded-md border border-border-subtle px-3 py-2">
                                    <div>
                                        <div className="text-sm font-medium text-content-primary">{skill.skill_name}</div>
                                        <div className="text-xs text-content-secondary">
                                            {skill.is_weakness
                                                ? t('teamProfiles.skillSummaryWeakness', {
                                                    summary: t('teamProfiles.skillSummary', {
                                                        category: skill.category || t('teamProfiles.uncategorized'),
                                                        level: skill.level,
                                                        interest: skill.interest,
                                                    }),
                                                })
                                                : t('teamProfiles.skillSummary', {
                                                    category: skill.category || t('teamProfiles.uncategorized'),
                                                    level: skill.level,
                                                    interest: skill.interest,
                                                })}
                                        </div>
                                    </div>
                                    <div className="flex gap-1">
                                        <Button type="button" size="sm" variant="ghost" onClick={() => editSkill(skill)}>
                                            {t('actions.edit')}
                                        </Button>
                                        <Button
                                            type="button"
                                            size="sm"
                                            variant="ghost"
                                            className="text-feedback-danger-foreground"
                                            aria-label={t('actions.delete')}
                                            onClick={() => requestConfirmation({
                                                title: t('actions.delete'),
                                                description: skill.skill_name,
                                                confirmLabel: t('actions.delete'),
                                                cancelLabel: t('actions.cancel'),
                                                closeLabel: t('actions.close'),
                                                onConfirm: () => deleteSkillMutation.mutateAsync({ profileId: selectedProfile.id, skillId: skill.id }),
                                            })}
                                        >
                                            <Trash2 className="h-4 w-4" />
                                        </Button>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
                {confirmationDialog}
            </div>
        </div>
    );
};

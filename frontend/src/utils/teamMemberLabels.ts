import type { TeamMemberOption, TeamMemberProfileCompact } from '../types/team';
import i18n from '../i18n/i18n';

const t = i18n.t.bind(i18n);

type TeamMemberLabelSource = Pick<TeamMemberOption, 'name' | 'position' | 'iteration_name'>;
type TeamMemberProfileLabelSource = Pick<TeamMemberProfileCompact, 'display_name' | 'headline' | 'email'>;

export const formatTeamMemberLabel = (member: TeamMemberLabelSource) => {
    const parts = [member.name, member.position, member.iteration_name]
        .map(part => part?.trim())
        .filter((part): part is string => Boolean(part));

    return parts.length > 0 ? parts.join(' - ') : t('common.unknownMember');
};

export const formatOwnerLabel = (
    owner?: TeamMemberLabelSource | null,
    ownerId?: number | null,
    emptyLabel?: string,
) => {
    if (owner) {
        return formatTeamMemberLabel(owner);
    }

    if (ownerId) {
        return t('common.ownerNumber', { id: ownerId });
    }

    return emptyLabel ?? t('common.unassigned');
};

export const formatTeamMemberProfileLabel = (profile: TeamMemberProfileLabelSource) => {
    const parts = [profile.display_name, profile.headline || profile.email]
        .map(part => part?.trim())
        .filter((part): part is string => Boolean(part));

    return parts.length > 0 ? parts.join(' - ') : t('common.unknownProfile');
};

export const formatPortfolioOwnerLabel = (
    ownerProfile?: TeamMemberProfileLabelSource | null,
    legacyOwner?: TeamMemberLabelSource | null,
    legacyOwnerId?: number | null,
    emptyLabel?: string,
) => {
    if (ownerProfile) {
        return formatTeamMemberProfileLabel(ownerProfile);
    }

    return formatOwnerLabel(legacyOwner, legacyOwnerId, emptyLabel);
};

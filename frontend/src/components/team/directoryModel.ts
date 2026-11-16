import type { AgentActorRosterItem, AgentModelBinding } from '../../types/agent';
import type { TeamMemberProfile, TeamMemberProfileSkill } from '../../types/team';

export type DirectoryKind = 'person' | 'agent';
export type DirectoryRole = 'pm' | 'worker' | 'reviewer';
/** Connected and Not connected are read from the roster; Unknown means the roster could not be read. */
export type ConnectionState = 'connected' | 'not_connected' | 'unknown';

/** An agent counts as connected when it has been seen by the server this recently. */
export const CONNECTED_WINDOW_MS = 15 * 60 * 1000;

export interface DirectoryRow {
    key: string;
    kind: DirectoryKind;
    name: string;
    /** Absent for an agent that has no profile yet. */
    profile: TeamMemberProfile | null;
    /** Absent for people, and for agents whose roster could not be read. */
    actor: AgentActorRosterItem | null;
    roles: DirectoryRole[];
    skills: TeamMemberProfileSkill[];
    /** The agent's default model; null when it has none, undefined when it cannot be read. */
    model: AgentModelBinding | null | undefined;
    connection: ConnectionState | null;
}

export type RosterState = 'loaded' | 'unavailable';

const ACTOR_ROLES: Record<string, DirectoryRole> = { pm: 'pm', worker: 'worker', verifier: 'reviewer' };
const MODE_ROLES: Record<string, DirectoryRole> = { ownership: 'pm', execution: 'worker', verification: 'reviewer' };

const unique = <T,>(items: T[]) => [...new Set(items)];

export const connectionOf = (actor: AgentActorRosterItem, now: number): ConnectionState => {
    if (!actor.enabled || actor.lifecycle_state === 'disabled' || !actor.last_seen_at) return 'not_connected';
    const seen = Date.parse(actor.last_seen_at);
    return Number.isFinite(seen) && now - seen <= CONNECTED_WINDOW_MS ? 'connected' : 'not_connected';
};

export const defaultBinding = (actor: AgentActorRosterItem): AgentModelBinding | null => {
    const usable = actor.eligible_model_bindings.filter(binding => binding.enabled);
    return usable.find(binding => binding.is_default) ?? usable[0] ?? null;
};

export const modelName = (binding: AgentModelBinding) => (
    binding.model_catalog?.configured_model_alias ?? binding.model_catalog_key ?? ''
);

const profileRoles = (profile: TeamMemberProfile) => unique(
    profile.assignment_modes.map(mode => MODE_ROLES[mode]).filter((role): role is DirectoryRole => Boolean(role)),
);

/**
 * One list of everyone who can do work. A profile is an agent when its kind says so or when an
 * agent actor is linked to it; an actor without a profile is listed on its own.
 */
export const buildDirectory = (
    profiles: TeamMemberProfile[],
    roster: AgentActorRosterItem[],
    rosterState: RosterState,
    now: number = Date.now(),
): DirectoryRow[] => {
    const known = rosterState === 'loaded';
    const actorByProfile = new Map<number, AgentActorRosterItem>();
    for (const actor of roster) if (actor.profile_id != null && !actorByProfile.has(actor.profile_id)) actorByProfile.set(actor.profile_id, actor);

    const agentRow = (key: string, name: string, profile: TeamMemberProfile | null, actor: AgentActorRosterItem | null): DirectoryRow => ({
        key,
        kind: 'agent',
        name,
        profile,
        actor,
        roles: actor ? [ACTOR_ROLES[actor.role]].filter(Boolean) : profile ? profileRoles(profile) : [],
        skills: profile?.skills ?? [],
        model: !known ? undefined : actor ? defaultBinding(actor) : null,
        connection: !known ? 'unknown' : actor ? connectionOf(actor, now) : 'not_connected',
    });

    const rows: DirectoryRow[] = profiles.map(profile => {
        const actor = actorByProfile.get(profile.id) ?? null;
        if (actor || profile.profile_kind === 'agent') return agentRow(`profile-${profile.id}`, profile.display_name, profile, actor);
        return {
            key: `profile-${profile.id}`,
            kind: 'person',
            name: profile.display_name,
            profile,
            actor: null,
            roles: profileRoles(profile),
            skills: profile.skills,
            model: null,
            connection: null,
        };
    });
    for (const actor of roster) {
        if (actor.profile_id != null && profiles.some(profile => profile.id === actor.profile_id)) continue;
        rows.push(agentRow(`actor-${actor.id}`, actor.display_name || actor.name, null, actor));
    }
    return rows.sort((a, b) => a.name.localeCompare(b.name));
};

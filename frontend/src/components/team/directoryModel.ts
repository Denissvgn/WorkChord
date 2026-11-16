import type { AgentActorRosterItem, AgentModelBinding } from '../../types/agent';
import type { TeamMemberProfile, TeamMemberProfileSkill } from '../../types/team';

export type DirectoryKind = 'person' | 'agent';
export type DirectoryRole = 'pm' | 'worker' | 'reviewer';
/** Connected and Not connected are read from the roster; Unknown means the roster could not be read. */
export type ConnectionState = 'connected' | 'not_connected' | 'unknown';

/** An agent counts as connected when it has been seen by the server this recently. */
export const CONNECTED_WINDOW_MS = 15 * 60 * 1000;

/** Loaded: the roster was read in this request. Loading: the first read is under way. Unavailable: no key, or the read failed. */
export type RosterState = 'loaded' | 'loading' | 'unavailable';

/** What an agent's model and connection cells show. */
export interface AgentStatus {
    /** The default model; null when it has none, undefined when it is Unknown. */
    model: AgentModelBinding | null | undefined;
    connection: ConnectionState;
}

/** One agent actor as read from the roster: a profile can have several, for example a Worker and a Reviewer. */
export interface DirectoryActor {
    actor: AgentActorRosterItem;
    role: DirectoryRole | null;
    status: AgentStatus;
}

export interface DirectoryRow {
    key: string;
    kind: DirectoryKind;
    name: string;
    /** Absent for an agent that has no profile yet. */
    profile: TeamMemberProfile | null;
    /** Every agent actor of this row, in role order. Empty for people, and for agents whose roster could not be read. */
    actors: DirectoryActor[];
    roles: DirectoryRole[];
    skills: TeamMemberProfileSkill[];
    /** The first actor's model, and Connected when any of the row's actors is connected; null for people. */
    status: AgentStatus | null;
    /** Whether the roster behind every status on this row could be read. */
    rosterState: RosterState;
}

const ROLE_ORDER: DirectoryRole[] = ['pm', 'worker', 'reviewer'];
const ACTOR_ROLES: Record<string, DirectoryRole> = { pm: 'pm', worker: 'worker', verifier: 'reviewer' };
const MODE_ROLES: Record<string, DirectoryRole> = { ownership: 'pm', execution: 'worker', verification: 'reviewer' };

const inRoleOrder = (roles: (DirectoryRole | null | undefined)[]) => ROLE_ORDER.filter(role => roles.includes(role));

const rolePosition = (role: DirectoryRole | null) => (role ? ROLE_ORDER.indexOf(role) : ROLE_ORDER.length);

const connectionOf = (actor: AgentActorRosterItem, now: number): Exclude<ConnectionState, 'unknown'> => {
    if (!actor.enabled || actor.lifecycle_state === 'disabled' || !actor.last_seen_at) return 'not_connected';
    const seen = Date.parse(actor.last_seen_at);
    return Number.isFinite(seen) && now - seen <= CONNECTED_WINDOW_MS ? 'connected' : 'not_connected';
};

const defaultBinding = (actor: AgentActorRosterItem): AgentModelBinding | null => {
    const usable = actor.eligible_model_bindings.filter(binding => binding.enabled);
    return usable.find(binding => binding.is_default) ?? usable[0] ?? null;
};

export const modelName = (binding: AgentModelBinding) => (
    binding.model_catalog?.configured_model_alias ?? binding.model_catalog_key ?? ''
);

export const actorName = (actor: AgentActorRosterItem) => actor.display_name || actor.name;

const UNKNOWN_STATUS: AgentStatus = { model: undefined, connection: 'unknown' };

/**
 * The only place a model or connection is read from roster data. It says Unknown whenever the roster
 * is not loaded, so actors cached from an earlier read never show a state after a refresh fails.
 */
export const agentStatus = (actors: AgentActorRosterItem[], rosterState: RosterState, now: number): AgentStatus => {
    if (rosterState !== 'loaded') return UNKNOWN_STATUS;
    return {
        model: actors[0] ? defaultBinding(actors[0]) : null,
        connection: actors.some(actor => connectionOf(actor, now) === 'connected') ? 'connected' : 'not_connected',
    };
};

/** True when a status was read from the roster rather than left Unknown. */
export const statusKnown = (status: AgentStatus | null): status is AgentStatus => status !== null && status.connection !== 'unknown';

/** The role that tells this actor apart within its row, or null when it has none or shares it with another actor. */
export const distinctRole = (row: DirectoryRow, entry: DirectoryActor): DirectoryRole | null => (
    entry.role && row.actors.filter(other => other.role === entry.role).length === 1 ? entry.role : null
);

const profileRoles = (profile: TeamMemberProfile) => inRoleOrder(profile.assignment_modes.map(mode => MODE_ROLES[mode]));

const directoryActor = (actor: AgentActorRosterItem, rosterState: RosterState, now: number): DirectoryActor => ({
    actor,
    role: ACTOR_ROLES[actor.role] ?? null,
    status: agentStatus([actor], rosterState, now),
});

/**
 * One list of everyone who can do work. A profile is an agent when its kind says so or when an
 * agent actor is linked to it; every actor linked to a profile is kept on that profile's row, and
 * an actor without a profile is listed on its own.
 */
export const buildDirectory = (
    profiles: TeamMemberProfile[],
    roster: AgentActorRosterItem[],
    rosterState: RosterState,
    now: number = Date.now(),
): DirectoryRow[] => {
    const profileIds = new Set(profiles.map(profile => profile.id));
    const actorsByProfile = new Map<number, DirectoryActor[]>();
    const unlinked: DirectoryActor[] = [];
    for (const actor of roster) {
        const entry = directoryActor(actor, rosterState, now);
        if (actor.profile_id != null && profileIds.has(actor.profile_id)) {
            actorsByProfile.set(actor.profile_id, [...(actorsByProfile.get(actor.profile_id) ?? []), entry]);
        } else {
            unlinked.push(entry);
        }
    }

    const agentRow = (key: string, name: string, profile: TeamMemberProfile | null, linked: DirectoryActor[]): DirectoryRow => {
        const actors = [...linked].sort((a, b) => rolePosition(a.role) - rolePosition(b.role) || a.actor.id - b.actor.id);
        const actorRoles = inRoleOrder(actors.map(entry => entry.role));
        return {
            key,
            kind: 'agent',
            name,
            profile,
            actors,
            roles: actorRoles.length || !profile ? actorRoles : profileRoles(profile),
            skills: profile?.skills ?? [],
            status: agentStatus(actors.map(entry => entry.actor), rosterState, now),
            rosterState,
        };
    };

    const rows: DirectoryRow[] = profiles.map(profile => {
        const linked = actorsByProfile.get(profile.id) ?? [];
        if (linked.length || profile.profile_kind === 'agent') return agentRow(`profile-${profile.id}`, profile.display_name, profile, linked);
        return {
            key: `profile-${profile.id}`,
            kind: 'person',
            name: profile.display_name,
            profile,
            actors: [],
            roles: profileRoles(profile),
            skills: profile.skills,
            status: null,
            rosterState,
        };
    });
    for (const entry of unlinked) rows.push(agentRow(`actor-${entry.actor.id}`, actorName(entry.actor), null, [entry]));
    return rows.sort((a, b) => a.name.localeCompare(b.name));
};

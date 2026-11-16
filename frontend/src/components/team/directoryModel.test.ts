import { describe, expect, it } from 'vitest';
import type { AgentActorRosterItem, AgentModelBinding } from '../../types/agent';
import type { TeamMemberProfile } from '../../types/team';
import { buildDirectory } from './directoryModel';

const NOW = Date.parse('2026-07-28T10:05:00Z');

const profile = (overrides: Partial<TeamMemberProfile>): TeamMemberProfile => ({
    id: 1, seed_key: null, display_name: 'Shared Agent', email: null, headline: null, summary: null, notes: null,
    automation_enabled: true, profile_kind: 'agent', assignment_modes: [], skills: [], created_at: '', updated_at: '',
    ...overrides,
});

const binding = (id: number, alias: string): AgentModelBinding => ({
    id, actor_id: id, model_catalog_id: id, is_default: true, enabled: true, tool_tags: [], data_policy_tags: [],
    revision: 1, model_catalog_key: alias, selectable: true, live_assignment_count: 0, historical_assignment_count: 0,
    run_reference_count: 0, created_at: '', updated_at: '',
    model_catalog: {
        id, key: alias, provider: 'anthropic', configured_model_alias: alias, reasoning_tier: 3, context_tier: 'large',
        modality_tags: [], cost_tier: 'medium', latency_tier: 'balanced', enabled: true, revision: 1,
        last_verified_at: null, created_at: '', updated_at: '',
    },
});

const actor = (overrides: Partial<AgentActorRosterItem>): AgentActorRosterItem => ({
    id: 9, name: 'worker', display_name: 'Worker Actor', scopes: [], enabled: true, role: 'worker', profile_id: 1,
    work_policy: 'default', max_parallel_work: 1, queue_revision: 1, created_at: '', last_seen_at: '2026-07-28T10:00:00Z',
    actor_revision: 1, profile_revision: null, profile: null, eligible_model_bindings: [binding(9, 'claude-sonnet-5-5')],
    queued_assignments: 0, accepted_assignments: 0, running_runs: 0,
    ...overrides,
});

describe('team directory model', () => {
    it('keeps every actor linked to one profile, with its own role, model and connection', () => {
        const reviewer = actor({ id: 10, name: 'reviewer', display_name: 'Reviewer Actor', role: 'verifier', last_seen_at: null, eligible_model_bindings: [binding(10, 'claude-opus-5-5')] });
        // The reviewer comes first in the roster; the row still lists actors in role order.
        const rows = buildDirectory([profile({})], [reviewer, actor({})], 'loaded', NOW);

        expect(rows).toHaveLength(1);
        const [row] = rows;
        expect(row.kind).toBe('agent');
        expect(row.roles).toEqual(['worker', 'reviewer']);
        expect(row.actors.map(entry => [entry.actor.id, entry.role, entry.model?.model_catalog?.configured_model_alias, entry.connection])).toEqual([
            [9, 'worker', 'claude-sonnet-5-5', 'connected'],
            [10, 'reviewer', 'claude-opus-5-5', 'not_connected'],
        ]);
        expect(row.connection).toBe('connected');
    });

    it('keeps two actors with the same role on one profile', () => {
        const rows = buildDirectory([profile({})], [actor({}), actor({ id: 11, name: 'second' })], 'loaded', NOW);
        expect(rows).toHaveLength(1);
        expect(rows[0].actors.map(entry => entry.actor.id)).toEqual([9, 11]);
        expect(rows[0].roles).toEqual(['worker']);
    });

    it('lists an actor whose profile is not in the list on its own row', () => {
        const rows = buildDirectory([profile({})], [actor({}), actor({ id: 12, display_name: 'Elsewhere', profile_id: 99 })], 'loaded', NOW);
        expect(rows.map(row => [row.key, row.actors.map(entry => entry.actor.id)])).toEqual([
            ['actor-12', [12]],
            ['profile-1', [9]],
        ]);
    });

    it('says Unknown for an agent when the roster cannot be read', () => {
        const [row] = buildDirectory([profile({ assignment_modes: ['execution'] })], [], 'unavailable', NOW);
        expect(row.actors).toEqual([]);
        expect(row.model).toBeUndefined();
        expect(row.connection).toBe('unknown');
        expect(row.roles).toEqual(['worker']);
    });
});

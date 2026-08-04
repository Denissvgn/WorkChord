import { describe, expect, it } from 'vitest';
import type { AgentTeamMaster, AgentTeamSetupStep } from '../../types/agent';
import {
    AGENT_TEAM_STEP_IDS,
    stateTone,
    stepProgress,
    stepsById,
} from './masters';
import { parseAgentTeamMasterEditor } from './manifest';

const serverSteps: AgentTeamSetupStep[] = [{
    id: 'authority',
    state: 'done',
    blocker_codes: [],
    next_action: null,
}, {
    id: 'workers',
    state: 'blocked',
    blocker_codes: ['minimum_workers_not_runtime_ready'],
    next_action: 'Acknowledge the worker runtime',
}];

describe('agent team setup master state', () => {
    it('derives progress and step state only from the server projection', () => {
        const indexed = stepsById(serverSteps);

        expect(Object.keys(indexed)).toEqual(AGENT_TEAM_STEP_IDS);
        expect(indexed.authority?.state).toBe('done');
        expect(indexed.workers?.state).toBe('blocked');
        expect(indexed.review).toBeUndefined();
        expect(stateTone(indexed.review?.state)).toBe('todo');
        expect(stepProgress(serverSteps)).toEqual({
            done: 1,
            total: 7,
        });
        expect(stepProgress(undefined)).toBeNull();
    });

    it('rejects secret-bearing fields and credential-shaped values before upload', () => {
        expect(() => parseAgentTeamMasterEditor(JSON.stringify({
            schema_version: 'agent-team-master-v1',
            api_key: 'not-allowed',
        }))).toThrow(/Secret-bearing field/);
        expect(() => parseAgentTeamMasterEditor(JSON.stringify({
            schema_version: 'agent-team-master-v1',
            runtime_ref: `pmag_${'a'.repeat(24)}`,
        }))).toThrow(/Credential-shaped value/);
    });

    it('parses a secret-free object without inventing completion state', () => {
        const value = {
            schema_version: 'agent-team-master-v1',
            topology_key: 'delivery-team',
        };

        expect(parseAgentTeamMasterEditor(
            JSON.stringify(value),
        )).toEqual(value as unknown as AgentTeamMaster);
    });
});

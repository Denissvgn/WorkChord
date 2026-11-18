import { describe, expect, it } from 'vitest';
import { AGENT_DISPATCH_LABEL_KEY, agentDispatchState, taskAgentDispatchState } from './agentDispatch';
import type { AgentDispatchFacts } from './agentDispatch';
import { englishResources } from '../i18n/resources.en';

describe('agentDispatchState', () => {
    it('says no agent is connected when there is no live assignment and no agent connected to the profile', () => {
        expect(agentDispatchState({ status: 'planned', liveAssignment: false, runBegun: false, agentConnected: false })).toBe('noAgentConnected');
    });

    it('says the task is not sent yet when a connected agent has no live assignment', () => {
        expect(agentDispatchState({ status: 'planned', liveAssignment: false, runBegun: false, agentConnected: true })).toBe('notSentYet');
        expect(agentDispatchState({ status: 'active', liveAssignment: false, runBegun: false, agentConnected: true })).toBe('notSentYet');
    });

    it('says queued when an assignment holds the task but its run has not begun', () => {
        expect(agentDispatchState({ status: 'planned', liveAssignment: true, runBegun: false, agentConnected: true })).toBe('queued');
        // A queued assignment names an agent, so a missing connection does not hide it.
        expect(agentDispatchState({ status: 'planned', liveAssignment: true, runBegun: false, agentConnected: false })).toBe('queued');
    });

    it('says working once a run has begun', () => {
        expect(agentDispatchState({ status: 'active', liveAssignment: true, runBegun: true, agentConnected: true })).toBe('working');
    });

    it('says waiting for review once the work is submitted', () => {
        expect(agentDispatchState({ status: 'resolved', liveAssignment: false, runBegun: false, agentConnected: true })).toBe('waitingForReview');
    });

    it('shows no line on a closed task', () => {
        expect(agentDispatchState({ status: 'closed', liveAssignment: false, runBegun: false, agentConnected: false })).toBeNull();
        expect(agentDispatchState({ status: 'closed', liveAssignment: false, runBegun: false, agentConnected: true })).toBeNull();
    });

    it('says the agent status is unknown only while a fact it needs is not known', () => {
        // The team read that says whether the agent is connected is loading or failed.
        expect(agentDispatchState({ status: 'planned', liveAssignment: false, runBegun: false })).toBe('unknown');
        // Without the live-assignment flag, a profile may still hold queued work.
        expect(agentDispatchState({ status: 'planned', liveAssignment: null, runBegun: false, agentConnected: false })).toBe('unknown');
        expect(agentDispatchState({ status: 'active', runBegun: false, agentConnected: true })).toBe('unknown');
    });

    it('gives an open agent task exactly one of the listed lines, each with its own label', () => {
        const listed = new Set(['noAgentConnected', 'notSentYet', 'queued', 'working', 'waitingForReview', 'unknown']);
        const seen = new Set<string>();
        for (const status of ['planned', 'active', 'resolved'] as const)
            for (const liveAssignment of [true, false, null, undefined])
                for (const runBegun of [true, false])
                    for (const agentConnected of [true, false, undefined]) {
                        const facts: AgentDispatchFacts = { status, liveAssignment, runBegun, agentConnected };
                        const state = agentDispatchState(facts);
                        expect(state).not.toBeNull();
                        expect(listed.has(state as string)).toBe(true);
                        seen.add(state as string);
                    }
        expect(seen).toEqual(listed);
        const labels = Object.values(AGENT_DISPATCH_LABEL_KEY).map(key => key.split('.').reduce<unknown>((node, part) => (node as Record<string, unknown>)[part], englishResources.translation));
        expect(labels).toEqual(['No agent connected', 'Not sent to the agent yet', 'Queued', 'Working', 'Waiting for review', 'Agent status unknown']);
    });

    it('reads the facts from the task fields the API returns', () => {
        const claim = { id: 3, name: 'builder', display_name: 'Builder' };
        expect(taskAgentDispatchState({ status: 'planned', agent_working: false, claimed_by: null }, false)).toBe('noAgentConnected');
        expect(taskAgentDispatchState({ status: 'planned', agent_working: false, claimed_by: null }, true)).toBe('notSentYet');
        expect(taskAgentDispatchState({ status: 'planned', agent_working: true, claimed_by: null }, true)).toBe('queued');
        expect(taskAgentDispatchState({ status: 'active', agent_working: true, claimed_by: claim }, true)).toBe('working');
        expect(taskAgentDispatchState({ status: 'resolved', agent_working: false, claimed_by: null }, true)).toBe('waitingForReview');
        expect(taskAgentDispatchState({ status: 'closed', agent_working: false, claimed_by: null }, true)).toBeNull();
        expect(taskAgentDispatchState({ status: 'planned', agent_working: false, claimed_by: null }, undefined)).toBe('unknown');
    });
});

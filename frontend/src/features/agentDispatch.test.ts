import { describe, expect, it } from 'vitest';
import { agentDispatchState, taskAgentDispatchState } from './agentDispatch';

describe('agentDispatchState', () => {
    it('says no agent is connected when there is no live assignment and no agent bound to the profile', () => {
        expect(agentDispatchState({ status: 'planned', liveAssignment: false, runBegun: false, agentBound: false })).toBe('noAgentConnected');
    });

    it('says queued when an assignment holds the task but its run has not begun', () => {
        expect(agentDispatchState({ status: 'planned', liveAssignment: true, runBegun: false, agentBound: true })).toBe('queued');
        // A queued assignment names an agent, so a missing binding does not hide it.
        expect(agentDispatchState({ status: 'planned', liveAssignment: true, runBegun: false, agentBound: false })).toBe('queued');
    });

    it('says working once a run has begun', () => {
        expect(agentDispatchState({ status: 'active', liveAssignment: true, runBegun: true, agentBound: true })).toBe('working');
    });

    it('says waiting for review once the work is submitted', () => {
        expect(agentDispatchState({ status: 'resolved', liveAssignment: false, runBegun: false, agentBound: true })).toBe('waitingForReview');
    });

    it('says nothing when the facts do not tell', () => {
        // An idle, bound agent has nothing to report.
        expect(agentDispatchState({ status: 'planned', liveAssignment: false, runBegun: false, agentBound: true })).toBeNull();
        // A reader who may not see the agent roster cannot tell whether an agent is connected.
        expect(agentDispatchState({ status: 'planned', liveAssignment: false, runBegun: false })).toBeNull();
        // Without the live-assignment flag, an unbound profile may still hold queued work.
        expect(agentDispatchState({ status: 'planned', liveAssignment: null, runBegun: false, agentBound: false })).toBeNull();
        expect(agentDispatchState({ status: 'closed', liveAssignment: false, runBegun: false, agentBound: false })).toBeNull();
    });

    it('reads the facts from the task fields the API returns', () => {
        const claim = { id: 3, name: 'builder', display_name: 'Builder' };
        expect(taskAgentDispatchState({ status: 'planned', agent_working: false, claimed_by: null }, false)).toBe('noAgentConnected');
        expect(taskAgentDispatchState({ status: 'planned', agent_working: true, claimed_by: null }, true)).toBe('queued');
        expect(taskAgentDispatchState({ status: 'active', agent_working: true, claimed_by: claim }, true)).toBe('working');
        expect(taskAgentDispatchState({ status: 'resolved', agent_working: false, claimed_by: null }, true)).toBe('waitingForReview');
    });
});

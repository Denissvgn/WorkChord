import type { Task, TaskStatus } from '../types/task';

/**
 * Where an agent's work on a task stands, as one line under the agent's name. `unknown` is the
 * neutral line while the reads that say whether the agent is connected are loading or failed.
 */
export type AgentDispatchState = 'noAgentConnected' | 'notSentYet' | 'queued' | 'working' | 'waitingForReview' | 'unknown';

export interface AgentDispatchFacts {
    status: TaskStatus;
    /** A live execution assignment, queued or begun, holds the task (`Task.agent_working`); null or undefined when not loaded. */
    liveAssignment?: boolean | null;
    /** An agent began a run and holds the task's claim (`Task.claimed_by`). */
    runBegun: boolean;
    /** An enabled agent is bound to the assignee's profile (`profile.agent_connected`); undefined while that is not known. */
    agentConnected?: boolean;
}

/**
 * The dispatch state of a task given to an agent, from fields the task and team APIs return.
 * A submitted task waits for review, a begun run is working and an assignment not yet begun is
 * queued. Without a live assignment, a connected agent has not been sent the task yet and an
 * agent with nothing bound has no agent connected. When either fact is not known yet, the state
 * is `unknown`, so the line never claims what the data does not show. Null for a closed task.
 */
export const agentDispatchState = ({ status, liveAssignment, runBegun, agentConnected }: AgentDispatchFacts): AgentDispatchState | null => {
    if (status === 'closed') return null;
    if (status === 'resolved') return 'waitingForReview';
    if (runBegun) return 'working';
    if (liveAssignment) return 'queued';
    if (liveAssignment !== false || agentConnected === undefined) return 'unknown';
    return agentConnected ? 'notSentYet' : 'noAgentConnected';
};

/** The dispatch facts a loaded task carries; whether the agent is connected comes from the team read. */
export const taskAgentDispatchState = (
    task: Pick<Task, 'status' | 'agent_working' | 'claimed_by'>,
    agentConnected: boolean | undefined,
): AgentDispatchState | null => agentDispatchState({
    status: task.status,
    liveAssignment: task.agent_working,
    runBegun: Boolean(task.claimed_by),
    agentConnected,
});

/** Translation keys for each state, shared by every surface that shows the line. */
export const AGENT_DISPATCH_LABEL_KEY: Record<AgentDispatchState, string> = {
    noAgentConnected: 'agentDispatch.noAgentConnected',
    notSentYet: 'agentDispatch.notSentYet',
    queued: 'agentDispatch.queued',
    working: 'agentDispatch.working',
    waitingForReview: 'agentDispatch.waitingForReview',
    unknown: 'agentDispatch.unknown',
};

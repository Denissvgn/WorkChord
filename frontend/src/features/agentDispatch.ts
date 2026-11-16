import type { Task, TaskStatus } from '../types/task';

/**
 * Where an agent's work on a task stands, as one line under the agent's name. `unknown` is the
 * neutral line for a reader whose reads cannot say whether an agent is connected.
 */
export type AgentDispatchState = 'noAgentConnected' | 'queued' | 'working' | 'waitingForReview' | 'unknown';

export interface AgentDispatchFacts {
    status: TaskStatus;
    /** A live execution assignment, queued or begun, holds the task (`Task.agent_working`); null or undefined when not loaded. */
    liveAssignment?: boolean | null;
    /** An agent began a run and holds the task's claim (`Task.claimed_by`). */
    runBegun: boolean;
    /** An enabled agent is bound to the assignee's profile; undefined when this reader cannot tell. */
    agentBound?: boolean;
}

/**
 * The dispatch state of a task given to an agent, from fields the task API already returns.
 * A submitted task waits for review, a begun run is working, an assignment not yet begun is
 * queued, and with neither a live assignment nor a bound agent no agent is connected. When the
 * reader cannot tell whether a live assignment exists or an agent is bound, the state is
 * `unknown`, so the line stays and never claims what the data does not show. Null for a closed
 * task and for a bound agent with nothing to do yet.
 */
export const agentDispatchState = ({ status, liveAssignment, runBegun, agentBound }: AgentDispatchFacts): AgentDispatchState | null => {
    if (status === 'closed') return null;
    if (status === 'resolved') return 'waitingForReview';
    if (runBegun) return 'working';
    if (liveAssignment) return 'queued';
    if (liveAssignment === false && agentBound === false) return 'noAgentConnected';
    if (liveAssignment === false && agentBound === true) return null;
    return 'unknown';
};

/** The dispatch facts a loaded task carries; whether an agent is bound comes from the actor roster. */
export const taskAgentDispatchState = (
    task: Pick<Task, 'status' | 'agent_working' | 'claimed_by'>,
    agentBound: boolean | undefined,
): AgentDispatchState | null => agentDispatchState({
    status: task.status,
    liveAssignment: task.agent_working,
    runBegun: Boolean(task.claimed_by),
    agentBound,
});

/** Translation keys for each state, shared by every surface that shows the line. */
export const AGENT_DISPATCH_LABEL_KEY: Record<AgentDispatchState, string> = {
    noAgentConnected: 'agentDispatch.noAgentConnected',
    queued: 'agentDispatch.queued',
    working: 'agentDispatch.working',
    waitingForReview: 'agentDispatch.waitingForReview',
    unknown: 'agentDispatch.unknown',
};

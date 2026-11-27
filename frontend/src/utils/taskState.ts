import type { TaskDisplayedState, TaskStatus } from '../types/task';

/** What a task is shown as: the server's displayed state, or its stored status. */
export const stateOf = (task: { status: TaskStatus; displayed_state?: TaskDisplayedState | string }): TaskDisplayedState =>
    (task.displayed_state ?? task.status) as TaskDisplayedState;

/** Work that is not in play: postponed, canceled or superseded. It is never scheduled or shown as active work. */
export const STOPPED_STATES = ['postponed', 'canceled', 'superseded'] as const;
export type StoppedState = typeof STOPPED_STATES[number];
export const isStoppedState = (state: string): state is StoppedState => (STOPPED_STATES as readonly string[]).includes(state);

/** Canceled and superseded work has ended; postponed work is paused and comes back. */
export const isEndedState = (state: string) => state === 'canceled' || state === 'superseded';

/** Every state a person can filter or count by, in the order lists show them. */
export const ALL_STATES: readonly TaskDisplayedState[] = ['planned', 'active', 'resolved', 'closed', 'postponed', 'canceled', 'superseded'];

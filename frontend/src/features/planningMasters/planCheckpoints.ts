import type { IterationPlanningReadinessSummary, PlanCheckpoint } from '../../types/iteration';
import { PLANNING_STEP_IDS } from './planningReturn';
import type { PlanningStepId } from './planningReturn';

export type PlanCheckpointState = PlanCheckpoint['state'];

/** One plan section as the page shows it, read from the server's planning-readiness response. */
export interface PlanCheckpointSection {
    id: PlanningStepId;
    /** 1-based position among the six checkpoints. */
    number: number;
    state: PlanCheckpointState;
    /** For a waiting checkpoint: the earlier checkpoint it waits for. */
    waitsFor?: PlanningStepId;
    reasonCodes: string[];
    counts: Record<string, number>;
}

// The server names the checkpoint a waiting one depends on through its reason code.
const WAITS_FOR_BY_REASON: Readonly<Record<string, PlanningStepId>> = {
    add_work_first: 'work',
    build_schedule_first: 'schedule',
};

const waitsFor = (
    item: PlanCheckpoint,
    earlier: readonly PlanCheckpoint[],
): PlanningStepId | undefined => {
    if (item.state !== 'blocked') return undefined;
    for (const code of item.reason_codes) {
        if (WAITS_FOR_BY_REASON[code]) return WAITS_FOR_BY_REASON[code];
    }
    // "Complete earlier checkpoints first": the first earlier one that is not done.
    return earlier.find(previous => previous.state !== 'done')?.id ?? earlier[earlier.length - 1]?.id;
};

/**
 * The six sections in order, with the states exactly as the server reported them.
 *
 * Returns null without an iteration in scope or without a complete response (all six
 * checkpoints): no checkpoint state is ever worked out in the browser.
 */
export const planCheckpointSections = (
    summary: IterationPlanningReadinessSummary | undefined,
    { hasIteration }: { hasIteration: boolean },
): PlanCheckpointSection[] | null => {
    if (!hasIteration) return null;
    const checkpoints = summary?.checkpoints;
    if (!checkpoints) return null;
    const byId = new Map(checkpoints.map(item => [item.id, item]));
    if (PLANNING_STEP_IDS.some(id => !byId.has(id))) return null;
    const ordered = PLANNING_STEP_IDS.map(id => byId.get(id)!);
    return ordered.map((item, index) => {
        const dependency = waitsFor(item, ordered.slice(0, index));
        return {
            id: item.id,
            number: index + 1,
            state: item.state,
            ...(dependency ? { waitsFor: dependency } : {}),
            reasonCodes: item.reason_codes,
            counts: item.counts,
        };
    });
};

/** The section that opens by default: the first incomplete one, or Review once all are done. */
export const firstIncompleteCheckpoint = (sections: readonly PlanCheckpointSection[]): PlanningStepId => (
    sections.find(section => section.state !== 'done')?.id ?? 'review'
);

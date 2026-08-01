import type {
    AgentCommandMetadata,
    TaskDifficultyAxes,
    TaskDifficultyBand,
    TaskReviewMode,
} from '../types/agent';

export const MODEL_AWARE_ROUTING_FEATURE = 'model-aware-routing-v1';

export const ASSESSMENT_REASON_CODES = [
    'novel-architecture',
    'material-ambiguity',
    'broad-context',
    'security',
    'authorization',
    'migration',
    'data-integrity',
    'concurrency',
    'production',
    'irreversible-change',
    'independent-verification',
    'specialist-verification',
] as const;

export type AssessmentReasonCode = typeof ASSESSMENT_REASON_CODES[number];

const ADVANCED_REASON_CODES = new Set<AssessmentReasonCode>(ASSESSMENT_REASON_CODES);

const INDEPENDENT_REASON_CODES = new Set<AssessmentReasonCode>([
    'security',
    'authorization',
    'migration',
    'data-integrity',
    'concurrency',
    'production',
    'irreversible-change',
    'independent-verification',
    'specialist-verification',
]);

const STANDARD_REVIEW_REASON_CODES = new Set<AssessmentReasonCode>([
    'novel-architecture',
    'material-ambiguity',
    'broad-context',
]);

const REVIEW_ORDER: Record<TaskReviewMode, number> = {
    none: 0,
    standard: 1,
    independent: 2,
    'specialist-independent': 3,
};

const AGENT_AUDIT_RATIONALE_MAX_LENGTH = 2_000;
const AGENT_AUDIT_RATIONALE_FALLBACK = 'See command payload rationale.';

export const deriveDifficultyBand = (
    axes: TaskDifficultyAxes,
    reasonCodes: readonly string[],
): TaskDifficultyBand => {
    const values = Object.values(axes);
    if (values.some(value => value === 3)) return 'advanced';
    if (reasonCodes.some(code => ADVANCED_REASON_CODES.has(code as AssessmentReasonCode))) {
        return 'advanced';
    }
    if (values.every(value => value === 1)) return 'routine';
    return 'standard';
};

export const minimumReviewMode = (
    axes: TaskDifficultyAxes,
    reasonCodes: readonly string[],
): TaskReviewMode => {
    if (reasonCodes.includes('specialist-verification')) {
        return 'specialist-independent';
    }
    if (
        axes.risk === 3
        || axes.verification_burden === 3
        || reasonCodes.some(code => INDEPENDENT_REASON_CODES.has(code as AssessmentReasonCode))
    ) {
        return 'independent';
    }
    if (reasonCodes.some(code => STANDARD_REVIEW_REASON_CODES.has(code as AssessmentReasonCode))) {
        return 'standard';
    }
    return 'none';
};

export const reviewModeMeets = (
    actual: TaskReviewMode,
    minimum: TaskReviewMode,
) => REVIEW_ORDER[actual] >= REVIEW_ORDER[minimum];

export const parseRoutingTags = (value: string) => (
    Array.from(new Set(
        value
            .split(',')
            .map(item => item.trim().toLowerCase())
            .filter(Boolean),
    )).sort()
);

export const formatRoutingCode = (value: string) => (
    value
        .replace(/[_-]+/g, ' ')
        .replace(/\b\w/g, character => character.toUpperCase())
);

const randomId = () => {
    if (typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function') {
        return crypto.randomUUID();
    }
    return `${Date.now()}-${Math.random().toString(16).slice(2)}`;
};

export const toAgentAuditRationale = (rationale: string) => {
    const controlSafe = Array.from(rationale, character => {
        const codePoint = character.codePointAt(0) ?? 0;
        return codePoint < 32 || codePoint === 127 ? ' ' : character;
    }).join('');
    const singleLine = controlSafe.replace(/\s+/g, ' ').trim();
    const bounded = Array.from(singleLine)
        .slice(0, AGENT_AUDIT_RATIONALE_MAX_LENGTH)
        .join('')
        .trim();
    return bounded || AGENT_AUDIT_RATIONALE_FALLBACK;
};

export const createAgentCommandMetadata = (rationale: string): AgentCommandMetadata => {
    const commandId = randomId();
    return {
        idempotencyKey: `ui-${commandId}`,
        rationale: toAgentAuditRationale(rationale),
        correlationId: `ui-${commandId}`,
    };
};

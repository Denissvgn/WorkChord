import { describe, expect, it } from 'vitest';
import type { TaskDifficultyAxes } from '../types/agent';
import {
    createAgentCommandMetadata,
    deriveDifficultyBand,
    minimumReviewMode,
    reviewModeMeets,
    toAgentAuditRationale,
} from './modelRouting';

const routineAxes: TaskDifficultyAxes = {
    reasoning: 1,
    ambiguity: 1,
    context_breadth: 1,
    risk: 1,
    verification_burden: 1,
};

describe('model routing policy helpers', () => {
    it('classifies an all-low assessment without reason codes as routine', () => {
        expect(deriveDifficultyBand(routineAxes, [])).toBe('routine');
    });

    it('classifies a level-three axis or policy reason code as advanced', () => {
        expect(deriveDifficultyBand(
            { ...routineAxes, context_breadth: 3 },
            [],
        )).toBe('advanced');
        expect(deriveDifficultyBand(
            routineAxes,
            ['novel-architecture'],
        )).toBe('advanced');
    });

    it('requires independent review for high-risk work', () => {
        const minimum = minimumReviewMode(
            { ...routineAxes, risk: 3 },
            [],
        );

        expect(minimum).toBe('independent');
        expect(reviewModeMeets('standard', minimum)).toBe(false);
        expect(reviewModeMeets('independent', minimum)).toBe(true);
    });

    it('keeps specialist verification above the independent review floor', () => {
        const minimum = minimumReviewMode(
            routineAxes,
            ['specialist-verification'],
        );

        expect(minimum).toBe('specialist-independent');
        expect(reviewModeMeets('independent', minimum)).toBe(false);
        expect(reviewModeMeets('specialist-independent', minimum)).toBe(true);
    });

    it('derives a bounded control-free audit header without changing payload text', () => {
        const payloadRationale = `First line\nSecond\tline\u0000 ${'x'.repeat(2_100)}`;
        const auditRationale = toAgentAuditRationale(payloadRationale);
        const metadata = createAgentCommandMetadata(payloadRationale);

        expect(payloadRationale).toContain('\n');
        expect(auditRationale).toMatch(/^First line Second line x+$/);
        expect(Array.from(auditRationale)).toHaveLength(2_000);
        expect(Array.from(auditRationale).every(character => {
            const codePoint = character.codePointAt(0) ?? 0;
            return codePoint >= 32 && codePoint !== 127;
        })).toBe(true);
        expect(metadata.rationale).toBe(auditRationale);
    });
});

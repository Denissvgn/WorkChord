import { describe, expect, it } from 'vitest';
import { STATUS_TONE, toneLineVar, toneSoftVar, toneVar, wcPillClass } from './tone';

describe('workspace status tone bridge', () => {
    it('keeps closed work on the canonical closed status family', () => {
        expect(STATUS_TONE.closed).toBe('purple');
        expect(wcPillClass.purple).toBe('closed');
        expect(toneVar.purple).toBe('var(--wc-status-closed)');
        expect(toneSoftVar.purple).toBe('var(--wc-status-closed-soft)');
        expect(toneLineVar.purple).toBe('var(--wc-status-closed-line)');
    });

    it('maps the task lifecycle to its own persistent-state variants', () => {
        expect(wcPillClass.gray).toBe('planned');
        expect(wcPillClass.blue).toBe('active');
        expect(wcPillClass.green).toBe('resolved');
    });
});

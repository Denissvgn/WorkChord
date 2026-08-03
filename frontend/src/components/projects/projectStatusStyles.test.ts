import { describe, expect, it } from 'vitest';
import {
    projectStatusBadgeClassName,
    projectStatusPillClassName,
} from './projectStatusStyles';

describe('projectStatusStyles', () => {
    it('keeps active work on the canonical cyan status tokens', () => {
        expect(projectStatusBadgeClassName('active')).toContain('bg-status-active-muted');
        expect(projectStatusBadgeClassName('active')).toContain('text-status-active-foreground');
        expect(projectStatusBadgeClassName('active')).toContain('border-status-active-border');
        expect(projectStatusPillClassName('active')).toBe('active');
    });

    it('maps terminal project states onto durable record-status colors', () => {
        expect(projectStatusBadgeClassName('completed')).toContain('bg-status-resolved-muted');
        expect(projectStatusBadgeClassName('canceled')).toContain('bg-status-closed-muted');
    });
});

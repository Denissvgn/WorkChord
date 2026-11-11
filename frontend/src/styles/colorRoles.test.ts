/// <reference types="node" />

import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { priorityChipClassName } from '../components/ui/tone';

const css = readFileSync(resolve(process.cwd(), 'src/styles/globals.css'), 'utf8');

/** The tokens one theme ends up with: the light defaults plus that theme's own block. */
const themeTokens = (theme: string) => {
    const tokens = new Map<string, number[]>();
    const read = (selector: string) => {
        const start = css.indexOf(selector);
        if (start < 0) throw new Error(`Missing theme block ${selector}`);
        const body = css.slice(css.indexOf('{', start) + 1, css.indexOf('}', start));
        for (const match of body.matchAll(/--color-([\w-]+):\s*(\d+)\s+(\d+)\s+(\d+)\s*;/g)) {
            tokens.set(match[1], [Number(match[2]), Number(match[3]), Number(match[4])]);
        }
    };
    read("[data-theme='light']");
    if (theme !== 'light') read(`[data-theme='${theme}']`);
    return tokens;
};

const distance = (a: number[], b: number[]) => Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2]);

// Each role keeps its own color: status hues for status, red and amber for exceptions, the action color for the next step.
const ROLES = ['status-planned-solid', 'status-active-solid', 'status-resolved-solid', 'status-closed-solid',
    'feedback-danger', 'feedback-warning', 'action-primary'];

describe('color roles', () => {
    it.each(['light', 'dark', 'blue', 'green'])('keeps status, exception and action colors apart in the %s theme', theme => {
        const tokens = themeTokens(theme);
        for (const [index, role] of ROLES.entries()) {
            expect(tokens.get(role), `${theme}: ${role}`).toBeDefined();
            for (const other of ROLES.slice(index + 1)) {
                expect(distance(tokens.get(role)!, tokens.get(other)!), `${theme}: ${role} vs ${other}`).toBeGreaterThan(40);
            }
        }
    });

    it.each(['light', 'dark', 'blue', 'green'])('keeps selection, success and ink apart in the %s theme', theme => {
        const tokens = themeTokens(theme);
        // A selected row (action tint) must not look like a quiet muted surface.
        expect(distance(tokens.get('action-muted')!, tokens.get('surface-muted')!), `${theme}: action-muted vs surface-muted`).toBeGreaterThan(8);
        // The action color must not read as success or Resolved.
        expect(distance(tokens.get('action-primary')!, tokens.get('feedback-success')!), `${theme}: action vs success`).toBeGreaterThan(80);
        expect(distance(tokens.get('action-primary')!, tokens.get('status-resolved-solid')!), `${theme}: action vs resolved`).toBeGreaterThan(80);
        // Body ink stays neutral: no channel far from the others.
        const ink = tokens.get('content-primary')!;
        expect(Math.max(...ink) - Math.min(...ink), `${theme}: ink is tinted`).toBeLessThan(40);
    });

    it('never colors priority with exception, status or action hues', () => {
        for (let priority = 1; priority <= 10; priority += 1) {
            expect(priorityChipClassName(priority)).not.toMatch(/feedback-|status-|action/);
        }
        expect(priorityChipClassName(1)).not.toBe(priorityChipClassName(7));
    });
});

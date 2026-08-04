import { describe, expect, it } from 'vitest';
import {
    accessibleNameViolations,
    summaryNameViolations,
} from './accessibilityInvariants';

describe('accessibility invariants', () => {
    it('reports empty and duplicate names within the same role', () => {
        document.body.innerHTML = `
            <button aria-label="Refresh"></button>
            <button>Refresh</button>
            <a href="/one"></a>
        `;

        expect(accessibleNameViolations(document.body)).toEqual([
            { role: 'button', names: ['Refresh', 'Refresh'] },
            { role: 'link', names: [''] },
        ]);
    });

    it('keeps equal names valid when their roles differ', () => {
        document.body.innerHTML = `
            <nav aria-label="Planning"></nav>
            <aside aria-label="Planning"></aside>
            <button>Refresh</button>
            <a href="/refresh">Open refresh</a>
        `;

        expect(accessibleNameViolations(document.body)).toEqual([]);
    });

    it('checks disclosure summaries outside the role map', () => {
        document.body.innerHTML = `
            <details><summary>Runtime details</summary></details>
            <details><summary>Runtime details</summary></details>
        `;

        expect(summaryNameViolations(document.body)).toEqual([
            'Runtime details',
        ]);
    });
});

/// <reference types="node" />

import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';

const planningMastersCss = readFileSync(
    resolve(process.cwd(), 'src/styles/planning-masters.css'),
    'utf8',
);
const agentTeamMasterSource = readFileSync(
    resolve(process.cwd(), 'src/pages/AgentTeamSetupMasterPage.tsx'),
    'utf8',
);

const cssRule = (selector: string) => {
    const start = planningMastersCss.indexOf(`${selector} {`);
    expect(start, `missing CSS rule for ${selector}`).toBeGreaterThan(-1);
    return planningMastersCss.slice(start, planningMastersCss.indexOf('}', start) + 1);
};

describe('responsive shell contracts', () => {
    it('restores the joined Overview panel on desktop and linearizes it on mobile', () => {
        expect(planningMastersCss).toContain(
            'grid-template-areas:\n    "focus snapshot"\n    "work work";',
        );

        const mobileStart = planningMastersCss.indexOf('@media (max-width: 768px)');
        const mobileEnd = planningMastersCss.indexOf('@media (max-width: 640px)', mobileStart);
        const mobileRules = planningMastersCss.slice(mobileStart, mobileEnd);

        expect(mobileStart).toBeGreaterThan(-1);
        expect(mobileEnd).toBeGreaterThan(mobileStart);
        expect(mobileRules).toContain('.wc .overview-thread-flow.has-focus-panel');
        expect(mobileRules).toContain('display: flex;');
        expect(mobileRules).toContain('> .overview-focus-progress');
    });

    it('keeps every shell control at least 44px on mobile and hybrid touch devices', () => {
        const responsiveStart = planningMastersCss.indexOf('@media (max-width: 1180px)');
        const responsiveEnd = planningMastersCss.indexOf('@media (max-width: 720px)', responsiveStart);
        const responsiveRules = planningMastersCss.slice(responsiveStart, responsiveEnd);
        const coarseStart = planningMastersCss.indexOf(
            '@media (pointer: coarse), (any-pointer: coarse)',
        );
        const coarseEnd = planningMastersCss.indexOf(
            '@media (prefers-reduced-motion: reduce)',
            coarseStart,
        );
        const coarseRules = planningMastersCss.slice(coarseStart, coarseEnd);

        expect(responsiveStart).toBeGreaterThan(-1);
        expect(responsiveEnd).toBeGreaterThan(responsiveStart);
        expect(responsiveRules).toContain('.wc .brand');
        expect(responsiveRules).toContain('.wc .mobile-nav-panel .sb-views > summary');
        expect(responsiveRules).toContain('.wc .mobile-nav-panel .sb-plan-select');
        expect(responsiveRules).toContain('.wc .mobile-nav-panel .sb-plan-link');
        expect(responsiveRules).toContain('min-height: 44px;');

        expect(coarseStart).toBeGreaterThan(-1);
        expect(coarseEnd).toBeGreaterThan(coarseStart);
        for (const selector of [
            '.wc .brand',
            '.wc .mobile-nav-trigger',
            '.wc .plan-master-step-rail .step-item',
            '.wc .plan-share-link-field input',
            '.wc .sb-plan-select',
            '.wc .sb-plan-option',
            '.wc .sb-plan-title',
            '.wc .sb-plan-link',
        ]) {
            expect(coarseRules).toContain(selector);
        }
        expect(coarseRules).toContain('min-height: 44px;');
    });

    it('keeps changed drawers safe, readable, and motion-aware', () => {
        expect(planningMastersCss).toContain(
            'padding-inline: env(safe-area-inset-left) env(safe-area-inset-right);',
        );
        expect(planningMastersCss).toContain(
            'width: min(calc(100vw - 12px - env(safe-area-inset-left) - env(safe-area-inset-right)), 380px);',
        );
        expect(planningMastersCss).toContain('@keyframes wc-drawer-enter');
        expect(planningMastersCss).toContain('.wc .overview-task-drawer .task-form input:not([type="checkbox"]):not([type="radio"])');
        expect(planningMastersCss).toContain('font-size: 16px;');
        expect(planningMastersCss).toContain('.wc .wc-slide-over > header .btn.icon');
    });

    it('keeps agent-team status scopes visible and linearizes them on mobile', () => {
        expect(planningMastersCss).toContain('.wc .agent-team-status-scopes');
        expect(planningMastersCss).toContain(
            'grid-template-columns: repeat(3, minmax(0, 1fr));',
        );

        const mobileStart = planningMastersCss.indexOf('@media (max-width: 768px)');
        const mobileEnd = planningMastersCss.indexOf('@media (max-width: 640px)', mobileStart);
        const mobileRules = planningMastersCss.slice(mobileStart, mobileEnd);

        expect(mobileRules).toContain('.wc .agent-team-status-scopes');
        expect(mobileRules).toContain(
            'grid-template-columns: minmax(0, 1fr);',
        );
    });

    it('shares semantic progress, focus, and reduced-motion treatments across masters', () => {
        expect(planningMastersCss).toContain('.wc .master-progress {');
        expect(planningMastersCss).toContain('.wc .master-progress > span {');
        expect(planningMastersCss).toContain('.wc .wc-master-rail-title {');
        expect(planningMastersCss).toContain('.wc .wc-master-rail-progress-text {');
        expect(planningMastersCss).toContain('.wc .wc-master-focus-heading:focus-visible');
        expect(planningMastersCss).toContain('.wc .wc-master-focus-region:focus-visible');
        expect(planningMastersCss).toContain(
            'outline: var(--wc-focus-width) solid var(--wc-focus-ring);',
        );

        const reducedMotionStart = planningMastersCss.indexOf(
            '@media (prefers-reduced-motion: reduce)',
        );
        const reducedMotionRules = planningMastersCss.slice(reducedMotionStart);
        expect(reducedMotionRules).toContain('.wc .master-progress > span');
        expect(reducedMotionRules).toContain('transition: none !important;');
    });

    it('keeps keyboard focus styling tokenized and modality-aware', () => {
        const sharedFocus = cssRule(
            ':where(.wc :is(button, a, input, select, textarea, summary)):focus-visible',
        );
        const headingFocus = cssRule('.wc .wc-master-focus-heading:focus-visible');
        const regionFocus = cssRule('.wc .wc-master-focus-region:focus-visible');
        const evidenceFocus = cssRule('.wc .plan-evidence-link:focus-visible');
        const inputFocus = cssRule(
            ':where(.wc .input):is(input, select, textarea):focus-visible',
        );

        for (const rule of [sharedFocus, headingFocus, regionFocus]) {
            expect(rule).toContain(
                'outline: var(--wc-focus-width) solid var(--wc-focus-ring);',
            );
        }
        expect(sharedFocus).toContain('outline-offset: var(--wc-focus-offset);');
        expect(headingFocus).toContain('outline-offset: var(--wc-focus-offset);');
        expect(regionFocus).toContain(
            'outline-offset: calc(-1 * var(--wc-focus-width));',
        );
        expect(inputFocus).toContain('border-color: var(--thread);');
        expect(inputFocus).toContain('box-shadow: 0 0 0 3px var(--thread-soft);');
        expect(evidenceFocus).toContain('border-radius: var(--wc-r-sm);');
        expect(evidenceFocus).not.toContain('outline:');
        expect(planningMastersCss).not.toContain(
            '.wc .plan-share-link-field input:focus {',
        );
        expect(cssRule('.wc .agent-team-runtime-handoff > summary'))
            .toContain('border-radius: var(--wc-r-sm);');

        const mobileStart = planningMastersCss.indexOf('@media (max-width: 768px)');
        const mobileEnd = planningMastersCss.indexOf('@media (max-width: 640px)', mobileStart);
        const mobileRules = planningMastersCss.slice(mobileStart, mobileEnd);
        expect(mobileRules).toMatch(
            /\.wc \.agent-team-mobile-steps > summary\s*{[^}]*border-radius: var\(--wc-r-sm\);/s,
        );
    });

    it('preserves interactive step states without making passive checks look clickable', () => {
        const stepRule = cssRule('.wc .step-item');
        const planStepRule = cssRule('.wc .plan-master-step-rail .step-item');

        expect(stepRule).toContain('background: transparent;');
        expect(stepRule).not.toContain('cursor: pointer;');
        expect(planningMastersCss).toContain('.wc button.step-item { cursor: pointer; }');
        expect(planningMastersCss).toContain(
            '.wc button.step-item:hover { background: var(--panel-3); }',
        );
        expect(cssRule('.wc .step-item[aria-current="step"]'))
            .toContain('background: var(--thread-soft);');
        expect(planStepRule).not.toContain('background: transparent;');
    });

    it('keeps the Master hierarchy role-based and tokenized', () => {
        expect(cssRule('.wc .wc-master-section-title'))
            .toContain('font-size: var(--wc-type-heading);');
        expect(cssRule('.wc .wc-master-aux-scope-title,\n.wc .wc-master-aux-title'))
            .toContain('font-size: var(--wc-type-base);');
        expect(cssRule('.wc .agent-team-step-scope'))
            .toContain('font-size: var(--wc-type-meta);');
        expect(agentTeamMasterSource).not.toContain('fontSize:');

        const mobileStart = planningMastersCss.indexOf('@media (max-width: 768px)');
        const mobileEnd = planningMastersCss.indexOf('@media (max-width: 640px)', mobileStart);
        const mobileRules = planningMastersCss.slice(mobileStart, mobileEnd);
        expect(mobileRules).toMatch(
            /\.wc \.agent-team-mobile-context > h2\s*{[^}]*font-size: var\(--wc-type-meta\);/s,
        );
        expect(mobileRules).toMatch(
            /\.wc \.agent-team-mobile-context-head h3\s*{[^}]*font-size: var\(--wc-type-heading\);/s,
        );
    });

    it('keeps Agent Setup context, editor geometry, and touch controls usable', () => {
        const tabletStart = planningMastersCss.indexOf('@media (max-width: 1100px)');
        const tabletEnd = planningMastersCss.indexOf('@media (max-width: 768px)', tabletStart);
        const tabletRules = planningMastersCss.slice(tabletStart, tabletEnd);
        const mobileStart = tabletEnd;
        const mobileEnd = planningMastersCss.indexOf('@media (max-width: 640px)', mobileStart);
        const mobileRules = planningMastersCss.slice(mobileStart, mobileEnd);
        const coarseStart = planningMastersCss.indexOf(
            '@media (pointer: coarse), (any-pointer: coarse)',
        );
        const coarseEnd = planningMastersCss.indexOf(
            '@media (prefers-reduced-motion: reduce)',
            coarseStart,
        );
        const coarseRules = planningMastersCss.slice(coarseStart, coarseEnd);

        expect(planningMastersCss).toContain('.wc .agent-team-master-editor {');
        expect(planningMastersCss).toContain('height: auto;');
        expect(planningMastersCss).toContain('min-height: clamp(22rem, 48vh, 32rem);');
        expect(planningMastersCss).toContain('resize: vertical;');

        expect(tabletRules).toContain(
            '.wc .agent-team-master-layout > .agent-team-runtime-aux',
        );
        expect(tabletRules).toContain('display: block;');
        expect(tabletRules).toContain('.wc .agent-team-runtime-summary');
        expect(tabletRules).toContain(
            '.wc .agent-team-runtime-details:not([open]) > .agent-team-runtime-details-body',
        );

        for (const selector of [
            '.wc .agent-team-mobile-context',
            '.wc .agent-team-mobile-steps',
            '.wc .agent-team-master-panel-head',
            '.wc .agent-team-master-actions',
            '.wc .agent-team-plan-action-layout',
            '.wc .agent-team-plan-action-controls',
            '.wc .agent-team-action-confirmation',
            '.wc.agent-team-setup-page :where(.btn):is(button, a, label)',
        ]) {
            expect(mobileRules).toContain(selector);
        }
        expect(mobileRules).toContain('min-height: clamp(18rem, 48dvh, 26rem);');
        expect(mobileRules).toContain('font-size: 16px;');
        expect(mobileRules).toContain('font-size: var(--wc-type-page);');
        expect(mobileRules).not.toMatch(
            /agent-team-master-layout > \.agent-team-runtime-aux\s*{[^}]*grid-row/s,
        );
        expect(mobileRules).not.toMatch(
            /agent-team-master-layout > \.wc-master-main\s*{[^}]*grid-row/s,
        );

        for (const selector of [
            '.wc.agent-team-setup-page input:not([type="checkbox"]):not([type="radio"]):not([type="file"])',
            '.wc.agent-team-setup-page textarea',
            '.wc .agent-team-action-confirmation',
            '.wc .agent-team-runtime-summary',
            '.wc .agent-team-runtime-handoff > summary',
        ]) {
            expect(coarseRules).toContain(selector);
        }
        expect(coarseRules).toContain('min-height: 44px;');
    });
});

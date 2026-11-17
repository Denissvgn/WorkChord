/// <reference types="node" />

import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { ESLint } from 'eslint';
import { describe, expect, it } from 'vitest';

const eslint = new ESLint({ cwd: process.cwd() });
const fixture = (name: string) => readFileSync(resolve(__dirname, 'lintFixtures', `${name}.fixture`), 'utf8');

/** Lints a fixture as if it were the given file of the app, and returns what the rules report. */
const lint = async (name: string, filePath: string) => {
    const [result] = await eslint.lintText(fixture(name), { filePath: resolve(process.cwd(), filePath) });
    return result.messages.filter(message => message.severity === 2).map(message => ({ rule: message.ruleId, text: message.message }));
};

describe('page frame lint rules', () => {
    it('rejects a bare button and a bare select outside the shared parts', async () => {
        for (const filePath of ['src/pages/Example.tsx', 'src/components/tasks/Example.tsx', 'src/features/identity/Example.tsx']) {
            const reports = await lint('bareControls', filePath);
            expect(reports.map(report => report.rule), filePath).toEqual(['no-restricted-syntax', 'no-restricted-syntax']);
            expect(reports[0].text).toMatch(/native <button>/);
            expect(reports[1].text).toMatch(/native <select>/);
        }
    });

    it('allows the native controls inside the shared parts and in tests', async () => {
        for (const filePath of ['src/components/common/Example.tsx', 'src/components/ui/Example.tsx', 'src/pages/Example.test.tsx']) {
            expect(await lint('bareControls', filePath), filePath).toEqual([]);
        }
    });

    it('rejects an import of the removed iteration selector', async () => {
        const reports = await lint('removedIterationSelector', 'src/pages/Example.tsx');
        expect(reports.map(report => report.rule)).toEqual(['no-restricted-imports']);
        expect(reports[0].text).toMatch(/scope bar/);
    });

    it('rejects a second PageToolbar in one page', async () => {
        const reports = await lint('secondToolbar', 'src/pages/Example.tsx');
        expect(reports.map(report => report.rule)).toEqual(['workchord/single-page-toolbar']);
        expect(reports[0].text).toMatch(/at most one PageToolbar/);
    });

    it('accepts a page built from the shared parts with one toolbar in each return', async () => {
        expect(await lint('sharedParts', 'src/pages/Example.tsx')).toEqual([]);
    });
});

/// <reference types="node" />

import { readdirSync, readFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import i18n from './i18n';
import { englishResources } from './resources.en';

const flatten = (value: unknown, prefix = ''): [string, string][] => (
    value && typeof value === 'object' && !Array.isArray(value)
        ? Object.entries(value as Record<string, unknown>).flatMap(([key, child]) => flatten(child, prefix ? `${prefix}.${key}` : key))
        : typeof value === 'string' ? [[prefix, value]] : []
);
const english = flatten(englishResources.translation);
const sources = (dir: string): string[] => readdirSync(dir, { withFileTypes: true }).flatMap(entry => {
    const path = join(dir, entry.name);
    if (entry.isDirectory()) return sources(path);
    return /\.tsx?$/.test(path) && !path.includes('.test.') && !path.includes('/i18n/') ? [path] : [];
});

describe('formats and wording', () => {
    it('writes counts with plural forms, not "(s)"', () => {
        expect(english.filter(([, text]) => text.includes('(s)')).map(([key]) => key)).toEqual([]);
    });

    it('writes labels in sentence case', () => {
        // Names keep their capitals: page and workspace names, products, acronyms, and the shared vocabulary.
        const names = /Delivery Hub|Timeline & Planning|Resource & Settings|My Work|Plan Work|Plan Master|Agent Pipeline|Agent Team Setup|United States/g;
        const skipped = /^(nav|documentTitles|breadcrumbs|statuses|languages|agentTeamSetup\.roles|agentTeamSetup\.steps)\./;
        const titleCase = english.filter(([key, text]) => {
            if (skipped.test(key) || /[<•{"]|--/.test(text)) return false;
            // A label that is only a name, or a name inside a label, is not Title Case.
            const words = text.replace(names, 'Name').split(/\s+/).filter(word => word !== 'Name');
            if (words.length < 2 || words.length > 5) return false;
            const rest = words.slice(1).filter(word => !/^(a|an|and|or|of|to|in|on|for|the|by|with|&|\/)$/i.test(word));
            return rest.length > 0 && rest.every(word => /^[A-Z][a-z]+$/.test(word) && !/^(WorkChord|GitHub|Gantt|Android|Overview|Tasks|Triage|Projects|Roadmap|Iterations|Calendar|Team|Analytics|Settings|Schedule|Review)$/.test(word));
        });
        expect(titleCase.map(([key, text]) => `${key}: ${text}`)).toEqual([]);
    });

    it('uses one ellipsis character', () => {
        expect(english.filter(([, text]) => text.includes('...')).map(([key]) => key)).toEqual([]);
    });

    it('reads singular and plural counts naturally', async () => {
        await i18n.changeLanguage('en');
        expect(i18n.t('units.days', { count: 1 })).toBe('1 day');
        expect(i18n.t('units.days', { count: 40 })).toBe('40 days');
        expect(i18n.t('surfaces.projectTaskTree.dependencies', { count: 1 })).toBe('1 dependency');
    });

    it('formats dates and times through the shared formatter', () => {
        const raw = sources(resolve(process.cwd(), 'src'))
            .filter(file => /new Date\([^)]*\)\.toLocale(String|DateString|TimeString)\(/.test(readFileSync(file, 'utf8')));
        expect(raw).toEqual([]);
    });
});

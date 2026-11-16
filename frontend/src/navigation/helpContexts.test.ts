/// <reference types="node" />

import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { englishResources } from '../i18n/resources.en';
import { russianResources } from '../i18n/resources.ru';
import { DESTINATIONS } from './destinations';
import { getHelpContext } from './helpContexts';

type Localized = { en: string; ru: string };
type VocabularyEntry = { id: string; name: Localized | string };

const vocabulary = JSON.parse(
    readFileSync(resolve(process.cwd(), '../config/workflow-vocabulary.json'), 'utf8'),
) as { terms: VocabularyEntry[]; checkpoints: VocabularyEntry[] };

const catalogs = {
    en: englishResources.translation,
    ru: russianResources.translation,
} as const;

const lookup = (catalog: unknown, key: string): unknown => key.split('.').reduce<unknown>(
    (value, segment) => (value && typeof value === 'object'
        ? (value as Record<string, unknown>)[segment]
        : undefined),
    catalog,
);

const textAt = (language: keyof typeof catalogs, key: string): string => {
    const value = lookup(catalogs[language], key);
    return typeof value === 'string' ? value : '';
};

const sentenceCount = (text: string) => (text.match(/[.!?](?=\s|$)/g) ?? []).length;

describe('destination help', () => {
    it('gives each of the ten destinations its own help text and at least two glossary terms', () => {
        expect(DESTINATIONS).toHaveLength(10);

        const summaryKeys = DESTINATIONS.map(destination => getHelpContext(destination.path).summaryKey);
        expect(new Set(summaryKeys).size).toBe(10);

        for (const destination of DESTINATIONS) {
            const help = getHelpContext(destination.path);
            expect(help.destination.id, destination.path).toBe(destination.id);
            expect(help.glossary.length, destination.id).toBeGreaterThanOrEqual(2);

            for (const language of ['en', 'ru'] as const) {
                const summary = textAt(language, help.summaryKey);
                expect(summary.trim(), `${language} ${help.summaryKey}`).not.toBe('');
                expect(sentenceCount(summary), `${language} ${help.summaryKey}`).toBeGreaterThanOrEqual(2);
                expect(sentenceCount(summary), `${language} ${help.summaryKey}`).toBeLessThanOrEqual(3);
            }
        }
    });

    it('answers views of a destination with the destination help, not a generic hint', () => {
        expect(getHelpContext('/roadmap').destination.id).toBe('projects');
        expect(getHelpContext('/agent-pipeline').destination.id).toBe('tasks');
        expect(getHelpContext('/iterations').destination.id).toBe('plan');
        expect(getHelpContext('/calendar').destination.id).toBe('settings');
        expect(getHelpContext('/agent-team/setup').destination.id).toBe('team');
        expect(getHelpContext('/plan/master').destination.id).toBe('plan');
    });

    it('defines every glossary term shown in the vocabulary source, in English and Russian', () => {
        const shownTerms = [...new Set(DESTINATIONS.flatMap(destination => getHelpContext(destination.path).glossary))];
        expect(shownTerms.length).toBeGreaterThan(0);

        for (const term of shownTerms) {
            const entry = [...vocabulary.terms, ...vocabulary.checkpoints].find(item => item.id === term);
            expect(entry, `${term} is missing from the vocabulary`).toBeDefined();
            const name = entry?.name as Localized | undefined;
            expect(name?.en, `${term} has no English name`).toBeTruthy();
            expect(name?.ru, `${term} has no Russian name`).toBeTruthy();

            for (const language of ['en', 'ru'] as const) {
                expect(textAt(language, `contextHelp.glossary.${term}.term`), `${language} ${term} term`)
                    .toBe(name?.[language]);
                expect(textAt(language, `contextHelp.glossary.${term}.definition`).trim(),
                    `${language} ${term} definition`).not.toBe('');
            }
        }
    });
});

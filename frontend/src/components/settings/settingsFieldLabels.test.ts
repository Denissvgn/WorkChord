import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import i18n, { ensureLanguageResources } from '../../i18n/i18n';
import { SETTINGS_FIELD_LABEL_KEYS } from './settingsFieldLabels';
import type { SettingsSectionId } from './settingsFieldLabels';

const source = (file: string) => readFileSync(resolve(process.cwd(), 'src/components/settings', file), 'utf8');

/** A visible field label: `label={t('…')}`, or the first `t('…')` inside a `<label>` or `<legend>` element. */
const LABEL_PATTERNS = [
    /(?<![\w-])label=\{t\(\s*'([^']+)'\s*\)\}/g,
    /<label\b[^>]*>(?:(?!<\/label>)[\s\S])*?\{t\(\s*'([^']+)'\s*\)\}/g,
    /<legend\b[^>]*>\s*\{t\(\s*'([^']+)'\s*\)\}/g,
];

const labelKeysIn = (text: string, extraPatterns: RegExp[] = []) => {
    const keys = new Set<string>();
    for (const pattern of [...LABEL_PATTERNS, ...extraPatterns]) {
        for (const match of text.matchAll(pattern)) keys.add(match[1]);
    }
    return [...keys];
};

/** The server settings form shows one part per section; each part starts at its `shows('…')` guard. */
const runtimePart = (part: string) => {
    const text = source('RuntimeConfigSettings.tsx');
    const start = text.indexOf(`{shows('${part}') &&`);
    expect(start, part).toBeGreaterThan(-1);
    const next = text.indexOf('{shows(', start + 1);
    return text.slice(start, next === -1 ? undefined : next);
};

const PANELS: Array<{ name: string; section: SettingsSectionId; text: () => string; extraPatterns?: RegExp[] }> = [
    { name: 'InterfaceLanguageSettings', section: 'language', text: () => source('InterfaceLanguageSettings.tsx') },
    { name: 'RuntimeConfigSettings aiLanguage', section: 'language', text: () => runtimePart('aiLanguage') },
    { name: 'EffortModifierCard', section: 'scheduling', text: () => source('EffortModifierCard.tsx') },
    { name: 'SchedulingPassCard', section: 'scheduling', text: () => source('SchedulingPassCard.tsx') },
    // The constraint checkboxes take their labels from a list in the panel.
    { name: 'ConstraintsPanel', section: 'scheduling', text: () => source('ConstraintsPanel.tsx'), extraPatterns: [/labelKey:\s*'([^']+)'/g] },
    { name: 'TemplateLabelSettings', section: 'templates_labels', text: () => source('TemplateLabelSettings.tsx') },
    { name: 'EmailSettingsPanel', section: 'notifications', text: () => source('EmailSettingsPanel.tsx') },
    { name: 'RuntimeConfigSettings github', section: 'github', text: () => runtimePart('github') },
    { name: 'GitHubSettingsPanel', section: 'github', text: () => source('GitHubSettingsPanel.tsx') },
    { name: 'OutboundWebhooksPanel', section: 'webhooks', text: () => source('OutboundWebhooksPanel.tsx') },
    { name: 'RuntimeConfigSettings webIntake', section: 'web_intake', text: () => runtimePart('webIntake') },
    { name: 'RuntimeConfigSettings llm', section: 'ai_provider', text: () => runtimePart('llm') },
    { name: 'AdminAccessPanel', section: 'access', text: () => source('AdminAccessPanel.tsx') },
    { name: 'AgentAccessPanel', section: 'access', text: () => source('AgentAccessPanel.tsx') },
    { name: 'AgentModelAdministration', section: 'models_agents', text: () => source('AgentModelAdministration.tsx') },
];

describe('settings field labels for search', () => {
    it.each(PANELS)('indexes every field label $name renders under its section', ({ section, text, extraPatterns }) => {
        const rendered = labelKeysIn(text(), extraPatterns);
        expect(rendered.length).toBeGreaterThan(0);
        expect(rendered.filter(key => !SETTINGS_FIELD_LABEL_KEYS[section].includes(key))).toEqual([]);
    });

    it('indexes only keys that have English and Russian text', async () => {
        await ensureLanguageResources('ru');
        const missing = Object.entries(SETTINGS_FIELD_LABEL_KEYS).flatMap(([section, keys]) => keys.flatMap(key => (
            (['en', 'ru'] as const)
                .filter(language => typeof i18n.getResource(language, 'translation', key) !== 'string')
                .map(language => `${section} ${language} ${key}`)
        )));
        expect(missing).toEqual([]);
    });
});

import { describe, expect, it } from 'vitest';
import i18n, { ensureLanguageResources } from '../../i18n/i18n';
import { SETTINGS_FIELD_LABEL_KEYS } from './settingsFieldLabels';

describe('settings field labels for search', () => {
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

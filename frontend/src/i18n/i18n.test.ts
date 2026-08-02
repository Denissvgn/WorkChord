import { describe, expect, it } from 'vitest';
import i18n, { changeAppLanguage } from './i18n';

describe('lazy language resources', () => {
    it('loads the Russian catalog only when that language is selected', async () => {
        expect(i18n.hasResourceBundle('ru', 'translation')).toBe(false);

        await changeAppLanguage('ru');

        expect(i18n.hasResourceBundle('ru', 'translation')).toBe(true);
        expect(i18n.t('common.loading')).toBe('Загрузка...');
    });
});

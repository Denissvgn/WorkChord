import { enUS, ru } from 'date-fns/locale';
import type { Locale } from 'date-fns';
import i18n from './i18n';

export const normalizedLanguage = (language = i18n.language) => (
    language.toLowerCase().startsWith('ru') ? 'ru' : 'en'
);

export const dateFnsLocale = (language = i18n.language): Locale => (
    normalizedLanguage(language) === 'ru' ? ru : enUS
);

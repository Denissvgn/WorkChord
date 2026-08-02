import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import { englishResources } from './resources.en';

type SupportedLanguage = 'en' | 'ru';

const normalizeLanguage = (language: string): SupportedLanguage => (
    language.split('-')[0] === 'ru' ? 'ru' : 'en'
);

let russianResourcePromise: Promise<void> | null = null;

export const ensureLanguageResources = async (language: string) => {
    const normalized = normalizeLanguage(language);
    if (normalized === 'en' || i18n.hasResourceBundle(normalized, 'translation')) {
        return normalized;
    }

    russianResourcePromise ??= import('./resources.ru').then(({ russianResources }) => {
        i18n.addResourceBundle(
            'ru',
            'translation',
            russianResources.translation,
            true,
            true,
        );
    });
    await russianResourcePromise;
    return normalized;
};

export const changeAppLanguage = async (language: string) => {
    const normalized = await ensureLanguageResources(language);
    await i18n.changeLanguage(normalized);
};

void i18n
    .use(initReactI18next)
    .init({
        resources: {
            en: englishResources,
        },
        lng: 'en',
        fallbackLng: 'en',
        interpolation: {
            escapeValue: false,
        },
    });

export default i18n;

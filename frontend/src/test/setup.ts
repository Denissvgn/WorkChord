import '@testing-library/jest-dom/vitest';
import { cleanup } from '@testing-library/react';
import { afterEach } from 'vitest';
import i18n from '../i18n/i18n';

afterEach(async () => {
    cleanup();
    window.localStorage.clear();
    window.sessionStorage.clear();

    if (i18n.language !== 'en') {
        await i18n.changeLanguage('en');
    }
});

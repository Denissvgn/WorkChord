import { afterEach, describe, expect, it } from 'vitest';
import { changeAppLanguage } from './i18n';
import { labelDisplay, labelGroupDisplay } from './seedDisplay';
import type { LabelGroupBrief } from '../types/label';

// A label carries only the brief group (id, key, name, colour, active); the full group record is not on it.
const embeddedGroup = (key: string, name: string): LabelGroupBrief => ({ id: 1, key, name, color: '#2563eb', is_active: true });

describe('seeded label group names', () => {
    afterEach(async () => {
        await changeAppLanguage('en');
    });

    it('shows the Russian name for a label whose embedded group is the seeded Type group', async () => {
        await changeAppLanguage('ru');

        expect(labelGroupDisplay(embeddedGroup('type', 'Type')).name).toBe('Тип');
        expect(labelGroupDisplay(embeddedGroup('area', 'Area')).name).toBe('Область');
        expect(labelGroupDisplay(embeddedGroup('risk', 'Risk')).name).toBe('Риск');
    });

    it('keeps the English name when the language is English', async () => {
        await changeAppLanguage('en');

        expect(labelGroupDisplay(embeddedGroup('type', 'Type')).name).toBe('Type');
    });

    it('translates a full seeded record by its seed key', async () => {
        await changeAppLanguage('ru');

        expect(labelGroupDisplay({ seed_key: 'group_source', name: 'Source' }).name).toBe('Источник');
    });

    it('translates a seeded label whose seed key the API writes with a hyphen', async () => {
        await changeAppLanguage('ru');

        expect(labelDisplay({ seed_key: 'label_needs-review', name: 'Needs review' }).name).toBe('Требует проверки');
    });

    it('leaves a renamed group alone', async () => {
        await changeAppLanguage('ru');

        expect(labelGroupDisplay(embeddedGroup('type', 'Kind')).name).toBe('Kind');
        expect(labelGroupDisplay(embeddedGroup('team_custom', 'Type')).name).toBe('Type');
    });
});

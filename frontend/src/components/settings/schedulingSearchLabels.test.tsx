import { screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import i18n from '../../i18n/i18n';
import { renderWithProviders } from '../../test/renderWithProviders';
import { EffortModifierCard } from './EffortModifierCard';
import { SchedulingPassCard } from './SchedulingPassCard';
import { SETTINGS_FIELD_LABEL_KEYS } from './settingsFieldLabels';

const indexed = () => SETTINGS_FIELD_LABEL_KEYS.scheduling.map(key => i18n.t(key));

const expectIndexed = (labels: string[]) => {
    expect(labels.length).toBeGreaterThan(0);
    expect(labels.filter(label => !indexed().includes(label))).toEqual([]);
};

describe('Scheduling search labels', () => {
    it.each(['effort / 4', 'effort * 2', 'effort + 3'])('indexes labels rendered for formula %s', async formula => {
        const { user } = renderWithProviders(<EffortModifierCard
            modifier={{ id: 'example', enabled: true, formula, fallback: 'effort', min_value: 0 }}
            onChange={vi.fn()} onRemove={vi.fn()}
        />);
        await user.click(screen.getByRole('button', { name: 'example' }));
        const labels = [...document.querySelectorAll('label')].map(label => label.textContent?.trim() ?? '').filter(Boolean);
        expectIndexed(labels);
    });

    it('indexes labels and headings rendered in a scheduling pass', async () => {
        const { user } = renderWithProviders(<SchedulingPassCard
            pass={{ id: 'example', description: '', enabled: true, filter: { all: [] }, sort: [] }}
            sortableId="example" onChange={vi.fn()} onRemove={vi.fn()}
        />);
        await user.click(screen.getByRole('button', { name: 'example' }));
        const labels = [...document.querySelectorAll('label, h4')].map(label => label.textContent?.trim() ?? '').filter(Boolean);
        expectIndexed(labels);
    });
});

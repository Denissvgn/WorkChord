import { screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { renderWithProviders } from '../../test/renderWithProviders';
import type { TriageItem } from '../../types/triage';
import { TriageList } from './TriageList';

const item: TriageItem = {
    id: 1,
    title: 'Clarify the export format',
    status: 'new',
    labels: [],
    metadata_json: {},
    request_count: 1,
    created_at: '2026-07-01T10:00:00Z',
    updated_at: '2026-07-01T10:00:00Z',
} as TriageItem;

describe('TriageList column names', () => {
    it('labels the first column "Request" in English', () => {
        renderWithProviders(
            <TriageList
                items={[item]}
                selectedId={null}
                projectsById={{}}
                iterationsById={{}}
                listErrorMessage={null}
                isLoading={false}
                activeFilterCount={0}
                onRetry={vi.fn()}
                onSelect={vi.fn()}
                onCreate={vi.fn()}
                onReset={vi.fn()}
            />,
        );
        const headers = screen.getAllByRole('columnheader').map(header => header.textContent?.trim());
        expect(headers[0]).toBe('Request');
        expect(headers).not.toContain('Item');
    });
});

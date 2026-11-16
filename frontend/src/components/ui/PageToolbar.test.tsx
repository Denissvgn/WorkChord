import { describe, expect, it } from 'vitest';
import { render, screen } from '@testing-library/react';
import { PageToolbar } from './PageToolbar';

describe('PageToolbar', () => {
    it('renders its named slots in one row and skips empty ones', () => {
        const { container } = render(
            <PageToolbar
                label="Task controls"
                search={<input aria-label="Search" />}
                filters={<span>Filters</span>}
                viewSwitch={<span>Switch</span>}
            />,
        );

        const toolbar = screen.getByRole('group', { name: 'Task controls' });
        expect(toolbar.children).toHaveLength(3);
        expect(container.querySelector('.wc-page-toolbar-view-options')).toBeNull();
        expect(screen.getByLabelText('Search')).toBeInTheDocument();
    });
});

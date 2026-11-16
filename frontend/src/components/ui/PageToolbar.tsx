import type { ReactNode } from 'react';
import clsx from 'clsx';

/**
 * The single row of controls above a page's records.
 *
 * Usage: a page has at most one PageToolbar. Fill only the named slots:
 * `search` (a search field), `filters` (a FilterBar), `viewSwitch` (a ViewSwitch)
 * and `viewOptions` (sorting, grouping, density). Empty slots are not rendered.
 * It is a single flowing row: search, filters and the view controls share one
 * line while the content area is wide. When it narrows (about a 1024 px
 * viewport with the sidebar open) the filters drop under search and the view
 * controls instead of adding a second toolbar.
 */
export const PageToolbar = ({ search, filters, viewSwitch, viewOptions, label, className }: {
    search?: ReactNode;
    filters?: ReactNode;
    viewSwitch?: ReactNode;
    viewOptions?: ReactNode;
    /** Accessible name of the toolbar region. */
    label?: string;
    className?: string;
}) => (
    <div className="wc-page-toolbar-frame">
        <div role={label ? 'group' : undefined} aria-label={label} className={clsx('wc-page-toolbar', className)} data-testid="page-toolbar">
            {search && <div className="wc-page-toolbar-search">{search}</div>}
            {filters && <div className="wc-page-toolbar-filters">{filters}</div>}
            {(viewSwitch || viewOptions) && (
                <div className="wc-page-toolbar-end">
                    {viewSwitch && <div className="wc-page-toolbar-view-switch">{viewSwitch}</div>}
                    {viewOptions && <div className="wc-page-toolbar-view-options">{viewOptions}</div>}
                </div>
            )}
        </div>
    </div>
);

import { useEffect, useId, useRef, useState } from 'react';
import type { ReactNode } from 'react';
import clsx from 'clsx';
import { ChevronDown, X } from 'lucide-react';
import { useTranslation } from 'react-i18next';

export type FilterBarOption = {
    value: string;
    label: string;
};

export type FilterBarFilter = {
    /** Stable key passed back to `onChange`. */
    id: string;
    /** Names the filter in its control, its chip and the remove button. */
    label: string;
    options: FilterBarOption[];
    /** The chosen option's value; an empty string means the filter is off. */
    value: string;
    /** `date` shows a date field instead of a list; the chip shows the matching option's label when there is one. */
    type?: 'select' | 'date';
    /**
     * A condition with no control of its own, shown only as its chip: one value of a filter that
     * holds several, or a condition another page handed over. Removing the chip sends `onChange(id, '')`.
     */
    chipOnly?: boolean;
};

/** How many filters are shown as quick filters; the rest sit under "More filters". */
const QUICK_FILTER_LIMIT = 5;

const FilterSelect = ({ filter, onChange, id }: { filter: FilterBarFilter; onChange: (value: string) => void; id?: string }) => filter.type === 'date' ? (
    <input
        type="date"
        id={id}
        className="input wc-filter-select wc-filter-date"
        aria-label={filter.label}
        value={filter.value}
        data-active={filter.value !== '' || undefined}
        onChange={event => onChange(event.target.value)}
    />
) : (
    <select
        data-page-chrome-control="select"
        id={id}
        className="input wc-filter-select"
        aria-label={filter.label}
        value={filter.value}
        data-active={filter.value !== '' || undefined}
        onChange={event => onChange(event.target.value)}
    >
        <option value="">{filter.label}</option>
        {filter.options.map(option => (
            <option key={option.value} value={option.value}>{option.label}</option>
        ))}
    </select>
);

/**
 * The one filter control every list page shares.
 *
 * Usage: describe each filter with `filters` (an id, a label, its options and
 * the current value, empty when off) and keep the values in page state.
 * `onChange(id, value)` receives every change and `onClear()` resets all of
 * them, so removing the last active condition returns the default, unfiltered
 * list. The first five filters are quick filters in the row; any others are
 * under a "More filters" popover. Each active condition also shows as one chip
 * that removes just that condition, and "Clear" removes them all. A filter
 * with `type: 'date'` is a date field; a `chipOnly` condition has no control
 * and shows only as its chip. Place it in the `filters` slot of PageToolbar.
 */
export const FilterBar = ({ filters, onChange, onClear, quickLimit = QUICK_FILTER_LIMIT, className }: {
    filters: FilterBarFilter[];
    onChange: (id: string, value: string) => void;
    onClear: () => void;
    /** How many filters stay in the row, at most five; a toolbar short of room shows fewer. */
    quickLimit?: number;
    className?: string;
}) => {
    const { t } = useTranslation();
    const [moreOpen, setMoreOpen] = useState(false);
    const moreButtonRef = useRef<HTMLButtonElement>(null);
    const panelId = useId();

    const controls = filters.filter(filter => !filter.chipOnly);
    const quickCount = Math.min(Math.max(quickLimit, 0), QUICK_FILTER_LIMIT);
    const quickFilters = controls.slice(0, quickCount);
    const moreFilters = controls.slice(quickCount);
    const activeFilters = filters.filter(filter => filter.value !== '');
    // Conditions without a quick control (those under More filters and chip-only ones) are counted on the button.
    const activeMoreCount = activeFilters.length - quickFilters.filter(filter => filter.value !== '').length;

    useEffect(() => {
        if (!moreOpen) return;
        const handleKeyDown = (event: KeyboardEvent) => {
            if (event.key === 'Escape') {
                event.preventDefault();
                setMoreOpen(false);
                moreButtonRef.current?.focus();
            }
        };
        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [moreOpen]);

    const chipText = (filter: FilterBarFilter): ReactNode => {
        const option = filter.options.find(candidate => candidate.value === filter.value);
        return `${filter.label}: ${option?.label ?? filter.value}`;
    };

    return (
        <div className={clsx('wc-filter-bar', className)} data-testid="filter-bar">
            <div className="wc-filter-controls">
                {quickFilters.map(filter => (
                    <FilterSelect key={filter.id} filter={filter} onChange={value => onChange(filter.id, value)} />
                ))}
                {moreFilters.length > 0 && (
                    <div className="wc-filter-more">
                        <button
                            data-page-chrome-control="button"
                            ref={moreButtonRef}
                            type="button"
                            className="btn"
                            aria-haspopup="dialog"
                            aria-expanded={moreOpen}
                            aria-controls={moreOpen ? panelId : undefined}
                            onClick={() => setMoreOpen(open => !open)}
                        >
                            {t('filterBar.more')}
                            {activeMoreCount > 0 && <span className="wc-filter-count" aria-hidden="true">{activeMoreCount}</span>}
                            <ChevronDown aria-hidden="true" className="h-4 w-4" />
                        </button>
                        {moreOpen && (
                            <>
                                <div className="wc-filter-more-backdrop" onClick={() => setMoreOpen(false)} aria-hidden />
                                <div id={panelId} role="dialog" aria-label={t('filterBar.more')} className="wc-filter-more-panel">
                                    {moreFilters.map(filter => (
                                        <label key={filter.id} className="field">
                                            <span className="field-lbl">{filter.label}</span>
                                            <FilterSelect filter={filter} onChange={value => onChange(filter.id, value)} />
                                        </label>
                                    ))}
                                </div>
                            </>
                        )}
                    </div>
                )}
            </div>
            {activeFilters.length > 0 && (
                <ul className="wc-filter-chips" aria-label={t('filterBar.active')}>
                    {activeFilters.map(filter => (
                        <li key={filter.id} className="wc-filter-chip">
                            <span>{chipText(filter)}</span>
                            <button
                                data-page-chrome-control="button"
                                type="button"
                                aria-label={t('filterBar.remove', { filter: chipText(filter) })}
                                title={t('filterBar.remove', { filter: chipText(filter) })}
                                onClick={() => onChange(filter.id, '')}
                            >
                                <X aria-hidden="true" className="h-3 w-3" />
                            </button>
                        </li>
                    ))}
                    <li>
                        <button data-page-chrome-control="button" type="button" className="btn ghost sm" onClick={onClear}>{t('actions.clear')}</button>
                    </li>
                </ul>
            )}
        </div>
    );
};

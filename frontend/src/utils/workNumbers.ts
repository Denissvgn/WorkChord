/**
 * One way to write work numbers everywhere: counts, decimals, percent and effort
 * in days, in the reader's locale. A missing value returns null so the caller says
 * "unknown" in words instead of showing 0.
 */
const known = (value: number | null | undefined): value is number => typeof value === 'number' && Number.isFinite(value);

export const formatCount = (value: number | null | undefined, locale: string) =>
    known(value) ? new Intl.NumberFormat(locale, { maximumFractionDigits: 0 }).format(value) : null;

export const formatDecimal = (value: number | null | undefined, locale: string, digits = 1) =>
    known(value) ? new Intl.NumberFormat(locale, { maximumFractionDigits: digits }).format(value) : null;

/** `value` is 0–100, as the server reports completion. */
export const formatPercent = (value: number | null | undefined, locale: string) =>
    known(value) ? new Intl.NumberFormat(locale, { style: 'percent', maximumFractionDigits: 0 }).format(value / 100) : null;

export const formatEffortDays = (value: number | null | undefined, locale: string) =>
    known(value) ? new Intl.NumberFormat(locale, { style: 'unit', unit: 'day', unitDisplay: 'narrow', maximumFractionDigits: 1 }).format(value) : null;

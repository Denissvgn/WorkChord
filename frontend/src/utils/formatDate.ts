import { format, isValid, parseISO } from 'date-fns';
import { dateFnsLocale } from '../i18n/dateLocale';

export type DateInput = string | Date | null | undefined;

export const EMPTY_DATE = '—';

const DATE_ONLY = /^\d{4}-\d{2}-\d{2}$/;

const parseDateInput = (value: DateInput): { date: Date; dateOnly: boolean } | null => {
    if (value === null || value === undefined || value === '') return null;
    if (value instanceof Date) {
        return isValid(value) ? { date: value, dateOnly: false } : null;
    }
    const dateOnly = DATE_ONLY.test(value);
    const parsed = parseISO(value);
    if (!isValid(parsed)) return null;
    if (dateOnly && format(parsed, 'yyyy-MM-dd') !== value) return null;
    return { date: parsed, dateOnly };
};

/** Build a local Date whose fields equal the source's UTC fields for stable rendering. */
const utcDisplayDate = (date: Date) => new Date(
    date.getUTCFullYear(),
    date.getUTCMonth(),
    date.getUTCDate(),
    date.getUTCHours(),
    date.getUTCMinutes(),
    date.getUTCSeconds(),
    date.getUTCMilliseconds(),
);

/**
 * Format a date using the active application language.
 *
 * Date-only ISO values retain their written calendar day. Timestamp inputs are
 * rendered by their UTC calendar day, so output never varies with browser time
 * zone. Empty and invalid inputs use the shared em-dash fallback.
 */
export const formatDate = (value: DateInput, language?: string): string => {
    const parsed = parseDateInput(value);
    if (!parsed) return EMPTY_DATE;
    const display = parsed.dateOnly ? parsed.date : utcDisplayDate(parsed.date);
    return format(display, 'PP', { locale: dateFnsLocale(language) });
};

/**
 * Format an instant in UTC using the active application language. Date-only
 * values are accepted as midnight UTC; invalid inputs use the shared fallback.
 */
export const formatDateTime = (value: DateInput, language?: string): string => {
    const parsed = parseDateInput(value);
    if (!parsed) return EMPTY_DATE;
    const display = parsed.dateOnly ? parsed.date : utcDisplayDate(parsed.date);
    return `${format(display, 'PP p', { locale: dateFnsLocale(language) })} UTC`;
};

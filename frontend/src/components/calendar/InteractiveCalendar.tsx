import { useTranslation } from 'react-i18next';
import {
    format, startOfMonth, endOfMonth, eachDayOfInterval,
    getDay,
} from 'date-fns';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import clsx from 'clsx';
import { dateFnsLocale } from '../../i18n/dateLocale';

interface CalendarPeriodNavigatorProps {
    year: number;
    month: number;
    holidays: string[];
    weekendDays: number[];
    onYearChange: (year: number) => void;
    onMonthChange: (month: number) => void;
    className?: string;
}

interface InteractiveCalendarProps {
    year: number;
    month: number;
    holidays: string[];
    shortDays: string[];
    weekendDays: number[];
    onYearChange: (year: number) => void;
    onMonthChange: (month: number) => void;
    onAddHoliday: (date: string) => void;
    onRemoveHoliday: (date: string) => void;
    onAddShortDay: (date: string) => void;
    onRemoveShortDay: (date: string) => void;
    onToggleWeekend: (day: number) => void;
}

const getEuropeanDay = (date: Date) => {
    const day = getDay(date);
    return day === 0 ? 6 : day - 1;
};

const isConfiguredWeekend = (date: Date, weekendDays: number[]) => {
    return weekendDays.includes(getEuropeanDay(date));
};

export const CalendarPeriodNavigator = ({
    year,
    month,
    holidays,
    weekendDays,
    onYearChange,
    onMonthChange,
    className,
}: CalendarPeriodNavigatorProps) => {
    const { t, i18n } = useTranslation();
    const locale = dateFnsLocale(i18n.language);
    const currentMonth = new Date(year, month, 1);
    const days = eachDayOfInterval({
        start: startOfMonth(currentMonth),
        end: endOfMonth(currentMonth),
    });
    const monthNames = Array.from({ length: 12 }, (_, index) => {
        const monthDate = new Date(year, index, 1);
        return format(monthDate, 'LLLL', { locale });
    });
    const monthHolidayCount = days.filter(day => holidays.includes(format(day, 'yyyy-MM-dd'))).length;
    const monthWeekendCount = days.filter(day => isConfiguredWeekend(day, weekendDays)).length;
    const canMovePrevious = month > 0;
    const canMoveNext = month < 11;

    const handleYearChange = (value: string) => {
        const nextYear = Number.parseInt(value, 10);
        if (Number.isFinite(nextYear)) {
            onYearChange(nextYear);
        }
    };

    return (
        <div className={clsx('calendar-period-nav', className)}>
            <div className="calendar-period-controls">
                <button
                    type="button"
                    className="btn icon"
                    onClick={() => onMonthChange(Math.max(0, month - 1))}
                    disabled={!canMovePrevious}
                    aria-label={t('calendar.previousMonth')}
                    title={t('calendar.previousMonth')}
                >
                    <ChevronLeft className="h-4 w-4" />
                </button>
                <label className="field calendar-month-field">
                    <span className="field-lbl">{t('calendar.month')}</span>
                    <select
                        value={month}
                        onChange={event => onMonthChange(Number.parseInt(event.target.value, 10))}
                        className="input"
                    >
                        {monthNames.map((name, index) => (
                            <option key={name} value={index}>{name}</option>
                        ))}
                    </select>
                </label>
                <label className="field calendar-year-field">
                    <span className="field-lbl">{t('calendar.displayYear')}</span>
                    <input
                        type="number"
                        min={2000}
                        max={2100}
                        value={year}
                        onChange={event => handleYearChange(event.target.value)}
                        className="input"
                    />
                </label>
                <button
                    type="button"
                    className="btn icon"
                    onClick={() => onMonthChange(Math.min(11, month + 1))}
                    disabled={!canMoveNext}
                    aria-label={t('calendar.nextMonth')}
                    title={t('calendar.nextMonth')}
                >
                    <ChevronRight className="h-4 w-4" />
                </button>
            </div>
            <p className="calendar-period-summary">
                {t('calendar.monthSummary', { weekends: monthWeekendCount, holidays: monthHolidayCount })}
            </p>
        </div>
    );
};

export const InteractiveCalendar = ({
    year,
    month,
    holidays,
    shortDays,
    weekendDays,
    onYearChange,
    onMonthChange,
    onAddHoliday,
    onRemoveHoliday,
    onAddShortDay,
    onRemoveShortDay
}: InteractiveCalendarProps) => {
    const { t } = useTranslation();
    const currentMonth = new Date(year, month, 1);

    const monthStart = startOfMonth(currentMonth);
    const monthEnd = endOfMonth(currentMonth);
    const days = eachDayOfInterval({ start: monthStart, end: monthEnd });
    const startPadding = getEuropeanDay(monthStart);

    const isHoliday = (date: Date) => {
        const dateStr = format(date, 'yyyy-MM-dd');
        return holidays.includes(dateStr);
    };

    const isShortDay = (date: Date) => {
        const dateStr = format(date, 'yyyy-MM-dd');
        return shortDays.includes(dateStr);
    };

    const isWeekendDate = (date: Date) => {
        return isConfiguredWeekend(date, weekendDays);
    };

    // Left click: toggle holiday
    const handleDayClick = (date: Date) => {
        const dateStr = format(date, 'yyyy-MM-dd');
        if (isHoliday(date)) {
            onRemoveHoliday(dateStr);
        } else {
            // If it's a short day, remove first
            if (isShortDay(date)) {
                onRemoveShortDay(dateStr);
            }
            onAddHoliday(dateStr);
        }
    };

    // Right click: toggle short day
    const handleDayRightClick = (e: React.MouseEvent, date: Date) => {
        e.preventDefault();
        const dateStr = format(date, 'yyyy-MM-dd');
        if (isHoliday(date)) return; // Can't mark holiday as short day
        if (isShortDay(date)) {
            onRemoveShortDay(dateStr);
        } else {
            onAddShortDay(dateStr);
        }
    };

    const dayNames = t('calendar.dayNames', { returnObjects: true }) as string[];

    return (
        <div className="calendar-surface">
            <CalendarPeriodNavigator
                year={year}
                month={month}
                holidays={holidays}
                weekendDays={weekendDays}
                onYearChange={onYearChange}
                onMonthChange={onMonthChange}
            />

            <div className="grid grid-cols-7 gap-1">
                {dayNames.map(day => (
                    <div key={day} className="text-center text-xs font-medium text-content-secondary py-1">
                        {day[0]}
                    </div>
                ))}

                {Array.from({ length: startPadding }).map((_, i) => (
                    <div key={`pad-${i}`} className="h-8" />
                ))}

                {days.map(day => {
                    const holiday = isHoliday(day);
                    const shortDay = isShortDay(day);
                    const weekend = isWeekendDate(day);

                    return (
                        <button
                            key={day.toISOString()}
                            type="button"
                            onClick={() => handleDayClick(day)}
                            onContextMenu={(e) => handleDayRightClick(e, day)}
                            className={clsx(
                                "h-8 w-full rounded text-sm font-medium transition-all",
                                "hover:ring-2 hover:ring-focus hover:ring-offset-1",
                                holiday && "bg-feedback-danger text-feedback-danger-emphasis hover:bg-feedback-danger/90",
                                !holiday && shortDay && "bg-feedback-warning text-feedback-warning-emphasis hover:bg-feedback-warning/90",
                                !holiday && !shortDay && weekend && "bg-status-active-muted text-action",
                                !holiday && !shortDay && !weekend && "bg-surface-muted text-content-primary hover:bg-surface-subtle"
                            )}
                            title={
                                holiday ? t('calendar.tooltipHoliday') :
                                    shortDay ? t('calendar.tooltipShortDay') :
                                        weekend ? t('calendar.tooltipWeekend') :
                                            t('calendar.tooltipWorkday')
                            }
                        >
                            {format(day, 'd')}
                        </button>
                    );
                })}
            </div>

            <div className="flex items-center justify-center gap-4 mt-4 text-xs flex-wrap">
                <div className="flex items-center gap-1">
                    <div className="w-3 h-3 rounded bg-status-active-muted border border-action" />
                    <span>{t('calendar.legendWeekend')}</span>
                </div>
                <div className="flex items-center gap-1">
                    <div className="w-3 h-3 rounded bg-feedback-danger" />
                    <span>{t('calendar.legendHoliday')}</span>
                </div>
                <div className="flex items-center gap-1">
                    <div className="w-3 h-3 rounded bg-feedback-warning" />
                    <span>{t('calendar.legendShortDay')}</span>
                </div>
                <div className="flex items-center gap-1">
                    <div className="w-3 h-3 rounded bg-surface-muted border border-border" />
                    <span>{t('calendar.legendWorkday')}</span>
                </div>
            </div>

            <p className="text-xs text-center text-content-tertiary mt-2">
                {t('calendar.help')}
            </p>
        </div>
    );
};

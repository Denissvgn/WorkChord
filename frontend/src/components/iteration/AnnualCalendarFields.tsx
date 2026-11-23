import { useTranslation } from 'react-i18next';
import { Select } from '../common/Select';
import type { Calendar } from '../../types/calendar';

interface Props {
    calendars: Calendar[];
    primary?: Calendar;
    startDate: string;
    endDate: string;
    selected: number[];
    onChange: (ids: number[]) => void;
    disabled?: boolean;
}

export const AnnualCalendarFields = ({ calendars, primary, startDate, endDate, selected, onChange, disabled }: Props) => {
    const { t } = useTranslation();
    if (!primary) return null;
    const years = new Set(calendars.filter(row => selected.includes(row.id)).map(row => row.year));
    const start = Number(startDate.slice(0, 4));
    const end = Number(endDate.slice(0, 4));
    if (start >= 2000 && end <= 2100) {
        for (let year = start; year <= end; year++) years.add(year);
    }
    years.delete(primary.year);
    return <>{Array.from(years).sort((a, b) => a - b).map(year => {
        const options = calendars.filter(row => row.year === year && row.timezone === primary.timezone);
        const current = options.find(row => selected.includes(row.id));
        return <Select key={year} label={t('iterationForm.calendarForYear', { year })} value={current?.id ?? ''} disabled={disabled}
            onChange={event => {
                const retained = selected.filter(id => calendars.find(row => row.id === id)?.year !== year);
                const next = event.target.value ? [...retained, Number(event.target.value)] : retained;
                onChange(next.sort((a, b) => a - b));
            }}>
            <option value="">{t('iterationForm.annualCalendarNotSelected')}</option>
            {options.map(row => <option key={row.id} value={row.id}>{row.name}</option>)}
        </Select>;
    })}</>;
};

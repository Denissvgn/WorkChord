import { useId, useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import api from '../../services/api';
import { calendarService } from '../../services/calendarService';
import { Button } from '../common/Button';
import { QueryErrorState } from '../feedback/QueryState';
import { getApiErrorMessage } from '../../utils/apiError';

interface Absence { id: number; version: number; start_date: string; end_date: string }
interface Availability { version: number; calendar_id: number | null; calendar_selection_required: boolean; allocation_calendar_conflicts: number[]; absences: Absence[] }
interface Capacity {
    calendar_uncertain: boolean; outside_calendar_year: boolean; timezone: string | null; has_unknown_effort: boolean;
    allocations: { member_id: number; availability_percent: number; operational_utilization: number; professionalism_coefficient: number }[];
    days: { date: string; available_hours: number | null; allocated_hours: number; productive_hours: number | null; private_busy_hours: number; committed_effort_hours: number; overallocated_hours: number | null }[];
}

const localDate = () => { const now = new Date(); return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`; };

export const PersonCapacity = ({ profileId, startDate, endDate, manage = false }: { profileId: number; startDate?: string; endDate?: string; manage?: boolean }) => {
    const { t } = useTranslation();
    const id = useId();
    const [expanded, setExpanded] = useState(false);
    const client = useQueryClient();
    const [start, setStart] = useState(startDate ?? localDate());
    const [end, setEnd] = useState(endDate ?? startDate ?? localDate());
    const [calendar, setCalendar] = useState('');
    const [absenceStart, setAbsenceStart] = useState('');
    const [absenceEnd, setAbsenceEnd] = useState('');
    const [editing, setEditing] = useState<Absence | null>(null);
    // feedback-policy: query loading,error,retry,empty - scoped results keep explicit loading, retry and empty feedback.
    const capacity = useQuery({ queryKey: ['profile-capacity', profileId, start, end], enabled: expanded && Boolean(start && end),
        queryFn: async () => (await api.get<Capacity>(`/team-member-profiles/${profileId}/capacity`, { params: { start, end } })).data });
    // feedback-policy: query loading,error,retry,empty - scoped results keep explicit loading, retry and empty feedback.
    const availability = useQuery({ queryKey: ['profile-availability', profileId], enabled: expanded && manage,
        queryFn: async () => (await api.get<Availability>(`/team-member-profiles/${profileId}/availability`)).data });
    // feedback-policy: query loading,error,retry,empty - scoped results keep explicit loading, retry and empty feedback.
    const calendars = useQuery({ queryKey: ['calendars'], enabled: expanded && manage, queryFn: calendarService.getAll });
    const refresh = async () => { await client.invalidateQueries({ queryKey: ['profile-capacity'] }); await availability.refetch(); await client.invalidateQueries({ queryKey: ['gantt'] }); };
    // feedback-policy: mutation pending,inline - disable repeat writes and retain the draft on failure.
    const selectCalendar = useMutation({ mutationFn: async () => api.put(`/team-member-profiles/${profileId}/availability`, { calendar_id: Number(calendar), expected_version: availability.data!.version }), onSuccess: refresh });
    // feedback-policy: mutation pending,inline - disable repeat writes and retain the draft on failure.
    const absence = useMutation({ mutationFn: async (removed?: Absence) => {
        const current = removed ?? editing;
        const body = { start_date: removed?.start_date ?? absenceStart, end_date: removed?.end_date ?? absenceEnd };
        return current ? api.put(`/team-member-profiles/${profileId}/absences/${current.id}`, { ...body, expected_version: current.version, deleted: Boolean(removed) })
            : api.post(`/team-member-profiles/${profileId}/absences`, body);
    }, onSuccess: async () => { setEditing(null); setAbsenceStart(''); setAbsenceEnd(''); await refresh(); } });

    return <details className="space-y-3 rounded-md border border-border p-3" onToggle={event => setExpanded(event.currentTarget.open)}>
        <summary className="cursor-pointer font-medium text-content-primary">{t(manage ? 'teamwork.myAvailability' : 'teamwork.personCapacity')}</summary>
        <p className="text-sm text-content-secondary">{t('teamwork.capacityHelp')}</p>
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
            <label className="text-sm" htmlFor={`${id}-start`}>{t('teamwork.from')}<input id={`${id}-start`} type="date" className="input w-full" value={start} onChange={event => setStart(event.target.value)} /></label>
            <label className="text-sm" htmlFor={`${id}-end`}>{t('teamwork.to')}<input id={`${id}-end`} type="date" className="input w-full" value={end} onChange={event => setEnd(event.target.value)} /></label>
        </div>
        {capacity.isLoading && <p role="status">{t('common.loading')}</p>}
        {capacity.isError && <QueryErrorState error={capacity.error} fallback={t('teamwork.loadFailed')} onRetry={() => void capacity.refetch()} />}
        {capacity.data && <>
            <p className="text-sm text-content-secondary">{t('teamwork.capacityFormula')} · {capacity.data.timezone ?? t('teamwork.unknownCalendar')}</p>
            {capacity.data.allocations.map(item => <p key={item.member_id} className="text-sm text-content-secondary">{t('teamwork.capacityFactors', { availability: item.availability_percent, utilization: item.operational_utilization, coefficient: item.professionalism_coefficient })}</p>)}
            {(capacity.data.calendar_uncertain || capacity.data.outside_calendar_year) && <p role="status" className="text-sm text-feedback-warning-foreground">{t('teamwork.calendarUncertain')}</p>}
            {capacity.data.has_unknown_effort && <p className="text-sm text-feedback-warning-foreground">{t('teamwork.unknownCommitment')}</p>}
            <div className="max-h-64 overflow-auto"><table className="w-full text-left text-sm"><caption className="sr-only">{t('teamwork.capacityHours')}</caption><thead><tr>{['date', 'available', 'allocated', 'productive', 'committed'].map(key => <th key={key} className="px-2 py-2 font-medium">{t(`teamwork.capacity_${key}`)}</th>)}</tr></thead>
                <tbody>{capacity.data.days.map(day => <tr key={day.date} className="border-t border-border"><td className="whitespace-nowrap px-2 py-2">{day.date}</td><td className="px-2">{day.available_hours ?? '—'}</td><td className="px-2">{day.allocated_hours}{day.overallocated_hours != null && day.overallocated_hours > 0 && <span className="block text-feedback-warning-foreground">{t('teamwork.overallocated', { hours: day.overallocated_hours })}</span>}</td><td className="px-2">{day.productive_hours ?? '—'}</td><td className="px-2">{day.committed_effort_hours}</td></tr>)}</tbody></table></div>
            <p className="text-xs text-content-secondary">{t('teamwork.capacityRounding')}</p>
        </>}
        {manage && <>
            {(availability.isLoading || calendars.isLoading) && <p role="status">{t('common.loading')}</p>}
            {availability.isError && <QueryErrorState error={availability.error} fallback={t('teamwork.loadFailed')} onRetry={() => void availability.refetch()} />}
            {calendars.isError && <QueryErrorState error={calendars.error} fallback={t('teamwork.loadFailed')} onRetry={() => void calendars.refetch()} />}
            {availability.data && <>
                {(availability.data.calendar_selection_required || availability.data.allocation_calendar_conflicts.length > 0) && <p className="text-sm text-feedback-warning-foreground">{t('teamwork.chooseCalendar')}</p>}
                <label className="field-lbl" htmlFor={`${id}-calendar`}>{t('teamwork.personCalendar')}</label>
                <select id={`${id}-calendar`} className="input w-full" value={calendar || availability.data.calendar_id || ''} onChange={event => setCalendar(event.target.value)}><option value="">{t('teamwork.chooseCalendar')}</option>{calendars.data?.map(item => <option key={item.id} value={item.id}>{item.name} · {item.year} · {item.timezone ?? t('teamwork.unknownCalendar')}</option>)}</select>
                <Button type="button" size="sm" variant="secondary" disabled={!calendar || selectCalendar.isPending} onClick={() => selectCalendar.mutate()}>{t('teamwork.saveCalendar')}</Button>
                <h4 className="pt-3 font-medium">{t('teamwork.absences')}</h4>
                <ul className="space-y-2">{availability.data.absences.map(item => <li key={item.id} className="flex flex-wrap items-center gap-2 text-sm"><span>{item.start_date} – {item.end_date}</span>
                    <Button type="button" size="sm" variant="ghost" disabled={absence.isPending} onClick={() => { setEditing(item); setAbsenceStart(item.start_date); setAbsenceEnd(item.end_date); }}>{t('teamwork.edit')}</Button>
                    <Button type="button" size="sm" variant="ghost" disabled={absence.isPending} onClick={() => absence.mutate(item)}>{t('teamwork.remove')}</Button></li>)}</ul>
                <div className="grid grid-cols-1 gap-3 sm:grid-cols-2"><label className="text-sm" htmlFor={`${id}-absence-start`}>{t('teamwork.absenceFrom')}<input id={`${id}-absence-start`} type="date" className="input w-full" value={absenceStart} onChange={event => setAbsenceStart(event.target.value)} /></label><label className="text-sm" htmlFor={`${id}-absence-end`}>{t('teamwork.absenceTo')}<input id={`${id}-absence-end`} type="date" className="input w-full" value={absenceEnd} onChange={event => setAbsenceEnd(event.target.value)} /></label></div>
                <Button type="button" size="sm" disabled={!absenceStart || !absenceEnd || absenceEnd < absenceStart || absence.isPending} onClick={() => absence.mutate(undefined)}>{t(editing ? 'teamwork.updateAbsence' : 'teamwork.addAbsence')}</Button>
            </>}
            {(absence.isError || selectCalendar.isError) && <p role="alert" className="text-sm text-feedback-danger-foreground">{getApiErrorMessage(absence.error ?? selectCalendar.error, t('teamwork.saveFailed'))}</p>}
        </>}
    </details>;
};

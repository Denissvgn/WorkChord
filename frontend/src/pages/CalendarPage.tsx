import { useEffect, useMemo, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { eachDayOfInterval, format, parseISO } from 'date-fns';
import type { Locale } from 'date-fns';
import {
    CalendarDays,
    CalendarRange,
    Download,
    Grid,
    List,
    Plane,
    Plus,
    Save,
    Trash2,
    Upload,
    X,
} from 'lucide-react';
import { Button } from '../components/common/Button';
import { Input } from '../components/common/Input';
import { useConfirmDialog } from '../components/common/useConfirmDialog';
import { QueryErrorState } from '../components/feedback/QueryState';
import { CalendarPeriodNavigator, InteractiveCalendar } from '../components/calendar/InteractiveCalendar';
import { OverflowMenu } from '../components/ui';
import { PlanningWorkbenchFrame } from '../components/planning/PlanningWorkbenchFrame';
import { calendarService } from '../services/calendarService';
import { iterationService } from '../services/iterationService';
import { teamService } from '../services/teamService';
import { dateFnsLocale } from '../i18n/dateLocale';
import { useIterationStore } from '../store/iterationStore';
import type { Calendar as WorkCalendar, CalendarCreate, CalendarUpdate } from '../types/calendar';
import type { TeamMember, Vacation } from '../types/team';

interface CalendarDraft {
    year: number;
    holidays: string[];
    weekend_days: number[];
    short_days: string[];
}

interface VacationRow {
    member: TeamMember;
    vacation: Vacation;
}

const makeDraft = (calendar: WorkCalendar): CalendarDraft => ({
    year: calendar.year,
    holidays: [...(calendar.holidays || [])].sort(),
    weekend_days: [...(calendar.weekend_days || [5, 6])].sort(),
    short_days: [...(calendar.short_days || [])].sort(),
});

const apiErrorMessage = (error: unknown, fallback: string) => {
    if (typeof error === 'object' && error !== null && 'response' in error) {
        const response = (error as { response?: { data?: { detail?: string } } }).response;
        return response?.data?.detail || fallback;
    }
    return fallback;
};

const toDateKey = (date: Date) => format(date, 'yyyy-MM-dd');

const getPythonWeekday = (date: Date) => {
    const day = date.getDay();
    return day === 0 ? 6 : day - 1;
};

const isDateInYear = (dateKey: string, year: number) => {
    try {
        return parseISO(dateKey).getFullYear() === year;
    } catch {
        return false;
    }
};

const formatDate = (dateKey: string, locale: Locale) => {
    try {
        return format(parseISO(dateKey), 'PP', { locale });
    } catch {
        return dateKey;
    }
};

const mergeDate = (values: string[], dateKey: string) => (
    Array.from(new Set([...values, dateKey])).sort()
);

const CalendarPage = () => {
    const { t, i18n } = useTranslation();
    const locale = dateFnsLocale(i18n.language);
    const queryClient = useQueryClient();
    const { selectedIterationId, setSelectedIterationId } = useIterationStore();
    const { requestConfirmation, confirmationDialog } = useConfirmDialog();
    const draftedCalendarId = useRef<number | null>(null);

    const [draft, setDraft] = useState<CalendarDraft | null>(null);
    const [selectedCalendarId, setSelectedCalendarId] = useState<number | null>(null);
    const [isCreatingCalendar, setIsCreatingCalendar] = useState(false);
    const [newCalendarName, setNewCalendarName] = useState('');
    const [newCalendarYear, setNewCalendarYear] = useState('');
    const [viewMode, setViewMode] = useState<'calendar' | 'list'>('calendar');
    const [visibleMonth, setVisibleMonth] = useState(0);
    const [manualDate, setManualDate] = useState('');
    const [rangeStart, setRangeStart] = useState('');
    const [rangeEnd, setRangeEnd] = useState('');
    const [publicCountry, setPublicCountry] = useState('US');
    const [calendarSummary, setCalendarSummary] = useState('');
    const [calendarError, setCalendarError] = useState('');
    const [selectedMemberId, setSelectedMemberId] = useState('');
    const [vacationStart, setVacationStart] = useState('');
    const [vacationEnd, setVacationEnd] = useState('');
    const [vacationSummary, setVacationSummary] = useState('');
    const [vacationError, setVacationError] = useState('');

    // feedback-policy: query loading,error,retry,empty
    const { data: calendars = [], isLoading: isLoadingCalendars, error: calendarsError, refetch: refetchCalendars } = useQuery({
        queryKey: ['calendars'],
        queryFn: calendarService.getAll,
    });
    const calendar = calendars.find(item => item.id === selectedCalendarId) ?? calendars[0] ?? null;

    // feedback-policy: query loading,error,retry,empty
    const { data: iterations = [], isLoading: isLoadingIterations, error: iterationsError, refetch: refetchIterations } = useQuery({
        queryKey: ['iterations'],
        queryFn: iterationService.getAll,
    });

    useEffect(() => {
        if (!calendar) return;
        if (draftedCalendarId.current === calendar.id) return;
        draftedCalendarId.current = calendar.id;
        let cancelled = false;
        queueMicrotask(() => {
            if (cancelled) return;
            setDraft(makeDraft(calendar));
            setVisibleMonth(0);
            setCalendarSummary('');
            setCalendarError('');
        });
        return () => {
            cancelled = true;
        };
    }, [calendar]);

    useEffect(() => {
        if (iterations.length === 0) {
            if (selectedIterationId !== 0) setSelectedIterationId(0);
            return;
        }
        const exists = iterations.some(iteration => iteration.id === selectedIterationId);
        if (selectedIterationId === 0 || !exists) {
            setSelectedIterationId(iterations[0].id);
        }
    }, [iterations, selectedIterationId, setSelectedIterationId]);

    const selectedIteration = iterations.find(iteration => iteration.id === selectedIterationId) ?? null;
    const hasSelectedIteration = selectedIteration !== null;

    // feedback-policy: query loading,error,retry,empty
    const { data: teamMembers = [], isLoading: isLoadingTeam, error: teamError, refetch: refetchTeam } = useQuery({
        queryKey: ['team', selectedIterationId],
        queryFn: () => teamService.getByIteration(selectedIterationId),
        enabled: hasSelectedIteration,
    });

    useEffect(() => {
        if (teamMembers.length === 0) {
            if (selectedMemberId) {
                let cancelled = false;
                queueMicrotask(() => {
                    if (!cancelled) setSelectedMemberId('');
                });
                return () => {
                    cancelled = true;
                };
            }
            return;
        }
        const exists = teamMembers.some(member => String(member.id) === selectedMemberId);
        if (!exists) {
            const nextMemberId = String(teamMembers[0].id);
            let cancelled = false;
            queueMicrotask(() => {
                if (!cancelled) setSelectedMemberId(nextMemberId);
            });
            return () => {
                cancelled = true;
            };
        }
    }, [teamMembers, selectedMemberId]);

    // feedback-policy: mutation pending,inline
    const updateCalendarMutation = useMutation({
        mutationFn: ({ calendarId, data }: { calendarId: number; data: CalendarUpdate }) =>
            calendarService.update(calendarId, data),
        onSuccess: (data) => {
            setDraft(makeDraft(data));
            queryClient.invalidateQueries({ queryKey: ['calendars'] });
            setCalendarError('');
            setCalendarSummary(t('calendar.settingsSaved'));
        },
        onError: (error: unknown) => {
            setCalendarSummary('');
            setCalendarError(apiErrorMessage(error, t('calendar.saveFailed')));
        },
    });

    // feedback-policy: mutation pending,inline
    const createCalendarMutation = useMutation({
        mutationFn: (data: CalendarCreate) => calendarService.create(data),
        onSuccess: (created) => {
            queryClient.invalidateQueries({ queryKey: ['calendars'] });
            setSelectedCalendarId(created.id);
            setIsCreatingCalendar(false);
            setNewCalendarName('');
            setNewCalendarYear('');
            setCalendarError('');
            setCalendarSummary(t('calendar.calendarCreated', { name: created.name }));
        },
        onError: (error: unknown) => {
            setCalendarSummary('');
            setCalendarError(apiErrorMessage(error, t('calendar.createFailed')));
        },
    });

    // feedback-policy: mutation pending,inline
    const deleteCalendarMutation = useMutation({
        mutationFn: (calendarId: number) => calendarService.delete(calendarId),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['calendars'] });
            setSelectedCalendarId(null);
            draftedCalendarId.current = null;
            setCalendarError('');
            setCalendarSummary(t('calendar.calendarDeleted'));
        },
        onError: (error: unknown) => {
            setCalendarSummary('');
            setCalendarError(apiErrorMessage(error, t('calendar.deleteFailed')));
        },
    });

    // feedback-policy: mutation pending,inline
    const publicImportMutation = useMutation({
        mutationFn: ({ calendarId, country, year }: { calendarId: number; country: string; year: number }) =>
            calendarService.importPublicHolidays(calendarId, country, year),
        onSuccess: (data) => {
            setDraft(prev => prev ? ({
                ...prev,
                holidays: data.calendar.holidays,
                weekend_days: data.calendar.weekend_days,
                short_days: data.calendar.short_days,
            }) : makeDraft(data.calendar));
            queryClient.invalidateQueries({ queryKey: ['calendars'] });
            setCalendarError(data.errors.length ? data.errors.map(err => `${err.row}: ${err.message}`).join('; ') : '');
            setCalendarSummary(t('calendar.importSummary', {
                imported: data.imported_count,
                skipped: data.skipped_count,
            }));
        },
        onError: (error: unknown) => {
            setCalendarSummary('');
            setCalendarError(apiErrorMessage(error, t('calendar.importFailed')));
        },
    });

    // feedback-policy: mutation pending,inline
    const holidayCsvImportMutation = useMutation({
        mutationFn: ({ calendarId, csvText }: { calendarId: number; csvText: string }) =>
            calendarService.importHolidayCsv(calendarId, csvText),
        onSuccess: (data) => {
            setDraft(prev => prev ? ({
                ...prev,
                holidays: data.calendar.holidays,
                weekend_days: data.calendar.weekend_days,
                short_days: data.calendar.short_days,
            }) : makeDraft(data.calendar));
            queryClient.invalidateQueries({ queryKey: ['calendars'] });
            setCalendarError(data.errors.length ? data.errors.map(err => `${err.row}: ${err.message}`).join('; ') : '');
            setCalendarSummary(t('calendar.importSummary', {
                imported: data.imported_count,
                skipped: data.skipped_count,
            }));
        },
        onError: (error: unknown) => {
            setCalendarSummary('');
            setCalendarError(apiErrorMessage(error, t('calendar.importFailed')));
        },
    });

    // feedback-policy: mutation pending,inline
    const addVacationMutation = useMutation({
        mutationFn: ({ memberId, start_date, end_date }: { memberId: number; start_date: string; end_date: string }) =>
            teamService.addVacation(memberId, { start_date, end_date }),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['team', selectedIterationId] });
            setVacationStart('');
            setVacationEnd('');
            setVacationError('');
            setVacationSummary(t('calendar.vacationAdded'));
        },
        onError: (error: unknown) => {
            setVacationSummary('');
            setVacationError(apiErrorMessage(error, t('teamVacations.importFailed')));
        },
    });

    // feedback-policy: mutation pending,inline
    const deleteVacationMutation = useMutation({
        mutationFn: teamService.deleteVacation,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['team', selectedIterationId] });
            setVacationError('');
            setVacationSummary(t('calendar.vacationDeleted'));
        },
        onError: (error: unknown) => {
            setVacationSummary('');
            setVacationError(apiErrorMessage(error, t('calendar.vacationDeleteFailed')));
        },
    });

    // feedback-policy: mutation pending,inline
    const vacationCsvImportMutation = useMutation({
        mutationFn: ({ iterationId, csvText }: { iterationId: number; csvText: string }) =>
            teamService.importVacationsCsv(iterationId, csvText),
        onSuccess: (data) => {
            queryClient.invalidateQueries({ queryKey: ['team', selectedIterationId] });
            setVacationSummary(t('teamVacations.importSummary', {
                imported: data.imported_count,
                skipped: data.skipped_count,
            }));
            setVacationError(data.errors.length ? data.errors.map(err => `${err.row}: ${err.message}`).join('; ') : '');
        },
        onError: (error: unknown) => {
            setVacationSummary('');
            setVacationError(apiErrorMessage(error, t('teamVacations.importFailed')));
        },
    });

    const displayYear = draft?.year ?? new Date().getFullYear();
    const yearDays = useMemo(() => eachDayOfInterval({
        start: new Date(displayYear, 0, 1),
        end: new Date(displayYear, 11, 31),
    }), [displayYear]);

    const selectedYearHolidays = useMemo(
        () => (draft?.holidays || []).filter(day => isDateInYear(day, displayYear)).sort(),
        [draft?.holidays, displayYear],
    );

    const selectedYearShortDays = useMemo(
        () => (draft?.short_days || []).filter(day => isDateInYear(day, displayYear)).sort(),
        [draft?.short_days, displayYear],
    );

    const yearSummary = useMemo(() => {
        const holidaySet = new Set(selectedYearHolidays);
        const weekendSet = new Set(draft?.weekend_days || []);
        const weekendDates = yearDays.filter(day => weekendSet.has(getPythonWeekday(day)));
        const workingDays = yearDays.filter(day => {
            const key = toDateKey(day);
            return !holidaySet.has(key) && !weekendSet.has(getPythonWeekday(day));
        });
        return {
            totalDays: yearDays.length,
            weekendDays: weekendDates.length,
            companyDays: selectedYearHolidays.length,
            shortDays: selectedYearShortDays.length,
            workingDays: workingDays.length,
        };
    }, [draft?.weekend_days, selectedYearHolidays, selectedYearShortDays, yearDays]);

    const vacationRows: VacationRow[] = useMemo(() => (
        teamMembers
            .flatMap(member => (member.vacations || []).map(vacation => ({ member, vacation })))
            .sort((a, b) => a.vacation.start_date.localeCompare(b.vacation.start_date) || a.member.name.localeCompare(b.member.name))
    ), [teamMembers]);

    const dayNames = (t('calendar.dayNames', { returnObjects: true }) as string[]) || [];
    const weekdayNames = dayNames.length === 7 ? dayNames : ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

    const setDraftYear = (year: number) => {
        if (!Number.isFinite(year)) return;
        setDraft(prev => prev ? { ...prev, year } : prev);
    };

    const setCalendarMonth = (month: number) => {
        if (!Number.isFinite(month)) return;
        setVisibleMonth(Math.min(11, Math.max(0, month)));
    };

    const toggleWeekend = (day: number) => {
        setDraft(prev => {
            if (!prev) return prev;
            const exists = prev.weekend_days.includes(day);
            return {
                ...prev,
                weekend_days: exists
                    ? prev.weekend_days.filter(value => value !== day)
                    : [...prev.weekend_days, day].sort(),
            };
        });
    };

    const addCompanyDay = (dateKey: string) => {
        if (!dateKey) return;
        setDraft(prev => prev ? ({
            ...prev,
            holidays: mergeDate(prev.holidays, dateKey),
            short_days: prev.short_days.filter(day => day !== dateKey),
        }) : prev);
    };

    const removeCompanyDay = (dateKey: string) => {
        setDraft(prev => prev ? ({
            ...prev,
            holidays: prev.holidays.filter(day => day !== dateKey),
        }) : prev);
    };

    const addShortDay = (dateKey: string) => {
        if (!dateKey) return;
        setDraft(prev => prev && !prev.holidays.includes(dateKey) ? ({
            ...prev,
            short_days: mergeDate(prev.short_days, dateKey),
        }) : prev);
    };

    const removeShortDay = (dateKey: string) => {
        setDraft(prev => prev ? ({
            ...prev,
            short_days: prev.short_days.filter(day => day !== dateKey),
        }) : prev);
    };

    const addManualDate = () => {
        addCompanyDay(manualDate);
        setManualDate('');
    };

    const addManualRange = () => {
        if (!rangeStart || !rangeEnd || rangeStart > rangeEnd) return;
        const days = eachDayOfInterval({
            start: parseISO(rangeStart),
            end: parseISO(rangeEnd),
        })
            .map(toDateKey)
            .filter(day => isDateInYear(day, displayYear));
        setDraft(prev => prev ? ({
            ...prev,
            holidays: Array.from(new Set([...prev.holidays, ...days])).sort(),
            short_days: prev.short_days.filter(day => !days.includes(day)),
        }) : prev);
        setRangeStart('');
        setRangeEnd('');
    };

    const handleHolidayCsvFile = async (file: File | null) => {
        if (!file || !calendar) return;
        holidayCsvImportMutation.mutate({ calendarId: calendar.id, csvText: await file.text() });
    };

    const handleVacationCsvFile = async (file: File | null) => {
        if (!file || !selectedIteration) return;
        vacationCsvImportMutation.mutate({ iterationId: selectedIteration.id, csvText: await file.text() });
    };

    const saveSettings = () => {
        if (!calendar || !draft) return;
        updateCalendarMutation.mutate({
            calendarId: calendar.id,
            data: {
                year: draft.year,
                holidays: draft.holidays,
                weekend_days: draft.weekend_days,
                short_days: draft.short_days,
            },
        });
    };

    const startCreateCalendar = () => {
        const suggestedYear = (draft?.year ?? new Date().getFullYear()) + 1;
        setNewCalendarYear(String(suggestedYear));
        setNewCalendarName(t('calendar.defaultCalendarName', { year: suggestedYear }));
        setIsCreatingCalendar(true);
    };

    const submitCreateCalendar = () => {
        const year = Number(newCalendarYear);
        if (!newCalendarName.trim() || !Number.isInteger(year) || year < 2000 || year > 2100) {
            setCalendarSummary('');
            setCalendarError(t('calendar.createValidation'));
            return;
        }
        createCalendarMutation.mutate({
            name: newCalendarName.trim(),
            year,
            holidays: [],
            weekend_days: draft?.weekend_days ?? [5, 6],
            short_days: [],
        });
    };

    const confirmDeleteCalendar = () => {
        if (!calendar) return;
        requestConfirmation({
            title: t('calendar.deleteCalendar'),
            description: t('calendar.deleteCalendarConfirm', { name: calendar.name, year: calendar.year }),
            confirmLabel: t('actions.delete'),
            cancelLabel: t('actions.cancel'),
            closeLabel: t('actions.close'),
            onConfirm: () => deleteCalendarMutation.mutateAsync(calendar.id),
        });
    };

    const addVacation = () => {
        const memberId = Number(selectedMemberId);
        if (!memberId || !vacationStart || !vacationEnd || vacationStart > vacationEnd) return;
        addVacationMutation.mutate({
            memberId,
            start_date: vacationStart,
            end_date: vacationEnd,
        });
    };

    const queryError = calendarsError ?? iterationsError ?? teamError;
    if (queryError) {
        return (
            <PlanningWorkbenchFrame
                title={t('calendar.workCalendar')}
                description={t('calendar.persistentDescription')}
            >
                <QueryErrorState
                    error={queryError}
                    onRetry={() => {
                        void refetchCalendars();
                        void refetchIterations();
                        if (hasSelectedIteration) void refetchTeam();
                    }}
                />
            </PlanningWorkbenchFrame>
        );
    }

    if (isLoadingCalendars) {
        return (
            <PlanningWorkbenchFrame
                title={t('calendar.workCalendar')}
                description={t('calendar.persistentDescription')}
            >
                <div className="banner muted" role="status">{t('common.loading')}</div>
            </PlanningWorkbenchFrame>
        );
    }

    if (!calendar) {
        return (
            <PlanningWorkbenchFrame
                title={t('calendar.workCalendar')}
                description={t('calendar.persistentDescription')}
            >
                <div className="empty">
                    <h4>{t('calendar.unavailable')}</h4>
                    <p>{t('calendar.noCalendarsBody')}</p>
                    <div className="empty-actions">
                        {isCreatingCalendar ? (
                            <div className="row" style={{gap:8, flexWrap:'wrap', justifyContent:'center'}}>
                                <Input
                                    aria-label={t('calendar.calendarName')}
                                    placeholder={t('calendar.calendarName')}
                                    value={newCalendarName}
                                    onChange={event => setNewCalendarName(event.target.value)}
                                />
                                <Input
                                    aria-label={t('calendar.calendarYear')}
                                    placeholder={t('calendar.calendarYear')}
                                    type="number"
                                    min="2000"
                                    max="2100"
                                    value={newCalendarYear}
                                    onChange={event => setNewCalendarYear(event.target.value)}
                                />
                                <Button type="button" onClick={submitCreateCalendar} isLoading={createCalendarMutation.isPending}>
                                    {t('calendar.createCalendar')}
                                </Button>
                                <Button type="button" variant="ghost" onClick={() => setIsCreatingCalendar(false)}>
                                    {t('actions.cancel')}
                                </Button>
                            </div>
                        ) : (
                            <Button type="button" onClick={startCreateCalendar}>
                                <Plus className="w-4 h-4" />
                                {t('calendar.newCalendar')}
                            </Button>
                        )}
                    </div>
                    {calendarError && <div className="banner warn" style={{marginTop:12}}>{calendarError}</div>}
                </div>
            </PlanningWorkbenchFrame>
        );
    }

    if (!draft) {
        return (
            <PlanningWorkbenchFrame
                title={t('calendar.workCalendar')}
                description={t('calendar.persistentDescription')}
            >
                <div className="banner muted" role="status">{t('common.loading')}</div>
            </PlanningWorkbenchFrame>
        );
    }

    return (
        <PlanningWorkbenchFrame
            title={t('calendar.workCalendar')}
            description={t('calendar.persistentDescription')}
            facts={[
                {
                    id: 'calendar',
                    label: t('calendar.calendarName'),
                    value: `${calendar.name} · ${calendar.year}`,
                },
                {
                    id: 'working-days',
                    label: t('calendar.workingDays'),
                    value: yearSummary.workingDays,
                },
                {
                    id: 'company-days',
                    label: t('calendar.companyDays'),
                    value: yearSummary.companyDays,
                },
                {
                    id: 'short-days',
                    label: t('calendar.shortDays'),
                    value: yearSummary.shortDays,
                },
            ]}
            contextControl={calendars.length > 1 ? (
                <select
                    className="input planning-workbench-select"
                    value={calendar.id}
                    onChange={event => setSelectedCalendarId(Number(event.target.value))}
                    aria-label={t('calendar.selectCalendar')}
                >
                    {calendars.map(item => (
                        <option key={item.id} value={item.id}>
                            {item.name} ({item.year})
                        </option>
                    ))}
                </select>
            ) : undefined}
            secondaryActions={(
                <Button type="button" variant="secondary" onClick={startCreateCalendar}>
                    <Plus className="h-4 w-4" />
                    {t('calendar.newCalendar')}
                </Button>
            )}
            primaryAction={(
                <Button
                    type="button"
                    onClick={saveSettings}
                    isLoading={updateCalendarMutation.isPending}
                >
                    <Save className="h-4 w-4" />
                    {t('calendar.saveSettings')}
                </Button>
            )}
            overflowAction={(
                <OverflowMenu
                    label={t('actions.moreActions')}
                    items={[
                        {
                            label: calendars.length <= 1
                                ? t('calendar.deleteLastCalendarHint')
                                : t('calendar.deleteCalendar'),
                            icon: <Trash2 className="h-4 w-4" aria-hidden="true" />,
                            onSelect: confirmDeleteCalendar,
                            disabled: calendars.length <= 1 || deleteCalendarMutation.isPending,
                            tone: 'danger',
                        },
                    ]}
                />
            )}
            state={(isCreatingCalendar || calendarSummary || calendarError) ? (
                <>
            {isCreatingCalendar && (
                <div className="card card-pad">
                    <div className="calendar-create-row">
                        <label className="field calendar-create-name">
                            <span className="field-lbl">{t('calendar.calendarName')}</span>
                            <Input
                                value={newCalendarName}
                                onChange={event => setNewCalendarName(event.target.value)}
                                placeholder={t('calendar.calendarName')}
                            />
                        </label>
                        <label className="field calendar-create-year">
                            <span className="field-lbl">{t('calendar.calendarYear')}</span>
                            <Input
                                type="number"
                                min="2000"
                                max="2100"
                                value={newCalendarYear}
                                onChange={event => setNewCalendarYear(event.target.value)}
                                placeholder={t('calendar.calendarYear')}
                            />
                        </label>
                        <Button type="button" onClick={submitCreateCalendar} isLoading={createCalendarMutation.isPending}>
                            {t('calendar.createCalendar')}
                        </Button>
                        <Button type="button" variant="ghost" onClick={() => setIsCreatingCalendar(false)}>
                            {t('actions.cancel')}
                        </Button>
                    </div>
                    <p className="muted" style={{margin:'8px 0 0', fontSize:12.5}}>{t('calendar.newCalendarHint')}</p>
                </div>
            )}

            {(calendarSummary || calendarError) && (
                <div className={`banner ${calendarError ? 'warn' : 'done'}`}>
                    {calendarSummary}
                    {calendarError && <div>{calendarError}</div>}
                </div>
            )}
                </>
            ) : undefined}
        >

            <section className="wc-content-rail">
                <div className="card card-pad">
                    <div className="between wrap" style={{marginBottom:16}}>
                        <div>
                            <h2 className="row" style={{margin:0, fontSize:16, fontWeight:600}}>
                                <CalendarDays className="h-5 w-5 text-action" />
                                {t('calendar.companyNonWorkingDays')}
                            </h2>
                            <p className="muted" style={{margin:0, fontSize:12.5}}>
                                {t('calendar.yearVisibleSummary', {
                                    year: displayYear,
                                    holidays: selectedYearHolidays.length,
                                    shortDays: selectedYearShortDays.length,
                                })}
                            </p>
                        </div>
                        <div className="seg">
                            <button
                                type="button"
                                onClick={() => setViewMode('calendar')}
                                aria-pressed={viewMode === 'calendar'}
                            >
                                <Grid className="h-4 w-4" />
                                {t('calendar.calendarView')}
                            </button>
                            <button
                                type="button"
                                onClick={() => setViewMode('list')}
                                aria-pressed={viewMode === 'list'}
                            >
                                <List className="h-4 w-4" />
                                {t('calendar.listView')}
                            </button>
                        </div>
                    </div>

                    <div className="wc-toolbar" style={{marginBottom:16}}>
                        <label className="field" style={{minWidth:150}}>
                            <span className="field-lbl">{t('calendar.country')}</span>
                            <select
                                value={publicCountry}
                                onChange={event => setPublicCountry(event.target.value)}
                                className="input"
                                aria-label={t('calendar.country')}
                            >
                                <option value="US">{t('calendar.countryUS')}</option>
                                <option value="ES">{t('calendar.countryES')}</option>
                                <option value="RU">{t('calendar.countryRU')}</option>
                            </select>
                        </label>
                        <Button
                            type="button"
                            variant="secondary"
                            onClick={() => publicImportMutation.mutate({
                                calendarId: calendar.id,
                                country: publicCountry,
                                year: displayYear,
                            })}
                            isLoading={publicImportMutation.isPending}
                        >
                            <Download className="w-4 h-4" />
                            {t('calendar.loadPublicHolidays')}
                        </Button>
                        <label className="btn secondary cursor-pointer">
                            <Upload className="w-4 h-4" />
                            {t('calendar.importHolidayCsv')}
                            <input
                                type="file"
                                accept=".csv,text/csv"
                                className="hidden"
                                onChange={event => {
                                    handleHolidayCsvFile(event.target.files?.[0] || null);
                                    event.currentTarget.value = '';
                                }}
                            />
                        </label>
                    </div>

                    <div className="field" style={{marginBottom:16}}>
                        <span className="field-lbl">{t('calendar.weekendDays')}</span>
                        <div className="row wrap">
                            {weekdayNames.map((day, index) => (
                                <button
                                    key={day}
                                    type="button"
                                    onClick={() => toggleWeekend(index)}
                                    className={`pill ${draft.weekend_days.includes(index) ? 'accent' : 'opt'}`}
                                >
                                    {day}
                                </button>
                            ))}
                        </div>
                    </div>

                    {viewMode === 'calendar' ? (
                        <InteractiveCalendar
                            year={displayYear}
                            month={visibleMonth}
                            holidays={draft.holidays}
                            shortDays={draft.short_days}
                            weekendDays={draft.weekend_days}
                            onYearChange={setDraftYear}
                            onMonthChange={setCalendarMonth}
                            onAddHoliday={addCompanyDay}
                            onRemoveHoliday={removeCompanyDay}
                            onAddShortDay={addShortDay}
                            onRemoveShortDay={removeShortDay}
                            onToggleWeekend={toggleWeekend}
                        />
                    ) : (
                        <div className="calendar-list-surface">
                            <CalendarPeriodNavigator
                                year={displayYear}
                                month={visibleMonth}
                                holidays={draft.holidays}
                                weekendDays={draft.weekend_days}
                                onYearChange={setDraftYear}
                                onMonthChange={setCalendarMonth}
                            />
                            <DateList
                                holidays={selectedYearHolidays}
                                shortDays={selectedYearShortDays}
                                locale={locale}
                                onRemoveHoliday={removeCompanyDay}
                                onRemoveShortDay={removeShortDay}
                            />
                        </div>
                    )}
                </div>

                <div className="wc-panel-stack">
                    <section className="card card-pad">
                        <h2 className="row" style={{margin:0, fontSize:14, fontWeight:600}}>
                            <Plus className="h-4 w-4 text-action" />
                            {t('calendar.manualCompanyDays')}
                        </h2>
                        <div className="wc-form-grid" style={{marginTop:12}}>
                            <Input
                                type="date"
                                label={t('calendar.date')}
                                value={manualDate}
                                onChange={event => setManualDate(event.target.value)}
                            />
                            <Button
                                type="button"
                                onClick={addManualDate}
                                disabled={!manualDate}
                            >
                                {t('calendar.addDay')}
                            </Button>
                            <Input
                                type="date"
                                label={t('calendar.startDate')}
                                value={rangeStart}
                                onChange={event => setRangeStart(event.target.value)}
                            />
                            <Input
                                type="date"
                                label={t('calendar.endDate')}
                                value={rangeEnd}
                                min={rangeStart}
                                onChange={event => setRangeEnd(event.target.value)}
                            />
                            <Button
                                type="button"
                                variant="secondary"
                                onClick={addManualRange}
                                disabled={!rangeStart || !rangeEnd || rangeStart > rangeEnd}
                            >
                                <CalendarRange className="w-4 h-4" />
                                {t('calendar.addRange')}
                            </Button>
                        </div>
                    </section>

                    <section className="card card-pad">
                        <h2 style={{margin:0, fontSize:14, fontWeight:600}}>{t('calendar.shortDayOverrides')}</h2>
                        <div className="wc-panel-stack" style={{marginTop:12, maxHeight:192, overflowY:'auto'}}>
                            {selectedYearShortDays.map(day => (
                                <DateChip
                                    key={day}
                                    dateKey={day}
                                    locale={locale}
                                    iconTone="amber"
                                    label={t('calendar.shortDay')}
                                    onRemove={() => removeShortDay(day)}
                                />
                            ))}
                            {selectedYearShortDays.length === 0 && (
                                <div className="empty" style={{padding:16}}>
                                    {t('calendar.noShortDays')}
                                </div>
                            )}
                        </div>
                    </section>
                </div>
            </section>

            <section className="card card-pad">
                <div className="between wrap" style={{marginBottom:16}}>
                    <div>
                        <h2 className="row" style={{margin:0, fontSize:16, fontWeight:600}}>
                            <Plane className="h-5 w-5 text-feedback-purple" />
                            {t('calendar.teamVacationWorkspace')}
                        </h2>
                        <p className="muted" style={{margin:0, fontSize:12.5}}>
                            {selectedIteration ? selectedIteration.name : t('calendar.noIterationSelected')}
                        </p>
                    </div>
                    {iterations.length > 0 && (
                        <select
                            value={selectedIterationId}
                            onChange={event => setSelectedIterationId(Number.parseInt(event.target.value, 10))}
                            className="input"
                            style={{ width: 'auto' }}
                            aria-label={t('calendar.iteration')}
                        >
                            {iterations.map(iteration => (
                                <option key={iteration.id} value={iteration.id}>{iteration.name}</option>
                            ))}
                        </select>
                    )}
                </div>

                {isLoadingIterations ? (
                    <div className="banner">{t('common.loading')}</div>
                ) : iterations.length === 0 ? (
                    <div className="empty">
                        <h4>{t('calendar.noIterationsTitle')}</h4>
                        <p>{t('calendar.noIterationsBody')}</p>
                        <div className="empty-actions">
                            <Link to="/iterations" className="btn primary">{t('tasks.goToIterations')}</Link>
                        </div>
                    </div>
                ) : isLoadingTeam ? (
                    <div className="banner">{t('teamCapacity.loading')}</div>
                ) : teamMembers.length === 0 ? (
                    <div className="empty">
                        <h4>{t('calendar.noTeamTitle')}</h4>
                        <p>{t('calendar.noTeamBody')}</p>
                        <div className="empty-actions">
                            <Link to="/team" className="btn primary">{t('nav.team')}</Link>
                        </div>
                    </div>
                ) : (
                    <div className="wc-content-rail">
                        <div>
                            {(vacationSummary || vacationError) && (
                                <div className={`banner ${vacationError ? 'warn' : 'done'}`} style={{marginBottom:12}}>
                                    {vacationSummary}
                                    {vacationError && <div>{vacationError}</div>}
                                </div>
                            )}
                            <div className="wc-toolbar">
                                <label className="field" style={{minWidth:220}}>
                                    <span className="field-lbl">{t('calendar.teamMember')}</span>
                                    <select
                                        value={selectedMemberId}
                                        onChange={event => setSelectedMemberId(event.target.value)}
                                        className="input"
                                    >
                                        {teamMembers.map(member => (
                                            <option key={member.id} value={member.id}>
                                                {member.name}{member.email ? ` · ${member.email}` : ''}
                                            </option>
                                        ))}
                                    </select>
                                </label>
                                <Input
                                    type="date"
                                    label={t('teamVacations.startDate')}
                                    value={vacationStart}
                                    onChange={event => setVacationStart(event.target.value)}
                                />
                                <Input
                                    type="date"
                                    label={t('teamVacations.endDate')}
                                    value={vacationEnd}
                                    min={vacationStart}
                                    onChange={event => setVacationEnd(event.target.value)}
                                />
                                <Button
                                    type="button"
                                    onClick={addVacation}
                                    disabled={!selectedMemberId || !vacationStart || !vacationEnd || vacationStart > vacationEnd}
                                    isLoading={addVacationMutation.isPending}
                                >
                                    <Plus className="w-4 h-4" />
                                    {t('teamVacations.addVacation')}
                                </Button>
                                <label className="btn secondary cursor-pointer">
                                    <Upload className="w-4 h-4" />
                                    {t('calendar.importVacationCsv')}
                                    <input
                                        type="file"
                                        accept=".csv,text/csv"
                                        className="hidden"
                                        onChange={event => {
                                            handleVacationCsvFile(event.target.files?.[0] || null);
                                            event.currentTarget.value = '';
                                        }}
                                    />
                                </label>
                            </div>
                        </div>
                        <div>
                            <h3 style={{margin:'0 0 12px', fontSize:13, fontWeight:600}}>
                                {t('calendar.currentTeamVacations', { count: vacationRows.length })}
                            </h3>
                            <div className="wc-panel-stack" style={{maxHeight:320, overflowY:'auto'}}>
                                {vacationRows.map(({ member, vacation }) => (
                                    <div key={vacation.id} className="data-row" style={{gridTemplateColumns:'1fr auto'}}>
                                        <div>
                                            <div className="dr-title">{member.name}</div>
                                            <div className="dr-sub">
                                                {formatDate(vacation.start_date, locale)}
                                                {' → '}
                                                {formatDate(vacation.end_date, locale)}
                                            </div>
                                        </div>
                                        <Button
                                            type="button"
                                            variant="ghost"
                                            size="sm"
                                            onClick={() => requestConfirmation({
                                                title: t('actions.delete'),
                                                description: t('teamVacations.deleteConfirm'),
                                                confirmLabel: t('actions.delete'),
                                                cancelLabel: t('actions.cancel'),
                                                closeLabel: t('actions.close'),
                                                onConfirm: () => deleteVacationMutation.mutateAsync(vacation.id),
                                                tone: 'danger',
                                            })}
                                            aria-label={t('actions.delete')}
                                            isLoading={deleteVacationMutation.isPending}
                                            className="text-feedback-danger hover:text-feedback-danger-foreground"
                                        >
                                            <Trash2 className="w-4 h-4" />
                                        </Button>
                                    </div>
                                ))}
                                {vacationRows.length === 0 && (
                                    <div className="empty" style={{padding:24}}>
                                        {t('teamVacations.empty')}
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>
                )}
            </section>
            {confirmationDialog}
        </PlanningWorkbenchFrame>
    );
};

interface DateListProps {
    holidays: string[];
    shortDays: string[];
    locale: Locale;
    onRemoveHoliday: (dateKey: string) => void;
    onRemoveShortDay: (dateKey: string) => void;
}

const DateList = ({
    holidays,
    shortDays,
    locale,
    onRemoveHoliday,
    onRemoveShortDay,
}: DateListProps) => {
    const { t } = useTranslation();

    return (
        <div className="grid gap-4 md:grid-cols-2">
            <div>
                <h3 className="mb-3 mt-0 text-sm font-medium text-content-primary">{t('calendar.companyDays')}</h3>
                <div className="max-h-72 space-y-2 overflow-y-auto">
                    {holidays.map(day => (
                        <DateChip
                            key={day}
                            dateKey={day}
                            locale={locale}
                            iconTone="red"
                            label={t('calendar.companyDay')}
                            onRemove={() => onRemoveHoliday(day)}
                        />
                    ))}
                    {holidays.length === 0 && (
                        <div className="rounded-lg border border-dashed bg-surface-muted p-6 text-center text-sm text-content-tertiary">
                            {t('calendar.noCompanyDays')}
                        </div>
                    )}
                </div>
            </div>
            <div>
                <h3 className="mb-3 mt-0 text-sm font-medium text-content-primary">{t('calendar.shortDays')}</h3>
                <div className="max-h-72 space-y-2 overflow-y-auto">
                    {shortDays.map(day => (
                        <DateChip
                            key={day}
                            dateKey={day}
                            locale={locale}
                            iconTone="amber"
                            label={t('calendar.shortDay')}
                            onRemove={() => onRemoveShortDay(day)}
                        />
                    ))}
                    {shortDays.length === 0 && (
                        <div className="rounded-lg border border-dashed bg-surface-muted p-6 text-center text-sm text-content-tertiary">
                            {t('calendar.noShortDays')}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

interface DateChipProps {
    dateKey: string;
    locale: Locale;
    iconTone: 'red' | 'amber';
    label: string;
    onRemove: () => void;
}

const DateChip = ({ dateKey, locale, iconTone, label, onRemove }: DateChipProps) => (
    <div className="flex items-center justify-between rounded-lg border bg-surface-card p-2 text-sm text-content-primary">
        <span>
            <span className={`mr-2 inline-flex h-2.5 w-2.5 rounded-full ${iconTone === 'red' ? 'bg-feedback-danger' : 'bg-feedback-warning'}`} />
            {formatDate(dateKey, locale)}
            <span className="ml-2 text-xs text-content-tertiary">{label}</span>
        </span>
        <button
            type="button"
            onClick={onRemove}
            className="rounded p-1 text-feedback-danger hover:bg-feedback-danger-muted hover:text-feedback-danger-foreground"
            aria-label={label}
        >
            <X className="h-4 w-4" />
        </button>
    </div>
);

export default CalendarPage;

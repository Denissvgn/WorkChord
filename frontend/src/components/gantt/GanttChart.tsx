/* eslint-disable jsx-a11y/no-noninteractive-element-interactions, jsx-a11y/no-noninteractive-tabindex -- The native scroll region is focusable for keyboard scrolling and supports optional pointer panning. */
import { useState, useMemo, useRef, useEffect, useCallback, useId } from 'react';
import { useVirtualizer } from '@tanstack/react-virtual';
import { eachDayOfInterval, format, isSameDay, addDays, differenceInCalendarDays, parseISO, startOfDay } from 'date-fns';
import { RefreshCw, ChevronRight, ChevronDown, ZoomIn, ZoomOut, Minimize2, Maximize2, Calendar, CalendarOff, ListFilter, Eye } from 'lucide-react';
import { Link } from 'react-router-dom';
import { Button } from '../common/Button';
import { Checkbox } from '../common/Checkbox';
import { TaskEditModal } from './TaskEditModal';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { ganttService } from '../../services/ganttService';
import clsx from 'clsx';
import type { GanttTask, SchedulePreviewResponse } from '../../types/gantt';
import { STATUS_TONE, toneSolidClassName } from '../ui/tone';
import { QueryErrorState, QueryLoadingState } from '../feedback/QueryState';
import { useToast } from '../feedback/toast';
import { dateFnsLocale } from '../../i18n/dateLocale';
import { formatDate } from '../../utils/formatDate';
import { useTranslation } from 'react-i18next';
import { OverflowMenu, SlideOverDrawer } from '../ui';

interface GanttChartProps {
    iterationId: number;
    startDate: string;
    endDate: string;
    tasks: GanttTask[];
    weekends: string[];
    holidays: string[];
    memberVacations: Record<number, string[]>;
    sandboxMode?: boolean;
    onSaveSandbox?: (taskId: number, updatedData: Partial<GanttTask>) => void;
}

interface FlattenedTask extends GanttTask {
    depth: number;
}

interface TaskTimelineDates {
    start: string | null;
    end: string | null;
}

const getTaskTimelineDates = (task: GanttTask): TaskTimelineDates => ({
    start: task.schedule_result?.scheduled_start ?? task.start_date,
    end: task.schedule_result?.scheduled_end ?? task.end_date,
});

const hasCompleteTimelineDates = (
    dates: TaskTimelineDates,
): dates is { start: string; end: string } => Boolean(dates.start && dates.end);

export const GanttChart = ({
    iterationId,
    startDate,
    endDate,
    tasks,
    weekends,
    holidays,
    memberVacations,
    sandboxMode = false,
    onSaveSandbox,
}: GanttChartProps) => {
    const { t, i18n: activeI18n } = useTranslation();
    const toast = useToast();
    const queryClient = useQueryClient();
    const [expandedTasks, setExpandedTasks] = useState<Set<number>>(new Set());
    const initialExpansionDone = useRef(false);
    const scrollContainerRef = useRef<HTMLDivElement>(null);
    const chartInstructionsId = useId();
    const [schedulePreview, setSchedulePreview] = useState<SchedulePreviewResponse | null>(null);
    const [isRefreshingSavedSchedule, setIsRefreshingSavedSchedule] = useState(false);
    const sourceTasks = schedulePreview?.tasks ?? tasks;
    const focusChart = useCallback(() => {
        window.requestAnimationFrame(() => scrollContainerRef.current?.focus());
    }, []);

    // A preview becomes stale as soon as its source changes, and it must never
    // be mixed with an active edit sandbox (which has its own preview contract).
    useEffect(() => {
        setSchedulePreview(null);
        setEditingTask(null);
    }, [iterationId, tasks, sandboxMode]);

    useEffect(() => {
        initialExpansionDone.current = false;
    }, [iterationId]);

    // Initial expansion logic
    useEffect(() => {
        if (sourceTasks.length > 0 && !initialExpansionDone.current) {
            const allIds = new Set<number>();
            const traverse = (t: GanttTask) => {
                if (t.children?.length) {
                    allIds.add(t.id);
                    t.children.forEach(traverse);
                }
            };
            sourceTasks.forEach(traverse);
            setExpandedTasks(allIds);
            initialExpansionDone.current = true;
        }
    }, [sourceTasks]);

    const [selectedAssigneeId, setSelectedAssigneeId] = useState<number | null>(null);
    const [hideUnassigned, setHideUnassigned] = useState(false);
    const [zoomLevel, setZoomLevel] = useState(40); // Width of day column
    const [isCompressed, setIsCompressed] = useState(false);
    const [isSortedByDate, setIsSortedByDate] = useState(false);
    const [editingTask, setEditingTask] = useState<GanttTask | null>(null);
    const [isFiltersOpen, setIsFiltersOpen] = useState(false);
    const activeFilterCount = Number(selectedAssigneeId !== null) + Number(hideUnassigned);
    const clearFilters = () => {
        setSelectedAssigneeId(null);
        setHideUnassigned(false);
    };

    // --- Data Preparation ---

    const sortedTasks = useMemo(() => {
        if (!isSortedByDate) return sourceTasks;

        const getTaskStart = (t: GanttTask) => t.schedule_result?.scheduled_start || t.start_date || '9999-12-31';

        const sortRecursive = (list: GanttTask[]): GanttTask[] => {
            return [...list].sort((a, b) => {
                return getTaskStart(a).localeCompare(getTaskStart(b));
            }).map(t => ({
                ...t,
                children: t.children ? sortRecursive(t.children) : []
            }));
        };

        return sortRecursive(sourceTasks);
    }, [sourceTasks, isSortedByDate]);

    const uniqueAssignees = useMemo(() => {
        const assigneeMap = new Map<number, { id: number; name: string }>();
        const collectAssignees = (taskList: GanttTask[]) => {
            taskList.forEach(t => {
                if (t.assignee) assigneeMap.set(t.assignee.id, t.assignee);
                if (t.children) collectAssignees(t.children);
            });
        };
        collectAssignees(sourceTasks);
        const collator = new Intl.Collator(activeI18n.language);
        return Array.from(assigneeMap.values()).sort((a, b) => collator.compare(a.name, b.name));
    }, [activeI18n.language, sourceTasks]);

    useEffect(() => {
        if (
            selectedAssigneeId !== null
            && !uniqueAssignees.some(assignee => assignee.id === selectedAssigneeId)
        ) {
            setSelectedAssigneeId(null);
        }
    }, [selectedAssigneeId, uniqueAssignees]);

    const isWeekendDay = useCallback((date: Date) => {
        const dateStr = format(date, 'yyyy-MM-dd');
        if (weekends.includes(dateStr)) return true;
        const dayOfWeek = date.getDay();
        return dayOfWeek === 0 || dayOfWeek === 6;
    }, [weekends]);

    const isHolidayDay = useCallback((date: Date) => {
        return holidays.includes(format(date, 'yyyy-MM-dd'));
    }, [holidays]);

    const isVacationDay = useCallback((date: Date, memberId: number | undefined) => {
        if (!memberId) return false;
        const vacationDates = memberVacations[memberId];
        return vacationDates?.includes(format(date, 'yyyy-MM-dd'));
    }, [memberVacations]);

    const days = useMemo(() => {
        const start = new Date(startDate);
        const iterationEnd = new Date(endDate);
        let end = addDays(iterationEnd, 7);

        const findMaxEndDate = (taskList: GanttTask[]): Date => {
            let maxDate = iterationEnd;
            taskList.forEach(task => {
                if (task.end_date) {
                    const taskEnd = new Date(task.end_date);
                    if (taskEnd > maxDate) maxDate = taskEnd;
                }
                if (task.children) {
                    const childMax = findMaxEndDate(task.children);
                    if (childMax > maxDate) maxDate = childMax;
                }
            });
            return maxDate;
        };

        const maxTaskEnd = findMaxEndDate(sourceTasks);
        if (maxTaskEnd > iterationEnd) {
            const overdueEnd = addDays(maxTaskEnd, 2);
            if (overdueEnd > end) end = overdueEnd;
        }

        return eachDayOfInterval({ start, end });
    }, [startDate, endDate, sourceTasks]);

    const visibleDays = useMemo(() => {
        if (!isCompressed) return days;

        const leafTaskRanges: { start: Date; end: Date }[] = [];
        const collectLeafRanges = (taskList: GanttTask[]) => {
            taskList.forEach(task => {
                if (!task.children || task.children.length === 0) {
                    const taskDates = getTaskTimelineDates(task);
                    if (!hasCompleteTimelineDates(taskDates)) return;
                    const taskStart = new Date(taskDates.start);
                    const taskEnd = new Date(taskDates.end);
                    leafTaskRanges.push({ start: taskStart, end: taskEnd });
                } else {
                    collectLeafRanges(task.children);
                }
            });
        };
        collectLeafRanges(sourceTasks);

        return days.filter(day => {
            const overlappingTasks = leafTaskRanges.filter(range => day >= range.start && day <= range.end);
            if (overlappingTasks.length === 0) return true;

            for (const taskRange of overlappingTasks) {
                const taskDuration = differenceInCalendarDays(taskRange.end, taskRange.start) + 1;
                if (taskDuration <= 8) return true;
                const daysSinceStart = differenceInCalendarDays(day, taskRange.start);
                const daysUntilEnd = differenceInCalendarDays(taskRange.end, day);
                if (daysSinceStart < 3 || daysUntilEnd < 3) return true;
            }
            return false;
        });
    }, [days, isCompressed, sourceTasks]);

    // O(1) index lookup
    const visibleDaysIndexMap = useMemo(() => {
        const map = new Map<string, number>();
        visibleDays.forEach((day, idx) => {
            map.set(format(day, 'yyyy-MM-dd'), idx);
        });
        return map;
    }, [visibleDays]);

    const monthGroups = useMemo(() => {
        const groups: { month: string; count: number; startIndex: number }[] = [];
        let currentMonth = '';
        let currentCount = 0;
        let startIndex = 0;

        visibleDays.forEach((day, idx) => {
            const monthKey = format(day, 'MMM yyyy', { locale: dateFnsLocale(activeI18n.language) });
            if (monthKey !== currentMonth) {
                if (currentMonth) {
                    groups.push({ month: currentMonth, count: currentCount, startIndex });
                }
                currentMonth = monthKey;
                currentCount = 1;
                startIndex = idx;
            } else {
                currentCount++;
            }
        });
        if (currentMonth) {
            groups.push({ month: currentMonth, count: currentCount, startIndex });
        }
        return groups;
    }, [activeI18n.language, visibleDays]);

    // Flattening tasks
    const taskMatchesFilter = useCallback((task: GanttTask, assigneeId: number | null, hideUnassignedTasks: boolean): boolean => {
        let matches = true;
        if (assigneeId) matches = task.assignee?.id === assigneeId;
        if (hideUnassignedTasks && !task.assignee) matches = false;
        if (matches) return true;
        if (task.children) return task.children.some(child => taskMatchesFilter(child, assigneeId, hideUnassignedTasks));
        return false;
    }, []);

    const displayTasks = useMemo(() => {
        const flattened: FlattenedTask[] = [];
        const processTask = (task: GanttTask, depth: number) => {
            if (!taskMatchesFilter(task, selectedAssigneeId, hideUnassigned)) return;
            flattened.push({ ...task, depth });
            if (
                task.children
                && task.children.length > 0
                && (activeFilterCount > 0 || expandedTasks.has(task.id))
            ) {
                task.children.forEach(child => processTask(child, depth + 1));
            }
        };
        sortedTasks.forEach(task => processTask(task, 0));
        return flattened;
    }, [activeFilterCount, sortedTasks, expandedTasks, selectedAssigneeId, hideUnassigned, taskMatchesFilter]);

    const currentTaskDatesById = useMemo(() => {
        const datesById = new Map<number, TaskTimelineDates>();
        const collectDates = (taskList: GanttTask[]) => {
            taskList.forEach(task => {
                datesById.set(task.id, getTaskTimelineDates(task));
                collectDates(task.children ?? []);
            });
        };
        collectDates(tasks);
        return datesById;
    }, [tasks]);

    const previewChangedTaskIds = useMemo(() => {
        if (!schedulePreview) return new Set<number>();

        const changed = new Set<number>();
        const collectChangedTasks = (taskList: GanttTask[]) => {
            taskList.forEach(task => {
                const current = currentTaskDatesById.get(task.id);
                const projected = getTaskTimelineDates(task);
                if (current && (current.start !== projected.start || current.end !== projected.end)) {
                    changed.add(task.id);
                }
                collectChangedTasks(task.children ?? []);
            });
        };

        collectChangedTasks(schedulePreview.tasks);
        return changed;
    }, [currentTaskDatesById, schedulePreview]);

    const expandableTaskIds = useMemo(() => {
        const ids = new Set<number>();
        const collectIds = (taskList: GanttTask[]) => {
            taskList.forEach(task => {
                if (task.children?.length) {
                    ids.add(task.id);
                    collectIds(task.children);
                }
            });
        };
        collectIds(sourceTasks);
        return ids;
    }, [sourceTasks]);
    const allTaskGroupsExpanded = expandableTaskIds.size > 0
        && [...expandableTaskIds].every(taskId => expandedTasks.has(taskId));


    // --- Virtualization ---
    // Column Virtualizer
    const columnVirtualizer = useVirtualizer({
        horizontal: true,
        count: visibleDays.length,
        getScrollElement: () => scrollContainerRef.current,
        estimateSize: () => zoomLevel,
        overscan: 10,
    });

    // Row Virtualizer
    const ROW_HEIGHT = 50;
    const rowVirtualizer = useVirtualizer({
        count: displayTasks.length,
        getScrollElement: () => scrollContainerRef.current,
        estimateSize: () => ROW_HEIGHT,
        overscan: 10,
    });

    const toggleExpand = (taskId: number) => {
        setExpandedTasks(prev => {
            const next = new Set(prev);
            if (next.has(taskId)) next.delete(taskId);
            else next.add(taskId);
            return next;
        });
    };

    // feedback-policy: mutation pending,inline - preview is non-persistent and exposes inline retry.
    const schedulePreviewMutation = useMutation({
        mutationFn: () => ganttService.previewSchedule(iterationId, []),
        onSuccess: preview => {
            setEditingTask(null);
            setSchedulePreview(preview);
        },
    });

    // feedback-policy: mutation pending,inline - Apply is disabled while pending and failures retain the preview for retry.
    const scheduleMutation = useMutation({
        mutationFn: () => ganttService.schedule(iterationId),
        onSuccess: async () => {
            setSchedulePreview(null);
            await Promise.all([
                queryClient.invalidateQueries({ queryKey: ['gantt', iterationId] }),
                queryClient.invalidateQueries({ queryKey: ['tasks', iterationId] }),
            ]);
            toast.success(t('gantt.scheduleApplied'));
            focusChart();
        },
    });

    const beginSchedulePreview = () => {
        if (
            sandboxMode
            || schedulePreview
            || schedulePreviewMutation.isPending
            || scheduleMutation.isPending
            || isRefreshingSavedSchedule
        ) return;
        scheduleMutation.reset();
        schedulePreviewMutation.mutate();
    };

    const applySchedulePreview = () => {
        if (!schedulePreview || scheduleMutation.isPending) return;
        scheduleMutation.mutate();
    };

    const returnToSavedSchedule = () => {
        scheduleMutation.reset();
        setSchedulePreview(null);
        focusChart();
    };

    const refreshSavedSchedule = async () => {
        if (isRefreshingSavedSchedule) return;
        setIsRefreshingSavedSchedule(true);
        setSchedulePreview(null);
        scheduleMutation.reset();
        try {
            await Promise.all([
                queryClient.refetchQueries({ queryKey: ['gantt', iterationId], type: 'active' }),
                queryClient.refetchQueries({ queryKey: ['tasks', iterationId], type: 'active' }),
            ]);
        } finally {
            setIsRefreshingSavedSchedule(false);
            focusChart();
        }
    };

    const getTaskBaseColorClass = (task: GanttTask) => {
        return toneSolidClassName[STATUS_TONE[task.status]];
    };

    const formatTaskTimelineDates = (dates: { start: string; end: string }) => ({
        start: formatDate(dates.start, activeI18n.language),
        end: formatDate(dates.end, activeI18n.language),
    });

    const getTaskTooltip = (task: GanttTask) => {
        const dates = getTaskTimelineDates(task);
        if (!hasCompleteTimelineDates(dates)) {
            return t('gantt.taskDatesUnavailable', { title: task.title });
        }
        return t('gantt.taskDateRange', {
            title: task.title,
            ...formatTaskTimelineDates(dates),
        });
    };

    const getTaskAccessibleLabel = (task: GanttTask) => {
        const dates = getTaskTimelineDates(task);
        if (!hasCompleteTimelineDates(dates)) {
            return t('gantt.openUnscheduledTask', { title: task.title });
        }
        return t('gantt.openScheduledTask', {
            title: task.title,
            assignee: task.assignee?.name ?? t('common.unassigned'),
            priority: task.priority,
            ...formatTaskTimelineDates(dates),
        });
    };

    const getUnscheduledTaskGuidance = (task: GanttTask) => (
        task.assignee
            ? t('gantt.reviewTaskToSchedule')
            : t('gantt.assignTaskToSchedule')
    );

    const getUnscheduledTaskDescription = (task: GanttTask) => t(
        'gantt.unscheduledTaskDescription',
        {
            title: task.title,
            guidance: getUnscheduledTaskGuidance(task),
        },
    );

    const getPreviewTaskDescription = (task: GanttTask) => {
        const projectedDates = getTaskTimelineDates(task);
        const currentDates = currentTaskDatesById.get(task.id);

        if (!hasCompleteTimelineDates(projectedDates)) {
            return t('gantt.schedulePreviewTaskUnscheduled', { title: task.title });
        }

        const projected = formatTaskTimelineDates(projectedDates);
        if (!currentDates || !hasCompleteTimelineDates(currentDates)) {
            return t('gantt.schedulePreviewTaskNewDates', {
                title: task.title,
                ...projected,
            });
        }

        const current = formatTaskTimelineDates(currentDates);
        if (previewChangedTaskIds.has(task.id)) {
            return t('gantt.schedulePreviewTaskMoved', {
                title: task.title,
                currentStart: current.start,
                currentEnd: current.end,
                projectedStart: projected.start,
                projectedEnd: projected.end,
            });
        }

        return t('gantt.schedulePreviewTaskUnchanged', {
            title: task.title,
            ...projected,
        });
    };

    const getCalendarDayLabel = (day: Date) => {
        const date = format(day, 'PPPP', { locale: dateFnsLocale(activeI18n.language) });
        if (isHolidayDay(day)) return t('gantt.calendarDayHoliday', { date });
        if (isSameDay(day, new Date())) return t('gantt.calendarDayToday', { date });
        if (isWeekendDay(day)) return t('gantt.calendarDayWeekend', { date });
        return date;
    };

    // --- Helpers for Absolute Positioning ---

    const getTaskPosition = (task: GanttTask) => {
        const startDateStr = task.schedule_result?.scheduled_start || task.start_date || startDate;
        const taskStart = typeof startDateStr === 'string' ? parseISO(startDateStr) : startDateStr;

        const endDateStr = task.schedule_result?.scheduled_end || task.end_date;
        const taskEnd = endDateStr
            ? (typeof endDateStr === 'string' ? parseISO(endDateStr) : endDateStr)
            : addDays(taskStart, task.calculated_effort_days || task.effort_days || 1);

        const startKey = format(taskStart, 'yyyy-MM-dd');
        let startIndex = visibleDaysIndexMap.get(startKey) ?? -1;

        if (startIndex === -1) {
            startIndex = visibleDays.findIndex(day => startOfDay(day) >= startOfDay(taskStart));
            if (startIndex === -1) startIndex = 0;
        }

        const endKey = format(taskEnd, 'yyyy-MM-dd');
        let endIndex = visibleDaysIndexMap.get(endKey) ?? -1;
        if (endIndex === -1) endIndex = visibleDays.length - 1;

        const span = Math.max(1, endIndex - startIndex + 1);

        return {
            left: startIndex * zoomLevel,
            width: span * zoomLevel
        };
    };

    // Pre-calculate user vacation ranges for a specific row to minimize DOM nodes
    const getCollapsedVacationRanges = (memberId: number | undefined) => {
        if (!memberId) return [];
        const ranges: { left: number; width: number }[] = [];
        let currentStart = -1;
        let currentLength = 0;

        visibleDays.forEach((day, idx) => {
            const isVac = isVacationDay(day, memberId);
            if (isVac) {
                if (currentStart === -1) {
                    currentStart = idx;
                    currentLength = 1;
                } else {
                    currentLength++;
                }
            } else {
                if (currentStart !== -1) {
                    ranges.push({ left: currentStart * zoomLevel, width: currentLength * zoomLevel });
                    currentStart = -1;
                    currentLength = 0;
                }
            }
        });
        if (currentStart !== -1) {
            ranges.push({ left: currentStart * zoomLevel, width: currentLength * zoomLevel });
        }
        return ranges;
    };

    // Drag to scroll logic
    const [isDragging, setIsDragging] = useState(false);
    const [startX, setStartX] = useState(0);
    const [startY, setStartY] = useState(0);
    const [scrollLeft, setScrollLeft] = useState(0);
    const [scrollTop, setScrollTop] = useState(0);

    const onMouseDown = (e: React.MouseEvent) => {
        if (!scrollContainerRef.current) return;
        if ((e.target as HTMLElement).closest('button, a, input, select, label')) return;
        setIsDragging(true);
        setStartX(e.pageX - scrollContainerRef.current.offsetLeft);
        setStartY(e.pageY - scrollContainerRef.current.offsetTop);
        setScrollLeft(scrollContainerRef.current.scrollLeft);
        setScrollTop(scrollContainerRef.current.scrollTop);
        document.body.style.userSelect = 'none';
        document.body.style.cursor = 'grabbing';
    };

    const stopDragging = () => {
        setIsDragging(false);
        document.body.style.userSelect = '';
        document.body.style.cursor = '';
    };

    const onMouseMove = (e: React.MouseEvent) => {
        if (!isDragging || !scrollContainerRef.current) return;
        e.preventDefault();
        const x = e.pageX - scrollContainerRef.current.offsetLeft;
        const y = e.pageY - scrollContainerRef.current.offsetTop;
        const walkX = (x - startX) * 1.5;
        const walkY = (y - startY) * 1.5;
        scrollContainerRef.current.scrollLeft = scrollLeft - walkX;
        scrollContainerRef.current.scrollTop = scrollTop - walkY;
    };

    const SIDEBAR_WIDTH = 300;
    const isFilteredEmpty = sourceTasks.length > 0
        && activeFilterCount > 0
        && displayTasks.length === 0;

    return (
        <div className="flex h-full min-h-0 flex-col overflow-hidden rounded-lg bg-surface-card shadow">
            {/* Toolbar */}
            <div className="z-10 flex shrink-0 justify-end border-b border-border bg-surface-card p-3 sm:p-4">
                <div className="flex min-w-0 flex-wrap items-center gap-2">
                    <Button
                        variant={activeFilterCount > 0 ? 'secondary' : 'outline'}
                        size="sm"
                        onClick={() => setIsFiltersOpen(true)}
                        aria-expanded={isFiltersOpen}
                        aria-label={activeFilterCount > 0
                            ? t('surfaces.ganttChart.openFiltersWithCount', { count: activeFilterCount })
                            : t('taskFilters.filters')}
                    >
                        <ListFilter className="mr-2 h-4 w-4" />
                        {t('taskFilters.filters')}
                        {activeFilterCount > 0 && (
                            <span
                                aria-hidden="true"
                                className="ml-1 rounded-full bg-surface-card/80 px-1.5 py-0.5 text-xs tabular-nums"
                            >
                                {activeFilterCount}
                            </span>
                        )}
                    </Button>
                    <OverflowMenu
                        label={t('surfaces.ganttChart.chartActions')}
                        items={[
                            ...(!sandboxMode && !schedulePreview ? [{
                                label: schedulePreviewMutation.isPending
                                    ? t('surfaces.ganttChart.generatingSchedulePreview')
                                    : t('surfaces.ganttChart.previewSchedule'),
                                icon: <RefreshCw className="h-4 w-4" aria-hidden="true" />,
                                onSelect: beginSchedulePreview,
                                disabled: schedulePreviewMutation.isPending
                                    || scheduleMutation.isPending
                                    || isRefreshingSavedSchedule,
                            }] : []),
                            {
                                label: t(isSortedByDate
                                    ? 'surfaces.ganttChart.restoreTaskOrder'
                                    : 'surfaces.ganttChart.sortByStartDate'),
                                icon: <Calendar className="h-4 w-4" aria-hidden="true" />,
                                onSelect: () => setIsSortedByDate(value => !value),
                            },
                            ...(expandableTaskIds.size > 0 && activeFilterCount === 0 ? [{
                                label: t(allTaskGroupsExpanded
                                    ? 'surfaces.ganttChart.collapseAllTaskGroups'
                                    : 'surfaces.ganttChart.expandAllTaskGroups'),
                                icon: allTaskGroupsExpanded
                                    ? <ChevronRight className="h-4 w-4" aria-hidden="true" />
                                    : <ChevronDown className="h-4 w-4" aria-hidden="true" />,
                                onSelect: () => setExpandedTasks(
                                    allTaskGroupsExpanded ? new Set() : new Set(expandableTaskIds),
                                ),
                            }] : []),
                            {
                                label: t('surfaces.ganttChart.zoomTimelineOut'),
                                icon: <ZoomOut className="h-4 w-4" aria-hidden="true" />,
                                onSelect: () => setZoomLevel(value => Math.max(20, value - 10)),
                                disabled: zoomLevel <= 20,
                            },
                            {
                                label: t('surfaces.ganttChart.zoomTimelineIn'),
                                icon: <ZoomIn className="h-4 w-4" aria-hidden="true" />,
                                onSelect: () => setZoomLevel(value => Math.min(100, value + 10)),
                                disabled: zoomLevel >= 100,
                            },
                            {
                                label: t(isCompressed
                                    ? 'surfaces.ganttChart.showEveryDate'
                                    : 'surfaces.ganttChart.condenseLongTaskSpans'),
                                icon: isCompressed
                                    ? <Maximize2 className="h-4 w-4" aria-hidden="true" />
                                    : <Minimize2 className="h-4 w-4" aria-hidden="true" />,
                                onSelect: () => setIsCompressed(value => !value),
                            },
                        ]}
                    />
                </div>
            </div>

            <SlideOverDrawer
                open={isFiltersOpen}
                title={t('taskFilters.filters')}
                subtitle={t('surfaces.ganttChart.filtersDescription')}
                icon={<ListFilter className="h-4 w-4" aria-hidden="true" />}
                onClose={() => setIsFiltersOpen(false)}
                footer={(
                    <Button
                        className="w-full"
                        type="button"
                        variant="secondary"
                        onClick={clearFilters}
                        disabled={activeFilterCount === 0}
                    >
                        {t('surfaces.ganttChart.clearFilters')}
                    </Button>
                )}
            >
                <div className="space-y-5 p-4">
                    <label className="block text-sm text-content-secondary">
                        <span className="mb-1 block text-xs font-medium uppercase tracking-wide">
                            {t('surfaces.ganttChart.assignee')}
                        </span>
                        <select
                            value={selectedAssigneeId ?? ''}
                            onChange={event => {
                                const nextAssigneeId = event.target.value ? parseInt(event.target.value) : null;
                                setSelectedAssigneeId(nextAssigneeId);
                                if (nextAssigneeId !== null) setHideUnassigned(false);
                            }}
                            className="w-full rounded-md border border-border-strong bg-surface-card px-3 py-2 text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-focus"
                        >
                            <option value="">{t('surfaces.ganttChart.allAssignees')}</option>
                            {uniqueAssignees.map(assignee => <option key={assignee.id} value={assignee.id}>{assignee.name}</option>)}
                        </select>
                    </label>
                    <Checkbox
                        checked={hideUnassigned}
                        onChange={setHideUnassigned}
                        label={t('surfaces.ganttChart.hideTasksWithoutAssignee')}
                    />
                </div>
            </SlideOverDrawer>

            {(schedulePreviewMutation.isPending || isRefreshingSavedSchedule) && (
                <QueryLoadingState
                    className="m-3 shrink-0 sm:m-4"
                    message={isRefreshingSavedSchedule
                        ? t('gantt.refreshingSavedSchedule')
                        : t('gantt.schedulePreviewPending')}
                />
            )}

            {schedulePreview && (
                <section
                    className="m-3 shrink-0 rounded-lg border border-action bg-action-muted/50 p-4 sm:m-4"
                    role="status"
                    aria-live="polite"
                >
                    <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                        <div className="flex min-w-0 items-start gap-3">
                            <div className="grid h-9 w-9 shrink-0 place-items-center rounded-md bg-surface-card text-action shadow-sm">
                                <Eye className="h-5 w-5" aria-hidden="true" />
                            </div>
                            <div className="min-w-0">
                                <h2 className="font-semibold text-content-primary">
                                    {t(scheduleMutation.isPending
                                        ? 'gantt.scheduleApplyPending'
                                        : 'gantt.schedulePreviewReady')}
                                </h2>
                                <p className="mt-1 text-sm text-content-secondary">
                                    {t(scheduleMutation.isPending
                                        ? 'gantt.scheduleApplyPendingBody'
                                        : 'gantt.schedulePreviewBody')}
                                </p>
                                {!scheduleMutation.isPending && (
                                    <div className="mt-2 flex flex-wrap gap-x-3 gap-y-1 text-xs text-content-secondary">
                                        {previewChangedTaskIds.size > 0 ? (
                                        <span>{t('gantt.schedulePreviewChangedTasks', { count: previewChangedTaskIds.size })}</span>
                                        ) : (
                                            <span>{t('gantt.schedulePreviewNoDateChanges')}</span>
                                        )}
                                        {schedulePreview.overdue_task_ids.length > 0 && (
                                            <span>{t('gantt.schedulePreviewOverdueTasks', { count: schedulePreview.overdue_task_ids.length })}</span>
                                        )}
                                    </div>
                                )}
                            </div>
                        </div>
                        <div className="flex flex-wrap gap-2 self-end sm:self-auto">
                            <Button
                                type="button"
                                size="sm"
                                variant="secondary"
                                onClick={returnToSavedSchedule}
                                disabled={scheduleMutation.isPending || scheduleMutation.isError}
                            >
                                {t('gantt.discardSchedulePreview')}
                            </Button>
                            <Button
                                type="button"
                                size="sm"
                                onClick={applySchedulePreview}
                                isLoading={scheduleMutation.isPending}
                                disabled={scheduleMutation.isError}
                            >
                                {t('gantt.applySchedulePreview')}
                            </Button>
                        </div>
                    </div>
                </section>
            )}

            {schedulePreviewMutation.isError && (
                <QueryErrorState
                    className="m-3 shrink-0 sm:m-4"
                    title={t('gantt.schedulePreviewFailedTitle')}
                    message={t('gantt.schedulePreviewFailed')}
                    retryLabel={t('gantt.retrySchedulePreview')}
                    onRetry={beginSchedulePreview}
                />
            )}

            {scheduleMutation.isError && (
                <QueryErrorState
                    className="m-3 shrink-0 sm:m-4"
                    title={t('gantt.scheduleSaveUnconfirmedTitle')}
                    message={t('gantt.scheduleSaveUnconfirmedBody')}
                    retryLabel={t('gantt.refreshSavedSchedule')}
                    onRetry={() => void refreshSavedSchedule()}
                />
            )}

            {/* Main Virtualized Area */}
            {displayTasks.length === 0 ? (
                <section
                    className="flex flex-1 flex-col items-center justify-center px-6 py-12 text-center"
                    aria-label={t('gantt.chartRegion')}
                >
                    {isFilteredEmpty ? (
                        <ListFilter aria-hidden="true" className="h-7 w-7 text-content-tertiary" />
                    ) : (
                        <CalendarOff aria-hidden="true" className="h-7 w-7 text-content-tertiary" />
                    )}
                    <h2 className="mt-3 text-base font-semibold text-content-primary">
                        {t(isFilteredEmpty ? 'gantt.noFilteredTasksTitle' : 'gantt.noTasksTitle')}
                    </h2>
                    <p className="mt-1 max-w-[60ch] text-sm text-content-secondary">
                        {t(isFilteredEmpty ? 'gantt.noFilteredTasksBody' : 'gantt.noTasksBody')}
                    </p>
                    {isFilteredEmpty ? (
                        <Button className="mt-4" size="sm" variant="secondary" onClick={clearFilters}>
                            {t('surfaces.ganttChart.clearFilters')}
                        </Button>
                    ) : (
                        <Link className="btn primary sm mt-4" to="/tasks?create=1">
                            {t('gantt.addTask')}
                        </Link>
                    )}
                </section>
            ) : (
                <div
                    ref={scrollContainerRef}
                    className="flex-1 overflow-auto relative select-none"
                    role="region"
                    tabIndex={0}
                    aria-label={t('gantt.chartRegion')}
                    aria-describedby={chartInstructionsId}
                    aria-busy={schedulePreviewMutation.isPending || scheduleMutation.isPending || isRefreshingSavedSchedule}
                    onMouseDown={onMouseDown}
                    onMouseLeave={stopDragging}
                    onMouseUp={stopDragging}
                    onMouseMove={onMouseMove}
                >
                    <p id={chartInstructionsId} className="sr-only">
                        {t('gantt.chartInstructions')}
                    </p>
                {/* 1. Header Layer (Sticky Top) */}
                <div
                    className="sticky top-0 z-40 bg-surface-subtle border-b shadow-sm"
                    style={{
                        width: `${SIDEBAR_WIDTH + columnVirtualizer.getTotalSize()}px`,
                        height: '60px'
                    }}
                >
                    {/* Top Row: Months */}
                    <div className="relative h-7 border-b border-border bg-surface-muted text-xs text-content-secondary font-semibold"
                        style={{ width: '100%' }}
                    >
                        <div className="absolute left-0 top-0 bottom-0 z-50 bg-surface-muted border-r border-border w-[300px]" />
                        {monthGroups.map((group, idx) => (
                            <div key={idx}
                                className={clsx("absolute top-0 bottom-0 text-center border-r border-border flex items-center justify-center truncate px-1", idx % 2 === 0 ? "bg-feedback-indigo-muted/50" : "bg-feedback-success-muted/50")}
                                style={{
                                    left: `${SIDEBAR_WIDTH + group.startIndex * zoomLevel}px`,
                                    width: `${group.count * zoomLevel}px`
                                }}
                            >
                                {group.month}
                            </div>
                        ))}
                    </div>

                    {/* Bottom Row: Days */}
                    <div className="relative h-8 bg-surface-card" style={{ width: '100%' }}>
                        <div className="absolute left-0 top-0 bottom-0 z-50 bg-surface-card border-r border-border-strong w-[300px] flex items-center pl-4 font-bold text-content-primary shadow-[2px_0_5px_-2px_rgba(0,0,0,0.1)]">
                            {t('surfaces.ganttChart.task')}
                        </div>
                        {columnVirtualizer.getVirtualItems().map(virtualColumn => {
                            const day = visibleDays[virtualColumn.index];
                            const isWknd = isWeekendDay(day);
                            const isHol = isHolidayDay(day);
                            return (
                                <div
                                    key={virtualColumn.index}
                                    className={clsx(
                                        "absolute top-0 bottom-0 border-r border-border-subtle flex flex-col items-center justify-center text-[10px]",
                                        isHol ? "bg-feedback-danger-muted text-feedback-danger-foreground" : isWknd ? "bg-action-muted text-action-muted-foreground" : "bg-surface-card text-content-secondary"
                                    )}
                                    style={{
                                        left: `${SIDEBAR_WIDTH + virtualColumn.start}px`,
                                        width: `${virtualColumn.size}px`
                                    }}
                                >
                                    <time
                                        dateTime={format(day, 'yyyy-MM-dd')}
                                        aria-label={getCalendarDayLabel(day)}
                                        className="flex flex-col items-center"
                                    >
                                        <span aria-hidden="true" className="font-bold">{format(day, 'd')}</span>
                                        <span aria-hidden="true" className="text-[9px]">
                                            {format(day, 'EEE', { locale: dateFnsLocale(activeI18n.language) })}
                                        </span>
                                    </time>
                                </div>
                            );
                        })}
                    </div>
                </div>

                {/* 2. Content Container */}
                <div
                    className="relative"
                    style={{
                        width: `${SIDEBAR_WIDTH + columnVirtualizer.getTotalSize()}px`,
                        height: `${rowVirtualizer.getTotalSize()}px`,
                    }}
                >
                    {/* A. Background Grid Layer (Absolute, Full Height of visible area) */}
                    <div className="absolute inset-0 pointer-events-none z-0">
                        {columnVirtualizer.getVirtualItems().map(virtualColumn => {
                            const day = visibleDays[virtualColumn.index];
                            const isWknd = isWeekendDay(day);
                            const isHol = isHolidayDay(day);
                            const isToday = isSameDay(day, new Date());

                            if (!isWknd && !isHol && !isToday) return null;

                            return (
                                <div
                                    key={`grid-${virtualColumn.index}`}
                                    className={clsx(
                                        "absolute top-0 bottom-0 h-full border-r border-border-subtle/50",
                                        isHol ? "bg-feedback-danger-muted/50" : isWknd ? "bg-action-muted/30" : "bg-transparent",
                                        isToday && "bg-feedback-warning-muted/30"
                                    )}
                                    style={{
                                        left: `${SIDEBAR_WIDTH + virtualColumn.start}px`,
                                        width: `${virtualColumn.size}px`,
                                    }}
                                >
                                    {isToday && <div className="w-0.5 h-full bg-feedback-warning absolute left-1/2 -translate-x-1/2 opacity-50" />}
                                </div>
                            );
                        })}
                        <div
                            className="absolute inset-0 z-[-1]"
                            style={{
                                left: `${SIDEBAR_WIDTH}px`,
                                backgroundImage: `linear-gradient(to right, transparent ${zoomLevel - 1}px, rgb(var(--color-border-subtle)) ${zoomLevel - 1}px)`,
                                backgroundSize: `${zoomLevel}px 100%`
                            }}
                        />
                    </div>

                    {/* B. Task Rows Layer */}
                    {rowVirtualizer.getVirtualItems().map(virtualRow => {
                        const task = displayTasks[virtualRow.index];
                        const taskDates = getTaskTimelineDates(task);
                        const taskPosition = hasCompleteTimelineDates(taskDates)
                            ? getTaskPosition(task)
                            : null;
                        const isSelected = editingTask?.id === task.id;
                        const isTaskExpanded = activeFilterCount > 0 || expandedTasks.has(task.id);

                        return (
                            <div
                                key={task.id}
                                className={clsx(
                                    "absolute left-0 w-full hover:bg-surface-muted/80 transition-colors border-b border-border-subtle",
                                    isSelected && "bg-action-muted/50"
                                )}
                                style={{
                                    top: `${virtualRow.start}px`,
                                    height: `${virtualRow.size}px`,
                                }}
                            >
                                {/* Fixed Sidebar Cell */}
                                <div
                                    className="absolute left-0 top-0 bottom-0 w-[300px] border-r border-border bg-surface-card z-20 flex flex-col justify-center px-2 shadow-[2px_0_5px_-2px_rgba(0,0,0,0.1)]"
                                >
                                    <div className="flex items-center gap-1" style={{ paddingLeft: `${task.depth * 16}px` }}>
                                        {task.children && task.children.length > 0 ? (
                                            activeFilterCount > 0 ? (
                                                <span className="p-0.5 text-content-secondary" aria-hidden="true">
                                                    <ChevronDown className="h-4 w-4" />
                                                </span>
                                            ) : (
                                                <button
                                                    type="button"
                                                    onClick={() => toggleExpand(task.id)}
                                                    className="p-0.5 hover:bg-surface-subtle rounded text-content-secondary focus:outline-none focus-visible:ring-2 focus-visible:ring-focus"
                                                    aria-expanded={isTaskExpanded}
                                                    aria-label={isTaskExpanded
                                                        ? t('gantt.collapseTask', { title: task.title })
                                                        : t('gantt.expandTask', { title: task.title })}
                                                >
                                                    {isTaskExpanded
                                                        ? <ChevronDown className="h-4 w-4" />
                                                        : <ChevronRight className="h-4 w-4" />}
                                                </button>
                                            )
                                        ) : <span className="w-5" />}
                                        <div className="font-medium truncate text-sm flex-1 text-content-primary" title={task.title}>{task.title}</div>
                                    </div>
                                    <div className="mt-1 flex items-center gap-1.5 pl-6 text-[10px] text-content-tertiary">
                                        <span
                                            className="max-w-[96px] truncate"
                                            title={task.assignee?.name ?? t('common.unassigned')}
                                        >
                                            {task.assignee?.name ?? t('common.unassigned')}
                                        </span>
                                        <span
                                            aria-label={t('surfaces.ganttChart.priorityScale', { priority: task.priority })}
                                            title={t('surfaces.ganttChart.priorityScale', { priority: task.priority })}
                                            className={clsx("shrink-0 rounded border px-1", task.priority <= 2 ? "border-feedback-danger-border text-feedback-danger-foreground bg-feedback-danger-muted" : "border-border")}
                                        >
                                            {t('surfaces.ganttChart.priority', { priority: task.priority })}
                                        </span>
                                        {previewChangedTaskIds.has(task.id) && (
                                            <span className="truncate rounded bg-action-muted px-1 text-action">
                                                {t('gantt.previewDatesChanged')}
                                            </span>
                                        )}
                                    </div>
                                </div>

                                {/* Row Content Area */}
                                <div className="absolute top-0 bottom-0" style={{ left: `${SIDEBAR_WIDTH}px`, right: 0 }}>

                                    {getCollapsedVacationRanges(task.assignee?.id).map((range, i) => (
                                        <div
                                            key={i}
                                            aria-hidden="true"
                                            className="absolute top-0 bottom-0 bg-feedback-purple-muted/60 pattern-diagonal-lines"
                                            title={t('surfaces.ganttChart.vacation')}
                                            style={{ left: `${range.left}px`, width: `${range.width}px` }}
                                        />
                                    ))}

                                    {taskPosition ? (
                                        <button
                                            type="button"
                                            className={clsx(
                                                "absolute top-3 z-10 flex h-6 items-center rounded px-2 text-xs shadow-sm transition-all",
                                                getTaskBaseColorClass(task),
                                                task.is_delayed && "ring-2 ring-feedback-purple ring-offset-1",
                                                task.is_overdue && "ring-2 ring-feedback-danger ring-offset-1",
                                                task.isSandboxModified && "ring-2 ring-focus ring-offset-2 border border-action font-semibold",
                                                previewChangedTaskIds.has(task.id) && "ring-2 ring-focus ring-offset-2 border border-action font-semibold",
                                                schedulePreview
                                                    ? "cursor-not-allowed opacity-80"
                                                    : "cursor-pointer hover:brightness-110 active:brightness-90"
                                            )}
                                            style={{ left: `${taskPosition.left}px`, width: `${taskPosition.width}px` }}
                                            onClick={(event) => {
                                                event.stopPropagation();
                                                if (schedulePreview) return;
                                                setEditingTask(task);
                                            }}
                                            aria-disabled={schedulePreview ? true : undefined}
                                            title={schedulePreview ? getPreviewTaskDescription(task) : getTaskTooltip(task)}
                                            aria-label={schedulePreview
                                                ? getPreviewTaskDescription(task)
                                                : getTaskAccessibleLabel(task)}
                                        >
                                            <span className="truncate font-medium drop-shadow-md">{task.title}</span>
                                        </button>
                                    ) : schedulePreview ? (
                                        <div
                                            className="absolute left-2 right-2 top-2.5 z-10 flex h-7 w-fit max-w-[calc(100%-1rem)] items-center gap-1.5 rounded-md border border-feedback-warning-border bg-feedback-warning-muted px-2 text-xs text-feedback-warning-foreground"
                                            role="note"
                                            aria-label={getPreviewTaskDescription(task)}
                                            title={getPreviewTaskDescription(task)}
                                        >
                                            <CalendarOff aria-hidden="true" className="h-3.5 w-3.5 shrink-0" />
                                            <span className="font-medium">{t('gantt.notScheduled')}</span>
                                        </div>
                                    ) : (
                                        <button
                                            type="button"
                                            className="absolute left-2 right-2 top-2.5 z-10 flex h-7 w-fit max-w-[calc(100%-1rem)] items-center gap-1.5 rounded-md border border-feedback-warning-border bg-feedback-warning-muted px-2 text-xs text-feedback-warning-foreground transition-colors hover:brightness-95 focus:outline-none focus-visible:ring-2 focus-visible:ring-focus"
                                            onClick={(event) => {
                                                event.stopPropagation();
                                                setEditingTask(task);
                                            }}
                                            aria-label={t('gantt.openUnscheduledTask', { title: task.title })}
                                            title={getUnscheduledTaskDescription(task)}
                                        >
                                            <CalendarOff aria-hidden="true" className="h-3.5 w-3.5 shrink-0" />
                                            <span className="shrink-0 font-medium">{t('gantt.notScheduled')}</span>
                                            <span aria-hidden="true" className="truncate text-content-secondary">
                                                · {getUnscheduledTaskGuidance(task)}
                                            </span>
                                        </button>
                                    )}
                                </div>
                            </div>
                        );
                    })}
                </div>
                </div>
            )}

            <TaskEditModal
                task={editingTask}
                iterationId={iterationId}
                isOpen={!!editingTask}
                onClose={() => setEditingTask(null)}
                sandboxMode={sandboxMode}
                onSaveSandbox={onSaveSandbox}
            />
        </div>
    );
};

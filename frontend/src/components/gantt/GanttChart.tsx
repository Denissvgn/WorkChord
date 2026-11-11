/* eslint-disable jsx-a11y/no-noninteractive-element-interactions, jsx-a11y/no-noninteractive-tabindex -- The native scroll region is focusable for keyboard scrolling and supports optional pointer panning. */
import { useState, useMemo, useRef, useEffect, useCallback, useId } from 'react';
import type { KeyboardEvent as ReactKeyboardEvent, PointerEvent as ReactPointerEvent } from 'react';
import { useVirtualizer } from '@tanstack/react-virtual';
import { eachDayOfInterval, format, isSameDay, addDays, differenceInCalendarDays, parseISO, startOfDay } from 'date-fns';
import { RefreshCw, ChevronRight, ChevronDown, ZoomIn, ZoomOut, Minimize2, Maximize2, Calendar, CalendarOff, CalendarRange, Crosshair, GitBranch, ListFilter, Eye, Pin, X } from 'lucide-react';
import { Link } from 'react-router-dom';
import { Button } from '../common/Button';
import { planningIssueTasksHref } from '../../features/planningMasters/planningTaskIssues';
import { Checkbox } from '../common/Checkbox';
import { TaskEditModal } from './TaskEditModal';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { ganttService } from '../../services/ganttService';
import clsx from 'clsx';
import { UnscheduledTasks } from './UnscheduledTasks';
import type { GanttTask, SchedulePreviewResponse } from '../../types/gantt';
import { STATUS_TONE, toneSolidClassName } from '../ui/tone';
import { QueryErrorState, QueryLoadingState } from '../feedback/QueryState';
import { useToast } from '../feedback/toast';
import { dateFnsLocale } from '../../i18n/dateLocale';
import { formatDate } from '../../utils/formatDate';
import { useTranslation } from 'react-i18next';
import { OverflowMenu, SlideOverDrawer } from '../ui';
import { GanttBarInputs } from './GanttBarInputs';

interface GanttChartProps {
    iterationId: number;
    iterationRevision?: number;
    startDate: string;
    endDate: string;
    tasks: GanttTask[];
    weekends: string[];
    holidays: string[];
    memberVacations: Record<number, string[]>;
    sandboxMode?: boolean;
    onSaveSandbox?: (taskId: number, updatedData: Partial<GanttTask>) => void;
}

const ZOOM_MIN = 20;
const ZOOM_MAX = 100;
const ZOOM_STEP = 10;
const ZOOM_DEFAULT = 40;
const TASK_COLUMN_MIN = 200;
const TASK_COLUMN_MAX = 480;
const TASK_COLUMN_DEFAULT = 300;
const TASK_COLUMN_STORAGE_KEY = 'workchord:gantt-task-column-width';
const LEGEND_STATUSES = ['planned', 'active', 'resolved', 'closed'] as const;
const LINKS_STORAGE_KEY = 'workchord:gantt-show-dependency-links';
const BAR_CENTER_Y = 24;

const readStoredShowLinks = () => {
    try {
        return window.localStorage.getItem(LINKS_STORAGE_KEY) !== 'false';
    } catch {
        return true;
    }
};

const readStoredTaskColumnWidth = () => {
    try {
        const stored = Number(window.localStorage.getItem(TASK_COLUMN_STORAGE_KEY));
        return Number.isFinite(stored) && stored >= TASK_COLUMN_MIN && stored <= TASK_COLUMN_MAX ? stored : TASK_COLUMN_DEFAULT;
    } catch {
        return TASK_COLUMN_DEFAULT;
    }
};

const isTypingTarget = (target: EventTarget | null) => target instanceof HTMLElement
    && (target.isContentEditable || ['INPUT', 'SELECT', 'TEXTAREA'].includes(target.tagName));

interface FlattenedTask extends GanttTask {
    depth: number;
}

type GanttGroupBy = 'none' | 'milestone' | 'prefix' | 'status';
type GanttStatusFilter = '' | 'planned' | 'active' | 'resolved' | 'closed';
type GanttRow =
    | { kind: 'task'; task: FlattenedTask }
    | { kind: 'group'; key: string; label: string; count: number };

const ID_PREFIX_PATTERN = /^([A-Za-z][A-Za-z0-9]*)[-_]\d+/;

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
    iterationRevision,    startDate,
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
    const [hideUnscheduled, setHideUnscheduled] = useState(false);
    const [zoomLevel, setZoomLevel] = useState(ZOOM_DEFAULT); // Width of one day column in pixels
    const [isCompressed, setIsCompressed] = useState(false);
    const [taskColumnWidth, setTaskColumnWidthState] = useState(readStoredTaskColumnWidth);
    const setTaskColumnWidth = (width: number) => {
        const next = Math.min(TASK_COLUMN_MAX, Math.max(TASK_COLUMN_MIN, Math.round(width)));
        setTaskColumnWidthState(next);
        try { window.localStorage.setItem(TASK_COLUMN_STORAGE_KEY, String(next)); } catch { /* Storage may be unavailable. */ }
    };
    const [isSortedByDate, setIsSortedByDate] = useState(false);
    const [editingTask, setEditingTask] = useState<GanttTask | null>(null);
    // In "Try changes", a bar opens its five date inputs first; the drawer is "More fields".
    // Drag in "Try changes": each gesture changes one scheduler input, never a date.
    type BarDrag = { kind: 'move' | 'resize' | 'link'; task: GanttTask; startX: number; dayDelta: number; pointerX: number; pointerY: number };
    const [barDrag, setBarDrag] = useState<BarDrag | null>(null);
    const suppressBarClick = useRef(false);
    const [barInputs, setBarInputs] = useState<{ task: GanttTask; anchor: { top: number; left: number }; origin: HTMLElement } | null>(null);
    const [isFiltersOpen, setIsFiltersOpen] = useState(false);
    const [showLinks, setShowLinksState] = useState(readStoredShowLinks);
    const setShowLinks = (value: boolean) => {
        setShowLinksState(value);
        try { window.localStorage.setItem(LINKS_STORAGE_KEY, String(value)); } catch { /* Storage may be unavailable. */ }
    };
    const [hoveredTaskId, setHoveredTaskId] = useState<number | null>(null);
    const [searchText, setSearchText] = useState('');
    const [statusFilter, setStatusFilter] = useState<GanttStatusFilter>('');
    const [groupBy, setGroupBy] = useState<GanttGroupBy>('none');
    const [collapsedGroups, setCollapsedGroups] = useState<Set<string>>(new Set());
    const normalizedSearch = searchText.trim().toLowerCase();
    const activeFilterCount = Number(selectedAssigneeId !== null) + Number(hideUnassigned)
        + Number(Boolean(normalizedSearch)) + Number(statusFilter !== '') + Number(hideUnscheduled);
    const clearFilters = () => {
        setSelectedAssigneeId(null);
        setHideUnassigned(false);
        setSearchText('');
        setStatusFilter('');
        setHideUnscheduled(false);
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
        if (matches && statusFilter) matches = task.status === statusFilter;
        if (matches && normalizedSearch) {
            matches = task.title.toLowerCase().includes(normalizedSearch) || `#${task.id}` === normalizedSearch || String(task.id) === normalizedSearch;
        }
        if (matches) return true;
        if (task.children) return task.children.some(child => taskMatchesFilter(child, assigneeId, hideUnassignedTasks));
        return false;
    }, [normalizedSearch, statusFilter]);

    const unscheduledTaskCount = useMemo(() => {
        let count = 0;
        const visit = (task: GanttTask) => {
            if (task.children?.length) task.children.forEach(visit);
            else if (!hasCompleteTimelineDates(getTaskTimelineDates(task))) count += 1;
        };
        tasks.forEach(visit);
        return count;
    }, [tasks]);
    const unassignedTaskCount = useMemo(() => {
        let count = 0;
        const visit = (task: GanttTask) => {
            if (task.children?.length) task.children.forEach(visit);
            // Same rule as the plan: only planned work can block the schedule.
            else if (!task.assignee && task.status === 'planned' && !task.is_deferred) count += 1;
        };
        tasks.forEach(visit);
        return count;
    }, [tasks]);

    const displayTasks = useMemo(() => {
        const flattened: FlattenedTask[] = [];
        const processTask = (task: GanttTask, depth: number) => {
            if (!taskMatchesFilter(task, selectedAssigneeId, hideUnassigned)) return;
            if (hideUnscheduled && !task.children?.length && !hasCompleteTimelineDates(getTaskTimelineDates(task))) return;
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
    }, [activeFilterCount, sortedTasks, expandedTasks, selectedAssigneeId, hideUnassigned, hideUnscheduled, taskMatchesFilter]);

    // Grouping keeps each top-level task with its children and adds one header per group.
    const rows = useMemo<GanttRow[]>(() => {
        if (groupBy === 'none') return displayTasks.map(task => ({ kind: 'task' as const, task }));
        const groupOf = (task: FlattenedTask): { key: string; label: string } => {
            if (groupBy === 'milestone') {
                return task.milestone ? { key: `m${task.milestone.id}`, label: task.milestone.name } : { key: 'm-none', label: t('surfaces.ganttChart.noMilestone') };
            }
            if (groupBy === 'status') return { key: task.status, label: t(`statuses.${task.status}`) };
            const prefix = ID_PREFIX_PATTERN.exec(task.title)?.[1]?.toUpperCase();
            return prefix ? { key: `p${prefix}`, label: prefix } : { key: 'p-none', label: t('surfaces.ganttChart.noIdPrefix') };
        };
        const groups = new Map<string, { label: string; tasks: FlattenedTask[]; count: number }>();
        let current: { label: string; tasks: FlattenedTask[]; count: number } | null = null;
        displayTasks.forEach(task => {
            if (task.depth === 0 || current === null) {
                const { key, label } = groupOf(task);
                current = groups.get(key) ?? { label, tasks: [], count: 0 };
                groups.set(key, current);
                current.count += 1;
            }
            current.tasks.push(task);
        });
        const result: GanttRow[] = [];
        groups.forEach((group, key) => {
            result.push({ kind: 'group', key, label: group.label, count: group.count });
            if (!collapsedGroups.has(key)) group.tasks.forEach(task => result.push({ kind: 'task', task }));
        });
        return result;
    }, [collapsedGroups, displayTasks, groupBy, t]);

    // Dependencies point from a task to its predecessors; invert them once for successors.
    const successorsById = useMemo(() => {
        const map = new Map<number, number[]>();
        const visit = (task: GanttTask) => {
            task.dependencies?.forEach(predecessorId => map.set(predecessorId, [...(map.get(predecessorId) ?? []), task.id]));
            task.children?.forEach(visit);
        };
        sourceTasks.forEach(visit);
        return map;
    }, [sourceTasks]);
    const rowIndexByTaskId = useMemo(() => {
        const map = new Map<number, number>();
        rows.forEach((row, index) => { if (row.kind === 'task') map.set(row.task.id, index); });
        return map;
    }, [rows]);

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
        count: rows.length,
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
        mutationFn: () => ganttService.previewSchedule(iterationId, [], iterationRevision),
        onSuccess: preview => {
            setEditingTask(null);
            setSchedulePreview(preview);
        },
    });

    // feedback-policy: mutation pending,inline - Apply is disabled while pending and failures retain the preview for retry.
    const scheduleMutation = useMutation({
        mutationFn: () => ganttService.schedule(iterationId, schedulePreview?.input_revision ?? iterationRevision, schedulePreview?.input_planning_revision),
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

    const taskTimingFlags = (task: GanttTask) => [
        task.is_overdue ? t('gantt.flagOverdue') : null,
        task.is_delayed ? t('gantt.flagLateStart') : null,
    ].filter(Boolean).map(flag => ` ${flag}`).join('');

    // The bar repeats nothing from the task column: who carries it and for how long.
    const getTaskBarText = (task: GanttTask) => {
        const dates = getTaskTimelineDates(task);
        const days = hasCompleteTimelineDates(dates)
            ? differenceInCalendarDays(parseISO(dates.end), parseISO(dates.start)) + 1
            : null;
        const owner = task.assignee?.name ?? t('common.unassigned');
        return days === null ? owner : t('gantt.taskBarText', { owner, count: days });
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
        return t('gantt.taskBarSummary', {
            title: task.title,
            status: t(`statuses.${task.status}`),
            flags: taskTimingFlags(task),
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
            status: t(`statuses.${task.status}`),
            assignee: task.assignee?.name ?? t('common.unassigned'),
            priority: task.priority,
            ...formatTaskTimelineDates(dates),
        }) + taskTimingFlags(task) + (dependencySummary(task) ? ` ${dependencySummary(task)}` : '');
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

    const SIDEBAR_WIDTH = taskColumnWidth;
    const startBarDrag = (event: ReactPointerEvent<HTMLElement>, task: GanttTask, kind: BarDrag['kind']) => {
        if (!sandboxMode || schedulePreview || event.button !== 0) return;
        event.stopPropagation();
        const startX = event.clientX;
        const drag: BarDrag = { kind, task, startX, dayDelta: 0, pointerX: event.clientX, pointerY: event.clientY };
        setBarDrag(drag);
        const move = (moveEvent: PointerEvent) => {
            const dayDelta = Math.round((moveEvent.clientX - startX) / zoomLevel);
            setBarDrag(current => current && { ...current, dayDelta, pointerX: moveEvent.clientX, pointerY: moveEvent.clientY });
        };
        const finish = (upEvent: PointerEvent) => {
            window.removeEventListener('pointermove', move);
            window.removeEventListener('pointerup', finish);
            const dayDelta = Math.round((upEvent.clientX - startX) / zoomLevel);
            setBarDrag(null);
            if (kind === 'link') {
                const target = document.elementFromPoint(upEvent.clientX, upEvent.clientY)?.closest<HTMLElement>('[data-gantt-task-id]');
                const targetId = Number(target?.dataset.ganttTaskId);
                const successor = Number.isFinite(targetId) ? rows.find(row => row.kind === 'task' && row.task.id === targetId) : undefined;
                if (successor?.kind === 'task' && successor.task.id !== task.id && !successor.task.dependencies?.includes(task.id)) {
                    suppressBarClick.current = true;
                    onSaveSandbox?.(successor.task.id, { dependencies: [...(successor.task.dependencies ?? []), task.id], sandbox_update: undefined });
                }
                return;
            }
            if (dayDelta === 0) return;
            suppressBarClick.current = true;
            const dates = getTaskTimelineDates(task);
            if (kind === 'move' && dates.start) {
                // Dragging the bar pins its earliest start; the scheduler still decides the dates.
                onSaveSandbox?.(task.id, { min_start_date: format(addDays(parseISO(dates.start), dayDelta), 'yyyy-MM-dd'), sandbox_update: undefined });
            } else if (kind === 'resize') {
                const effort = Math.max(0.5, (task.effort_days ?? 1) + dayDelta);
                onSaveSandbox?.(task.id, { effort_days: effort, sandbox_update: undefined });
            }
        };
        window.addEventListener('pointermove', move);
        window.addEventListener('pointerup', finish);
    };
    const focusTaskId = hoveredTaskId ?? editingTask?.id ?? null;
    const focusTask = focusTaskId === null ? undefined : rows.find(row => row.kind === 'task' && row.task.id === focusTaskId);
    const highlightedTaskIds = new Set<number>(focusTask && focusTask.kind === 'task'
        ? [focusTask.task.id, ...(focusTask.task.dependencies ?? []), ...(successorsById.get(focusTask.task.id) ?? [])]
        : []);
    const dependencySummary = (task: GanttTask) => {
        const predecessors = task.dependencies?.length ?? 0;
        const successors = successorsById.get(task.id)?.length ?? 0;
        return predecessors + successors > 0
            ? t('gantt.dependencySummary', { predecessors, successors })
            : '';
    };
    const zoomPercent = Math.round((zoomLevel / ZOOM_DEFAULT) * 100);
    const zoomOut = () => setZoomLevel(value => Math.max(ZOOM_MIN, value - ZOOM_STEP));
    const zoomIn = () => setZoomLevel(value => Math.min(ZOOM_MAX, value + ZOOM_STEP));
    const todayIndex = visibleDays.findIndex(day => isSameDay(day, new Date()));
    const scrollToToday = () => {
        const container = scrollContainerRef.current;
        if (!container || todayIndex < 0) return;
        const timelineWidth = Math.max(0, container.clientWidth - SIDEBAR_WIDTH);
        container.scrollTo({ left: Math.max(0, todayIndex * zoomLevel - timelineWidth / 2 + zoomLevel / 2), behavior: 'smooth' });
    };
    const fitIteration = () => {
        const container = scrollContainerRef.current;
        const iterationDays = differenceInCalendarDays(new Date(endDate), new Date(startDate)) + 1;
        if (!container || iterationDays <= 0) return;
        const timelineWidth = Math.max(0, container.clientWidth - SIDEBAR_WIDTH);
        setZoomLevel(Math.min(ZOOM_MAX, Math.max(ZOOM_MIN, Math.floor(timelineWidth / iterationDays))));
        container.scrollTo({ left: 0 });
    };
    // "+" and "-" zoom and "T" jumps to today, unless the person is typing.
    const handleChartShortcut = (event: ReactKeyboardEvent<HTMLDivElement>) => {
        if (event.altKey || event.ctrlKey || event.metaKey || isTypingTarget(event.target)) return;
        if (event.key === '+' || event.key === '=') { event.preventDefault(); zoomIn(); }
        else if (event.key === '-' || event.key === '_') { event.preventDefault(); zoomOut(); }
        else if (event.key === 't' || event.key === 'T') { event.preventDefault(); scrollToToday(); }
    };
    const isFilteredEmpty = sourceTasks.length > 0
        && activeFilterCount > 0
        && displayTasks.length === 0;

    return (
        <div role="region" aria-label={t('surfaces.ganttChart.chartRegion')} className="flex h-full min-h-0 flex-col overflow-hidden rounded-lg bg-surface-card shadow" onKeyDown={handleChartShortcut}>
            {unscheduledTaskCount > 0 && (
                // One summary replaces a warning on every unscheduled row.
                <div role="status" className="flex shrink-0 flex-wrap items-center gap-3 border-b border-border bg-surface-muted px-4 py-2 text-sm text-content-primary">
                    <CalendarOff aria-hidden="true" className="h-4 w-4 shrink-0 text-content-secondary" />
                    <span className="min-w-0 flex-1">
                        {unassignedTaskCount > 0
                            ? t('surfaces.ganttChart.unscheduledSummaryUnassigned', { count: unscheduledTaskCount })
                            : t('surfaces.ganttChart.unscheduledSummary', { count: unscheduledTaskCount })}
                    </span>
                    {unassignedTaskCount > 0 && (
                        <Link className="btn sm" to={planningIssueTasksHref({ issue: 'unassigned', iterationId, returnStepId: 'schedule' })}>
                            {t('surfaces.ganttChart.assignOwners', { count: unassignedTaskCount })}
                        </Link>
                    )}
                    <Button size="sm" variant="ghost" aria-pressed={hideUnscheduled} onClick={() => setHideUnscheduled(value => !value)}>
                        {hideUnscheduled ? t('surfaces.ganttChart.showUnscheduled') : t('surfaces.ganttChart.hideUnscheduled')}
                    </Button>
                </div>
            )}
            {/* Toolbar */}
            <div className="z-10 flex shrink-0 flex-wrap items-center justify-between gap-2 border-b border-border bg-surface-card p-3 sm:p-4">
                <div role="group" aria-label={t('surfaces.ganttChart.timelineControls')} className="flex min-w-0 flex-wrap items-center gap-2">
                    <Button variant="ghost" size="sm" onClick={zoomOut} disabled={zoomLevel <= ZOOM_MIN}
                        aria-label={t('surfaces.ganttChart.zoomTimelineOut')} title={t('surfaces.ganttChart.zoomOutShortcut')}>
                        <ZoomOut className="h-4 w-4" aria-hidden="true" />
                    </Button>
                    <span className="min-w-14 text-center text-sm tabular-nums text-content-secondary" aria-live="polite">
                        {t('surfaces.ganttChart.zoomLevel', { percent: zoomPercent })}
                    </span>
                    <Button variant="ghost" size="sm" onClick={zoomIn} disabled={zoomLevel >= ZOOM_MAX}
                        aria-label={t('surfaces.ganttChart.zoomTimelineIn')} title={t('surfaces.ganttChart.zoomInShortcut')}>
                        <ZoomIn className="h-4 w-4" aria-hidden="true" />
                    </Button>
                    <Button variant="secondary" size="sm" onClick={scrollToToday} disabled={todayIndex < 0}
                        title={todayIndex < 0 ? t('surfaces.ganttChart.todayOutsideTimeline') : t('surfaces.ganttChart.todayShortcut')}>
                        <Crosshair className="mr-2 h-4 w-4" aria-hidden="true" />
                        {t('surfaces.ganttChart.today')}
                    </Button>
                    <Button variant="secondary" size="sm" onClick={fitIteration}>
                        <CalendarRange className="mr-2 h-4 w-4" aria-hidden="true" />
                        {t('surfaces.ganttChart.fitIteration')}
                    </Button>
                    <Button variant="ghost" size="sm" aria-pressed={showLinks} onClick={() => setShowLinks(!showLinks)}>
                        <GitBranch className="mr-2 h-4 w-4" aria-hidden="true" />
                        {t('surfaces.ganttChart.dependencyLinks')}
                    </Button>
                </div>
                <div className="flex min-w-0 flex-wrap items-center gap-2">
                    <input
                        type="search"
                        value={searchText}
                        onChange={event => setSearchText(event.target.value)}
                        placeholder={t('surfaces.ganttChart.searchPlaceholder')}
                        aria-label={t('surfaces.ganttChart.searchTasks')}
                        className="input h-9 w-44 text-sm"
                    />
                    <select value={statusFilter} onChange={event => setStatusFilter(event.target.value as GanttStatusFilter)}
                        aria-label={t('surfaces.ganttChart.statusFilter')} className="input h-9 w-auto text-sm">
                        <option value="">{t('surfaces.ganttChart.anyStatus')}</option>
                        {LEGEND_STATUSES.map(status => <option key={status} value={status}>{t(`statuses.${status}`)}</option>)}
                    </select>
                    <select value={groupBy} onChange={event => { setGroupBy(event.target.value as GanttGroupBy); setCollapsedGroups(new Set()); }}
                        aria-label={t('surfaces.ganttChart.groupBy')} className="input h-9 w-auto text-sm">
                        <option value="none">{t('surfaces.ganttChart.groupNone')}</option>
                        <option value="milestone">{t('surfaces.ganttChart.groupMilestone')}</option>
                        <option value="prefix">{t('surfaces.ganttChart.groupPrefix')}</option>
                        <option value="status">{t('surfaces.ganttChart.groupStatus')}</option>
                    </select>
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

            <details className="shrink-0 border-b border-border bg-surface-card px-4 py-2 text-xs text-content-secondary">
                <summary className="cursor-pointer font-medium text-content-primary">{t('surfaces.ganttChart.legend')}</summary>
                <p className="mt-2">{t('gantt.datesAreCalculated')}</p>
                <ul className="mt-2 flex flex-wrap gap-x-4 gap-y-2">
                    {LEGEND_STATUSES.map(status => <li key={status} className="flex items-center gap-1.5">
                        <span aria-hidden="true" className={clsx('inline-block h-3 w-5 rounded', toneSolidClassName[STATUS_TONE[status]])} />
                        {t(`statuses.${status}`)}
                    </li>)}
                    <li className="flex items-center gap-1.5"><span aria-hidden="true" className="inline-block h-3 w-5 rounded bg-surface-card ring-2 ring-feedback-danger" />{t('surfaces.ganttChart.legendOverdue')}</li>
                    <li className="flex items-center gap-1.5"><span aria-hidden="true" className="inline-block h-3 w-5 rounded bg-surface-card ring-2 ring-feedback-purple" />{t('surfaces.ganttChart.legendLateStart')}</li>
                    <li className="flex items-center gap-1.5"><span aria-hidden="true" className="inline-block h-3 w-5 rounded border border-action bg-surface-card ring-2 ring-focus" />{t('surfaces.ganttChart.legendChanged')}</li>
                    <li className="flex items-center gap-1.5"><span aria-hidden="true" className="inline-block h-3 w-0.5 bg-action" />{t('surfaces.ganttChart.legendToday')}</li>
                    <li className="flex items-center gap-1.5"><span aria-hidden="true" className="inline-block h-3 w-5 rounded bg-surface-muted" />{t('surfaces.ganttChart.legendWeekend')}</li>
                    <li className="flex items-center gap-1.5"><span aria-hidden="true" className="inline-block h-3 w-5 rounded bg-feedback-danger-muted" />{t('surfaces.ganttChart.legendHoliday')}</li>
                    <li className="flex items-center gap-1.5"><span aria-hidden="true" className="inline-block h-3 w-5 rounded border border-dashed border-border-strong" />{t('surfaces.ganttChart.legendNoDates')}</li>
                </ul>
            </details>

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
                                {Boolean(schedulePreview.schedule_result?.capacity_issues?.length) && <p className="mt-2 text-sm text-feedback-warning-foreground">{t('teamwork.capacityConflicts')}</p>}
                                {!scheduleMutation.isPending && <UnscheduledTasks items={schedulePreview.schedule_result?.unscheduled} />}
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
                                disabled={scheduleMutation.isError || Boolean(schedulePreview.schedule_result?.capacity_issues?.length)}
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
                        <div className="absolute left-0 top-0 bottom-0 z-50 bg-surface-muted border-r border-border" style={{ width: `${SIDEBAR_WIDTH}px` }} />
                        {monthGroups.map((group, idx) => (
                            <div key={idx}
                                className={clsx("absolute top-0 bottom-0 text-center border-r border-border flex items-center justify-center truncate px-1", idx % 2 === 0 ? "bg-surface-muted" : "bg-surface-card")}
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
                        <div className="absolute left-0 top-0 bottom-0 z-50 bg-surface-card border-r border-border-strong flex items-center pl-4 font-bold text-content-primary shadow-[2px_0_5px_-2px_rgba(0,0,0,0.1)]"
                            style={{ width: `${SIDEBAR_WIDTH}px` }}>
                            {t('surfaces.ganttChart.task')}
                            <div
                                role="separator"
                                aria-orientation="vertical"
                                aria-label={t('surfaces.ganttChart.resizeTaskColumn')}
                                aria-valuemin={TASK_COLUMN_MIN}
                                aria-valuemax={TASK_COLUMN_MAX}
                                aria-valuenow={SIDEBAR_WIDTH}
                                tabIndex={0}
                                className="absolute right-0 top-0 h-full w-2 cursor-col-resize hover:bg-action-muted focus-visible:bg-action-muted focus-visible:outline-none"
                                onKeyDown={event => {
                                    if (event.key === 'ArrowLeft') { event.preventDefault(); event.stopPropagation(); setTaskColumnWidth(SIDEBAR_WIDTH - 20); }
                                    if (event.key === 'ArrowRight') { event.preventDefault(); event.stopPropagation(); setTaskColumnWidth(SIDEBAR_WIDTH + 20); }
                                }}
                                onPointerDown={event => {
                                    event.preventDefault();
                                    event.stopPropagation();
                                    const startX = event.clientX;
                                    const startWidth = SIDEBAR_WIDTH;
                                    const move = (moveEvent: PointerEvent) => setTaskColumnWidth(startWidth + moveEvent.clientX - startX);
                                    const stop = () => { window.removeEventListener('pointermove', move); window.removeEventListener('pointerup', stop); };
                                    window.addEventListener('pointermove', move);
                                    window.addEventListener('pointerup', stop);
                                }}
                            />
                        </div>
                        {columnVirtualizer.getVirtualItems().map(virtualColumn => {
                            const day = visibleDays[virtualColumn.index];
                            const isWknd = isWeekendDay(day);
                            const isHol = isHolidayDay(day);
                            return (
                                <div
                                    key={virtualColumn.index}
                                    className={clsx(
                                        "absolute top-0 bottom-0 border-r border-border-subtle flex flex-col items-center justify-center text-wc-micro",
                                        isSameDay(day, new Date()) ? "bg-action-muted font-semibold text-action" : isHol ? "bg-feedback-danger-muted text-feedback-danger-foreground" : isWknd ? "bg-surface-muted text-content-tertiary" : "bg-surface-card text-content-secondary"
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
                                        <span aria-hidden="true" className="text-wc-micro">
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
                    {/* Dependency links for the rendered rows only, so virtualization stays cheap. */}
                    {showLinks && (
                        <svg aria-hidden="true" className="pointer-events-none absolute left-0 top-0 z-[5] text-content-tertiary"
                            width={SIDEBAR_WIDTH + columnVirtualizer.getTotalSize()} height={rowVirtualizer.getTotalSize()}>
                            <defs>
                                <marker id={`${chartInstructionsId}-arrow`} viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto">
                                    <path d="M0,0 L8,4 L0,8 z" fill="currentColor" />
                                </marker>
                            </defs>
                            {rowVirtualizer.getVirtualItems().flatMap(virtualRow => {
                                const row = rows[virtualRow.index];
                                if (row.kind !== 'task' || !row.task.dependencies?.length) return [];
                                const successor = row.task;
                                const successorDates = getTaskTimelineDates(successor);
                                if (!hasCompleteTimelineDates(successorDates)) return [];
                                const successorPosition = getTaskPosition(successor);
                                return successor.dependencies.flatMap(predecessorId => {
                                    const predecessorIndex = rowIndexByTaskId.get(predecessorId);
                                    if (predecessorIndex === undefined) return [];
                                    const predecessorRow = rows[predecessorIndex];
                                    if (predecessorRow.kind !== 'task' || !hasCompleteTimelineDates(getTaskTimelineDates(predecessorRow.task))) return [];
                                    const predecessorPosition = getTaskPosition(predecessorRow.task);
                                    const x1 = SIDEBAR_WIDTH + predecessorPosition.left + predecessorPosition.width;
                                    const y1 = predecessorIndex * ROW_HEIGHT + BAR_CENTER_Y;
                                    const x2 = SIDEBAR_WIDTH + successorPosition.left;
                                    const y2 = virtualRow.index * ROW_HEIGHT + BAR_CENTER_Y;
                                    const elbow = Math.max(x1 + 8, Math.min(x2 - 8, x1 + 16));
                                    const highlighted = highlightedTaskIds.has(successor.id) && highlightedTaskIds.has(predecessorId)
                                        && (focusTaskId === successor.id || focusTaskId === predecessorId);
                                    return [(
                                        <path key={`${predecessorId}-${successor.id}`}
                                            d={`M${x1},${y1} H${elbow} V${y2} H${x2}`}
                                            fill="none" stroke="currentColor"
                                            className={highlighted ? 'text-action' : undefined}
                                            strokeWidth={highlighted ? 2.5 : 1.25}
                                            markerEnd={`url(#${chartInstructionsId}-arrow)`} />
                                    )];
                                });
                            })}
                        </svg>
                    )}

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
                                        isHol ? "bg-feedback-danger-muted/50" : isWknd ? "bg-surface-muted" : "bg-transparent"
                                    )}
                                    style={{
                                        left: `${SIDEBAR_WIDTH + virtualColumn.start}px`,
                                        width: `${virtualColumn.size}px`,
                                    }}
                                >
                                    {isToday && <div aria-hidden="true" className="absolute left-1/2 h-full w-0.5 -translate-x-1/2 bg-action" />}
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
                        const row = rows[virtualRow.index];
                        if (row.kind === 'group') {
                            const collapsed = collapsedGroups.has(row.key);
                            return (
                                <div key={`group-${row.key}`} className="absolute left-0 w-full border-b border-border bg-surface-muted"
                                    style={{ top: `${virtualRow.start}px`, height: `${virtualRow.size}px` }}>
                                    <button type="button" aria-expanded={!collapsed}
                                        className="sticky left-0 flex h-full items-center gap-2 px-3 text-sm font-semibold text-content-primary focus:outline-none focus-visible:ring-2 focus-visible:ring-focus"
                                        onClick={() => setCollapsedGroups(previous => {
                                            const next = new Set(previous);
                                            if (next.has(row.key)) next.delete(row.key); else next.add(row.key);
                                            return next;
                                        })}>
                                        {collapsed ? <ChevronRight className="h-4 w-4" aria-hidden="true" /> : <ChevronDown className="h-4 w-4" aria-hidden="true" />}
                                        {t('surfaces.ganttChart.groupHeader', { label: row.label, count: row.count })}
                                    </button>
                                </div>
                            );
                        }
                        const task = row.task;
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
                                    className="absolute left-0 top-0 bottom-0 border-r border-border bg-surface-card z-20 flex flex-col justify-center px-2 shadow-[2px_0_5px_-2px_rgba(0,0,0,0.1)]"
                                    style={{ width: `${SIDEBAR_WIDTH}px` }}
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
                                                        : t('gantt.expandTask', { title: task.title })} title={isTaskExpanded
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
                                    <div className="mt-1 flex items-center gap-1.5 pl-6 text-wc-micro text-content-tertiary">
                                        <span
                                            className="max-w-[96px] truncate"
                                            title={task.assignee?.name ?? t('common.unassigned')}
                                        >
                                            {task.assignee?.name ?? t('common.unassigned')}
                                        </span>
                                        <span
                                            aria-label={t('surfaces.ganttChart.priorityScale', { priority: task.priority })}
                                            title={t('surfaces.ganttChart.priorityScale', { priority: task.priority })}
                                            className={clsx("shrink-0 rounded border border-border px-1 text-content-secondary", task.priority <= 2 && "font-semibold text-content-primary")}
                                        >
                                            {t('surfaces.ganttChart.priority', { priority: task.priority })}
                                        </span>
                                        {dependencySummary(task) && (
                                            <span className="shrink-0 rounded border border-border px-1 text-content-secondary" title={dependencySummary(task)}
                                                aria-label={dependencySummary(task)}>
                                                {t('surfaces.ganttChart.dependencyCount', { count: (task.dependencies?.length ?? 0) + (successorsById.get(task.id)?.length ?? 0) })}
                                            </span>
                                        )}
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

                                    {taskPosition ? (<>
                                        <button
                                            type="button"
                                            className={clsx(
                                                "absolute top-3 z-10 flex h-6 items-center rounded px-2 text-xs shadow-sm transition-all",
                                                getTaskBaseColorClass(task),
                                                task.is_delayed && "ring-2 ring-feedback-purple ring-offset-1",
                                                task.is_overdue && "ring-2 ring-feedback-danger ring-offset-1",
                                                task.isSandboxModified && "ring-2 ring-focus ring-offset-2 border border-action font-semibold",
                                                previewChangedTaskIds.has(task.id) && "ring-2 ring-focus ring-offset-2 border border-action font-semibold",
                                                highlightedTaskIds.has(task.id) && focusTaskId !== task.id && "outline outline-2 outline-offset-2 outline-action",
                                                schedulePreview
                                                    ? "cursor-not-allowed opacity-80"
                                                    : "cursor-pointer hover:brightness-110 active:brightness-90"
                                            )}
                                            style={{
                                                left: `${taskPosition.left + (barDrag?.kind === 'move' && barDrag.task.id === task.id ? barDrag.dayDelta * zoomLevel : 0)}px`,
                                                width: `${Math.max(zoomLevel, taskPosition.width + (barDrag?.kind === 'resize' && barDrag.task.id === task.id ? barDrag.dayDelta * zoomLevel : 0))}px`,
                                            }}
                                            data-gantt-task-id={task.id}
                                            onPointerDown={event => startBarDrag(event, task, 'move')}
                                            onMouseEnter={() => setHoveredTaskId(task.id)}
                                            onMouseLeave={() => setHoveredTaskId(null)}
                                            onFocus={() => setHoveredTaskId(task.id)}
                                            onBlur={() => setHoveredTaskId(null)}
                                            onClick={(event) => {
                                                event.stopPropagation();
                                                if (schedulePreview) return;
                                                if (suppressBarClick.current) { suppressBarClick.current = false; return; }
                                                if (sandboxMode) {
                                                    const rect = event.currentTarget.getBoundingClientRect();
                                                    setBarInputs({
                                                        task,
                                                        origin: event.currentTarget,
                                                        anchor: {
                                                            top: Math.min(rect.bottom + 8, window.innerHeight - 440),
                                                            left: Math.max(16, Math.min(rect.left, window.innerWidth - 336)),
                                                        },
                                                    });
                                                    return;
                                                }
                                                setEditingTask(task);
                                            }}
                                            aria-disabled={schedulePreview ? true : undefined}
                                            aria-haspopup={sandboxMode ? 'dialog' : undefined}
                                            title={schedulePreview ? getPreviewTaskDescription(task) : getTaskTooltip(task)}
                                            aria-label={schedulePreview
                                                ? getPreviewTaskDescription(task)
                                                : getTaskAccessibleLabel(task)}
                                        >
                                            <span className="truncate font-medium drop-shadow-md">{getTaskBarText(task)}</span>
                                            {sandboxMode && !schedulePreview && (
                                                <>
                                                    {/* Right edge: drag to change effort. */}
                                                    <span aria-hidden="true" title={t('gantt.dragToChangeEffort')}
                                                        className="absolute right-0 top-0 h-full w-2 cursor-ew-resize rounded-r bg-surface-card/40"
                                                        onPointerDown={event => startBarDrag(event, task, 'resize')} />
                                                    {/* End handle: drag onto another bar to make it wait for this one. */}
                                                    <span aria-hidden="true" title={t('gantt.dragToLink')}
                                                        className="absolute -right-3 top-1/2 h-2.5 w-2.5 -translate-y-1/2 cursor-crosshair rounded-full border border-action bg-surface-card"
                                                        onPointerDown={event => startBarDrag(event, task, 'link')} />
                                                </>
                                            )}
                                        </button>
                                        {sandboxMode && task.isSandboxModified && task.min_start_date && (
                                            <button type="button"
                                                className="absolute top-3 z-10 flex h-6 items-center gap-1 rounded border border-border bg-surface-card px-1.5 text-xs text-content-secondary hover:bg-surface-muted"
                                                style={{ left: `${Math.max(0, taskPosition.left - 64)}px` }}
                                                aria-label={t('gantt.removeStartPin', { title: task.title, date: formatDate(task.min_start_date, activeI18n.language) })}
                                                title={t('gantt.removeStartPin', { title: task.title, date: formatDate(task.min_start_date, activeI18n.language) })}
                                                onClick={event => { event.stopPropagation(); onSaveSandbox?.(task.id, { min_start_date: null, sandbox_update: undefined }); }}>
                                                <Pin className="h-3 w-3" aria-hidden="true" /><X className="h-3 w-3" aria-hidden="true" />
                                            </button>
                                        )}
                                        </>
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
                                            className="absolute left-2 right-2 top-2.5 z-10 flex h-7 w-fit max-w-[calc(100%-1rem)] items-center gap-1.5 rounded-md border border-dashed border-border-strong bg-surface-card px-2 text-xs text-content-secondary transition-colors hover:bg-surface-muted focus:outline-none focus-visible:ring-2 focus-visible:ring-focus"
                                            onClick={(event) => {
                                                event.stopPropagation();
                                                setEditingTask(task);
                                            }}
                                            aria-label={t('gantt.openUnscheduledTask', { title: task.title })}
                                            title={getUnscheduledTaskDescription(task)}
                                        >
                                            <CalendarOff aria-hidden="true" className="h-3.5 w-3.5 shrink-0" />
                                            <span className="shrink-0 font-medium">{t('gantt.notScheduled')}</span>
                                        </button>
                                    )}
                                </div>
                            </div>
                        );
                    })}
                </div>
                </div>
            )}

            {barInputs && (
                <GanttBarInputs
                    task={barInputs.task}
                    iterationId={iterationId}
                    anchor={barInputs.anchor}
                    taskOptions={displayTasks.filter(item => !item.children?.length).map(item => ({ id: item.id, title: item.title }))}
                    onApply={changes => {
                        // Clear any full-form payload so these inputs are what the dry-run sends.
                        onSaveSandbox?.(barInputs.task.id, { ...changes, sandbox_update: undefined });
                        const origin = barInputs.origin;
                        setBarInputs(null);
                        origin.focus();
                    }}
                    onMoreFields={() => { const task = barInputs.task; setBarInputs(null); setEditingTask(task); }}
                    onClose={() => { const origin = barInputs.origin; setBarInputs(null); origin.focus(); }}
                />
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

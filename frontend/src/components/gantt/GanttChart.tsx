import i18n from '../../i18n/i18n';
import { useState, useMemo, useRef, useEffect, useCallback } from 'react';
import { useVirtualizer } from '@tanstack/react-virtual';
import { eachDayOfInterval, format, isSameDay, addDays, differenceInCalendarDays, parseISO, startOfDay } from 'date-fns';
import { RefreshCw, ChevronRight, ChevronDown, ZoomIn, ZoomOut, Minimize2, Maximize2, Calendar } from 'lucide-react';
import { Button } from '../common/Button';
import { Checkbox } from '../common/Checkbox';
import { TaskEditModal } from './TaskEditModal';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { ganttService } from '../../services/ganttService';
import clsx from 'clsx';
import type { GanttTask } from '../../types/gantt';
import { STATUS_TONE, toneSolidClassName } from '../ui/tone';
import { QueryErrorState } from '../feedback/QueryState';
import { dateFnsLocale } from '../../i18n/dateLocale';
import { formatDate } from '../../utils/formatDate';
import { useTranslation } from 'react-i18next';

const t = i18n.t.bind(i18n);

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
    const { i18n: activeI18n } = useTranslation();
    const queryClient = useQueryClient();
    const [expandedTasks, setExpandedTasks] = useState<Set<number>>(new Set());
    const initialExpansionDone = useRef(false);
    const scrollContainerRef = useRef<HTMLDivElement>(null);

    // Initial expansion logic
    useEffect(() => {
        if (tasks.length > 0 && !initialExpansionDone.current) {
            const allIds = new Set<number>();
            const traverse = (t: GanttTask) => {
                if (t.children?.length) {
                    allIds.add(t.id);
                    t.children.forEach(traverse);
                }
            };
            tasks.forEach(traverse);
            setExpandedTasks(allIds);
            initialExpansionDone.current = true;
        }
    }, [tasks]);

    const [selectedAssigneeId, setSelectedAssigneeId] = useState<number | null>(null);
    const [hideUnassigned, setHideUnassigned] = useState(false);
    const [zoomLevel, setZoomLevel] = useState(40); // Width of day column
    const [isCompressed, setIsCompressed] = useState(false);
    const [isSortedByDate, setIsSortedByDate] = useState(false);
    const [editingTask, setEditingTask] = useState<GanttTask | null>(null);

    // --- Data Preparation ---

    const sortedTasks = useMemo(() => {
        if (!isSortedByDate) return tasks;

        const getTaskStart = (t: GanttTask) => t.schedule_result?.scheduled_start || t.start_date || '9999-12-31';

        const sortRecursive = (list: GanttTask[]): GanttTask[] => {
            return [...list].sort((a, b) => {
                return getTaskStart(a).localeCompare(getTaskStart(b));
            }).map(t => ({
                ...t,
                children: t.children ? sortRecursive(t.children) : []
            }));
        };

        return sortRecursive(tasks);
    }, [tasks, isSortedByDate]);

    const uniqueAssignees = useMemo(() => {
        const assigneeMap = new Map<number, { id: number; name: string }>();
        const collectAssignees = (taskList: GanttTask[]) => {
            taskList.forEach(t => {
                if (t.assignee) assigneeMap.set(t.assignee.id, t.assignee);
                if (t.children) collectAssignees(t.children);
            });
        };
        collectAssignees(tasks);
        return Array.from(assigneeMap.values()).sort((a, b) => a.name.localeCompare(b.name));
    }, [tasks]);

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

        const maxTaskEnd = findMaxEndDate(tasks);
        if (maxTaskEnd > iterationEnd) {
            const overdueEnd = addDays(maxTaskEnd, 2);
            if (overdueEnd > end) end = overdueEnd;
        }

        return eachDayOfInterval({ start, end });
    }, [startDate, endDate, tasks]);

    const visibleDays = useMemo(() => {
        if (!isCompressed) return days;

        const leafTaskRanges: { start: Date; end: Date }[] = [];
        const collectLeafRanges = (taskList: GanttTask[]) => {
            taskList.forEach(task => {
                if (!task.children || task.children.length === 0) {
                    const taskStart = new Date(task.schedule_result?.scheduled_start || task.start_date || startDate);
                    const taskEnd = new Date(task.schedule_result?.scheduled_end || task.end_date || addDays(taskStart, task.duration_days || task.effort_days || 1));
                    leafTaskRanges.push({ start: taskStart, end: taskEnd });
                } else {
                    collectLeafRanges(task.children);
                }
            });
        };
        collectLeafRanges(tasks);

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
    }, [days, isCompressed, tasks, startDate]);

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
            if (task.children && task.children.length > 0 && expandedTasks.has(task.id)) {
                task.children.forEach(child => processTask(child, depth + 1));
            }
        };
        sortedTasks.forEach(task => processTask(task, 0));
        return flattened;
    }, [sortedTasks, expandedTasks, selectedAssigneeId, hideUnassigned, taskMatchesFilter]);


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

    const scheduleMutation = useMutation({
        mutationFn: () => ganttService.schedule(iterationId),
        onSuccess: () => queryClient.invalidateQueries({ queryKey: ['gantt', iterationId] }),
    });

    const getTaskBaseColorClass = (task: GanttTask) => {
        return toneSolidClassName[STATUS_TONE[task.status]];
    };

    const getTaskTooltip = (task: GanttTask) => {
        return `${task.title}\n${formatDate(task.start_date)} → ${formatDate(task.end_date)}`;
    };

    // --- Helpers for Absolute Positioning ---

    const getTaskPosition = (task: GanttTask) => {
        const startDateStr = task.schedule_result?.scheduled_start || task.start_date || startDate;
        const taskStart = typeof startDateStr === 'string' ? parseISO(startDateStr) : startDateStr;

        const endDateStr = task.schedule_result?.scheduled_end || task.end_date;
        const taskEnd = endDateStr
            ? (typeof endDateStr === 'string' ? parseISO(endDateStr) : endDateStr)
            : addDays(taskStart, task.duration_days || task.effort_days || 1);

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

    return (
        <div className="flex h-full min-h-0 flex-col overflow-hidden rounded-lg bg-surface-card shadow">
            {/* Toolbar */}
            <div className="z-10 flex shrink-0 flex-col gap-3 border-b border-border bg-surface-card p-3 sm:p-4 lg:flex-row lg:items-center lg:justify-between">
                <h2 className="text-lg font-bold sm:text-xl">{t('surfaces.ganttChart.projectSchedule')}</h2>
                <div className="flex min-w-0 flex-wrap items-center gap-2">
                    <select
                        value={selectedAssigneeId ?? ''}
                        onChange={e => setSelectedAssigneeId(e.target.value ? parseInt(e.target.value) : null)}
                        className="min-w-44 flex-1 rounded-md border border-border-strong bg-surface-card px-3 py-2 text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-focus sm:flex-none"
                    >
                        <option value="">{t('surfaces.ganttChart.allAssignees')}</option>
                        {uniqueAssignees.map(a => <option key={a.id} value={a.id}>{a.name}</option>)}
                    </select>

                    <Checkbox className="shrink-0" checked={hideUnassigned} onChange={setHideUnassigned} label={t('surfaces.ganttChart.hideUnassigned')} />

                    <div className="mx-1 hidden h-6 w-px bg-surface-hover sm:block" />

                    <Button
                        variant={isSortedByDate ? "primary" : "ghost"}
                        size="sm"
                        onClick={() => setIsSortedByDate(!isSortedByDate)}
                        title={t(isSortedByDate ? 'surfaces.ganttChart.sortingByDate' : 'surfaces.ganttChart.sortByDate')}
                    >
                        <Calendar className="w-4 h-4 mr-2" />
                        {t(isSortedByDate ? 'surfaces.ganttChart.dateOrder' : 'surfaces.ganttChart.sortDate')}
                    </Button>

                    <div className="flex flex-wrap items-center gap-2">
                        <Button variant="ghost" size="sm" onClick={() => {
                            const allIds = new Set<number>();
                            const traverse = (t: GanttTask) => { if (t.children?.length) { allIds.add(t.id); t.children.forEach(traverse); } };
                            tasks.forEach(traverse);
                            setExpandedTasks(allIds);
                        }}>{t('surfaces.ganttChart.expandAll')}</Button>

                        <Button variant="ghost" size="sm" onClick={() => setExpandedTasks(new Set())}>{t('surfaces.ganttChart.collapseAll')}</Button>
                    </div>

                    <Button onClick={() => scheduleMutation.mutate()} isLoading={scheduleMutation.isPending}>
                        <RefreshCw className="w-4 h-4 mr-2" /> {t('surfaces.ganttChart.autoSchedule')}
                    </Button>

                    <div className="flex items-center gap-1 border-l border-border pl-2 sm:ml-2">
                        <Button variant="ghost" size="sm" aria-label={t('gantt.zoomOut')} onClick={() => setZoomLevel(p => Math.max(20, p - 10))}><ZoomOut className="w-4 h-4" /></Button>
                        <Button variant="ghost" size="sm" aria-label={t('gantt.zoomIn')} onClick={() => setZoomLevel(p => Math.min(100, p + 10))}><ZoomIn className="w-4 h-4" /></Button>
                        <Button variant="ghost" size="sm" aria-label={isCompressed ? t('gantt.expandLayout') : t('gantt.compressLayout')} onClick={() => setIsCompressed(p => !p)}>
                            {isCompressed ? <Maximize2 className="w-4 h-4" /> : <Minimize2 className="w-4 h-4" />}
                        </Button>
                    </div>
                </div>
            </div>

            {scheduleMutation.isError && (
                <QueryErrorState
                    className="m-3 shrink-0 sm:m-4"
                    error={scheduleMutation.error}
                    fallback={t('surfaces.ganttChart.scheduleFailed')}
                    onRetry={() => scheduleMutation.mutate()}
                />
            )}

            {/* Main Virtualized Area */}
            <div
                ref={scrollContainerRef}
                className="flex-1 overflow-auto relative select-none"
                role="grid"
                tabIndex={0}
                aria-label={t('gantt.chartRegion')}
                onMouseDown={onMouseDown}
                onMouseLeave={stopDragging}
                onMouseUp={stopDragging}
                onMouseMove={onMouseMove}
            >
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
                                    <span className="font-bold">{format(day, 'd')}</span>
                                    <span className="text-[9px]">{format(day, 'EEE', { locale: dateFnsLocale(activeI18n.language) })}</span>
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
                        const { left, width } = getTaskPosition(task);
                        const isSelected = editingTask?.id === task.id;

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
                                            <button
                                                type="button"
                                                onClick={() => toggleExpand(task.id)}
                                                className="p-0.5 hover:bg-surface-subtle rounded text-content-secondary focus:outline-none focus-visible:ring-2 focus-visible:ring-focus"
                                                aria-expanded={expandedTasks.has(task.id)}
                                                aria-label={expandedTasks.has(task.id) ? t('gantt.collapseTask', { title: task.title }) : t('gantt.expandTask', { title: task.title })}
                                            >
                                                {expandedTasks.has(task.id) ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
                                            </button>
                                        ) : <span className="w-5" />}
                                        <div className="font-medium truncate text-sm flex-1 text-content-primary" title={task.title}>{task.title}</div>
                                    </div>
                                    <div className="flex items-center gap-2 pl-6 mt-1 text-[10px] text-content-tertiary">
                                        {task.assignee?.name && <span className="truncate max-w-[100px]">{task.assignee.name}</span>}
                                        <span className={clsx("px-1 rounded border", task.priority <= 2 ? "border-feedback-danger-border text-feedback-danger-foreground bg-feedback-danger-muted" : "border-border")}>
                                            P{task.priority}
                                        </span>
                                    </div>
                                </div>

                                {/* Row Content Area */}
                                <div className="absolute top-0 bottom-0" style={{ left: `${SIDEBAR_WIDTH}px`, right: 0 }}>

                                    {getCollapsedVacationRanges(task.assignee?.id).map((range, i) => (
                                        <div
                                            key={i}
                                            className="absolute top-0 bottom-0 bg-feedback-purple-muted/60 pattern-diagonal-lines"
                                            title={t('surfaces.ganttChart.vacation')}
                                            style={{ left: `${range.left}px`, width: `${range.width}px` }}
                                        />
                                    ))}

                                    <button
                                        type="button"
                                        className={clsx(
                                            "absolute top-3 h-6 rounded px-2 text-xs shadow-sm flex items-center cursor-pointer hover:brightness-110 active:brightness-90 transition-all z-10",
                                            getTaskBaseColorClass(task),
                                            task.is_delayed && "ring-2 ring-feedback-purple ring-offset-1",
                                            task.is_overdue && "ring-2 ring-feedback-danger ring-offset-1",
                                            task.isSandboxModified && "ring-2 ring-focus ring-offset-2 border border-action font-semibold"
                                        )}
                                        style={{ left: `${left}px`, width: `${width}px` }}
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            setEditingTask(task);
                                        }}
                                        title={getTaskTooltip(task)}
                                        aria-label={t('gantt.openTask', { title: task.title })}
                                    >
                                        <span className="truncate font-medium drop-shadow-md">{task.title}</span>
                                    </button>
                                </div>
                            </div>
                        );
                    })}
                </div>

                <TaskEditModal
                    task={editingTask}
                    iterationId={iterationId}
                    isOpen={!!editingTask}
                    onClose={() => setEditingTask(null)}
                    sandboxMode={sandboxMode}
                    onSaveSandbox={onSaveSandbox}
                />
            </div>
        </div>
    );
};

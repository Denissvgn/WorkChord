import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import type { KeyboardEvent as ReactKeyboardEvent } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
    ArrowUpDown,
    ClipboardCheck,
    Command,
    GanttChartSquare,
    Layers,
    List,
    LayoutGrid,
    ListFilter,
    ListTodo,
    MapPin,
    Maximize2,
    Minimize2,
    Plus,
    Search,
    Settings,
    Users,
} from 'lucide-react';
import type { LucideIcon } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { Checkbox } from '../common/Checkbox';
import { Modal } from '../common/Modal';
import { OPEN_COMMAND_MENU_EVENT } from './commandMenuEvents';
import { useSingleKeyShortcutPreference } from '../../hooks/useSingleKeyShortcutPreference';
import { getWorkspaceForPath } from '../../navigation/workspaces';

type CommandGroup = 'tasks' | 'current' | 'navigate' | 'suggested';

interface CommandAction {
    id: string;
    group: CommandGroup;
    label: string;
    description: string;
    keywords?: string[];
    icon: LucideIcon;
    shortcut?: string;
    ariaShortcut?: string;
    to: string;
}

const TASKS_FIRST_GROUPS = ['tasks', 'current', 'navigate'] as const satisfies readonly CommandGroup[];
const CURRENT_FIRST_GROUPS = ['current', 'navigate', 'tasks'] as const satisfies readonly CommandGroup[];
const COMPACT_GROUPS = ['current', 'suggested'] as const satisfies readonly CommandGroup[];
const MAX_COMPACT_SUGGESTIONS = 3;
const MAX_RECENT_COMMANDS = 3;

export const RECENT_COMMANDS_STORAGE_KEY = 'workchord.command-menu.recent';

const WORKSPACE_SUGGESTION_IDS: Record<
    ReturnType<typeof getWorkspaceForPath>['key'],
    readonly string[]
> = {
    delivery: ['new-task', 'task-filters', 'plan-work', 'gantt'],
    planning: ['gantt', 'tasks', 'team', 'settings'],
    resource: ['settings', 'team', 'tasks', 'gantt', 'plan-work'],
};

const readRecentCommandIds = () => {
    if (typeof window === 'undefined') return [];
    try {
        const parsed = JSON.parse(window.localStorage.getItem(RECENT_COMMANDS_STORAGE_KEY) ?? '[]');
        return Array.isArray(parsed)
            ? [...new Set(parsed.filter((value): value is string => typeof value === 'string'))]
                .slice(0, MAX_RECENT_COMMANDS)
            : [];
    } catch {
        return [];
    }
};

const isTasksWorkspacePath = (pathname: string) => (
    pathname === '/tasks' || pathname.startsWith('/tasks/')
);

const isInteractiveTarget = (target: EventTarget | null) => {
    if (!(target instanceof HTMLElement)) return false;
    return target.isContentEditable || Boolean(target.closest([
        'a[href]',
        'button',
        'input',
        'select',
        'textarea',
        '[contenteditable]:not([contenteditable="false"])',
        '[role="button"]',
        '[role="combobox"]',
        '[role="link"]',
        '[role="menuitem"]',
        '[role="option"]',
        '[role="slider"]',
        '[role="spinbutton"]',
        '[role="switch"]',
        '[role="tab"]',
        '[role="textbox"]',
    ].join(',')));
};

const withTaskCommand = (
    location: ReturnType<typeof useLocation>,
    key: string,
    value: string | null,
) => {
    const params = isTasksWorkspacePath(location.pathname)
        ? new URLSearchParams(location.search)
        : new URLSearchParams();
    if (key !== 'layout') {
        ['create', 'panel', 'sort', 'mode', 'fullscreen'].forEach(param => {
            if (param !== key) params.delete(param);
        });
    }
    if (value === null) params.delete(key);
    else params.set(key, value);
    const search = params.toString();
    return search ? `/tasks?${search}` : '/tasks';
};

export const CommandMenu = () => {
    const { t } = useTranslation();
    const navigate = useNavigate();
    const location = useLocation();
    const searchInputRef = useRef<HTMLInputElement>(null);
    const [open, setOpen] = useState(false);
    const [query, setQuery] = useState('');
    const [activeIndex, setActiveIndex] = useState(0);
    const [showAllCommands, setShowAllCommands] = useState(false);
    const [recentCommandIds, setRecentCommandIds] = useState<string[]>(readRecentCommandIds);
    const {
        enabled: singleKeyShortcutsEnabled,
        setEnabled: setSingleKeyShortcutsEnabled,
    } = useSingleKeyShortcutPreference();
    const inTasksWorkspace = isTasksWorkspacePath(location.pathname);
    const taskParams = inTasksWorkspace
        ? new URLSearchParams(location.search)
        : null;
    const isBoardView = taskParams?.get('layout') === 'board';
    const isTaskFullscreen = taskParams?.get('fullscreen') === '1';
    const currentWorkspace = getWorkspaceForPath(location.pathname);

    const commands = useMemo<CommandAction[]>(() => [
        {
            id: 'new-task',
            group: 'tasks',
            label: t('commandMenu.commands.newTask.label'),
            description: t('commandMenu.commands.newTask.description'),
            icon: Plus,
            shortcut: 'N',
            ariaShortcut: 'N',
            to: withTaskCommand(location, 'create', '1'),
        },
        {
            id: 'task-filters',
            group: 'tasks',
            label: t('commandMenu.commands.filters.label'),
            description: t('commandMenu.commands.filters.description'),
            icon: ListFilter,
            shortcut: 'F',
            ariaShortcut: 'F',
            to: withTaskCommand(location, 'panel', 'filters'),
        },
        {
            id: 'reorder-tasks',
            group: 'tasks',
            label: t('commandMenu.commands.reorder.label'),
            description: t('commandMenu.commands.reorder.description'),
            icon: ArrowUpDown,
            shortcut: 'R',
            ariaShortcut: 'R',
            to: withTaskCommand(location, 'sort', 'manual'),
        },
        {
            id: 'bulk-edit',
            group: 'tasks',
            label: t('commandMenu.commands.bulkEdit.label'),
            description: t('commandMenu.commands.bulkEdit.description'),
            icon: ClipboardCheck,
            shortcut: 'B',
            ariaShortcut: 'B',
            to: withTaskCommand(location, 'mode', 'bulk'),
        },
        {
            id: 'merge-tasks',
            group: 'tasks',
            label: t('commandMenu.commands.merge.label'),
            description: t('commandMenu.commands.merge.description'),
            icon: Layers,
            shortcut: 'M',
            ariaShortcut: 'M',
            to: withTaskCommand(location, 'mode', 'merge'),
        },
        {
            id: 'task-layout',
            group: 'tasks',
            label: t(isBoardView
                ? 'commandMenu.commands.list.label'
                : 'commandMenu.commands.board.label'),
            description: t(isBoardView
                ? 'commandMenu.commands.list.description'
                : 'commandMenu.commands.board.description'),
            icon: isBoardView ? List : LayoutGrid,
            to: withTaskCommand(location, 'layout', isBoardView ? null : 'board'),
        },
        {
            id: 'task-fullscreen',
            group: 'tasks',
            label: t(isTaskFullscreen
                ? 'commandMenu.commands.exitFullscreen.label'
                : 'commandMenu.commands.fullscreen.label'),
            description: t(isTaskFullscreen
                ? 'commandMenu.commands.exitFullscreen.description'
                : 'commandMenu.commands.fullscreen.description'),
            icon: isTaskFullscreen ? Minimize2 : Maximize2,
            to: withTaskCommand(location, 'fullscreen', isTaskFullscreen ? null : '1'),
        },
        {
            id: 'plan-work',
            group: 'navigate',
            label: t('commandMenu.commands.planWork.label'),
            description: t('commandMenu.commands.planWork.description'),
            icon: MapPin,
            to: '/plan',
        },
        {
            id: 'tasks',
            group: 'navigate',
            label: t('commandMenu.commands.tasks.label'),
            description: t('commandMenu.commands.tasks.description'),
            icon: ListTodo,
            to: '/tasks',
        },
        {
            id: 'gantt',
            group: 'navigate',
            label: t('commandMenu.commands.gantt.label'),
            description: t('commandMenu.commands.gantt.description'),
            icon: GanttChartSquare,
            to: '/gantt',
        },
        {
            id: 'team',
            group: 'navigate',
            label: t('commandMenu.commands.team.label'),
            description: t('commandMenu.commands.team.description'),
            icon: Users,
            to: '/team',
        },
        {
            id: 'settings',
            group: 'navigate',
            label: t('commandMenu.commands.settings.label'),
            description: t('commandMenu.commands.settings.description'),
            icon: Settings,
            to: '/settings',
        },
    ], [isBoardView, isTaskFullscreen, location, t]);

    const contextualCommands = useMemo<CommandAction[]>(() => {
        const isWorkspaceHome = location.pathname === currentWorkspace.defaultPath;
        const promotedCommandId = isWorkspaceHome
            ? {
                delivery: 'tasks',
                planning: null,
                resource: 'settings',
            }[currentWorkspace.key]
            : null;
        const promotedCommand = promotedCommandId
            ? commands.find(command => command.id === promotedCommandId)
            : undefined;
        const homeCommand = commands.find(command => (
            command.group === 'navigate'
            && command.to === currentWorkspace.defaultPath
        ));

        const currentWorkspaceAction: CommandAction = promotedCommand
            ? {
                ...promotedCommand,
                id: 'current-workspace-action',
                group: 'current',
            }
            : isWorkspaceHome && currentWorkspace.key === 'planning'
                ? {
                    id: 'current-workspace-action',
                    group: 'current',
                    label: t('commandMenu.commands.continuePlanWork.label'),
                    description: t('commandMenu.commands.continuePlanWork.description'),
                    keywords: homeCommand
                        ? [homeCommand.label, homeCommand.description]
                        : undefined,
                    icon: MapPin,
                    to: '/plan/master',
                }
                : {
                    id: 'current-workspace-action',
                    group: 'current',
                    label: t('nav.openWorkAreaHome', {
                        area: t(currentWorkspace.labelKey, currentWorkspace.defaultLabel),
                    }),
                    description: t(
                        currentWorkspace.descriptionKey,
                        currentWorkspace.defaultDescription,
                    ),
                    keywords: homeCommand
                        ? [homeCommand.label, homeCommand.description]
                        : undefined,
                    icon: currentWorkspace.icon,
                    to: currentWorkspace.defaultPath,
                };
        const suppressPlanLauncher = isWorkspaceHome && currentWorkspace.key === 'planning';

        return [
            currentWorkspaceAction,
            ...commands.filter(command => (
                command.to !== currentWorkspaceAction.to
                && !(suppressPlanLauncher && command.id === 'plan-work')
            )),
        ];
    }, [commands, currentWorkspace, location.pathname, t]);

    const groupOrder = inTasksWorkspace
        ? TASKS_FIRST_GROUPS
        : CURRENT_FIRST_GROUPS;
    const orderedCommands = useMemo(() => (
        groupOrder.flatMap(group => contextualCommands.filter(command => command.group === group))
    ), [contextualCommands, groupOrder]);

    const compactCommands = useMemo<CommandAction[]>(() => {
        const currentAction = contextualCommands.find(command => command.group === 'current');
        if (!currentAction) return [];

        const commandById = new Map(contextualCommands.map(command => [command.id, command]));
        const suggestions: CommandAction[] = [];
        const seenIds = new Set([currentAction.id]);
        const seenTargets = new Set([currentAction.to]);
        const currentLocation = `${location.pathname}${location.search}`;
        const addSuggestion = (command: CommandAction | undefined) => {
            if (
                !command
                || command.group === 'current'
                || command.to === currentLocation
                || seenIds.has(command.id)
                || seenTargets.has(command.to)
                || suggestions.length >= MAX_COMPACT_SUGGESTIONS
            ) return;

            seenIds.add(command.id);
            seenTargets.add(command.to);
            suggestions.push({ ...command, group: 'suggested' });
        };

        recentCommandIds.forEach(id => addSuggestion(commandById.get(id)));
        WORKSPACE_SUGGESTION_IDS[currentWorkspace.key]
            .forEach(id => addSuggestion(commandById.get(id)));
        orderedCommands.forEach(command => addSuggestion(command));

        return [currentAction, ...suggestions];
    }, [
        contextualCommands,
        currentWorkspace.key,
        location.pathname,
        location.search,
        orderedCommands,
        recentCommandIds,
    ]);

    const hasSearchQuery = query.trim().length > 0;
    const isCompactView = !hasSearchQuery && !showAllCommands;
    const visibleGroupOrder: readonly CommandGroup[] = isCompactView
        ? COMPACT_GROUPS
        : groupOrder;
    const filteredCommands = useMemo(() => {
        const normalizedQuery = query.trim().toLocaleLowerCase();
        if (!normalizedQuery) return showAllCommands ? orderedCommands : compactCommands;
        return orderedCommands.filter(command => (
            `${command.label} ${command.description} ${command.keywords?.join(' ') ?? ''}`
                .toLocaleLowerCase()
                .includes(normalizedQuery)
        ));
    }, [compactCommands, orderedCommands, query, showAllCommands]);

    useEffect(() => {
        if (!open) return;
        const activeCommand = filteredCommands[activeIndex];
        if (!activeCommand) return;

        document
            .getElementById(`workchord-command-option-${activeCommand.id}`)
            ?.scrollIntoView?.({ block: 'nearest' });
    }, [activeIndex, filteredCommands, open]);

    const closeMenu = () => {
        setOpen(false);
        setQuery('');
        setActiveIndex(0);
        setShowAllCommands(false);
    };

    const rememberCommand = useCallback((commandId: string) => {
        if (commandId === 'current-workspace-action') return;
        setRecentCommandIds(current => {
            const next = [commandId, ...current.filter(id => id !== commandId)]
                .slice(0, MAX_RECENT_COMMANDS);
            try {
                window.localStorage.setItem(RECENT_COMMANDS_STORAGE_KEY, JSON.stringify(next));
            } catch {
                // The command still runs when browser storage is unavailable.
            }
            return next;
        });
    }, []);

    const runCommand = (command: CommandAction) => {
        rememberCommand(command.id);
        closeMenu();
        navigate(command.to);
    };

    useEffect(() => {
        const handleOpenRequest = () => {
            setQuery('');
            setActiveIndex(0);
            setShowAllCommands(false);
            setOpen(true);
        };
        const handleKeyDown = (event: KeyboardEvent) => {
            if ((event.metaKey || event.ctrlKey) && event.key.toLocaleLowerCase() === 'k') {
                event.preventDefault();
                setQuery('');
                setActiveIndex(0);
                setShowAllCommands(false);
                setOpen(!open);
                return;
            }
            if (
                open
                || !singleKeyShortcutsEnabled
                || event.defaultPrevented
                || event.repeat
                || !inTasksWorkspace
                || isInteractiveTarget(event.target)
                || document.querySelector('[role="dialog"][aria-modal="true"]')
                || event.metaKey
                || event.ctrlKey
                || event.altKey
            ) {
                return;
            }

            const shortcut = event.key.toLocaleUpperCase();
            const command = commands.find(item => item.shortcut === shortcut);
            if (!command) return;
            event.preventDefault();
            rememberCommand(command.id);
            navigate(command.to);
        };

        window.addEventListener(OPEN_COMMAND_MENU_EVENT, handleOpenRequest);
        window.addEventListener('keydown', handleKeyDown);
        return () => {
            window.removeEventListener(OPEN_COMMAND_MENU_EVENT, handleOpenRequest);
            window.removeEventListener('keydown', handleKeyDown);
        };
    }, [
        commands,
        inTasksWorkspace,
        navigate,
        open,
        rememberCommand,
        singleKeyShortcutsEnabled,
    ]);

    const handleSearchKeyDown = (event: ReactKeyboardEvent<HTMLInputElement>) => {
        if (event.key === 'ArrowDown') {
            event.preventDefault();
            setActiveIndex(current => (
                filteredCommands.length === 0 ? 0 : (current + 1) % filteredCommands.length
            ));
        } else if (event.key === 'ArrowUp') {
            event.preventDefault();
            setActiveIndex(current => (
                filteredCommands.length === 0
                    ? 0
                    : (current - 1 + filteredCommands.length) % filteredCommands.length
            ));
        } else if (event.key === 'Enter' && filteredCommands[activeIndex]) {
            event.preventDefault();
            runCommand(filteredCommands[activeIndex]);
        }
    };

    return (
        <Modal
            open={open}
            title={(
                <span className="command-menu-title">
                    <Command aria-hidden="true" className="h-5 w-5" />
                    {t('commandMenu.title')}
                </span>
            )}
            description={t('commandMenu.description')}
            closeLabel={t('actions.close')}
            onClose={closeMenu}
            initialFocusRef={searchInputRef}
            className="command-menu-dialog"
            contentClassName="command-menu-content"
            footer={(
                <div className="command-menu-shortcut-setting">
                    <Checkbox
                        checked={singleKeyShortcutsEnabled}
                        onChange={setSingleKeyShortcutsEnabled}
                        label={t('commandMenu.singleKeyShortcuts.label')}
                        aria-describedby="command-menu-shortcut-description"
                    />
                    <p id="command-menu-shortcut-description">
                        {t('commandMenu.singleKeyShortcuts.description')}
                    </p>
                </div>
            )}
        >
            <div className="command-menu-search">
                <Search aria-hidden="true" className="h-4 w-4" />
                <label className="sr-only" htmlFor="workchord-command-search">
                    {t('commandMenu.searchLabel')}
                </label>
                <input
                    ref={searchInputRef}
                    id="workchord-command-search"
                    value={query}
                    onChange={event => {
                        setQuery(event.target.value);
                        setActiveIndex(0);
                    }}
                    onKeyDown={handleSearchKeyDown}
                    placeholder={t('commandMenu.searchPlaceholder')}
                    autoComplete="off"
                    role="combobox"
                    aria-autocomplete="list"
                    aria-expanded="true"
                    aria-haspopup="listbox"
                    aria-controls="workchord-command-results"
                    aria-activedescendant={
                        filteredCommands[activeIndex]
                            ? `workchord-command-option-${filteredCommands[activeIndex].id}`
                            : undefined
                    }
                />
                <kbd>{t('commandMenu.closeShortcut')}</kbd>
            </div>

            {!hasSearchQuery && (
                <div className="command-menu-view-mode">
                    <p>
                        {showAllCommands
                            ? t('commandMenu.allCommandsHint', { count: orderedCommands.length })
                            : t('commandMenu.suggestedCommandsHint')}
                    </p>
                    <button
                        type="button"
                        onClick={() => {
                            setShowAllCommands(value => !value);
                            setActiveIndex(0);
                            searchInputRef.current?.focus();
                        }}
                    >
                        {showAllCommands
                            ? t('commandMenu.showSuggestedCommands')
                            : t('commandMenu.showAllCommands')}
                    </button>
                </div>
            )}

            <div
                id="workchord-command-results"
                className="command-menu-results"
                role="listbox"
                aria-label={t('commandMenu.resultsLabel')}
            >
                {filteredCommands.length === 0 ? (
                    <div className="command-menu-empty" role="status">
                        <Search aria-hidden="true" className="h-5 w-5" />
                        <p>{t('commandMenu.noResults')}</p>
                    </div>
                ) : (
                    visibleGroupOrder.map(group => {
                        const groupedCommands = filteredCommands
                            .map((command, index) => ({ command, index }))
                            .filter(item => item.command.group === group);
                        if (groupedCommands.length === 0) return null;

                        return (
                            <section
                                key={group}
                                role="group"
                                aria-labelledby={`command-menu-group-${group}`}
                            >
                                <h3 id={`command-menu-group-${group}`}>
                                    {t(`commandMenu.groups.${group}`)}
                                </h3>
                                <div>
                                    {groupedCommands.map(({ command, index }) => {
                                        const Icon = command.icon;
                                        const active = activeIndex === index;
                                        return (
                                            <button
                                                key={command.id}
                                                id={`workchord-command-option-${command.id}`}
                                                type="button"
                                                role="option"
                                                tabIndex={-1}
                                                className="command-menu-item"
                                                data-active={active || undefined}
                                                aria-selected={active}
                                                aria-keyshortcuts={
                                                    singleKeyShortcutsEnabled
                                                        ? command.ariaShortcut
                                                        : undefined
                                                }
                                                onMouseEnter={() => setActiveIndex(index)}
                                                onClick={() => runCommand(command)}
                                            >
                                                <span className="command-menu-item-icon" aria-hidden="true">
                                                    <Icon className="h-4 w-4" />
                                                </span>
                                                <span className="command-menu-item-copy">
                                                    <strong>{command.label}</strong>
                                                    <span>{command.description}</span>
                                                </span>
                                                {singleKeyShortcutsEnabled && command.shortcut && (
                                                    <kbd aria-hidden="true">{command.shortcut}</kbd>
                                                )}
                                            </button>
                                        );
                                    })}
                                </div>
                            </section>
                        );
                    })
                )}
            </div>
        </Modal>
    );
};

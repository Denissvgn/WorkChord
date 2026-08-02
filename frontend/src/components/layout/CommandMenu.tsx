import { useEffect, useMemo, useRef, useState } from 'react';
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

interface CommandAction {
    id: string;
    group: 'tasks' | 'navigate';
    label: string;
    description: string;
    icon: LucideIcon;
    shortcut?: string;
    ariaShortcut?: string;
    to: string;
}

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
    const params = location.pathname === '/tasks'
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
    const {
        enabled: singleKeyShortcutsEnabled,
        setEnabled: setSingleKeyShortcutsEnabled,
    } = useSingleKeyShortcutPreference();
    const taskParams = location.pathname === '/tasks'
        ? new URLSearchParams(location.search)
        : null;
    const isBoardView = taskParams?.get('layout') === 'board';
    const isTaskFullscreen = taskParams?.get('fullscreen') === '1';

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
            to: '/plan/master',
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

    const filteredCommands = useMemo(() => {
        const normalizedQuery = query.trim().toLocaleLowerCase();
        if (!normalizedQuery) return commands;
        return commands.filter(command => (
            `${command.label} ${command.description}`
                .toLocaleLowerCase()
                .includes(normalizedQuery)
        ));
    }, [commands, query]);

    const closeMenu = () => {
        setOpen(false);
        setQuery('');
        setActiveIndex(0);
    };

    const runCommand = (command: CommandAction) => {
        closeMenu();
        navigate(command.to);
    };

    useEffect(() => {
        const handleOpenRequest = () => setOpen(true);
        const handleKeyDown = (event: KeyboardEvent) => {
            if ((event.metaKey || event.ctrlKey) && event.key.toLocaleLowerCase() === 'k') {
                event.preventDefault();
                setOpen(current => !current);
                return;
            }
            if (
                open
                || !singleKeyShortcutsEnabled
                || event.defaultPrevented
                || event.repeat
                || location.pathname !== '/tasks'
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
            navigate(command.to);
        };

        window.addEventListener(OPEN_COMMAND_MENU_EVENT, handleOpenRequest);
        window.addEventListener('keydown', handleKeyDown);
        return () => {
            window.removeEventListener(OPEN_COMMAND_MENU_EVENT, handleOpenRequest);
            window.removeEventListener('keydown', handleKeyDown);
        };
    }, [commands, location.pathname, navigate, open, singleKeyShortcutsEnabled]);

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
                    (['tasks', 'navigate'] as const).map(group => {
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

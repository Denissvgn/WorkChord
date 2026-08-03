import { useId, useState } from 'react';
import {
    ArrowDownUp,
    ChevronRight,
    CircleHelp,
    Command,
    CornerDownLeft,
    Keyboard,
} from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { Link, useLocation } from 'react-router-dom';
import { useSingleKeyShortcutPreference } from '../../hooks/useSingleKeyShortcutPreference';
import { getHelpContext, type HelpContentProvider } from '../../navigation/helpContexts';
import { Checkbox } from '../common/Checkbox';
import {
    PlanningWorkflowHelpContent,
} from '../planning/PlanningWorkflowGuide';
import { SettingsGoalHelpContent } from '../settings/SettingsGoalHelpContent';
import { TaskWorkflowHelpContent } from '../tasks/TaskWorkflowGuide';
import { SlideOverDrawer } from '../ui';
import { openCommandMenu } from './commandMenuEvents';

const PROVIDER_COPY_KEYS: Record<
    Exclude<HelpContentProvider, 'workspace'>,
    { title: string; summary: string }
> = {
    plan: {
        title: 'plan.help.title',
        summary: 'plan.help.summary',
    },
    gantt: {
        title: 'gantt.help.title',
        summary: 'gantt.help.summary',
    },
    tasks: {
        title: 'tasks.guide.title',
        summary: 'tasks.guide.summary',
    },
    settings: {
        title: 'settingsPage.goalGuide.title',
        summary: 'settingsPage.goalGuide.description',
    },
};

const TASK_SHORTCUTS = [
    { key: 'N', labelKey: 'commandMenu.commands.newTask.label' },
    { key: 'F', labelKey: 'commandMenu.commands.filters.label' },
    { key: 'R', labelKey: 'commandMenu.commands.reorder.label' },
    { key: 'B', labelKey: 'commandMenu.commands.bulkEdit.label' },
    { key: 'M', labelKey: 'commandMenu.commands.merge.label' },
] as const;

export const ContextHelp = () => {
    const { t } = useTranslation();
    const location = useLocation();
    const shortcutDescriptionId = useId();
    const [open, setOpen] = useState(false);
    const {
        enabled: singleKeyShortcutsEnabled,
        setEnabled: setSingleKeyShortcutsEnabled,
    } = useSingleKeyShortcutPreference();
    const helpContext = getHelpContext(location.pathname);
    const showTaskShortcuts = helpContext.provider === 'tasks';
    const pageTitle = t(helpContext.pageTitleKey);
    const workspaceTitle = t(
        helpContext.workspace.labelKey,
        helpContext.workspace.defaultLabel,
    );
    const providerCopy = helpContext.provider === 'workspace'
        ? {
            title: t(`contextHelp.workspaceGuides.${helpContext.workspace.key}.title`),
            summary: t(`contextHelp.workspaceGuides.${helpContext.workspace.key}.summary`),
        }
        : {
            title: t(PROVIDER_COPY_KEYS[helpContext.provider].title),
            summary: t(PROVIDER_COPY_KEYS[helpContext.provider].summary),
        };

    const closeForNavigation = () => {
        setOpen(false);
        if (typeof window === 'undefined') return;
        window.setTimeout(() => {
            document.getElementById('workspace-main')?.focus();
        }, 0);
    };

    const openCommands = () => {
        setOpen(false);
        if (typeof window === 'undefined') return;
        window.setTimeout(openCommandMenu, 0);
    };

    const workflowContent = (() => {
        if (helpContext.provider === 'plan') {
            return <PlanningWorkflowHelpContent surface="plan" showAction={false} />;
        }
        if (helpContext.provider === 'gantt') {
            return <PlanningWorkflowHelpContent surface="gantt" showAction={false} />;
        }
        if (helpContext.provider === 'tasks') {
            return <TaskWorkflowHelpContent showAction={false} />;
        }
        if (helpContext.provider === 'settings') {
            return <SettingsGoalHelpContent onNavigate={closeForNavigation} />;
        }

        const WorkspaceIcon = helpContext.workspace.icon;
        return (
            <div className="context-help-workspace-note">
                <span aria-hidden="true">
                    <WorkspaceIcon className="h-4 w-4" />
                </span>
                <p>
                    {t(`contextHelp.workspaceGuides.${helpContext.workspace.key}.hint`, {
                        workspace: workspaceTitle,
                    })}
                </p>
            </div>
        );
    })();

    return (
        <>
            <button
                type="button"
                className="context-help-trigger"
                aria-label={t('contextHelp.openForPage', { page: pageTitle })}
                aria-expanded={open}
                aria-haspopup="dialog"
                onClick={() => setOpen(true)}
            >
                <CircleHelp aria-hidden="true" className="h-4 w-4" />
                <span className="context-help-trigger-label">{t('contextHelp.trigger')}</span>
            </button>
            <SlideOverDrawer
                open={open}
                title={t('contextHelp.title')}
                subtitle={t('contextHelp.subtitle', { page: pageTitle })}
                icon={<CircleHelp aria-hidden="true" className="h-4 w-4" />}
                onClose={() => setOpen(false)}
                className="context-help-drawer"
            >
                <div className="context-help-content">
                    <section
                        className="context-help-section context-help-current"
                        aria-labelledby="context-help-workflow-heading"
                    >
                        <header>
                            <span>{t('contextHelp.currentWorkflow', { page: pageTitle })}</span>
                            <h4 id="context-help-workflow-heading">{providerCopy.title}</h4>
                            <p>{providerCopy.summary}</p>
                        </header>
                        <div className="context-help-provider">
                            {workflowContent}
                        </div>
                    </section>

                    <section
                        className="context-help-section"
                        aria-labelledby="context-help-shortcuts-heading"
                    >
                        <header>
                            <span>{t('contextHelp.expertPath')}</span>
                            <h4 id="context-help-shortcuts-heading">{t('contextHelp.shortcuts.title')}</h4>
                            <p>{t(showTaskShortcuts
                                ? 'contextHelp.shortcuts.description'
                                : 'contextHelp.shortcuts.globalDescription')}</p>
                        </header>

                        <div className="context-help-global-shortcuts">
                            <button type="button" onClick={openCommands}>
                                <span className="context-help-shortcut-icon" aria-hidden="true">
                                    <Command className="h-4 w-4" />
                                </span>
                                <span>
                                    <strong>{t('commandMenu.triggerLabel')}</strong>
                                    <span>{t('contextHelp.shortcuts.commandsBody')}</span>
                                </span>
                                <kbd>{t('commandMenu.openShortcut')}</kbd>
                            </button>
                            <div>
                                <span className="context-help-shortcut-icon" aria-hidden="true">
                                    <ArrowDownUp className="h-4 w-4" />
                                </span>
                                <span>
                                    <strong>{t('contextHelp.shortcuts.reviewCommands')}</strong>
                                    <span>{t('contextHelp.shortcuts.reviewCommandsBody')}</span>
                                </span>
                                <span className="context-help-key-pair" aria-hidden="true">
                                    <kbd>↑↓</kbd>
                                    <kbd><CornerDownLeft className="h-3 w-3" /></kbd>
                                </span>
                            </div>
                        </div>

                        {showTaskShortcuts && (
                            <div className="context-help-task-shortcuts">
                                <div className="context-help-task-shortcuts-head">
                                    <span>
                                        <Keyboard aria-hidden="true" className="h-4 w-4" />
                                        <strong>{t('contextHelp.shortcuts.taskKeys')}</strong>
                                    </span>
                                    <span
                                        className="context-help-shortcut-status"
                                        data-enabled={singleKeyShortcutsEnabled || undefined}
                                    >
                                        {t(singleKeyShortcutsEnabled
                                            ? 'contextHelp.shortcuts.enabled'
                                            : 'contextHelp.shortcuts.disabled')}
                                    </span>
                                </div>
                                <ul aria-label={t('contextHelp.shortcuts.taskKeys')}>
                                    {TASK_SHORTCUTS.map(shortcut => (
                                        <li key={shortcut.key}>
                                            <kbd>{shortcut.key}</kbd>
                                            <span>{t(shortcut.labelKey)}</span>
                                        </li>
                                    ))}
                                </ul>
                                <Checkbox
                                    checked={singleKeyShortcutsEnabled}
                                    onChange={setSingleKeyShortcutsEnabled}
                                    label={t('commandMenu.singleKeyShortcuts.label')}
                                    aria-describedby={shortcutDescriptionId}
                                />
                                <p id={shortcutDescriptionId}>
                                    {t('commandMenu.singleKeyShortcuts.description')}
                                </p>
                            </div>
                        )}
                    </section>

                    <section
                        className="context-help-section"
                        aria-labelledby="context-help-related-heading"
                    >
                        <header>
                            <span>{workspaceTitle}</span>
                            <h4 id="context-help-related-heading">{t('contextHelp.related.title')}</h4>
                            <p>{t('contextHelp.related.description')}</p>
                        </header>
                        <nav
                            className="context-help-related-links"
                            aria-label={t('contextHelp.related.navigationLabel')}
                        >
                            {helpContext.relatedLinks.map(link => (
                                <Link
                                    key={link.to}
                                    to={link.to}
                                    onClick={closeForNavigation}
                                >
                                    <span>
                                        <strong>
                                            {t('contextHelp.related.openDestination', {
                                                destination: t(link.labelKey, link.defaultLabel),
                                            })}
                                        </strong>
                                        {link.descriptionKey && (
                                            <span>{t(link.descriptionKey)}</span>
                                        )}
                                    </span>
                                    <ChevronRight aria-hidden="true" className="h-4 w-4" />
                                </Link>
                            ))}
                        </nav>
                    </section>
                </div>
            </SlideOverDrawer>
        </>
    );
};

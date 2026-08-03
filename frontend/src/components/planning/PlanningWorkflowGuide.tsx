import { useState } from 'react';
import {
    CalendarClock,
    ChevronRight,
    CircleHelp,
    FlaskConical,
    History,
    ListChecks,
    LockKeyhole,
    Share2,
} from 'lucide-react';
import type { LucideIcon } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import { Button } from '../common/Button';
import { SlideOverDrawer } from '../ui/SlideOverDrawer';

type PlanningSurface = 'plan' | 'gantt';

type GuideItem = {
    icon: LucideIcon;
    title: string;
    body: string;
};

export const PlanningWorkflowGuide = ({ surface }: { surface: PlanningSurface }) => {
    const { t } = useTranslation();
    const [open, setOpen] = useState(false);
    const translationPrefix = `${surface}.help`;
    const items: GuideItem[] = surface === 'plan'
        ? [
            {
                icon: ListChecks,
                title: t(`${translationPrefix}.readinessTitle`),
                body: t(`${translationPrefix}.readinessBody`),
            },
            {
                icon: LockKeyhole,
                title: t(`${translationPrefix}.blockedTitle`),
                body: t(`${translationPrefix}.blockedBody`),
            },
            {
                icon: Share2,
                title: t(`${translationPrefix}.shareTitle`),
                body: t(`${translationPrefix}.shareBody`),
            },
        ]
        : [
            {
                icon: CalendarClock,
                title: t(`${translationPrefix}.savedTitle`),
                body: t(`${translationPrefix}.savedBody`),
            },
            {
                icon: FlaskConical,
                title: t(`${translationPrefix}.sandboxTitle`),
                body: t(`${translationPrefix}.sandboxBody`),
            },
            {
                icon: History,
                title: t(`${translationPrefix}.recoverTitle`),
                body: t(`${translationPrefix}.recoverBody`),
            },
        ];
    const destination = surface === 'plan' ? '/plan/master' : '/plan';
    const closeForNavigation = () => {
        setOpen(false);
        if (typeof window === 'undefined') return;
        window.setTimeout(() => {
            document.getElementById('workspace-main')?.focus();
        }, 0);
    };

    return (
        <>
            <Button
                type="button"
                variant="ghost"
                size="sm"
                className="planning-workflow-trigger gap-1.5"
                aria-expanded={open}
                aria-haspopup="dialog"
                onClick={() => setOpen(true)}
            >
                <CircleHelp aria-hidden="true" className="h-4 w-4" />
                <span>{t(`${translationPrefix}.trigger`)}</span>
            </Button>
            <SlideOverDrawer
                open={open}
                title={t(`${translationPrefix}.title`)}
                subtitle={t(`${translationPrefix}.summary`)}
                icon={<CircleHelp aria-hidden="true" className="h-4 w-4" />}
                onClose={() => setOpen(false)}
                className="planning-workflow-drawer"
            >
                <div className="planning-workflow-help">
                    <ul>
                        {items.map(({ icon: Icon, title, body }) => (
                            <li key={title}>
                                <span className="planning-workflow-help-icon">
                                    <Icon aria-hidden="true" className="h-4 w-4" />
                                </span>
                                <span>
                                    <strong>{title}</strong>
                                    <span>{body}</span>
                                </span>
                            </li>
                        ))}
                    </ul>
                    <Link
                        to={destination}
                        className="btn secondary sm"
                        onClick={closeForNavigation}
                    >
                        {t(`${translationPrefix}.action`)}
                        <ChevronRight aria-hidden="true" className="h-3.5 w-3.5" />
                    </Link>
                </div>
            </SlideOverDrawer>
        </>
    );
};

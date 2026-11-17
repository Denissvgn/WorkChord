import { ButtonLink } from '../common/ButtonLink';
import {
    CalendarClock,
    ChevronRight,
    FlaskConical,
    History,
    ListChecks,
    LockKeyhole,
    Share2,
} from 'lucide-react';
import type { LucideIcon } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { useScopeLink } from '../../features/scope/useScopeLink';

type PlanningSurface = 'plan' | 'gantt';

type GuideItem = {
    icon: LucideIcon;
    title: string;
    body: string;
};

export const PlanningWorkflowHelpContent = ({
    surface,
    showAction = true,
    onNavigate,
}: {
    surface: PlanningSurface;
    showAction?: boolean;
    onNavigate?: () => void;
}) => {
    const { t } = useTranslation();
    const scopeLink = useScopeLink();
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
    const destination = '/plan';

    return (
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
            {showAction && (
                <ButtonLink
                    to={scopeLink(destination)}

                    onClick={onNavigate}
                 variant="secondary" size="sm">
                    {t(`${translationPrefix}.action`)}
                    <ChevronRight aria-hidden="true" className="h-3.5 w-3.5" />
                </ButtonLink>
            )}
        </div>
    );
};


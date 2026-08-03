import { ArrowRight } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { Link, useSearchParams } from 'react-router-dom';

type SettingsGoalTab = 'scheduling' | 'github' | 'models_agents';

export const SettingsGoalHelpContent = ({
    onNavigate,
}: {
    onNavigate?: () => void;
}) => {
    const { t } = useTranslation();
    const [searchParams] = useSearchParams();
    const settingsHref = (tab: SettingsGoalTab) => {
        const nextParams = new URLSearchParams(searchParams);
        nextParams.set('tab', tab);
        return `/settings?${nextParams.toString()}`;
    };

    const goals = [
        {
            tab: 'scheduling',
            title: t('settingsPage.goalGuide.scheduleTitle'),
            body: t('settingsPage.goalGuide.scheduleBody'),
        },
        {
            tab: 'github',
            title: t('settingsPage.goalGuide.githubTitle'),
            body: t('settingsPage.goalGuide.githubBody'),
        },
        {
            tab: 'models_agents',
            title: t('settingsPage.goalGuide.agentsTitle'),
            body: t('settingsPage.goalGuide.agentsBody'),
        },
    ] as const;

    return (
        <nav className="settings-goal-help" aria-label={t('settingsPage.goalGuide.navigationLabel')}>
            {goals.map(goal => (
                <Link
                    key={goal.tab}
                    to={settingsHref(goal.tab)}
                    onClick={onNavigate}
                >
                    <span>
                        <strong>{goal.title}</strong>
                        <span>{goal.body}</span>
                    </span>
                    <ArrowRight aria-hidden="true" className="h-4 w-4" />
                </Link>
            ))}
        </nav>
    );
};

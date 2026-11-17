import { ButtonLink } from '../common/ButtonLink';
import {
    Bot,
    CalendarRange,
    CheckCircle2,
    ChevronRight,
    UserRoundCheck,
} from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { useScopeLink } from '../../features/scope/useScopeLink';

export const TaskWorkflowHelpContent = ({
    showAction = true,
    onNavigate,
}: {
    showAction?: boolean;
    onNavigate?: () => void;
}) => {
    const { t } = useTranslation();
    const scopeLink = useScopeLink();

    return (
        <div className="task-workflow-help">
            <section className="task-workflow-required">
                <h4>{t('tasks.guide.requiredTitle')}</h4>
                <p>{t('tasks.guide.description')}</p>
                <ol>
                    <li>
                        <span className="task-workflow-guide-step" aria-hidden="true">1</span>
                        <UserRoundCheck aria-hidden="true" className="h-4 w-4" />
                        <span>
                            <strong>{t('tasks.guide.defineTitle')}</strong>
                            <span>{t('tasks.guide.defineBody')}</span>
                        </span>
                    </li>
                    <li>
                        <span className="task-workflow-guide-step" aria-hidden="true">2</span>
                        <CheckCircle2 aria-hidden="true" className="h-4 w-4" />
                        <span>
                            <strong>{t('tasks.guide.readyTitle')}</strong>
                            <span>{t('tasks.guide.readyBody')}</span>
                        </span>
                    </li>
                    <li>
                        <span className="task-workflow-guide-step" aria-hidden="true">3</span>
                        <CalendarRange aria-hidden="true" className="h-4 w-4" />
                        <span>
                            <strong>{t('tasks.guide.scheduleTitle')}</strong>
                            <span>{t('tasks.guide.scheduleBody')}</span>
                        </span>
                    </li>
                </ol>
            </section>
            <section className="task-workflow-agent-branch">
                <Bot aria-hidden="true" className="h-4 w-4" />
                <div>
                    <h4>{t('tasks.guide.optionalAgentTitle')}</h4>
                    <p>{t('tasks.guide.optionalAgentBody')}</p>
                </div>
            </section>
            {showAction && (
                <ButtonLink
                    to={scopeLink('/plan')}

                    onClick={onNavigate}
                 variant="secondary" size="sm">
                    {t('tasks.guide.openPlanWork')}
                    <ChevronRight aria-hidden="true" className="h-3.5 w-3.5" />
                </ButtonLink>
            )}
        </div>
    );
};


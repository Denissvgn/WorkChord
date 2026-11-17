import type { ReactNode } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '../../components/common/Button';
import { InlineEmptyState } from '../../components/ui/InlineEmptyState';
import { useNextSetupAction, type NextAction } from './useNextSetupAction';

/**
 * An empty page or view: what appears here, and the one button that fills it. The button is the
 * next first-run step, or the page's own fallback once setup has no step left.
 */
export const NextStepEmptyState = ({ title, description, icon, className, fallback, onCreateProject, headingLevel = 2 }: {
    title?: ReactNode;
    description: ReactNode;
    icon?: ReactNode;
    className?: string;
    fallback: NextAction;
    onCreateProject?: () => void;
    headingLevel?: 2 | 3;
}) => {
    const action = useNextSetupAction({ fallback, onCreateProject });
    return (
        <InlineEmptyState
            icon={icon}
            title={title}
            description={description}
            className={className}
            headingLevel={headingLevel}
            actions={'to' in action ? (
                <Link className="btn primary" to={action.to}>{action.label}</Link>
            ) : (
                <Button variant="primary" onClick={action.onClick}>{action.label}</Button>
            )}
        />
    );
};

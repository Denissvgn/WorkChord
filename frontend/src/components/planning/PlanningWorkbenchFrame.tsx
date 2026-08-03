import type { ReactNode } from 'react';
import clsx from 'clsx';
import { PageHeader, PageLayout } from '../ui';
import { PlanReturnBar } from './PlanReturnBar';

export type PlanningWorkbenchFact = {
    id: string;
    label: ReactNode;
    value: ReactNode;
};

type PlanningWorkbenchFrameProps = {
    title: ReactNode;
    description?: ReactNode;
    facts?: PlanningWorkbenchFact[];
    contextControl?: ReactNode;
    secondaryActions?: ReactNode;
    primaryAction?: ReactNode;
    overflowAction?: ReactNode;
    state?: ReactNode;
    children: ReactNode;
    variant?: 'default' | 'wide' | 'workbench';
    className?: string;
    headerClassName?: string;
    canvasClassName?: string;
    testId?: string;
};

const PlanningWorkbenchFacts = ({ facts }: { facts: PlanningWorkbenchFact[] }) => (
    <dl className="planning-workbench-facts">
        {facts.map(fact => (
            <div key={fact.id} className="planning-workbench-fact">
                <dt>{fact.label}</dt>
                <dd>{fact.value}</dd>
            </div>
        ))}
    </dl>
);

export const PlanningWorkbenchFrame = ({
    title,
    description,
    facts = [],
    contextControl,
    secondaryActions,
    primaryAction,
    overflowAction,
    state,
    children,
    variant = 'default',
    className,
    headerClassName,
    canvasClassName,
    testId,
}: PlanningWorkbenchFrameProps) => {
    const hasActions = Boolean(contextControl || secondaryActions || primaryAction || overflowAction);

    return (
        <PageLayout
            variant={variant}
            className={clsx('planning-workbench-frame', className)}
            testId={testId}
        >
            <PlanReturnBar />
            <PageHeader
                className={clsx('planning-workbench-header', headerClassName)}
                title={title}
                subtitle={description}
                meta={facts.length > 0 ? <PlanningWorkbenchFacts facts={facts} /> : undefined}
                actions={hasActions ? (
                    <div className="planning-workbench-action-row">
                        {contextControl && (
                            <div className="planning-workbench-context-control">
                                {contextControl}
                            </div>
                        )}
                        {secondaryActions && (
                            <div className="planning-workbench-secondary-actions">
                                {secondaryActions}
                            </div>
                        )}
                        {primaryAction && (
                            <div className="planning-workbench-primary-action">
                                {primaryAction}
                            </div>
                        )}
                        {overflowAction && (
                            <div className="planning-workbench-overflow-action">
                                {overflowAction}
                            </div>
                        )}
                    </div>
                ) : undefined}
            />
            {state && (
                <div className="planning-workbench-state-region">
                    {state}
                </div>
            )}
            <div className={clsx('planning-workbench-canvas', canvasClassName)}>
                {children}
            </div>
        </PageLayout>
    );
};

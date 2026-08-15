import type { ReactNode } from 'react';
import clsx from 'clsx';

type PageLayoutProps = {
    children: ReactNode;
    variant?: 'default' | 'wide' | 'workbench';
    className?: string;
    testId?: string;
};

export const PageLayout = ({ children, variant = 'default', className, testId }: PageLayoutProps) => (
    <div
        className={clsx(
            variant === 'workbench' ? 'wc-workbench' : variant === 'wide' ? 'wc-page-wide' : 'wc-page',
            'wc-page-stack',
            className,
        )}
        data-testid={testId}
    >
        {children}
    </div>
);

type PageHeaderProps = {
    title: ReactNode;
    subtitle?: ReactNode;
    meta?: ReactNode;
    actions?: ReactNode;
    className?: string;
};

export const PageHeader = ({ title, subtitle, meta, actions, className }: PageHeaderProps) => (
    <div className={clsx('wc-page-head', className)} data-testid="page-header">
        <div className="wc-page-copy">
            <h1 className="wc-page-title">{title}</h1>
            {subtitle && <div className="wc-page-sub">{subtitle}</div>}
            {meta && <div className="wc-page-meta">{meta}</div>}
        </div>
        {actions && <PageActions>{actions}</PageActions>}
    </div>
);

export const PageActions = ({ children, className }: { children: ReactNode; className?: string }) => (
    <div className={clsx('wc-page-actions', className)}>{children}</div>
);

export const Toolbar = ({ children, className }: { children: ReactNode; className?: string }) => (
    <div className={clsx('wc-toolbar', className)}>{children}</div>
);

export const ActionGroup = ({ children, className }: { children: ReactNode; className?: string }) => (
    <div className={clsx('wc-action-group', className)}>{children}</div>
);

export const FormGrid = ({ children, className }: { children: ReactNode; className?: string }) => (
    <div className={clsx('wc-form-grid', className)}>{children}</div>
);

export const InlineField = ({
    label,
    children,
    hint,
    className,
}: {
    label: ReactNode;
    children: ReactNode;
    hint?: ReactNode;
    className?: string;
}) => (
    <label className={clsx('field', className)}>
        <span className="field-lbl">{label}</span>
        {children}
        {hint && <span className="field-hint">{hint}</span>}
    </label>
);

export const MetricGrid = ({ children, columns = 4, className }: { children: ReactNode; columns?: 3 | 4 | 5 | 6; className?: string }) => (
    <div className={clsx('kpi-grid', `kpi-grid-${columns}`, className)}>{children}</div>
);

export const TableFrame = ({ children, className }: { children: ReactNode; className?: string }) => (
    <div className={clsx('wc-table-frame', className)}>{children}</div>
);

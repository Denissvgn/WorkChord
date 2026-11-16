import { Children, Fragment, cloneElement, isValidElement } from 'react';
import type { ReactNode } from 'react';
import clsx from 'clsx';
import { OverflowMenu, type OverflowMenuItem } from './OverflowMenu';

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
    /** One sentence saying what the page is for. */
    purpose?: ReactNode;
    /** The one action the page leads with. A second one is refused in development. */
    primaryAction?: ReactNode;
    /** Up to two supporting actions. */
    secondaryActions?: ReactNode;
    /** Every further page-level action, shown in one overflow menu. */
    overflowItems?: OverflowMenuItem[];
    /** A control that sets the scope of the page, placed before the actions. */
    context?: ReactNode;
    /** Pre-built overflow control, for callers that already own the menu. */
    overflow?: ReactNode;
    meta?: ReactNode;
    className?: string;
    /** @deprecated Use `purpose`. */
    subtitle?: ReactNode;
    /** @deprecated Use `primaryAction`, `secondaryActions` and `overflowItems`. */
    actions?: ReactNode;
    /**
     * Compatibility path for pages that have not moved to the action limits yet:
     * the primary and secondary slots are rendered exactly as given, with no
     * count and no truncation. New pages must not set it.
     */
    unlimitedActions?: boolean;
};

const MAX_SECONDARY_ACTIONS = 2;

/**
 * Splits a slot into its elements so the number of actions can be counted.
 * Fragments are opened, so wrapping actions in `<>…</>` does not hide them.
 */
const slotItems = (slot: ReactNode, prefix = ''): ReactNode[] =>
    Children.toArray(slot).flatMap(item => {
        if (!isValidElement<{ children?: ReactNode }>(item)) return [item];
        const key = `${prefix}${item.key ?? ''}`;
        if (item.type === Fragment) return slotItems(item.props.children, `${key}/`);
        return [cloneElement(item, { key })];
    });

/**
 * The header every page opens with.
 *
 * Usage: pass `title` and one sentence of `purpose`. Put the single most
 * important action in `primaryAction`, up to two supporting ones in
 * `secondaryActions`, and everything else in `overflowItems`. A second primary
 * action, or a third secondary one, logs an error in development and is not
 * rendered.
 */
export const PageHeader = ({
    title,
    purpose,
    subtitle,
    primaryAction,
    secondaryActions,
    overflowItems,
    overflow,
    context,
    meta,
    actions,
    unlimitedActions = false,
    className,
}: PageHeaderProps) => {
    const primaryItems = slotItems(primaryAction);
    const secondaryItems = slotItems(secondaryActions);
    if (import.meta.env.DEV && !unlimitedActions) {
        if (primaryItems.length > 1) {
            console.error(`PageHeader accepts one primary action but received ${primaryItems.length}.`);
        }
        if (secondaryItems.length > MAX_SECONDARY_ACTIONS) {
            console.error(`PageHeader accepts at most ${MAX_SECONDARY_ACTIONS} secondary actions but received ${secondaryItems.length}.`);
        }
    }
    const primary = unlimitedActions ? primaryItems : primaryItems.slice(0, 1);
    const secondary = unlimitedActions ? secondaryItems : secondaryItems.slice(0, MAX_SECONDARY_ACTIONS);
    const menu = overflowItems && overflowItems.length > 0 ? <OverflowMenu items={overflowItems} /> : overflow;
    const sentence = purpose ?? subtitle;
    const hasActions = Boolean(context || primary.length || secondary.length || menu || actions);

    return (
        <div className={clsx('wc-page-head', className)} data-testid="page-header">
            <div className="wc-page-copy">
                <h1 className="wc-page-title">{title}</h1>
                {sentence && <div className="wc-page-sub">{sentence}</div>}
                {meta && <div className="wc-page-meta">{meta}</div>}
            </div>
            {hasActions && (
                <PageActions>
                    {context && <div className="wc-page-context">{context}</div>}
                    {secondary.length > 0 && <div className="wc-page-secondary">{secondary}</div>}
                    {primary.length > 0 && <div className="wc-page-primary">{primary}</div>}
                    {menu && <div className="wc-page-overflow">{menu}</div>}
                    {actions}
                </PageActions>
            )}
        </div>
    );
};

export const PageActions = ({ children, className }: { children: ReactNode; className?: string }) => (
    <div className={clsx('wc-page-actions', className)}>{children}</div>
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

export const TableFrame = ({ children, className }: { children: ReactNode; className?: string }) => (
    <div className={clsx('wc-table-frame', className)}>{children}</div>
);

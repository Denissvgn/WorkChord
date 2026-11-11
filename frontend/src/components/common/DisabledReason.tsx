import clsx from 'clsx';

/** Says, next to a disabled button, what would enable it. Renders nothing when there is no reason. */
export const DisabledReason = ({ reason, className }: { reason?: string | null | false; className?: string }) => (
    reason ? <p className={clsx('text-xs text-content-secondary', className)}>{reason}</p> : null
);

import i18n from '../../i18n/i18n';
import { useState, useRef, useEffect, useCallback } from 'react';
import { createPortal } from 'react-dom';
import { useLocation } from 'react-router-dom';
import { AlertTriangle, Bot, CheckCircle2, XCircle } from 'lucide-react';
import clsx from 'clsx';
import type { TaskAgentReadiness } from '../../types/task';

const t = i18n.t.bind(i18n);

interface TaskAgentReadinessBadgeProps {
    readiness: TaskAgentReadiness;
    mode?: 'compact' | 'panel';
}

export const TaskAgentReadinessBadge = ({ readiness, mode = 'compact' }: TaskAgentReadinessBadgeProps) => {
    const [isOpen, setIsOpen] = useState(false);
    const triggerRef = useRef<HTMLButtonElement>(null);
    const panelRef = useRef<HTMLDivElement>(null);
    const [panelPosition, setPanelPosition] = useState({ left: 0, top: 0 });

    const location = useLocation();

    useEffect(() => {
        // eslint-disable-next-line react-hooks/set-state-in-effect
        setIsOpen(false);
    }, [location]);

    const updatePosition = useCallback(() => {
        const trigger = triggerRef.current;
        if (!trigger) return;
        const rect = trigger.getBoundingClientRect();
        const menuWidth = 320; // w-80 is 320px
        const viewportMargin = 8;
        const preferredLeft = rect.left;
        const maxLeft = Math.max(viewportMargin, window.innerWidth - menuWidth - viewportMargin);
        const left = Math.min(Math.max(viewportMargin, preferredLeft), maxLeft);

        let top = rect.bottom + viewportMargin;
        const approxHeight = 250;
        if (top + approxHeight > window.innerHeight && rect.top - approxHeight > viewportMargin) {
            top = rect.top - approxHeight - viewportMargin;
        }
        setPanelPosition({ left, top });
    }, []);

    useEffect(() => {
        if (isOpen) {
            updatePosition();
        }
    }, [isOpen, updatePosition]);

    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            const target = event.target as Node;
            if (triggerRef.current?.contains(target) || panelRef.current?.contains(target)) {
                return;
            }
            setIsOpen(false);
        };

        const handleKeyDown = (event: KeyboardEvent) => {
            if (event.key === 'Escape') {
                setIsOpen(false);
                triggerRef.current?.focus();
            }
        };

        if (isOpen) {
            document.addEventListener('mousedown', handleClickOutside);
            document.addEventListener('keydown', handleKeyDown);
            window.addEventListener('resize', updatePosition);
            window.addEventListener('scroll', updatePosition, true);
        }
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
            document.removeEventListener('keydown', handleKeyDown);
            window.removeEventListener('resize', updatePosition);
            window.removeEventListener('scroll', updatePosition, true);
        };
    }, [isOpen, updatePosition]);

    const badgeClassName = readiness.is_ready
        ? 'border-feedback-success-border bg-feedback-success-muted text-feedback-success-foreground hover:bg-feedback-success-muted-hover'
        : 'border-feedback-warning-border bg-feedback-warning-muted text-feedback-warning-foreground hover:bg-feedback-warning-muted-hover';
    const Icon = readiness.is_ready ? CheckCircle2 : AlertTriangle;
    const label = t(readiness.is_ready ? 'surfaces.taskReadiness.ready' : 'surfaces.taskReadiness.notReady');

    const details = (
        <div className="space-y-2 text-xs">
            {readiness.blockers.length > 0 && (
                <div>
                    <p className="font-semibold text-feedback-warning-foreground">{t('surfaces.taskReadiness.blockers')}</p>
                    <ul className="mt-1 space-y-1 text-feedback-warning-foreground">
                        {readiness.blockers.map((blocker, index) => (
                            <li key={`${index}-${blocker}`} className="flex gap-1.5">
                                <span aria-hidden="true">-</span>
                                <span className="text-left">{blocker}</span>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
            {readiness.warnings.length > 0 && (
                <div>
                    <p className="font-semibold text-content-primary">{t('surfaces.taskReadiness.warnings')}</p>
                    <ul className="mt-1 space-y-1 text-content-secondary">
                        {readiness.warnings.map((warning, index) => (
                            <li key={`${index}-${warning}`} className="flex gap-1.5">
                                <span aria-hidden="true">-</span>
                                <span className="text-left">{warning}</span>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
            <div className="grid gap-1 pt-1 border-t border-border-subtle">
                {readiness.criteria.map(criterion => (
                    <div key={criterion.key} className="flex items-start gap-2">
                        {criterion.passed ? (
                            <CheckCircle2 className="mt-0.5 h-3.5 w-3.5 flex-shrink-0 text-feedback-success" />
                        ) : (
                            <XCircle className="mt-0.5 h-3.5 w-3.5 flex-shrink-0 text-feedback-warning" />
                        )}
                        <div className="min-w-0">
                            <p className="font-medium text-content-primary text-left truncate">{criterion.label}</p>
                            <p className="text-content-secondary text-left text-[10px] leading-snug">{criterion.reason}</p>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );

    if (mode === 'panel') {
        return (
            <section className={clsx('rounded-md border p-3', badgeClassName)}>
                <div className="mb-2 flex items-center gap-2 text-sm font-semibold">
                    <Bot className="h-4 w-4" />
                    <span>{label}</span>
                </div>
                {details}
            </section>
        );
    }

    return (
        <>
            <button
                ref={triggerRef}
                type="button"
                onClick={(e) => {
                    e.stopPropagation();
                    e.preventDefault();
                    setIsOpen(!isOpen);
                }}
                aria-expanded={isOpen}
                className={clsx('flex items-center rounded-full border px-2 py-0.5 text-xs font-medium focus:outline-none focus:ring-2 focus:ring-focus focus:ring-offset-1', badgeClassName)}
            >
                <Icon className="mr-1 h-3 w-3" />
                {label}
            </button>
            {isOpen && typeof document !== 'undefined' && createPortal(
                <div
                    ref={panelRef}
                    className="fixed w-80 rounded-md border border-border bg-surface-card p-3 shadow-lg z-[100] animate-in fade-in slide-in-from-top-1 text-left"
                    style={{ left: panelPosition.left, top: panelPosition.top }}
                >
                    {details}
                </div>,
                document.body
            )}
        </>
    );
};

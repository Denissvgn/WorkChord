import type { TaskStatus } from '../../types/task';

export type PillTone = 'gray' | 'blue' | 'green' | 'yellow' | 'red' | 'purple' | 'indigo';

// ── Planning-masters design-system mappings ──────────────────────────────────
// The WorkChord system has 5 semantic pill variants: default(opt) / accent / done / warn / blocked.
// Map the legacy 7-tone palette onto them.

/** WorkChord `.pill` modifier class for a tone (used as `pill ${wcPillClass[tone]}`). */
export const wcPillClass: Record<PillTone, string> = {
    gray: 'opt',
    blue: 'accent',
    green: 'done',
    yellow: 'warn',
    red: 'blocked',
    purple: 'accent',
    indigo: 'accent',
};

/** CSS variable carrying the tone's primary colour (for dots, bars, rings). */
export const toneVar: Record<PillTone, string> = {
    gray: 'var(--ink-4)',
    blue: 'var(--accent)',
    green: 'var(--done)',
    yellow: 'var(--warn)',
    red: 'var(--blocked)',
    purple: 'var(--accent)',
    indigo: 'var(--accent)',
};

/** CSS variable for the tone's soft background tint. */
export const toneSoftVar: Record<PillTone, string> = {
    gray: 'var(--panel-2)',
    blue: 'var(--accent-soft)',
    green: 'var(--done-soft)',
    yellow: 'var(--warn-soft)',
    red: 'var(--blocked-soft)',
    purple: 'var(--accent-soft)',
    indigo: 'var(--accent-soft)',
};

/** CSS variable for the tone's border/line colour. */
export const toneLineVar: Record<PillTone, string> = {
    gray: 'var(--border-2)',
    blue: 'var(--accent-line)',
    green: 'var(--done-line)',
    yellow: 'var(--warn-line)',
    red: 'var(--blocked-line)',
    purple: 'var(--accent-line)',
    indigo: 'var(--accent-line)',
};

export const STATUS_TONE: Record<TaskStatus, PillTone> = {
    planned: 'gray',
    active: 'blue',
    resolved: 'green',
    closed: 'purple',
};

export const isTaskStatus = (value: string): value is TaskStatus => value in STATUS_TONE;

export const pillToneClassName: Record<PillTone, string> = {
    gray: 'bg-status-planned-muted text-status-planned-foreground',
    blue: 'bg-status-active-muted text-status-active-foreground',
    green: 'bg-status-resolved-muted text-status-resolved-foreground',
    yellow: 'bg-feedback-warning-muted text-feedback-warning-foreground',
    red: 'bg-feedback-danger-muted text-feedback-danger-foreground',
    purple: 'bg-status-closed-muted text-status-closed-foreground',
    indigo: 'bg-feedback-indigo-muted text-feedback-indigo-foreground',
};

export const toneBorderClassName: Record<PillTone, string> = {
    gray: 'border-status-planned-border bg-status-planned-muted text-status-planned-foreground',
    blue: 'border-status-active-border bg-status-active-muted text-status-active-foreground',
    green: 'border-status-resolved-border bg-status-resolved-muted text-status-resolved-foreground',
    yellow: 'border-feedback-warning-border bg-feedback-warning-muted text-feedback-warning-foreground',
    red: 'border-feedback-danger-border bg-feedback-danger-muted text-feedback-danger-foreground',
    purple: 'border-status-closed-border bg-status-closed-muted text-status-closed-foreground',
    indigo: 'border-feedback-indigo-border bg-feedback-indigo-muted text-feedback-indigo-foreground',
};

export const toneDotClassName: Record<PillTone, string> = {
    gray: 'bg-status-planned',
    blue: 'bg-status-active',
    green: 'bg-status-resolved',
    yellow: 'bg-feedback-warning',
    red: 'bg-feedback-danger',
    purple: 'bg-status-closed',
    indigo: 'bg-feedback-indigo',
};

export const toneGradientClassName: Record<PillTone, string> = {
    gray: 'from-status-planned/70 to-status-active/70',
    blue: 'from-status-active/70 to-feedback-indigo/70',
    green: 'from-status-resolved/70 to-status-active/70',
    yellow: 'from-feedback-warning/70 to-feedback-info/70',
    red: 'from-feedback-danger/70 to-feedback-info/70',
    purple: 'from-status-closed/70 to-status-active/70',
    indigo: 'from-feedback-indigo/70 to-feedback-info/70',
};

export const toneSolidClassName: Record<PillTone, string> = {
    gray: 'bg-status-planned text-status-planned-emphasis',
    blue: 'bg-status-active text-status-active-emphasis',
    green: 'bg-status-resolved text-status-resolved-emphasis',
    yellow: 'bg-feedback-warning text-feedback-warning-emphasis',
    red: 'bg-feedback-danger text-feedback-danger-emphasis',
    purple: 'bg-status-closed text-status-closed-emphasis',
    indigo: 'bg-feedback-indigo text-feedback-indigo-emphasis',
};

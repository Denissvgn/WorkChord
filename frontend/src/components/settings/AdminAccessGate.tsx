import { useId, useState } from 'react';
import type { ReactNode } from 'react';
import { LockKeyhole } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { useAdminAccess, useKeylessReader } from '../../hooks/useAdminAccess';
import { Button } from '../common/Button';
import { AdminAccessPanel } from './AdminAccessPanel';
import { SettingsReadOnlyContext, useSharedUnlock } from './sharedUnlock';

interface AdminAccessGateProps {
    children: ReactNode;
    showPanel?: boolean;
    recovery?: ReactNode;
    accessGranted?: boolean;
    headingLevel?: 2 | 3;
    /** Show the panel read-only to people who may read it without the key, instead of the gate. */
    readable?: boolean;
    /**
     * The content disables its own editing controls through `useSettingsReadOnly`, so that its
     * view controls (tabs, type lists, filters, expanders) stay usable when it is read-only.
     * Without it, every control inside is disabled.
     */
    managesReadOnly?: boolean;
}

export const AdminAccessGate = ({
    children,
    showPanel = true,
    recovery,
    accessGranted,
    headingLevel = 3,
    readable = false,
    managesReadOnly = false,
}: AdminAccessGateProps) => {
    const { t } = useTranslation();
    const { hasAdminKey } = useAdminAccess();
    const reader = useKeylessReader();
    const shared = useSharedUnlock();
    const hasAccess = accessGranted ?? hasAdminKey;
    const Heading = headingLevel === 2 ? 'h2' : 'h3';

    if (hasAccess) {
        // Same root as the read-only content, so unlocking keeps the panel's own state (open tab, filters).
        return <SettingsReadOnlyContext.Provider value={null}>{children}</SettingsReadOnlyContext.Provider>;
    }
    if (readable && reader.settings) {
        if (shared) {
            // The page's own Unlock editing control serves this section.
            return readOnlyContent(children, shared.noteId, managesReadOnly);
        }
        return <ReadOnlySettings headingLevel={headingLevel} managesReadOnly={managesReadOnly}>{children}</ReadOnlySettings>;
    }
    if (shared) {
        return (
            <div className="card card-pad max-w-3xl">
                <div className="admin-access-gate">
                    <div className="iconbox warn">
                        <LockKeyhole aria-hidden="true" className="h-4 w-4" />
                    </div>
                    <div className="admin-access-gate-copy">
                        <Heading>{t('settings.adminAccessProtectedTitle')}</Heading>
                        <p>{t('settings.sharedUnlockProtectedDescription')}</p>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="wc-panel-stack max-w-3xl">
            <div className="card card-pad">
                <div className="admin-access-gate">
                    <div className="iconbox warn">
                        <LockKeyhole aria-hidden="true" className="h-4 w-4" />
                    </div>
                    <div className="admin-access-gate-copy">
                        <Heading>
                            {t('settings.adminAccessProtectedTitle')}
                        </Heading>
                        <p>
                            {t('settings.adminAccessProtectedDescription')}
                        </p>
                        {recovery && <div className="mt-3">{recovery}</div>}
                    </div>
                </div>
            </div>
            {showPanel && <AdminAccessPanel headingLevel={headingLevel} />}
        </div>
    );
};

/**
 * Content that can be read but not changed: either it disables its own editing controls, or all
 * of them are. A plain function, not a component, so its root is the same Provider as the unlocked
 * content's and React keeps the content mounted when the key is entered.
 */
const readOnlyContent = (children: ReactNode, noteId: string, managesReadOnly: boolean) => (
    <SettingsReadOnlyContext.Provider value={{ noteId }}>
        {managesReadOnly ? children : (
            <fieldset disabled aria-describedby={noteId} className="m-0 min-w-0 border-0 p-0">
                {children}
            </fieldset>
        )}
    </SettingsReadOnlyContext.Provider>
);

/** The panel stays readable; its controls are disabled until the admin key is entered in place. */
const ReadOnlySettings = ({ children, headingLevel, managesReadOnly }: { children: ReactNode; headingLevel: 2 | 3; managesReadOnly: boolean }) => {
    const { t } = useTranslation();
    const id = useId();
    const [unlocking, setUnlocking] = useState(false);
    return (
        <div className="wc-panel-stack">
            <div className="flex flex-wrap items-center gap-3 rounded-md border border-border bg-surface-muted px-4 py-3 text-sm">
                <LockKeyhole aria-hidden="true" className="h-4 w-4 shrink-0" />
                <p id={`${id}-note`} className="min-w-0 flex-1">
                    <strong>{t('settings.readOnlyTitle')}</strong> · {t('settings.readOnlyBody')}
                </p>
                <Button type="button" size="sm" variant="secondary" aria-expanded={unlocking} aria-controls={`${id}-unlock`}
                    onClick={() => setUnlocking(value => !value)}>{t('settings.unlockEditing')}</Button>
            </div>
            {unlocking && <div id={`${id}-unlock`}><AdminAccessPanel headingLevel={headingLevel} /></div>}
            {readOnlyContent(children, `${id}-note`, managesReadOnly)}
        </div>
    );
};

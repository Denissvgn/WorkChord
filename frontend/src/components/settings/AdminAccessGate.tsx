import { useId, useState } from 'react';
import type { ReactNode } from 'react';
import { LockKeyhole } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { useAdminAccess, useKeylessReader } from '../../hooks/useAdminAccess';
import { Button } from '../common/Button';
import { AdminAccessPanel } from './AdminAccessPanel';

interface AdminAccessGateProps {
    children: ReactNode;
    showPanel?: boolean;
    recovery?: ReactNode;
    accessGranted?: boolean;
    headingLevel?: 2 | 3;
    /** Show the panel read-only to people who may read it without the key, instead of the gate. */
    readable?: boolean;
}

export const AdminAccessGate = ({
    children,
    showPanel = true,
    recovery,
    accessGranted,
    headingLevel = 3,
    readable = false,
}: AdminAccessGateProps) => {
    const { t } = useTranslation();
    const { hasAdminKey } = useAdminAccess();
    const reader = useKeylessReader();
    const hasAccess = accessGranted ?? hasAdminKey;
    const Heading = headingLevel === 2 ? 'h2' : 'h3';

    if (hasAccess) {
        return <>{children}</>;
    }
    if (readable && reader.settings) {
        return <ReadOnlySettings headingLevel={headingLevel}>{children}</ReadOnlySettings>;
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

/** The panel stays readable; its controls are disabled until the admin key is entered in place. */
const ReadOnlySettings = ({ children, headingLevel }: { children: ReactNode; headingLevel: 2 | 3 }) => {
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
            <fieldset disabled aria-describedby={`${id}-note`} className="m-0 min-w-0 border-0 p-0">
                {children}
            </fieldset>
        </div>
    );
};

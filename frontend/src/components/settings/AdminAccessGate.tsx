import type { ReactNode } from 'react';
import { LockKeyhole } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { useAdminAccess } from '../../hooks/useAdminAccess';
import { AdminAccessPanel } from './AdminAccessPanel';

interface AdminAccessGateProps {
    children: ReactNode;
    showPanel?: boolean;
    recovery?: ReactNode;
    accessGranted?: boolean;
    headingLevel?: 2 | 3;
}

export const AdminAccessGate = ({
    children,
    showPanel = true,
    recovery,
    accessGranted,
    headingLevel = 3,
}: AdminAccessGateProps) => {
    const { t } = useTranslation();
    const { hasAdminKey } = useAdminAccess();
    const hasAccess = accessGranted ?? hasAdminKey;
    const Heading = headingLevel === 2 ? 'h2' : 'h3';

    if (hasAccess) {
        return <>{children}</>;
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

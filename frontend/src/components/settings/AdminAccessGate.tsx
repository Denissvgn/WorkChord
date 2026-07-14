import type { ReactNode } from 'react';
import { LockKeyhole } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { useAdminAccess } from '../../hooks/useAdminAccess';
import { AdminAccessPanel } from './AdminAccessPanel';

interface AdminAccessGateProps {
    children: ReactNode;
    showPanel?: boolean;
}

export const AdminAccessGate = ({ children, showPanel = true }: AdminAccessGateProps) => {
    const { t } = useTranslation();
    const { hasAdminKey } = useAdminAccess();

    if (hasAdminKey) {
        return <>{children}</>;
    }

    return (
        <div className="wc-panel-stack max-w-3xl">
            <div className="card card-pad">
                <div className="row" style={{ alignItems: 'flex-start' }}>
                    <div className="iconbox warn">
                        <LockKeyhole className="h-4 w-4" />
                    </div>
                    <div>
                        <h3 style={{ margin: 0, fontSize: 15, fontWeight: 600 }}>
                            {t('settings.adminAccessProtectedTitle')}
                        </h3>
                        <p className="muted" style={{ margin: '4px 0 0', fontSize: 13 }}>
                            {t('settings.adminAccessProtectedDescription')}
                        </p>
                    </div>
                </div>
            </div>
            {showPanel && <AdminAccessPanel />}
        </div>
    );
};

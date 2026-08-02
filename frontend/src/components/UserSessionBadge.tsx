import { useEffect, useState } from 'react';
import { User, Loader2 } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { sessionService, type UserSession } from '../services/sessionService';

export const UserSessionBadge = () => {
    const { t } = useTranslation();
    const [session, setSession] = useState<UserSession | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchSession = async () => {
            try {
                const data = await sessionService.getWhoAmI();
                setSession(data);
            } catch (error) {
                console.error('Failed to fetch session:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchSession();
    }, []);

    if (loading) {
        return (
            <div className="session-badge session-badge-loading" role="status">
                <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
                <span>{t('common.loading')}</span>
            </div>
        );
    }

    if (!session) return null;

    return (
        <div
            className="session-badge"
            title={t('session.guestDiagnostic', { code: session.public_id })}
        >
            <User className="h-4 w-4" aria-hidden="true" />
            <strong>
                {t('session.guestLabel', { code: session.public_id.slice(-6).toUpperCase() })}
            </strong>
        </div>
    );
};

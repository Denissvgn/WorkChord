import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import {
    Save,
    Mail,
    Server,
    Shield,
    Eye,
    EyeOff,
    Send,
} from 'lucide-react';
import { Button } from '../common/Button';
import { Input } from '../common/Input';
import { Checkbox } from '../common/Checkbox';
import { QueryErrorState, QueryLoadingState } from '../feedback/QueryState';
import { emailSettingsService } from '../../services/emailSettingsService';
import { getAdminAccessErrorMessage } from '../../utils/adminAccess';
import { useAdminAccess } from '../../hooks/useAdminAccess';
import { protectedQueryRetry } from '../../utils/protectedQueries';
import type { EmailSettings } from '../../types/emailSettings';
import type { RuntimeSettingSource } from '../../types/systemSettings';
import { useToast } from '../feedback/toast';

const sourceLabelKey: Record<RuntimeSettingSource, string> = {
    runtime: 'common.runtime',
    environment: 'common.environment',
    default: 'common.default',
};

const sourceClass: Record<RuntimeSettingSource, string> = {
    runtime: 'bg-action-muted text-action border-action',
    environment: 'bg-feedback-warning-muted text-feedback-warning-foreground border-feedback-warning-border',
    default: 'bg-surface-muted text-content-secondary border-border',
};

const SourceBadge = ({ source }: { source?: RuntimeSettingSource }) => {
    const { t } = useTranslation();
    if (!source) return null;
    return (
        <span className={`inline-flex items-center rounded-full border px-2 py-0.5 text-xs font-medium ${sourceClass[source]}`}>
            {t(sourceLabelKey[source])}
        </span>
    );
};

export const EmailSettingsPanel = () => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const { hasAdminKey } = useAdminAccess();
    const toast = useToast();
    const [localSettings, setLocalSettings] = useState<EmailSettings | null>(null);
    const [hasChanges, setHasChanges] = useState(false);
    const [showPassword, setShowPassword] = useState(false);
    const [testEmail, setTestEmail] = useState('');

    // Fetch settings
    const { data: settings, isLoading, error, isError, refetch } = useQuery({
        queryKey: ['email-settings'],
        queryFn: emailSettingsService.getSettings,
        enabled: hasAdminKey,
        retry: protectedQueryRetry,
    });

    const editableSettings = localSettings || settings || null;

    // Save mutation
    const saveMutation = useMutation({
        mutationFn: emailSettingsService.updateSettings,
        onSuccess: (updatedSettings) => {
            queryClient.setQueryData(['email-settings'], updatedSettings);
            setLocalSettings({ ...updatedSettings, smtp_password: '', clear_smtp_password: false });
            setHasChanges(false);
            toast.success(t('surfaces.emailSettings.saveSuccess'));
        },
        onError: (err: unknown) => {
            toast.error(getAdminAccessErrorMessage(err, {
                missingOrInvalid: t('settings.adminAccessMissingOrInvalid'),
                backendNotConfigured: t('settings.adminAccessBackendNotConfigured'),
                fallback: t('surfaces.emailSettings.saveFailed'),
            }));
        },
    });

    // Test email mutation
    const testMutation = useMutation({
        mutationFn: emailSettingsService.testConnection,
        onSuccess: (response) => {
            if (response.success) {
                toast.success(t('surfaces.emailSettings.testSuccess'));
            } else {
                toast.error(t('surfaces.emailSettings.testFailed'));
            }
        },
        onError: (err: unknown) => {
            toast.error(getAdminAccessErrorMessage(err, {
                missingOrInvalid: t('settings.adminAccessMissingOrInvalid'),
                backendNotConfigured: t('settings.adminAccessBackendNotConfigured'),
                fallback: t('surfaces.emailSettings.testFailed'),
            }));
        },
    });

    const updateField = <K extends keyof EmailSettings>(field: K, value: EmailSettings[K]) => {
        if (!editableSettings) return;
        setLocalSettings({ ...editableSettings, [field]: value });
        setHasChanges(true);
    };

    const handleSave = () => {
        if (!editableSettings) return;
        saveMutation.mutate({
            ...editableSettings,
            smtp_password: editableSettings.smtp_password || undefined,
            clear_smtp_password: Boolean(editableSettings.clear_smtp_password),
        });
    };

    const handleTestEmail = () => {
        const recipient = testEmail.trim() || editableSettings?.smtp_from_email || '';
        if (!recipient) {
            toast.error(t('surfaces.emailSettings.enterRecipient'));
            return;
        }
        testMutation.mutate(recipient);
    };

    if (isLoading) {
        return <QueryLoadingState message={t('surfaces.emailSettings.loadingEmailSettings')} />;
    }

    if (isError || !editableSettings) {
        const message = getAdminAccessErrorMessage(error, {
            missingOrInvalid: t('settings.adminAccessMissingOrInvalid'),
            backendNotConfigured: t('settings.adminAccessBackendNotConfigured'),
            fallback: t('settings.emailSettingsLoadFailed'),
        });
        return (
            <QueryErrorState
                message={message}
                onRetry={() => { void refetch(); }}
                title={t('surfaces.emailSettings.emailNotifications')}
            />
        );
    }

    const { enabled } = editableSettings;

    return (
        <div className="max-w-3xl space-y-6">
            {/* Master Toggle */}
            <div className="card flex items-center justify-between p-4">
                <div className="flex items-center gap-3">
                    <div className={`p-2 rounded-full ${enabled ? 'bg-status-active-muted text-action' : 'bg-surface-subtle text-content-tertiary'}`}>
                        <Mail className="w-6 h-6" />
                    </div>
                    <div>
                        <h3 className="text-lg font-medium text-content-primary">{t('surfaces.emailSettings.emailNotifications')}</h3>
                        <p className="text-sm text-content-secondary">{t('surfaces.emailSettings.enableEmailNotificationsForTaskUpdates')}</p>
                    </div>
                    <SourceBadge source={editableSettings.field_sources?.enabled} />
                </div>
                <Checkbox
                    checked={enabled}
                    onChange={(checked) => updateField('enabled', checked)}
                    className="scale-125"
                />
            </div>

            {/* Settings Form */}
            <div className={`space-y-6 transition-opacity duration-200 ${enabled ? 'opacity-100' : 'opacity-60 pointer-events-none'}`}>

                {/* Connection Settings */}
                <div className="card space-y-4">
                    <h4 className="text-sm font-semibold text-content-primary uppercase tracking-wider flex items-center gap-2">
                        <Server className="w-4 h-4" />
                        {t('surfaces.emailSettings.smtpConnection')}
                    </h4>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div className="md:col-span-2">
                            <Input
                                label={t('surfaces.emailSettings.smtpHost')}
                                placeholder={t('surfaces.emailSettings.smtpGmailCom')}
                                value={editableSettings.smtp_host}
                                onChange={(e) => updateField('smtp_host', e.target.value)}
                                disabled={!enabled}
                            />
                            <div className="mt-1 flex justify-end">
                                <SourceBadge source={editableSettings.field_sources?.smtp_host} />
                            </div>
                        </div>
                        <div>
                            <Input
                                label={t('surfaces.emailSettings.port')}
                                type="number"
                                placeholder="587"
                                value={editableSettings.smtp_port}
                                onChange={(e) => updateField('smtp_port', parseInt(e.target.value) || 0)}
                                disabled={!enabled}
                            />
                            <div className="mt-1 flex justify-end">
                                <SourceBadge source={editableSettings.field_sources?.smtp_port} />
                            </div>
                        </div>
                    </div>

                    <div className="flex items-center gap-2 pt-2">
                        <Checkbox
                            label={t('surfaces.emailSettings.useTLSTransportLayerSecurity')}
                            checked={editableSettings.smtp_use_tls}
                            onChange={(checked) => updateField('smtp_use_tls', checked)}
                            disabled={!enabled}
                        />
                    </div>
                </div>

                {/* Authentication Settings */}
                <div className="card space-y-4">
                    <h4 className="text-sm font-semibold text-content-primary uppercase tracking-wider flex items-center gap-2">
                        <Shield className="w-4 h-4" />
                        {t('surfaces.emailSettings.authentication')}
                    </h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <Input
                            label={t('surfaces.emailSettings.usernameEmail')}
                            placeholder={t('surfaces.emailSettings.notificationsExampleCom')}
                            value={editableSettings.smtp_user}
                            onChange={(e) => updateField('smtp_user', e.target.value)}
                            disabled={!enabled}
                        />
                        <div className="relative">
                            {editableSettings.has_password && (
                                <div className="mb-1 flex items-center justify-between text-xs text-content-secondary">
                                    <span>{t('surfaces.emailSettings.passwordConfigured')}</span>
                                    <SourceBadge source={editableSettings.field_sources?.smtp_password} />
                                </div>
                            )}
                            <Input
                                type={showPassword ? "text" : "password"}
                                label={t('surfaces.emailSettings.passwordAppPassword')}
                                placeholder={editableSettings.has_password ? "••••••••••••" : t('surfaces.emailSettings.enterPassword')}
                                value={editableSettings.smtp_password || ''}
                                onChange={(e) => updateField('smtp_password', e.target.value)}
                                disabled={!enabled}
                            />
                            <button
                                type="button"
                                onClick={() => setShowPassword(!showPassword)}
                                aria-label={t(showPassword ? 'surfaces.emailSettings.hidePassword' : 'surfaces.emailSettings.showPassword')}
                                className="absolute right-3 top-[34px] text-content-tertiary hover:text-content-secondary"
                            >
                                {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                            </button>
                        </div>
                    </div>
                    <Checkbox
                        label={t('surfaces.emailSettings.clearRuntimePasswordOverride')}
                        checked={Boolean(editableSettings.clear_smtp_password)}
                        onChange={(checked) => updateField('clear_smtp_password', checked)}
                        disabled={!enabled}
                    />
                </div>

                {/* Sender Settings */}
                <div className="card space-y-4">
                    <h4 className="text-sm font-semibold text-content-primary uppercase tracking-wider flex items-center gap-2">
                        <Send className="w-4 h-4" />
                        {t('surfaces.emailSettings.senderInfo')}
                    </h4>
                    <Input
                        label={t('surfaces.emailSettings.fromEmailAddress')}
                        placeholder={t('surfaces.emailSettings.notificationsCompanyCom')}
                        value={editableSettings.smtp_from_email}
                        onChange={(e) => updateField('smtp_from_email', e.target.value)}
                        disabled={!enabled}
                    />
                    <div className="flex justify-end">
                        <SourceBadge source={editableSettings.field_sources?.smtp_from_email} />
                    </div>
                </div>
            </div>

            {/* Action Bar */}
            <div className="sticky bottom-0 bg-surface-card/80 backdrop-blur-md p-4 rounded-xl border border-border shadow-lg flex items-center justify-between z-10">
                <div className="flex items-center gap-2 w-full max-w-md">
                    <Input
                        placeholder={t('surfaces.emailSettings.enterEmailToTest')}
                        value={testEmail}
                        onChange={(e) => setTestEmail(e.target.value)}
                        className="bg-surface-card"
                        disabled={!enabled}
                    />
                    <Button
                        variant="secondary"
                        onClick={handleTestEmail}
                        isLoading={testMutation.isPending}
                        disabled={!enabled || !(testEmail.trim() || editableSettings.smtp_from_email)}
                    >
                        {t('surfaces.emailSettings.test')}
                    </Button>
                </div>

                <div className="flex items-center gap-4">
                    {hasChanges && (
                        <span className="text-feedback-warning-foreground text-sm font-medium animate-pulse">
                            {t('surfaces.emailSettings.unsavedChanges')}
                        </span>
                    )}
                    <Button
                        onClick={handleSave}
                        isLoading={saveMutation.isPending}
                        disabled={!hasChanges}
                    >
                        <Save className="w-4 h-4 mr-2" />
                        {t('surfaces.emailSettings.saveSettings')}
                    </Button>
                </div>
            </div>
        </div>
    );
};

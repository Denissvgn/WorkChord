import { useRef, useState } from 'react';
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

type EmailValidationErrors = Partial<Record<
    'smtp_host' | 'smtp_port' | 'smtp_from_email' | 'test_email',
    string
>>;

const isValidEmailAddress = (value: string) => (
    /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)
);

const isValidSmtpHost = (value: string) => {
    if (!value || /\s/.test(value) || value.includes('://')) return false;
    try {
        const parsed = new URL(`http://${value}`);
        return Boolean(parsed.hostname)
            && !parsed.username
            && !parsed.password
            && !parsed.port
            && parsed.pathname === '/'
            && !parsed.search
            && !parsed.hash;
    } catch {
        return false;
    }
};

const FieldError = ({ id, message }: { id: string; message?: string }) => (
    message ? (
        <p id={id} className="mt-1 text-sm text-feedback-danger-foreground" role="alert">
            {message}
        </p>
    ) : null
);

export const EmailSettingsPanel = () => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const { hasAdminKey } = useAdminAccess();
    const toast = useToast();
    const [localSettings, setLocalSettings] = useState<EmailSettings | null>(null);
    const [showPassword, setShowPassword] = useState(false);
    const [testEmail, setTestEmail] = useState('');
    const [validationErrors, setValidationErrors] = useState<EmailValidationErrors>({});
    const smtpHostRef = useRef<HTMLInputElement>(null);
    const smtpPortRef = useRef<HTMLInputElement>(null);
    const senderEmailRef = useRef<HTMLInputElement>(null);
    const testEmailRef = useRef<HTMLInputElement>(null);

    // Fetch settings
    const { data: settings, isLoading, error, isError, refetch } = useQuery({
        queryKey: ['email-settings'],
        queryFn: emailSettingsService.getSettings,
        enabled: hasAdminKey,
        retry: protectedQueryRetry,
    });

    const editableSettings = localSettings || settings || null;
    const hasChanges = Boolean(localSettings && settings && (
        localSettings.enabled !== settings.enabled
        || localSettings.smtp_host !== settings.smtp_host
        || localSettings.smtp_port !== settings.smtp_port
        || localSettings.smtp_user !== settings.smtp_user
        || localSettings.smtp_from_email !== settings.smtp_from_email
        || localSettings.smtp_use_tls !== settings.smtp_use_tls
        || Boolean(localSettings.smtp_password)
        || Boolean(localSettings.clear_smtp_password)
    ));

    // Save mutation
    const saveMutation = useMutation({
        mutationFn: emailSettingsService.updateSettings,
        onSuccess: (updatedSettings) => {
            queryClient.setQueryData(['email-settings'], updatedSettings);
            setLocalSettings({ ...updatedSettings, smtp_password: '', clear_smtp_password: false });
            setValidationErrors({});
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
        if (!editableSettings || saveMutation.isPending) return;
        setLocalSettings({ ...editableSettings, [field]: value });
        if (field === 'smtp_host' || field === 'smtp_port' || field === 'smtp_from_email') {
            setValidationErrors(current => ({ ...current, [field]: undefined }));
        }
    };

    const updatePassword = (value: string) => {
        if (!editableSettings || saveMutation.isPending) return;
        setLocalSettings({
            ...editableSettings,
            smtp_password: value,
            clear_smtp_password: false,
        });
    };

    const updateClearPassword = (checked: boolean) => {
        if (!editableSettings || saveMutation.isPending) return;
        setLocalSettings({
            ...editableSettings,
            clear_smtp_password: checked,
            smtp_password: checked ? '' : editableSettings.smtp_password,
        });
        if (checked) setShowPassword(false);
    };

    const validateConfiguration = (draft: EmailSettings): EmailValidationErrors => {
        const nextErrors: EmailValidationErrors = {};
        const host = draft.smtp_host.trim();
        const senderEmail = draft.smtp_from_email.trim();

        if (!host) {
            if (draft.enabled) {
                nextErrors.smtp_host = t('surfaces.emailSettings.smtpHostRequired');
            }
        } else if (!isValidSmtpHost(host)) {
            nextErrors.smtp_host = t('surfaces.emailSettings.smtpHostInvalid');
        }

        if (!senderEmail) {
            nextErrors.smtp_from_email = t('surfaces.emailSettings.senderEmailRequired');
        } else if (!isValidEmailAddress(senderEmail)) {
            nextErrors.smtp_from_email = t('surfaces.emailSettings.emailAddressInvalid');
        }

        if (!Number.isInteger(draft.smtp_port) || draft.smtp_port < 1 || draft.smtp_port > 65535) {
            nextErrors.smtp_port = t('surfaces.emailSettings.smtpPortInvalid');
        }

        return nextErrors;
    };

    const handleSave = () => {
        if (!editableSettings || saveMutation.isPending) return;
        const nextErrors = validateConfiguration(editableSettings);
        setValidationErrors(current => ({ ...nextErrors, test_email: current.test_email }));
        if (Object.keys(nextErrors).length > 0) {
            if (nextErrors.smtp_host) smtpHostRef.current?.focus();
            else if (nextErrors.smtp_port) smtpPortRef.current?.focus();
            else if (nextErrors.smtp_from_email) senderEmailRef.current?.focus();
            return;
        }

        saveMutation.mutate({
            ...editableSettings,
            smtp_host: editableSettings.smtp_host.trim(),
            smtp_user: editableSettings.smtp_user.trim(),
            smtp_from_email: editableSettings.smtp_from_email.trim(),
            smtp_password: editableSettings.smtp_password || undefined,
            clear_smtp_password: Boolean(editableSettings.clear_smtp_password),
        });
    };

    const handleTestEmail = () => {
        if (hasChanges || saveMutation.isPending || testMutation.isPending) return;
        const recipient = testEmail.trim() || settings?.smtp_from_email.trim() || '';
        if (!recipient) {
            setValidationErrors(current => ({
                ...current,
                test_email: t('surfaces.emailSettings.enterRecipient'),
            }));
            testEmailRef.current?.focus();
            return;
        }
        if (!isValidEmailAddress(recipient)) {
            setValidationErrors(current => ({
                ...current,
                test_email: t('surfaces.emailSettings.emailAddressInvalid'),
            }));
            testEmailRef.current?.focus();
            return;
        }
        setValidationErrors(current => ({ ...current, test_email: undefined }));
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
    const configurationDisabled = !enabled || saveMutation.isPending;
    const testDisabled = !enabled
        || hasChanges
        || saveMutation.isPending
        || testMutation.isPending;

    return (
        <div className="max-w-3xl space-y-6">
            {/* Master Toggle */}
            <div className="card flex items-center justify-between gap-4 p-4">
                <div className="flex min-w-0 items-center gap-3">
                    <div className={`p-2 rounded-full ${enabled ? 'bg-status-active-muted text-action' : 'bg-surface-subtle text-content-tertiary'}`}>
                        <Mail aria-hidden="true" className="w-6 h-6" />
                    </div>
                    <div className="min-w-0">
                        <h3 className="text-lg font-medium text-content-primary">{t('surfaces.emailSettings.emailNotifications')}</h3>
                        <p className="text-sm text-content-secondary">{t('surfaces.emailSettings.enableEmailNotificationsForTaskUpdates')}</p>
                    </div>
                    <SourceBadge source={editableSettings.field_sources?.enabled} />
                </div>
                <Checkbox
                    aria-label={t('surfaces.emailSettings.enableEmailNotificationsForTaskUpdates')}
                    checked={enabled}
                    onChange={(checked) => updateField('enabled', checked)}
                    disabled={saveMutation.isPending}
                    className="scale-125"
                />
            </div>

            {/* Settings Form */}
            <div className={`space-y-6 transition-opacity duration-200 ${enabled ? 'opacity-100' : 'opacity-60'}`}>

                {/* Connection Settings */}
                <div className="card space-y-4">
                    <h4 className="text-sm font-semibold text-content-primary uppercase tracking-wider flex items-center gap-2">
                        <Server aria-hidden="true" className="w-4 h-4" />
                        {t('surfaces.emailSettings.smtpConnection')}
                    </h4>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div className="md:col-span-2">
                            <Input
                                ref={smtpHostRef}
                                id="email-smtp-host"
                                label={t('surfaces.emailSettings.smtpHost')}
                                placeholder={t('surfaces.emailSettings.smtpGmailCom')}
                                value={editableSettings.smtp_host}
                                onChange={(e) => updateField('smtp_host', e.target.value)}
                                disabled={configurationDisabled}
                                autoCapitalize="none"
                                spellCheck={false}
                                aria-invalid={Boolean(validationErrors.smtp_host)}
                                aria-describedby={validationErrors.smtp_host ? 'email-smtp-host-error' : undefined}
                            />
                            <FieldError id="email-smtp-host-error" message={validationErrors.smtp_host} />
                            <div className="mt-1 flex justify-end">
                                <SourceBadge source={editableSettings.field_sources?.smtp_host} />
                            </div>
                        </div>
                        <div>
                            <Input
                                ref={smtpPortRef}
                                id="email-smtp-port"
                                label={t('surfaces.emailSettings.port')}
                                type="number"
                                placeholder="587"
                                value={editableSettings.smtp_port}
                                onChange={(e) => updateField(
                                    'smtp_port',
                                    Number.isNaN(e.target.valueAsNumber) ? 0 : e.target.valueAsNumber,
                                )}
                                disabled={configurationDisabled}
                                min={1}
                                max={65535}
                                step={1}
                                aria-invalid={Boolean(validationErrors.smtp_port)}
                                aria-describedby={validationErrors.smtp_port ? 'email-smtp-port-error' : undefined}
                            />
                            <FieldError id="email-smtp-port-error" message={validationErrors.smtp_port} />
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
                            disabled={configurationDisabled}
                        />
                    </div>
                </div>

                {/* Authentication Settings */}
                <div className="card space-y-4">
                    <h4 className="text-sm font-semibold text-content-primary uppercase tracking-wider flex items-center gap-2">
                        <Shield aria-hidden="true" className="w-4 h-4" />
                        {t('surfaces.emailSettings.authentication')}
                    </h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <Input
                            label={t('surfaces.emailSettings.usernameEmail')}
                            placeholder={t('surfaces.emailSettings.notificationsExampleCom')}
                            value={editableSettings.smtp_user}
                            onChange={(e) => updateField('smtp_user', e.target.value)}
                            disabled={configurationDisabled}
                            autoCapitalize="none"
                            spellCheck={false}
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
                                onChange={(e) => updatePassword(e.target.value)}
                                disabled={configurationDisabled || Boolean(editableSettings.clear_smtp_password)}
                                autoComplete="new-password"
                            />
                            <button
                                type="button"
                                onClick={() => setShowPassword(!showPassword)}
                                disabled={configurationDisabled || Boolean(editableSettings.clear_smtp_password)}
                                aria-label={t(showPassword ? 'surfaces.emailSettings.hidePassword' : 'surfaces.emailSettings.showPassword')}
                                className="absolute right-3 top-[34px] text-content-tertiary hover:text-content-secondary disabled:cursor-not-allowed disabled:opacity-50"
                            >
                                {showPassword
                                    ? <EyeOff aria-hidden="true" className="w-4 h-4" />
                                    : <Eye aria-hidden="true" className="w-4 h-4" />}
                            </button>
                        </div>
                    </div>
                    <Checkbox
                        label={t('surfaces.emailSettings.clearRuntimePasswordOverride')}
                        checked={Boolean(editableSettings.clear_smtp_password)}
                        onChange={updateClearPassword}
                        disabled={configurationDisabled}
                    />
                </div>

                {/* Sender Settings */}
                <div className="card space-y-4">
                    <h4 className="text-sm font-semibold text-content-primary uppercase tracking-wider flex items-center gap-2">
                        <Send aria-hidden="true" className="w-4 h-4" />
                        {t('surfaces.emailSettings.senderInfo')}
                    </h4>
                    <Input
                        ref={senderEmailRef}
                        id="email-sender-address"
                        type="email"
                        label={t('surfaces.emailSettings.fromEmailAddress')}
                        placeholder={t('surfaces.emailSettings.notificationsCompanyCom')}
                        value={editableSettings.smtp_from_email}
                        onChange={(e) => updateField('smtp_from_email', e.target.value)}
                        disabled={configurationDisabled}
                        autoComplete="email"
                        autoCapitalize="none"
                        spellCheck={false}
                        aria-invalid={Boolean(validationErrors.smtp_from_email)}
                        aria-describedby={validationErrors.smtp_from_email ? 'email-sender-address-error' : undefined}
                    />
                    <FieldError id="email-sender-address-error" message={validationErrors.smtp_from_email} />
                    <div className="flex justify-end">
                        <SourceBadge source={editableSettings.field_sources?.smtp_from_email} />
                    </div>
                </div>
            </div>

            {/* Action Bar */}
            <div className="sticky bottom-0 z-10 flex flex-col gap-4 rounded-xl border border-border bg-surface-card/80 p-4 shadow-lg backdrop-blur-md lg:flex-row lg:items-end lg:justify-between">
                <div className="min-w-0 space-y-1 lg:max-w-md lg:flex-1">
                    <div className="flex flex-col gap-2 sm:flex-row sm:items-end">
                        <Input
                            ref={testEmailRef}
                            id="email-test-recipient"
                            type="email"
                            label={t('surfaces.emailSettings.testRecipient')}
                            placeholder={t('surfaces.emailSettings.enterEmailToTest')}
                            value={testEmail}
                            onChange={(e) => {
                                setTestEmail(e.target.value);
                                setValidationErrors(current => ({ ...current, test_email: undefined }));
                            }}
                            className="bg-surface-card"
                            disabled={!enabled || saveMutation.isPending || testMutation.isPending}
                            autoComplete="email"
                            autoCapitalize="none"
                            spellCheck={false}
                            aria-invalid={Boolean(validationErrors.test_email)}
                            aria-describedby={validationErrors.test_email
                                ? 'email-test-recipient-error email-test-recipient-help'
                                : 'email-test-recipient-help'}
                        />
                        <Button
                            className="w-full sm:w-auto"
                            variant="secondary"
                            onClick={handleTestEmail}
                            isLoading={testMutation.isPending}
                            disabled={testDisabled}
                        >
                            {t('surfaces.emailSettings.test')}
                        </Button>
                    </div>
                    <FieldError id="email-test-recipient-error" message={validationErrors.test_email} />
                    <p
                        id="email-test-recipient-help"
                        className={`text-xs ${hasChanges ? 'text-feedback-warning-foreground' : 'text-content-secondary'}`}
                        aria-live="polite"
                    >
                        {t(hasChanges
                            ? 'surfaces.emailSettings.testSaveFirst'
                            : 'surfaces.emailSettings.testUsesSavedConfiguration')}
                    </p>
                </div>

                <div className="flex w-full flex-col gap-2 sm:flex-row sm:items-center sm:justify-end lg:w-auto">
                    {hasChanges && (
                        <span className="text-sm font-medium text-feedback-warning-foreground" role="status">
                            {t('surfaces.emailSettings.unsavedChanges')}
                        </span>
                    )}
                    <Button
                        className="w-full sm:w-auto"
                        onClick={handleSave}
                        isLoading={saveMutation.isPending}
                        disabled={!hasChanges || saveMutation.isPending}
                    >
                        <Save aria-hidden="true" className="w-4 h-4 mr-2" />
                        {t('surfaces.emailSettings.saveSettings')}
                    </Button>
                </div>
            </div>
        </div>
    );
};

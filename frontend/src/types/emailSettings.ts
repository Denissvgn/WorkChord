import type { RuntimeSettingSource } from './systemSettings';

export interface EmailSettings {
    enabled: boolean;
    smtp_host: string;
    smtp_port: number;
    smtp_user: string;
    smtp_from_email: string;
    smtp_use_tls: boolean;
    has_password: boolean;
    smtp_password?: string; // Optional field for frontend form state
    clear_smtp_password?: boolean;
    field_sources?: Record<string, RuntimeSettingSource>;
}

export interface EmailSettingsUpdate {
    enabled: boolean;
    smtp_host: string;
    smtp_port: number;
    smtp_user: string;
    smtp_password?: string | null;
    smtp_from_email: string;
    smtp_use_tls: boolean;
    clear_smtp_password?: boolean;
    reset_fields?: string[];
}

export interface TestEmailRequest {
    recipient: string;
}

export interface TestEmailResponse {
    success: boolean;
    message: string;
}

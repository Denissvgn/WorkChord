export type RuntimeSettingSource = 'runtime' | 'environment' | 'default';
export type LLMProvider = 'openai' | 'openrouter' | 'nvidia' | 'custom';
export type LanguageCode = 'en' | 'ru';
export type AILanguageMode = 'auto' | LanguageCode;

export interface AppRuntimeSettings {
    ui_language: LanguageCode;
    ai_language_mode: AILanguageMode;
    field_sources: Record<string, RuntimeSettingSource>;
}

export interface AppRuntimeSettingsUpdate {
    ui_language?: LanguageCode;
    ai_language_mode?: AILanguageMode;
    reset_fields?: string[];
}

export interface LLMRuntimeSettings {
    provider: LLMProvider;
    api_url: string;
    model: string;
    temperature: number;
    max_output_tokens: number;
    has_api_key: boolean;
    field_sources: Record<string, RuntimeSettingSource>;
}

export interface LLMRuntimeSettingsUpdate {
    provider?: LLMProvider;
    api_url?: string;
    model?: string;
    temperature?: number;
    max_output_tokens?: number;
    api_key?: string | null;
    clear_api_key?: boolean;
    reset_fields?: string[];
}

export interface GitHubRuntimeSettings {
    api_url: string;
    request_timeout_seconds: number;
    webhook_create_triage_for_unmatched: boolean;
    has_token: boolean;
    has_webhook_secret: boolean;
    field_sources: Record<string, RuntimeSettingSource>;
}

export interface GitHubRuntimeSettingsUpdate {
    api_url?: string;
    token?: string | null;
    clear_token?: boolean;
    request_timeout_seconds?: number;
    webhook_secret?: string | null;
    clear_webhook_secret?: boolean;
    webhook_create_triage_for_unmatched?: boolean;
    reset_fields?: string[];
}

export interface WebIntakeRuntimeSettings {
    rate_limit_per_minute: number;
    has_token: boolean;
    field_sources: Record<string, RuntimeSettingSource>;
}

export interface WebIntakeRuntimeSettingsUpdate {
    token?: string | null;
    clear_token?: boolean;
    rate_limit_per_minute?: number;
    reset_fields?: string[];
}

export interface RestartRequiredSetting {
    key: string;
    description: string;
}

export interface SystemSettings {
    app: AppRuntimeSettings;
    llm: LLMRuntimeSettings;
    github: GitHubRuntimeSettings;
    web_intake: WebIntakeRuntimeSettings;
    restart_required: RestartRequiredSetting[];
}

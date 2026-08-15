const color = (name) => `rgb(var(--color-${name}) / <alpha-value>)`;
const feedbackTone = (name) => ({
    DEFAULT: color(`feedback-${name}`),
    muted: color(`feedback-${name}-muted`),
    'muted-hover': color(`feedback-${name}-muted-hover`),
    foreground: color(`feedback-${name}-foreground`),
    border: color(`feedback-${name}-border`),
    emphasis: color(`feedback-${name}-on-solid`),
});

/** @type {import('tailwindcss').Config} */
export default {
    content: [
        './index.html',
        './src/**/*.{js,ts,jsx,tsx}',
    ],
    darkMode: ['selector', '[data-theme="dark"]'],
    theme: {
        extend: {
            colors: {
                surface: {
                    canvas: color('surface-canvas'),
                    card: color('surface-card'),
                    muted: color('surface-muted'),
                    subtle: color('surface-subtle'),
                    hover: color('surface-hover'),
                },
                content: {
                    primary: color('content-primary'),
                    secondary: color('content-secondary'),
                    tertiary: color('content-tertiary'),
                    inverse: color('content-inverse'),
                    emphasis: color('content-emphasis'),
                },
                border: {
                    DEFAULT: color('border-default'),
                    subtle: color('border-subtle'),
                    strong: color('border-strong'),
                },
                action: {
                    DEFAULT: color('action-primary'),
                    hover: color('action-primary-hover'),
                    muted: color('action-muted'),
                    'muted-hover': color('action-muted-hover'),
                    'muted-foreground': color('action-muted-foreground'),
                    foreground: color('action-foreground'),
                },
                focus: color('focus-ring'),
                status: {
                    planned: {
                        DEFAULT: color('status-planned-solid'),
                        muted: color('status-planned-muted'),
                        foreground: color('status-planned-foreground'),
                        border: color('status-planned-border'),
                        emphasis: color('status-planned-on-solid'),
                    },
                    active: {
                        DEFAULT: color('status-active-solid'),
                        muted: color('status-active-muted'),
                        foreground: color('status-active-foreground'),
                        border: color('status-active-border'),
                        emphasis: color('status-active-on-solid'),
                    },
                    resolved: {
                        DEFAULT: color('status-resolved-solid'),
                        muted: color('status-resolved-muted'),
                        foreground: color('status-resolved-foreground'),
                        border: color('status-resolved-border'),
                        emphasis: color('status-resolved-on-solid'),
                    },
                    closed: {
                        DEFAULT: color('status-closed-solid'),
                        muted: color('status-closed-muted'),
                        foreground: color('status-closed-foreground'),
                        border: color('status-closed-border'),
                        emphasis: color('status-closed-on-solid'),
                    },
                },
                feedback: {
                    neutral: feedbackTone('neutral'),
                    info: feedbackTone('info'),
                    success: feedbackTone('success'),
                    warning: feedbackTone('warning'),
                    danger: feedbackTone('danger'),
                    purple: feedbackTone('purple'),
                    indigo: feedbackTone('indigo'),
                },
                overlay: color('overlay'),
                terminal: {
                    canvas: color('terminal-canvas'),
                    surface: color('terminal-surface'),
                    border: color('terminal-border'),
                    primary: color('terminal-primary'),
                    secondary: color('terminal-secondary'),
                    muted: color('terminal-muted'),
                },
            },
            fontFamily: {
                sans: ['var(--font-family-sans)'],
                mono: ['var(--font-family-mono)'],
            },
            fontSize: {
                'wc-micro': ['var(--wc-type-micro)', { lineHeight: 'var(--wc-leading-ui)' }],
                'wc-meta': ['var(--wc-type-meta)', { lineHeight: 'var(--wc-leading-body)' }],
                'wc-label': ['var(--wc-type-label)', { lineHeight: 'var(--wc-leading-ui)' }],
                'wc-base': ['var(--wc-type-base)', { lineHeight: 'var(--wc-leading-body)' }],
                'wc-heading': ['var(--wc-type-heading)', { lineHeight: 'var(--wc-leading-ui)' }],
                'wc-section': ['var(--wc-type-section)', { lineHeight: 'var(--wc-leading-tight)' }],
                'wc-step': ['var(--wc-type-step)', { lineHeight: 'var(--wc-leading-tight)' }],
                'wc-page': ['var(--wc-type-page)', { lineHeight: 'var(--wc-leading-tight)' }],
            },
            borderRadius: {
                sm: 'var(--radius-sm)',
                md: 'var(--radius-md)',
                lg: 'var(--radius-lg)',
                xl: 'var(--radius-xl)',
            },
            spacing: {
                xs: 'var(--space-xs)',
                sm: 'var(--space-sm)',
                md: 'var(--space-md)',
                lg: 'var(--space-lg)',
                xl: 'var(--space-xl)',
                '2xl': 'var(--space-2xl)',
                '3xl': 'var(--space-3xl)',
            },
        },
    },
    plugins: [],
};

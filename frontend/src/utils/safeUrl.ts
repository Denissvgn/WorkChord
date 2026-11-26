export const safeExternalHref = (value?: string | null): string | undefined => {
    if (!value) return undefined;
    try {
        const url = new URL(value);
        if (url.protocol === 'http:' || url.protocol === 'https:') {
            return url.href;
        }
    } catch {
        return undefined;
    }
    return undefined;
};

/** An intake or task source link: a path inside this instance, or a safe http(s) address. */
export const sourceLinkHref = (value?: string | null): string | undefined => {
    if (value && value.startsWith('/') && !value.startsWith('//') && !value.includes('\\')) return value;
    return safeExternalHref(value);
};

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

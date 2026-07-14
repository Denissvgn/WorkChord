export const mergeLabels = (current: string[] = [], incoming: string[] = []) => {
    const seen = new Set<string>();
    const result: string[] = [];

    [...current, ...incoming].forEach(label => {
        const trimmed = label.trim();
        const key = trimmed.toLowerCase();
        if (trimmed && !seen.has(key)) {
            seen.add(key);
            result.push(trimmed);
        }
    });

    return result;
};

export const appendChecklistToDescription = (
    description: string | null | undefined,
    checklist: string[] = [],
) => {
    const base = description?.trim() ?? '';
    const validItems = checklist.map(item => item.trim()).filter(Boolean);
    if (validItems.length === 0) {
        return base;
    }

    const checklistText = [
        'Checklist:',
        ...validItems.map(item => `- ${item}`),
    ].join('\n');
    return base ? `${base}\n\n${checklistText}` : checklistText;
};

export const getPayloadString = (
    payload: Record<string, unknown>,
    key: string,
    fallback: string | null = null,
) => {
    const value = payload[key];
    return typeof value === 'string' ? value : fallback;
};

export const getPayloadBoolean = (
    payload: Record<string, unknown>,
    key: string,
    fallback: boolean,
) => {
    const value = payload[key];
    return typeof value === 'boolean' ? value : fallback;
};

export const getPayloadNumber = (
    payload: Record<string, unknown>,
    key: string,
    fallback: number,
) => {
    const value = payload[key];
    return typeof value === 'number' && Number.isFinite(value) ? value : fallback;
};

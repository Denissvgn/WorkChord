export const isGraphLimitError = (error: unknown) => {
    const detail = (error as { response?: { data?: { detail?: { code?: string } } } })?.response?.data?.detail;
    return detail?.code === 'collection_limit_exceeded';
};

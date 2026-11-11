/** "18:42" for a claim that ends today, a short date and time otherwise, in the reader's time zone. */
export const formatClaimUntil = (value: string, locale: string, now = new Date()) => {
    const until = new Date(value);
    if (Number.isNaN(until.getTime())) return null;
    const sameDay = until.toDateString() === now.toDateString();
    return new Intl.DateTimeFormat(locale, sameDay ? { hour: '2-digit', minute: '2-digit' } : { dateStyle: 'medium', timeStyle: 'short' }).format(until);
};

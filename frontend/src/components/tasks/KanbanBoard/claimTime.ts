/**
 * "18:42 GMT+3" for a claim that ends today, a short date and time otherwise: the reader's
 * local time, with its zone named so it reads unambiguously next to UTC times elsewhere.
 */
export const formatClaimUntil = (value: string, locale: string, now = new Date()) => {
    const until = new Date(value);
    if (Number.isNaN(until.getTime())) return null;
    const sameDay = until.toDateString() === now.toDateString();
    const time = { hour: '2-digit', minute: '2-digit', timeZoneName: 'short' } as const;
    return new Intl.DateTimeFormat(locale, sameDay ? time : { ...time, day: 'numeric', month: 'short', year: 'numeric' }).format(until);
};

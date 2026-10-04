import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { executionUsageService } from '../../services/executionUsageService';
import { QueryErrorState } from '../feedback/QueryState';
import { Button } from '../common/Button';

export const ExecutionUsagePanel = ({ scope }: { scope: { project_id?: number; iteration_id?: number; lookback_days: number } }) => {
    const { t, i18n } = useTranslation();
    const [amount, setAmount] = useState('');
    const [currency, setCurrency] = useState('');
    const [budget, setBudget] = useState<{ budget_amount?: string; budget_currency?: string }>({});
    const [inputError, setInputError] = useState(false);
    // feedback-policy: query loading,error,retry,empty
    const query = useQuery({ queryKey: ['executionUsage', scope, budget], queryFn: () => executionUsageService.get({ ...scope, ...budget }) });
    const data = query.isError ? undefined : query.data;
    const currencies = Array.from(new Set([...Object.keys(data?.provider_reported_cost ?? {}), ...Object.keys(data?.estimated_cost ?? {})])).sort();
    const value = (amount: string | null | undefined) => amount === null || amount === undefined ? t('executionUsage.unknown') : amount;
    return <section className="space-y-4 border-t border-border-subtle pt-5" aria-labelledby="execution-usage-title">
        <div><h4 id="execution-usage-title" className="font-semibold">{t('executionUsage.title')}</h4>
            <p className="mt-1 max-w-prose text-sm text-content-secondary">{t('executionUsage.description')}</p></div>
        {query.isLoading && <p role="status">{t('common.loading')}</p>}
        {query.isError && <QueryErrorState error={query.error} onRetry={() => { void query.refetch(); }} />}
        {data && <>
            <p className="text-sm text-content-secondary">{t('executionUsage.asOf', { time: new Date(data.window_end).toLocaleString(i18n.language) })}</p>
            <p className="text-sm">{t('executionUsage.coverage', { reports: data.reported_runs, attempts: data.expected_runs,
                missing: data.unreported_runs, partial: data.partial_reports, unavailable: data.unavailable_reports })}</p>
            {data.measured_report_count === 0 && <p className="text-sm text-content-secondary">{t('executionUsage.noMeasurements')}</p>}
            {currencies.length === 0 ? <p className="text-sm text-content-secondary">{t('executionUsage.noCosts')}</p> : <div className="overflow-x-auto">
                <table className="w-full text-left text-sm"><caption className="pb-2 text-left text-content-secondary">{t('executionUsage.costBasis')}</caption>
                    <thead><tr className="border-b border-border-subtle"><th className="px-3 py-2" scope="col">{t('executionUsage.currency')}</th><th className="px-3 py-2" scope="col">{t('executionUsage.reported')}</th><th className="px-3 py-2" scope="col">{t('executionUsage.estimated')}</th><th className="px-3 py-2" scope="col">{t('executionUsage.reports')}</th></tr></thead>
                    <tbody>{currencies.map(code => <tr className="border-b border-border-subtle" key={code}><th scope="row" className="px-3 py-3 font-medium">{code}</th>
                        <td className="break-all px-3 py-3 tabular-nums">{value(data.provider_reported_cost[code])}</td><td className="break-all px-3 py-3 tabular-nums">{value(data.estimated_cost[code])}</td>
                        <td className="px-3 py-3 tabular-nums">{data.known_cost_reports[code] ?? 0}</td></tr>)}</tbody>
                </table>
            </div>}
            <p className="text-sm text-content-secondary">{t('executionUsage.outcomes', { accepted: data.accepted_task_identities,
                linked: data.reports_linked_to_accepted_tasks, unknown: data.unknown_cost_reports })}</p>
            {Object.keys(data.reported_units).length > 0 && <dl className="flex flex-wrap gap-x-6 gap-y-2 text-sm">
                {Object.entries(data.reported_units).map(([unit, quantity]) => <div key={unit} className="flex items-baseline gap-2"><dt>{unit.replaceAll('_', ' ')}</dt><dd className="tabular-nums">{value(quantity)} ({data.unit_report_counts[unit] ?? 0} {t('executionUsage.reports')})</dd></div>)}
            </dl>}
            <p className="text-sm text-content-secondary">{t('executionUsage.humanEffort', { minutes: value(data.reported_human_effort_minutes), reports: data.human_effort_reports })}</p>
            {data.simulated_reports > 0 && <details className="text-sm"><summary className="cursor-pointer font-medium">{t('executionUsage.simulated', { count: data.simulated_reports })}</summary>
                <div className="mt-3 space-y-2 text-content-secondary"><p>{t('executionUsage.simulatedBasis')}</p>
                    {Object.entries(data.simulated_reported_cost).map(([code, amount]) => <p key={code}>{code}: {amount}</p>)}
                </div>
            </details>}
        </>}
            <form className="flex flex-wrap items-end gap-3" onSubmit={event => {
                event.preventDefault();
                if (amount === '') { setBudget({}); setInputError(false); return; }
                const normalized = amount.replace(',', '.');
                if (!/^[A-Z]{3}$/.test(currency) || !/^\d+(\.\d{1,6})?$/.test(normalized) || normalized.replace('.', '').length > 18) { setInputError(true); return; }
                setBudget({ budget_amount: normalized, budget_currency: currency }); setInputError(false);
            }}>
                <label className="text-sm">{t('executionUsage.budget')}<input className="mt-1 block w-36 rounded border px-2 py-1" inputMode="decimal" value={amount} onChange={event => setAmount(event.target.value)} /></label>
                <label className="text-sm">{t('executionUsage.currency')}<input className="mt-1 block w-24 rounded border px-2 py-1" maxLength={3} value={currency} onChange={event => setCurrency(event.target.value.toUpperCase())} placeholder="EUR" /></label>
                <Button type="submit" variant="secondary">{t('executionUsage.compare')}</Button>
            </form>
            {inputError && <p role="alert" className="text-sm text-feedback-danger-foreground">{t('executionUsage.budgetError')}</p>}
            {data?.advisory_budget && <p className="text-sm text-content-secondary">{t('executionUsage.advisory', {
                amount: data.advisory_budget.amount, currency: data.advisory_budget.currency,
                reported: value(data.advisory_budget.known_reported_cost), estimated: value(data.advisory_budget.known_estimated_cost) })}</p>}
    </section>;
};

import { useTranslation } from 'react-i18next';
import { Checkbox } from '../common/Checkbox';
import { Input } from '../common/Input';
import type { Constraints } from '../../types/schedulingRules';

interface Props {
    constraints: Constraints;
    onChange: (constraints: Constraints) => void;
}

export const ConstraintsPanel = ({ constraints, onChange }: Props) => {
    const { t } = useTranslation();
    const toggleConstraint = (key: keyof Omit<Constraints, 'balance_workload'>) => {
        onChange({
            ...constraints,
            [key]: !constraints[key],
        });
    };

    const toggleBalanceWorkload = (enabled: boolean) => {
        onChange({
            ...constraints,
            balance_workload: enabled
                ? { enabled: true, max_overload_percent: 10 }
                : null,
        });
    };

    const updateMaxOverload = (value: string) => {
        if (!constraints.balance_workload) return;
        onChange({
            ...constraints,
            balance_workload: {
                ...constraints.balance_workload,
                max_overload_percent: parseFloat(value) || 0,
            },
        });
    };

    const constraintItems: Array<{
        key: keyof Omit<Constraints, 'balance_workload'>;
        labelKey: string;
        helpKey: string;
    }> = [
            {
                key: 'sequential_per_assignee',
                labelKey: 'settingsScheduling.constraints.sequential_per_assignee.label',
                helpKey: 'settingsScheduling.constraints.sequential_per_assignee.help',
            },
            {
                key: 'respect_dependencies',
                labelKey: 'settingsScheduling.constraints.respect_dependencies.label',
                helpKey: 'settingsScheduling.constraints.respect_dependencies.help',
            },
            {
                key: 'min_start_date',
                labelKey: 'settingsScheduling.constraints.min_start_date.label',
                helpKey: 'settingsScheduling.constraints.min_start_date.help',
            },
            {
                key: 'max_finish_date',
                labelKey: 'settingsScheduling.constraints.max_finish_date.label',
                helpKey: 'settingsScheduling.constraints.max_finish_date.help',
            },
            {
                key: 'prefer_uninterrupted',
                labelKey: 'settingsScheduling.constraints.prefer_uninterrupted.label',
                helpKey: 'settingsScheduling.constraints.prefer_uninterrupted.help',
            },
        ];

    return (
        <div className="space-y-4">
            {/* Boolean constraints grid */}
            <div className="grid grid-cols-1 gap-4">
                {constraintItems.map(item => (
                    <div
                        key={item.key}
                        className={`
                            p-4 rounded-lg border transition-all cursor-pointer
                            ${constraints[item.key]
                                ? 'bg-action-muted border-action shadow-sm'
                                : 'bg-surface-card border-border hover:border-action'
                            }
                        `}
                    >
                        <div className="flex items-start gap-4">
                            <Checkbox
                                checked={constraints[item.key]}
                                onChange={() => toggleConstraint(item.key)}
                                className="mt-1"
                            />
                            <div>
                                <span className="font-semibold text-content-primary block mb-1">{t(item.labelKey)}</span>
                                <p className="text-sm text-content-secondary leading-relaxed">
                                    {t(item.helpKey)}
                                </p>
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {/* Balance workload (special handling) */}
            <div className="border-t border-border pt-6">
                <div
                    className={`
                        p-4 rounded-lg border transition-all
                        ${constraints.balance_workload
                            ? 'bg-action-muted border-action shadow-sm'
                            : 'bg-surface-card border-border hover:border-action'
                        }
                    `}
                >
                    <div className="flex items-start gap-4">
                        <Checkbox
                            checked={!!constraints.balance_workload}
                            onChange={toggleBalanceWorkload}
                            className="mt-1"
                        />
                        <div className="flex-1">
                            <span className="font-semibold text-content-primary block mb-1">
                                {t('settingsScheduling.constraints.balance_workload.label')}
                            </span>
                            <p className="text-sm text-content-secondary leading-relaxed">
                                {t('settingsScheduling.constraints.balance_workload.help')}
                            </p>

                            {constraints.balance_workload && (
                                <div className="mt-4 flex items-center gap-3 bg-surface-card/50 p-2 rounded border border-action w-fit">
                                    <span className="text-sm font-medium text-content-primary">{t('settingsScheduling.fields.maxAllowableOverload')}</span>
                                    <Input
                                        type="number"
                                        value={constraints.balance_workload.max_overload_percent.toString()}
                                        onChange={(e) => updateMaxOverload(e.target.value)}
                                        className="w-24"
                                        min={0}
                                        max={100}
                                    />
                                    <span className="text-sm text-content-secondary">%</span>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

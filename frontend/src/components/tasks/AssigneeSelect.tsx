import type { ComponentProps } from 'react';
import type { TaskRowAssigneeOption } from './TaskRow';

export interface AssigneeSelectProps extends Omit<ComponentProps<'select'>, 'value' | 'onChange' | 'children' | 'aria-label'> {
    /** Names the picker for assistive technology, such as "Assignee: <task title>". */
    'aria-label': string;
    /** The chosen person or agent; `null` shows the empty option. */
    value: number | null | undefined;
    options: TaskRowAssigneeOption[];
    /** The first option, which clears the assignee (the list says Unassigned, the board's dialog asks to choose). */
    emptyLabel: string;
    onChange: (assigneeId: number | null) => void;
}

/**
 * The one assignee picker: the list row and the board's assign-on-drop dialog both use it, so
 * the people and agents offered, and the way one is chosen, are the same everywhere.
 */
export const AssigneeSelect = ({ value, options, emptyLabel, onChange, 'aria-label': ariaLabel, ...selectProps }: AssigneeSelectProps) => (
    <select
        {...selectProps}
        aria-label={ariaLabel}
        value={value ?? ''}
        onChange={event => onChange(event.target.value === '' ? null : Number(event.target.value))}
    >
        <option value="">{emptyLabel}</option>
        {options.map(option => <option key={option.id} value={option.id}>{option.name}</option>)}
    </select>
);

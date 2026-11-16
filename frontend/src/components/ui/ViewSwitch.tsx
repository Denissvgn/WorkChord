import { SegmentedControl, type SegmentedOption } from './SegmentedControl';

/**
 * Switches between views of the same records, such as a list and a board.
 *
 * Usage: give the group an accessible `label`, two to four `options` and the
 * current `value`. Each option is a button with a pressed state; the arrow keys
 * move to the neighbouring view and show it. Put it in the `viewSwitch` slot of
 * PageToolbar. Do not use it to move between different pages or record types.
 */
export const ViewSwitch = <T extends string,>({ label, options, value, onChange, className }: {
    label: string;
    options: SegmentedOption<T>[];
    value: T;
    onChange: (value: T) => void;
    className?: string;
}) => (
    <SegmentedControl arrowKeys label={label} options={options} value={value} onChange={onChange} className={className} />
);

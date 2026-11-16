import { useEffect, useId, useMemo, useRef, useState } from 'react';
import type { KeyboardEvent as ReactKeyboardEvent, ReactNode } from 'react';
import { ChevronDown } from 'lucide-react';
import clsx from 'clsx';

export interface ScopePickerOption {
    /** Identifies the option; unique within one picker. */
    key: string;
    /** The text announced and matched by search. */
    label: string;
    /** Secondary text shown after the label, for example dates. */
    detail?: string;
    /** A short marker shown beside the label. */
    marker?: string;
    /** Extra words that search also matches. */
    keywords?: string;
    /** Options with the same group are listed under one heading. */
    group?: string;
    /** Actions run when chosen and are not a value of the picker. */
    action?: boolean;
    selected?: boolean;
}

interface ScopePickerProps {
    label: string;
    /** What the closed picker shows and announces as its value. */
    valueLabel: string;
    options: readonly ScopePickerOption[];
    onChoose: (option: ScopePickerOption) => void;
    searchHint: string;
    noMatches: string;
    disabled?: boolean;
    className?: string;
    renderOption?: (option: ScopePickerOption) => ReactNode;
}

const normalized = (value: string) => value.toLocaleLowerCase().normalize('NFKD').replace(/\p{M}/gu, '');

/**
 * A combobox with a list that opens below it. Closed, it shows its value; open, the same
 * field takes the search text. Arrow keys move through the list, Enter chooses, Escape
 * closes without choosing, and Tab leaves.
 */
export const ScopePicker = ({
    label,
    valueLabel,
    options,
    onChoose,
    searchHint,
    noMatches,
    disabled = false,
    className,
    renderOption,
}: ScopePickerProps) => {
    const baseId = useId();
    const listId = `${baseId}-list`;
    const containerRef = useRef<HTMLDivElement>(null);
    const inputRef = useRef<HTMLInputElement>(null);
    const popupRef = useRef<HTMLDivElement>(null);
    const [open, setOpen] = useState(false);
    const [query, setQuery] = useState('');
    const [activeKey, setActiveKey] = useState<string | null>(null);

    const visible = useMemo(() => {
        const needle = normalized(query.trim());
        if (needle === '') return options;
        // Actions stay listed so a search that finds nothing can still lead to one.
        return options.filter(option => (
            option.action || normalized(`${option.label} ${option.keywords ?? ''} ${option.group ?? ''}`).includes(needle)
        ));
    }, [options, query]);

    const activeOption = visible.find(option => option.key === activeKey) ?? null;
    const optionId = (key: string) => `${baseId}-option-${key.replace(/[^a-zA-Z0-9_-]/g, '_')}`;

    const openList = () => {
        if (disabled || open) return;
        setQuery('');
        setActiveKey(options.find(option => option.selected)?.key ?? options[0]?.key ?? null);
        setOpen(true);
    };

    const closeList = () => {
        setOpen(false);
        setQuery('');
    };

    // The active option follows the search: the first match is active, so Enter chooses it.
    const changeQuery = (next: string) => {
        setQuery(next);
        setOpen(true);
        const needle = normalized(next.trim());
        const first = needle === ''
            ? options.find(option => option.selected) ?? options[0]
            : options.find(option => !option.action && normalized(`${option.label} ${option.keywords ?? ''} ${option.group ?? ''}`).includes(needle));
        setActiveKey((first ?? null)?.key ?? null);
    };

    const choose = (option: ScopePickerOption) => {
        closeList();
        onChoose(option);
    };

    const move = (step: 1 | -1 | 'first' | 'last') => {
        if (visible.length === 0) return;
        const index = visible.findIndex(option => option.key === activeKey);
        let next: number;
        if (step === 'first') next = 0;
        else if (step === 'last') next = visible.length - 1;
        else next = index === -1 ? (step === 1 ? 0 : visible.length - 1) : (index + step + visible.length) % visible.length;
        setActiveKey(visible[next]!.key);
    };

    const handleKeyDown = (event: ReactKeyboardEvent<HTMLInputElement>) => {
        switch (event.key) {
            case 'ArrowDown':
                event.preventDefault();
                if (!open) openList(); else move(1);
                break;
            case 'ArrowUp':
                event.preventDefault();
                if (!open) openList(); else move(-1);
                break;
            case 'Home':
                if (open) { event.preventDefault(); move('first'); }
                break;
            case 'End':
                if (open) { event.preventDefault(); move('last'); }
                break;
            case 'Enter':
                if (open) {
                    event.preventDefault();
                    if (activeOption) choose(activeOption);
                } else {
                    event.preventDefault();
                    openList();
                }
                break;
            case 'Escape':
                if (open) {
                    event.preventDefault();
                    event.stopPropagation();
                    closeList();
                }
                break;
            case 'Tab':
                if (open) closeList();
                break;
            default:
        }
    };

    useEffect(() => {
        if (!open) return undefined;
        const closeOnOutsidePress = (event: MouseEvent) => {
            if (!containerRef.current?.contains(event.target as Node)) closeList();
        };
        document.addEventListener('mousedown', closeOnOutsidePress);
        return () => document.removeEventListener('mousedown', closeOnOutsidePress);
    }, [open]);

    // Pressing inside the list, including its scrollbar, keeps focus in the field.
    useEffect(() => {
        const popup = popupRef.current;
        if (!open || !popup) return undefined;
        const keepFocus = (event: MouseEvent) => event.preventDefault();
        popup.addEventListener('mousedown', keepFocus);
        return () => popup.removeEventListener('mousedown', keepFocus);
    }, [open]);

    useEffect(() => {
        if (!open || !activeKey) return;
        document.getElementById(optionId(activeKey))?.scrollIntoView?.({ block: 'nearest' });
        // optionId only depends on baseId.
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [activeKey, open]);

    const groups = useMemo(() => {
        const result: Array<{ name: string | null; options: ScopePickerOption[] }> = [];
        for (const option of visible) {
            const name = option.group ?? null;
            const last = result[result.length - 1];
            if (last && last.name === name) last.options.push(option);
            else result.push({ name, options: [option] });
        }
        return result;
    }, [visible]);

    return (
        <div ref={containerRef} className={clsx('scope-picker', className)} data-open={open || undefined}>
            <label className="scope-picker-label" htmlFor={`${baseId}-input`}>{label}</label>
            <div className="scope-picker-field">
                <input
                    ref={inputRef}
                    id={`${baseId}-input`}
                    type="text"
                    role="combobox"
                    className="scope-picker-input"
                    aria-expanded={open}
                    aria-controls={listId}
                    aria-haspopup="listbox"
                    aria-autocomplete="list"
                    aria-activedescendant={open && activeOption ? optionId(activeOption.key) : undefined}
                    autoComplete="off"
                    spellCheck={false}
                    disabled={disabled}
                    value={open ? query : valueLabel}
                    placeholder={open ? searchHint : undefined}
                    title={valueLabel}
                    onChange={event => changeQuery(event.target.value)}
                    onKeyDown={handleKeyDown}
                    onClick={() => { if (open) closeList(); else openList(); }}
                    onBlur={event => {
                        if (!containerRef.current?.contains(event.relatedTarget as Node | null)) closeList();
                    }}
                />
                <ChevronDown aria-hidden="true" className="scope-picker-chevron h-4 w-4" />
            </div>
            {open && (
                <div ref={popupRef} className="scope-picker-popup">
                    <div id={listId} role="listbox" aria-label={label} className="scope-picker-list">
                        {visible.length === 0 && <p className="scope-picker-empty" role="status">{noMatches}</p>}
                        {groups.map((group, groupIndex) => {
                            const rows = group.options.map(option => (
                                <button
                                    key={option.key}
                                    id={optionId(option.key)}
                                    type="button"
                                    role="option"
                                    tabIndex={-1}
                                    aria-selected={option.selected === true}
                                    className={clsx('scope-picker-option', option.action && 'scope-picker-action')}
                                    data-active={option.key === activeKey || undefined}
                                    data-selected={option.selected || undefined}
                                    onMouseEnter={() => setActiveKey(option.key)}
                                    onClick={() => choose(option)}
                                >
                                    {renderOption ? renderOption(option) : (
                                        <>
                                            <span className="scope-picker-option-label">{option.label}</span>
                                            {option.marker && <span className="scope-picker-marker">{option.marker}</span>}
                                            {option.detail && <span className="scope-picker-detail">{option.detail}</span>}
                                        </>
                                    )}
                                </button>
                            ));
                            return group.name === null ? (
                                <div key={`group-${groupIndex}`} role="presentation" className={clsx(groupIndex > 0 && 'scope-picker-rule')}>{rows}</div>
                            ) : (
                                <div key={group.name} role="group" aria-label={group.name}>
                                    <p className="scope-picker-group" aria-hidden="true">{group.name}</p>
                                    {rows}
                                </div>
                            );
                        })}
                    </div>
                </div>
            )}
        </div>
    );
};

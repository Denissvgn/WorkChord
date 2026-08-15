import { afterEach, describe, expect, it } from 'vitest';
import { captureFocusOrigin, focusOwnedTarget } from './focusLifecycle';

const appendButton = (label: string) => {
    const button = document.createElement('button');
    button.textContent = label;
    document.body.append(button);
    return button;
};

describe('focus lifecycle ownership', () => {
    afterEach(() => {
        document.body.replaceChildren();
    });

    it('moves focus only while the initiating control still owns it', () => {
        const origin = appendButton('Start');
        const target = appendButton('Result');
        origin.focus();

        expect(captureFocusOrigin()).toBe(origin);
        expect(focusOwnedTarget(origin, target)).toBe(true);
        expect(target).toHaveFocus();
    });

    it('does not steal focus after the operator moves elsewhere', () => {
        const origin = appendButton('Start');
        const target = appendButton('Result');
        const elsewhere = appendButton('Elsewhere');
        origin.focus();
        elsewhere.focus();

        expect(focusOwnedTarget(origin, target)).toBe(false);
        expect(elsewhere).toHaveFocus();
    });

    it('recovers focus when a pending control is removed or disabled', () => {
        const removedOrigin = appendButton('Removed start');
        const removedTarget = appendButton('Removed result');
        removedOrigin.focus();
        removedOrigin.remove();

        expect(focusOwnedTarget(removedOrigin, removedTarget)).toBe(true);
        expect(removedTarget).toHaveFocus();

        const disabledOrigin = appendButton('Disabled start');
        const disabledTarget = appendButton('Disabled result');
        disabledOrigin.focus();
        disabledOrigin.disabled = true;
        document.body.focus();

        expect(focusOwnedTarget(disabledOrigin, disabledTarget)).toBe(true);
        expect(disabledTarget).toHaveFocus();
    });

    it('keeps an owned request pending when its target is not mounted', () => {
        const origin = appendButton('Start');
        origin.focus();

        expect(focusOwnedTarget(origin, null)).toBe(false);
        expect(origin).toHaveFocus();
    });
});

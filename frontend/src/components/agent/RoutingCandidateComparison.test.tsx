import { screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import i18n from '../../i18n/i18n';
import {
    eligibleRoutingCandidate,
    modelAwareRoutingPreview,
    modelAwareRoutingRoster,
} from '../../test/fixtures/modelAwareRouting';
import { renderWithProviders } from '../../test/renderWithProviders';
import { RoutingCandidateComparison } from './RoutingCandidateComparison';

const secretSentinels = [
    'sk-live-provider-secret',
    'Bearer internal-routing-token',
    'private-credential-material',
];

const previewWithSecretSentinels = {
    ...modelAwareRoutingPreview,
    provider_api_key: secretSentinels[0],
    eligible_candidates: modelAwareRoutingPreview.eligible_candidates.map(candidate => ({
        ...candidate,
        provider_authorization: secretSentinels[1],
    })),
    exclusions: modelAwareRoutingPreview.exclusions.map(exclusion => ({
        ...exclusion,
        provider_credentials: secretSentinels[2],
    })),
};

describe('RoutingCandidateComparison', () => {
    it('distinguishes eligible and excluded results without selecting or leaking secrets', () => {
        const onSelectCandidate = vi.fn();

        renderWithProviders(
            <RoutingCandidateComparison
                preview={previewWithSecretSentinels}
                roster={modelAwareRoutingRoster}
                selectedCandidateKey={null}
                onSelectCandidate={onSelectCandidate}
            />,
        );

        const eligibleText = i18n.t('taskRouting.eligible');
        const excludedText = i18n.t('taskRouting.excluded');
        expect(eligibleText).not.toBe(excludedText);
        expect(screen.getByText(eligibleText)).toBeVisible();
        expect(screen.getByText(excludedText)).toBeVisible();

        expect(screen.getByRole('radio')).not.toBeChecked();
        expect(onSelectCandidate).not.toHaveBeenCalled();

        for (const secret of secretSentinels) {
            expect(document.body).not.toHaveTextContent(secret);
        }
    });

    it('selects an eligible candidate from the keyboard', async () => {
        const onSelectCandidate = vi.fn();
        const { user } = renderWithProviders(
            <RoutingCandidateComparison
                preview={modelAwareRoutingPreview}
                roster={modelAwareRoutingRoster}
                selectedCandidateKey={null}
                onSelectCandidate={onSelectCandidate}
            />,
        );

        const radio = screen.getByRole('radio');
        radio.focus();
        await user.keyboard('[Space]');

        expect(onSelectCandidate).toHaveBeenCalledOnce();
        expect(onSelectCandidate).toHaveBeenCalledWith(eligibleRoutingCandidate);
    });

    it('selects an eligible candidate with a pointer click', async () => {
        const onSelectCandidate = vi.fn();
        const { user } = renderWithProviders(
            <RoutingCandidateComparison
                preview={modelAwareRoutingPreview}
                roster={modelAwareRoutingRoster}
                selectedCandidateKey={null}
                onSelectCandidate={onSelectCandidate}
            />,
        );

        await user.click(screen.getByRole('radio'));

        expect(onSelectCandidate).toHaveBeenCalledOnce();
        expect(onSelectCandidate).toHaveBeenCalledWith(eligibleRoutingCandidate);
    });
});

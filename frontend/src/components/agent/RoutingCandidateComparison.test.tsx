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

    it('marks a local-first candidate beside its cost tier', () => {
        renderWithProviders(
            <RoutingCandidateComparison
                preview={{
                    ...modelAwareRoutingPreview,
                    eligible_candidates: modelAwareRoutingPreview.eligible_candidates.map(candidate => ({ ...candidate, local_first: true })),
                }}
                roster={modelAwareRoutingRoster}
                selectedCandidateKey={null}
                onSelectCandidate={vi.fn()}
            />,
        );

        expect(screen.getByText(/\(Local or free model\)/)).toBeVisible();
    });

    it('shows the effort of an eligible candidate and of an excluded one', () => {
        renderWithProviders(
            <RoutingCandidateComparison
                preview={{
                    ...modelAwareRoutingPreview,
                    eligible_candidates: modelAwareRoutingPreview.eligible_candidates.map(candidate => ({ ...candidate, effort: 'xhigh' })),
                    exclusions: modelAwareRoutingPreview.exclusions.map(exclusion => ({
                        ...exclusion,
                        effort: 'low',
                        hard_blocker_codes: ['model_effort_insufficient'],
                    })),
                }}
                roster={modelAwareRoutingRoster}
                selectedCandidateKey={null}
                onSelectCandidate={vi.fn()}
            />,
        );

        expect(screen.getByText(/Extra high/)).toBeVisible();
        expect(screen.getByText('Model Effort Insufficient')).toBeVisible();
        expect(screen.getByText('Low', { selector: 'dd' })).toBeVisible();
    });

    it('names the qualification keys a candidate holds and the ones an exclusion lacks', () => {
        renderWithProviders(
            <RoutingCandidateComparison
                preview={{
                    ...modelAwareRoutingPreview,
                    eligible_candidates: modelAwareRoutingPreview.eligible_candidates.map(candidate => ({ ...candidate, qualification_keys: ['qualified.schema-review'] })),
                    exclusions: modelAwareRoutingPreview.exclusions.map(exclusion => ({
                        ...exclusion,
                        hard_blocker_codes: ['model_qualification_missing'],
                        missing_qualification_keys: ['qualified.migrations'],
                    })),
                }}
                roster={modelAwareRoutingRoster}
                selectedCandidateKey={null}
                onSelectCandidate={vi.fn()}
            />,
        );

        expect(screen.getByText('Qualification keys held')).toBeVisible();
        expect(screen.getAllByText('qualified.schema-review')[0]).toBeVisible();
        expect(screen.getByText('Missing qualification keys')).toBeVisible();
        expect(screen.getAllByText('qualified.migrations')[0]).toBeVisible();
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

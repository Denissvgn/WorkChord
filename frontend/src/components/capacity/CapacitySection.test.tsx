import { screen } from '@testing-library/react';
import { it, expect, vi } from 'vitest';
import { renderWithProviders } from '../../test/renderWithProviders';
import type { Iteration } from '../../types/iteration';
import { CapacitySection } from './CapacitySection';

vi.mock('./TeamList', () => ({ TeamList: () => <div>Capacity rows with time off</div> }));
vi.mock('./PlanQuickAddCapacity', () => ({ PlanQuickAddCapacity: () => null }));
vi.mock('../team/VacationCsvImport', () => ({ VacationCsvImport: ({ iterationId }: { iterationId: number }) => <div>Import time off for {iterationId}</div> }));

it('offers vacation CSV import in the capacity overflow', async () => {
    const iteration = { id: 9, start_date: '2026-01-01', end_date: '2026-01-31' } as Iteration;
    const view = renderWithProviders(<CapacitySection iteration={iteration} iterations={[iteration]} members={[]} primary />);
    expect(screen.getByText('Capacity rows with time off')).toBeInTheDocument();
    await view.user.click(screen.getByRole('button', { name: /capacity actions/i }));
    await view.user.click(screen.getByRole('menuitem', { name: /import.*csv/i }));
    expect(screen.getByText('Import time off for 9')).toBeInTheDocument();
});

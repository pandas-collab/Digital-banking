import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { LedgerTable } from '../components/shared/LedgerTable';

const mockData = [
  {
    ledger_id: 1,
    event_type: 'transfer',
    account_id: 42,
    amount: 1500,
    balance_snapshot: 2500,
    metadata: { currency: 'USD' },
    created_at: '2024-04-12T19:25:00Z',
  },
  {
    ledger_id: 2,
    event_type: 'policy_payment',
    account_id: 42,
    amount: 500,
    balance_snapshot: 2000,
    metadata: {},
    created_at: '2024-04-13T11:00:00Z',
  },
];

global.fetch = vi.fn().mockResolvedValue({
  ok: true,
  json: async () => mockData,
});

describe('LedgerTable', () => {
  it('renders ledger rows', async () => {
    render(<LedgerTable accountId={42} />);
    expect(await screen.findByText('Transfer')).toBeInTheDocument();
    expect(await screen.findByText('Policy Payment')).toBeInTheDocument();
    expect(screen.getAllByRole('row').length).toBeGreaterThan(2);
  });
});

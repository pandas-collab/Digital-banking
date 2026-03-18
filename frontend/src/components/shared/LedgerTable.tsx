import React, { useState } from 'react';
import { useLedger } from '../../hooks/useLedger';

// simple currency formatter, safe for decimals
function formatCurrency(value: number): string {
  return value.toLocaleString('en-US', { style: 'currency', currency: 'USD' });
}

function titleCase(str: string): string {
  return str.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
}

interface Props {
  accountId: number | null;
}

export function LedgerTable({ accountId }: Props) {
  const { ledger, loading, error } = useLedger(accountId);

  const [expanded, setExpanded] = useState<number | null>(null);

  if (error) return <div style={{ color: 'red' }}>Error: {error}</div>;
  if (loading) return <div>Loading ledger...</div>;

  return (
    <table style={{ borderCollapse: 'collapse', width: '100%' }}>
      <thead>
        <tr>
          <th style={{ textAlign: 'left', borderBottom: '1px solid #ccc' }}>Date</th>
          <th style={{ textAlign: 'left', borderBottom: '1px solid #ccc' }}>Type</th>
          <th style={{ textAlign: 'right', borderBottom: '1px solid #ccc' }}>Amount</th>
          <th style={{ textAlign: 'right', borderBottom: '1px solid #ccc' }}>Running Balance</th>
        </tr>
      </thead>
      <tbody>
        {ledger.map((row) => (
          <React.Fragment key={row.ledger_id}>
            <tr
              onClick={() => setExpanded(row.ledger_id === expanded ? null : row.ledger_id)}
              style={{ cursor: 'pointer' }}
            >
              <td>{new Date(row.created_at).toLocaleString()}</td>
              <td>{titleCase(row.event_type)}</td>
              <td style={{ textAlign: 'right' }}>{formatCurrency(row.amount)}</td>
              <td style={{ textAlign: 'right' }}>{formatCurrency(row.balance_snapshot)}</td>
            </tr>
            {expanded === row.ledger_id && (
              <tr>
                <td colSpan={4}>
                  <pre style={{ margin: 0, padding: '.5rem', background: '#f7f7f7', fontSize: '0.8rem' }}>
                    {JSON.stringify(row.metadata, null, 2)}
                  </pre>
                </td>
              </tr>
            )}
          </React.Fragment>
        ))}
      </tbody>
    </table>
  );
}

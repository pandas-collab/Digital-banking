import React from 'react';
import { useTransfers } from '../hooks/useTransfers';

export const TransferHistory: React.FC = () => {
  const [page, setPage] = React.useState(1);
  const [size] = React.useState(10);

  const { data, isLoading, error } = useTransfers(page, size);

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error loading transfers</div>;
  if (!data?.data.length) return <div>No transfers found</div>;

  return (
    <div style={{ padding: '20px' }}>
      <h2>Transfer History</h2>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th style={{ border: '1px solid #ddd', padding: '8px' }}>From</th>
            <th style={{ border: '1px solid #ddd', padding: '8px' }}>To</th>
            <th style={{ border: '1px solid #ddd', padding: '8px' }}>Amount</th>
            <th style={{ border: '1px solid #ddd', padding: '8px' }}>Status</th>
            <th style={{ border: '1px solid #ddd', padding: '8px' }}>Date</th>
          </tr>
        </thead>
        <tbody>
          {data.data.map((transfer) => (
            <tr key={transfer.id}>
              <td style={{ border: '1px solid #ddd', padding: '8px' }}>
                {transfer.fromAccount.substring(0, 8)}...
              </td>
              <td style={{ border: '1px solid #ddd', padding: '8px' }}>
                {transfer.toAccount.substring(0, 8)}...
              </td>
              <td style={{ border: '1px solid #ddd', padding: '8px' }}>
                ${transfer.amount.toFixed(2)}
              </td>
              <td style={{ border: '1px solid #ddd', padding: '8px' }}>
                {transfer.status}
              </td>
              <td style={{ border: '1px solid #ddd', padding: '8px' }}>
                {new Date(transfer.createdAt).toLocaleDateString()}
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <div style={{ marginTop: '20px', display: 'flex', gap: '10px', justifyContent: 'center' }}>
        <button
          onClick={() => setPage(Math.max(1, page - 1))}
          disabled={page <= 1}
        >
          Previous
        </button>
        <span>Page {page} of {Math.ceil(data.total / size)}</span>
        <button
          onClick={() => setPage(Math.min(Math.ceil(data.total / size), page + 1))}
          disabled={page >= Math.ceil(data.total / size)}
        >
          Next
        </button>
      </div>
    </div>
  );
};

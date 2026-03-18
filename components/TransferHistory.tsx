import React, { useState, useEffect } from 'react';

interface Transaction {
  id: string;
  from_account: string;
  to_account: string;
  amount: number;
  description: string;
  timestamp: string;
}

const TransferHistory: React.FC = () => {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedAccount, setSelectedAccount] = useState('ACC001');

  const fetchHistory = async (account: string) => {
    setLoading(true);
    setError(null);

    const maxRetries = 3;
    let attempt = 0;

    while (attempt < maxRetries) {
      try {
        const response = await fetch(`http://localhost:8000/api/transfers/${account}`);
        if (!response.ok) throw new Error('Failed to fetch history');

        const data = await response.json();
        setTransactions(data);
        break;

      } catch (err: any) {
        attempt++;
        if (attempt >= maxRetries) {
          setError(err.message || 'Failed to fetch transfer history');
        } else {
          await new Promise(resolve => setTimeout(resolve, 1000 * attempt));
        }
      }
    }

    setLoading(false);
  };

  useEffect(() => {
    fetchHistory(selectedAccount);
  }, [selectedAccount]);

  return (
    <div className="transfer-history">
      <h2>Transfer History</h2>

      <select
        value={selectedAccount}
        onChange={(e) => setSelectedAccount(e.target.value)}
        disabled={loading}
      >
        <option value="ACC001">ACC001</option>
        <option value="ACC002">ACC002</option>
        <option value="ACC003">ACC003</option>
      </select>

      {error && <div className="error-message">{error}</div>}

      {loading ? (
        <div>Loading...</div>
      ) : transactions.length === 0 ? (
        <div>No transfers found</div>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>From</th>
              <th>To</th>
              <th>Amount</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map((tx) => (
              <tr key={tx.id}>
                <td>{new Date(tx.timestamp).toLocaleString()}</td>
                <td>{tx.from_account}</td>
                <td>{tx.to_account}</td>
                <td>${tx.amount.toFixed(2)}</td>
                <td>{tx.description || '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default TransferHistory;

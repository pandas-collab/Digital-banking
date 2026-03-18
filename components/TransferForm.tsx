import React, { useState, useEffect } from 'react';
import './TransferForm.module.css';

interface TransferRequest {
  from_account: string;
  to_account: string;
  amount: number;
  description: string;
}

interface TransferResponse {
  success: boolean;
  transaction_id: string;
  message: string;
}

const TransferForm: React.FC = () => {
  const [accounts, setAccounts] = useState<string[]>([]);
  const [formData, setFormData] = useState<TransferRequest>({
    from_account: '',
    to_account: '',
    amount: 0,
    description: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  useEffect(() => {
    fetchAccounts();
  }, []);

  const fetchAccounts = async () => {
    try {
      const accounts = ['ACC001', 'ACC002', 'ACC003'];
      setAccounts(accounts);
      setFormData(prev => ({ ...prev, from_account: accounts[0] || '' }));
    } catch (err) {
      setError('Failed to fetch accounts');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(null);

    const maxRetries = 3;
    let attempt = 0;

    while (attempt < maxRetries) {
      try {
        const response = await fetch('http://localhost:8000/api/transfers', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(formData),
        });

        if (!response.ok) {
          const data = await response.json();
          throw new Error(data.detail || 'Transfer failed');
        }

        const result: TransferResponse = await response.json();
        setSuccess(result.message);

        // Reset form
        setFormData({
          from_account: accounts[0] || '',
          to_account: '',
          amount: 0,
          description: ''
        });

        break; // Success

      } catch (err: any) {
        attempt++;
        if (attempt >= maxRetries) {
          setError(err.message || 'Failed to process transfer. Please try again.');
        } else {
          // Exponential backoff
          await new Promise(resolve => setTimeout(resolve, 1000 * attempt));
        }
      }
    }

    setLoading(false);
  };

  return (
    <div className="transfer-form">
      <h2>Transfer Funds</h2>

      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>From Account</label>
          <select
            value={formData.from_account}
            onChange={(e) => setFormData({...formData, from_account: e.target.value})}
            disabled={loading}
          >
            {accounts.map(acc => (
              <option key={acc} value={acc}>{acc}</option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label>To Account</label>
          <select
            value={formData.to_account}
            onChange={(e) => setFormData({...formData, to_account: e.target.value})}
            disabled={loading}
            required
          >
            <option value="">Select destination</option>
            {accounts.filter(acc => acc !== formData.from_account).map(acc => (
              <option key={acc} value={acc}>{acc}</option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label>Amount</label>
          <input
            type="number"
            step="0.01"
            min="0.01"
            max="1000"
            value={formData.amount}
            onChange={(e) => setFormData({...formData, amount: parseFloat(e.target.value) || 0})}
            disabled={loading}
            required
          />
          <small>Daily limit: $1,000</small>
        </div>

        <div className="form-group">
          <label>Description (optional)</label>
          <input
            type="text"
            value={formData.description}
            onChange={(e) => setFormData({...formData, description: e.target.value.slice(0, 200)})}
            disabled={loading}
            placeholder="Transfer description"
          />
        </div>

        <button type="submit" disabled={loading || !formData.to_account || formData.amount <= 0}>
          {loading ? 'Processing...' : 'Transfer Funds'}
        </button>
      </form>
    </div>
  );
};

export default TransferForm;

import React, { useState } from 'react';
import { useCreateTransfer } from '../hooks/useTransfers';
import { CreateTransferRequest } from '../types/transfer.types';

interface TransferFormProps {
  accounts: Array<{ id: string; balance: number }>;
  onSuccess?: () => void;
}

export const TransferForm: React.FC<TransferFormProps> = ({ accounts, onSuccess }) => {
  const [formData, setFormData] = useState<CreateTransferRequest>({
    fromAccount: '',
    toAccount: '',
    amount: 0,
  });

  const createTransfer = useCreateTransfer();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (formData.fromAccount === formData.toAccount) {
      alert('Cannot transfer to the same account');
      return;
    }

    if (formData.amount <= 0) {
      alert('Amount must be greater than 0');
      return;
    }

    try {
      await createTransfer.mutateAsync(formData);
      onSuccess?.();
      setFormData({ fromAccount: '', toAccount: '', amount: 0 });
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Transfer failed');
    }
  };

  return (
    <div style={{ maxWidth: '500px', margin: '0 auto', padding: '20px' }}>
      <h2>Transfer Funds</h2>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '1rem' }}>
          <label>From Account:</label>
          <select
            value={formData.fromAccount}
            onChange={(e) => setFormData({ ...formData, fromAccount: e.target.value })}
            required
            style={{ width: '100%', padding: '8px', marginTop: '4px' }}
          >
            <option value="">Select account</option>
            {accounts.map(account => (
              <option key={account.id} value={account.id}>
                {account.id} - Balance: ${account.balance.toFixed(2)}
              </option>
            ))}
          </select>
        </div>

        <div style={{ marginBottom: '1rem' }}>
          <label>To Account:</label>
          <select
            value={formData.toAccount}
            onChange={(e) => setFormData({ ...formData, toAccount: e.target.value })}
            required
            style={{ width: '100%', padding: '8px', marginTop: '4px' }}
          >
            <option value="">Select account</option>
            {accounts.map(account => (
              <option key={account.id} value={account.id}>
                {account.id} - Balance: ${account.balance.toFixed(2)}
              </option>
            ))}
          </select>
        </div>

        <div style={{ marginBottom: '1rem' }}>
          <label>Amount:</label>
          <input
            type="number"
            step="0.01"
            min="0.01"
            value={formData.amount}
            onChange={(e) => setFormData({ ...formData, amount: parseFloat(e.target.value) })}
            required
            style={{ width: '100%', padding: '8px', marginTop: '4px' }}
          />
        </div>

        <button
          type="submit"
          disabled={createTransfer.isPending}
          style={{
            width: '100%',
            padding: '10px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: createTransfer.isPending ? 'not-allowed' : 'pointer'
          }}
        >
          {createTransfer.isPending ? 'Processing...' : 'Transfer'}
        </button>
      </form>
    </div>
  );
};
